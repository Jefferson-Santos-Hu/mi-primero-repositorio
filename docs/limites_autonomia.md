# Límites de autonomía del agente técnico

## Herramientas y nivel de riesgo

- `consultar_error_http`: bajo, consulta un catálogo local sintético. `incluir_detalle` cambia la salida y no modifica estado.
- `calcular_presupuesto`: bajo, realiza aritmética con cantidades explícitas. Es una estimación de referencia, no ejecuta pagos.

El agente no dispone de herramientas de escritura reversible ni de acciones irreversibles con impacto económico. No se añaden acciones financieras para simular una clasificación de riesgo que no existe en este proyecto.

## Herramientas que requieren aprobación humana

Las dos herramientas actuales son de lectura/cálculo y no requieren confirmación por invocación. Si se añadieran herramientas de escritura o pagos, deberán pasar una revisión de permisos y un control de aprobación fuera de los argumentos generados por el modelo antes de estar disponibles. El cambio de prompt tiene un mecanismo separado en `gobernanza.py`: LangGraph pausa mediante `interrupt` y solo activa la huella tras una reanudación explícita verdadera. Sus pruebas simulan aprobación y rechazo; no constituyen aprobación humana de producción. El historial en memoria es para el laboratorio y no autentica revisores ni usuarios.

## Revisión de trazas

Revisar cada nueva versión y semanalmente o cada 50 interacciones, lo que ocurra primero. `trazas_agente.jsonl` contiene ejecuciones reales con entradas sintéticas, selección de ambas herramientas y un saludo sin herramienta. Revisar llamadas fuera de propósito, herramientas repetidas, argumentos negativos o fuera de límites, ausencia de llamadas cuando sí hacen falta y respuestas que contradigan observaciones. El ejecutor limita a 4 iteraciones y 90 segundos de ejecución; cada llamada de red además tiene timeout. No se registra razonamiento interno ni firmas opacas del SDK. En uso con datos de usuarios debe sustituirse esta evidencia didáctica por un registro de metadatos, sin entrada ni respuesta cruda.

## Qué hacer ante un comportamiento inesperado

1. Detener la sesión y retirar la herramienta afectada de `crear_ejecutor`.
2. Revisar selección y argumentos de la traza, conservando un caso sintético que reproduzca el fallo.
3. Ajustar docstring, esquema Pydantic o instrucciones; añadir una prueba del comportamiento observado.
4. Volver a correr las pruebas de herramientas y aislamiento; comprobar con el modelo real sin acciones externas.
5. Revisar el cambio de prompt con supervisión antes de habilitarlo. Las pruebas locales de memoria pasan; su validación real se registra por separado y no se deduce de un mock.
