# Asistente técnico con Gemini — Gate 1

Miniaplicación de consola de Jefferson Santos para el Módulo 1 de la
Especialización en Desarrollo con IA Generativa. Clasifica consultas técnicas,
extrae el contexto de una incidencia o resume una explicación. Consulta la
API real de Gemini y entrega un objeto JSON después de validar su estructura.

## Requisitos

- Python 3.14, Git y conexión a internet. Verificado en Windows con PowerShell.
- Una API key propia de Gemini y acceso a `gemini-3.5-flash-lite`.
- Cuota disponible: una ejecución normal hace una petición real. El ensayo del
  banco hace nueve. Los errores de cuota o disponibilidad no son resultados válidos.

## Instalar desde una clonación nueva

En PowerShell, desde una carpeta donde quieras guardar el proyecto:

```powershell
git clone https://github.com/Jefferson-Santos-Hu/mi-primero-repositorio.git
cd mi-primero-repositorio
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m pip check
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Abre `.env` en tu editor y reemplaza **solo el valor de `API_KEY`** por tu
clave real de Gemini, creada en [Google AI Studio](https://aistudio.google.com/apikey).
La clave no se escribe en el código, en comandos ni en Git. El archivo contiene:

```dotenv
API_KEY=tu_llave_aqui
GEMINI_MODEL=gemini-3.5-flash-lite
```

`API_KEY` es obligatorio salvo que uses la alternativa `GEMINI_API_KEY`.
Si defines ambas, `GEMINI_API_KEY` tiene prioridad. `GEMINI_MODEL` es opcional:
el código usa `gemini-3.5-flash-lite` cuando se omite. Las variables de proceso
prevalecen sobre `.env`. No dejes el valor de ejemplo como si fuera una clave real.

Se utiliza directamente el Python de `venv`: no hace falta activar scripts ni
cambiar la política de ejecución de PowerShell. En macOS/Linux usa `python3`
para crear el entorno y `./venv/bin/python` en lugar de `.\venv\Scripts\python.exe`.

## Ejecutar la miniaplicación

Desde la raíz del repositorio:

```powershell
.\venv\Scripts\python.exe main.py
```

Sin argumentos, usa el ejemplo de clasificación de una consulta que recibe
HTTP 429. Imprime un objeto con `categoria` (string) y `confianza` (número).
La respuesta y su confianza vienen del modelo y pueden variar entre llamadas.

Para usar una entrada propia o elegir otra tarea:

```powershell
.\venv\Scripts\python.exe main.py --prompt clasificar_consulta_tecnica --texto "Mi petición a Gemini devuelve HTTP 429."
.\venv\Scripts\python.exe main.py --prompt extraer_contexto_tecnico
.\venv\Scripts\python.exe main.py --prompt resumir_explicacion_tecnica
.\venv\Scripts\python.exe main.py --help
```

Al omitir `--texto`, cada tarea usa su ejemplo incluido en el banco.
Una entrada vacía se rechaza antes de enviar una petición. El programa devuelve
código **0** cuando imprime una salida válida y **1** si falla la operación;
los errores se muestran sin traceback ni credenciales. En PowerShell puedes
consultar `$LASTEXITCODE` inmediatamente después del comando.

La consulta de texto libre del Bloque 7 también se conserva:

```powershell
.\venv\Scripts\python.exe -m src.consumir_gemini "Explica brevemente para qué sirve venv."
```

## Qué procesa y valida

`main.py` coordina el banco y las funciones `armar_peticion`, `enviar_peticion`,
`extraer_texto` y `parsear_respuesta_json`. La instrucción de sistema se envía
separada de la entrada de usuario, junto con `responseSchema`. El validador
compartido de `src/validacion_json.py` revisa claves, tipos, enum, intervalos,
listas y textos no vacíos. La clave viaja por HTTPS en `x-goog-api-key`.

El cliente controla conexión, tiempo de espera, estado HTTP, JSON inválido y
campos faltantes. El timeout es 10 segundos para conectar y 90 para leer.
La aplicación no implementa reintentos automáticos, interfaz web ni RAG.
La consistencia estructural no garantiza que todo el contenido sea correcto:
las respuestas técnicas requieren revisión antes de aplicarlas.

## Pruebas y banco de prompts

Las pruebas locales no usan internet ni una clave real:

```powershell
.\venv\Scripts\python.exe -m unittest discover -s tests -v
```

Suite actual: **32 pruebas**. El banco del Bloque 10 tiene tres prompts y su
[registro final](prompts/registro_resultados.json) contiene **9/9 respuestas
estructuralmente válidas** (tres por prompt). La [documentación del banco](prompts/README.md)
explica los esquemas, los límites de esa medición y el ajuste del resumen.

Para repetir la medición real, que consume cuota y reemplaza el registro:

```powershell
.\venv\Scripts\python.exe -m prompts.test_consistencia
```

Para guardarla aparte, añade `--destino prompts/historial/otra_medicion.json`.
La [primera medición](prompts/historial/registro_inicial.json) permanece como
antecedente. No se fabrican resultados ni se excluyen intentos fallidos.

## Si algo falla

| Situación | Qué revisar |
|---|---|
| Clave ausente o HTTP 400/401/403 | `.env` en la raíz, valor real y acceso al proyecto/modelo; también la forma de la petición si hubo cambios al esquema |
| HTTP 404 | Modelo configurado y disponibilidad para la cuenta |
| HTTP 429 | Cuota y límites del proyecto; esperar y repetir cuando corresponda |
| HTTP 5xx o timeout | Disponibilidad del proveedor y conexión; volver a ejecutar después |
| JSON o estructura inválida | El programa lo rechaza; revisar el esquema y el texto antes de ajustar el prompt |
| Dependencias ausentes | Usar el Python de `venv` e instalar desde `requirements.txt` |

## Estructura y evidencias del Módulo 1

- `main.py`: entrada de la miniaplicación con salida JSON validada.
- `src/`: cliente Gemini y validación compartida.
- `prompts/`: banco, script de consistencia, resultados y explicación del ajuste.
- `tests/`: pruebas locales con respuestas simuladas.
- `requirements.txt`: versiones fijadas del entorno, incluidas las dependencias
  instaladas en el Bloque 4; la aplicación usa `requests` y `python-dotenv`.
- `.env.example`: variables de referencia sin credenciales reales.
- [Arquitectura y diagrama](docs/arquitectura.md).
- [Decisión de modelo y comparación real](docs/decision-arquitectura.md).
- [Evidencia de la petición del Bloque 4](docs/evidencia_peticion_autenticada.txt).
- [Validación y errores del Bloque 7](docs/evidencia_bloque7.txt).
- [Ensayo de instalación limpia y lista de comprobación del Gate 1](docs/verificacion_gate1.md).

`.env`, `venv/` y las cachés están excluidos por `.gitignore`. Cada persona que
clone el repositorio configura su propia clave; ninguna entrega incluye `.env`.
El historial de Git conserva los avances y pruebas de los bloques del módulo.

## Módulo 2 y API del Módulo 3

Los avances actuales están en la carpeta local `mi-primero-repositorio`. Entorno probado: Python 3.14, con versiones fijadas en `requirements.txt`.

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m pytest -q
.\venv\Scripts\python.exe indexar_documentos.py
.\venv\Scripts\python.exe servicio_rag.py
.\venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8000
```

