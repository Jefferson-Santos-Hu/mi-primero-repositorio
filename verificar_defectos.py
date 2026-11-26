"""Mutaciones controladas en copias temporales, nunca en el proyecto activo."""
import json,os,subprocess,sys,tempfile,shutil
from pathlib import Path
MUTACIONES=[
('cliente','cliente.py','if respuesta.status_code in (400,401,403):','if respuesta.status_code in (400,403):','tests/parciales/test_cliente_contrato.py'),
('recuperacion','indexar_documentos.py',"citas[i]=fuente","citas[i]='inventada.md'",'tests/parciales/test_recuperar.py'),
('modelo','modelo_simulado.py',"'modo':'simulado'","'modo':'real'",'tests/parciales/test_modelo.py'),
('api','api.py','status_code=422','status_code=200','tests/parciales/test_api_contrato.py'),
('fundamentacion','fundamentacion.py',"if not numeros<=soportados:","if False:",'tests/parciales/test_fundamentacion.py')]


def verificar():
    raiz=Path.cwd();archivos=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],text=True).splitlines();resultados=[]
    for componente,ruta,antes,despues,prueba in MUTACIONES:
        with tempfile.TemporaryDirectory(prefix='skillnest-mutacion-') as tmp:
            destino=Path(tmp).resolve()
            assert destino.is_relative_to(Path(tempfile.gettempdir()).resolve())
            for nombre in archivos:
                origen=raiz/nombre
                if origen.suffix=='.py' and origen.is_file():
                    copia=destino/nombre;copia.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(origen,copia)
            p=destino/ruta;s=p.read_text(encoding='utf-8-sig');assert antes in s
            p.write_text(s.replace(antes,despues,1),encoding='utf8')
            r=subprocess.run([sys.executable,'-m','pytest',prueba,'-q'],cwd=destino,capture_output=True,text=True,encoding='utf8',errors='replace',env={**os.environ,'PYTHONUTF8':'1','CARGAR_DOTENV':'false'},timeout=60)
            detectado=r.returncode==1 and 'FAILED ' in r.stdout and 'ERROR collecting' not in r.stdout
            resultados.append({'componente':componente,'archivo':ruta,'prueba':prueba,'defecto':antes+' → '+despues,'detectado':detectado,'codigo':r.returncode})
    Path('docs/defectos_resultados.json').write_text(json.dumps(resultados,ensure_ascii=False,indent=2),encoding='utf8')
    print(sum(r['detectado'] for r in resultados),'de',len(resultados),'defectos detectados')
    return all(r['detectado'] for r in resultados)


if __name__=='__main__':raise SystemExit(not verificar())
