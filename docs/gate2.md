# Gate 2 — Integración y orquestación

Fecha de verificación: 25 de noviembre de 2026. Repositorio: https://github.com/Jefferson-Santos-Hu/mi-primero-repositorio

## Entrega reunida

| Dimensión | Archivos y evidencia |
|---|---|
| Pipeline y persistencia | indexar_documentos.py, corpus/ (6 documentos propios), servicio_rag.py; reapertura comprobada en docs/gate2_evidencia.json |
| Actualización incremental | python indexar_documentos.py --actualizar; test_indice_incremental.py demuestra que solo se embedde el chunk modificado, sin duplicados |
| Recuperación y citas | evaluacion_recuperacion.py; resultados_evaluacion.txt: 11 consultas, 10 con fuente relevante; recall 1.0 para k=1 y k=3; el caso sin respuesta no entra en recall |
| Costo y latencia | registro_rag.py, registros_latencia_costo.jsonl, docs/evaluacion_rag.md; generación y embeddings reales |
| Personalización | decision.py, decision_personalizacion.md y docs/decision_evidencia.json; matriz RAG 2, PEFT 1, tuning completo 0; dataset propio de 12 ejemplos validado sin entrenar |
| Observabilidad | Eventos JSON por etapa con trace_id y consumo real, sin preguntas/documentos en logs; docs/gate2_evidencia.json separa la respuesta pública sintética de los logs operativos |
| Seguridad | Filtro sobre Document.page_content, rechazo de citas inexistentes, logs sin contenido; test_servicio_rag.py y test_gate2.py |
| Gobernanza | gobernanza.py; interrupt/Command probado en los caminos aprobar/rechazar; docs/registro_prompts.json y docs/supervision_evidencia.json |
| Riesgos | docs/matriz_riesgos.md: 7 riesgos propios y puntos concretos de supervisión para todos los inicialmente altos/críticos |
| Instalación | README.md, requirements.txt y verificar_entorno.py; Python 3.14.8 probado |

## Criterios no compensables

- Pipeline de punta a punta: verificado con consulta real a Gemini 3.5 Flash Lite y embeddings Gemini, respuesta sobre HTTP 429.
- Respuestas con fuentes: la corrida final cita cliente.md; el servicio rechaza citas inexistentes. Validar existencia de cita no demuestra fidelidad semántica.
- Logs sin contenido crudo: la corrida final comprueba que no contienen la pregunta ni los documentos; los eventos comparten trace_id. Las preguntas sintéticas aparecen en archivos de evidencia deliberadamente públicos, no en los logs operativos.
- Supervisión funcionando: el grafo se detiene antes de activar y reanuda según decisión explícita. Las decisiones del ensayo son simuladas y están identificadas como tales; no acreditan aprobación humana ni despliegue en producción.

`python -m pytest test_gate2.py -q`: 4 pruebas aprobadas. Suite completa del repositorio: 98 pruebas y 60 subpruebas aprobadas. Hay advertencias de deprecación de LangChain, documentadas; no hay fallos.

`python verificar_gate2.py`: consulta real con fuente, índice reabierto sin reindexar y 4 criterios no compensables verificados. Resultado detallado y fecha UTC en docs/gate2_evidencia.json.

## Autoevaluación orientativa del alumno, asistida

No es calificación del instructor ni una garantía de aprobación. Escala 0–100; pesos de la consigna.

| Dimensión | Peso | Estimación | Fundamento y límite |
|---|---|---|---|
| Pipeline funcional | 25 % | 95 | Consulta real y persistencia; actualización incremental probada localmente sin concurrencia |
| Recuperación/citación | 15 % | 85 | Recall 1.0 en 10 casos respondibles; corpus pequeño y sin evaluación semántica independiente |
| Costo/latencia | 10 % | 75 | Medición real por etapa y tokens de generación; costo monetario de embeddings no determinado |
| Personalización | 15 % | 90 | Decisión cuantificada y dataset validado; 12 ejemplos, sin tuning ni revisión independiente |
| Observabilidad | 15 % | 90 | Logs estructurados correlacionados y uso real; no hay plataforma de observabilidad externa |
| Seguridad/gobernanza | 20 % | 85 | Filtro, pruebas, riesgos y pausa ejecutable; patrones evadibles y aprobación solo en memoria |

Promedio ponderado: 88.0/100. Los cuatro criterios no compensables se comprueban aparte y no se sustituyen por este promedio.

## Límites declarados

El costo de generación es equivalente a tarifa estándar y no factura. No se inventa costo de embeddings; permanece sin determinar. La revisión cualitativa es asistida. Las evaluaciones de recuperación no prueban generalización ni resistencia a ataques nuevos. La revisión cruzada por Javier está pendiente: las observaciones propuestas no se atribuyen como hechas por él. El checkpoint de supervisión se pierde al reiniciar y no autentica al revisor; es el mecanismo didáctico requerido, no un flujo de autorización de producción. Docker corresponde al Módulo 3 y no es requisito de este Gate 2.


## Instalación desde clon nuevo

Verificación adicional completada desde GitHub con entorno virtual nuevo: 98 pruebas aprobadas, índice nuevo de 6 chunks con embeddings reales y consulta final citando cliente.md. Procedimiento y límites en docs/verificacion_gate2_clon_limpio.md.
