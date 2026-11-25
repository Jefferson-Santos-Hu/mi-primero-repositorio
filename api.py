"""API local del asistente RAG. No registra cuerpos ni errores del proveedor."""
import os
import threading
import uuid
from fastapi import FastAPI,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,ConfigDict,field_validator
from starlette.exceptions import HTTPException
from servicio_rag import crear_servicio,detectar_inyeccion


class Consulta(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    pregunta: str=Field(min_length=1,max_length=4000)
    k:int=Field(default=3,ge=1,le=6)

    @field_validator('pregunta')
    @classmethod
    def no_blanco(cls,valor):
        if not valor.strip():raise ValueError('Pregunta vacía')
        return valor.strip()


def crear_app(servicio=None):
    app=FastAPI(title='Asistente técnico Python/Gemini',version='2.0.0',description='RAG sobre corpus sintético del proyecto con fuentes y auditoría.')
    app.state.servicio=servicio
    app.state.lock=threading.Lock()

    @app.exception_handler(RequestValidationError)
    async def validacion(request,exc):
        return JSONResponse(status_code=422,content={'codigo':'entrada_invalida','mensaje':'Revisa pregunta (1–4000 caracteres), k (1–6) y campos permitidos.'})

    @app.exception_handler(HTTPException)
    async def http_error(request,exc):
        return JSONResponse(status_code=exc.status_code,content={'codigo':'no_encontrado' if exc.status_code==404 else 'error_http','mensaje':'Recurso no disponible.'})

    @app.get('/salud',summary='Comprueba el proceso sin llamar a Gemini')
    def salud():
        return {'estado':'ok','modelo_activo':'real','servicio':'asistente_tecnico'}

    @app.get('/errores/{codigo}',summary='Consulta el catálogo HTTP local')
    def errores(codigo:int):
        from agente_con_herramientas import consultar_error_http
        if not 100<=codigo<=599:
            return JSONResponse(status_code=422,content={'codigo':'entrada_invalida','mensaje':'Código HTTP fuera de rango.'})
        return {'codigo_http':codigo,'detalle':consultar_error_http.invoke({'codigo':codigo,'incluir_detalle':True})}

    @app.post('/consultas',summary='Responde con recuperación y citas')
    def consultar(consulta:Consulta):
        if detectar_inyeccion(consulta.pregunta):
            return {'estado':'rechazado','respuesta':'No puedo atender instrucciones que alteren las reglas del sistema.','fuentes':[],'trace_id':'trace-'+uuid.uuid4().hex}
        try:
            with app.state.lock:
                if app.state.servicio is None:
                    app.state.servicio,_=crear_servicio(os.getenv('INDICE_DIR','vectorstore'))
                return app.state.servicio.consultar(consulta.pregunta,consulta.k)
        except (RuntimeError,TimeoutError,ValueError,ConnectionError):
            return JSONResponse(status_code=503,content={'codigo':'modelo_no_disponible','mensaje':'No se pudo generar una respuesta validada. Revisa configuración, cuota y conexión.'})
        except Exception:
            return JSONResponse(status_code=503,content={'codigo':'servicio_no_disponible','mensaje':'El servicio no está disponible temporalmente.'})
    return app


app=crear_app()
