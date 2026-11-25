from dataset_tuning import construir_ejemplos,validar_dataset,chequear_balance
from google.genai import types


def test_dataset_propio_balanceado():
    ejemplos=construir_ejemplos()
    assert len(ejemplos)>=10
    assert validar_dataset(ejemplos)==[]
    assert set(chequear_balance().values())=={3}


def test_detecta_duplicado_y_claves_y_json():
    original=construir_ejemplos()[0]
    malos=[original,original,types.TuningExample(text_input='otro',output='{}'),types.TuningExample(text_input=' ',output='no json')]
    errores=validar_dataset(malos)
    assert any('duplicada' in e for e in errores)
    assert any('claves' in e for e in errores)
    assert any('JSON' in e for e in errores)
