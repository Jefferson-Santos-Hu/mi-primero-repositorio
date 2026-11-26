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
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
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
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\venv\Scripts\python.exe -m pytest -q
.\venv\Scripts\python.exe indexar_documentos.py
.\venv\Scripts\python.exe servicio_rag.py
.\venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8000
```

La clave `API_KEY` o `GEMINI_API_KEY` se configura en `.env`, ignorado por Git. No la pegues en capturas ni entregas. El índice `vectorstore/` es regenerable e ignorado. Tras crearlo, las siguientes corridas lo reabren sin volver a indexar; si cambia el corpus, detener el servicio y ejecutar `python indexar_documentos.py --actualizar`. Esta operación explícita recalcula solo chunks nuevos/modificados y elimina IDs obsoletos. Para conservar una versión anterior, utilizar otro directorio. La lectura normal rechaza cambios sin actualizar.

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

## Gate 2 — entrega y verificación

```powershell
.\venv\Scripts\python.exe verificar_entorno.py
.\venv\Scripts\python.exe -m pytest test_gate2.py test_indice_incremental.py -q
.\venv\Scripts\python.exe verificar_gate2.py
```

`verificar_gate2.py` realiza una consulta con embeddings y generación reales, comprueba reapertura del índice, fuentes, logs sin contenido crudo y la pausa/reanudación de LangGraph. Las decisiones de aprobación y rechazo del ensayo están marcadas como simuladas: no autorizan despliegue. Guarda `docs/gate2_evidencia.json`. La autoevaluación, los entregables y límites están en [docs/gate2.md](docs/gate2.md). Las consultas reales consumen cuota del proveedor; las pruebas pytest usan dobles explícitos.

## Decisiones del Módulo 3

- D-01: interfaz Nginx y FastAPI separadas.
- D-02: modo real o simulado explícito; sin sustitución silenciosa.
- D-03: Chroma persistente con actualización deliberada.
- D-04: validación estructural y revisión semántica humana.
- D-05: secretos en ejecución y puertos locales.
- D-06: supervisión didáctica, sin identidad ni persistencia durable.

Contexto, alternativas y costos: [docs/decisiones.md](docs/decisiones.md).

## Limitaciones del Módulo 3

- LIM-01: el control estructural no prueba verdad semántica.
- LIM-02: el filtro de patrones admite evasiones.
- LIM-03: el modo simulado es una demo limitada, sin consumo de Gemini.
- LIM-04: la aprobación local no es un control de producción.

Origen, riesgos y decisiones: [docs/limitaciones.md](docs/limitaciones.md).

## Módulo 3: requisitos y configuración

Se probó en Windows con Python 3.14.8 y Docker Desktop con motor Linux. Se necesitan Git, Docker Compose y los puertos locales 8000 y 8080 libres. Las bases de imágenes se fijan por digest en ambos Dockerfiles. `requirements.txt` contiene ejecución; `requirements-dev.txt` agrega pytest y coverage.

Variables: `API_KEY` o `GEMINI_API_KEY` identifica la credencial del proveedor; `GEMINI_MODEL` selecciona el modelo real. `MODELO` elige `real` o `simulado`. `INDICE_DIR` apunta al volumen `/app/vectorstore` dentro del contenedor. `CARGAR_DOTENV=false` permite probar ausencia real de credenciales sin leer un archivo local. Ninguna clave se compila en las imágenes.

### Cómo arrancar

```powershell
Copy-Item .env.example .env
# Configurar una clave propia en .env para modo real; no compartirla.
$env:MODELO='simulado'
docker compose up -d --build --wait --wait-timeout 120
```

La demostración funciona en modo simulado incluso con el marcador de clave de `.env.example`. Para consultar Gemini, configurar una credencial real y ejecutar `$env:MODELO='real'` antes de `docker compose up -d --wait`. Nunca se cambia automáticamente a simulación si falla el proveedor.

### Cómo comprobar

Abrir http://127.0.0.1:8080 para la interfaz y http://127.0.0.1:8000/docs para OpenAPI. La pantalla muestra el modo. El endpoint `/salud` solo comprueba el proceso; una consulta real comprueba proveedor y recuperación.

```powershell
.\venv\Scripts\python.exe verificar_stack.py
.\venv\Scripts\python.exe verificar_dockerfile.py
.\venv\Scripts\python.exe verificar_imagen.py
.\venv\Scripts\python.exe verificar_matriz.py --generar
.\venv\Scripts\python.exe verificar_riesgos.py
.\venv\Scripts\python.exe verificar_decisiones.py
.\venv\Scripts\python.exe verificar_mitigaciones.py
```

### Cómo detener

```powershell
docker compose down
```

El volumen `indice` se conserva. La actualización de corpus exige detener consultas y ejecutar `indexar_documentos.py --actualizar` en el entorno que contiene ese índice; no reutilizar un índice incompatible. Para reiniciar, repetir el comando de arranque.

### Problemas frecuentes del despliegue

- Motor Docker no disponible: abrir Docker Desktop y comprobar `docker version` antes de construir.
- Puertos ocupados: detener la instancia local que los usa o la composición anterior.
- Estado 503: revisar clave, cuota, conectividad o fundamentación; no se devuelve una respuesta de respaldo silenciosa.
- Registro desactualizado: confirmar el código, volver a ejecutar escenarios y regenerar `registrar_ejecucion.py`.
- El banner no cambia tras reconstruir: recargar la interfaz; el script lleva versión y cabecera no-store.

### Estructura y pruebas del Módulo 3

`api.py`, `modelo_simulado.py`, `fundamentacion.py`, `interfaz/`, `Dockerfile` y `compose.yaml` forman la aplicación. `tests/parciales/` prueba contratos sin proveedor. `escenarios.py`, `matriz_pruebas.py`, `riesgos.py` y los verificadores mantienen registros reproducibles en `docs/`. `verificar_defectos.py` solo modifica copias temporales. [Ficha funcional](docs/ficha_diseno_funcional.md), [diagrama](docs/diagrama_arquitectura.png) y [pruebas parciales](docs/pruebas_parciales.md).

### Cierre, transferencia y defensa

Los ejemplos de endpoints se generan con `python generar_api_md.py` y se comprueban con `python generar_api_md.py --comprobar`. [API y ejemplos](docs/api.md), [matriz de pruebas](docs/matriz_pruebas.md), [riesgos](docs/matriz_riesgos.md), [decisiones](docs/decisiones.md), [limitaciones](docs/limitaciones.md), [presentación ejecutiva](docs/presentacion.md) y [PowerPoint](docs/defensa_gate3.pptx).

```powershell
.\venv\Scripts\python.exe verificar_parciales.py
.\venv\Scripts\python.exe verificar_defectos.py
.\venv\Scripts\python.exe ensayo_demo.py --respaldo
.\venv\Scripts\python.exe ensayo_demo.py --comprobar
.\venv\Scripts\python.exe medir_guion.py
.\venv\Scripts\python.exe transferencia.py
.\venv\Scripts\python.exe registrar_ejecucion.py
.\venv\Scripts\python.exe verificar_registro.py
.\venv\Scripts\python.exe probar_en_frio.py
.\venv\Scripts\python.exe verificar_gate3.py --con-docker --escribir
```

El ensayo usa los puertos temporales 18000 y 18001, sin interferir con Compose. La prueba en frío crea un clon local y un entorno nuevo; no usa credenciales reales. Las pruebas parciales no llaman al proveedor. `registrar_ejecucion.py` conserva las secciones manuales y actualiza hechos, commit y huella del código; repetirlo después de modificar código o escenarios. El verificador del Gate 3 conserva pesos y umbral del programa; indica PROVISIONAL mientras falten revisiones por personas o defensa oral, incluso si las comprobaciones técnicas pasan.

Las revisiones de alcance, composición y transferencia contienen propuestas para Javier pendientes de confirmación. Se pueden comprobar técnicamente con `--sin-revision`, pero esa opción no acredita que él haya revisado el proyecto. El alumno debe ensayar la defensa oral con cronómetro delante de alguien; los scripts solo estiman su duración.
