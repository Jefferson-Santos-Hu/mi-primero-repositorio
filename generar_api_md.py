"""Ejemplos y rutas generados contra la aplicación, sin datos del proveedor."""
import json,os,sys
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from api import crear_app


def generar():
    lineas=['# API del asistente técnico','','Base API local: http://127.0.0.1:8000. Proxy de interfaz: http://127.0.0.1:8080/api.','','Ejemplos generados ejecutando FastAPI con MODELO=simulado. No prueban disponibilidad de Gemini. Se omiten trace_id y auditoría por ser variables.','']
    with patch.dict(os.environ,{'MODELO':'simulado'}):
        with TestClient(crear_app()) as c:
            for metodo,ruta,cuerpo in [('GET','/salud',None),('GET','/errores/429',None),('POST','/consultas',{'pregunta':'HTTP 429'}),('POST','/consultas',{'pregunta':''}),('DELETE','/salud',None),('GET','/inexistente',None)]:
                r=c.request(metodo,ruta,json=cuerpo);datos=r.json()
                for clave in ['trace_id','auditoria']:datos.pop(clave,None)
                lineas+=['## '+metodo+' '+ruta,'', 'Entrada: `'+json.dumps(cuerpo,ensure_ascii=False)+'`' if cuerpo is not None else 'Sin cuerpo.',f'HTTP {r.status_code}','```json',json.dumps(datos,ensure_ascii=False,indent=2),'```','']
    lineas+=['## Validación y fallos','','POST /consultas admite pregunta string de 1–4000 caracteres, sin solo espacios; k entero 1–6, default 3; campos extra rechazados. Error uniforme contiene codigo y mensaje, sin el valor enviado. Los fallos del proveedor, clave o validación de fundamentación devuelven 503. La salud del proceso no acredita la cuota del proveedor.','','## Documentación OpenAPI','','GET /openapi.json y /docs describen el contrato generado. No hay autenticación multiusuario: el servicio se mantiene ligado a localhost.']
    return '\n'.join(lineas)+'\n'


if __name__=='__main__':
    p=Path('docs/api.md');texto=generar()
    if '--comprobar' in sys.argv:
        ok=p.exists() and p.read_text(encoding='utf8')==texto;print('API documentada vigente' if ok else 'FALLA: regenerar docs/api.md');raise SystemExit(not ok)
    p.write_text(texto,encoding='utf8');print('docs/api.md generado')
