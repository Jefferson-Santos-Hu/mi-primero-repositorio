"""Ejecuta regresiones de mitigación y registra límites conocidos por separado."""
import subprocess,sys
from ataques import ejecutar_ataques
from alucinaciones import ejecutar_sondas


def verificar():
    ataques=ejecutar_ataques();sondas=ejecutar_sondas()
    normales=all(a['detectado']==a['detectable'] for a in ataques if not a.get('limite'))
    sondas_ok=all(s['rechazada']==s['debe_rechazar'] for s in sondas if not s.get('limite'))
    limites=any(a.get('limite') and a['detectado']!=a['detectable'] for a in ataques) and any(s.get('limite') and s['rechazada']!=s['debe_rechazar'] for s in sondas)
    r=subprocess.run([sys.executable,'-m','pytest','tests/parciales/test_fundamentacion.py','test_servicio_rag.py','test_api.py','-q'],capture_output=True,text=True)
    print('Mitigaciones:',normales,sondas_ok,'límites observados:',limites,'regresiones:',r.returncode==0)
    return normales and sondas_ok and limites and r.returncode==0


if __name__=='__main__':raise SystemExit(not verificar())
