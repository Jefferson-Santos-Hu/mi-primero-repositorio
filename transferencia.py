"""Prueba técnica de transferencia; no inventa ejecución por un compañero."""
import json
from pathlib import Path
import httpx
CASOS=[('T-01','salud','GET','/salud',None,200),('T-02','respuesta con fuente','POST','/consultas',{'pregunta':'HTTP 429'},200),('T-03','validación','POST','/consultas',{'pregunta':''},422),('T-04','catálogo','GET','/errores/429',None,200),('T-05','fuera del catálogo simulado','POST','/consultas',{'pregunta':'capital de Mongolia'},200),('T-06','otro idioma sin regla de demo','POST','/consultas',{'pregunta':'What is the weather?'},200)]


def ejecutar():
    filas=[]
    with httpx.Client(base_url='http://127.0.0.1:8080/api',timeout=30) as c:
        for id_,descripcion,metodo,ruta,cuerpo,estado in CASOS:
            r=c.request(metodo,ruta,json=cuerpo);d=r.json();pasa=r.status_code==estado
            if id_=='T-02':pasa=pasa and d.get('fuentes')==['cliente.md']
            if id_ in {'T-05','T-06'}:pasa=pasa and d.get('fuentes')==[]
            filas.append({'id':id_,'descripcion':descripcion,'pasa':pasa,'estado':r.status_code,'limitacion':'LIM-03' if id_ in {'T-05','T-06'} else None})
    resultado={'autor':'ensayo técnico automatizado; revisión por Javier pendiente','resultados':filas}
    Path('docs/transferencia_evidencia.json').write_text(json.dumps(resultado,ensure_ascii=False,indent=2),encoding='utf8')
    print(sum(f['pasa'] for f in filas),'de',len(filas),'casos técnicos; no acredita transferencia humana')
    return all(f['pasa'] for f in filas)


if __name__=='__main__':raise SystemExit(not ejecutar())
