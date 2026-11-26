# Matriz de riesgos verificada
Huella: 8449862d3bef901d3062bc03b85da298e9ba9032e3847cd9254f874b4fa0bbe4

Estimaciones de diseño, no probabilidades medidas. Un estado parcial mantiene residual alto.

| ID | Riesgo | P | I | Inicial | Mitigación | Evidencia ejecutable | Estado | Residual | Supervisión |
|---|---|---|---|---|---|---|---|---|---|
| R-01 | Inyección mediante contexto no confiable | 3 | 4 | 12 | Filtro de patrones y separación de roles | test_servicio_rag.py::test_inyeccion_se_excluye_antes_del_modelo | parcial | 12 ALTO | Revisión humana del corpus y descartes antes de cada indexación |
| R-06 | Afirmación falsa con cita existente | 4 | 3 | 12 | Control estructural y declaración de límite semántico | tests/parciales/test_fundamentacion.py::test_limite_parafrasis_falsa_puede_escapar | parcial | 12 ALTO | Usuario contrasta cada respuesta con el documento antes de actuar |
| R-09 | Aprobación local sin identidad ni persistencia durable | 3 | 4 | 12 | Pausa LangGraph didáctica; no habilitar producción | test_gobernanza.py::test_interrupcion_y_aprobacion_o_rechazo | parcial | 12 ALTO | Titular vuelve a revisar tras reinicio; no usar como autorización de producción |
| R-02 | Citas inexistentes o cifras inventadas | 3 | 3 | 9 | Validación de índices y números contra fuentes | tests/parciales/test_fundamentacion.py::test_rechaza_numero_inventado_y_cita | verificado | 6 MEDIO | Contrastar fuente antes de aplicar recomendaciones |
| R-04 | Cuota consumida por reintentos ilimitados | 3 | 3 | 9 | Intentos y esperas acotados | tests/parciales/test_cliente_contrato.py::test_backoff_no_duerme_despues_del_ultimo_intento | verificado | 6 MEDIO | Titular revisa cuota cuando se agotan los intentos |
| R-03 | Fuga de clave o pregunta en errores y logs | 3 | 5 | 15 | Errores uniformes, metadatos y exclusión .env | test_api.py::test_error_proveedor_y_ruta_no_exponen_datos, test_gate2.py::test_logs_json_correlacionados_sin_contenido | verificado | 5 MEDIO | Titular revisa diff y escaneo antes de publicar |
| R-05 | Índice duplicado o de versiones mezcladas | 3 | 3 | 9 | IDs estables, manifiesto y actualización explícita | test_indice_incremental.py::test_actualizacion_incremental_solo_embedde_cambios | verificado | 3 BAJO | Detener servicio y revisar corpus antes de actualizar |
| R-07 | Mezcla de historiales entre sesiones | 3 | 3 | 9 | Historial por session_id; servicio público RAG sin memoria de agente | test_agente.py::test_memoria_dos_turnos_y_aislamiento | verificado | 3 BAJO | Revisar aislamiento tras cambios de memoria |
| R-08 | Demo simulada confundida con proveedor real | 3 | 3 | 9 | Modo explícito en salud, respuesta y banner; sin fallback silencioso | test_api.py::test_modo_simulado_explicito_sin_proveedor | verificado | 3 BAJO | Anunciar el modo antes de la demo |

R-01 y R-06 son parciales: A-07 y H-04 documentan evasiones, no éxitos de mitigación. R-09 prueba la pausa, no identidad del revisor ni persistencia durable. No se inventa una revisión de Javier; sigue pendiente.

El prompt vigente y la pausa del Gate 2 siguen en docs/registro_prompts.json y gobernanza.py. La matriz se amplía para el Módulo 3, sin borrar la evidencia histórica del Gate 2.
