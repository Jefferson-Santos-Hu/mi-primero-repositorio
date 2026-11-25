# Propuesta de revisión para Javier Omar Muñoz Muñoz

Estado: BORRADOR PENDIENTE DE CONFIRMACIÓN DEL REVISOR.
Autor de las observaciones propuestas: asistencia automatizada. El alumno indicó el nombre del compañero; no se ha recibido una evaluación suya. No acredita revisión cruzada, ejecución por un tercero ni ensayo de defensa.

| ID | Observación propuesta para contrastar | Evidencia que debe revisar Javier | Decisión propuesta |
|---|---|---|---|
| REV-01 | El alcance de soporte técnico es más pequeño y verificable que un asistente general. Mantener entrenamiento fuera del MVP. | docs/ficha_diseno_funcional.md y decision_personalizacion.md | Mantener RF-07 fuera del MVP. |
| REV-02 | La interfaz debe mostrar fuentes y errores sin insertar HTML generado por el modelo. | interfaz/app.js usa textContent | Mantener salida como texto y probarla en navegador. |
| REV-03 | Las citas numéricas solo validan que existe una fuente; falta comprobar soporte semántico de cada afirmación. | servicio_rag.py y riesgo R-06 | Declarar límite y exigir revisión de fuentes. |
| REV-04 | La salud del proceso no demuestra que Gemini tenga cuota o que el índice esté listo. | GET /salud frente a POST /consultas | Documentar diferencia y probar ambos. |
| REV-05 | El índice debe reutilizarse sin duplicados y rechazar corpus cambiado. | indexar_documentos.py y manifiesto | Verificar reinicio y cambio de corpus en una copia. |
| REV-06 | La aprobación de pruebas del grafo no acredita autorización humana de producción. | gobernanza.py y test_gobernanza.py | Mantener revisión pendiente y declarar falta de identidad/durabilidad. |

## Pasos que debe realizar el revisor

1. Clonar el repositorio siguiendo únicamente el README y configurar su propia clave local, sin compartirla.
2. Ejecutar las pruebas y, con Docker disponible, levantar la composición, consultar y detenerla.
3. Comprobar las observaciones y registrar cuáles acepta, rechaza o modifica, con fecha y evidencia.
4. Escuchar la defensa con cronómetro y comentar claridad, exactitud y tiempo.

## Registro real recibido

Ninguno hasta el momento. Los campos de fecha de ejecución, resultado externo y comentarios personales de Javier permanecen sin completar. Este borrador se sustituirá o complementará con sus observaciones efectivas.
