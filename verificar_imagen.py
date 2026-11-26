import json,time
from pathlib import Path
from docker_util import docker


def verificar():
    nombre='asistente-tecnico-comprobacion'
    identificador=docker('run','-d','--name',nombre,'-e','MODELO=simulado','asistente-tecnico-api:1.0.0').strip()
    try:
        usuario=docker('inspect','--format','{{.Config.User}}',identificador).strip()
        salud=''
        for _ in range(30):
            salud=docker('inspect','--format','{{.State.Health.Status}}',identificador).strip()
            if salud=='healthy':break
            time.sleep(1)
        assert salud=='healthy' and usuario not in {'','root','0'}
        contenido=docker('exec',identificador,'python','-c',"import pathlib; print(any(p.name=='.env' for p in pathlib.Path('/app').rglob('*')))")
        assert contenido.strip()=='False'
        respuesta=json.loads(docker('exec',identificador,'python','-c',"import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/salud').read().decode())"))
        assert respuesta['modelo_activo']=='simulado'
        evidencia={'salud':salud,'usuario':usuario,'env_en_imagen':False,'modo':respuesta['modelo_activo'],'imagen':docker('image','inspect','--format','{{.Id}}','asistente-tecnico-api:1.0.0').strip()}
        Path('docs/imagen_evidencia.json').write_text(json.dumps(evidencia,indent=2),encoding='utf8');print('Imagen verificada sin secretos y sin root')
    finally:
        docker('rm','-f',identificador)


if __name__=='__main__':verificar()
