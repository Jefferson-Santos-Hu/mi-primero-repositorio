"""Sondas sintéticas del detector, sin atribuirlas a respuestas reales del proveedor."""
from langchain_core.documents import Document
from fundamentacion import comprobar_fundamentacion
DOCS=[Document(page_content='El cliente reintenta tres veces ante HTTP 429. No reintenta errores 401 y 403.')]
SONDAS=[{'id':'H-01','respuesta':'El cliente reintenta 99 veces [1].','debe_rechazar':True,'tipo':'cifra_inventada'}, {'id':'H-02','respuesta':'El cliente reintenta [99].','debe_rechazar':True,'tipo':'fuente_inventada'}, {'id':'H-03','respuesta':'Se reintenta el error 401 [1].','debe_rechazar':True,'tipo':'contradiccion_autenticacion'}, {'id':'H-04','respuesta':'El cliente reintenta siempre [1].','debe_rechazar':True,'tipo':'afirmacion_semantica','limite':'LIM-01'}, {'id':'H-05','respuesta':'El cliente reintenta tres veces [1].','debe_rechazar':False,'tipo':'control'}]


def ejecutar_sondas():
    return [{**s,'rechazada':not comprobar_fundamentacion(s['respuesta'],DOCS)['valida']} for s in SONDAS]


if __name__=='__main__':
    import json
    from pathlib import Path
    resultados=ejecutar_sondas()
    Path('docs/alucinaciones_resultados.json').write_text(json.dumps(resultados,ensure_ascii=False,indent=2),encoding='utf8')
    lineas=['# Registro de alucinaciones controladas','','Sondas escritas antes de ejecutar el detector. No son salidas atribuidas a Gemini.','', '| ID | Tipo | Debe rechazar | Rechazada | Resultado | Decisión |','|---|---|---|---|---|---|']
    for s in resultados:
        coincide=s['rechazada']==s['debe_rechazar'];lineas.append(f"| {s['id']} | {s['tipo']} | {s['debe_rechazar']} | {s['rechazada']} | {'PASA' if coincide else 'LIMITE'} | {'Mantener regresión' if coincide else 'LIM-01: revisar fuentes manualmente; residual alto'} |")
    Path('docs/registro_alucinaciones.md').write_text('\n'.join(lineas)+'\n',encoding='utf8')
    print('Sondas registradas; límite semántico H-04 declarado')
