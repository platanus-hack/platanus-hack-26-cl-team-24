# team-24 Platanus Hack 26: Santiago ft. Buk Project

<img src="./project-logo.png" alt="Logo de mosAIc" width="200" />

Track: 🛡️ AI Security

team-24

- Claudio Alexis Canales Pavez ([@claudiocanalespavez](https://github.com/claudiocanalespavez))
- Gabriel Joaquín Carmona Díaz ([@m1tuw](https://github.com/m1tuw))
- Juan Pablo Herrera Pizarro ([@jpherrerap](https://github.com/jpherrerap))
- Diego Agustín Moreno Guzmán ([@diegomorenoxor](https://github.com/diegomorenoxor))
- Sebastián Nicolás Ferrá Sepúlveda ([@sebastianferra](https://github.com/sebastianferra))

## mosAIc

mosAIc es un guardrail que revisa mensajes antes de entregarlos, ya sea de personas o agentes de IA. Detecta cuándo una frase inocente, sumada a lo que el destinatario ya sabe, le permitiría deducir un secreto, y en ese caso detiene el envío y notifica al usuario.

## Probarlo

Para usar el panel con Claude en Python 3.11 o posterior:

```bash
python -m pip install -e '.[api]'
mosaic key
python -m uvicorn isde.api:create_app --factory --host 127.0.0.1 --port 8001
```

Abre http://127.0.0.1:8001/ para usar las pestañas de simulación, configuración, notificaciones y elementos marcados. Puedes editar prompts y secretos, analizar fuentes y evaluar respuestas de texto libre. El panel empieza sin secretos de ejemplo; el análisis adversarial busca posibles datos sensibles incluso antes de que configures categorías. Si prefieres, configura `ANTHROPIC_API_KEY` en el entorno en lugar de `mosaic key`. Los análisis con Claude consumen API. La configuración y los registros se guardan en la base de datos de la API. Detalles y límites en [docs/panel.md](docs/panel.md).

La demo original, con respuestas de catálogo y sin Claude, sigue disponible:

Requiere Python 3.11 o posterior. Desde la raíz del repositorio, en macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
python -m isde demo
python -m unittest discover -s tests
```

La demo usa datos ficticios, corre en memoria y no necesita clave de Claude. La API de texto libre requiere una clave y el extra de instalación `api`. `python -m isde serve` muestra el mismo caso como página local en http://127.0.0.1:8000/.

## Documentación

- [docs/isde.md](docs/isde.md): cómo decide, política en YAML, historial persistente, integración con Claude y límites conocidos.
- [docs/demo.md](docs/demo.md): guion de 3 minutos para presentar la demo.
- [docs/panel.md](docs/panel.md): configuración de agentes, secretos y pruebas desde la página.
- [docs/inferencias-multinivel.md](docs/inferencias-multinivel.md): reglas y pruebas de inferencias encadenadas.
- [isde/prompts.py](isde/prompts.py): guías para construir la ontología interna y evaluar la perspectiva adversarial.
- [project-description.md](project-description.md): ficha del proyecto.
- [testbeds/alphacorp-intranet](https://github.com/jpherrerap/alphacorp-intranet): intranet MVC ficticia (Node) que usa la API de mosAIc. Es un submódulo: `git submodule update --init`.
