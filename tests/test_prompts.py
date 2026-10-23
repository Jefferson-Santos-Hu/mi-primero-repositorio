"""Contratos del Bloque 10; la API se sustituye en las pruebas locales."""
import importlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from src import consumir_gemini as cliente


class PruebasSalidaJSON(unittest.TestCase):
    def test_separa_instruccion_y_datos_y_configura_json(self):
        esquema = {"type": "OBJECT", "properties": {"tema": {"type": "STRING"}}, "required": ["tema"]}
        with patch.dict("os.environ", {"API_KEY": "clave-ficticia"}, clear=True), patch.object(cliente, "load_dotenv"):
            _, _, cuerpo = cliente.armar_peticion("contenido del usuario", "instrucción de sistema", esquema)
        self.assertEqual(cuerpo["systemInstruction"]["parts"][0]["text"], "instrucción de sistema")
        self.assertEqual(cuerpo["contents"][0]["parts"][0]["text"], "contenido del usuario")
        self.assertEqual(cuerpo["generationConfig"], {"responseMimeType": "application/json", "responseSchema": esquema})

    def test_sistema_sin_esquema_y_argumentos_invalidos(self):
        with patch.dict("os.environ", {"API_KEY": "ficticia"}, clear=True), patch.object(cliente, "load_dotenv"):
            _, _, cuerpo = cliente.armar_peticion("Hola", "Responde brevemente")
            self.assertNotIn("generationConfig", cuerpo)
            for sistema in ("", "  ", 12):
                with self.subTest(sistema=sistema), self.assertRaises(ValueError):
                    cliente.armar_peticion("Hola", sistema)
            with self.assertRaises(ValueError):
                cliente.armar_peticion("Hola", "Sistema", [])

    def test_parsea_objeto_y_variantes_markdown(self):
        for texto in ('{"tema": "Python"}', '  ```json\n{"tema":"Python"}\n```  ', '```\n{"tema":"Python"}\n```', '```JSON\n{"tema":"Python"}\n```'):
            with self.subTest(texto=texto):
                self.assertEqual(cliente.parsear_respuesta_json(texto), {"tema": "Python"})

    def test_rechaza_json_cortado_prosa_y_valores_no_objeto(self):
        for texto in (None, 1, "", '{"tema":', 'Aquí tienes: {"tema":"Python"}', '[]', 'null', '"hola"', '{"numero":NaN}', '{"numero":Infinity}'):
            with self.subTest(texto=texto), self.assertRaises(ValueError):
                cliente.parsear_respuesta_json(texto)


