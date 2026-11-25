"""Clasificación y rutas técnicas con fallback específico y control general."""
import logging
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch,RunnableLambda,RunnablePassthrough

logger=logging.getLogger(__name__)


def normalizar_categoria(texto):
    return texto.strip().strip('"\'').lower()


def construir_cadena_queja_segura(cadena_queja):
    def respaldo(_):
        logger.warning('Fallback de la ruta técnica: no se pudo generar la respuesta.')
        return 'No pude revisar la configuración ahora. Consulta al equipo de soporte con el código de error, sin incluir contraseñas ni claves.'
    return cadena_queja.with_fallbacks([RunnableLambda(respaldo)])


def construir_cadena_con_enrutamiento(modelo,paso_clasificacion=None):
    if paso_clasificacion is None:
        paso_clasificacion=PromptTemplate.from_template('Clasifica el mensaje técnico en credenciales, limite_uso o general. Devuelve solo una etiqueta: {mensaje}')|modelo|StrOutputParser()
    clasificar=paso_clasificacion|RunnableLambda(normalizar_categoria)
    credenciales=PromptTemplate.from_template('Ayuda con autenticación en Gemini: explica verificación local de variables y permisos, sin pedir claves. Mensaje: {mensaje}')|modelo|StrOutputParser()
    limite=PromptTemplate.from_template('Ayuda con cuota y rate limits: revisar límites, Retry-After y backoff, sin recomendar saturar el servicio. Mensaje: {mensaje}')|modelo|StrOutputParser()
    general=PromptTemplate.from_template('Eres un tutor de Python: responde brevemente con pasos seguros a este mensaje técnico: {mensaje}')|modelo|StrOutputParser()
    rutas=RunnableBranch((lambda d:d['categoria']=='credenciales',construir_cadena_queja_segura(credenciales)),(lambda d:d['categoria']=='limite_uso',limite),general)
    return RunnablePassthrough.assign(categoria=clasificar)|rutas


def procesar_mensaje_seguro(cadena,mensaje):
    try:
        if not isinstance(mensaje,str) or not mensaje.strip():
            raise ValueError('Mensaje vacío')
        return cadena.invoke({'mensaje':mensaje})
    except Exception as error:
        logger.warning('Fallo del flujo orquestado; tipo=%s',type(error).__name__)
        return 'No pudimos procesar tu mensaje en este momento. Intenta de nuevo más tarde.'
