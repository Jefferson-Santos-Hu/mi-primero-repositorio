"""Verifica el punto de entrada del Gate 1 sin llamar a la API real."""
import importlib
import io
import json
import unittest
from unittest.mock import patch

from src import consumir_gemini as cliente


class PruebasAplicacion(unittest.TestCase):
    def setUp(self):
        self.app = importlib.import_module("main")
        entorno = patch.dict("os.environ", {"API_KEY": "ficticia-local"}, clear=True)
        carga = patch.object(cliente, "load_dotenv")
        entorno.start()
        carga.start()
        self.addCleanup(entorno.stop)
        self.addCleanup(carga.stop)

    @patch.object(cliente.requests, "post")
    def test_recorrido_completo_con_json_y_esquema(self, post):
        datos = {"categoria": "http", "confianza": 0.9}
        post.return_value.json.return_value = {"candidates": [{"content": {"parts": [{"text": json.dumps(datos)}]}}]}
        self.assertEqual(self.app.consultar("clasificar_consulta_tecnica", "Tengo HTTP 429"), datos)
        cuerpo = post.call_args.kwargs["json"]
        self.assertEqual(cuerpo["contents"][0]["parts"][0]["text"], "Tengo HTTP 429")
        self.assertIn("systemInstruction", cuerpo)
        self.assertEqual(cuerpo["generationConfig"]["responseMimeType"], "application/json")

    @patch.object(cliente.requests, "post")
    def test_prompt_desconocido_no_usa_red(self, post):
        with self.assertRaises(ValueError):
            self.app.consultar("inexistente", "Hola")
        post.assert_not_called()

    @patch.object(cliente.requests, "post")
    def test_entrada_vacia_se_rechaza_antes_de_red(self, post):
        with self.assertRaises(ValueError):
            self.app.consultar("clasificar_consulta_tecnica", " ")
        post.assert_not_called()

    @patch.object(cliente.requests, "post")
    def test_no_acepta_json_con_tipo_equivocado(self, post):
        post.return_value.json.return_value = {"candidates": [{"content": {"parts": [{"text": '{"categoria":"http","confianza":"alta"}'}]}}]}
        with self.assertRaises(ValueError):
            self.app.consultar("clasificar_consulta_tecnica")

    def test_cli_imprime_objeto_y_devuelve_cero(self):
        datos = {"categoria": "http", "confianza": 1}
        with patch.object(self.app, "consultar", return_value=datos) as consultar, patch("sys.stdout", new_callable=io.StringIO) as salida:
            self.assertEqual(self.app.main([]), 0)
        self.assertEqual(json.loads(salida.getvalue()), datos)
        consultar.assert_called_once_with("clasificar_consulta_tecnica", None)

    def test_cli_error_no_imprime_traceback(self):
        for error in (ValueError("JSON inválido"), RuntimeError("Sin conexión")):
            with patch.object(self.app, "consultar", side_effect=error), patch("sys.stderr", new_callable=io.StringIO) as salida:
                self.assertEqual(self.app.main([]), 1)
            self.assertIn("Error:", salida.getvalue())
            self.assertNotIn("Traceback", salida.getvalue())


if __name__ == "__main__":
    unittest.main()