class PruebasBanco(unittest.TestCase):
    def setUp(self):
        self.banco = importlib.import_module("prompts.banco").BANCO_DE_PROMPTS
        self.runner = importlib.import_module("prompts.test_consistencia")

    def test_tres_prompts_completos_y_ejemplos_validos(self):
        self.assertGreaterEqual(len(self.banco), 3)
        self.assertEqual(len({p["nombre"] for p in self.banco}), len(self.banco))
        for prompt in self.banco:
            self.assertTrue(prompt["system_instruction"].strip())
            self.assertTrue(prompt["ejemplo_usuario"].strip())
            self.assertEqual(set(prompt["claves_esperadas"]), set(prompt["response_schema"]["properties"]))
            self.runner.validar_estructura(prompt["ejemplo_salida"], prompt["response_schema"])

    def test_rechaza_claves_tipos_dominios_y_limites(self):
        esquema = self.banco[0]["response_schema"]
        for datos in ([], {}, {"categoria": "http"}, {"categoria": "http", "confianza": True},
                      {"categoria": "inexistente", "confianza": 0.5}, {"categoria": "http", "confianza": -1},
                      {"categoria": "http", "confianza": 2}, {"categoria": "http", "confianza": float('nan')},
                      {"categoria": "http", "confianza": 0.5, "extra": 1}):
            with self.subTest(datos=datos), self.assertRaises(ValueError):
                self.runner.validar_estructura(datos, esquema)
        self.runner.validar_estructura({"categoria": "http", "confianza": 0}, esquema)
        self.runner.validar_estructura({"categoria": "http", "confianza": 1}, esquema)

    def test_entero_no_acepta_bool_y_textos_no_vacios(self):
        esquema = self.banco[1]["response_schema"]
        for cambio in ({"codigo_http": True}, {"codigo_http": 429.0}, {"tecnologia": " "}, {"problema": ""}):
            datos = {**self.banco[1]["ejemplo_salida"], **cambio}
            with self.subTest(cambio=cambio), self.assertRaises(ValueError):
                self.runner.validar_estructura(datos, esquema)

    def test_valida_items_y_tamano_de_lista(self):
        esquema = self.banco[2]["response_schema"]
        for pasos in ("no es lista", [], [1], [" "], ["a", "b", "c", "d"]):
            with self.subTest(pasos=pasos), self.assertRaises(ValueError):
                self.runner.validar_estructura({"resumen": "Breve", "pasos": pasos}, esquema)

    def test_esquema_desconocido_falla_explicitamente(self):
        with self.assertRaises(ValueError):
            self.runner.validar_estructura("x", {"type": "DESCONOCIDO"})

    def test_registra_respuestas_y_fallos_sin_detener_serie(self):
        prompt = self.banco[0]
        valido = {"candidates": [{"content": {"parts": [{"text": json.dumps(prompt["ejemplo_salida"])}]}}]}
        with tempfile.TemporaryDirectory() as carpeta:
            destino = Path(carpeta) / "registro.json"
            with patch.object(self.runner, "armar_peticion", return_value=("https://servicio/models/modelo:generateContent", {}, {})), patch.object(self.runner, "enviar_peticion", side_effect=[valido, RuntimeError("Sin conexión"), valido]), patch.object(self.runner.time, "sleep"), patch("sys.stdout", new_callable=io.StringIO):
                registro = self.runner.ejecutar_consistencia([prompt], repeticiones=3, pausa=0, destino=destino)
            grupo = registro["prompts"][prompt["nombre"]]
            self.assertEqual((grupo["exitos"], grupo["fallos"], grupo["intentos"]), (2, 1, 3))
            self.assertEqual(grupo["repeticiones"][1]["error"], "Sin conexión")
            self.assertEqual(grupo["repeticiones"][0]["datos"], prompt["ejemplo_salida"])
            self.assertEqual(json.loads(destino.read_text(encoding="utf-8")), registro)

    def test_json_valido_con_tipo_incorrecto_cuenta_como_fallo(self):
        respuesta = {"candidates": [{"content": {"parts": [{"text": '{"categoria":"http","confianza":"alta"}'}]}}]}
        with tempfile.TemporaryDirectory() as carpeta, patch.object(self.runner, "armar_peticion", return_value=("https://servicio/models/modelo:generateContent", {}, {})), patch.object(self.runner, "enviar_peticion", return_value=respuesta), patch.object(self.runner.time, "sleep"), patch("sys.stdout", new_callable=io.StringIO):
            registro = self.runner.ejecutar_consistencia([self.banco[0]], pausa=0, destino=Path(carpeta)/"registro.json")
        grupo = registro["prompts"][self.banco[0]["nombre"]]
        self.assertEqual((grupo["exitos"], grupo["fallos"]), (0, 3))
        self.assertIn("texto_original", grupo["repeticiones"][0])

    def test_rechaza_menos_de_tres_intentos_o_pausa_invalida(self):
        for argumentos in ({"repeticiones": 2}, {"pausa": -1}):
            with self.subTest(argumentos=argumentos), self.assertRaises(ValueError):
                self.runner.ejecutar_consistencia(**argumentos)

    def test_cli_senala_fallos_y_exito_con_codigo_de_salida(self):
        for exitos, esperado in ((3, 0), (2, 1)):
            registro = {"prompts": {"prueba": {"exitos": exitos, "intentos": 3}}}
            with patch.object(self.runner, "ejecutar_consistencia", return_value=registro):
                self.assertEqual(self.runner.main(["--pausa", "0"]), esperado)


if __name__ == "__main__":
    unittest.main()
