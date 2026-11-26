"""Cruza decisiones, limitaciones, riesgos y referencias de README."""
import re
from pathlib import Path
from riesgos import RIESGOS


def comprobar():
    decisiones=Path('docs/decisiones.md').read_text(encoding='utf-8-sig');limites=Path('docs/limitaciones.md').read_text(encoding='utf-8-sig');readme=Path('README.md').read_text(encoding='utf-8-sig')
    bloques=re.findall(r'## (D-\d+)[^\n]*\n(.*?)(?=\n## |\Z)',decisiones,re.S)
    ids=set(re.findall(r'^\| (LIM-\d+) \|',limites,re.M));riesgos={r['id'] for r in RIESGOS};declarados={l for r in RIESGOS for l in r['limites']}
    filas=[l for l in limites.splitlines() if re.match(r'^\| LIM-',l)]
    return [('cinco decisiones',len(bloques)>=5),('campos completos',all(all(c in b for c in ['Estado:','Contexto:','Decisión:','Alternativas:','Costo:']) for _,b in bloques)),('limitaciones registradas',declarados<=ids),('riesgos existentes',all(set(re.findall(r'R-\d+',f))<=riesgos for f in filas)),('decisiones en README',all(i in readme for i,_ in bloques)),('limites en README',all(i in readme for i in ids)),('enlaces existentes',all(p in readme and Path(p).exists() for p in ['docs/decisiones.md','docs/limitaciones.md']))]


if __name__=='__main__':
    r=comprobar()
    for n,v in r:print('PASA' if v else 'FALLA',n)
    print(sum(v for _,v in r),'de',len(r),'reglas cumplidas');raise SystemExit(not all(v for _,v in r))
