"""Instrumentación real del RAG, separando costo de generación de embeddings."""
import json
from datetime import datetime,timezone
from pathlib import Path
from servicio_rag import crear_servicio


def registrar_consulta(pregunta,persist_directory='vectorstore',k=3):
    servicio,creado=crear_servicio(persist_directory)
    resultado=servicio.consultar(pregunta,k)
    return {'timestamp':datetime.now(timezone.utc).isoformat(),'pregunta':pregunta,'k':k,'indice_creado':creado,**resultado,'costo_embedding_usd':None,'nota_costo':'Costo de generación equivalente a tarifa estándar; embeddings no exponen aquí contador de tokens, por lo que su costo y el costo total monetario se dejan sin determinar.'}


if __name__=='__main__':
    for k in [1,3]:
        registro=registrar_consulta('¿Qué hace el cliente ante HTTP 429?',k=k)
        with Path('registros_latencia_costo.jsonl').open('a',encoding='utf8') as f:
            f.write(json.dumps(registro,ensure_ascii=False)+'\n')
        print(k,registro['tiempo_total_ms'],registro['costo_generacion_usd'])
