from langchain_core.documents import Document
from fundamentacion import comprobar_fundamentacion
DOCS=[Document(page_content='El cliente reintenta hasta tres intentos ante HTTP 429. Los errores 401 y 403 no se reintentan.')]


def test_contrato_fundamentacion_devuelve_decision():
    r=comprobar_fundamentacion('Ante HTTP 429 se usan 3 intentos [1].',DOCS)
    assert r['valida'] is True and isinstance(r['motivo'],str)


def test_rechaza_numero_inventado_y_cita():
    assert not comprobar_fundamentacion('Se usan 99 intentos [1].',DOCS)['valida']
    assert not comprobar_fundamentacion('El cliente reintenta [9].',DOCS)['valida']


def test_detecta_contradiccion_de_auth():
    assert not comprobar_fundamentacion('Se reintenta 401 [1].',DOCS)['valida']
    assert comprobar_fundamentacion('No se reintentan errores 401 [1].',DOCS)['valida']


def test_limite_parafrasis_falsa_puede_escapar():
    # Una frase falsa sin cifras y con solapamiento puede pasar: límite declarado.
    assert comprobar_fundamentacion('El cliente reintenta siempre [1].',DOCS)['valida']
