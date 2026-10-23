"""Verificación manual REAL: usa dos peticiones y guarda salida sin secretos.

Ejecutar desde la raíz: python -m tests.verificar_bloque7
No forma parte del descubrimiento de pruebas locales.
"""
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
import io
from pathlib import Path
from unittest.mock import patch

from src import consumir_gemini as cliente


def verificar():
    salida = io.StringIO()
    with redirect_stdout(salida), redirect_stderr(salida):
        print("Bloque 7 - Ejecución real y secuencial")
        print(f"Fecha: {datetime.now().astimezone().isoformat(timespec='seconds')}")
        print("Modelo: gemini-3.5-flash-lite (configurable mediante GEMINI_MODEL)")
        print("1. Credencial inválida (reemplazo temporal en memoria, sin editar .env)")
        with patch.dict("os.environ", {"API_KEY": "clave-invalida-de-prueba", "GEMINI_API_KEY": "clave-invalida-de-prueba"}):
            invalida = cliente.main(["Confirma en una frase corta que esta conexión funciona."])
        print(f"Código de salida: {invalida}")
        print("2. Entrada vacía (validación antes de la red)")
        vacia = cliente.main([""])
        print(f"Código de salida: {vacia}")
        print("3. Credencial local restaurada y pregunta válida (API real)")
        correcta = cliente.main(["Confirma en una frase corta, en español, que esta conexión funciona."])
        print(f"Código de salida: {correcta}")
        print("Las pruebas de red desconectada, JSON y campos faltantes son simulaciones en unittest.")
    registro = salida.getvalue()
    print(registro, end="")
    destino = Path(__file__).resolve().parents[1] / "docs" / "evidencia_bloque7.txt"
    destino.write_text(registro, encoding="utf-8")
    return 0 if (invalida, vacia, correcta) == (1, 1, 0) else 1


if __name__ == "__main__":
    raise SystemExit(verificar())
