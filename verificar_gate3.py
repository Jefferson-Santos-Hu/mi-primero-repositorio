"""Evalúa evidencia real; nunca declara aprobado lo que omitió o espera a una persona."""
import argparse,json,os,re,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
from rubrica_gate3 import CRITERIOS,NO_COMPENSABLES,ENTREGABLES,UMBRAL
from buscar_secretos import buscar
PY=sys.executable
FUENTES={
'ficha':([PY,'verificar_ficha_completa.py','--sin-revision'],False),
'decisiones':([PY,'verificar_decisiones.py'],False),
'frio':([PY,'probar_en_frio.py','--comprobar'],False),
'demo':([PY,'ensayo_demo.py'],False),
'respaldo':([PY,'ensayo_demo.py','--comprobar'],False),
'mitigaciones':([PY,'verificar_mitigaciones.py'],False),
'ia':([PY,'-m','pytest','test_gate2.py','test_orquestacion.py','test_indice_incremental.py','tests/parciales/test_fundamentacion.py','-q'],False),
'servicio':([PY,'verificar_servicio.py'],False),
'api_md':([PY,'generar_api_md.py','--comprobar'],False),
'dockerfile':([PY,'verificar_dockerfile.py'],False),
'compose':([PY,'verificar_entrega.py','--sin-revision'],False),
'pytest':([PY,'-m','pytest','-q'],False),
'matriz':([PY,'verificar_matriz.py'],False),
'parciales':([PY,'verificar_parciales.py'],False),
'riesgos':([PY,'verificar_riesgos.py'],False),
'secretos':([PY,'buscar_secretos.py'],False),
'readme':([PY,'verificar_readme.py'],False),
'transferencia':([PY,'verificar_transferencia.py','--sin-revision'],False),
'guion':([PY,'medir_guion.py'],False),
'stack':([PY,'verificar_stack.py'],True),
'ejecucion':([PY,'verificar_ejecucion.py'],True),
'registro':([PY,'verificar_registro.py'],True)}


def faltantes():return {n:[p for p in ps if not Path(p).is_file()] for n,ps in ENTREGABLES.items() if any(not Path(p).is_file() for p in ps)}


def puntuar(resultados):
    return [(c,c['peso']*sum(bool(resultados.get(f,{}).get('pasa')) for f in c['fuentes'])/len(c['fuentes'])) for c in CRITERIOS]


def no_compensables_que_fallan(resultados,omitidas):
    fallan=[]
    for nc in NO_COMPENSABLES:
        usadas=[f for f in nc['fuentes'] if f not in omitidas]
        if any(not resultados.get(f,{}).get('pasa') for f in usadas):fallan.append(nc['id'])
    return fallan


def decidir(puntaje,fallan,pendientes):
    if fallan or puntaje<UMBRAL:return 'NO APRUEBA'
    if pendientes:return 'PROVISIONAL'
    return 'APRUEBA'


def nota(p):return 1+3*p/UMBRAL if p<UMBRAL else 4+3*(p-UMBRAL)/(100-UMBRAL)


def revisiones_pendientes():
    return [n for n,p in [('Revisión de alcance','docs/revision_alcance.md'),('Revisión de composición','docs/verificacion_cruzada.md'),('Transferencia por compañero','docs/transferencia.md')] if not Path(p).exists() or 'CONFIRMADA POR REVISOR' not in Path(p).read_text(encoding='utf-8-sig')]


