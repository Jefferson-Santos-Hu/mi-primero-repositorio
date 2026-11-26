from ficha_datos import validar_ficha
if __name__=='__main__':
    errores=validar_ficha(completa=False)
    for e in errores:print('ERROR:',e)
    print('Ficha secciones 1 a 3:', 'verificada' if not errores else 'incompleta')
    raise SystemExit(bool(errores))
