"""Ensayo desde un checkout limpio y un venv nuevo, sin credenciales reales."""
import json,os,socket,subprocess,sys,tempfile,time,uuid
from pathlib import Path
import httpx
from registrar_ejecucion import huella_codigo


def ejecutar():
    raiz=Path.cwd();destino=Path(tempfile.gettempdir())/('skillnest-frio-'+uuid.uuid4().hex[:10])
    commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    subprocess.run(['git','clone','--quiet',str(raiz),str(destino)],check=True,timeout=60)
    subprocess.run([sys.executable,'-m','venv',str(destino/'venv')],check=True,timeout=60)
    py=destino/'venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
    subprocess.run([str(py),'-m','pip','install','-r','requirements-dev.txt','--quiet'],cwd=destino,check=True,timeout=420)
    pruebas=subprocess.run([str(py),'-m','pytest','-q'],cwd=destino,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=120)
    if pruebas.returncode:raise RuntimeError('Las pruebas fallaron en el clon limpio')
    env={k:v for k,v in os.environ.items() if k not in {'API_KEY','GEMINI_API_KEY','GOOGLE_API_KEY'}}
    env.update({'MODELO':'simulado','CARGAR_DOTENV':'false','LANGSMITH_TRACING':'false','LANGCHAIN_TRACING_V2':'false'})
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0));puerto=sock.getsockname()[1]
    p=subprocess.Popen([str(py),'-m','uvicorn','api:app','--host','127.0.0.1','--port',str(puerto)],cwd=destino,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                salud=httpx.get(f'http://127.0.0.1:{puerto}/salud',timeout=1)
                if salud.status_code==200:break
            except httpx.RequestError:pass
            time.sleep(.25)
        else:raise RuntimeError('No arrancó el clon limpio')
        r=httpx.post(f'http://127.0.0.1:{puerto}/consultas',json={'pregunta':'HTTP 429'},timeout=10)
        assert r.status_code==200 and 'cliente.md' in r.json()['fuentes']
        evidencia={'commit':commit,'huella_codigo':huella_codigo(),'venv_nuevo':True,'instalacion':True,'pruebas':True,'salud':salud.status_code,'consulta':r.status_code,'fuentes':r.json()['fuentes'],'modo':'simulado','nota':'Clon local del commit con venv nuevo, sin clave real. No es ejecución por Javier ni otro sistema operativo.'}
        Path('docs/frio_evidencia.json').write_text(json.dumps(evidencia,ensure_ascii=False,indent=2),encoding='utf8')
        print('5 de 5 comprobaciones cumplidas: clon, instalación, pruebas, salud y consulta')
    finally:
        p.terminate()
        try:p.wait(timeout=5)
        except subprocess.TimeoutExpired:p.kill();p.wait()


if __name__=='__main__':
    if '--comprobar' in sys.argv:
        p=Path('docs/frio_evidencia.json');r=json.loads(p.read_text(encoding='utf8')) if p.exists() else {}
        ok=r.get('huella_codigo')==huella_codigo() and all(r.get(c) for c in ['venv_nuevo','instalacion','pruebas']) and r.get('consulta')==200
        print('Ensayo en frío vigente' if ok else 'FALLA: repetir probar_en_frio.py');raise SystemExit(not ok)
    ejecutar()
