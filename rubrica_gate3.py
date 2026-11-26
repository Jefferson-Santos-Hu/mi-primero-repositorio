"""Rúbrica del programa; pesos y umbral no se ajustan para cambiar el resultado."""
UMBRAL=60
CRITERIOS=[
{'id':'C1','nombre':'Problema, requerimientos y arquitectura','peso':10,'fuentes':['ficha','decisiones']},
{'id':'C2','nombre':'Funcionamiento end-to-end','peso':25,'fuentes':['frio','demo','stack','ejecucion']},
{'id':'C3','nombre':'Integración IA, orquestación y RAG','peso':15,'fuentes':['mitigaciones','ia']},
{'id':'C4','nombre':'Backend FastAPI y Docker','peso':15,'fuentes':['servicio','api_md','dockerfile','compose']},
{'id':'C5','nombre':'QA, pruebas y evaluación de calidad','peso':10,'fuentes':['pytest','matriz','parciales']},
{'id':'C6','nombre':'Seguridad, riesgos y trazabilidad','peso':10,'fuentes':['riesgos','secretos','registro']},
{'id':'C7','nombre':'Documentación técnica','peso':5,'fuentes':['readme','transferencia']},
{'id':'C8','nombre':'Demo y defensa técnica','peso':10,'fuentes':['guion','demo','respaldo']}]
NO_COMPENSABLES=[{'id':'NC-1','nombre':'Ejecución E2E en contenedores','fuentes':['stack','ejecucion','registro']},{'id':'NC-2','nombre':'Endpoints funcionales y validados','fuentes':['servicio']},{'id':'NC-3','nombre':'Defensa en vivo del alumno','fuentes':[],'evaluador':'El alumno debe ejecutar y defender el proyecto delante del evaluador.'},{'id':'NC-4','nombre':'Sin credenciales ni datos personales reales en repositorio/corpus','fuentes':['secretos'],'evaluador':'Confirmar que el corpus es sintético.'}]
ENTREGABLES={'Código y contenedor':['api.py','interfaz/index.html','Dockerfile','compose.yaml'],'README técnico':['README.md'],'Matrices':['docs/matriz_pruebas.md','docs/matriz_riesgos.md'],'Demo':['ensayo_demo.py','docs/demo_respaldo.md'],'Presentación':['docs/defensa.md','docs/defensa_gate3.pptx']}
