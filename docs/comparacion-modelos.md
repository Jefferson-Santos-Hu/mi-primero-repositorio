# Comparación de modelos — Bloque 9

Fecha de inicio: 2026-10-23T18:45:04-03:00

4 repeticiones de P1 por modelo, alternando modelos; P2 y P3 una vez por modelo. Mismo POST y configuración predeterminada del módulo; sin caché explícita, herramientas ni streaming.

La serie actual contiene 12 respuestas válidas, 6 por modelo. No se incorporan los fallos del registro inicial a estos promedios.

## Preguntas

**P1:** Responde en español en un máximo de 80 palabras: ¿Para qué sirve un entorno virtual de Python y cómo lo creas con venv?

**P2:** Responde en español en un máximo de 80 palabras: ¿Cómo protejo una API key en un proyecto Python con Git usando .env y .gitignore?

**P3:** Responde en español en un máximo de 80 palabras: Mi petición HTTP devuelve 429. ¿Qué significa y qué debo hacer?

## Cada ejecución, en orden

| Intento | Modelo | Pregunta | Segundos | Entrada | Salida visible | Razonamiento | Equivalente Standard USD |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | gemini-3.5-flash-lite | P1 | 1.883243 | 31 | 97 | 0 | 0.0002518000 |
| 2 | gemini-3.6-flash | P1 | 8.138419 | 31 | 132 | 1191 | 0.0049845000 |
| 3 | gemini-3.5-flash-lite | P1 | 1.848427 | 31 | 134 | 0 | 0.0003443000 |
| 4 | gemini-3.6-flash | P1 | 7.309327 | 31 | 120 | 1167 | 0.0048495000 |
| 5 | gemini-3.5-flash-lite | P1 | 1.967179 | 31 | 127 | 0 | 0.0003268000 |
| 6 | gemini-3.6-flash | P1 | 5.931747 | 31 | 115 | 819 | 0.0035257500 |
| 7 | gemini-3.5-flash-lite | P1 | 1.934578 | 31 | 134 | 0 | 0.0003443000 |
| 8 | gemini-3.6-flash | P1 | 6.415505 | 31 | 93 | 1063 | 0.0043582500 |
| 9 | gemini-3.5-flash-lite | P2 | 2.034006 | 33 | 139 | 0 | 0.0003574000 |
| 10 | gemini-3.6-flash | P2 | 6.605337 | 33 | 135 | 821 | 0.0036097500 |
| 11 | gemini-3.5-flash-lite | P3 | 1.957089 | 30 | 107 | 0 | 0.0002765000 |
| 12 | gemini-3.6-flash | P3 | 7.024738 | 30 | 135 | 1098 | 0.0046462500 |

## Promedios de P1

- **gemini-3.5-flash-lite:** 1.908357 segundos, 4/4 respuestas. Costo equivalente medio de esas cuatro peticiones: 0.0003168000 USD.
- **gemini-3.6-flash:** 6.948749 segundos, 4/4 respuestas. Costo equivalente medio de esas cuatro peticiones: 0.0044295000 USD.

## Evaluación cualitativa asistida

Criterios: pertinencia, corrección técnica de los conceptos básicos, utilidad de los pasos y brevedad. Se analiza la primera respuesta P1 y las respuestas P2/P3. La revisión no es ciega ni estadísticamente representativa.

| Pregunta | Flash-Lite | Flash |
|---|---|---|
| P1: venv | Explica aislamiento y cómo crear/activar el entorno. Útil. | Explica aislamiento y creación/activación. Útil. |
| P2: API key | Muestra `.env`, `.gitignore` y carga desde Python, incluso código. Útil. | Explica los mismos pasos con menos código. Útil; la frase «jamás se subirá» es demasiado absoluta. |
| P3: HTTP 429 | Recomienda `Retry-After`, reducir frecuencia y backoff. Útil, pero atribuirlo a «seguridad» es impreciso. | Identifica rate limit y recomienda `Retry-After`, menor frecuencia y backoff. Útil y más preciso en ese punto. |

