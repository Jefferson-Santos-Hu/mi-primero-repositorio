# Comparación de modelos — evidencia del Bloque 9

Fecha de inicio: 2026-10-23T18:32:08-03:00

4 repeticiones de P1 por modelo, alternando modelos; P2 y P3 una vez por modelo. Mismo POST y configuración predeterminada del módulo; sin caché explícita, herramientas ni streaming.

Las configuraciones de razonamiento son las predeterminadas de cada modelo; no se modificaron para igualarlas. La medición refleja cómo el módulo actual los solicita.

## Preguntas

**P1:** Responde en español en un máximo de 80 palabras: ¿Para qué sirve un entorno virtual de Python y cómo lo creas con venv?

**P2:** Responde en español en un máximo de 80 palabras: ¿Cómo protejo una API key en un proyecto Python con Git usando .env y .gitignore?

**P3:** Responde en español en un máximo de 80 palabras: Mi petición HTTP devuelve 429. ¿Qué significa y qué debo hacer?

## Todos los intentos, en orden de ejecución

| Intento | Modelo solicitado | Pregunta | Segundos | Resultado | Costo equivalente Standard USD |
|---:|---|---|---:|---|---:|
| 1 | gemini-3.5-flash-lite | P1 | 2.176795 | Texto recibido | 0.0003493 |
| 2 | gemini-3.8-flash | P1 | 90.072782 | Gemini superó el tiempo de espera. Intenta nuevamente. | No calculable: sin usageMetadata |
| 3 | gemini-3.5-flash-lite | P1 | 1.285718 | Texto recibido | 0.0002418 |
| 4 | gemini-3.8-flash | P1 | 90.088493 | Gemini superó el tiempo de espera. Intenta nuevamente. | No calculable: sin usageMetadata |
| 5 | gemini-3.5-flash-lite | P1 | 2.009059 | Texto recibido | 0.0003568 |
| 6 | gemini-3.8-flash | P1 | 90.094687 | Gemini superó el tiempo de espera. Intenta nuevamente. | No calculable: sin usageMetadata |
| 7 | gemini-3.5-flash-lite | P1 | 1.925330 | Texto recibido | 0.0002593 |
| 8 | gemini-3.8-flash | P1 | 90.081967 | Gemini superó el tiempo de espera. Intenta nuevamente. | No calculable: sin usageMetadata |
| 9 | gemini-3.5-flash-lite | P2 | 2.022987 | Texto recibido | 0.0003349 |
| 10 | gemini-3.8-flash | P2 | 90.087090 | Gemini superó el tiempo de espera. Intenta nuevamente. | No calculable: sin usageMetadata |
| 11 | gemini-3.5-flash-lite | P3 | 2.341531 | Texto recibido | 0.0002965 |
| 12 | gemini-3.8-flash | P3 | 4.428900 | Gemini respondió HTTP 503. El servicio no pudo completar la solicitud. Intenta más tarde. | No calculable: sin usageMetadata |

Los errores se incluyen y no se sustituyen por tiempos de respuesta exitosos. No se infiere facturación de las peticiones fallidas.

## Evaluación cualitativa asistida

Se revisaron los textos reales según pertinencia, corrección de conceptos básicos, utilidad de los pasos y brevedad. No es una evaluación ciega ni una muestra estadística.

| Pregunta | Flash-Lite | Flash |
|---|---|---|
| P1 | Explica aislamiento de dependencias y muestra `python -m venv`; útil para el alcance básico. La activación en Windows debe elegirse según la terminal; el README ya indica `Activate.ps1` para PowerShell. | Sin texto: no evaluable. |
| P2 | Indica `.env`, `.gitignore`, `load_dotenv` y `os.getenv`; cubre la protección básica. No explica cómo retirar una clave ya filtrada: sería necesario rotarla. | Sin texto: no evaluable. |
| P3 | Identifica 429, `Retry-After`, reducción de frecuencia y backoff. Es una respuesta introductoria; no detalla cómo distinguir cuota agotada de límite temporal. | Sin texto: no evaluable. |

Flash-Lite cumple el nivel introductorio de las tres consultas, con los límites descritos. No se concluye que supere la calidad de Flash, porque ese candidato no respondió.

## Respuestas completas

Se normalizan únicamente espacios al final de las líneas para Markdown. El texto original exacto permanece en el JSON.

### Intento 1: gemini-3.5-flash-lite, P1

Fecha: 2026-10-23T18:32:08-03:00. Duración: 2.176795 segundos.

```text
Un **entorno virtual** sirve para aislar las dependencias de un proyecto Python, evitando conflictos entre versiones de librerías en tu sistema.

Para crearlo y activarlo con `venv`, usa estos comandos en tu terminal:

1. **Crear el entorno** (reemplaza `mi_entorno` por el nombre que prefieras):
   ```bash
   python -m venv mi_entorno
   ```

2. **Activar el entorno**:
   * En Windows: `mi_entorno\Scripts\activate`
   * En Mac/Linux: `source mi_entorno/bin/activate`
```

Palabras aproximadas (`len(texto.split())`): 63.

usageMetadata devuelto:

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 136,
  "totalTokenCount": 167,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 2: gemini-3.8-flash, P1

Fecha: 2026-10-23T18:32:10-03:00. Duración: 90.072782 segundos.

Gemini superó el tiempo de espera. Intenta nuevamente.

### Intento 3: gemini-3.5-flash-lite, P1

Fecha: 2026-10-23T18:33:40-03:00. Duración: 1.285718 segundos.

```text
Un entorno virtual de Python sirve para aislar las dependencias de un proyecto, evitando conflictos entre diferentes versiones de paquetes en tu sistema.

Para crearlo, abre tu terminal en la carpeta del proyecto y ejecuta el comando:

`python -m venv venv`

Luego, actívalo con `venv\Scripts\activate` (en Windows) o `source venv/bin/activate` (en Mac/Linux). ¡Listo!
```

