from verificar_gate3 import puntuar,decidir,nota,no_compensables_que_fallan,FUENTES
from rubrica_gate3 import CRITERIOS


def perfectos():return {f:{'pasa':True} for f in FUENTES}


def test_contrato_pesos_y_fuentes():
    assert sum(c['peso'] for c in CRITERIOS)==100
    assert {f for c in CRITERIOS for f in c['fuentes']}==set(FUENTES)


def test_fuente_ausente_no_pasa_en_vacio():
    r=perfectos();del r['secretos']
    assert no_compensables_que_fallan(r,[])==['NC-4']
    assert decidir(99,['NC-4'],[])=='NO APRUEBA'


def test_sin_docker_o_revision_es_provisional():
    assert decidir(100,[],['stack'])=='PROVISIONAL'
    assert decidir(100,[],['revisión pendiente'])=='PROVISIONAL'


def test_cero_evidencia_cero_puntos():
    assert sum(p for _,p in puntuar({}))==0
    assert decidir(59,[],[])=='NO APRUEBA'


def test_escala_nota():
    assert nota(60)==4 and nota(100)==7 and nota(80)==5.5
