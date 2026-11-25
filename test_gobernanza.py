import pytest
from langgraph.types import Command
from gobernanza import crear_supervision, huella_prompt, puntaje_riesgo,categoria_riesgo


def test_interrupcion_y_aprobacion_o_rechazo():
    app=crear_supervision()
    for decision,sesion in [(True,'aprobado'),(False,'rechazado')]:
        cfg={'configurable':{'thread_id':sesion}}
        r=app.invoke({'huella_nueva':huella_prompt('nuevo'),'aprobado':False},cfg)
        assert '__interrupt__' in r
        assert r.get('activa') is None
        r=app.invoke(Command(resume=decision),cfg)
        assert r['aprobado'] is decision
        assert bool(r.get('activa')) is decision


def test_riesgos_y_huella():
    assert huella_prompt('A')!=huella_prompt('B')
    assert categoria_riesgo(puntaje_riesgo(4,4))=='CRITICO'
    with pytest.raises(ValueError):puntaje_riesgo(0,5)
