import pytest
from pydantic import ValidationError
from agente_con_herramientas import consultar_error_http, calcular_presupuesto, crear_agente_con_memoria
from langchain_core.runnables import RunnableLambda


def test_herramienta_historial_cambia_salida():
    simple=consultar_error_http.invoke({'codigo':429,'incluir_detalle':False})
    detalle=consultar_error_http.invoke({'codigo':429,'incluir_detalle':True})
    assert 'cuota' in simple
    assert len(detalle)>len(simple)
    assert 'desconocido' in consultar_error_http.invoke({'codigo':418})


def test_presupuesto_y_validacion():
    assert '0.00280000' in calcular_presupuesto.invoke({'tokens_entrada':1000,'tokens_salida':1000})
    with pytest.raises(ValidationError):
        calcular_presupuesto.invoke({'tokens_entrada':-1,'tokens_salida':10})


def test_memoria_dos_turnos_y_aislamiento():
    def responder(datos):
        anteriores=[m.content for m in datos['chat_history']]
        return {'output':' | '.join(anteriores+[datos['entrada']])}
    agente,historiales=crear_agente_con_memoria(ejecutor=RunnableLambda(responder))
    cfg={'configurable':{'session_id':'A'}}
    agente.invoke({'entrada':'Mi error es 429'},cfg)
    segundo=agente.invoke({'entrada':'¿Y su solución?'},cfg)
    assert 'Mi error es 429' in segundo['output']
    otro=agente.invoke({'entrada':'Hola'},{'configurable':{'session_id':'B'}})
    assert otro['output']=='Hola'
    assert len(historiales['A'].messages)==4
    assert len(historiales['B'].messages)==2
