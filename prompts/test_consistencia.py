"""Prueba REAL: python -m prompts.test_consistencia. No se ejecuta al importar."""
import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import time

from prompts.banco import BANCO_DE_PROMPTS
from src.consumir_gemini import armar_peticion, enviar_peticion, extraer_texto, parsear_respuesta_json

RUTA_REGISTRO = Path(__file__).resolve().parent / "registro_resultados.json"


def validar_estructura(valor, esquema, ruta="respuesta"):
    """Valida el subconjunto del esquema usado por este banco, no JSON Schema general."""
    tipo = esquema["type"]
    if tipo == "OBJECT":
        propiedades = esquema["properties"]
        if not isinstance(valor, dict) or not set(esquema["required"]) <= set(valor) or not set(valor) <= set(propiedades):
            raise ValueError(f"{ruta}: faltan claves requeridas o aparecen claves inesperadas.")
        for clave, dato in valor.items():
            validar_estructura(dato, propiedades[clave], f"{ruta}.{clave}")
    elif tipo == "STRING":
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{ruta}: se esperaba un string no vacío.")
    elif tipo in ("NUMBER", "INTEGER"):
        valido = type(valor) is int if tipo == "INTEGER" else type(valor) in (int, float)
        if not valido or not math.isfinite(valor):
            raise ValueError(f"{ruta}: se esperaba un {tipo.lower()} finito, no booleano.")
        if valor < esquema.get("minimum", -math.inf) or valor > esquema.get("maximum", math.inf):
            raise ValueError(f"{ruta}: número fuera del intervalo permitido.")
    elif tipo == "ARRAY":
        if not isinstance(valor, list) or not esquema.get("minItems", 0) <= len(valor) <= esquema.get("maxItems", math.inf):
            raise ValueError(f"{ruta}: lista inválida o longitud incorrecta.")
        for indice, item in enumerate(valor):
            validar_estructura(item, esquema["items"], f"{ruta}[{indice}]")
    else:
        raise ValueError(f"{ruta}: tipo de esquema no implementado.")
    if "enum" in esquema and valor not in esquema["enum"]:
        raise ValueError(f"{ruta}: valor fuera de las opciones permitidas.")


def ejecutar_consistencia(banco=BANCO_DE_PROMPTS, repeticiones=3, pausa=1, destino=RUTA_REGISTRO):
    """Registra éxitos y fallos reales, sin descartar intentos ni detener la serie."""
    if type(repeticiones) is not int or repeticiones < 3 or not math.isfinite(pausa) or pausa < 0:
        raise ValueError("Usa al menos 3 repeticiones y una pausa finita no negativa.")
    registro = {
        "fecha_inicio": datetime.now().astimezone().isoformat(timespec="seconds"),
        "banco_sha256": hashlib.sha256(json.dumps(banco, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        "repeticiones_por_prompt": repeticiones,
        "pausa_segundos": pausa,
        "criterio": "Objeto JSON, claves exactas, tipos, textos no vacíos, enum, intervalos y longitud de listas. No mide equivalencia literal ni garantiza corrección semántica.",
        "prompts": {},
    }
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    for prompt in banco:
        grupo = {"version": prompt["version"], "intentos": repeticiones, "exitos": 0, "fallos": 0, "repeticiones": []}
        registro["prompts"][prompt["nombre"]] = grupo
        for intento in range(1, repeticiones + 1):
            detalle = {"intento": intento, "fecha": datetime.now().astimezone().isoformat(timespec="seconds")}
            inicio = time.perf_counter()
            try:
                url, encabezados, cuerpo = armar_peticion(prompt["ejemplo_usuario"], prompt["system_instruction"], prompt.get("response_schema"))
                detalle["modelo_solicitado"] = url.rsplit("/", 1)[-1].removesuffix(":generateContent")
                respuesta = enviar_peticion(url, encabezados, cuerpo)
                detalle["modelo_devuelto"] = respuesta.get("modelVersion")
                detalle["usageMetadata"] = respuesta.get("usageMetadata", {})
                texto = extraer_texto(respuesta)
                detalle["texto_original"] = texto
                datos = parsear_respuesta_json(texto)
                validar_estructura(datos, prompt["response_schema"])
                detalle.update({"valida": True, "datos": datos})
                grupo["exitos"] += 1
            except (ValueError, RuntimeError) as error:
                detalle.update({"valida": False, "error": str(error)})
                grupo["fallos"] += 1
                print(f"{prompt['nombre']}, intento {intento} falló: {error}")
            detalle["segundos"] = round(time.perf_counter() - inicio, 6)
            grupo["repeticiones"].append(detalle)
            destino.write_text(json.dumps(registro, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"{prompt['nombre']}: intento {intento}/{repeticiones}, {'válido' if detalle['valida'] else 'fallido'}", flush=True)
            time.sleep(pausa)
        grupo["consistencia"] = grupo["exitos"] / repeticiones
        print(f"{prompt['nombre']}: {grupo['exitos']}/{repeticiones} respuestas válidas; {grupo['fallos']} fallos", flush=True)
    registro["fecha_fin"] = datetime.now().astimezone().isoformat(timespec="seconds")
    destino.write_text(json.dumps(registro, indent=2, ensure_ascii=False), encoding="utf-8")
    return registro


def main(argumentos=None):
    parser = argparse.ArgumentParser(description="Mide la consistencia con peticiones reales a Gemini")
    parser.add_argument("--repeticiones", type=int, default=3)
    parser.add_argument("--pausa", type=float, default=1)
    parser.add_argument("--destino", type=Path, default=RUTA_REGISTRO)
    opciones = parser.parse_args(argumentos)
    registro = ejecutar_consistencia(repeticiones=opciones.repeticiones, pausa=opciones.pausa, destino=opciones.destino)
    return 0 if all(p["exitos"] == p["intentos"] for p in registro["prompts"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
