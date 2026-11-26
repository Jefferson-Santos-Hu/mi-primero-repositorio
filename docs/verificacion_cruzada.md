# Verificación cruzada de composición

Estado: PENDIENTE DE CONFIRMACIÓN DEL COMPAÑERO. Revisor previsto: Javier Omar Muñoz Muñoz.

| Criterio | Verificación técnica del asistente | Revisión por Javier |
|---|---|---|
| VC-1 Instalar desde README | Procedimiento preparado; ensayo en frío automatizado | Pendiente |
| VC-2 Arrancar servicios | Dos contenedores healthy comprobados | Pendiente |
| VC-3 Configurar sin exponer claves | .env ignorado; imagen inspeccionada sin .env | Pendiente |
| VC-4 Realizar consulta | 15 escenarios sintéticos por el proxy; modo declarado | Pendiente |
| VC-5 Interpretar respuesta y fuentes | Prueba de navegador con cliente.md y rechazo de ataque | Pendiente |
| VC-6 Detener y conservar datos | Compose down sin borrar volumen; comprobación automatizada | Pendiente |

Observaciones propuestas: explicitar que /salud no verifica cuota del proveedor; distinguir demo simulada de evidencia real; no exponer el laboratorio sin autenticación. Decisión aplicada: banner de modo, explicación de salud y enlace a limitaciones en README. Son propuestas para contrastar, no declaraciones atribuidas a Javier.
