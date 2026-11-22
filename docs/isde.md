# mosAIc

mosAIc revisa una respuesta antes de entregarla a un destinatario. La primera versión ofrece una API Python y una CLI para una bandeja local. El ejemplo es ficticio.

## Ejecutar desde la raíz del repositorio

Si ya instalaste el paquete anterior `isde-guard` en este entorno, ejecuta `python -m pip uninstall isde-guard` antes de instalar `mosaic-guard`. También puedes usar un entorno virtual nuevo.

Requiere Python 3.11 o posterior.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[claude]'
python -m isde demo
python -m unittest discover -s tests -v
```

La demo funciona sin credenciales. Para cada destinatario narra el contexto, el borrador del agente, la evaluación y lo que llega a su bandeja; `python -m isde demo --json` entrega la traza completa. El guion para presentarla está en [demo.md](demo.md).

La demo muestra la divulgación acumulativa. En el turno 1, la misma respuesta («El trámite vence el viernes. El expediente O-17 corresponde a BetaAI.») se entrega completa a Ana y se repara para Luis, que ya citó la firma de O-17. En el turno 2 ambos piden la tarea `record` y el agente propone «El expediente O-17 ya está firmado.», inocuo por sí solo. Luis lo recibe. Para Ana queda en revisión humana: con lo que recibió en el turno 1 deduciría que la oferta para BetaAI está firmada (de 0 % a 56 %).

`python -m isde serve` abre la misma demo como página local para proyector en http://127.0.0.1:8000/. Al cargar, reinicia el historial y recorre los dos turnos paso a paso con → (guion en [demo.md](demo.md)). «Modo libre» conserva los controles (`?user=luis` lo abre con el destinatario elegido). «Evaluar» es una vista previa. «Entregar» pasa por la misma decisión y, si no queda en revisión, confirma la entrega en una base en memoria con un identificador nuevo, de modo que cuenta en la siguiente evaluación. «Reiniciar» vuelve al historial de ejemplo. La página solo escucha en 127.0.0.1, rechaza otros encabezados `Host` y solo acepta cambios por POST JSON desde su propio origen.

El extra `claude` solo hace falta para `key`, `interpret` y `propose`; la demo, `serve` y los tests funcionan sin él. Para usar un historial persistente:

```bash
python -m isde load examples/history.yaml
python -m isde preview luis due --draft "El trámite vence el viernes. El expediente O-17 corresponde a BetaAI."
python -m isde deliver luis due solicitud_001
python -m isde inbox luis
```

La salida de `preview` y `deliver` es una traza privada para el operador. El destinatario recibe exclusivamente el texto de la bandeja. En el ejemplo Luis recibe «El trámite vence el viernes». La bandeja, el historial y la selección de la respuesta se confirman en una sola transacción de SQLite. Repetir el identificador de una entrega devuelve su resultado original, también cuando quedó en revisión (que no llega a la bandeja), y reutilizarlo para otra tarea o borrador es un error. La CLI es una herramienta local de confianza. Una integración debe suministrar la identidad autenticada, la organización y la operación, y publicar únicamente desde la bandeja. El envío a servicios externos requiere su propio adaptador.

## Política y conocimiento

[examples/policy.yaml](../examples/policy.yaml) configura roles, herencia, permisos para consultar recursos y recibir conclusiones, vocabulario, estados protegidos y umbrales. [examples/case.yaml](../examples/case.yaml) define el ámbito, el directorio de asignaciones, las cláusulas permitidas y las alternativas en orden de utilidad. Se pueden sustituir con `python -m isde --policy ruta --case ruta --db ruta.sqlite …`. Los identificadores de rol y de origen proceden de la integración de confianza.

RDFLib construye una vista interna y una vista de evidencia por destinatario a partir de eventos en SQLite. OWL 2 RL deriva la jerarquía de roles y las cadenas de propiedades. A partir de la misma cadena configurable, ProbLog calcula la probabilidad de que el observador pueda reunir las premisas. El evaluador consulta afirmaciones y negaciones explícitas. La falta de evidencia da soporte cero a esa vía y deja abierto el estado real. Una hipótesis externa plausible también puede motivar una reparación si la empresa carece de verificación interna. La traza indica si el grafo interno respalda la conclusión.

| Evidencia sobre el conocimiento | Valor de partida |
| --- | ---: |
| El rol permitía consultar la fuente en la fecha de exposición | 0,15 |
| Hipótesis sobre información externa al directorio | Hasta 0,50 |
| Mensaje entregado | 0,75 |
| Lectura registrada | 0,90 |
| La persona citó la pista | 0,98 |

Los valores son supuestos editables. Una estimación de Claude se limita al máximo del grado de evidencia. El motor recalcula históricos con los pesos vigentes, manteniendo intactos los registros de entrega. La revocación de un rol elimina su autorización desde el fin de vigencia y conserva las exposiciones anteriores. Para reproducir una evaluación histórica se necesita la versión de política y directorio de aquel momento.

Para la familia del ejemplo, el guardrail protege tanto la confirmación como el descarte. Cuando falta autorización, una revelación directa se retiene incluso si se estima que el destinatario ya conoce el secreto. Una inferencia indirecta se retiene si aumenta el conocimiento y el resultado alcanza 0,75 o el aumento alcanza 0,45. Se escoge la primera alternativa admisible que cumple la tarea. Si faltan hechos de respaldo o alternativas útiles, la decisión es `review`.

El modelo de probabilidad supone independencia entre orígenes distintos. Las pistas y copias de un mismo origen comparten un evento aleatorio. El adaptador debe conservar el identificador del origen subyacente y distinguir piezas que se leen por separado. El número estima la capacidad de deducción conforme al modelo. Su calibración requiere casos etiquetados de destinatarios reales o simulados. La vista del piloto está acotada a un destinatario, organización y operación. El historial cruza sesiones de ese ámbito.

## Añadir Claude

```bash
python -m isde key
python -m isde load examples/history.yaml
python -m isde interpret examples/vendor-card.yaml --grade possible_access
python -m isde propose examples/internal-source.yaml > propuestas.json
# Tras revisar las citas, los IDs y los triples propuestos:
python -m isde load propuestas.json
```

Estos comandos requieren `pip install '.[claude]'` y una clave válida. Los tests cubren este flujo con un cliente simulado, sin llamar a la API.

`isde key` usa entrada oculta y el llavero del sistema. También se admite `ANTHROPIC_API_KEY`. El modelo se elige con `ISDE_CLAUDE_MODEL`. Las llamadas envían a Anthropic la política, el texto de la fuente y la vista correspondiente. Para una tarjeta externa, se incluye únicamente el conocimiento atribuido al destinatario y sus roles aplicables.

`interpret` utiliza una tarjeta con fragmentos previamente vinculados a triples por el adaptador. Con `propose`, Claude puede descubrir entidades y relaciones en texto nuevo usando el vocabulario activo. Una propuesta conserva la cita literal para revisar su significado antes de incorporarla. Para sugerir conocimientos externos se suministra una fuente del observador con `user` y `--grade external_hint`. Las reglas y las autorizaciones se cambian en YAML.

## Integrar un agente

```python
from datetime import date
from isde.guard import Guard
from isde.model import Batch, Case, Policy