def evaluar(con_docker=False):
    resultados={};omitidas=[]
    for nombre,(orden,necesita_docker) in FUENTES.items():
        if necesita_docker and not con_docker:omitidas.append(nombre);continue
        try:
            r=subprocess.run(orden,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=180,env={**os.environ,'PYTHONUTF8':'1'})
            lineas=(r.stdout+r.stderr).strip().splitlines();detalle=next((x for x in lineas if x.startswith(('FALLA','ERROR','FAILED'))),lineas[-1] if lineas else 'sin salida')
            resultados[nombre]={'pasa':r.returncode==0,'codigo':r.returncode,'detalle':detalle[:300]}
        except subprocess.TimeoutExpired:resultados[nombre]={'pasa':False,'codigo':1,'detalle':'Tiempo agotado'}
        print('PASA' if resultados[nombre]['pasa'] else 'FALLA',nombre,'->',resultados[nombre]['detalle'],flush=True)
    filas=puntuar(resultados);total=sum(p for _,p in filas);fallan=no_compensables_que_fallan(resultados,omitidas)
    pendientes=omitidas+revisiones_pendientes()+['Defensa oral del alumno y confirmaciones del evaluador']
    veredicto=decidir(total,fallan,pendientes)
    return {'fecha':datetime.now(timezone.utc).isoformat(),'modo':'con Docker' if con_docker else 'sin Docker','resultados':resultados,'omitidas':omitidas,'puntaje':round(total,2),'nota':round(nota(total),2),'no_compensables_fallan':fallan,'pendientes':pendientes,'veredicto':veredicto}


def escribir(d):
    lineas=['# Informe del Gate 3',f"Fecha: {d['fecha']}",f"Modo: {d['modo']}",f"Resultado: {d['veredicto']}",f"Puntaje técnico: {d['puntaje']}/100 (umbral {UMBRAL}); nota orientativa {d['nota']}/7",'', 'El puntaje es una autoevaluación automática de fuentes ejecutadas, no calificación del instructor. Las fuentes de ficha, composición y transferencia verifican solo su parte técnica; su revisión humana está separada y pendiente. Una fuente omitida vale cero, nunca éxito.','', '| Criterio | Peso | Puntos | Evidencia |','|---|---|---|---|']
    for c,p in puntuar(d['resultados']):lineas.append(f"| {c['id']} {c['nombre']} | {c['peso']} | {p:.2f} | {', '.join(c['fuentes'])} |")
    lineas+=['','## Comprobaciones','', '| Fuente | Resultado | Detalle |','|---|---|---|']
    for f,r in d['resultados'].items():lineas.append(f"| {f} | {'PASA' if r['pasa'] else 'FALLA'} | {r['detalle'].replace('|','/')} |")
    lineas+=['','## No compensables','']
    for nc in NO_COMPENSABLES:
        estado='FALLA' if nc['id'] in d['no_compensables_fallan'] else 'requiere evaluador' if not nc['fuentes'] else 'sin verificar por completo' if set(nc['fuentes'])&set(d['omitidas']) else 'comprobado técnicamente'
        lineas.append(f"- {nc['id']}: {nc['nombre']} — {estado}.")
    lineas+=['','## Pendientes explícitos','']+[f'- {x}.' for x in d['pendientes']]
    lineas+=['','## Lo que este informe no demuestra','','No acredita que Javier haya revisado el proyecto ni que el alumno haya realizado una defensa oral. No mide calidad universal del modelo, carga, autenticación multiusuario ni seguridad de producción. La demo es simulada explícitamente; las llamadas reales se documentan por separado. Los pesos y el umbral no se modificaron para mejorar el resultado.']
    Path('docs/gate3.md').write_text('\n'.join(lineas)+'\n',encoding='utf8');Path('docs/gate3_resultados.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--con-docker',action='store_true');p.add_argument('--escribir',action='store_true');p.add_argument('--preflight',action='store_true');a=p.parse_args()
    faltan=faltantes();secretos=buscar()
    if faltan or secretos:
        if faltan:print('FALTA:',json.dumps(faltan,ensure_ascii=False))
        if secretos:print('FALLA NC-4: credencial con patrón de clave en archivo público; no se imprime su valor')
        raise SystemExit(1)
    if a.preflight:print('Preflight correcto');raise SystemExit(0)
    d=evaluar(a.con_docker)
    if a.escribir:escribir(d)
    print('Resultado:',d['veredicto'],'Puntaje técnico:',d['puntaje'],'No compensables que fallan:',d['no_compensables_fallan'])
    raise SystemExit({'APRUEBA':0,'NO APRUEBA':1,'PROVISIONAL':2}[d['veredicto']])
