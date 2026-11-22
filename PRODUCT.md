# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Dos audiencias con el mismo peso:

- **Operadores de seguridad o compliance** de una empresa que despliega agentes de IA. Configuran los secretos protegidos, los prompts y la política, y revisan las respuestas que el guardrail marcó o dejó en revisión humana.
- **Jurado de Platanus Hack 26** (track AI Security), que ve una demo de tres minutos en un proyector y necesita entender el mecanismo sin leer.

## Product Purpose

mosAIc es un guardrail que revisa la respuesta de un agente de IA antes de que llegue al destinatario. Detecta la divulgación acumulativa: una frase inocente que, sumada a lo que ese destinatario ya sabe, le permitiría deducir una conclusión protegida. Cuando detecta riesgo, entrega una reformulación que igual cumple la tarea o deja la respuesta en revisión humana.

El horizonte actual es la demo del hackathon. El éxito es que el jurado entienda, en una sola pasada, que la misma respuesta es segura para una persona y peligrosa para otra.

## Positioning

mosAIc no busca secretos en el texto. Mide, para cada destinatario, cuánto sube la probabilidad de que pueda deducir una conclusión protegida. Combina un grafo interno RDF/OWL, un grafo de evidencia sobre lo que cada destinatario pudo saber y ProbLog. La decisión depende de quién recibe la respuesta y de lo que esa persona recibió antes, no solo de la respuesta.

## Operating Context

- Panel local (FastAPI, `isde/api.py` + `isde/dashboard.py`) en http://127.0.0.1:8001/, con pestañas de simulación, configuración, notificaciones y elementos marcados. Usa Claude y consume API.
- Demo de catálogo sin Claude (`python -m isde serve`, http://127.0.0.1:8000/) y CLI (`isde demo`).
- Guion para la presentación en vivo de tres minutos: `docs/demo.md`.
- Integración de prueba: submódulo `testbeds/alphacorp-intranet` (intranet ficticia en Node).

## Capabilities and Constraints

- Decisión por destinatario: entregar, reformular o `review`. Nada llega a la bandeja sin pasar por `Guard._decide`.
- Muestra la probabilidad de inferencia antes y después de la respuesta (p. ej., de 0 % a 56 %) y si el grafo interno respalda la conclusión.
- Adjuntos de imagen, PDF y audio: un mensaje con adjuntos nunca se reescribe; si no es admisible, va a revisión.
- Los pesos de inferencia son supuestos sin calibrar, y el análisis de texto libre depende de la extracción de Claude.
- El contexto de un destinatario nunca incluye el grafo interno ni datos de otros destinatarios.
- Todos los datos de la demo y de los ejemplos son ficticios.

## Brand Commitments

- Nombre: **mosAIc**, con esta grafía exacta («AI» en mayúsculas).
- Logo: `project-logo.png` es el logo oficial y debe respetarse.
- Idioma: toda la interfaz va en español.
- Restricción obligatoria del usuario (textual): "Frontend for a projector. Use very little text. Do not use small text. Use large shapes, strong contrast, and clear motion."
- Solo modo oscuro, sin modo claro (decisión del usuario).
- Preferencia del usuario: el estándar de la categoría bien ejecutado, con Stripe Radar y Linear como vara de acabado.

## Evidence on Hand

- Caso de demo ficticio: Ana y Luis, el expediente O-17 y BetaAI. En el turno 2, «El expediente O-17 ya está firmado.» llega a Luis y queda en revisión para Ana (de 0 % a 56 %). Fuente: `docs/isde.md`, `docs/demo.md`.
- Política, caso, historial y fuentes de ejemplo: `examples/*.yaml`.
- Logo: `project-logo.png`.
- No hay clientes reales, testimonios, benchmarks ni métricas calibradas. No se inventan, y Buk no se presenta como cliente.

## Product Principles

1. **El destinatario es la unidad.** Cada vista responde qué podría deducir esta persona en particular.
2. **Mostrar el mecanismo, no la jerga.** El salto de probabilidad y la decisión (entregar, reformular, revisar) se leen de un vistazo; RDF, OWL y ProbLog quedan en segundo plano.
3. **Fallar cerrado, a la vista.** Ante la duda, revisión, y la interfaz lo dice con claridad.
4. **Honesto con sus límites.** Los pesos sin calibrar y los datos ficticios nunca se presentan como prueba.

## Accessibility & Inclusion

Se proyecta en una sala: el texto tiene que leerse a distancia y con contraste fuerte. El movimiento explica un cambio de estado, no decora.
