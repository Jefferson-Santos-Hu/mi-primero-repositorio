from ensayo_demo import evaluar,tiempo,PASOS,estable


def test_contrato_paso_exige_estado_contenido_y_tiempo():
    p=PASOS[0]
    assert evaluar(p,200,'simulado',.1)
    assert not evaluar(p,503,'simulado',.1)
    assert not evaluar(p,200,'real',.1)
    assert not evaluar(p,200,'simulado',3)


def test_tiempo_incluye_teclado():
    assert tiempo(40,1)[0]
    assert not tiempo(70,1)[0]


def test_respaldo_omite_solo_campos_variables():
    assert estable({'respuesta':'hola','trace_id':'aleatorio','auditoria':[{}]})=={'respuesta':'hola'}
