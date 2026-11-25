"""Comprueba dependencias, credencial presente e índice, sin revelar secretos."""
import sys
from importlib.metadata import version
from pathlib import Path
from dotenv import load_dotenv
import os


def verificar():
    load_dotenv(Path(__file__).resolve().parent/'.env')
    errores=[]
    print('Python:',sys.version.split()[0])
    for paquete in ['langchain-core','langchain-chroma','langgraph','python-dotenv','langchain-google-genai']:
        try:print(paquete+':',version(paquete))
        except Exception:errores.append('Falta '+paquete)
    if not (os.getenv('API_KEY') or os.getenv('GEMINI_API_KEY')):errores.append('Configurar API_KEY o GEMINI_API_KEY')
    else:print('Credencial: definida (valor oculto)')
    if not (Path('vectorstore')/'manifiesto.json').exists():errores.append('Ejecutar indexar_documentos.py')
    else:print('Índice persistido: presente')
    if errores:raise SystemExit('; '.join(errores))
    print('Entorno listo para el Gate 2')


if __name__=='__main__':verificar()
