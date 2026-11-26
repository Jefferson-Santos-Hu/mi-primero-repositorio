# Informe del Gate 3
Fecha: 2026-11-26T15:15:42.007490+00:00
Modo: con Docker
Resultado: APRUEBA
Puntaje técnico: 94.05/100 (umbral 60); nota orientativa 6.55/7

El puntaje es una autoevaluación automática de fuentes ejecutadas, no calificación del instructor. Las fuentes de ficha, composición y transferencia incluyen sus revisiones humanas y muestran FALLA mientras falten. Esos fallos compensables reducen el puntaje. La defensa oral y la condición de corpus sintético se confirman por el evaluador; no las decide el programa. Una fuente omitida vale cero, nunca éxito. APRUEBA significa superar la rúbrica automática, no una calificación del instructor.

| Criterio | Peso | Puntos | Evidencia |
|---|---|---|---|
| C1 Problema, requerimientos y arquitectura | 10 | 5.00 | ficha, decisiones |
| C2 Funcionamiento end-to-end | 25 | 25.00 | frio, demo, stack, ejecucion |
| C3 Integración IA, orquestación y RAG | 15 | 15.00 | mitigaciones, ia |
| C4 Backend FastAPI y Docker | 15 | 14.46 | servicio, api_md, dockerfile, compose |
| C5 QA, pruebas y evaluación de calidad | 10 | 10.00 | pytest, matriz, parciales |
| C6 Seguridad, riesgos y trazabilidad | 10 | 10.00 | riesgos, secretos, registro |
| C7 Documentación técnica | 5 | 4.58 | readme, transferencia |
| C8 Demo y defensa técnica | 10 | 10.00 | guion, demo, respaldo |

## Comprobaciones

| Fuente | Resultado | Detalle |
|---|---|---|
| ficha | FALLA | ERROR: Revisión cruzada pendiente; no se acredita una revisión ajena |
| decisiones | PASA | 7 de 7 reglas cumplidas |
| frio | PASA | Ensayo en frío vigente |
| demo | PASA | 8 de 8 comprobaciones cumplidas; 89.9 segundos incluyendo teclado |
| respaldo | PASA | 8 de 8 comprobaciones cumplidas; 88.71 segundos incluyendo teclado |
| mitigaciones | PASA | Mitigaciones: True True límites observados: True regresiones: True |
| ia | PASA | 16 passed, 18 warnings in 2.27s |
| servicio | PASA | 11 de 11 casos de API cumplidos |
| api_md | PASA | API documentada vigente |
| dockerfile | PASA | 7 de 7 comprobaciones cumplidas |
| compose | FALLA | FALLA revisión por par confirmada |
| pytest | PASA | 135 passed, 21 warnings, 60 subtests passed in 3.04s |
| matriz | PASA | 6 de 6 reglas cumplidas |
| parciales | PASA | Plan y contratos verificados |
| riesgos | PASA | 6 de 6 reglas cumplidas |
| secretos | PASA | Escaneo público: 0 archivos con coincidencias |
| readme | PASA | 8 de 8 reglas cumplidas |
| transferencia | FALLA | FALLA confirmacion de revisor |
| guion | PASA | 9 de 9 reglas cumplidas |
| stack | PASA | Dos servicios sanos; proxy y salud verificados; modo simulado |
| ejecucion | PASA | 5 de 5 comprobaciones cumplidas |
| registro | PASA | 6 de 6 comprobaciones cumplidas |

## No compensables

- NC-1: Ejecución E2E en contenedores — comprobado técnicamente.
- NC-2: Endpoints funcionales y validados — comprobado técnicamente.
- NC-3: Defensa en vivo del alumno — requiere evaluador.
- NC-4: Sin credenciales ni datos personales reales en repositorio/corpus — comprobado técnicamente.

## Pendientes explícitos

- Revisión de alcance.
- Revisión de composición.
- Transferencia por compañero.
- Defensa oral del alumno y confirmaciones del evaluador.

## Lo que este informe no demuestra

No acredita que Javier haya revisado el proyecto ni que el alumno haya realizado una defensa oral. No mide calidad universal del modelo, carga, autenticación multiusuario ni seguridad de producción. La demo es simulada explícitamente; las llamadas reales se documentan por separado. Los pesos y el umbral no se modificaron para mejorar el resultado.
