import json,sys
from pathlib import Path
from ejecutar_escenarios import ejecutar,huella
from matriz_pruebas import MATRIZ
from ficha_datos import leer_ficha


def generar():
    r=ejecutar()
    lineas=['# Matriz de pruebas',f"Modo: {r['modo']}",f"Huella: {r['huella']}",'', '| ID | Tipo | Requisitos | Esperado | Obtenido | Resultado | Hallazgo |','|---|---|---|---|---|---|---|']
    for m,x in zip(MATRIZ,r['resultados']):
        lineas.append(f"| {m['id']} | {m['tipo']} | {', '.join(m['requisitos'])} | {x['esperado']} | {x['estado']} | {'PASA' if x['pasa'] else 'FALLA'} | {'Sin hallazgo' if x['pasa'] else 'Contrato incumplido: revisar escenario '+x['id']} |")
    Path('docs/matriz_pruebas.md').write_text('\n'.join(lineas)+'\n',encoding='utf8')


def comprobar():
    r=json.loads(Path('docs/escenarios_resultados.json').read_text(encoding='utf8'));texto=Path('docs/matriz_pruebas.md').read_text(encoding='utf8')
    cubiertos={rf for m in MATRIZ for rf in m['requisitos']}
    return [('cuatro o más',len(MATRIZ)>=4),('tipos',{'válido','inválido','borde'}<={m['tipo'] for m in MATRIZ}),('alcance cubierto',leer_ficha()['imprescindibles']<=cubiertos),('huella vigente',r['huella']==huella() and huella() in texto),('registros completos',all(m['id'] in texto for m in MATRIZ)),('hallazgos',all(x['pasa'] or 'Contrato incumplido: revisar escenario '+x['id'] in texto for x in r['resultados']))]


if __name__=='__main__':
    if '--generar' in sys.argv:generar()
    r=comprobar()
    for n,ok in r:print('PASA' if ok else 'FALLA',n)
    print(sum(v for _,v in r),'de',len(r),'reglas cumplidas');raise SystemExit(not all(v for _,v in r))
