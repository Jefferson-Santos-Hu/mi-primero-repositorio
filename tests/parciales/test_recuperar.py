from indexar_documentos import preparar_chunks,formatear_contexto
from langchain_core.documents import Document
import pytest


def test_contrato_contexto_conserva_fuente():
    contexto,citas=formatear_contexto([Document(page_content='Dato',metadata={'fuente':'propia.md'})])
    assert citas=={1:'propia.md'} and '[1] Dato'==contexto


def test_fuente_ausente_rechazada():
    with pytest.raises(ValueError):formatear_contexto([Document(page_content='Dato')])


def test_ids_estables(tmp_path):
    (tmp_path/'uno.md').write_text('Dato propio',encoding='utf8')
    assert preparar_chunks(tmp_path)[0].id=='uno-0'
    assert preparar_chunks(tmp_path)[0].id==preparar_chunks(tmp_path)[0].id
