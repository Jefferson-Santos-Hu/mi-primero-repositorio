"""Doble didáctico explícito para ensayo offline; nunca reemplaza un fallo real."""
import uuid


class ServicioSimulado:
    def consultar(self,pregunta,k=3):
        texto=pregunta.casefold()
        if any(x in texto for x in ['429','reintento','backoff']):
            respuesta='Ante HTTP 429 el cliente usa backoff exponencial con jitter y tres intentos [1].';fuentes=['cliente.md']
        elif any(x in texto for x in ['venv','entorno','clave']):
            respuesta='Usa el intérprete del venv y conserva la clave exclusivamente en .env [1].';fuentes=['entorno.md']
        else:
            respuesta='No encuentro esa información en el corpus de demostración.';fuentes=[]
        trace='trace-'+uuid.uuid4().hex
        return {'estado':'ok' if fuentes else 'sin_contexto','modo':'simulado','respuesta':respuesta,'fuentes':fuentes,'trace_id':trace,'tokens':None,'costo_generacion_usd':None,'auditoria':[{'evento':'respuesta_simulada','trace_id':trace,'pregunta_len':len(pregunta)}]}