Ambos dan respuestas útiles en 3/3 preguntas para el alcance introductorio. No se exige ni se demuestra una superioridad universal. En Windows la activación depende de la terminal: para PowerShell debe usarse `Activate.ps1`, como indica el README. `.gitignore` no retira secretos ya versionados; una clave expuesta debe rotarse. Un 429 también puede exigir revisar cuota o límites del proyecto. Son límites de las explicaciones breves, no funciones nuevas implementadas en el módulo.

## Respuestas completas

Solo se normalizan espacios al final de las líneas para Markdown; los textos y contadores originales permanecen en el JSON.

### Intento 1: gemini-3.5-flash-lite, P1

Fecha: 2026-10-23T18:45:04-03:00. Duración: 1.883243 segundos. Modelo devuelto: `gemini-3.5-flash-lite`.

```text
Un entorno virtual de Python sirve para aislar las dependencias de un proyecto, evitando conflictos entre versiones de paquetes en tu sistema.

Para crearlo, abre la terminal en la carpeta de tu proyecto y ejecuta el comando:

`python -m venv mi_entorno`

Luego, actívalo con `mi_entorno\Scripts\activate` (en Windows) o `source mi_entorno/bin/activate` (en Mac/Linux).
```

Palabras aproximadas (`len(texto.split())`): 52.

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 97,
  "totalTokenCount": 128,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 2: gemini-3.6-flash, P1

Fecha: 2026-10-23T18:45:06-03:00. Duración: 8.138419 segundos. Modelo devuelto: `gemini-3.6-flash`.

```text
Un entorno virtual aísla las dependencias y librerías de un proyecto específico, evitando conflictos de versiones entre distintas aplicaciones o con el sistema global. Mantiene tus desarrollos limpios y reproducibles.

Para crearlo usando el módulo integrado `venv`, abre la terminal en la carpeta de tu proyecto y ejecuta:

`python -m venv nombre_entorno`

Esto creará un directorio con la copia aislada de Python. Para usarlo, solo debes activarlo según tu sistema operativo (`source nombre_entorno/bin/activate` en Linux/Mac o `nombre_entorno\Scripts\activate` en Windows).
```

Palabras aproximadas (`len(texto.split())`): 79.

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 132,
  "totalTokenCount": 1354,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "thoughtsTokenCount": 1191,
  "serviceTier": "standard"
}
```

### Intento 3: gemini-3.5-flash-lite, P1

Fecha: 2026-10-23T18:45:14-03:00. Duración: 1.848427 segundos. Modelo devuelto: `gemini-3.5-flash-lite`.

```text
Un **entorno virtual** sirve para aislar las dependencias de un proyecto Python, evitando conflictos entre versiones de paquetes en tu sistema.

Para crearlo y activarlo, usa estos comandos en la terminal:

1. **Crear:**
   `python -m venv mi_entorno`
2. **Activar (Windows):**
   `mi_entorno\Scripts\activate`
3. **Activar (Mac/Linux):**
   `source mi_entorno/bin/activate`

Una vez activo, cualquier paquete que instales (`pip install`) solo afectará a este proyecto.
```

Palabras aproximadas (`len(texto.split())`): 60.

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 134,
  "totalTokenCount": 165,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 4: gemini-3.6-flash, P1

Fecha: 2026-10-23T18:45:16-03:00. Duración: 7.309327 segundos. Modelo devuelto: `gemini-3.6-flash`.

```text
Un entorno virtual aísla las dependencias y paquetes de un proyecto específico, evitando conflictos entre versiones de diferentes proyectos o con la instalación global de Python.

Para crearlo con **`venv`**, abre la terminal en la carpeta de tu proyecto y ejecuta:

`python -m venv nombre_del_entorno`

Esto generará una carpeta aislada con su propio ejecutable de Python. Después, solo debes activarlo (por ejemplo, con `source nombre_del_entorno/bin/activate` en Linux/Mac) para instalar librerías independientemente.
```

Palabras aproximadas (`len(texto.split())`): 71.

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 120,
  "totalTokenCount": 1318,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "thoughtsTokenCount": 1167,
  "serviceTier": "standard"
}
```

### Intento 5: gemini-3.5-flash-lite, P1

Fecha: 2026-10-23T18:45:23-03:00. Duración: 1.967179 segundos. Modelo devuelto: `gemini-3.5-flash-lite`.