guard = Guard("isde.sqlite", Policy.load("examples/policy.yaml"), Case.load("examples/case.yaml"))
try:
    # El adaptador de confianza registra la evidencia antes de decidir.
    guard.observe(Batch.load("examples/history.yaml").observations)
    borrador = "El trámite vence el viernes. El expediente O-17 corresponde a BetaAI."
    decision = guard.run("luis", "due", date.today(), request_id="solicitud_002", draft=borrador)
    print(decision["action"], guard.inbox("luis"))  # repair [{'id': 'solicitud_002', 'text': 'El trámite vence el viernes.'}]
finally:
    guard.close()
```

La CLI y la demo web original entregan respuestas de catálogo. La API semántica descrita más abajo evalúa borradores libres con Claude y admite reformulaciones de un agente externo.

## Modelo de amenazas y límites

Qué cubre:

- Un destinatario legítimo que, sin mala intención o a propósito, combina respuestas del agente con lo que ya vio para deducir una conclusión protegida mediante las cadenas declaradas en la política.
- Una salida de Claude errónea o manipulada por texto de la fuente: el modelo solo elige IDs ofrecidos o propone triples con cita literal y vocabulario de la política, la confianza queda topada por el grado de evidencia y las propuestas de `propose` se revisan antes de cargarlas. Rol, organización, operación y origen nunca vienen del modelo.
- Repetición y desorden: las entregas son idempotentes por `request_id`, respetan el orden del historial y la bandeja se confirma en la misma transacción que la decisión.

Qué supone o no cubre:

- Confía en la integración: identidad, roles, directorio, catálogo de cláusulas y su correspondencia con hechos. Si esas entradas mienten, la decisión también.
- Las cadenas configuradas deciden por sí solas. Un camino sin regla entre los extremos de un secreto solo aporta un peso orientativo (`paths.weight`) hasta que Claude lo lee en una revisión semántica. Los caminos de más de `paths.max_length` aristas no se buscan.
- La demo de catálogo reemplaza un borrador desconocido por una respuesta aprobada. La API semántica depende de la cobertura de extracción de Claude.
- No modela colusión entre destinatarios, grupos ni correlación entre operaciones.
- Las probabilidades dependen de pesos sin calibrar y de suponer independencia entre orígenes distintos.
- `interpret` y `propose` envían a Anthropic la política y el texto de la fuente. Para una fuente interna también envían los hechos del grafo interno. Para una externa, solo lo atribuido a ese destinatario y sus roles.
- No se ha medido el rendimiento con grafos grandes.

## Grafo de relaciones y caminos

Cada hecho es una arista `sujeto relación objeto` entre dos nodos. Un mismo par de nodos puede tener varias aristas, con distinto origen, destinatario o relación. Los estados de una familia protegida (`signed`, `yes`) son nodos de tipo `valor`: un camino puede terminar en ellos, pero no los atraviesa. Así, dos entidades que solo comparten un estado no quedan conectadas. Un nodo con más de `paths.max_degree` aristas tampoco sirve de puente.

Una fuente interna puede declarar entidades con `id`, `type`, `label` y `aliases`. Antes de guardar un hecho, mosAIc resuelve cada mención a su nodo usando, en este orden, un alias declarado, el identificador exacto o el único identificador igual sin guiones bajos (`o_17` → `o17`). Un alias que ya nombra a otro nodo se descarta: dos nodos existentes nunca se fusionan. Claude recibe la lista de entidades en `ontology.entities` para reutilizar sus identificadores. Una etiqueta propuesta debe aparecer literalmente en la fuente.

Para cada secreto del grafo interno, el evaluador busca en el grafo del destinatario, más el borrador, caminos de 2 a `paths.max_length` aristas entre sus dos extremos. Una arista directa con otra relación no cuenta como camino, salvo que una regla deduzca el secreto a partir de ella. Cada cambio en la traza incluye `paths`. Cada camino trae las aristas, una oración por arista (`text`), si una regla lo convierte en la conclusión (`rule`) y las relaciones nuevas que esas reglas deducen entre los extremos (`relations`). Esa es la lectura determinística.

En ProbLog, un camino respaldado por una regla ya está cubierto. Un camino sin regla suma una vía con probabilidad `paths.weight` (0,4 por defecto) multiplicada por la de sus aristas. Con ese valor, dos aristas citadas quedan bajo el aumento por defecto. En la revisión semántica, Claude lee hasta cinco caminos nuevos por solicitud y responde qué relación podría deducir el destinatario, si implica el secreto y con qué confianza. Esa lectura reemplaza el peso por defecto de ese camino y se guarda en `path_ratings`. Para hacerlo, se envían a Anthropic las oraciones del camino, el sujeto y la familia protegida. El valor protegido nunca se envía.

`GET /v1/graph?user=ana&day=2026-01-04`, con el encabezado `X-Mosaic-Operator-Token`, devuelve los nodos y las aristas del grafo de ese destinatario. Sin `user`, devuelve el grafo interno.

## API HTTP con reformulación del agente

La API de demostración recibe el borrador de un agente y usa LangGraph para evaluar, pedir una reformulación y volver a evaluar. Claude genera la reformulación con la alternativa del catálogo que el guardrail encontró admisible. mosAIc evalúa el texto generado nuevamente al confirmar la entrega. Si Claude falla, el texto no coincide con el catálogo o se agotan dos intentos, la solicitud queda en revisión. Los comandos siguientes usan explícitamente el caso empresarial histórico; la API sin estas variables inicia el perfil genérico del panel.

```bash
python -m pip install -e '.[api]'
export ANTHROPIC_API_KEY="tu-clave"
export MOSAIC_POLICY=examples/policy.yaml
export MOSAIC_CASE=examples/case.yaml
export MOSAIC_HISTORY=examples/history.yaml
export MOSAIC_API_DB=mosaic-ejemplo.sqlite
python -m uvicorn isde.api:create_app --factory --host 127.0.0.1 --port 8001
```

La clave también puede configurarse con `isde key` si el llavero del sistema está disponible. La API usa `ISDE_CLAUDE_MODEL` para seleccionar el modelo. Los borradores y la alternativa permitida se envían a Anthropic cuando se necesita reformular.

Desde otra terminal:

```bash
curl -X POST http://127.0.0.1:8001/v1/messages \
  -H 'Content-Type: application/json' \
  -d '{"user":"luis","task":"due","day":"2026-01-04","request_id":"solicitud-1","draft":"El trámite vence el viernes. El expediente O-17 corresponde a BetaAI."}'
