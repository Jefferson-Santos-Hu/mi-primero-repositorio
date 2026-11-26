"""Lectura de la ficha: referencias e hitos comprobables, sin acreditar revisiones."""
import re
from pathlib import Path


def leer_ficha(ruta='docs/ficha_diseno_funcional.md'):
    texto=Path(ruta).read_text(encoding='utf-8-sig')
    requerimientos=set(re.findall(r'^- ((?:RF|RNF)-\d+):',texto,re.M))
    imprescindibles=set(re.findall(r'RF-\d+',re.search(r'Imprescindible:(.*)',texto).group(1)))
    criterios={m[0]:{'requisito':m[1],'texto':m[2]} for m in re.findall(r'^\| (CA-\d+) \| ((?:RF|RNF)-\d+) \| ([^\n]+)',texto,re.M)}
    hitos=re.findall(r'^- (H\d+) \(([\d.]+) h\): (.+)$',texto,re.M)
    return {'texto':texto,'requerimientos':requerimientos,'imprescindibles':imprescindibles,'criterios':criterios,'hitos':hitos}


def validar_ficha(ruta='docs/ficha_diseno_funcional.md',completa=True):
    errores=[]
    try:d=leer_ficha(ruta)
    except (OSError,AttributeError):return ['Ficha ausente o estructura inválida']
    for n in range(1,6 if completa else 4):
        if f'## {n}.' not in d['texto']:errores.append(f'Falta sección {n}')
    if '[COMPLETAR' in d['texto']:errores.append('Hay marcas sin completar')
    if not Path('docs/diagrama_arquitectura.png').exists():errores.append('Falta diagrama')
    if completa:
        obligatorios=d['imprescindibles']|{r for r in d['requerimientos'] if r.startswith('RNF-')}
        cubiertos={v['requisito'] for v in d['criterios'].values()}
        for r in obligatorios-cubiertos:errores.append(r+' no tiene criterio')
        for c,valor in d['criterios'].items():
            if valor['requisito'] not in d['requerimientos']:errores.append(c+' referencia desconocida')
        if not 3<=len(d['hitos'])<=6:errores.append('Se requieren 3 a 6 hitos')
        for h,horas,t in d['hitos']:
            if not re.search(r'CA-\d+',t):errores.append(h+' sin criterio')
        citados=set(re.findall(r'CA-\d+',' '.join(t for _,_,t in d['hitos'])))
        if set(d['criterios'])-citados:errores.append('Criterios sin hito')
        disponibles=re.search(r'Horas disponibles: ([\d.]+) h',d['texto']);margen=re.search(r'Margen de imprevistos: ([\d.]+) h',d['texto'])
        if not disponibles or not margen:errores.append('Falta presupuesto de horas')
        elif sum(float(h) for _,h,_ in d['hitos'])>float(disponibles[1])-float(margen[1]):errores.append('Hitos exceden presupuesto')
    return errores
