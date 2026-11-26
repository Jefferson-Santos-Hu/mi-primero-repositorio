"""Invocaciones acotadas de Docker sin volcar configuración ni secretos."""
import os,shutil,subprocess
from pathlib import Path


def ejecutable():
    ruta=shutil.which('docker')
    if ruta:return ruta
    candidatos=[Path(os.getenv('LOCALAPPDATA',''))/'Programs/DockerDesktop/resources/bin/docker.exe',Path('C:/Program Files/Docker/Docker/resources/bin/docker.exe')]
    for p in candidatos:
        if p.exists():return str(p)
    raise RuntimeError('Docker CLI no disponible')


def docker(*args,timeout=180):
    ruta=ejecutable();env={**os.environ,'PATH':str(Path(ruta).parent)+os.pathsep+os.environ.get('PATH','')}
    r=subprocess.run([ruta,*args],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=timeout,env=env)
    if r.returncode:
        raise RuntimeError(f'Docker falló en {args[0]} (código {r.returncode}); revisar Docker Desktop y los registros locales')
    return r.stdout