```text
Un **entorno virtual** sirve para aislar las dependencias de un proyecto Python, evitando conflictos entre versiones de librerías en tu sistema.

Para crearlo y activarlo, usa estos comandos en tu terminal:

1. **Crear:** `python -m venv mi_entorno`
2. **Activar (Windows):** `mi_entorno\Scripts\activate`
3. **Activar (Mac/Linux):** `source mi_entorno/bin/activate`

Una vez activo, cualquier librería que instales con `pip` solo afectará a ese proyecto.
```

Palabras aproximadas (`len(texto.split())`): 60.

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 127,
  "totalTokenCount": 158,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 6: gemini-3.6-flash, P1

Fecha: 2026-10-23T18:45:25-03:00. Duración: 5.931747 segundos. Modelo devuelto: `gemini-3.6-flash`.

```text
Un entorno virtual de Python sirve para aislar las dependencias y librerías de un proyecto específico, evitando conflictos entre versiones de diferentes proyectos o el sistema global.

Para crearlo con **venv**, abre la terminal y ejecuta:
`python -m venv nombre_entorno`

Esto creará una carpeta con el entorno. Para empezarlo a usar, actívalo según tu sistema:
* **Linux/Mac:** `source nombre_entorno/bin/activate`
* **Windows:** `nombre_entorno\Scripts\activate`
```

Palabras aproximadas (`len(texto.split())`): 62.

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 115,
  "totalTokenCount": 965,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "thoughtsTokenCount": 819,
  "serviceTier": "standard"
}
```

### Intento 7: gemini-3.5-flash-lite, P1

Fecha: 2026-10-23T18:45:31-03:00. Duración: 1.934578 segundos. Modelo devuelto: `gemini-3.5-flash-lite`.

```text
Un **entorno virtual** sirve para aislar las dependencias de un proyecto Python, evitando conflictos entre versiones de librerías en tu sistema.

Para crearlo y activarlo, usa estos comandos en tu terminal:

1. **Crear el entorno** (llamado *venv*):
   `python -m venv venv`

2. **Activar el entorno**:
   * **Windows:** `venv\Scripts\activate`
   * **Mac/Linux:** `source venv/bin/activate`

Una vez activo, cualquier librería que instales con `pip` quedará confinada exclusivamente a ese proyecto.
```

Palabras aproximadas (`len(texto.split())`): 67.

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 134,
  "totalTokenCount": 165,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 8: gemini-3.6-flash, P1

Fecha: 2026-10-23T18:45:33-03:00. Duración: 6.415505 segundos. Modelo devuelto: `gemini-3.6-flash`.

```text
Un entorno virtual de Python aísla las dependencias de un proyecto específico, evitando conflictos de versiones entre paquetes y manteniendo limpio el sistema global.

Para crearlo con `venv`, abre la terminal en la carpeta de tu proyecto y ejecuta el siguiente comando:

`python -m venv nombre_del_entorno`

Esto generará una carpeta con una copia aislada de Python y su propio gestor de paquetes, lista para ser activada.
```

Palabras aproximadas (`len(texto.split())`): 66.

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 93,
  "totalTokenCount": 1187,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "thoughtsTokenCount": 1063,
  "serviceTier": "standard"
}
```

### Intento 9: gemini-3.5-flash-lite, P2

Fecha: 2026-10-23T18:45:39-03:00. Duración: 2.034006 segundos. Modelo devuelto: `gemini-3.5-flash-lite`.

