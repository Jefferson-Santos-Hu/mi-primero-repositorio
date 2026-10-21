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
