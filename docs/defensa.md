# Guion de defensa técnica

## Problema (1 min)
El proyecto ayuda a estudiantes que trabajan con Python y Gemini a consultar las decisiones de su propio repositorio. Una respuesta general del modelo no demuestra cómo está configurado este proyecto, ni de dónde salió una recomendación. Por eso el objetivo no es conversar sobre cualquier tema: es responder sobre un corpus pequeño, mostrar fuentes y admitir límites. La carga de diez consultas semanales de cinco minutos es una hipótesis de planificación, no una medición de usuarios. El alcance excluye entrenar modelos y ejecutar acciones económicas. La ficha vincula los requisitos RF-01 a RF-06 con criterios verificables. Hoy mostraré la aplicación, sus comprobaciones y lo que todavía necesita revisión humana.

## Arquitectura (2 min)
La decisión D-01 separa una interfaz HTML y JavaScript, servida por Nginx, de una API FastAPI. La interfaz envía consultas al proxy y presenta texto y fuentes sin insertar HTML generado. Los dos servicios se ejecutan en Docker y publican únicamente puertos locales. D-05 mantiene la clave en ejecución, fuera de Git y de las imágenes, y utiliza un usuario sin privilegios.

El servicio RAG crea un vector de la consulta, busca en Chroma y construye contexto numerado. La decisión D-03 conserva ese índice en un volumen. Los identificadores y la huella permiten reabrirlo sin generar embeddings otra vez y actualizar solo lo que cambia con el servicio detenido. Luego el cliente de Gemini genera una respuesta y el servicio comprueba las citas y cifras. Cada etapa deja un evento con el mismo trace_id, pero sin la pregunta ni el documento completos.

La evidencia incluye 15 escenarios sintéticos de extremo a extremo, 5 defectos controlados que las pruebas detectaron y 9 riesgos con evidencia ejecutable. Los números no acreditan calidad universal: dicen exactamente qué se probó. El Gate 2 conserva por separado la ejecución real de Gemini. En la demo siguiente usaré el modo simulado de D-02, anunciado en la pantalla, para que la red no cambie el resultado del ensayo.

## Demo (2 min)
Antes de comenzar anuncio que las respuestas del recorrido principal son simuladas. La última prueba abre una instancia real sin credencial para mostrar el fallo honesto. El ensayo cronometra peticiones y añade ocho segundos de teclado por paso. Si falla en vivo, mostraré el respaldo de la última ejecución e indicaré que es un registro anterior.

- PASO-1 Servicio vivo
- PASO-2 Respuesta con fuente
- PASO-3 Catálogo HTTP local
- PASO-4 Error uniforme
- PASO-5 Ataque rechazado
- PASO-6 Límite declarado
- PASO-7 Falla honesta sin clave

## Riesgos (2 min)
El riesgo R-01 conserva residual alto. El filtro bloquea instrucciones conocidas, pero A-07 demuestra que una paráfrasis puede escapar. Esa es LIM-02: no prometemos detener toda inyección. Se mantiene el contexto separado de las instrucciones, se controla el corpus y se revisa antes de indexar nuevo material.

R-06 también conserva residual alto. La decisión D-04 comprueba si una cita existe y si las cifras aparecen en los fragmentos citados. Una frase falsa sin cifra nueva puede superar esa comprobación. La sonda H-04 registra ese límite, LIM-01. No ejecutaríamos automáticamente una recomendación producida por el asistente: el usuario debe contrastar la fuente.

R-09 explica LIM-04. El grafo de supervisión pausa y reanuda realmente, pero usa memoria y no autentica al revisor. Las decisiones de aprobación de las pruebas son simuladas. Ese mecanismo cumple la demostración didáctica y no constituye autorización de producción. Harían falta identidad, permisos y almacenamiento durable para tal uso.

Finalmente, LIM-03 recuerda que la simulación no mide calidad, cuota ni costo del proveedor. Un fallo real devuelve 503 y no activa un respaldo silencioso. Mantener estas distinciones permite evaluar las mitigaciones sin atribuirles más alcance del que las pruebas sostienen.

## Cierre (1 min)
El resultado es un MVP local con interfaz, API, recuperación y fuentes, empaquetado y acompañado de comandos reproducibles. La documentación explica instalación, decisiones y límites; las matrices enlazan cada comprobación con un requisito o un riesgo. Los verificadores detectan un registro viejo cuando cambia el código o los escenarios. La presentación y el respaldo ayudan a repetir la demostración, pero no sustituyen que una persona la ejecute y explique.

La siguiente validación es la revisión efectiva del compañero y la defensa en voz alta del alumno. Las observaciones propuestas para Javier no se registran como si él ya las hubiera hecho. La calificación final corresponde al instructor. El valor del proyecto es que cada afirmación puede contrastarse con código, una prueba o una limitación declarada.

## Diapositivas

| Número | Sección | Contenido |
|---|---|---|
| 1 | Problema | Asistente técnico y alcance |
| 2 | Arquitectura | Dos servicios y RAG |
| 3 | Arquitectura | Evidencia y métricas |
| 4 | Demo | Siete pasos en vivo |
| 5 | Riesgos | Residuales altos y límites |
| 6 | Cierre | Entrega y validación humana |
