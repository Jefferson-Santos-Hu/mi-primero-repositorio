import shutil
from pathlib import Path
from verificar_decisiones import comprobar
from crear_ficha import crear
import pytest


def preparar(tmp_path):
    raiz=Path.cwd();(tmp_path/'docs').mkdir()
    for n in ['README.md','docs/decisiones.md','docs/limitaciones.md']:shutil.copy2(raiz/n,tmp_path/n)


def test_contrato_decisiones_rechaza_campo_ausente(tmp_path,monkeypatch):
    preparar(tmp_path);p=tmp_path/'docs/decisiones.md';p.write_text(p.read_text(encoding='utf8').replace('Costo:','Coste no tipado:'),encoding='utf8')
    monkeypatch.chdir(tmp_path)
    assert not dict(comprobar())['campos completos']


def test_referencia_de_riesgo_inexistente_falla(tmp_path,monkeypatch):
    preparar(tmp_path);p=tmp_path/'docs/limitaciones.md';p.write_text(p.read_text(encoding='utf8').replace('R-06','R-99'),encoding='utf8')
    monkeypatch.chdir(tmp_path)
    assert not dict(comprobar())['riesgos existentes']


def test_generador_no_sobrescribe_ficha(tmp_path):
    p=crear(tmp_path/'ficha.md');p.write_text('Trabajo propio',encoding='utf8')
    with pytest.raises(FileExistsError):crear(p)
    assert p.read_text(encoding='utf8')=='Trabajo propio'
