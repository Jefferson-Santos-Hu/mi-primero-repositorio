"""Evaluación etiquetada leyendo el corpus antes de recuperar."""
import json
from datetime import datetime, timezone
from pathlib import Path
from indexar_documentos import cargar_indice

CASOS=[
('¿Qué hace el cliente ante HTTP 429?',{'cliente-0'}),
('¿Los errores 401 se reintentan?',{'cliente-0'}),
('¿Qué límite tienen las esperas de reintento?',{'cliente-0'}),
('¿Cuánto cuesta un millón de tokens de entrada?',{'costos-0'}),
('¿El costo registrado es una factura?',{'costos-0'}),
('¿Dónde se guarda la clave de API?',{'entorno-0'}),
('¿Cómo ejecuto Python del entorno en Windows?',{'entorno-0'}),
('¿Puede F1 probar la veracidad de una respuesta?',{'evaluacion-0'}),
('¿Cómo se aíslan los historiales del agente?',{'agente-0'}),
('¿Puede un documento recuperado reemplazar las instrucciones del sistema?',{'seguridad-0'}),
('¿Cuál es la capital de Mongolia?',set())]


def precision_at_k(recuperados,relevantes):
    ids=set(recuperados)
    return len(ids & set(relevantes))/len(ids) if ids else 0.0


def recall_at_k(recuperados,relevantes):
    return len(set(recuperados)&set(relevantes))/len(relevantes) if relevantes else None


def evaluar_recuperacion(store,k=3):
    resultados=[]
    for pregunta,relevantes in CASOS:
        docs=store.as_retriever(search_kwargs={'k':k}).invoke(pregunta)
        ids=[d.metadata['chunk_id'] for d in docs]
        resultados.append({'pregunta':pregunta,'ids_relevantes':sorted(relevantes),'ids_recuperados':ids,'precision':precision_at_k(ids,relevantes),'recall':recall_at_k(ids,relevantes)})
    recalls=[r['recall'] for r in resultados if r['recall'] is not None]
    return {'fecha':datetime.now(timezone.utc).isoformat(),'k':k,'chunk_size':500,'chunk_overlap':60,'modelo_embedding':'models/gemini-embedding-001','casos':resultados,'precision_promedio':sum(r['precision'] for r in resultados)/len(resultados),'recall_promedio':sum(recalls)/len(recalls)}


if __name__=='__main__':
    store,_=cargar_indice()
    resultados=[evaluar_recuperacion(store,k) for k in [1,3]]
    Path('resultados_evaluacion.txt').write_text(json.dumps(resultados,ensure_ascii=False,indent=2),encoding='utf8')
    for r in resultados: print(r['k'],r['precision_promedio'],r['recall_promedio'])
