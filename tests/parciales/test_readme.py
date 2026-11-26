from verificar_readme import comprobar
from verificar_decisiones import comprobar as decisiones


def test_contrato_readme_devuelve_reglas():
    r=comprobar(ejecutar_pruebas=False)
    assert len(r)==8 and all(isinstance(v,bool) for _,v in r)


def test_readme_sin_instalacion_no_pasa():
    r=dict(comprobar('texto incompleto',ejecutar_pruebas=False))
    assert not r['instalacion'] and not r['arranque y parada']


def test_decisiones_tienen_limites_riesgos_y_readme():
    assert all(v for _,v in decisiones())
