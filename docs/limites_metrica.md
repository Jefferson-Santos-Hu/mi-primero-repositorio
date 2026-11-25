# Límites de la métrica de evaluación

## Qué mide

El pipeline normaliza mayúsculas, puntuación y espacios y compara frecuencias
de palabras con `Counter`. La precisión divide las coincidencias por las
palabras de la respuesta; la cobertura las divide por las de la referencia.
F1 es su media armónica. No mide verdad, orden, utilidad ni equivalencia semántica.
Los textos vacíos producen ceros, no división por cero.

## Modos de falla conocidos

- Paráfrasis correctas puntúan bajo: el caso 5, diccionarios, tiene F1 de
  aproximadamente 0,154, aunque explica correctamente pares clave-valor y
  mutabilidad. El caso 2 explica correctamente venv con F1 cercano a 0,231.
- Una respuesta relativamente alta puede introducir una generalización:
  el caso 13 obtiene 0,480, pero limita `pip install` a descargar desde PyPI;
  también puede instalar desde archivos, otros índices y ubicaciones locales.
- Una respuesta corta puede omitir una condición decisiva: el caso 9 no
  distingue archivos ya rastreados de los ignorados. Su puntuación baja no
  revela por sí sola esa omisión; hay que leerla.
- El orden no se evalúa. Como control sintético, «perro muerde hombre» y
  «hombre muerde perro» tienen las mismas frecuencias y F1=1 con sentidos
  diferentes. Este control está escrito para explicar la métrica; no se
  presenta como una respuesta recibida del modelo.
- Las referencias son breves y no exhaustivas. El detalle correcto adicional
  reduce la precisión léxica: el caso 1 incluye tipado dinámico y legibilidad,
  aunque la referencia solo menciona que Python es interpretado.

## Muestra revisada

Se generaron 20 respuestas reales mediante `consultar_modelo`, guardadas junto
con referencias, fechas, métricas y el antes/después de normalizar en
[`resultados_metricas.json`](../resultados_metricas.json).
Se seleccionaron los cinco F1 más bajos (9, 5, 14, 17, 2) y los cinco más
altos (13, 8, 1, 4, 15). La revisión cualitativa asistida está en
[`revision_manual.json`](../revision_manual.json): cada caso incluye corrección
factual, completitud, contradicción y una nota. No se atribuye a un compañero
ni se presenta como una revisión humana independiente.

El F1 promedio observado es aproximadamente 0,362. No significa que solo el
36,2 % del contenido sea correcto. Los ejemplos revisados muestran que el
vocabulario adicional y las paráfrasis afectan mucho la cifra.

## Recomendación de uso

Usar los números para ordenar la revisión, comparar cambios sobre las mismas
referencias y detectar cambios de vocabulario, conservando los textos.
Revisar también puntajes altos: no aceptar automáticamente una instrucción
operativa, una afirmación de seguridad o un dato factual porque tenga F1 alto.
En este tutor técnico, comprobar especialmente las condiciones de Git,
instalación y credenciales antes de aplicar las instrucciones. Mantener
referencias revisadas y una evaluación semántica complementaria.
