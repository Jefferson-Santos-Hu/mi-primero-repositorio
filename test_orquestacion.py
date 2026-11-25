from unittest.mock import Mock
import pytest
from langchain_core.runnables import RunnableLambda
from cadena_tres_pasos import construir_cadena
from enrutamiento import construir_cadena_con_enrutamiento, construir_cadena_queja_segura, procesar_mensaje_seguro, normalizar_categoria


def test_tres_pasos_consumen_salida_anterior():
    modelo=Mock(side_effect=['diagnostico único','borrador único','respuesta revisada'])
    resultado=construir_cadena(modelo).invoke({'texto':'Python falla con HTTP 429'})
    assert resultado=='respuesta revisada'
    assert modelo.call_count==3
    assert 'diagnostico único' in str(modelo.call_args_list[1].args[0])
    assert 'borrador único' in str(modelo.call_args_list[2].args[0])


@pytest.mark.parametrize('categoria',['credenciales','limite_uso','otra'])
def test_enrutamiento_y_ruta_por_defecto(categoria):
    modelo=Mock(return_value='respuesta normal')
    clasificador=RunnableLambda(lambda _:categoria)
    cadena=construir_cadena_con_enrutamiento(modelo,clasificador)
    assert cadena.invoke({'mensaje':'necesito ayuda'})=='respuesta normal'
    assert modelo.call_count==1
    esperado={'credenciales':'autenticación','limite_uso':'cuota'}.get(categoria,'Python')
    assert esperado in str(modelo.call_args.args[0])


def test_normalizacion_categoria():
    assert normalizar_categoria(' "CREDENCIALES"\n')=='credenciales'


def test_fallback_ruta_especifica():
    def fallar(_):
        raise ConnectionError('simulado')
    cadena=construir_cadena_queja_segura(RunnableLambda(fallar))
    assert 'equipo' in cadena.invoke({'mensaje':'error'})


def test_fallo_clasificacion_se_controla(caplog):
    def fallar(_):
        raise ConnectionError('contenido sensible que no debe aparecer')
    cadena=construir_cadena_con_enrutamiento(Mock(),RunnableLambda(fallar))
    assert 'No pudimos procesar' in procesar_mensaje_seguro(cadena,'texto')
    assert 'ConnectionError' in caplog.text
    assert 'contenido sensible' not in caplog.text
