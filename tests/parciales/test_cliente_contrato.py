from unittest.mock import Mock,patch
import pytest
from cliente import enviar_peticion,con_reintento,registrar_costo


def test_contrato_http_401_no_se_reintenta():
    respuesta=Mock(status_code=401)
    with patch('cliente.requests.post',return_value=respuesta) as enviar:
        with pytest.raises(ValueError):enviar_peticion('https://ejemplo.invalid',{}, {})
    assert enviar.call_count==1


def test_backoff_no_duerme_despues_del_ultimo_intento():
    f=Mock(side_effect=TimeoutError())
    with patch('cliente.time.sleep') as dormir:
        with pytest.raises(TimeoutError):con_reintento(f,intentos=2)
    assert f.call_count==2 and dormir.call_count==1


def test_costo_exige_uso_real():
    with pytest.raises(ValueError):registrar_costo({})
