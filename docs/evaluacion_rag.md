# Medición real del flujo RAG

| k | Embedding ms | Búsqueda ms | Generación ms | Total ms | Costo generación USD |
|---|---|---|---|---|---|
| 1 | 1099.51 | 2.29 | 1485.70 | 2588.25 | 0.00008370 |
| 3 | 1115.53 | 7.22 | 1395.09 | 2518.62 | 0.00011910 |

Las dos ejecuciones consultaron realmente Gemini y citaron cliente.md. El índice se reabrió sin añadir chunks. Hay seis documentos propios, con chunks de 500 caracteres y solapamiento 60: en este corpus compacto cada documento cabe entero y conserva una regla coherente. Los IDs estables y la huella del corpus impiden duplicar o mezclar versiones.

La comparación es exploratoria de una sola muestra por configuración, no una estimación robusta de p95 ni una garantía de rendimiento. Cambian latencia de red y respuesta del proveedor entre llamadas. k=1 obtuvo recall 1.0 sobre los 10 casos respondibles y precisión media 0.909 sobre 11 casos; k=3 también recall 1.0, pero precisión 0.303. La pregunta sin respuesta tiene recall no aplicable y revela que recuperar documentos no equivale a poder responder.

Se conserva k=3 como configuración didáctica comparada; k=1 es candidato por precisión y menor contexto para este corpus, sujeto a validar preguntas nuevas y multifuente. La búsqueda no tiene un umbral de abstención semántica calibrado: el sistema pide abstenerse al modelo y valida números de cita, pero una cita existente no prueba que el texto la respalde.

El costo informado corresponde exclusivamente a generación, con promptTokenCount, candidatesTokenCount y thoughtsTokenCount reales. Tarifa Gemini 3.5 Flash Lite estándar: USD 0.30/M entrada y USD 2.50/M salida, verificada al 2026-11-25 en https://ai.google.dev/gemini-api/docs/pricing. Es equivalente de tarifa pagada y no factura. El costo de embeddings y el monetario total permanecen sin determinar porque esta integración no obtiene sus tokens reales.

Durante una primera prueba con k=3 el modelo no produjo citas válidas: el servicio rechazó la respuesta con ValueError. Se volvió a ejecutar la consulta y se conserva el resultado válido, sin transformar el fallo previo en éxito. Los logs operativos solo contienen longitudes, conteos y trace_id; este JSONL de evidencia contiene una pregunta sintética deliberadamente pública.
