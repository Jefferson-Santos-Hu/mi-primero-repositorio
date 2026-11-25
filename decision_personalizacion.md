# Decisión de personalización

## 1. El problema
El asistente necesita responder sobre decisiones específicas del repositorio y mostrar su fuente. Los modelos generales no poseen ese corpus privado de ejecución. En una revisión estructural reproducible de 20 respuestas existentes hubo 0 incumplimientos del formato breve sin Markdown (criterio y casos en docs/decision_evidencia.json). Eso no acredita corrección factual: la revisión cualitativa de 10 casos está separada en revision_manual.json.

## 2. Resultado del método de decisión
{"RAG": 2, "Fine-tuning completo": 0, "PEFT": 1}. Candidata: RAG.

Información que cambia seguido=False: no existe una serie histórica de tres meses que demuestre cambios mensuales, por lo que no se afirma ese dato. Formato/tono=False, usando el umbral de 3/20 del curso con un control estructural limitado. Dataset grande=False: hay 12 ejemplos, no 200. Iterar rápido=True: el MVP fija evaluar un cambio de corpus en menos de un día y no incluye entrenamiento pagado. Múltiples variantes=False: un único asistente en español.

## 3. Técnica elegida y por qué
Elijo RAG con prompt versionado. El contenido del repositorio debe poder citarse y actualizarse sin entrenar. No hay empate en esta aplicación del método. El costo inicial es preparar seis documentos sintéticos y un índice persistente; cada consulta añade embeddings y contexto. PEFT sería un experimento posterior para comportamiento si se demuestra incumplimiento persistente con una muestra adecuada. El fine-tuning completo no se justifica con 12 ejemplos ni con esta necesidad de conocimiento trazable. El laboratorio valida el dataset sin enviar ningún trabajo de tuning.

## 4. Qué necesitarías para ejecutarla
Ya existen 6 documentos, 6 chunks y 11 preguntas de recuperación etiquetadas antes de consultar. No falta ningún documento para el alcance actual del MVP; falta validar generalización con al menos 20 preguntas nuevas independientes antes de ampliar el uso. Para alcanzar el piso orientativo de 200 ejemplos de tuning faltarían 188 respecto de los 12 actuales, más una partición de validación independiente. Esos datos no son necesarios para ejecutar RAG. No se asume habilitación ni presupuesto de entrenamiento en la cuenta.
