"""Cliente modular: bloques 12 a 14. Sin llamadas de red al importar."""
import math
import random
import time

import requests
from src.consumir_gemini import armar_peticion, extraer_texto

# Standard de pago, USD por millón; consulta 2026-11-25.
# https://ai.google.dev/gemini-api/docs/pricing
PRECIO_ENTRADA = 0.30
PRECIO_SALIDA = 2.50
costo_total_sesion = 0.0


def enviar_peticion(url, encabezados, cuerpo):
    """Traduce fallos transitorios a TimeoutError y configuración a ValueError."""
    try:
        respuesta = requests.post(url, headers=encabezados, json=cuerpo, timeout=(10,90), allow_redirects=False)
    except (requests.Timeout, requests.ConnectionError):
        raise TimeoutError("No se pudo contactar al proveedor temporalmente.") from None
    if respuesta.status_code in (400,401,403):
        raise ValueError("Credencial inválida, sin permiso o petición incorrecta; revisa configuración y esquema.")
    if respuesta.status_code == 429 or respuesta.status_code >= 500:
        raise TimeoutError("El proveedor alcanzó un límite de uso o no está disponible temporalmente.")
    if respuesta.status_code != 200:
        raise RuntimeError(f"El proveedor rechazó la petición: HTTP {respuesta.status_code}.")
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("El proveedor no devolvió JSON válido.") from None


def con_reintento(funcion, intentos=3, espera_base=2, espera_maxima=30):
    """Reintenta solo fallos temporales, con backoff acotado y jitter."""
    if type(intentos) is not int or intentos < 1 or any(not math.isfinite(v) or v < 0 for v in (espera_base, espera_maxima)):
        raise ValueError("Los intentos deben ser positivos y las esperas finitas no negativas.")
    for intento in range(intentos):
        try:
            return funcion()
        except TimeoutError:
            if intento == intentos - 1:
                raise
            espera = min(espera_base * 2**intento, espera_maxima)
            time.sleep(min(espera + random.uniform(0, espera * .1), espera_maxima))


def registrar_costo(respuesta, precio_entrada=PRECIO_ENTRADA, precio_salida=PRECIO_SALIDA):
    """Acumula el equivalente Standard; no afirma un cobro a la cuenta."""
    global costo_total_sesion
    uso = respuesta.get("usageMetadata", {})
    entrada, salida = uso.get("promptTokenCount"), uso.get("candidatesTokenCount")
    pensamiento = uso.get("thoughtsTokenCount", 0)
    if any(type(t) is not int or t < 0 for t in (entrada, salida, pensamiento)):
        raise ValueError("No hay contadores de tokens válidos para estimar el costo.")
    if any(not math.isfinite(p) or p < 0 for p in (precio_entrada, precio_salida)):
        raise ValueError("Las tarifas deben ser finitas y no negativas.")
    costo = (entrada * precio_entrada + (salida + pensamiento) * precio_salida) / 1_000_000
    costo_total_sesion += costo
    return costo


def consultar_modelo(pregunta, system_instruction=None, response_schema=None):
    """Entrada pública; selecciona tarifas solo para el modelo verificado."""
    url, encabezados, cuerpo = armar_peticion(pregunta, system_instruction or None, response_schema)
    if "/gemini-3.5-flash-lite:" not in url:
        raise ValueError("Configura las tarifas antes de utilizar otro modelo en este cliente.")
    try:
        respuesta = con_reintento(lambda: enviar_peticion(url, encabezados, cuerpo))
    except TimeoutError:
        raise RuntimeError("El servicio no respondió tras varios intentos. Intenta más tarde.") from None
    texto = extraer_texto(respuesta)
    registrar_costo(respuesta)
    return texto