```text
Para proteger tu API key:

1. Instala la librería para variables de entorno: `pip install python-dotenv`.
2. Crea un archivo llamado `.env` en la raíz de tu proyecto y guarda tu clave así: `API_KEY=tu_clave_secreta`.
3. Crea un archivo `.gitignore` y añade la línea `.env` para evitar que Git lo suba al repositorio.
4. En tu código Python, carga y usa la clave así:
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()
   api_key = os.getenv("API_KEY")
```
```

Palabras aproximadas (`len(texto.split())`): 75.

```json
{
  "promptTokenCount": 33,
  "candidatesTokenCount": 139,
  "totalTokenCount": 172,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 33
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 10: gemini-3.6-flash, P2

Fecha: 2026-10-23T18:45:41-03:00. Duración: 6.605337 segundos. Modelo devuelto: `gemini-3.6-flash`.

```text
Sigue estos pasos para proteger tu API key:

1. **Crea un archivo `.env`** en la raíz del proyecto y guarda tu clave: `API_KEY=tu_clave_secreta`.
2. **Añade `.env` a tu `.gitignore`** para evitar que Git rastree y publique tus credenciales en el repositorio.
3. **Accede desde Python:** Instala `python-dotenv`, carga el archivo con `load_dotenv()` y lee la variable usando `os.getenv("API_KEY")`.

Así, tu clave se mantendrá segura localmente y jamás se subirá a GitHub.
```

Palabras aproximadas (`len(texto.split())`): 71.

```json
{
  "promptTokenCount": 33,
  "candidatesTokenCount": 135,
  "totalTokenCount": 989,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 33
    }
  ],
  "thoughtsTokenCount": 821,
  "serviceTier": "standard"
}
```

### Intento 11: gemini-3.5-flash-lite, P3

Fecha: 2026-10-23T18:45:48-03:00. Duración: 1.957089 segundos. Modelo devuelto: `gemini-3.5-flash-lite`.

```text
El código **429 (Too Many Requests)** significa que has enviado demasiadas peticiones al servidor en muy poco tiempo y te ha bloqueado temporalmente por seguridad (límite de velocidad).

**Qué debes hacer:**
1. **Espera:** Revisa si la cabecera `Retry-After` indica cuánto tiempo debes aguardar.
2. **Optimiza:** Reduce la frecuencia de tus peticiones, añade pausas (reintentos con *backoff* exponencial) y evita bucles.
```

Palabras aproximadas (`len(texto.split())`): 60.

```json
{
  "promptTokenCount": 30,
  "candidatesTokenCount": 107,
  "totalTokenCount": 137,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 30
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 12: gemini-3.6-flash, P3

Fecha: 2026-10-23T18:45:50-03:00. Duración: 7.024738 segundos. Modelo devuelto: `gemini-3.6-flash`.

```text
El error **429 (Too Many Requests)** significa que has superado el límite de peticiones permitidas por el servidor en un periodo determinado (*rate limit*).

**Qué hacer:**
1. **Espera:** Revisa la cabecera `Retry-After` en la respuesta para saber cuántos segundos esperar antes de reintentar.
2. **Espacia las solicitudes:** Disminuye la frecuencia de tus peticiones.
3. **Usa *Exponential Backoff*:** Duplica progresivamente el tiempo entre reintentos fallidos.
4. **Solicita más margen:** Contacta al proveedor para aumentar tu límite.
```

Palabras aproximadas (`len(texto.split())`): 75.

```json
{
  "promptTokenCount": 30,
  "candidatesTokenCount": 135,
  "totalTokenCount": 1263,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 30
    }
  ],
  "thoughtsTokenCount": 1098,
  "serviceTier": "standard"
}
```

## Precios, cálculo y reproducción

[Precios oficiales de Gemini](https://ai.google.dev/gemini-api/docs/pricing), consultados el 2026-10-23. Standard de pago por millón de tokens: Flash-Lite 0,30 USD entrada / 2,50 USD salida; Flash 0,75 USD entrada / 3,75 USD salida, promocional hasta 2026-12-31. La tarifa de salida incluye razonamiento.

La fórmula está en [arquitectura.md](arquitectura.md): entrada por su tarifa más salida visible y razonamiento por la tarifa de salida. Los costos son equivalentes a tarifas de pago; no verifican un cobro a la cuenta. No se activaron herramientas ni caché explícita.

Para reproducir, revisar las tarifas en `medir_modelos.py` y ejecutar `python docs/medir_modelos.py` desde la raíz. Hace 12 llamadas reales y reemplaza el JSON.

El [registro inicial con Gemini 3.8 Flash](mediciones_bloque9_inicial.json) se conserva separado. Los intentos exploratorios para escoger un candidato disponible no forman parte de esta serie controlada.

[Volver a la decisión de arquitectura](decision-arquitectura.md).
