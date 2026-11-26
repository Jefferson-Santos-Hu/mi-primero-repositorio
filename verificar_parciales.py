"""Comprueba plan, contratos y resultados de defectos; ejecuta pruebas aisladas."""
import ast,json,subprocess,sys
from pathlib import Path
from verificar_defectos import MUTACIONES


def comprobar():
    resultados=json.loads(Path('docs/defectos_resultados.json').read_text(encoding='utf8'));plan=Path('docs/pruebas_parciales.md').read_text(encoding='utf8')
    errores=[]
    for componente,_,_,_,archivo in MUTACIONES:
        funciones=[n.name for n in ast.walk(ast.parse(Path(archivo).read_text(encoding='utf-8-sig'))) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
        if len(funciones)<3 or not any(f.startswith('test_contrato') for f in funciones):errores.append(componente+' sin 3 pruebas y contrato')
        if componente not in plan or archivo not in plan:errores.append(componente+' falta en plan')
    if not all(r['detectado'] for r in resultados):errores.append('Hay defectos no detectados')
    r=subprocess.run([sys.executable,'-m','pytest','tests/parciales','-q'],capture_output=True,text=True,encoding='utf8',errors='replace')
    if r.returncode:errores.append('Pruebas parciales fallan')
    return errores


if __name__=='__main__':
    errores=comprobar()
    for e in errores:print('FALLA',e)
    print('Plan y contratos verificados' if not errores else 'Plan con fallos');raise SystemExit(bool(errores))
