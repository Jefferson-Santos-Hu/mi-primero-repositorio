"""Registra hechos de la corrida; preserva observaciones fuera de la zona automática."""
import hashlib,json,subprocess
from pathlib import Path
from datetime import datetime,timezone


def huella_codigo():
    nombres=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],text=True).splitlines()
    archivos=sorted(n for n in nombres if (n.endswith(('.py','.js','.html')) or n in ['Dockerfile','compose.yaml','requirements.txt','requirements-dev.txt','.dockerignore','interfaz/Dockerfile','interfaz/nginx.conf']) and Path(n).is_file())
    return hashlib.sha256(''.join(n+hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in archivos).encode()).hexdigest()


def registrar():
    resultados=json.loads(Path('docs/escenarios_resultados.json').read_text(encoding='utf8'))
    commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    datos={'fecha':datetime.now(timezone.utc).isoformat(),'commit':commit,'huella_codigo':huella_codigo(),'modo':resultados['modo'],'escenarios_huella':resultados['huella'],'casos':len(resultados['resultados']),'cumplidos':sum(x['pasa'] for x in resultados['resultados'])}
    Path('docs/registro_ejecucion.json').write_text(json.dumps(datos,indent=2),encoding='utf8')
    p=Path('docs/registro_ejecucion.md');manual='''\n\n## Qué se observó
Las peticiones atravesaron Nginx y FastAPI en contenedores sanos. El modo simulado permite repetir entradas, errores y fuentes sin depender de una red externa. El modo se declara expresamente y no se confunde con una respuesta real de Gemini.

## Qué no se probó
Esta corrida de catorce escenarios usa el modelo simulado, sin medir calidad ni costo del proveedor. La evidencia real de Gemini se guarda separadamente. No prueba carga, autenticación multiusuario ni revisión independiente de un compañero.

## Siguiente paso
Ejecutar la defensa en voz alta con el alumno y confirmar por el revisor las observaciones de transferencia todavía pendientes.
'''
    if p.exists() and '<!-- AUTO:FIN -->' in p.read_text(encoding='utf-8-sig'):manual=p.read_text(encoding='utf-8-sig').split('<!-- AUTO:FIN -->',1)[1]
    auto='\n'.join(f'- {k}: {v}' for k,v in datos.items())
    p.write_text('# Registro de ejecución\n\n<!-- AUTO:INICIO -->\n'+auto+'\n<!-- AUTO:FIN -->'+manual,encoding='utf8')
    print('Registro generado:',datos['cumplidos'],'de',datos['casos'])


if __name__=='__main__':registrar()
