"""Bloque 14: pruebas deterministas del cliente, sin red ni esperas reales."""
from unittest.mock import Mock, patch
import pytest
import requests
import cliente


@pytest.fixture(autouse=True)
def reiniciar(monkeypatch):
    monkeypatch.setattr(cliente, "costo_total_sesion", 0.0)


@pytest.mark.parametrize("codigo", [400, 401, 403])
def test_enviar_peticion_credencial_o_configuracion_invalida(codigo):
    with patch.object(cliente.requests, "post", return_value=Mock(status_code=codigo)):
        with pytest.raises(ValueError):
            cliente.enviar_peticion("https://servicio", {}, {})


@pytest.mark.parametrize("codigo", [429, 500, 503])
def test_enviar_peticion_fallo_transitorio(codigo):
    with patch.object(cliente.requests, "post", return_value=Mock(status_code=codigo)):
        with pytest.raises(TimeoutError):
            cliente.enviar_peticion("https://servicio", {}, {})


@pytest.mark.parametrize("error", [requests.Timeout(), requests.ConnectionError()])
def test_enviar_peticion_error_red(error):
    with patch.object(cliente.requests, "post", side_effect=error):
        with pytest.raises(TimeoutError):
            cliente.enviar_peticion("https://servicio", {}, {})


def test_enviar_peticion_exito_y_json_invalido():
    respuesta = Mock(status_code=200)
    respuesta.json.return_value = {"dato": 1}
    with patch.object(cliente.requests, "post", return_value=respuesta):
        assert cliente.enviar_peticion("https://servicio", {}, {}) == {"dato": 1}
        respuesta.json.side_effect = requests.exceptions.JSONDecodeError("invalido", "x", 0)
        with pytest.raises(RuntimeError, match="JSON"):
            cliente.enviar_peticion("https://servicio", {}, {})


def test_con_reintento_recupera_y_usa_backoff_con_techo():
    operacion = Mock(side_effect=[TimeoutError(), TimeoutError(), "correcto"])
    with patch.object(cliente.time, "sleep") as dormir, patch.object(cliente.random, "uniform", return_value=0):
        assert cliente.con_reintento(operacion, espera_base=2, espera_maxima=3) == "correcto"
    assert [llamada.args[0] for llamada in dormir.call_args_list] == [2, 3]


def test_con_reintento_agota_intentos():
    operacion = Mock(side_effect=TimeoutError("simulado"))
    with patch.object(cliente.time, "sleep") as dormir, pytest.raises(TimeoutError):
        cliente.con_reintento(operacion)
    assert operacion.call_count == 3
    assert dormir.call_count == 2


def test_con_reintento_no_reintenta_value_error():
    operacion = Mock(side_effect=ValueError("credencial"))
    with patch.object(cliente.time, "sleep") as dormir, pytest.raises(ValueError):
        cliente.con_reintento(operacion)
    assert operacion.call_count == 1
    dormir.assert_not_called()


@pytest.mark.parametrize("argumentos", [{"intentos":0}, {"espera_base":-1}, {"espera_maxima":float('inf')}])
def test_configuracion_reintentos_invalida(argumentos):
    with pytest.raises(ValueError):
        cliente.con_reintento(lambda: None, **argumentos)


def test_registrar_costo_acumula_entrada_salida_y_razonamiento():
    respuesta = {"usageMetadata": {"promptTokenCount":1000,"candidatesTokenCount":100,"thoughtsTokenCount":100}}
    assert cliente.registrar_costo(respuesta) == pytest.approx(0.0008)
    cliente.registrar_costo(respuesta)
    assert cliente.costo_total_sesion == pytest.approx(0.0016)


def test_no_inventa_costo_si_faltan_tokens():
    with pytest.raises(ValueError, match="tokens"):
        cliente.registrar_costo({})
    assert cliente.costo_total_sesion == 0


def test_consultar_modelo_orquesta_y_oculta_reintentos():
    respuesta = {"candidates":[{"content":{"parts":[{"text":"Santiago"}]}}],"usageMetadata":{"promptTokenCount":10,"candidatesTokenCount":2}}
    with patch.object(cliente, "armar_peticion", return_value=("url",{},{})), patch.object(cliente,"con_reintento",return_value=respuesta) as reintentar:
        assert cliente.consultar_modelo("Capital de Chile") == "Santiago"
    reintentar.assert_called_once()
    assert cliente.costo_total_sesion > 0


def test_consultar_modelo_convierte_agotamiento():
    with patch.object(cliente,"armar_peticion",return_value=("url",{},{})), patch.object(cliente,"con_reintento",side_effect=TimeoutError()), pytest.raises(RuntimeError,match="intentos"):
        cliente.consultar_modelo("Pregunta")
