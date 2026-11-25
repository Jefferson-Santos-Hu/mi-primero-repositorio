"""Gobernanza local: revisión explícita; no sustituye autenticación de un revisor."""
import hashlib
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt


def huella_prompt(texto):
    return hashlib.sha256(texto.encode()).hexdigest()


def puntaje_riesgo(probabilidad,impacto):
    if any(isinstance(v,bool) or not isinstance(v,int) or not 1<=v<=5 for v in (probabilidad,impacto)):
        raise ValueError('Probabilidad e impacto deben ser enteros de 1 a 5')
    return probabilidad*impacto


def categoria_riesgo(puntaje):
    return 'CRITICO' if puntaje>=15 else 'ALTO' if puntaje>=9 else 'MEDIO' if puntaje>=4 else 'BAJO'


class Estado(TypedDict,total=False):
    huella_nueva:str
    aprobado:bool
    activa:str


def crear_supervision():
    def revisar(estado):
        decision=interrupt({'motivo':'Revisión humana previa a activar una versión del prompt','huella_propuesta':estado['huella_nueva']})
        return {'aprobado':decision is True}
    def aplicar(estado):
        return {'activa':estado['huella_nueva']} if estado['aprobado'] else {}
    grafo=StateGraph(Estado)
    grafo.add_node('revisar',revisar);grafo.add_node('aplicar',aplicar)
    grafo.add_edge(START,'revisar');grafo.add_edge('revisar','aplicar');grafo.add_edge('aplicar',END)
    return grafo.compile(checkpointer=InMemorySaver())
