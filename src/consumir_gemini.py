"""Primer módulo de Gemini: preparar, enviar, extraer y coordinar."""
import argparse
import os
from pathlib import Path
import re
import sys

from dotenv import load_dotenv
import requests


def armar_peticion(pregunta):
    """Valida la entrada y prepara la petición sin realizar llamadas de red."""
    if not isinstance(pregunta, str) or not pregunta.strip():
        raise ValueError("La pregunta debe ser un texto no vacío.")

    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
    clave = (os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY") or "").strip()
    if not clave:
        raise ValueError("Configura API_KEY o GEMINI_API_KEY en tu archivo .env.")
    modelo = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", modelo):
        raise ValueError("GEMINI_MODEL debe contener solamente el nombre del modelo.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"
    encabezados = {"Content-Type": "application/json", "x-goog-api-key": clave}
    cuerpo = {"contents": [{"parts": [{"text": pregunta.strip()}]}]}
    return url, encabezados, cuerpo


def enviar_peticion(url, encabezados, cuerpo):
    """Envía el POST y convierte errores de transporte, HTTP y JSON."""
    try:
        respuesta = requests.post(
            url, headers=encabezados, json=cuerpo,
            timeout=(10, 90), allow_redirects=False,
        )
        respuesta.raise_for_status()
    except requests.Timeout:
        raise RuntimeError("Gemini superó el tiempo de espera. Intenta nuevamente.") from None
    except requests.ConnectionError:
        raise RuntimeError("No se pudo conectar con Gemini. Revisa tu conexión a internet.") from None
    except requests.HTTPError as error:
        estado = error.response.status_code
        if estado in (400, 401, 403):
            detalle = "Revisa la petición, la credencial y los permisos del proyecto."
        elif estado == 429:
            detalle = "Se alcanzó el límite de solicitudes o cuota. Revisa tu cuota y espera."
        elif estado == 404:
            detalle = "Revisa que el modelo configurado esté disponible para tu proyecto."
        else:
            detalle = "El servicio no pudo completar la solicitud. Intenta más tarde."
        raise RuntimeError(f"Gemini respondió HTTP {estado}. {detalle}") from None
    except requests.RequestException:
        raise RuntimeError("No se pudo completar la petición a Gemini.") from None

    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("Gemini devolvió una respuesta que no es JSON válido.") from None


def extraer_texto(datos):
    """Extrae el texto esperado y rechaza respuestas incompletas."""
    try:
        texto = datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("La respuesta de Gemini no contiene el campo de texto esperado.") from None
    if not isinstance(texto, str) or not texto.strip():
        raise RuntimeError("La respuesta de Gemini contiene un texto vacío o inválido.")
    return texto.strip()


def obtener_dato_de_prueba(pregunta):
    """Coordina las tres responsabilidades del módulo."""
    url, encabezados, cuerpo = armar_peticion(pregunta)
    datos = enviar_peticion(url, encabezados, cuerpo)
    return extraer_texto(datos)


def main(argumentos=None):
    """Muestra un resultado o un mensaje legible, sin traceback ni credenciales."""
    parser = argparse.ArgumentParser(description="Consulta de prueba a Gemini")
    parser.add_argument("pregunta", help="Pregunta entre comillas")
    opciones = parser.parse_args(argumentos)
    try:
        print(obtener_dato_de_prueba(opciones.pregunta))
        return 0
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
