"""Ocho reglas verificables del README; no acredita lectura por otro alumno."""
import re,subprocess,sys
from pathlib import Path


def comprobar(texto=None,ejecutar_pruebas=True):
    s=texto if texto is not None else Path('README.md').read_text(encoding='utf-8-sig')
    rutas=re.findall(r'\]\(([^)]+)\)',s);locales=[p for p in rutas if not re.match(r'\w+://',p) and not p.startswith('#')]
    pruebas=subprocess.run([sys.executable,'-m','pytest','tests/parciales/test_api_contrato.py','-q'],capture_output=True,text=True) if ejecutar_pruebas else None
    return [('descripcion','Asistente' in s or 'asistente' in s),('requisitos',all(x in s for x in ['Python','Docker','Git'])),('instalacion',all(x in s for x in ['git clone','python -m venv','requirements-dev.txt'])),('rutas',all(Path(p).exists() for p in locales)),('configuracion',all(x in s for x in ['API_KEY','MODELO','.env'])),('arranque y parada','docker compose up' in s and 'docker compose down' in s),('decisiones y limites',all(x in s for x in ['D-01','LIM-01','docs/decisiones.md','docs/limitaciones.md'])),('pruebas',pruebas is not None and pruebas.returncode==0)]


if __name__=='__main__':
    r=comprobar()
    for n,v in r:print('PASA' if v else 'FALLA',n)
    print(sum(v for _,v in r),'de',len(r),'reglas cumplidas');raise SystemExit(not all(v for _,v in r))
