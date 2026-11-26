# API del asistente técnico

Base API local: http://127.0.0.1:8000. Proxy de interfaz: http://127.0.0.1:8080/api.

Ejemplos generados ejecutando FastAPI con MODELO=simulado. No prueban disponibilidad de Gemini. Se omiten trace_id y auditoría por ser variables.

## GET /salud

Sin cuerpo.
HTTP 200
```json
{
  "estado": "ok",
  "modelo_activo": "simulado",
  "servicio": "asistente_tecnico"
}
```

## GET /errores/429

Sin cuerpo.
HTTP 200
```json
{
  "codigo_http": 429,
  "detalle": "Límite de cuota o frecuencia. Usar backoff exponencial con jitter y máximo de intentos; revisar la cuota."
}
```

## POST /consultas

Entrada: `{"pregunta": "HTTP 429"}`
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

## POST /consultas

Entrada: `{"pregunta": ""}`
HTTP 422
```json
{
  "codigo": "entrada_invalida",
  "mensaje": "Revisa pregunta (1–4000 caracteres), k (1–6) y campos permitidos."
}
```

## DELETE /salud

Sin cuerpo.
HTTP 405
```json
{
  "codigo": "error_http",
  "mensaje": "Recurso no disponible."
}
```

## GET /inexistente

Sin cuerpo.
HTTP 404
```json
{
  "codigo": "no_encontrado",
  "mensaje": "Recurso no disponible."
}
```

## Validación y fallos

POST /consultas admite pregunta string de 1–4000 caracteres, sin solo espacios; k entero 1–6, default 3; campos extra rechazados. Error uniforme contiene codigo y mensaje, sin el valor enviado. Los fallos del proveedor, clave o validación de fundamentación devuelven 503. La salud del proceso no acredita la cuota del proveedor.

## Documentación OpenAPI

GET /openapi.json y /docs describen el contrato generado. No hay autenticación multiusuario: el servicio se mantiene ligado a localhost.
