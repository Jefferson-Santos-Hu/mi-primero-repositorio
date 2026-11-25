import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from api import crear_app
from casos import CASOS,ejecutar_caso


@pytest.mark.parametrize('caso',CASOS,ids=[c['id'] for c in CASOS])
def test_contrato_compartido(caso):
    servicio=Mock();servicio.consultar.return_value={'respuesta':'Backoff [1].','fuentes':['cliente.md'],'estado':'ok'}
    with TestClient(crear_app(servicio)) as cliente:
        ok,estado,_=ejecutar_caso(cliente,caso)
        assert ok, f"{caso['id']}: HTTP {estado}"
