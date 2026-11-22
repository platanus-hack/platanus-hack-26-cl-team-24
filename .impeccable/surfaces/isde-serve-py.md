---
version: 1
slug: "isde-serve-py"
primary_target: "isde/serve.py"
related_targets: []
---

Scope: demo visual de `python -m isde serve` (página única en `isde/serve.py`). Modo: Persuade. La ve el jurado de Platanus Hack 26 en un proyector, mientras quien presenta avanza con el teclado.

Audiencia y tarea: el jurado entiende en una pasada que el mismo mensaje se entrega a una persona y se retiene para otra según lo que ya sabe. Quien presenta avanza con → y responde preguntas en modo libre (destinatario, tarea, borrador, Evaluar, Entregar, Reiniciar).

Restricciones: modo oscuro, sin modo claro. Muy poco texto, nada pequeño, formas grandes, contraste fuerte y movimiento claro. Todo en español. Los datos salen del Guard real (reset y cuatro entregas al cargar), sin cifras escritas a mano. El CSP de la página sigue estricto (nonce y fuentes solo de 'self').

## Direction contract

THESIS: el estándar de la categoría, ejecutado al nivel de Stripe Radar y Linear. Un escenario de dos columnas, Ana y Luis, con veredicto y puntaje de riesgo grandes. Rechaza el panel de tarjetas pequeñas y métricas en fila.

OWN-WORLD: fondo azul marino del logo (#15182d), superficies un paso más claras con borde fino y Inter (variable, alojada en el paquete). Un solo acento, el lavanda de «AI» en el logo (#ae81fd), para la marca y la acción. Las dos citas vienen del logo oficial (PRODUCT.md). Los veredictos tienen colores semánticos: verde para entregado, ámbar para reparado y rojo para revisión humana. Cifras tabulares.

STORY: título → turno 1 con el mensaje → contexto de cada persona → la barra sube (Luis de 0 % a 74 %) → veredicto y bandeja → turno 2 → Ana de 0 % a 56 % y revisión humana; Luis recibe → cierre «Mismo texto. Otra persona. Otra decisión.».

FIRST VIEWPORT: barra superior con el logo mosAIc a la izquierda y el turno y los puntos de paso a la derecha. Banda del mensaje del agente a todo el ancho, en texto grande. Dos columnas iguales: nombre a 3.2rem (4rem no entra a 1280×720 con el resto de la columna), contexto, barra de probabilidad gruesa con marca de límite y porcentaje a 5rem, y el veredicto como placa a todo el ancho de la columna. En la barra superior va la etiqueta «Caso ficticio · pesos sin calibrar». Nada baja de 1.35rem. Abajo a la derecha, «Siguiente →» como acción primaria y «← Anterior» y «Modo libre» como secundarias.

FORM: canon (estándar de la categoría) elegido por el usuario en la ronda 2 de la tirada; seed:f1800f17f20af654. Interacción distintiva: la barra se llena desde «antes» hasta «después» con una curva exponencial y cruza la marca de límite, y entonces la placa del veredicto aparece. Gramática de movimiento: regiones fijas; cada paso cambia el contenido con un fundido y un desplazamiento de 12px.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