La clave `API_KEY` o `GEMINI_API_KEY` se configura en `.env`, ignorado por Git. No la pegues en capturas ni entregas. El índice `vectorstore/` es regenerable e ignorado. Tras crearlo, las siguientes corridas lo reabren sin volver a indexar; si cambia el corpus se debe usar un directorio nuevo. No se mezcla contenido de versiones.

- Cliente, backoff y costo: `cliente.py`, `test_cliente.py`, `docs/cliente_modular_evidencia.json`.
- Pipeline, 20 respuestas reales y revisión asistida de 10 casos: `pipeline_texto.py`, `resultados_metricas.json`, `revision_manual.json`, `docs/limites_metrica.md`.
- Cadenas y rutas: `cadena_tres_pasos.py`, `enrutamiento.py`, `test_orquestacion.py`.
- Agente, herramientas y memoria: `agente_con_herramientas.py`, `trazas_agente.jsonl`, `docs/limites_autonomia.md`. Se usa el API clásico solicitado por el curso; LangChain señala su deprecación y una migración futura a LangGraph.
- RAG: `indexar_documentos.py`, `servicio_rag.py`, corpus propio en `corpus/`, `evaluacion_recuperacion.py`, `resultados_evaluacion.txt`, `registro_rag.py`, `docs/evaluacion_rag.md`.
- Personalización: `dataset_tuning.py`, `decision.py`, `decision_personalizacion.md`. Preparar datos no envía un trabajo de entrenamiento.
- Riesgos y supervisión: `docs/matriz_riesgos.md`, `docs/registro_prompts.json`, `gobernanza.py`, `docs/supervision_evidencia.json`. La pausa está probada; la identidad y persistencia de aprobaciones no son funciones de producción implementadas.
- API: `api.py`, `casos.py`, `registrar_pruebas.py`, `docs/endpoints_evidencia.json`. Con el servidor activo, ejecutar `python registrar_pruebas.py` para registrar casos internos y externos del contrato.

La API publica `GET /salud`, `GET /errores/{codigo}`, `POST /consultas`, `/docs` y `/openapi.json`. Salud indica que el proceso está vivo; no prueba disponibilidad o cuota de Gemini. Las respuestas con fuentes deben revisarse: una cita existente no garantiza fidelidad semántica.

La revisión por pares permanece pendiente. `docs/revision_propuesta_javier.md` es una propuesta de observaciones para el compañero, no una revisión atribuida a él.
