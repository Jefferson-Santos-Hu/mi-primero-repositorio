"""Validación compartida por la miniaplicación y la prueba de prompts."""
import math


def validar_estructura(valor, esquema, ruta="respuesta"):
    """Valida el subconjunto del esquema usado por este banco, no JSON Schema general."""
    tipo = esquema["type"]
    if tipo == "OBJECT":
        propiedades = esquema["properties"]
        if not isinstance(valor, dict) or not set(esquema["required"]) <= set(valor) or not set(valor) <= set(propiedades):
            raise ValueError(f"{ruta}: faltan claves requeridas o aparecen claves inesperadas.")
        for clave, dato in valor.items():
            validar_estructura(dato, propiedades[clave], f"{ruta}.{clave}")
    elif tipo == "STRING":
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{ruta}: se esperaba un string no vacío.")
    elif tipo in ("NUMBER", "INTEGER"):
        valido = type(valor) is int if tipo == "INTEGER" else type(valor) in (int, float)
        if not valido or not math.isfinite(valor):
            raise ValueError(f"{ruta}: se esperaba un {tipo.lower()} finito, no booleano.")
        if valor < esquema.get("minimum", -math.inf) or valor > esquema.get("maximum", math.inf):
            raise ValueError(f"{ruta}: número fuera del intervalo permitido.")
    elif tipo == "ARRAY":
        if not isinstance(valor, list) or not esquema.get("minItems", 0) <= len(valor) <= esquema.get("maxItems", math.inf):
            raise ValueError(f"{ruta}: lista inválida o longitud incorrecta.")
        for indice, item in enumerate(valor):
            validar_estructura(item, esquema["items"], f"{ruta}[{indice}]")
    else:
        raise ValueError(f"{ruta}: tipo de esquema no implementado.")
    if "enum" in esquema and valor not in esquema["enum"]:
        raise ValueError(f"{ruta}: valor fuera de las opciones permitidas.")
