# Registro de pruebas de la API
Fecha: 2026-11-25
Servicio probado: http://127.0.0.1:8000; cliente httpx externo sobre Uvicorn real.
Resultado: 11 de 11 casos cumplidos

| Caso | Descripción | Petición | Esperado | Obtenido | Resultado |
|---|---|---|---|---|---|
| V-01 | salud | GET /salud | 200 | 200 | PASA |
| V-02 | catálogo HTTP | GET /errores/429 | 200 | 200 | PASA |
| V-03 | respuesta citada | POST /consultas | 200 | 200 | PASA |
| I-01 | campo ausente | POST /consultas | 422 | 422 | PASA |
| I-02 | pregunta vacía | POST /consultas | 422 | 422 | PASA |
| I-03 | tipo numérico | POST /consultas | 422 | 422 | PASA |
| I-04 | ruta inexistente | GET /inexistente | 404 | 404 | PASA |
| I-05 | método incorrecto | DELETE /salud | 405 | 405 | PASA |
| I-06 | JSON incompleto | POST /consultas | 422 | 422 | PASA |
| I-07 | k fuera de límites | POST /consultas | 422 | 422 | PASA |
| I-08 | exceso de longitud | POST /consultas | 422 | 422 | PASA |
