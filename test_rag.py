import pytest
from langchain_core.documents import Document
from indexar_documentos import preparar_chunks, formatear_contexto


def test_chunks_estables_y_metadata(tmp_path):
    (tmp_path/'uno.md').write_text('Python y Gemini. '*100,encoding='utf8')
    a=preparar_chunks(tmp_path);b=preparar_chunks(tmp_path)
    assert len(a)>1
    assert [d.id for d in a]==[d.id for d in b]
    assert len(set(d.id for d in a))==len(a)
    assert all(d.metadata['fuente']=='uno.md' for d in a)
    assert all(len(d.page_content)<=500 for d in a)


def test_contexto_y_fuente_obligatoria():
    contexto,citas=formatear_contexto([Document(page_content='Una regla',metadata={'fuente':'reglas.md'})])
    assert '[1]' in contexto and citas=={1:'reglas.md'}
    with pytest.raises(ValueError):
        formatear_contexto([Document(page_content='sin fuente')])
