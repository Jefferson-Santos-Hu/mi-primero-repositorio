# Plantilla de repositorio base — Especialización en Desarrollo con IA Generativa (Accenture)

Esta es la estructura base que vas a usar como punto de partida para tu proyecto en este programa. Es la misma estructura que vas a ir ampliando bloque a bloque, hasta llegar a la aplicación completa que entregas en el Gate 3.

## Cómo empezar

Estos pasos se completan de forma progresiva a lo largo de la Unidad U1.2, no todos el mismo día:

1. Descarga este archivo comprimido (adjunto en la plataforma) y descomprímelo en tu computador. Inicializa el control de versiones sobre esa carpeta y registra tu primer commit con esta estructura base, tal como llegó, antes de modificar nada.
2. Crea tu entorno virtual de Python (por ejemplo, con `venv`) y actívalo.
3. Instala las dependencias que necesites y regístralas en `requirements.txt` (al inicio puede estar vacío o con muy pocas).
4. Copia `.env.example` a un archivo nuevo llamado `.env`, y completa ahí tus credenciales reales (llaves de API, tokens). El archivo `.env` nunca se sube al repositorio: ya está excluido en `.gitignore`.

## Estructura de carpetas

- `src/` : todo el código fuente de tu proyecto va aquí.
- `docs/` : documentación técnica del proyecto (diagramas, decisiones de arquitectura, notas).
- `tests/` : pruebas de tu código (las vas a usar más adelante en el programa, cuando el proyecto lo requiera).
- `requirements.txt` : dependencias de Python de tu proyecto, para que cualquier otra persona pueda reconstruir tu entorno con un solo comando.
- `.env.example` : plantilla de las variables de entorno que tu proyecto necesita, sin valores reales. Tu archivo `.env` real (con tus credenciales) nunca se commitea.
- `.gitignore` : le dice a Git qué archivos y carpetas ignorar (entre ellos, tu entorno virtual y tu archivo `.env`).

## Reglas que se mantienen durante todo el programa

- Ningún secreto (contraseña, llave de API, token) va escrito directamente en el código ni en ningún archivo que se suba al repositorio.
- Cada proyecto nuevo tiene su propio entorno virtual: no se comparten dependencias entre proyectos distintos.
- Todo el trabajo que se entrega en este programa vive en un repositorio de GitHub, sin excepción.

## Entorno de trabajo — Unidad U1.2, bloques 2 a 4

El proyecto utiliza Python 3.14 y un entorno virtual local llamado `venv`.
Desde la raíz del repositorio, en PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

La copia de `.env.example` se hace solo la primera vez, si todavía no existe
`.env`, para conservar cualquier credencial configurada. Completa localmente
`API_KEY` con tu clave de Gemini. Nunca subas `.env` ni compartas su contenido.

