"""Ejecuta contratos por HTTP a través de la interfaz/proxy, con registro real."""
import hashlib,json,time
from pathlib import Path
from datetime import datetime,timezone
import httpx
from escenarios import ESCENARIOS


def huella(escenarios=ESCENARIOS):
    return hashlib.sha256(json.dumps(escenarios,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def evaluar(caso,estado,texto):
    return estado==caso['estado'] and caso['contiene'] in texto


def ejecutar(base='http://127.0.0.1:8080',casos=ESCENARIOS,guardar=True):
    filas=[]
    with httpx.Client(base_url=base,timeout=120) as cliente:
        salud=cliente.get('/api/salud').json()
        for c in casos:
            t=time.perf_counter();r=cliente.request(c['metodo'],c['ruta'] if c.get('directa') else '/api'+c['ruta'],json=c.get('json'))
            filas.append({'id':c['id'],'categoria':c['categoria'],'estado':r.status_code,'esperado':c['estado'],'pasa':evaluar(c,r.status_code,r.text),'latencia_ms':round((time.perf_counter()-t)*1000,2),'respuesta':r.json() if 'application/json' in r.headers.get('content-type','') else r.text})
    salida={'fecha':datetime.now(timezone.utc).isoformat(),'base':base,'modo':salud['modelo_activo'],'huella':huella(casos),'resultados':filas}
    if guardar:Path('docs/escenarios_resultados.json').write_text(json.dumps(salida,ensure_ascii=False,indent=2),encoding='utf8')
    return salida


if __name__=='__main__':
    r=ejecutar();print(sum(x['pasa'] for x in r['resultados']),'de',len(r['resultados']),'escenarios cumplidos; modo',r['modo'])
    raise SystemExit(not all(x['pasa'] for x in r['resultados']))
