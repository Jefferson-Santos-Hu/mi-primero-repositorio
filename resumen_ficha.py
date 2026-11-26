from ficha_datos import leer_ficha,validar_ficha
if __name__=='__main__':
    d=leer_ficha();print('Requerimientos:',len(d['requerimientos']),'Criterios:',len(d['criterios']),'Hitos:',len(d['hitos']),'Horas:',sum(float(h) for _,h,_ in d['hitos']))
    print('Problemas:',validar_ficha())
