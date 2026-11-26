# Limitaciones del MVP

| ID | Qué no hace | Origen ejecutable | Riesgo | Efecto | Decisión |
|---|---|---|---|---|---|
| LIM-01 | No demuestra implicación semántica de cada afirmación | H-04 en alucinaciones.py y test_limite_parafrasis_falsa_puede_escapar | R-06 | Una frase falsa con cita existente y sin cifra nueva puede pasar | Usuario contrasta fuente antes de actuar; mantener residual alto |
| LIM-02 | No detecta toda paráfrasis de inyección | A-07 en ataques.py | R-01 | Instrucciones reescritas pueden evadir la lista de patrones | Mantener roles, corpus controlado y revisión antes de incorporar documentos |
| LIM-03 | El modo simulado no mide calidad, cuota ni costo de Gemini | S-08 y S-10 en escenarios.py; modelo_simulado.py | R-08 | Solo responde un catálogo limitado de demostración; se abstiene fuera del catálogo | Declarar modo en banner y registrar evidencia real por separado |
| LIM-04 | La aprobación del grafo no autentica al revisor ni sobrevive reinicio | test_gobernanza.py y gobernanza.py | R-09 | Una pausa local no equivale a autorización durable de producción | No desplegar como control de acceso; repetir revisión tras reinicio |

La API es un laboratorio local sin autenticación multiusuario. No se expone a Internet. El costo de embeddings queda sin determinar cuando el proveedor no expone su contador en esta integración. Ninguna de estas condiciones se disfraza como una mitigación verificada. Revisión cruzada y defensa oral siguen pendientes de sus participantes humanos.
