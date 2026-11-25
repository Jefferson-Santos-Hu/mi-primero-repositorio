"""Agente de soporte técnico: herramientas locales y memoria aislada por sesión."""
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent


class ConsultaHTTP(BaseModel):
    codigo: int = Field(ge=100,le=599)
    incluir_detalle: bool = False


@tool(args_schema=ConsultaHTTP)
def consultar_error_http(codigo: int, incluir_detalle: bool=False) -> str:
    """Consulta significado de un código HTTP y, opcionalmente, su diagnóstico técnico. Usar para errores HTTP concretos."""
    errores={401:('Autenticación inválida.','Revisar la clave local sin compartirla; no reintentar automáticamente.'),403:('Acceso denegado.','Revisar permisos del proyecto y restricciones de la clave.'),429:('Límite de cuota o frecuencia.','Usar backoff exponencial con jitter y máximo de intentos; revisar la cuota.'),503:('Servicio temporalmente no disponible.','Reintentar con espera acotada; informar si persiste.')}
    if codigo not in errores:
        return f'Código {codigo} desconocido en este catálogo local; consultar documentación oficial.'
    resumen,detalle=errores[codigo]
    return resumen+(' '+detalle if incluir_detalle else '')


class Presupuesto(BaseModel):
    tokens_entrada: int = Field(ge=0,le=10000000)
    tokens_salida: int = Field(ge=0,le=10000000)


@tool(args_schema=Presupuesto)
def calcular_presupuesto(tokens_entrada: int,tokens_salida: int) -> str:
    """Estima USD para Gemini 3.5 Flash Lite estándar a partir de cantidades de tokens de entrada y salida, incluyendo pensamiento. No realiza pagos."""
    costo=(tokens_entrada*.30+tokens_salida*2.50)/1000000
    return f'Estimación: USD {costo:.8f}; tarifa estándar de referencia al 2026-11-25, no factura real.'


def crear_ejecutor(modelo=None):
    if modelo is None:
        from modelo_langchain import crear_modelo
        modelo=crear_modelo()
    herramientas=[consultar_error_http,calcular_presupuesto]
    prompt=ChatPromptTemplate.from_messages([
        ('system','Eres un asistente de soporte Python/Gemini. Usa consultar_error_http para códigos HTTP y calcular_presupuesto para costos con tokens explícitos. Si faltan datos, pregúntalos. Para saludos o contacto, no uses herramientas. Nunca solicites claves. Usa el historial para referencias de turnos anteriores.'),
        MessagesPlaceholder('chat_history',optional=True),
        ('human','{entrada}'),MessagesPlaceholder('agent_scratchpad')])
    agente=create_tool_calling_agent(modelo,herramientas,prompt)
    return AgentExecutor(agent=agente,tools=herramientas,return_intermediate_steps=True,max_iterations=4,max_execution_time=90,verbose=False)


def crear_agente_con_memoria(modelo=None,ejecutor=None):
    historiales={}
    def obtener_historial(session_id):
        if not session_id or len(session_id)>128:
            raise ValueError('Identificador de sesión inválido')
        if session_id not in historiales:
            historiales[session_id]=InMemoryChatMessageHistory()
        return historiales[session_id]
    def normalizar_salida(resultado):
        salida=resultado['output']
        if isinstance(salida,list):
            salida='\n'.join(b.get('text','') for b in salida if isinstance(b,dict) and b.get('type')=='text')
        return {**resultado,'output':salida}
    base=(ejecutor if ejecutor is not None else crear_ejecutor(modelo)) | RunnableLambda(normalizar_salida)
    agente=RunnableWithMessageHistory(base,obtener_historial,input_messages_key='entrada',history_messages_key='chat_history',output_messages_key='output')
    return agente,historiales
