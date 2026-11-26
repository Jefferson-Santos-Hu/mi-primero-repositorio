"""Genera una ficha inicial solo si el destino no existe."""
from pathlib import Path
ESQUELETO='''# Ficha de Diseño Funcional

## 1. Problema de negocio
[COMPLETAR: usuario, problema y resultado esperado]

## 2. Requerimientos y alcance (MVP)
[COMPLETAR: RF, RNF y alcance]

## 3. Arquitectura de la solución
[COMPLETAR: decisiones y diagrama]

## 4. Criterios de aceptación
[COMPLETAR: criterios observables]

## 5. Plan de construcción por hitos
[COMPLETAR: horas, margen y dependencias]
'''


def crear(ruta='docs/ficha_diseno_funcional.md'):
    p=Path(ruta)
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf8') as f:f.write(ESQUELETO)
    return p


if __name__=='__main__':
    try:print('Ficha creada:',crear())
    except FileExistsError:raise SystemExit('La ficha ya existe: no se sobrescribe el trabajo completado.')
