"""Escanea archivos públicos; nunca imprime coincidencias ni valores secretos."""
import re,subprocess
from pathlib import Path
from dotenv import dotenv_values


def buscar(rutas=None):
    rutas=rutas if rutas is not None else subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],text=True).splitlines()
    secretos=[v for k,v in dotenv_values('.env').items() if ('KEY' in k or 'TOKEN' in k) and v]
    hallazgos=[]
    for nombre in rutas:
        p=Path(nombre)
        if not p.is_file():continue
        contenido=p.read_bytes()
        if re.search(rb'AIza[0-9A-Za-z_-]{35}',contenido) or any(v.encode() in contenido for v in secretos):hallazgos.append(nombre)
    return hallazgos


if __name__=='__main__':
    encontrados=buscar();print('Escaneo público:',len(encontrados),'archivos con coincidencias')
    for nombre in encontrados:print('REVISAR:',nombre)
    raise SystemExit(bool(encontrados))
