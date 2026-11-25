"""Bloques 15–17: genera 20 respuestas reales y preserva cada resultado."""
from datetime import datetime
import json
from pathlib import Path
import time
from cliente import consultar_modelo
from pipeline_texto import calcular_metricas, procesar_texto, resumir_metricas

CASOS = [
    ('¿Qué es Python?','Python es un lenguaje de programación interpretado.'),
    ('¿Para qué sirve venv?','Un entorno virtual aísla las dependencias de un proyecto.'),
    ('¿Qué es una lista en Python?','Una lista es una colección ordenada y modificable.'),
    ('¿Qué es una tupla en Python?','Una tupla es una colección ordenada e inmutable.'),
    ('¿Qué es un diccionario en Python?','Un diccionario relaciona claves con valores.'),
    ('¿Qué significa HTTP 429?','HTTP 429 indica demasiadas solicitudes o límites de uso.'),
    ('¿Qué significa HTTP 401?','HTTP 401 indica que falta una autenticación válida.'),
    ('¿Qué significa HTTP 404?','HTTP 404 indica que no se encontró el recurso.'),
    ('¿Para qué sirve .gitignore?','.gitignore evita agregar archivos no rastreados que coinciden con sus patrones.'),
    ('¿Qué guarda .env?','.env guarda variables de configuración local, incluidas credenciales.'),
    ('¿Qué es un commit?','Un commit registra un estado del proyecto en Git.'),
    ('¿Qué hace git clone?','git clone crea una copia local de un repositorio.'),
    ('¿Qué hace pip install?','pip install instala paquetes de Python.'),
    ('¿Qué representa requirements.txt?','requirements.txt declara las dependencias necesarias del proyecto.'),
    ('¿Qué es JSON?','JSON es un formato de intercambio de datos.'),
    ('¿Qué hace json.loads en Python?','json.loads convierte un texto JSON en objetos de Python.'),
    ('¿Para qué sirve try except?','try except permite capturar y manejar excepciones.'),
    ('¿Qué es un timeout de red?','Un timeout limita el tiempo de espera de una operación de red.'),
    ('¿Qué es backoff exponencial?','El backoff exponencial aumenta la espera entre reintentos consecutivos.'),
    ('¿Qué hace una prueba con mocks?','Una prueba con mocks sustituye dependencias externas por objetos controlados.'),
]


def coincidencia(referencia,respuesta):
    a,b=set(referencia),set(respuesta)
    return len(a & b)/len(a) if a else 0


def main():
    ruta=Path(__file__).resolve().parent/'resultados_metricas.json'
    resultados=[]
    for indice,(pregunta,referencia) in enumerate(CASOS,1):
        respuesta=consultar_modelo(pregunta,'Responde en español con una frase breve y técnicamente precisa, sin Markdown.')
        resultados.append({'id':indice,'fecha':datetime.now().astimezone().isoformat(timespec='seconds'),
            'consulta':pregunta,'referencia':referencia,'respuesta':respuesta,
            'coincidencia_cruda':coincidencia(referencia.split(),respuesta.split()),
            'coincidencia_procesada':coincidencia(procesar_texto(referencia),procesar_texto(respuesta)),
            **calcular_metricas(referencia,respuesta)})
        ruta.write_text(json.dumps(resultados,ensure_ascii=False,indent=2),encoding='utf-8')
        print(f'Caso {indice}/20 guardado; F1={resultados[-1]["f1"]:.3f}',flush=True)
        time.sleep(1)
    print(resumir_metricas(resultados))


if __name__=='__main__':
    main()
