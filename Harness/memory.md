> **Nota:** esta plantilla inicial fue reemplazada por el sistema de memoria descrito en
> [`AGENTS.md`](../AGENTS.md) (`.memoria/` y `docs/`). Se conserva como antecedente.

# Memoria del Agente y Registro de Decisiones

Este archivo sirve para mantener el estado del proyecto, registrar supuestos y documentar los episodios de delegación requeridos por la consigna para el README final. 

**Instrucción para el LLM (Claude):** Actualiza este archivo cada vez que completes un hito, tomes una decisión técnica importante o interactúes con el usuario para validar un cambio.

## 1. Estado del Proyecto
- [ ] Inicialización del proyecto (Git, entorno virtual, requirements.txt).
- [ ] Configuración de la base de datos SQLite y carga del inventario.
- [ ] Modelos de datos (Pydantic / SQLAlchemy o SQLite puro).
- [ ] Endpoints de la API (Disponibilidad, Reserva, Cancelación).
- [ ] Implementación de lógica de negocio (validación de fechas y superposiciones).
- [ ] Pruebas automáticas (`pytest`).
- [ ] Redacción del `README.md` final (Especificación, Solución, Prep del Agente, Registro).

## 2. Supuestos y Decisiones Técnicas
*   **Zona Horaria:** Se asumirá UTC o uso de fechas locales sin validación estricta de timezone, documentándolo en el README.
*   *(Claude: documenta aquí otros supuestos como límites de anticipación, cómo manejar reservas en el pasado, etc.)*

## 3. Registro de Episodios de Delegación (Requisito de Evaluación)
*Nota: Debemos registrar 3 episodios reales a lo largo del desarrollo. Rellenar a medida que ocurran.*

### Episodio 1: [Título breve, ej. Lógica de superposición]
*   **Objetivo/Requisito:** 
*   **Contexto/Instrucción suministrada:** *(Extracto del prompt)*
*   **Acción/Resultado del agente:** *(Qué código generó o qué decisión tomó)*
*   **Decisión humana:** *(Aceptar/Corregir/Rechazar y Motivo)*
*   **Enlace/Evidencia:** *(Archivo modificado, nombre del commit o nombre del test verificable)*

### Episodio 2: [Título breve, ej. Persistencia y carga inicial]
*   **Objetivo/Requisito:** 
*   **Contexto/Instrucción suministrada:** 
*   **Acción/Resultado del agente:** 
*   **Decisión humana:** 
*   **Enlace/Evidencia:** 

### Episodio 3: [Título breve, ej. Casos de prueba borde]
*   **Objetivo/Requisito:** 
*   **Contexto/Instrucción suministrada:** 
*   **Acción/Resultado del agente:** 
*   **Decisión humana:** 
*   **Enlace/Evidencia:** 