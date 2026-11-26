"""Comprueba dos servicios sanos sin imprimir variables ni credenciales."""
import json
from pathlib import Path
import httpx
from docker_util import docker


def verificar(levantar=False):
    if levantar:docker('compose','up','-d','--build','--wait','--wait-timeout','120',timeout=600)
    lineas=docker('compose','ps','--format','json').strip()
    try:
        objetos=json.loads(lineas);objetos=objetos if isinstance(objetos,list) else [objetos]
    except json.JSONDecodeError:objetos=[json.loads(l) for l in lineas.splitlines()]
    servicios={x['Service']:{'estado':x['State'],'salud':x.get('Health')} for x in objetos}
    assert set(servicios)=={'api','interfaz'}
    assert all(x['estado']=='running' and x['salud']=='healthy' for x in servicios.values())
    with httpx.Client(timeout=15) as c:
        assert c.get('http://127.0.0.1:8080/').status_code==200
        salud=c.get('http://127.0.0.1:8080/api/salud').json()
    evidencia={'servicios':servicios,'modo':salud['modelo_activo'],'api_local':8000,'interfaz_local':8080}
    Path('docs/stack_evidencia.json').write_text(json.dumps(evidencia,indent=2),encoding='utf8')
    print('Dos servicios sanos; proxy y salud verificados; modo',salud['modelo_activo'])
    return evidencia


if __name__=='__main__':
    import sys
    verificar('--levantar' in sys.argv)
