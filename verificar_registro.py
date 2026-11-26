import json,subprocess
from pathlib import Path
from registrar_ejecucion import huella_codigo
from ejecutar_escenarios import huella


def comprobar():
    d=json.loads(Path('docs/registro_ejecucion.json').read_text(encoding='utf8'));s=Path('docs/registro_ejecucion.md').read_text(encoding='utf-8-sig')
    ancestor=subprocess.run(['git','merge-base','--is-ancestor',d['commit'],'HEAD'],capture_output=True).returncode==0
    return [('codigo vigente',d['huella_codigo']==huella_codigo()),('commit rastreable',ancestor),('corrida completa',d['casos']>=10 and d['casos']==d['cumplidos']),('escenarios vigentes',d['escenarios_huella']==huella()),('manual completo',all(t in s and len(s.split(t,1)[1].split('##')[0].strip())>=40 for t in ['## Qué se observó','## Qué no se probó','## Siguiente paso'])),('modo honesto',d['modo'] in {'real','simulado'} and (d['modo']!='simulado' or 'modelo simulado' in s))]


if __name__=='__main__':
    r=comprobar()
    for nombre,ok in r:print('PASA' if ok else 'FALLA',nombre)
    print(sum(x for _,x in r),'de',len(r),'comprobaciones cumplidas');raise SystemExit(not all(x for _,x in r))
