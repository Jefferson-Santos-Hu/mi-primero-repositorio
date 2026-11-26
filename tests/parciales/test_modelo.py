from modelo_simulado import ServicioSimulado


def test_contrato_simulado_declara_modo_y_fuente():
    r=ServicioSimulado().consultar('HTTP 429')
    assert r['modo']=='simulado' and r['fuentes']==['cliente.md']
    assert r['tokens'] is None


def test_fuera_de_alcance_se_abstiene():
    assert ServicioSimulado().consultar('capital Mongolia')['fuentes']==[]


def test_identificadores_distintos_por_consulta():
    s=ServicioSimulado()
    assert s.consultar('429')['trace_id']!=s.consultar('429')['trace_id']
