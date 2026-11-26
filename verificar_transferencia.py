import json,sys
from pathlib import Path


def comprobar(incluir_persona=True):
    d=json.loads(Path('docs/transferencia_evidencia.json').read_text(encoding='utf8'));filas=d['resultados']
    r=[('seis casos',len(filas)>=6),('contrato externo',all(f['pasa'] for f in filas)),('limites declarados',all(f.get('limitacion')=='LIM-03' for f in filas if f['id'] in {'T-05','T-06'})),('documentacion',all(Path(p).exists() for p in ['README.md','docs/api.md','docs/decisiones.md','docs/limitaciones.md'])),('sin atribucion falsa','pendiente' in d['autor'])]
    if incluir_persona:
        p=Path('docs/transferencia.md');r.append(('confirmacion de revisor',p.exists() and 'CONFIRMADA POR REVISOR' in p.read_text(encoding='utf-8-sig')))
    return r


if __name__=='__main__':
    r=comprobar('--sin-revision' not in sys.argv)
    for n,v in r:print('PASA' if v else 'FALLA',n)
    print(sum(v for _,v in r),'de',len(r),'reglas cumplidas');raise SystemExit(not all(v for _,v in r))
