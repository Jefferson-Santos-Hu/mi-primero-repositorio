"""Ensayo final del Gate 2 con Gemini real y decisiones simuladas de supervisión."""
import io,json,logging
from pathlib import Path
from datetime import datetime,timezone
from servicio_rag import crear_servicio,PROMPT_VERSION
from gobernanza import crear_supervision
from langgraph.types import Command


def verificar():
    captura=io.StringIO();handler=logging.StreamHandler(captura)
    logger=logging.getLogger('servicio_rag');nivel=logger.level
    logger.setLevel(logging.INFO);logger.addHandler(handler)
    try:
        servicio,creado=crear_servicio()
        cantidad_antes=len(servicio.store.get()['ids'])
        pregunta='¿Qué hace el cliente ante HTTP 429?'
        resultado=servicio.consultar(pregunta,k=1)
        otro,recreado=crear_servicio()
        cantidad_despues=len(otro.store.get()['ids'])
        logs=[json.loads(l) for l in captura.getvalue().splitlines()]
        assert resultado['estado']=='ok' and resultado['fuentes']
        assert not recreado and cantidad_antes==cantidad_despues
        assert len(logs)>=5 and all(l['trace_id']==resultado['trace_id'] for l in logs)
        assert pregunta not in captura.getvalue()
        for doc in servicio.store.get()['documents']:
            assert doc not in captura.getvalue()
        supervision=[]
        for decision,nombre in [(True,'aprobacion-simulada'),(False,'rechazo-simulado')]:
            app=crear_supervision();cfg={'configurable':{'thread_id':nombre}}
            pausa=app.invoke({'huella_nueva':PROMPT_VERSION,'aprobado':False},cfg)
            assert '__interrupt__' in pausa and not pausa.get('activa')
            final=app.invoke(Command(resume=decision),cfg)
            assert final['aprobado'] is decision
            supervision.append({'caso':nombre,'pausado':True,'aprobado':final['aprobado'],'activa':final.get('activa')})
        evidencia={'fecha':datetime.now(timezone.utc).isoformat(),'modelo':'gemini-3.5-flash-lite','tipo':'Embeddings y generación reales; reanudaciones de supervisión simuladas explícitamente','indice_creado':creado,'reapertura_sin_reindexar':not recreado,'chunks_antes':cantidad_antes,'chunks_despues':cantidad_despues,'consulta':pregunta,'resultado':resultado,'logs':logs,'supervision':supervision,'no_compensables':{'pipeline_corre_de_punta_a_punta':True,'respuestas_citan_fuente':True,'logs_sin_contenido_crudo':True,'supervision_humana_funciona':True}}
        Path('docs/gate2_evidencia.json').write_text(json.dumps(evidencia,ensure_ascii=False,indent=2),encoding='utf8')
        print('4 de 4 criterios no compensables verificados; consulta real con fuentes:',resultado['fuentes'])
    finally:
        logger.removeHandler(handler);logger.setLevel(nivel)


if __name__=='__main__':verificar()