Palabras aproximadas (`len(texto.split())`): 53.

usageMetadata devuelto:

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 93,
  "totalTokenCount": 124,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 4: gemini-3.8-flash, P1

Fecha: 2026-10-23T18:33:41-03:00. Duración: 90.088493 segundos.

Gemini superó el tiempo de espera. Intenta nuevamente.

### Intento 5: gemini-3.5-flash-lite, P1

Fecha: 2026-10-23T18:35:11-03:00. Duración: 2.009059 segundos.

```text
Un **entorno virtual** sirve para aislar las dependencias de un proyecto Python, evitando conflictos entre versiones de librerías instaladas en el sistema.

Para crearlo y activarlo, usa estos comandos en tu terminal:

1. **Crear el entorno** (llamado *venv*):
   ```bash
   python -m venv venv
   ```

2. **Activar el entorno**:
   * En Windows: `venv\Scripts\activate`
   * En Mac/Linux: `source venv/bin/activate`

Una vez activo, cualquier librería que instales con `pip` solo afectará a ese proyecto.
```

Palabras aproximadas (`len(texto.split())`): 71.

usageMetadata devuelto:

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 139,
  "totalTokenCount": 170,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 6: gemini-3.8-flash, P1

Fecha: 2026-10-23T18:35:13-03:00. Duración: 90.094687 segundos.

Gemini superó el tiempo de espera. Intenta nuevamente.

### Intento 7: gemini-3.5-flash-lite, P1

Fecha: 2026-10-23T18:36:43-03:00. Duración: 1.925330 segundos.

```text
Un **entorno virtual** de Python sirve para aislar las dependencias de un proyecto, evitando conflictos entre diferentes versiones de paquetes en tu sistema.

Para crearlo, abre tu terminal en la carpeta del proyecto y ejecuta el siguiente comando:

```bash
python -m venv venv
```

Esto genera una carpeta llamada `venv`. Para activarlo, usa `venv\Scripts\activate` en Windows o `source venv/bin/activate` en macOS/Linux.
```

Palabras aproximadas (`len(texto.split())`): 61.

usageMetadata devuelto:

```json
{
  "promptTokenCount": 31,
  "candidatesTokenCount": 100,
  "totalTokenCount": 131,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 31
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 8: gemini-3.8-flash, P1

Fecha: 2026-10-23T18:36:45-03:00. Duración: 90.081967 segundos.

Gemini superó el tiempo de espera. Intenta nuevamente.

### Intento 9: gemini-3.5-flash-lite, P2

Fecha: 2026-10-23T18:38:15-03:00. Duración: 2.022987 segundos.

```text
1. Instala la librería para variables de entorno: `pip install python-dotenv`.
2. Crea un archivo llamado `.env` en la raíz de tu proyecto y guarda tu clave así: `API_KEY=tu_clave_secreta`.
3. Crea un archivo `.gitignore` y añade `.env` para evitar que Git lo suba al repositorio.
4. En tu código Python, cárgala de forma segura:
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()
   api_key = os.getenv("API_KEY")
```
```

Palabras aproximadas (`len(texto.split())`): 66.

usageMetadata devuelto:

```json
{
  "promptTokenCount": 33,
  "candidatesTokenCount": 130,
  "totalTokenCount": 163,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 33
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 10: gemini-3.8-flash, P2

Fecha: 2026-10-23T18:38:17-03:00. Duración: 90.087090 segundos.

Gemini superó el tiempo de espera. Intenta nuevamente.

### Intento 11: gemini-3.5-flash-lite, P3

Fecha: 2026-10-23T18:39:48-03:00. Duración: 2.341531 segundos.

```text
El código **429 (Too Many Requests)** significa que has superado el límite de peticiones permitidas por el servidor en un tiempo determinado (por ejemplo, 100 solicitudes por minuto).

**Qué debes hacer:**
1. **Espera:** Revisa la cabecera `Retry-After` para saber cuánto tiempo esperar antes de reintentar.
2. **Optimiza:** Reduce la frecuencia de tus peticiones, implementa la técnica de *caching* y usa esperas exponenciales (*backoff*) en tu código.
```

Palabras aproximadas (`len(texto.split())`): 66.

usageMetadata devuelto:

```json
{
  "promptTokenCount": 30,
  "candidatesTokenCount": 115,
  "totalTokenCount": 145,
  "promptTokensDetails": [
    {
      "modality": "TEXT",
      "tokenCount": 30
    }
  ],
  "serviceTier": "standard"
}
```

### Intento 12: gemini-3.8-flash, P3

Fecha: 2026-10-23T18:39:50-03:00. Duración: 4.428900 segundos.

Gemini respondió HTTP 503. El servicio no pudo completar la solicitud. Intenta más tarde.

## Fuente de precios y reproducción

[Precios oficiales de Gemini](https://ai.google.dev/gemini-api/docs/pricing), consulta 2026-10-23; Standard de pago, USD por millón: Flash-Lite 0,30 entrada / 2,50 salida; Flash 0,75 entrada / 3,75 salida (promoción hasta 2026-12-31). Incluye razonamiento en salida.

El costo calculado es una estimación a tarifa de pago; no acredita un cobro real. No hay herramientas ni caché explícita en las peticiones.

Para reproducir: revisar las tarifas de `medir_modelos.py` y ejecutar `python docs/medir_modelos.py` desde la raíz. Consume cuota y reemplaza el JSON. Las credenciales permanecen en `.env` y no se registran.

[Volver a la decisión](decision-arquitectura.md).
