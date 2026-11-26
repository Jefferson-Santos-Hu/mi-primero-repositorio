FROM python:3.14.8-slim@sha256:fbecd461fc72d21b2143c6eaba25143738079154a6d0ea3da3aec724f50eed4a
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 LANGSMITH_TRACING=false LANGCHAIN_TRACING_V2=false ANONYMIZED_TELEMETRY=false
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY fundamentacion.py api.py modelo_simulado.py servicio_rag.py cliente.py indexar_documentos.py agente_con_herramientas.py modelo_langchain.py ./
COPY src/ ./src/
COPY prompts/ ./prompts/
COPY corpus/ ./corpus/
RUN useradd --create-home appuser && mkdir vectorstore && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/salud',timeout=2)"
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
