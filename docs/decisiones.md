# Decisiones de arquitectura

## D-01 — Separar interfaz y API
Estado: aceptada para el MVP.
Contexto: la vista debe poder cambiar sin modificar el cliente Gemini.
Decisión: HTML/JS servido por Nginx con proxy /api hacia FastAPI, en dos servicios Compose.
Alternativas: una sola aplicación de escritorio simplifica despliegue pero limita acceso por navegador; un frontend con framework agrega dependencias sin necesidad funcional.
Costo: dos imágenes y comprobaciones de salud; se conserva una interfaz sin compilación. Evidencia: compose.yaml, interfaz/nginx.conf y api.py.

## D-02 — Modo real y simulado explícitos
Estado: aceptada para demostración.
Contexto: la demo debe caber en dos minutos sin depender de cuota o latencia de Gemini.
Decisión: MODELO=real o MODELO=simulado, visible en salud y banner; un error real devuelve 503, nunca cambia silenciosamente de modelo.
Alternativas: un fallback silencioso facilitaría continuidad pero falsearía la evidencia; solo modo real haría frágil el ensayo.
Costo: mantener casos del doble y dos recorridos. Evidencia: modelo_simulado.py, api.py y test_api.py. Límite LIM-03.

## D-03 — Persistir Chroma con actualización explícita
Estado: aceptada para el corpus pequeño.
Contexto: reconstruir embeddings en cada arranque consume tiempo y cuota.
Decisión: volumen persistente, IDs estables y manifiesto; actualizar solo cambios con el servicio detenido.
Alternativas: embeddings en memoria desaparecen al reiniciar; un vector store remoto agrega operación y credenciales que este MVP no requiere.
Costo: mantener versiones de corpus y respaldo del volumen; no se garantiza actualización concurrente. Evidencia: indexar_documentos.py y test_indice_incremental.py.

## D-04 — Validar salida sin prometer veracidad semántica
Estado: aceptada con riesgo residual alto.
Contexto: una respuesta puede incluir [1] y aun inventar cifras o contradicciones.
Decisión: comprobar índice de cita, cifras en los chunks y una regla de autenticación; pedir revisión humana para aplicar recomendaciones.
Alternativas: confiar en el prompt no permite rechazar cifras inventadas; un juez semántico externo agrega costo y también requiere evaluación independiente.
Costo: falsos positivos ante paráfrasis y falsos negativos semánticos; H-04 lo declara. Evidencia: fundamentacion.py y tests/parciales/test_fundamentacion.py. Límites LIM-01 y LIM-02.

## D-05 — Secretos en ejecución y servicio local
Estado: aceptada para laboratorio.
Contexto: el repositorio público y las imágenes no deben incluir la clave.
Decisión: .env ignorado e inyectado por Compose; puertos publicados solo en 127.0.0.1, usuario de contenedor sin root y bases fijadas por digest.
Alternativas: incrustar credenciales en Dockerfile las expondría en capas; publicar en todas las interfaces exigiría autenticación y revisión de acceso adicionales.
Costo: configurar cada instalación; la API no incorpora autenticación multiusuario y no está autorizada para exposición pública. Evidencia: Dockerfile, compose.yaml y buscar_secretos.py.

## D-06 — Supervisión didáctica con LangGraph
Estado: aceptada para el ejercicio; insuficiente para producción.
Contexto: el Gate 2 exige un punto de pausa real antes de activar una huella propuesta.
Decisión: interrupt/Command y checkpoint en memoria con decisiones de ensayo expresamente simuladas.
Alternativas: aprobar automáticamente quitaría supervisión; persistencia e identidad del revisor son necesarias para producción pero exceden este ejercicio.
Costo: tras reinicio se debe volver a revisar; no se usa como autorización de despliegue real. Evidencia: gobernanza.py y test_gobernanza.py. Límite LIM-04.
