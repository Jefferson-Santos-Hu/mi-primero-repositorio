# Decisión de arquitectura: elección de modelo

**Fecha del registro, precios y mediciones:** 2026-10-23 (America/Santiago).

**Responsable del proyecto:** Jefferson Santos. **Estado:** aceptada para el prototipo actual.

## Modelo elegido

Se mantiene **Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`)**, ya utilizado
en los bloques 4 y 7. El caso evaluado es la CLI Python actual: recibe una
pregunta y devuelve texto en español mediante una petición HTTPS a Gemini.
Las consultas de prueba son de aprendizaje técnico básico: entornos virtuales,
protección de credenciales y errores HTTP. No se presupone una aplicación de
producción ni un asistente especializado ya construido.

## Diagrama de arquitectura

![Arquitectura del prototipo](diagrama_arquitectura.png)

El [detalle del flujo](arquitectura.md) identifica las tres funciones reales
(`armar_peticion`, `enviar_peticion`, `extraer_texto`), su orquestador, la
credencial local, las excepciones y el dato que cruza cada flecha. También
identifica dónde la herramienta de medición calcula el costo desde
`usageMetadata`. La CLI imprime texto; el costo se registra en la comparación.

## Comparación de candidatos

Tarifas **Standard de pago**, USD para texto sin caché explícita, herramientas
ni procesamiento por lotes. Consultadas el 2026-10-23 en la
[página oficial de precios de Gemini](https://ai.google.dev/gemini-api/docs/pricing).
La tarifa de salida incluye razonamiento. No se afirma que estos importes
se hayan cobrado: el nivel de facturación de la cuenta no se verificó.

| Criterio | Gemini 3.5 Flash-Lite | Gemini 3.6 Flash |
|---|---|---|
| ID solicitado | `gemini-3.5-flash-lite` | `gemini-3.6-flash` |
| Costo por 1.000 tokens de entrada | 0,00030 USD | 0,00075 USD |
| Costo por 1.000 tokens de salida | 0,00250 USD | 0,00375 USD |
| Latencia promedio observada, misma P1 repetida 4 veces | 1,908 segundos | 6,949 segundos |
| Calidad para las tres preguntas del caso | Buena: 3/3 respuestas útiles; explica venv, .env y 429. En 429 atribuye imprecisamente el límite a seguridad. | Buena: 3/3 respuestas útiles; en 429 distingue rate limit y recomienda backoff. En credenciales usa una garantía demasiado absoluta. |
| Peticiones exitosas en la serie completa | 6/6 | 6/6 |

Precios originales por millón de tokens (entrada/salida): 0,30/2,50 USD para
Flash-Lite y 0,75/3,75 USD para Flash. Se dividieron por 1.000 para la tabla.
Los precios de Flash son promocionales hasta el 31 de diciembre de 2026;
la página anuncia 1,50/7,50 USD por millón desde el 1 de enero de 2027.
Las tarifas de ambos modelos deben volver a consultarse antes de presupuestar.

**Método:** cuatro repeticiones de la misma P1 por modelo, alternando candidatos,
y una ejecución de P2 y P3 por candidato. Se cronometró `enviar_peticion` con
`time.perf_counter()`, desde el envío hasta convertir la respuesta completa
a JSON. Se usaron los mismos prompts, equipo, conexión y código, sin reintentos
automáticos ni streaming; el timeout de lectura fue 90 segundos.
Cada modelo conservó su configuración predeterminada de razonamiento, por lo
que se compara el uso real de la aplicación y no una igualdad de cómputo interno.

La calidad se revisó sobre las tres preguntas distintas según pertinencia,
corrección de los conceptos básicos, utilidad de los pasos y brevedad.
Para P1 se tomó la primera respuesta para el análisis cualitativo; las cuatro
se usaron para latencia y todas se conservan. Es una revisión cualitativa
asistida, no ciega, y una muestra pequeña; no demuestra superioridad general.
Los textos completos, tokens, costos calculados y tiempos están en el
[informe de comparación](comparacion-modelos.md) y el [JSON original](mediciones_bloque9.json).

## Justificación

El criterio que más pesa para esta CLI educativa es **la latencia, siempre
que la respuesta cubra lo esencial**. Ambos modelos respondieron las tres
preguntas con pasos útiles. Flash fue más preciso al explicar 429, pero esa
diferencia puntual no justifica para este alcance esperar aproximadamente
3.64 veces más en la prueba repetida.
La revisión también detectó límites en ambos, documentados en el informe;
las respuestas generadas no sustituyen la verificación técnica.

El costo refuerza la decisión: Flash cobra 2,5 veces por token de entrada y
1,5 veces por token de salida respecto de Flash-Lite. Es una comparación de
tarifas por token; el costo por petición además depende de cuántos tokens
produzca cada modelo, incluidos los de razonamiento.

Como escenario hipotético de escala, 1.000 tokens de entrada y 200 de salida
(incluido razonamiento) equivalen a 0,00080 USD con Flash-Lite y 0,00150 USD
con Flash. Con 50.000 peticiones iguales serían 40 USD y 75 USD, sin impuestos
ni servicios adicionales. Este escenario no reemplaza los consumos medidos.

## Alternativa descartada y por qué

Se descarta **Gemini 3.6 Flash (`gemini-3.6-flash`) para esta versión**: aunque
sus respuestas sirven para el caso y su explicación de 429 es más precisa,
la mayor espera observada y las tarifas superiores no compensan ese beneficio
para consultas introductorias breves. No se concluye que sea peor para tareas
complejas ni que esta latencia sea permanente.

La elección se revisará si cambia el caso de uso, la calidad exigida, los
precios o la disponibilidad. La aplicación depende de internet y de la cuota
del proveedor; el manejo de errores no elimina esas dependencias.

## Evidencia y reproducción

- [Diagrama y fórmula del costo](arquitectura.md).
- [Tabla de cada ejecución y evaluación de respuestas](comparacion-modelos.md).
- [Serie completa actual: 12 respuestas válidas](mediciones_bloque9.json).
- [Registro inicial con fallos de Gemini 3.8 Flash](mediciones_bloque9_inicial.json).
  Se conserva como antecedente; no se mezcla con los promedios actuales.
- [Herramienta de medición](medir_modelos.py): revisar las tarifas y ejecutar
  `python docs/medir_modelos.py` desde la raíz. Realiza 12 peticiones reales,
  consume cuota y reemplaza el JSON; no modifica `.env` ni muestra claves.

Fuente de tarifas: [Google AI for Developers — Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing),
secciones Gemini 3.5 Flash-Lite y Gemini 3.6 Flash, Standard, consulta 2026-10-23.