```

La respuesta contiene `request_id`, `action` y `text`. Los estados son `allow`, `repair` y `review`. Si queda en revisión, `text` es `null`. La bandeja simulada se consulta con `GET /v1/inbox/luis`. El destinatario solo ve las entregas confirmadas. Repetir el identificador con la misma solicitud recupera el resultado anterior. Para una nueva evaluación, usa otro identificador.

Un adaptador de confianza puede registrar información recibida con `POST /v1/observations`, usando el mismo formato de `examples/history.yaml`. La API persiste evidencia y entregas en `mosaic-api.sqlite` por defecto. La ruta puede cambiarse con `MOSAIC_API_DB` o `ISDE_API_DB`. Los archivos de política, caso e historial inicial pueden sustituirse con `MOSAIC_POLICY`, `MOSAIC_CASE` y `MOSAIC_HISTORY`, o sus equivalentes con prefijo `ISDE_`.

Esta API es una demo local de un único proceso para integraciones de confianza. El agente que llama aporta destinatario, tarea e identificador de solicitud. Para un servicio accesible por red se necesita autenticación, autorización de esos datos y un adaptador de entrega real. Este endpoint de catálogo conserva el ciclo de reformulación con Claude. Los endpoints semánticos siguientes reciben revisiones de un agente externo y usan la vista adversarial.
## RUT de personas

Antes de entregar una respuesta, el canal general comprueba el texto final y los hechos asociados a sus cláusulas. Aplica la misma comprobación a las alternativas de reparación. Retiene valores con formato usual de RUT (cuerpo de siete u ocho cifras y dígito verificador válido), incluso sin etiqueta. Si el texto identifica expresamente el valor como RUT o RUN, también lo retiene con un verificador mal escrito. Un número de otro sistema que coincida con ese formato también puede pasar a revisión.

El vocabulario de base incluye `personal_rut` para vincular una persona o ficha con el valor canónico `rut_<cuerpo>_<dv>`, y `identifies_person` para indicar la persona titular de una ficha. Si el destinatario ya pudo conocer el RUT de esa ficha, identificar a su titular también pasa a revisión. Una respuesta de ayuda, como indicar dónde hacer el trámite, puede entregarse si cumple los requisitos de la tarea. Los permisos para conocer otras familias de secretos siguen siendo independientes.

Estas comprobaciones cubren valores literales y relaciones representadas en el grafo. Interpretar preguntas abiertas, alusiones libres o cifras repartidas entre varios mensajes requiere que la integración aporte los hechos correspondientes.

## Hipótesis en la ontología del observador

Una hipótesis expresa una interpretación que un destinatario podría extraer de un texto o de sus antecedentes. Puede clasificar una referencia como identificador personal, relacionar dos entidades o sugerir que un cliente se prepara para abandonar un contrato. El grafo RDF del observador representa cada hipótesis en un nodo de tipo `Interpretation`, con sujeto, relación, valor, cita, origen, fecha, modelo y dos probabilidades. El grafo interno conserva únicamente los hechos aceptados.

- `p_seen` estima la posibilidad de que la pista esté disponible y sea utilizable por ese observador. Procede del grado de evidencia y del límite configurado para la fuente.
- `p_if_seen` estima la posibilidad de que el observador llegue a esa interpretación si ve la pista. Claude propone ese número a partir de la vista individual y el texto visible. La verdad de la conclusión en el mundo real es una cuestión distinta.

ProbLog utiliza el producto para esa vía de inferencia. Puede combinarla con otras pistas mediante las reglas de la política. La implementación agrupa la evidencia con el mismo origen, de modo que reprocesar una copia no añade una fuente independiente. Las probabilidades del modelo requieren calibración. Los predicados, estados protegidos y umbrales se configuran en YAML.

Para incorporar un texto visible para un destinatario:

```bash
isde propose examples/renewal-source.yaml --grade read > hipotesis.json
# Revisar el destinatario, las citas y las afirmaciones antes de cargar la propuesta.
isde load hipotesis.json
```

Para evaluar las interpretaciones de las respuestas candidatas, usa `isde preview luis due --assess` o activa `assess_drafts: true` en la política. Esta opción requiere Claude y envía a la API el texto candidato, el vocabulario y la vista del destinatario. Las vistas previas y las alternativas descartadas dejan intacto su historial. La entrega confirma únicamente las hipótesis de la respuesta que efectivamente llega a la bandeja. Si el modelo falla o cambia la vista mientras se evalúa, el mensaje queda en revisión.

La política de ejemplo incluye `information_type` y `renewal_outlook`. Las señales de formato, como el dígito verificador, se calculan localmente y ayudan al modelo a interpretar el contexto. Las protecciones existentes para identificadores explícitos siguen aplicándose.

## API semántica de mosAIc

La API usa LangGraph para procesar fuentes y para revisar texto libre. Se instala con `python -m pip install -e '.[api]'` y se inicia con `python -m uvicorn isde.api:create_app --factory --host 127.0.0.1 --port 8001`. Configura `ANTHROPIC_API_KEY` o ejecuta `mosaic key`. El modelo puede elegirse con `MOSAIC_CLAUDE_MODEL`.

El panel disponible en http://127.0.0.1:8001/ permite configurar los agentes, el vocabulario y las conclusiones protegidas y probar fuentes y respuestas; consulta [panel.md](panel.md). Un adaptador de confianza puede proponer hechos y perspectivas de destinatarios mediante `POST /v1/sources`. El cuerpo contiene `origin`, `at`, `text` y `recipients`. La llamada devuelve propuestas con citas literales. Para aceptarlas, envía el mismo cuerpo con `accept: true`. La aceptación se registra una vez por origen y contenido. También se pueden incorporar observaciones estructuradas con `POST /v1/observations`.

Un agente externo revisa su borrador con `POST /v1/reviews`. El ejemplo usa los hechos del caso de prueba.

```bash
curl -s http://127.0.0.1:8001/v1/reviews \
  -H 'Content-Type: application/json' \
  -d '{"review_id":"ejemplo-1","user":"luis","task":"due","day":"2026-01-04","question":"¿Cuándo vence el trámite?","text":"El plazo acaba el viernes. O-17 corresponde a BetaAI."}'
