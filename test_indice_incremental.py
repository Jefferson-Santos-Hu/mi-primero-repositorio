import pytest
from langchain_core.embeddings import DeterministicFakeEmbedding
from indexar_documentos import cargar_indice


class EmbeddingsContados(DeterministicFakeEmbedding):
    llamadas: int=0
    def embed_documents(self,texts):
        self.llamadas+=len(texts)
        return super().embed_documents(texts)


def test_actualizacion_incremental_solo_embedde_cambios(tmp_path):
    corpus=tmp_path/'corpus';corpus.mkdir()
    (corpus/'uno.md').write_text('Regla original.',encoding='utf8')
    (corpus/'dos.md').write_text('Otra regla.',encoding='utf8')
    emb=EmbeddingsContados(size=16)
    store,creado=cargar_indice(tmp_path/'indice',corpus,emb)
    assert creado and emb.llamadas==2
    store,creado=cargar_indice(tmp_path/'indice',corpus,emb)
    assert not creado and emb.llamadas==2
    (corpus/'uno.md').write_text('Regla actualizada.',encoding='utf8')
    with pytest.raises(ValueError,match='corpus cambió'):
        cargar_indice(tmp_path/'indice',corpus,emb)
    store,_=cargar_indice(tmp_path/'indice',corpus,emb,actualizar=True)
    assert emb.llamadas==3
    datos=store.get()
    assert len(datos['ids'])==2
    assert 'Regla actualizada.' in datos['documents']
    cargar_indice(tmp_path/'indice',corpus,emb,actualizar=True)
    assert emb.llamadas==3
