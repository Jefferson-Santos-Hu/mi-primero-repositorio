"""Contrato compartido por pruebas internas y cliente HTTP externo."""
CASOS=[
 {'id':'V-01','descripcion':'salud','metodo':'GET','ruta':'/salud','estado':200,'contiene':'ok'},
 {'id':'V-02','descripcion':'catálogo HTTP','metodo':'GET','ruta':'/errores/429','estado':200,'contiene':'cuota'},
 {'id':'V-03','descripcion':'respuesta citada','metodo':'POST','ruta':'/consultas','json':{'pregunta':'¿Qué hace el cliente ante HTTP 429?'},'estado':200,'contiene':'cliente.md'},
 {'id':'I-01','descripcion':'campo ausente','metodo':'POST','ruta':'/consultas','json':{},'estado':422,'contiene':'entrada_invalida'},
 {'id':'I-02','descripcion':'pregunta vacía','metodo':'POST','ruta':'/consultas','json':{'pregunta':''},'estado':422,'contiene':'entrada_invalida'},
 {'id':'I-03','descripcion':'tipo numérico','metodo':'POST','ruta':'/consultas','json':{'pregunta':123},'estado':422,'contiene':'entrada_invalida'},
 {'id':'I-04','descripcion':'ruta inexistente','metodo':'GET','ruta':'/inexistente','estado':404,'contiene':'no_encontrado'},
 {'id':'I-05','descripcion':'método incorrecto','metodo':'DELETE','ruta':'/salud','estado':405,'contiene':'error_http'},
 {'id':'I-06','descripcion':'JSON incompleto','metodo':'POST','ruta':'/consultas','contenido':'{"pregunta":','estado':422,'contiene':'entrada_invalida'},
 {'id':'I-07','descripcion':'k fuera de límites','metodo':'POST','ruta':'/consultas','json':{'pregunta':'consulta','k':7},'estado':422,'contiene':'entrada_invalida'},
 {'id':'I-08','descripcion':'exceso de longitud','metodo':'POST','ruta':'/consultas','json':{'pregunta':'x'*4001},'estado':422,'contiene':'entrada_invalida'}]


def ejecutar_caso(cliente,caso):
    opciones={'content':caso['contenido'],'headers':{'Content-Type':'application/json'}} if 'contenido' in caso else {'json':caso.get('json')}
    r=cliente.request(caso['metodo'],caso['ruta'],**opciones)
    return r.status_code==caso['estado'] and caso['contiene'] in r.text,r.status_code,r.text
