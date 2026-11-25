# Matriz de riesgos del asistente técnico

Escala cualitativa de probabilidad e impacto de 1 a 5. Puntaje=P×I; bajo <4, medio 4–8, alto 9–14 y crítico ≥15. Son estimaciones de diseño para este MVP sintético, no probabilidades medidas. Residual considera únicamente controles implementados; una prueba no elimina el riesgo.

| ID | Riesgo concreto | P | I | Puntaje / categoría | Mitigación implementada y bloque | Verificación | Residual P×I |
|---|---|---|---|---|---|---|---|
| R-01 | Un chunk instruye ignorar el sistema y obtener secretos | 3 | 4 | 12 alto | Patrón de inyección, exclusión previa, rol sistema y delimitación (31) | test_inyeccion_se_excluye_antes_del_modelo | 2×4=8 medio |
| R-02 | Una respuesta cita una fuente inexistente | 3 | 3 | 9 alto | Validación de índices de citas, rechazo cerrado (26/31) | test_cita_inventada_falla_cerrado | 2×3=6 medio |
| R-03 | Se filtra una pregunta o clave en un error HTTP o log | 3 | 5 | 15 crítico | Errores externos uniformes; logs con tipos, longitudes y conteos; .env ignorado (14/31/36) | test_error_proveedor_y_ruta_no_exponen_datos y test_servicio_cita_y_traza_sin_texto; escaneo de Git previo a push | 1×5=5 medio |
| R-04 | La API consume cuota sin límite ante fallos transitorios | 3 | 3 | 9 alto | Backoff con jitter, 3 intentos y tope; auth no se reintenta (13) | test_cliente.py: recuperación, agotamiento y no-reintento | 2×3=6 medio |
| R-05 | Un cambio del corpus mezcla chunks de versiones diferentes | 3 | 3 | 9 alto | Huella del corpus, IDs estables y rechazo de índice incompatible (24) | test_chunks_estables_y_metadata; reapertura real de índice | 1×3=3 bajo |
| R-06 | La respuesta usa una cita existente pero afirma algo no sustentado | 4 | 3 | 12 alto | Contexto limitado, pedido de abstención y evaluación cualitativa (17/26/27) | evaluación de 11 consultas y revisión asistida de 10 salidas | 3×3=9 alto |
| R-07 | Se mezclan historiales de sesiones | 3 | 3 | 9 alto | Diccionario por session_id y pruebas de aislamiento (22) | test_memoria_dos_turnos_y_aislamiento | 1×3=3 bajo |

## Supervisión y límites

R-03 exige revisión humana de los archivos públicos antes de cambios de despliegue y de cualquier ampliación de logs. R-06 conserva residual alto: las respuestas del MVP son apoyo técnico que debe revisarse contra las fuentes; no se autoriza ejecutar comandos automáticamente. Una validación de número de cita no es entailment semántico. No existe revisión por pares acreditada: las revisiones presentes son asistidas y deben contrastarse por el alumno/evaluador.

`gobernanza.py` implementa una pausa real con LangGraph antes de activar una huella propuesta. `docs/supervision_evidencia.json` muestra la pausa pendiente; `test_gobernanza.py` verifica los caminos de aprobación y rechazo con decisiones simuladas. El control de identidad del revisor, persistencia durable de aprobaciones y aplicación de versiones en producción quedan fuera del MVP local; no se anuncia su existencia.

## Versionado

`docs/registro_prompts.json` registra texto, versión y SHA-256 del sistema. Cada consulta de ServicioRAG incluye esa huella y los eventos la correlacionan con trace_id. Cambiar el prompt requiere nueva versión, repetir casos de regresión, revisar diferencias y resolver la revisión humana. Un reinicio pierde el checkpoint de memoria: se debe volver a solicitar revisión, nunca suponer aprobación.

## Incertidumbre y frecuencia

Revisar esta matriz en cada cambio de corpus, prompt, modelo, herramienta o endpoint, y semanalmente en uso. R-01, R-02, R-04, R-06 y R-07 están cerca de cambios de categoría al variar un punto una de sus estimaciones; requieren especial contraste con otra persona. Ante fuga, retirar publicación afectada y rotar la clave con el titular; ante respuestas incorrectas, suspender generación y conservar evidencia sintética del fallo.

## Puntos de supervisión por riesgo inicial alto o crítico

| Riesgo | Punto concreto de supervisión | Responsable previsto | Acción ante fallo |
|---|---|---|---|
| R-01 | Revisar corpus y descartes antes de indexar material nuevo y antes de autorizar un prompt | titular/revisor técnico | Retirar documento y repetir prueba de inyección |
| R-02 | Revisar fuentes y resultados de citas antes de habilitar una versión | titular/revisor técnico | Mantener rechazo de respuesta y corregir generación |
| R-03 | Revisión del diff y escaneo de secretos antes de publicar o ampliar logs | titular del repositorio | Bloquear publicación y rotar credencial si se expuso |
| R-04 | Revisar cuota y consumo después de agotamiento de reintentos; no autorizar bucles ilimitados | titular de la API | Pausar consultas y resolver cuota manualmente |
| R-05 | Aprobar cambios de corpus y ejecutar actualización incremental con servicio detenido | titular/revisor técnico | Restaurar versión anterior del corpus y directorio |
| R-06 | Contrastar respuesta con fuente antes de aplicar cualquier recomendación técnica | usuario del asistente | No ejecutar recomendación no sustentada |
| R-07 | Revisar pruebas de aislamiento antes de modificar el manejo de sesiones | titular/revisor técnico | Deshabilitar memoria y corregir contrato de sesión |

La aprobación programática del cambio de prompt corresponde a `crear_supervision`; las revisiones anteriores son procedimientos operativos previstos, no afirmaciones de que otra persona ya los haya realizado.
