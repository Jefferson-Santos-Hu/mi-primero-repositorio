from fastapi.testclient import TestClient
from api import crear_app
from unittest.mock import Mock


def test_contrato_validacion_no_invoca_modelo():
    servicio=Mock()
    with TestClient(crear_app(servicio)) as c:
        assert c.post('/consultas',json={'pregunta':17}).status_code==422
    servicio.consultar.assert_not_called()


def test_error_no_filtra_proveedor():
    servicio=Mock();servicio.consultar.side_effect=RuntimeError('CLAVE_PRIVADA')
    with TestClient(crear_app(servicio)) as c:
        r=c.post('/consultas',json={'pregunta':'HTTP 429'})
    assert r.status_code==503 and 'CLAVE_PRIVADA' not in r.text


def test_metodo_no_permitido_uniforme():
    with TestClient(crear_app(Mock())) as c:
        r=c.delete('/salud')
    assert r.status_code==405 and r.json()['codigo']=='error_http'
