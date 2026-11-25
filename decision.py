"""Decisión reproducible sobre la estrategia de personalización del proyecto."""
import json,re
from pathlib import Path
from dataset_tuning import EJEMPLOS_RAW


def recomendar_estrategia(r):
    puntos={'RAG':0,'Fine-tuning completo':0,'PEFT':0}
    if r['informacion_cambia_seguido']:puntos['RAG']+=3
    if r['problema_de_formato_o_tono']:puntos['PEFT']+=2;puntos['Fine-tuning completo']+=1
    if r['dataset_grande_y_de_calidad']:puntos['Fine-tuning completo']+=2;puntos['PEFT']+=1
    if r['presupuesto_limitado_o_iterar_rapido']:puntos['RAG']+=2;puntos['PEFT']+=1
    if r['necesita_multiples_variantes']:puntos['PEFT']+=2
    mayor=max(puntos.values())
    return puntos,[t for t,p in puntos.items() if p==mayor]


if __name__=='__main__':
    muestra=json.loads(Path('resultados_metricas.json').read_text(encoding='utf8'))
    revision=[{'id':e['id'],'incumple_formato':bool(re.search(r'[`#*]|\n',e['respuesta'])) or len(e['respuesta'].split())>60} for e in muestra]
    fallos=sum(r['incumple_formato'] for r in revision)
    respuestas={'informacion_cambia_seguido':False,'problema_de_formato_o_tono':fallos>=3,'dataset_grande_y_de_calidad':len(EJEMPLOS_RAW)>=200,'presupuesto_limitado_o_iterar_rapido':True,'necesita_multiples_variantes':False}
    puntos,ganadoras=recomendar_estrategia(respuestas)
    Path('docs/decision_evidencia.json').write_text(json.dumps({'revision_formato':revision,'criterio':'Sin Markdown/saltos de línea y hasta 60 palabras. No evalúa factualidad ni tono semántico.','incumplimientos':fallos,'respuestas':respuestas,'puntos':puntos,'ganadoras':ganadoras},ensure_ascii=False,indent=2),encoding='utf8')
    texto=f'''# Decisión de personalización

## 1. El problema
El asistente necesita responder sobre decisiones específicas del repositorio y mostrar su fuente. Los modelos generales no poseen ese corpus privado de ejecución. En una revisión estructural reproducible de 20 respuestas existentes hubo {fallos} incumplimientos del formato breve sin Markdown (criterio y casos en docs/decision_evidencia.json). Eso no acredita corrección factual: la revisión cualitativa de 10 casos está separada en revision_manual.json.

## 2. Resultado del método de decisión
{json.dumps(puntos,ensure_ascii=False)}. Candidata: {', '.join(ganadoras)}.

Información que cambia seguido=False: no existe una serie histórica de tres meses que demuestre cambios mensuales, por lo que no se afirma ese dato. Formato/tono={respuestas['problema_de_formato_o_tono']}, usando el umbral de 3/20 del curso con un control estructural limitado. Dataset grande=False: hay 12 ejemplos, no 200. Iterar rápido=True: el MVP fija evaluar un cambio de corpus en menos de un día y no incluye entrenamiento pagado. Múltiples variantes=False: un único asistente en español.

## 3. Técnica elegida y por qué
Elijo RAG con prompt versionado. El contenido del repositorio debe poder citarse y actualizarse sin entrenar. No hay empate en esta aplicación del método. El costo inicial es preparar seis documentos sintéticos y un índice persistente; cada consulta añade embeddings y contexto. PEFT sería un experimento posterior para comportamiento si se demuestra incumplimiento persistente con una muestra adecuada. El fine-tuning completo no se justifica con 12 ejemplos ni con esta necesidad de conocimiento trazable. El laboratorio valida el dataset sin enviar ningún trabajo de tuning.

## 4. Qué necesitarías para ejecutarla
Ya existen 6 documentos, 6 chunks y 11 preguntas de recuperación etiquetadas antes de consultar. No falta ningún documento para el alcance actual del MVP; falta validar generalización con al menos 20 preguntas nuevas independientes antes de ampliar el uso. Para alcanzar el piso orientativo de 200 ejemplos de tuning faltarían 188 respecto de los 12 actuales, más una partición de validación independiente. Esos datos no son necesarios para ejecutar RAG. No se asume habilitación ni presupuesto de entrenamiento en la cuenta.
'''
    Path('decision_personalizacion.md').write_text(texto,encoding='utf8')
    print(puntos,fallos)
