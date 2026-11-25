"""Diagnosticar, proponer pasos y revisar seguridad de una consulta técnica."""
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def construir_cadena(modelo):
    diagnosticar=PromptTemplate.from_template('Identifica el síntoma y los datos que faltan en esta consulta técnica. No inventes causas. Responde brevemente en español: {texto}')|modelo|StrOutputParser()
    proponer=PromptTemplate.from_template('Con este diagnóstico, redacta hasta tres pasos de verificación seguros para un principiante. No pidas claves: {diagnostico}')|modelo|StrOutputParser()
    revisar=PromptTemplate.from_template('Revisa este borrador. Corrige instrucciones inseguras y afirmaciones no justificadas. Devuelve solo la guía final breve en español: {borrador}')|modelo|StrOutputParser()
    return diagnosticar|(lambda texto:{'diagnostico':texto})|proponer|(lambda texto:{'borrador':texto})|revisar


if __name__=='__main__':
    from modelo_langchain import crear_modelo
    print(construir_cadena(crear_modelo()).invoke({'texto':'Mi programa Python usa requests para Gemini y recibe HTTP 429. Lo intento en un bucle sin pausas y sigue fallando.'}))
