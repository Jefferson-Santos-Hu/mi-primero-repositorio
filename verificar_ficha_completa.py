import sys
from pathlib import Path
from ficha_datos import validar_ficha
if __name__=='__main__':
    errores=validar_ficha()
    revision=Path('docs/revision_alcance.md')
    if '--sin-revision' not in sys.argv:
        if not revision.exists() or 'CONFIRMADA POR REVISOR' not in revision.read_text(encoding='utf-8-sig'):
            errores.append('Revisión cruzada pendiente; no se acredita una revisión ajena')
    for e in errores:print('ERROR:',e)
    print('Ficha técnicamente coherente' if not errores else 'Ficha con pendientes')
    raise SystemExit(bool(errores))
