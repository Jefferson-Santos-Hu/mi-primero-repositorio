from ejecutar_escenarios import evaluar,huella
from escenarios import ESCENARIOS


def test_contrato_evaluar_estado_y_contenido():
    c=ESCENARIOS[0]
    assert evaluar(c,200,'cliente.md')
    assert not evaluar(c,503,'cliente.md')


def test_texto_incorrecto_falla():
    assert not evaluar(ESCENARIOS[0],200,'fuente inventada')


def test_huella_cambia_con_matriz():
    assert huella()!=huella(ESCENARIOS[:-1])
