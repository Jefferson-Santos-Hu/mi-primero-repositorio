"""Pruebas locales: ninguna necesita una clave real ni conexión."""
import io
import unittest
from unittest.mock import Mock, patch

import requests

from src import consumir_gemini as cliente


class PruebasGemini(unittest.TestCase):
    def setUp(self):
        self.entorno = patch.dict("os.environ", {"API_KEY": "clave-de-prueba"}, clear=True)
        self.entorno.start()
        self.carga = patch.object(cliente, "load_dotenv")
        self.carga.start()
        self.addCleanup(self.entorno.stop)
        self.addCleanup(self.carga.stop)

    def test_rechaza_preguntas_invalidas_antes_de_usar_red(self):
        with patch.object(cliente.requests, "post") as enviar:
            for pregunta in ("", "  \n", None, 123, []):
                with self.subTest(pregunta=pregunta), self.assertRaises(ValueError):
                    cliente.obtener_dato_de_prueba(pregunta)
            enviar.assert_not_called()

    def test_construye_peticion_y_separa_credencial_de_url(self):
        url, encabezados, cuerpo = cliente.armar_peticion(" Hola ")
        self.assertIn("gemini-3.5-flash-lite:generateContent", url)
        self.assertNotIn("clave-de-prueba", url)
        self.assertEqual(encabezados["x-goog-api-key"], "clave-de-prueba")
        self.assertEqual(cuerpo["contents"][0]["parts"][0]["text"], "Hola")

    def test_falta_clave(self):
        with patch.dict("os.environ", {"API_KEY": " "}, clear=True):
            with self.assertRaisesRegex(ValueError, "API_KEY"):
                cliente.armar_peticion("Hola")

    def test_configuracion_gemini(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY": "otra", "GEMINI_MODEL": "gemini-prueba"}):
            url, encabezados, _ = cliente.armar_peticion("Hola")
            self.assertIn("gemini-prueba:", url)
            self.assertEqual(encabezados["x-goog-api-key"], "otra")

    def test_modelo_invalido(self):
        with patch.dict("os.environ", {"GEMINI_MODEL": "../otro?key=x"}):
            with self.assertRaises(ValueError):
                cliente.armar_peticion("Hola")

    @patch.object(cliente.requests, "post")
    def test_orquesta_peticion_correcta(self, post):
        post.return_value.json.return_value = {"candidates": [{"content": {"parts": [{"text": "Hola"}]}}]}
        self.assertEqual(cliente.obtener_dato_de_prueba("Saluda"), "Hola")
        self.assertEqual(post.call_args.kwargs["timeout"], (10, 90))
        self.assertFalse(post.call_args.kwargs["allow_redirects"])

    @patch.object(cliente.requests, "post")
    def test_errores_de_transporte_no_exponen_secreto(self, post):
        for error, mensaje in ((requests.ConnectionError("clave-de-prueba"), "conectar"),
                               (requests.Timeout("clave-de-prueba"), "tiempo"),
                               (requests.RequestException("clave-de-prueba"), "petición")):
            post.side_effect = error
            with self.subTest(error=type(error).__name__), self.assertRaisesRegex(RuntimeError, mensaje) as resultado:
                cliente.obtener_dato_de_prueba("Hola")
            self.assertNotIn("clave-de-prueba", str(resultado.exception))

    @patch.object(cliente.requests, "post")
    def test_errores_http(self, post):
        for estado in (400, 401, 403, 404, 429, 500, 503):
            respuesta = Mock(status_code=estado)
            respuesta.raise_for_status.side_effect = requests.HTTPError(response=respuesta)
            post.return_value = respuesta
            with self.subTest(estado=estado), self.assertRaisesRegex(RuntimeError, str(estado)):
                cliente.obtener_dato_de_prueba("Hola")

    @patch.object(cliente.requests, "post")
    def test_json_invalido(self, post):
        post.return_value.json.side_effect = requests.exceptions.JSONDecodeError("JSON inválido", "x", 0)
        with self.assertRaisesRegex(RuntimeError, "JSON"):
            cliente.obtener_dato_de_prueba("Hola")

    def test_respuestas_sin_texto(self):
        casos = ({}, {"candidates": []}, {"candidates": [{}]}, None, [],
                 {"candidates": [{"content": {"parts": []}}]},
                 {"candidates": [{"content": {"parts": [{"text": " "}]}}]},
                 {"candidates": [{"content": {"parts": [{"text": 1}]}}]})
        for datos in casos:
            with self.subTest(datos=datos), self.assertRaisesRegex(RuntimeError, "texto"):
                cliente.extraer_texto(datos)

    def test_extrae_texto(self):
        self.assertEqual(cliente.extraer_texto({"candidates": [{"content": {"parts": [{"text": " Bien "}]}}]}), "Bien")

    @patch.object(cliente, "obtener_dato_de_prueba", return_value="Respuesta")
    def test_cli_exitoso(self, obtener):
        with patch("sys.stdout", new_callable=io.StringIO) as salida:
            self.assertEqual(cliente.main(["Hola"]), 0)
        self.assertIn("Respuesta", salida.getvalue())
        obtener.assert_called_once_with("Hola")

    @patch.object(cliente, "obtener_dato_de_prueba")
    def test_cli_error_limpio(self, obtener):
        for error in (ValueError("Entrada inválida"), RuntimeError("Sin conexión")):
            obtener.side_effect = error
            with patch("sys.stderr", new_callable=io.StringIO) as salida:
                self.assertEqual(cliente.main(["Hola"]), 1)
            self.assertIn("Error:", salida.getvalue())
            self.assertNotIn("Traceback", salida.getvalue())


if __name__ == "__main__":
    unittest.main()
