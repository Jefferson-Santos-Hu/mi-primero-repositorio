"""Comprobación estructural/numérica de citas; no prueba implicación semántica."""
import re,unicodedata


def normalizar(texto):
    s=unicodedata.normalize('NFKC',texto).casefold()
    for palabra,numero in [('tres','3'),('dos','2'),('treinta','30')]:s=re.sub(r'\b'+palabra+r'\b',numero,s)
    return s


def comprobar_fundamentacion(texto,documentos):
    indices={int(x) for x in re.findall(r'\[(\d+)\]',texto)}
    if not indices:return {'valida':False,'motivo':'sin_citas'}
    if any(n<1 or n>len(documentos) for n in indices):return {'valida':False,'motivo':'cita_inexistente'}
    contexto=' '.join(documentos[n-1].page_content for n in indices)
    respuesta=normalizar(re.sub(r'\[\d+\]','',texto));fuente=normalizar(contexto)
    numeros=set(re.findall(r'\b\d+(?:[.,]\d+)?\b',respuesta))
    soportados=set(re.findall(r'\b\d+(?:[.,]\d+)?\b',fuente))
    if not numeros<=soportados:return {'valida':False,'motivo':'numero_no_sustentado'}
    if re.search(r'\b(401|403)\b',respuesta) and 'reintent' in respuesta and not re.search(r'\b(no|nunca|sin)\b',respuesta):
        return {'valida':False,'motivo':'contradiccion_autenticacion'}
    palabras=set(re.findall(r'\w{4,}',respuesta));base=set(re.findall(r'\w{4,}',fuente))
    coincidencia=len(palabras&base)/len(palabras) if palabras else 0
    return {'valida':coincidencia>=.20,'motivo':'control_estructural_superado' if coincidencia>=.20 else 'bajo_solapamiento','solapamiento':coincidencia}
