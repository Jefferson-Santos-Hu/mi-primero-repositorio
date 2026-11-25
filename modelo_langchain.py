"""Construcción explícita y diferida del modelo; usa la misma configuración."""
from langchain_google_genai import ChatGoogleGenerativeAI
from src.consumir_gemini import armar_peticion


def crear_modelo():
    url,encabezados,_=armar_peticion('Verificar configuración')
    modelo=url.rsplit('/',1)[-1].removesuffix(':generateContent')
    return ChatGoogleGenerativeAI(model=modelo,api_key=encabezados['x-goog-api-key'],timeout=90,max_retries=2)
