# Respaldo de la demo

Corrida de ensayo con modelo simulado explícito y caso real sin credencial. No es una grabación de defensa ni aprobación del instructor. Se omiten trace_id y latencias variables de las respuestas comparadas.

## PASO-1 Servicio vivo

Qué dices: El servicio está sano y anuncia modo simulado.
Petición: GET /salud
HTTP 200
```json
{
  "estado": "ok",
  "modelo_activo": "simulado",
  "servicio": "asistente_tecnico"
}
```

## PASO-2 Respuesta con fuente

Qué dices: Consulto HTTP 429: responde con backoff y cita cliente.md.
Petición: POST /consultas
HTTP 200
```json
{
  "estado": "ok",
  "modo": "simulado",
  "respuesta": "Ante HTTP 429 el cliente usa backoff exponencial con jitter y tres intentos [1].",
  "fuentes": [
    "cliente.md"
  ],
  "tokens": null,
  "costo_generacion_usd": null
}
```

## PASO-3 Catálogo HTTP local

Qué dices: El catálogo local distingue la cuota sin llamar al proveedor.
Petición: GET /errores/429
HTTP 200
```json
{
  "codigo_http": 429,
  "detalle": "Límite de cuota o frecuencia. Usar backoff exponencial con jitter y máximo de intentos; revisar la cuota."
}
```

## PASO-4 Error uniforme

Qué dices: Una entrada inválida devuelve 422 sin repetir datos sensibles.
Petición: POST /consultas
HTTP 422
```json
{
  "codigo": "entrada_invalida",
  "mensaje": "Revisa pregunta (1–4000 caracteres), k (1–6) y campos permitidos."
}
```

## PASO-5 Ataque rechazado

Qué dices: La instrucción de ignorar reglas se rechaza antes del modelo.
Petición: POST /consultas
HTTP 200
```json
{
  "estado": "rechazado",
  "respuesta": "No puedo atender instrucciones que alteren las reglas del sistema.",
  "fuentes": []
}
```

## PASO-6 Límite declarado

Qué dices: La capital de Mongolia queda fuera del catálogo simulado.
Petición: POST /consultas
HTTP 200
```json
{
  "estado": "sin_contexto",
  "modo": "simulado",
  "respuesta": "No encuentro esa información en el corpus de demostración.",
  "fuentes": [],
  "tokens": null,
  "costo_generacion_usd": null
}
```

## PASO-7 Falla honesta sin clave

Qué dices: El modo real sin clave devuelve 503, sin cambiar a simulación.
Petición: POST /consultas
HTTP 503
```json
{
  "codigo": "modelo_no_disponible",
  "mensaje": "No se pudo generar una respuesta validada. Revisa configuración, cuota y conexión."
}
```

