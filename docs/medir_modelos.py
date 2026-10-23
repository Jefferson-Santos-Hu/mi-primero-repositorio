"""Medición real del Bloque 9. Ejecutar desde la raíz: python docs/medir_modelos.py.
Hace 12 peticiones reales (pueden consumir cuota); actualiza mediciones_bloque9.json.
Antes de repetir, verifica y actualiza PRECIOS con la fuente oficial fechada.
No modifica el módulo de la aplicación ni el archivo .env.
"""
from datetime import datetime
import json
from pathlib import Path
import statistics
import sys
import time
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from src.consumir_gemini import armar_peticion, enviar_peticion, extraer_texto

MODELOS = ("gemini-3.5-flash-lite", "gemini-3.8-flash")
PRECIOS = {MODELOS[0]: (0.30, 2.50), MODELOS[1]: (0.75, 3.75)}
PREGUNTAS = (
    "Responde en español en un máximo de 80 palabras: ¿Para qué sirve un entorno virtual de Python y cómo lo creas con venv?",
    "Responde en español en un máximo de 80 palabras: ¿Cómo protejo una API key en un proyecto Python con Git usando .env y .gitignore?",
    "Responde en español en un máximo de 80 palabras: Mi petición HTTP devuelve 429. ¿Qué significa y qué debo hacer?",
)
destino = REPO / "docs" / "mediciones_bloque9.json"
datos = {"fecha_inicio": datetime.now().astimezone().isoformat(timespec="seconds"),
         "protocolo": "4 repeticiones de P1 por modelo, alternando modelos; P2 y P3 una vez por modelo. Mismo POST y configuración predeterminada del módulo; sin caché explícita, herramientas ni streaming.",
         "fuente_precios": "https://ai.google.dev/gemini-api/docs/pricing",
         "precios_usd_por_millon_entrada_salida": PRECIOS,
         "preguntas": PREGUNTAS, "ejecuciones": []}
for indice in (0, 0, 0, 0, 1, 2):
    for modelo in MODELOS:
        registro = {"modelo_solicitado": modelo, "pregunta": indice + 1,
                    "fecha": datetime.now().astimezone().isoformat(timespec="seconds")}
        with patch.dict("os.environ", {"GEMINI_MODEL": modelo}):
            url, encabezados, cuerpo = armar_peticion(PREGUNTAS[indice])
        inicio = time.perf_counter()
        try:
            respuesta = enviar_peticion(url, encabezados, cuerpo)
            registro["segundos"] = round(time.perf_counter() - inicio, 6)
            registro["texto"] = extraer_texto(respuesta)
            registro["usageMetadata"] = respuesta.get("usageMetadata", {})
            registro["modelo_devuelto"] = respuesta.get("modelVersion")
            uso = registro["usageMetadata"]
            entrada = uso.get("promptTokenCount")
            salida = uso.get("candidatesTokenCount")
            pensamiento = uso.get("thoughtsTokenCount", 0)
            if entrada is not None and salida is not None:
                pe, ps = PRECIOS[modelo]
                registro["costo_equivalente_pago_usd"] = round((entrada * pe + (salida + pensamiento) * ps) / 1_000_000, 10)
            registro["resultado"] = "correcto"
        except RuntimeError as error:
            registro["segundos"] = round(time.perf_counter() - inicio, 6)
            registro["resultado"] = "error"
            registro["mensaje"] = str(error)
        datos["ejecuciones"].append(registro)
        destino.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{modelo} P{indice+1}: {registro['resultado']} {registro['segundos']:.3f}s", flush=True)
for modelo in MODELOS:
    tiempos = [r["segundos"] for r in datos["ejecuciones"] if r["modelo_solicitado"] == modelo and r["pregunta"] == 1 and r["resultado"] == "correcto"]
    print(modelo, "respuestas P1:", len(tiempos), "promedio:", statistics.mean(tiempos) if tiempos else "sin respuestas")