```

Si la respuesta indica `revise`, el agente crea un borrador nuevo y lo envía con un identificador de revisión.

```bash
curl -s http://127.0.0.1:8001/v1/reviews/ejemplo-1/revisions \
  -H 'Content-Type: application/json' \
  -d '{"revision_id":"intento-1","user":"luis","text":"El plazo acaba el viernes."}'
```

Tras recibir `approved`, la integración solicita la entrega. La operación comprueba de nuevo el historial y los hechos, y registra una sola entrega en la bandeja local.

```bash
curl -s http://127.0.0.1:8001/v1/reviews/ejemplo-1/deliver \
  -H 'Content-Type: application/json' -d '{"user":"luis"}'
curl -s http://127.0.0.1:8001/v1/inbox/luis
```

El detalle privado puede consultarse en `GET /v1/reviews/ejemplo-1?user=luis` cuando la API se inicia con `MOSAIC_OPERATOR_TOKEN` configurado y la petición incluye la cabecera `X-Mosaic-Operator-Token`. Las respuestas provisionales no actualizan el historial. Los reintentos con el mismo identificador de revisión y texto son idempotentes. Si cambia el contexto antes de entregar, se devuelve `context_changed` y el agente puede solicitar una nueva revisión. Se permiten dos reformulaciones.

Claude debe extraer una cita literal para cada afirmación y evaluar si la respuesta cumple la tarea. Los hechos deben corresponder al vocabulario y contar con respaldo interno. También propone hipótesis desde la vista individual del destinatario. Una extracción incompleta o un error del proveedor impide la aprobación. Estos controles dependen de la calidad de extracción del modelo y las probabilidades no están calibradas. La API funciona como demo local para integraciones de confianza y la bandeja es local. La entrega por correo u otro servicio requiere un adaptador y autenticación.

## Inferencias de varios niveles

La política admite reglas positivas en `rules` además de las cadenas `chains` anteriores. Una regla contiene una o varias premisas en `when` y una conclusión en `then`. Cada una es un triple con sujeto, predicado y objeto. Una variable como `"?x"` vincula las mismas entidades entre premisas y conclusión. Las conclusiones intermedias se declaran en `vocabulary`. Solo las proposiciones que deben protegerse necesitan una entrada en `families`.

Las reglas se aplican hasta alcanzar un punto fijo, tanto en el grafo interno como en la evaluación de lo que un destinatario podría deducir. ProbLog calcula cada conclusión protegida con sus fuentes compartidas, sin contar como evidencias independientes los pasos de la deducción. Para el ejemplo `a ⇒ b ⇒ c ⇒ d`, las reglas y comandos están en [inferencias-multinivel.md](inferencias-multinivel.md).

Las reglas no generan individuos, no aceptan código Prolog y no infieren una negación por ausencia. La corrección de los resultados depende de que las reglas, fuentes y estimaciones estén bien modeladas. Todavía no se ha medido el rendimiento con grafos grandes.
