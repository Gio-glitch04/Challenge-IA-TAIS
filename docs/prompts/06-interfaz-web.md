# Especificación técnica — Feature 6: Interfaz web

**Rama:** `feature/interfaz-web`

## Qué se pidió (resumen)

Una interfaz para que cualquier persona pueda navegar la aplicación y hacer las pruebas por
su cuenta desde el navegador, sin escribir comandos.

## Requisitos de entrada

- Las operaciones existentes de la API: inventario, disponibilidad, crear, listar y
  cancelar (features 1 a 5).
- Consigna: la interfaz gráfica no es obligatoria y un frente gráfico complejo está fuera de
  alcance. Por eso la página es mínima y complementa la API, no la reemplaza.

## Decisiones y por qué

| Tema | Decisión | Motivo | Alternativa descartada |
| :--- | :--- | :--- | :--- |
| Tecnología | Un HTML con CSS y JS sin librerías, servido en `/` (ADR-021) | Sin dependencias, sin build, sin CORS, funciona sin internet | React/Vue o plantillas Jinja |
| Reglas | Ninguna en la página: todo lo valida la API (ADR-022) | Una sola versión de cada regla | Validar también en el navegador |
| Fechas | `datetime-local` enviado tal cual (`AAAA-MM-DDTHH:MM`) | La API ya acepta ese formato (ADR-005) | Convertir a otro formato en JS |
| Errores | Se muestran el código y el mensaje de la API | Lo que ve la persona es lo mismo que recibe un cliente de la API | Mensajes propios de la página |
| Seguridad | Los datos se insertan con `textContent` | Un solicitante con HTML no se ejecuta | `innerHTML` |

## Criterios de aceptación (pruebas)

1. `GET /` devuelve 200 con `text/html` y el título de la app.
2. La página tiene los formularios de disponibilidad y reserva y la tabla de reservas.
3. La página usa los endpoints `/unidades`, `/disponibilidad`, `/reservas` y `/cancelar`.
4. `/` no aparece en el esquema OpenAPI de la API.

## Episodios

- [Episodio 06](../evidence/episodio-06-interfaz-web.md)
