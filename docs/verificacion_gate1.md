# Gate 1 — ensayo y comprobación de entrega

Fecha: **24 de octubre de 2026**. Proyecto: asistente técnico con Gemini.
Este registro describe verificaciones realizadas; la aprobación del Gate
corresponde al instructor del programa.

## Ensayo de instalación limpia

Se clonó el repositorio remoto en una carpeta nueva, distinta de la carpeta
de desarrollo. El código clonado corresponde al commit **`f855371`**. Se siguió
el procedimiento del README con Python 3.14, un `venv` nuevo y la instalación
exclusiva mediante `pip install -r requirements.txt`.

Se creó el `.env` local desde `.env.example` y se configuró la clave propia,
sin copiar el entorno virtual ni paquetes de la carpeta de desarrollo.
Las variables de API heredadas del proceso y `PYTHONPATH` se retiraron solo
de los subprocesos del ensayo, para comprobar la configuración del clon.
El entorno tiene `include-system-site-packages = false`.

Resultado observado:

| Comprobación | Resultado |
|---|---|
| Instalación desde `requirements.txt` | Correcta, sin agregar dependencias manuales |
| `python -m pip check` | Sin dependencias rotas |
| `python -m pip freeze` frente al archivo declarado | Coinciden las 26 versiones |
| `python -m unittest discover -s tests -q` | 32 pruebas, OK |
| `python main.py --prompt clasificar_consulta_tecnica` | Código 0, JSON generado y validado |
| `python main.py --prompt extraer_contexto_tecnico` | Código 0, JSON generado y validado |
| `python main.py --prompt resumir_explicacion_tecnica` | Código 0, JSON generado y validado |
| `python main.py --texto ""` | Código 1, mensaje controlado antes de usar red |
| `.env` y `venv/` en el clon | Ignorados por Git; no aparecen en `git status` |
| `git log --all --oneline -- .env` | Sin resultados |

Las salidas originales, fechas y objetos generados están en
[`ensayo_gate1.json`](ensayo_gate1.json). El campo `errores` guarda stderr:
`unittest` escribe su resumen allí incluso cuando las pruebas terminan bien.

No hubo fallos de instalación que requirieran corregir dependencias. Se
documentó una entrada única `main.py` y se compartió el validador entre la
aplicación y la prueba de prompts, para que el recorrido completo sea explícito.

El ensayo se hizo en el mismo Windows, con un entorno nuevo y sin paquetes
globales. Pip reutilizó ruedas de su caché; no reutilizó el entorno virtual
anterior. Es una comprobación local de reproducibilidad, no una prueba en
otro equipo o sistema operativo.

## Corrida final contra la API

Después del ensayo se ejecutó `python main.py` en la carpeta de desarrollo,
con el estado de código que se entrega. Terminó con código 0, una respuesta
JSON real y sin traceback. La evidencia exacta se conserva en
[`ejecucion_final_gate1.json`](ejecucion_final_gate1.json).
El código de aplicación no cambió después de la prueba del clon; el commit
final agrega los registros y esta documentación.

## Revisión contra las seis dimensiones

| Dimensión de la rúbrica | Evidencia verificable |
|---|---|
| Entorno y repositorio, 20 % | README, versiones fijadas, ensayo limpio y commits progresivos |
| Python y estructura, 20 % | `main.py`, funciones separadas en `src/consumir_gemini.py` y validador compartido |
| Consumo de API, 25 % | Tres tareas ejecutadas contra Gemini en el clon y una corrida final |
| Prompt y respuesta, 15 % | Sistema separado del usuario, esquema de salida y banco con 9/9 respuestas estructuralmente válidas |
| Seguridad, 10 % | `.gitignore`, `.env.example` sin valores reales, revisión del historial y del clon |
| Documentación, 10 % | README de instalación y uso, diagrama, decisión de modelo y este registro |

Las cuatro condiciones no compensables se comprobaron: API funcional,
entorno reproducible en el ensayo, credenciales protegidas y código ejecutable.
No se asigna una calificación ni se anticipa la decisión del instructor.

## Seguridad y acceso a la entrega

El repositorio se comprobó accesible como público mediante una consulta sin
autenticar a la API de GitHub (HTTP 200, `private: false`). No se ampliaron
permisos ni se cambió su visibilidad.

Se revisaron los blobs del historial contra la clave real configurada y el
patrón de claves de Google; no se detectaron coincidencias. `.env` no figura
en el historial. Los registros solo contienen entradas sintéticas y respuestas,
sin encabezados de autenticación ni valores secretos.

## Piezas del módulo

- [Guía de instalación y uso](../README.md).
- [Arquitectura y diagrama](arquitectura.md).
- [Decisión de modelo y mediciones reales](decision-arquitectura.md).
- [Banco de prompts y explicación del ajuste](../prompts/README.md).
- [Registro final del banco: tres repeticiones por prompt](../prompts/registro_resultados.json).
- [Consigna del Gate 1](https://learning-pro.skillnest.com/mod/page/view.php?id=20320).
