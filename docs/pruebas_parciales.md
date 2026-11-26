# Pruebas parciales

Pruebas sin clave, red externa ni modelo real. Todas las interfaces inyectan dobles explícitos o usan datos locales sintéticos. `verificar_defectos.py` modifica únicamente copias temporales y exige un fallo de aserción, no un error de importación. Resultado real: 5 de 5 defectos detectados; detalles en defectos_resultados.json.

| Componente | Entrada | Salida | Doble | Archivo | Defecto introducido en copia | Detectado |
|---|---|---|---|---|---|---|
| cliente | respuesta HTTP 401 | ValueError sin reintento | requests.post y sleep simulados | tests/parciales/test_cliente_contrato.py | quitar 401 de errores de autenticación | Sí |
| recuperacion | Document con metadata | contexto y mapa de fuente | corpus temporal | tests/parciales/test_recuperar.py | devolver inventada.md | Sí |
| modelo | consulta HTTP 429 | modo simulado con fuente | ServicioSimulado explícito | tests/parciales/test_modelo.py | anunciar real estando simulado | Sí |
| api | pregunta numérica inválida | HTTP 422 uniforme | servicio Mock | tests/parciales/test_api_contrato.py | retornar HTTP 200 en error de validación | Sí |
| fundamentacion | respuesta con 99 intentos no soportados | rechazo estructural | Document sintético | tests/parciales/test_fundamentacion.py | desactivar control de números | Sí |

Cada archivo tiene al menos tres pruebas y una cuyo nombre comienza por test_contrato. La prueba de limitación de fundamentación demuestra que una afirmación semántica falsa sin cifras puede escapar: no se cuenta como seguridad resuelta.
