# Decisión de arquitectura: elección de modelo

**Fecha del registro y las mediciones:** 2026-10-23 (America/Santiago).
**Responsable del proyecto:** Jefferson Santos.
**Estado:** elección operativa vigente; comparación de calidad del candidato alternativo pendiente por falta de respuesta.

## Modelo elegido

Se mantiene **Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`)**, ya utilizado en
los bloques 4 y 7. Este registro documenta esa elección con mediciones nuevas;
no cambia el modelo predeterminado del código.

El caso evaluado es el prototipo actual: una CLI Python que recibe una pregunta
y devuelve texto en español mediante una petición a Gemini. Para concretar la
evaluación se usan consultas básicas de aprendizaje técnico (venv, protección
de una API key y HTTP 429), acordes con el módulo implementado. No se presupone
una aplicación de producción ni un asistente especializado ya construido.

## Diagrama de arquitectura

![Arquitectura del prototipo](diagrama_arquitectura.png)

El [detalle del flujo](arquitectura.md) identifica `armar_peticion`,
`enviar_peticion`, `extraer_texto`, el orquestador, la credencial local,
los errores y los datos de cada conexión. Incluye también el cálculo documental
del costo a partir de `usageMetadata`, separado de la CLI que imprime texto.
El diagrama se incorpora en esta entrega porque aún no existía en el repositorio.

## Comparación de candidatos

Tarifas **Standard de pago**, en USD para texto sin caché, herramientas ni
procesamiento por lotes, consultadas el 2026-10-23 en la
[página oficial de precios de Gemini](https://ai.google.dev/gemini-api/docs/pricing).
La salida incluye tokens de razonamiento. Son tarifas públicas; no confirman
el nivel de facturación ni un cargo real a esta cuenta.

| Criterio | Gemini 3.5 Flash-Lite | Gemini 3.8 Flash |
|---|---|---|
| ID solicitado | `gemini-3.5-flash-lite` | `gemini-3.8-flash` |
| Costo por 1.000 tokens de entrada | 0,00030 USD | 0,00075 USD |
| Costo por 1.000 tokens de salida | 0,00250 USD | 0,00375 USD |
| Latencia promedio observada, P1 | 1,849 s; 4 respuestas correctas | Sin respuestas válidas; espera media de 90,084 s hasta Timeout en 4 intentos |
| Calidad para las tres preguntas del prototipo | Buena para el alcance introductorio: cubre los conceptos esenciales en P1, P2 y P3; todas las respuestas tienen hasta 80 palabras por separación en espacios | No evaluable: el proveedor no devolvió texto en las tres preguntas |
| Disponibilidad en la serie completa | 6/6 respuestas útiles | 0/6 respuestas útiles |

Precios originales por millón: 0,30/2,50 USD (entrada/salida) para Flash-Lite y
0,75/3,75 USD para Flash. Se dividieron por 1.000 para la tabla.
El precio de Flash es promocional hasta el 31 de diciembre de 2026; la página
anuncia 1,50/7,50 USD por millón desde el 1 de enero de 2027.
Las tarifas de Flash-Lite corresponden a la consulta indicada y deben revisarse.

**Método:** cuatro repeticiones de la misma P1 por modelo, alternando candidatos,
cronometrajes con `time.perf_counter()` alrededor de `enviar_peticion`, y P2/P3
una vez por modelo. Se usa el módulo existente, la misma conexión, los mismos
prompts y la configuración predeterminada de cada modelo. El timeout de lectura
es 90 segundos. La medición es hasta la respuesta JSON completa, no al primer
token. No se excluyen repeticiones ni se activan reintentos automáticos.

**Evaluación:** pertinencia, corrección técnica de los conceptos y utilidad de
los pasos para una consulta introductoria. También se comprueba brevedad
(la pregunta pide un máximo de 80 palabras). La revisión es cualitativa y la
muestra es pequeña; no demuestra superioridad general de ningún modelo.
Los prompts, las respuestas y el resultado de cada intento están en el
[informe de mediciones](comparacion-modelos.md) y en el
[registro JSON original](mediciones_bloque9.json).

**Límite importante:** los tiempos de espera de Flash no son latencias de
respuestas exitosas ni permiten juzgar su calidad intrínseca. Falta repetir la
evaluación con dos candidatos que respondan para cerrar esa parte de la tabla
solicitada en el curso. No se sustituyen esos datos por valores ilustrativos.

## Justificación

El criterio principal es que el prototipo devuelva una explicación técnicamente
útil sin hacer esperar al usuario hasta agotar el timeout. En esta sesión,
Flash-Lite respondió las preguntas del caso y permitió medir su latencia;
Flash no produjo una respuesta utilizable. Por ello se mantiene el modelo que
ya funciona en la aplicación, dejando explícito el límite de esta evidencia.

El costo refuerza la elección: las tarifas de Flash son 2,5 veces la entrada
y 1,5 veces la salida de Flash-Lite. Esto compara precios por token, no costos
reales por petición de Flash, porque no se recibieron sus contadores de uso.
Para un prototipo de consultas breves no hay, con estas pruebas, una mejora
observada que justifique migrar al candidato alternativo.

Como escenario de escala (hipotético, no medición), 1.000 tokens de entrada y
200 de salida/razonamiento cuestan 0,00080 USD con Flash-Lite y 0,00150 USD
con Flash a las tarifas consultadas. 50.000 peticiones equivalentes serían
40 USD y 75 USD, respectivamente, sin impuestos ni servicios adicionales.

## Alternativa descartada y por qué

Se descarta **Gemini 3.8 Flash (`gemini-3.8-flash`) para esta versión del
prototipo** por no devolver texto dentro del timeout en la serie registrada y
por su mayor tarifa. No se afirma que produzca peores respuestas: no hubo
respuestas con las que evaluar ese punto.

La decisión se revisará si Flash-Lite deja de estar disponible, si cambian las
tarifas o si el caso requiere razonamiento más complejo. En ese momento se
repetirán los mismos prompts y se compararán respuestas válidas antes de
modificar `GEMINI_MODEL`. La aplicación sigue dependiendo de internet, de la
cuota y de la disponibilidad del proveedor; el control de errores no las elimina.

## Evidencia y reproducción

- [Arquitectura y fórmula de costo](arquitectura.md).
- [Resultados legibles y evaluación](comparacion-modelos.md).
- [Cada ejecución con su fecha, texto, tokens y tiempo](mediciones_bloque9.json).
- [Herramienta para repetir la medición](medir_modelos.py): revisar tarifas antes
  de ejecutar `python docs/medir_modelos.py`; realiza 12 llamadas reales y
  reemplaza el registro JSON. No modifica `.env` ni imprime credenciales.

Fuente de precios: [Google AI for Developers — Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing),
secciones Gemini 3.5 Flash-Lite y Gemini 3.8 Flash, Standard. La evidencia
histórica del Bloque 4 queda separada de estas mediciones nuevas.
