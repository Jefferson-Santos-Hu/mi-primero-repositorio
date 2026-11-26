from pathlib import Path
import re


def comprobar(ruta='Dockerfile'):
    s=Path(ruta).read_text(encoding='utf-8-sig');ignore=Path('.dockerignore').read_text(encoding='utf-8-sig')
    reglas=[('base fija',bool(re.search(r'^FROM .*@sha256:[a-f0-9]{64}',s,re.M))),('dependencias antes de código',s.find('COPY requirements.txt') < s.find('RUN pip install') < min((m.start() for m in re.finditer(r'^COPY (?!requirements\.txt)',s,re.M)),default=-1) and 'pip install --no-cache-dir' in s),('usuario sin privilegios',bool(re.search(r'^USER (?!root\b)\S+',s,re.M))),('salud','HEALTHCHECK' in s),('host externo','0.0.0.0' in s),('secretos fuera',all(x in ignore.splitlines() for x in ['.env','.git','venv'])),('sin clave ni copia global','COPY . ' not in s and 'API_KEY=' not in s)]
    return reglas


if __name__=='__main__':
    r=comprobar()
    for nombre,ok in r:print('PASA' if ok else 'FALLA',nombre)
    print(sum(ok for _,ok in r),'de',len(r),'comprobaciones cumplidas');raise SystemExit(not all(ok for _,ok in r))
