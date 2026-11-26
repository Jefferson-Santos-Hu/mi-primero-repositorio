"""Tres fallos provocados solo en clones temporales del repositorio."""
import json,os,subprocess,sys,tempfile,uuid
from pathlib import Path


def ejecutar():
    resultados=[]
    for caso in ['README ausente','clave sintética detectada','ruta cambiada']:
        destino=Path(tempfile.gettempdir())/('skillnest-gate-fallo-'+uuid.uuid4().hex[:10])
        assert destino.resolve().is_relative_to(Path(tempfile.gettempdir()).resolve())
        subprocess.run(['git','clone','--quiet',str(Path.cwd()),str(destino)],check=True,timeout=60)
        if caso=='README ausente':(destino/'README.md').unlink()
        elif caso=='clave sintética detectada':(destino/'docs/clave_sintetica.txt').write_text('AIza'+'X'*35,encoding='utf8')
        else:
            p=destino/'api.py';s=p.read_text(encoding='utf-8-sig').replace("@app.get('/salud',","@app.get('/salud-cambiada',");p.write_text(s,encoding='utf8')
            subprocess.run(['git','add','api.py'],cwd=destino,check=True)
            subprocess.run(['git','-c','user.name=Ensayo automatizado','-c','user.email=ensayo@example.invalid','commit','--quiet','-m','introduce defecto de ruta en copia'],cwd=destino,check=True)
        orden=[sys.executable,'verificar_gate3.py']+(['--preflight'] if caso!='ruta cambiada' else [])
        r=subprocess.run(orden,cwd=destino,capture_output=True,text=True,encoding='utf8',errors='replace',env={**os.environ,'PYTHONUTF8':'1'},timeout=180)
        esperado='FALTA:' if caso=='README ausente' else 'FALLA NC-4' if caso=='clave sintética detectada' else 'NO APRUEBA'
        detectado=r.returncode==1 and esperado in r.stdout
        if caso=='ruta cambiada':detectado=detectado and 'NC-2' in r.stdout
        resultados.append({'caso':caso,'codigo':r.returncode,'detectado':detectado,'senal_esperada':esperado})
        print(caso,':','detectado' if detectado else 'no detectado',flush=True)
    Path('docs/fallos_gate3_evidencia.json').write_text(json.dumps(resultados,ensure_ascii=False,indent=2),encoding='utf8')
    return all(r['detectado'] for r in resultados)


if __name__=='__main__':raise SystemExit(not ejecutar())
