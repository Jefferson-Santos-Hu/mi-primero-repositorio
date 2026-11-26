"""Comprueba coherencia de la ejecución E2E documentada."""
import json
from pathlib import Path
from escenarios import ESCENARIOS
from ejecutar_escenarios import huella


def comprobar():
    r=json.loads(Path('docs/escenarios_resultados.json').read_text(encoding='utf8'))
    categorias={c['categoria'] for c in ESCENARIOS}
    bitacora=Path('docs/bitacora_ajustes.md').read_text(encoding='utf-8-sig')
    return [('cobertura',len(ESCENARIOS)>=10 and len(categorias)>=4 and {'fuera de alcance','error esperado','control'}<=categorias),('registro vigente',r['huella']==huella() and {x['id'] for x in r['resultados']}=={x['id'] for x in ESCENARIOS}),('casos cumplidos',all(x['pasa'] for x in r['resultados'])),('modo declarado',r['modo'] in {'real','simulado'}),('ajustes documentados',bitacora.count('| IT-')>=2 and 'Conservar' in bitacora)]


if __name__=='__main__':
    r=comprobar()
    for nombre,ok in r:print('PASA' if ok else 'FALLA',nombre)
    print(sum(x for _,x in r),'de',len(r),'comprobaciones cumplidas');raise SystemExit(not all(x for _,x in r))
