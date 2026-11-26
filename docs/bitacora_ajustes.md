# Bitácora de ajustes

| ID | Problema observado | Hipótesis | Cambio | Evidencia antes | Evidencia después | Decisión |
|---|---|---|---|---|---|---|
| IT-01 | La interfaz respondía sin decir que usaba simulación | Un usuario podría creer que la demo llamó a Gemini | Mostrar el modo obtenido de GET /api/salud | DOM de la primera prueba mostró Consulta terminada y cliente.md, sin modo | Prueba del banner en interfaz y salud del contenedor | Conservar: modo explícito; verificar banner al recargar |
| IT-02 | La mera existencia de [1] permitía cifras inventadas | Comprobar cifras contra los chunks citados detecta invenciones numéricas | Añadir comprobar_fundamentacion a la salida del RAG | Regla anterior solo verificaba índices de cita; no contrastaba cifras | test_rechaza_numero_inventado_y_cita y mutación de la regla detectada | Conservar: control numérico/estructural; no presentarlo como prueba semántica |

Las respuestas de las sondas son sintéticas y controladas para comprobar el detector, no alucinaciones atribuidas a una ejecución real de Gemini. La matriz E2E se ejecuta con modo simulado a propósito y la evidencia de Gemini real se mantiene separada.
