import hashlib,json,subprocess,sys
from pathlib import Path
from riesgos import RIESGOS
from gobernanza import categoria_riesgo


def huella():return hashlib.sha256(json.dumps(RIESGOS,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def generar():
    lineas=['# Matriz de riesgos verificada',f'Huella: {huella()}','','Estimaciones de diseño, no probabilidades medidas. Un estado parcial mantiene residual alto.','', '| ID | Riesgo | P | I | Inicial | Mitigación | Evidencia ejecutable | Estado | Residual | Supervisión |','|---|---|---|---|---|---|---|---|---|---|']
    for r in sorted(RIESGOS,key=lambda x:-x['residual']):
        lineas.append(f"| {r['id']} | {r['riesgo']} | {r['probabilidad']} | {r['impacto']} | {r['probabilidad']*r['impacto']} | {r['mitigacion']} | {', '.join(r['evidencia'])} | {r['estado']} | {r['residual']} {categoria_riesgo(r['residual'])} | {r['supervision']} |")
    lineas+=['','R-01 y R-06 son parciales: A-07 y H-04 documentan evasiones, no éxitos de mitigación. R-09 prueba la pausa, no identidad del revisor ni persistencia durable. No se inventa una revisión de Javier; sigue pendiente.','', 'El prompt vigente y la pausa del Gate 2 siguen en docs/registro_prompts.json y gobernanza.py. La matriz se amplía para el Módulo 3, sin borrar la evidencia histórica del Gate 2.']
    Path('docs/matriz_riesgos.md').write_text('\n'.join(lineas)+'\n',encoding='utf8')


def comprobar(ejecutar=True):
    evidencia=sorted({p for r in RIESGOS for p in r['evidencia']})
    pruebas=subprocess.run([sys.executable,'-m','pytest','-q',*evidencia],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=120) if ejecutar else None
    return [('campos y cantidad',len(RIESGOS)>=6 and all({'id','riesgo','probabilidad','impacto','mitigacion','evidencia','estado','residual','supervision'}<=set(r) for r in RIESGOS)),('escala',all(1<=r['probabilidad']<=5 and 1<=r['impacto']<=5 and 1<=r['residual']<=r['probabilidad']*r['impacto'] for r in RIESGOS)),('evidencia ejecutada',pruebas is not None and pruebas.returncode==0),('parciales honestos',all(r['estado']!='parcial' or (r['limites'] and r['residual']>=9) for r in RIESGOS)),('supervision',all(r['residual']<9 or bool(r['supervision']) for r in RIESGOS)),('registro vigente',huella() in Path('docs/matriz_riesgos.md').read_text(encoding='utf8'))]


if __name__=='__main__':
    if '--generar' in sys.argv:generar()
    r=comprobar()
    for n,v in r:print('PASA' if v else 'FALLA',n)
    print(sum(v for _,v in r),'de',len(r),'reglas cumplidas');raise SystemExit(not all(v for _,v in r))
