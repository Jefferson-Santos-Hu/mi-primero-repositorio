"""Verificación de entrega: distingue comprobación técnica de revisión ajena."""
import sys,yaml
from pathlib import Path
from buscar_secretos import buscar


def comprobar(incluir_revision=True):
    composicion=yaml.safe_load(Path('compose.yaml').read_text(encoding='utf-8-sig'));s=composicion['services'];readme=Path('README.md').read_text(encoding='utf-8-sig')
    r=[('dos servicios y dependencia',len(s)>=2 and 'depends_on' in s['interfaz']),('variables documentadas',all(v in readme for v in ['API_KEY','MODELO','INDICE_DIR'])),('puertos locales',all('127.0.0.1:' in p for servicio in s.values() for p in servicio.get('ports',[]))),('procedimiento',all(x in readme for x in ['docker compose up','docker compose down','verificar_stack.py'])),('archivos',all(Path(p).exists() for p in ['.env.example','.gitignore','Dockerfile','interfaz/Dockerfile'])),('sin secretos',not buscar())]
    if incluir_revision:
        p=Path('docs/verificacion_cruzada.md');r.append(('revisión por par confirmada',p.exists() and 'CONFIRMADA POR REVISOR' in p.read_text(encoding='utf-8-sig')))
    return r


if __name__=='__main__':
    r=comprobar('--sin-revision' not in sys.argv)
    for n,v in r:print('PASA' if v else 'FALLA',n)
    print(sum(v for _,v in r),'de',len(r),'comprobaciones cumplidas');raise SystemExit(not all(v for _,v in r))
