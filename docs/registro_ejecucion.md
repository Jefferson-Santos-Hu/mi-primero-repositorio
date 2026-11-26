# Registro de ejecución

<!-- AUTO:INICIO -->
- fecha: 2026-11-26T15:14:53.929732+00:00
- commit: 60988c06aff4dd2f20f736836499764b9b01c5aa
- huella_codigo: 1ee24bc3f5574c3528f51b856dbf809bef61038245da75d901dc9fccfdc2f77b
- modo: simulado
- escenarios_huella: 9694761bb420769342eff3eaa796620a0f353016e7f6acdf3111eb362895b4ce
- casos: 15
- cumplidos: 15
<!-- AUTO:FIN -->

## Qué se observó
Las peticiones atravesaron Nginx y FastAPI en contenedores sanos. El modo simulado permite repetir entradas, errores y fuentes sin depender de una red externa. El modo se declara expresamente y no se confunde con una respuesta real de Gemini.

## Qué no se probó
Esta corrida de catorce escenarios usa el modelo simulado, sin medir calidad ni costo del proveedor. La evidencia real de Gemini se guarda separadamente. No prueba carga, autenticación multiusuario ni revisión independiente de un compañero.

## Siguiente paso
Ejecutar la defensa en voz alta con el alumno y confirmar por el revisor las observaciones de transferencia todavía pendientes.
