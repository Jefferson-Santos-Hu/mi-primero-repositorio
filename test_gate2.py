"""Cuatro criterios no compensables del Gate 2, sin llamadas pagadas."""
import json,logging
from unittest.mock import Mock
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langgraph.types import Command
from indexar_documentos import cargar_indice
from servicio_rag import ServicioRAG
from gobernanza import crear_supervision,huella_prompt


def test_pipeline_persistido_de_punta_a_punta(tmp_path):
    corpus=tmp_path/'corpus';corpus.mkdir()
    (corpus/'cliente.md').write_text('Ante HTTP 429 usar backoff.',encoding='utf8')
    emb=DeterministicFakeEmbedding(size=16)
    store,creado=cargar_indice(tmp_path/'indice',corpus,emb)
    assert creado
    store,creado=cargar_indice(tmp_path/'indice',corpus,emb)
    assert not creado
    generar=Mock(return_value={'candidates':[{'content':{'parts':[{'text':'Usar backoff [1].'}]}}],'usageMetadata':{'promptTokenCount':30,'candidatesTokenCount':8}})
    r=ServicioRAG(store,emb,generar).consultar('HTTP 429',k=1)
    assert r['estado']=='ok' and r['fuentes']==['cliente.md']
    generar.assert_called_once()


def test_respuesta_tiene_cita_y_fuente():
    store=Mock();store.similarity_search_by_vector.return_value=[Document(page_content='Regla.',metadata={'fuente':'regla.md'})]
    generar=lambda p:{'candidates':[{'content':{'parts':[{'text':'Regla [1].'}]}}],'usageMetadata':{'promptTokenCount':10,'candidatesTokenCount':4}}
    r=ServicioRAG(store,Mock(),generar).consultar('Consulta sintética')
    assert '[1]' in r['respuesta'] and r['fuentes']==['regla.md']


def test_logs_json_correlacionados_sin_contenido(caplog):
    pregunta='PREGUNTA_PRIVADA_DE_PRUEBA'
    documento='DOCUMENTO_PRIVADO_DE_PRUEBA'
    store=Mock();store.similarity_search_by_vector.return_value=[Document(page_content=documento,metadata={'fuente':'sintetica.md'})]
    generar=lambda p:{'candidates':[{'content':{'parts':[{'text':'Regla [1].'}]}}],'usageMetadata':{'promptTokenCount':10,'candidatesTokenCount':4}}
    with caplog.at_level(logging.INFO,logger='servicio_rag'):
        r=ServicioRAG(store,Mock(),generar).consultar(pregunta)
    eventos=[json.loads(x.message) for x in caplog.records if x.name=='servicio_rag']
    assert len(eventos)>=5
    assert {e['trace_id'] for e in eventos}=={r['trace_id']}
    assert pregunta not in caplog.text and documento not in caplog.text


def test_supervision_pausa_y_reanuda_sin_aprobar_antes():
    app=crear_supervision();huella=huella_prompt('Cambio sintético')
    for decision,sesion in [(True,'aceptar'),(False,'rechazar')]:
        cfg={'configurable':{'thread_id':sesion}}
        r=app.invoke({'huella_nueva':huella,'aprobado':False},cfg)
        assert '__interrupt__' in r and 'activa' not in r
        r=app.invoke(Command(resume=decision),cfg)
        assert r['aprobado'] is decision
        assert (r.get('activa')==huella) is decision
