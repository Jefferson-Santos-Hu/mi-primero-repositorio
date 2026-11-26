"""Medidor del guion: estructura, tiempos, evidencia y coherencia con la demo."""
import re
from pathlib import Path
PALABRAS_POR_MINUTO=130
SECCIONES={'Problema':1,'Arquitectura':2,'Demo':2,'Riesgos':2,'Cierre':1}


def palabras(texto):return len(re.findall(r'\b\w+\b',texto))


def comprobar(texto=None):
    from ensayo_demo import PASOS
    from riesgos import RIESGOS
    from escenarios import ESCENARIOS
    from verificar_defectos import MUTACIONES
    t=texto if texto is not None else Path('docs/defensa.md').read_text(encoding='utf-8-sig')
    partes={n:re.search(r'## '+n+r' \('+str(m)+r' min\)\n(.*?)(?=\n## |\Z)',t,re.S) for n,m in SECCIONES.items()}
    existentes='\n'.join(Path(p).read_text(encoding='utf-8-sig') for p in ['docs/decisiones.md','docs/limitaciones.md','docs/ficha_diseno_funcional.md'])+'\n'+' '.join(r['id'] for r in RIESGOS)+' H-04 A-07'
    referencias=set(re.findall(r'\b(?:RF|RNF|CA|R|D|LIM|H|A)-\d+\b',t))
    pasos=re.findall(r'^- (PASO-\d+) (.+)$',t,re.M)
    return [('secciones y tiempo',all(partes.values()) and sum(SECCIONES.values())==8),('palabras',all(m and palabras(m[1])<=SECCIONES[n]*PALABRAS_POR_MINUTO for n,m in partes.items())),('identificadores',all(x in existentes for x in referencias)),('riesgos altos',all(r['id'] in t for r in RIESGOS if r['residual']>=9)),('cifras',f'{len(ESCENARIOS)} escenarios' in t and f'{len(MUTACIONES)} defectos' in t and f'{len(RIESGOS)} riesgos' in t),('tecnologias',all(x in t for x in ['FastAPI','Docker','Chroma','Gemini'])),('diapositivas',all(f'| {n} |' in t for n in range(1,7))),('demo coincide',pasos==[(p['id'],p['titulo']) for p in PASOS]),('sin marcas pendientes','[COMPLETAR' not in t and '[PENDIENTE' not in t)]


if __name__=='__main__':
    r=comprobar()
    for n,v in r:print('PASA' if v else 'FALLA',n)
    print(sum(v for _,v in r),'de',len(r),'reglas cumplidas');raise SystemExit(not all(v for _,v in r))
