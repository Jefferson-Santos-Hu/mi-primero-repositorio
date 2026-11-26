from medir_guion import comprobar,palabras
from pathlib import Path


def test_contrato_guion_tiene_nueve_reglas():
    assert len(comprobar())==9


def test_paso_renombrado_no_pasa():
    t=Path('docs/defensa.md').read_text(encoding='utf-8-sig').replace('PASO-1 Servicio vivo','PASO-1 Otra cosa')
    assert not dict(comprobar(t))['demo coincide']


def test_guion_sin_pasos_no_pasa():
    assert not dict(comprobar('Sin guion'))['demo coincide']
    assert palabras('Una prueba breve')==3
