"""Dataset de comportamiento: clasificación de incidentes del asistente técnico.
Preparar y validar no envía trabajos de entrenamiento ni genera cargos de tuning.
"""
import json
from collections import Counter
from google.genai import types

EJEMPLOS_RAW=[
('Gemini devuelve 401 al usar mi clave',{'categoria':'autenticacion','accion':'revisar_credenciales'}),
('Me deniega acceso con HTTP 403',{'categoria':'autenticacion','accion':'revisar_credenciales'}),
('El servidor dice API key not valid',{'categoria':'autenticacion','accion':'revisar_credenciales'}),
('Recibo 429 al enviar muchas consultas',{'categoria':'cuota','accion':'esperar_y_reintentar'}),
('RESOURCE_EXHAUSTED por límite de uso',{'categoria':'cuota','accion':'esperar_y_reintentar'}),
('Superé las peticiones por minuto',{'categoria':'cuota','accion':'esperar_y_reintentar'}),
('Se agotó el tiempo de conexión',{'categoria':'transitorio','accion':'reintentar_acotado'}),
('Gemini devuelve HTTP 503',{'categoria':'transitorio','accion':'reintentar_acotado'}),
('La red se cortó durante la petición',{'categoria':'transitorio','accion':'reintentar_acotado'}),
('Python no encuentra el módulo requests',{'categoria':'entorno','accion':'verificar_venv'}),
('pip instaló en otro intérprete',{'categoria':'entorno','accion':'verificar_venv'}),
('No encuentro venv Scripts python.exe',{'categoria':'entorno','accion':'verificar_venv'})]
ACCIONES={'autenticacion':'revisar_credenciales','cuota':'esperar_y_reintentar','transitorio':'reintentar_acotado','entorno':'verificar_venv'}


def construir_ejemplos(raw=EJEMPLOS_RAW):
    return [types.TuningExample(text_input=texto,output=json.dumps(salida,ensure_ascii=False)) for texto,salida in raw]


def chequear_balance(raw=EJEMPLOS_RAW,clave='categoria'):
    return Counter(s[clave] for _,s in raw)


def validar_dataset(ejemplos,claves_esperadas=('categoria','accion')):
    problemas=[];vistos=set()
    for i,e in enumerate(ejemplos):
        entrada=(e.text_input or '').strip().casefold()
        if not entrada: problemas.append(f'{i}: entrada vacía')
        if entrada in vistos: problemas.append(f'{i}: entrada duplicada')
        vistos.add(entrada)
        try: salida=json.loads(e.output or '')
        except (json.JSONDecodeError,TypeError):
            problemas.append(f'{i}: JSON inválido');continue
        if not isinstance(salida,dict) or set(salida)!=set(claves_esperadas):
            problemas.append(f'{i}: claves incorrectas');continue
        if ACCIONES.get(salida['categoria'])!=salida['accion']:
            problemas.append(f'{i}: categoría/acción incoherentes')
    return problemas


if __name__=='__main__':
    ejemplos=construir_ejemplos()
    print(json.dumps({'ejemplos':len(ejemplos),'balance':chequear_balance(),'problemas':validar_dataset(ejemplos)},ensure_ascii=False))
