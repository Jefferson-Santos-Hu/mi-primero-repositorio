# Verificación desde clon limpio — Gate 2

Fecha: 25 de noviembre de 2026.

Se clonó el repositorio público desde GitHub al commit bb41976a34bf6a14f2f3eed38af7a86dca0d9e15, en una carpeta nueva. Se creó un entorno virtual nuevo con Python 3.14.8 y se instalaron las versiones de requirements.txt. La credencial se configuró únicamente en el .env local ignorado: no formó parte del clon ni del commit.

Comandos ejecutados desde el clon:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
.\venv\Scripts\python.exe -m pytest -q
.\venv\Scripts\python.exe indexar_documentos.py
.\venv\Scripts\python.exe verificar_gate2.py
```

Resultados observados:

- Instalación terminada con código de salida 0.
- 98 pruebas y 60 subpruebas aprobadas; 21 advertencias de deprecación, sin fallos.
- Índice nuevo creado con embeddings reales: 6 chunks.
- Consulta real final con generación Gemini: fuente cliente.md.
- Reapertura sin reindexar, logs correlacionados sin texto crudo y supervisión con interrupt/Command: 4 de 4 criterios comprobados.
- Las decisiones de aprobación/rechazo de ese ensayo son simuladas, sin activar servicios externos.

Esta verificación es de instalación y ejecución por el asistente en una carpeta y entorno nuevos del mismo equipo. No se presenta como revisión por un compañero ni como prueba en otro sistema operativo. Se guardó además gate2_evidencia.json en el clon como resultado de esa ejecución.