Si usas el intérprete del entorno directamente, no necesitas activar scripts:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m pip check
```

Las dependencias incluyen `requests`, `python-dotenv` y el cliente de Gemini
`google-genai`, con sus versiones instaladas registradas en `requirements.txt`.

### Primera petición autenticada — Bloque 4

La prueba se realiza desde Thunder Client en VS Code, usando una petición POST
al endpoint `generateContent` de Gemini. La autenticación usa el encabezado
`x-goog-api-key`, cuyo valor se copia del `.env` local; el cuerpo se envía como
JSON con una pregunta breve. La versión instalada de Thunder Client requiere
iniciar sesión antes de crear peticiones.

La evidencia de la ejecución se guarda dentro de `docs/`, con fecha, endpoint,
modelo, estado HTTP y respuesta real. Los encabezados de autenticación no deben
aparecer en capturas o archivos versionados. Para repetir la prueba se necesita
una clave propia y acceso al modelo elegido.

La ejecución del 21 de octubre de 2026 se realizó con `gemini-3.5-flash-lite`
y respondió **HTTP 200 OK**. El texto generado fue:
«¡Conexión establecida y funcionando correctamente!».

Consulta [la evidencia de la petición](docs/evidencia_peticion_autenticada.txt)
para ver el endpoint exacto, la fecha, los tokens observados y la referencia a
la captura de pantalla guardada junto al registro.

## Módulo Python — Unidad U1.3, Bloque 7

El archivo `src/consumir_gemini.py` implementa las cuatro funciones del curso:
`armar_peticion` valida la pregunta y prepara la URL, los encabezados y el JSON;
`enviar_peticion` envía el POST y maneja errores de conexión, tiempo de espera,
HTTP y JSON; `extraer_texto` valida el campo de respuesta; y
`obtener_dato_de_prueba` coordina las anteriores.

Usa la credencial `API_KEY` que ya estaba configurada en el `.env` de este
proyecto. También admite `GEMINI_API_KEY`, que tiene prioridad si ambas existen.
El modelo predeterminado es `gemini-3.5-flash-lite`, el mismo verificado en el
Bloque 4. Puedes cambiarlo con `GEMINI_MODEL` en `.env` según disponibilidad.
La clave viaja en el encabezado `x-goog-api-key`; nunca se incorpora a la URL.

Desde la raíz del repositorio, en PowerShell:

```powershell
.\venv\Scripts\python.exe -m src.consumir_gemini "Confirma que la conexión funciona."
.\venv\Scripts\python.exe -m src.consumir_gemini ""
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

El programa devuelve código 0 cuando funciona y 1 ante un error controlado.
Los mensajes de error se muestran sin traceback ni datos de autenticación.
El tiempo de espera es de 10 segundos para conectar y 90 para recibir datos.

Las 13 pruebas locales no hacen llamadas de red: simulan las respuestas de
Gemini para provocar conexión fallida, JSON inválido, campos ausentes y errores
HTTP, además de verificar entradas y el flujo correcto. La cobertura medida
del módulo fue del 99 % (69 instrucciones, una sin ejecutar: el punto de entrada).

La [evidencia del Bloque 7](docs/evidencia_bloque7.txt) registra, en orden,
la clave inválida real (HTTP 400), la entrada vacía y la respuesta real exitosa.
Para repetir esa secuencia, usando dos peticiones reales a tu proveedor:

```powershell
.\venv\Scripts\python.exe -m tests.verificar_bloque7
```

La credencial inválida se sustituye únicamente en memoria durante esa prueba;
el archivo `.env` se conserva. La última prueba usa tu credencial local.
La respuesta generada puede variar y el proveedor puede rechazar solicitudes
por cuota o disponibilidad. La evidencia se actualiza con el resultado real.

El repositorio partía sin código en `src/`: en este avance se construyó la
base descrita en los bloques 5 y 6 y se completó con la validación y las
excepciones del Bloque 7. El historial conserva la prueba RED por módulo
ausente y la implementación verificada; no se recrean avances anteriores.

## Decisión de arquitectura — Bloque 9

La [decisión de arquitectura](docs/decision-arquitectura.md) documenta el modelo
elegido, el [diagrama del prototipo](docs/arquitectura.md), la comparación de
precios, latencia y calidad, la justificación y la alternativa descartada.
Incluye la fecha de consulta de precios y los límites de la medición.

Los [registros reales](docs/mediciones_bloque9.json) conservan cada intento,
sus tiempos y, cuando el proveedor respondió, el texto y los tokens reportados.
Los errores y tiempos de espera también se guardan; no se cuentan como
respuestas generadas ni se les atribuye una calidad no observada.

Para repetir la comparación, revisa primero las tarifas en
`docs/medir_modelos.py` y luego ejecuta desde la raíz:

```powershell
.\venv\Scripts\python.exe docs/medir_modelos.py
```

Esa herramienta hace 12 solicitudes reales, consume cuota y reemplaza el
registro JSON; la decisión escrita debe actualizarse después si cambian los
resultados. La CLI de `src/` conserva su funcionamiento del Bloque 7.
