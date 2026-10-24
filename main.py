"""Miniaplicación Gate 1: consulta real y salida JSON validada."""
import argparse
import json
import sys

from prompts.banco import BANCO_DE_PROMPTS
from src.consumir_gemini import armar_peticion, enviar_peticion, extraer_texto, parsear_respuesta_json
from src.validacion_json import validar_estructura


def consultar(nombre_prompt, texto=None):
    """Ejecuta una tarea del banco con entrada propia o con su ejemplo."""
    prompt = next((p for p in BANCO_DE_PROMPTS if p["nombre"] == nombre_prompt), None)
    if prompt is None:
        raise ValueError("El prompt solicitado no existe en el banco.")
    entrada = prompt["ejemplo_usuario"] if texto is None else texto
    url, encabezados, cuerpo = armar_peticion(
        entrada, prompt["system_instruction"], prompt["response_schema"],
    )
    respuesta = enviar_peticion(url, encabezados, cuerpo)
    datos = parsear_respuesta_json(extraer_texto(respuesta))
    validar_estructura(datos, prompt["response_schema"])
    return datos


def main(argumentos=None):
    parser = argparse.ArgumentParser(description="Asistente técnico con salida JSON validada")
    parser.add_argument("--prompt", choices=[p["nombre"] for p in BANCO_DE_PROMPTS], default="clasificar_consulta_tecnica")
    parser.add_argument("--texto", help="Entrada propia; si se omite, usa el ejemplo del prompt")
    opciones = parser.parse_args(argumentos)
    try:
        datos = consultar(opciones.prompt, opciones.texto)
        print(json.dumps(datos, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
