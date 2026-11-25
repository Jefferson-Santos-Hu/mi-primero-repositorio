"""Limpieza y evaluación léxica; no evalúa verdad, orden ni significado."""
from collections import Counter
import re
import unicodedata


def limpiar_texto(texto: str) -> str:
    if not isinstance(texto,str):
        raise ValueError("El texto debe ser un string.")
    normalizado=unicodedata.normalize('NFC',texto).lower()
    return ' '.join(re.sub(r'[^\w\s]',' ',normalizado).split())


def tokenizar(texto_limpio: str) -> list[str]:
    return texto_limpio.split()


def procesar_texto(texto: str) -> list[str]:
    return tokenizar(limpiar_texto(texto))


def calcular_precision_cobertura_f1(tokens_referencia,tokens_respuesta):
    referencia,respuesta=Counter(tokens_referencia),Counter(tokens_respuesta)
    coincidencias=sum((referencia & respuesta).values())
    precision=coincidencias/sum(respuesta.values()) if respuesta else 0
    cobertura=coincidencias/sum(referencia.values()) if referencia else 0
    f1=2*precision*cobertura/(precision+cobertura) if precision+cobertura else 0
    return {'precision':precision,'cobertura':cobertura,'f1':f1}


def calcular_metricas(texto_referencia,texto_respuesta):
    return calcular_precision_cobertura_f1(procesar_texto(texto_referencia),procesar_texto(texto_respuesta))


def resumir_metricas(resultados):
    return {clave+'_promedio':sum(r[clave] for r in resultados)/len(resultados) if resultados else 0 for clave in ('precision','cobertura','f1')}
