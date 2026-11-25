import pytest
from pipeline_texto import procesar_texto, calcular_metricas, resumir_metricas


def test_normaliza_mayusculas_puntuacion_y_espacios():
    assert procesar_texto('El Cielo, es AZUL!') == ['el','cielo','es','azul']
    assert procesar_texto('acción\n  Python') == ['acción','python']


def test_vacio_y_tipo_invalido():
    assert procesar_texto('¡¡¡...!!!') == []
    with pytest.raises(ValueError):
        procesar_texto(None)


def test_contabiliza_repeticiones_y_no_solo_sets():
    resultado=calcular_metricas('uno uno dos','uno dos dos dos')
    assert resultado['precision']==.5
    assert resultado['cobertura']==pytest.approx(2/3)
    assert resultado['f1']==pytest.approx(4/7)


@pytest.mark.parametrize('referencia,respuesta',[('',''),('hola',''),('','hola')])
def test_vacios_no_dividen_por_cero(referencia,respuesta):
    assert calcular_metricas(referencia,respuesta)=={'precision':0,'cobertura':0,'f1':0}


def test_identidad_y_resumen():
    metricas=calcular_metricas('Hola Python!','hola python')
    assert metricas=={'precision':1,'cobertura':1,'f1':1}
    assert resumir_metricas([metricas])['f1_promedio']==1
    assert resumir_metricas([])['f1_promedio']==0
