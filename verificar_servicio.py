"""Verifica el contrato HTTP compartido usando un doble explícito del servicio."""
import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from api import crear_app
from casos import CASOS,ejecutar_caso


if __name__=='__main__':
    with patch.dict(os.environ,{'MODELO':'simulado'}):
        with TestClient(crear_app()) as c:
            resultados=[ejecutar_caso(c,caso)[0] for caso in CASOS]
            assert c.get('/openapi.json').status_code==200
    print(sum(resultados),'de',len(resultados),'casos de API cumplidos');raise SystemExit(not all(resultados))
