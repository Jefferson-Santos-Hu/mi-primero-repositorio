import sys
import httpx
from datetime import date
from pathlib import Path
from casos import CASOS,ejecutar_caso


def verificar_cobertura(casos):
    errores=[]
    if sum(c['id'].startswith('V-') for c in casos)<3:errores.append('Se requieren 3 válidos')
    invalidos=[c for c in casos if c['id'].startswith('I-')]
    if len(invalidos)<5:errores.append('Se requieren 5 inválidos')
    if not {404,405,422}<={c['estado'] for c in invalidos}:errores.append('Faltan estados 404,405,422')
    return errores


def registrar(base='http://127.0.0.1:8000'):
    errores=verificar_cobertura(CASOS)
    if errores:raise ValueError('; '.join(errores))
    lineas=['# Registro de pruebas de la API',f'Fecha: {date.today()}',f'Servicio probado: {base}; cliente httpx externo sobre Uvicorn real.','', '| Caso | Descripción | Petición | Esperado | Obtenido | Resultado |','|---|---|---|---|---|---|']
    cumplidos=0
    with httpx.Client(base_url=base,timeout=120) as cliente:
        for caso in CASOS:
            ok,estado,_=ejecutar_caso(cliente,caso);cumplidos+=ok
            lineas.append(f"| {caso['id']} | {caso['descripcion']} | {caso['metodo']} {caso['ruta']} | {caso['estado']} | {estado} | {'PASA' if ok else 'FALLA'} |")
    lineas.insert(3,f'Resultado: {cumplidos} de {len(CASOS)} casos cumplidos')
    Path('docs/registro_pruebas.md').write_text('\n'.join(lineas)+'\n',encoding='utf8')
    return cumplidos,len(CASOS)


if __name__=='__main__':
    bien,total=registrar(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000')
    print(f'{bien} de {total} casos cumplidos');raise SystemExit(0 if bien==total else 1)
