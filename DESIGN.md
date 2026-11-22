---
name: mosAIc
description: Guardrail que decide, por destinatario, si una respuesta se entrega, se repara o queda en revisión humana.
colors:
  bg: "#15182d"
  deep: "#0e1022"
  surface: "#1c2040"
  raise: "#262b52"
  line: "#363c6b"
  ink: "#f7f7fb"
  mute: "#b4b9d9"
  accent: "#ae81fd"
  accent-hi: "#c4a3ff"
  ok: "#3ddc97"
  warn: "#ffc145"
  bad: "#ff5d6c"
typography:
  display:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "4.6rem"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.04em"
  figure:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "5rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.04em"
    fontFeature: "tnum"
  headline:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "3.2rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.035em"
  verdict:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "2.1rem"
    fontWeight: 800
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1.65rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1.35rem"
    fontWeight: 650
    lineHeight: 1.3
  label:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1.35rem"
    fontWeight: 750
rounded:
  tag: "0.6rem"
  chip: "0.65rem"
  field: "0.7rem"
  control: "0.8rem"
  plate: "0.9rem"
  band: "1.1rem"
  panel: "1.2rem"
spacing:
  xs: "0.6rem"
  sm: "0.9rem"
  md: "1.1rem"
  lg: "1.5rem"
  xl: "2rem"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.deep}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "0.7rem 1.3rem"
  button-primary-hover:
    backgroundColor: "{colors.accent-hi}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "0.7rem 1.3rem"
  button-secondary-hover:
    backgroundColor: "{colors.raise}"
  chip:
    backgroundColor: "{colors.raise}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.chip}"
    padding: "0.4rem 0.85rem"
  plate-allow:
    backgroundColor: "{colors.ok}"
    textColor: "{colors.deep}"
    typography: "{typography.verdict}"
    rounded: "{rounded.plate}"
    padding: "0.85rem 1.2rem"
  plate-repair:
    backgroundColor: "{colors.warn}"
    textColor: "{colors.deep}"
    typography: "{typography.verdict}"
    rounded: "{rounded.plate}"
    padding: "0.85rem 1.2rem"
  plate-review:
    backgroundColor: "{colors.bad}"
    textColor: "{colors.deep}"
    typography: "{typography.verdict}"
    rounded: "{rounded.plate}"
    padding: "0.85rem 1.2rem"
  panel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.panel}"
    padding: "1.3rem 1.5rem"
  field:
    backgroundColor: "{colors.deep}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "0.6rem 0.8rem"
  meter-track:
    backgroundColor: "{colors.deep}"
    height: "1.7rem"
  meter-fill:
    backgroundColor: "{colors.accent}"
  meter-fill-over:
    backgroundColor: "{colors.bad}"
---

# Design System: mosAIc

## Overview

**Creative North Star: "La sala de control nocturna"**

El estándar de la categoría de seguridad (la familia de Stripe Radar y Linear) llevado a escala de proyector. Un fondo azul marino tomado del logo, superficies un paso más claras con borde fino, Inter en pesos altos y un único acento lavanda. Todo se lee a distancia: el texto más chico mide 1.35rem sobre una raíz que escala con el viewport (`clamp(14px, 2.05vmin, 34px)`), así que la página entera crece con la pantalla y no con un zoom.

La densidad es baja a propósito. Cada vista tiene pocas regiones fijas (barra superior, banda del mensaje, dos columnas, controles) y lo que cambia es el contenido dentro de ellas. El color semántico solo aparece donde hay una decisión: la barra que cruza el límite y la placa del veredicto. El resto es azul marino, tinta y lavanda.

Solo modo oscuro; no existe una variante clara.

**Key Characteristics:**
- Fondo azul marino del logo, superficies tonales con borde de 1px, sin sombras.
- Inter variable autoalojada, pesos 650 a 800, tracking negativo en los tamaños grandes.
- Un acento lavanda para marca, acción primaria y progreso; verde, ámbar y rojo solo para veredictos.
- Cifras tabulares en todo número.
- Escala relativa al viewport: nada por debajo de 1.35rem.
- Movimiento que explica un cambio de estado: la barra se llena con curva exponencial y la placa entra con un barrido.

## Colors

Azul marino profundo en tres pasos tonales, tinta casi blanca, un lavanda y tres semánticos saturados.

### Primary
- **Lavanda AI** (`accent`): el lavanda de «AI» en el logo. Botón primario, punto de paso activo, relleno de la barra de probabilidad mientras está bajo el límite, icono del mensaje del agente, palabra destacada del cierre y color de selección.
- **Lavanda claro** (`accent-hi`): hover del primario, anillo de foco y la cifra dentro de un chip de contexto.

### Neutral
- **Azul marino del logo** (`bg`): fondo de página.
- **Pozo** (`deep`): el paso más oscuro. Interior de la barra y de los campos, y texto sobre cualquier relleno de color (botón primario, placas, alerta).
- **Superficie** (`surface`): paneles, banda del mensaje, botones secundarios.
- **Relieve** (`raise`): chips, avatar, hover de botones secundarios.
- **Línea** (`line`): todo borde de 1px, puntos de paso inactivos, separadores.
- **Tinta** (`ink`): texto principal y la marca de límite de la barra.
- **Tinta tenue** (`mute`): etiquetas, estados vacíos, contexto secundario, hover de bordes.

### Semantic
- **Verde entregado** (`ok`): placa «Entregado».
- **Ámbar reparado** (`warn`): placa «Reparado».
- **Rojo revisión** (`bad`): placa «Revisión humana», relleno de la barra después de cruzar el límite, icono del candado de la conclusión protegida y alerta de error.

### Named Rules
**The One Voice Rule.** El lavanda es el único color de marca y de acción. Ningún otro tono hace de acento decorativo.

**The Verdict Owns Color Rule.** Verde, ámbar y rojo significan entregado, reparado y revisión. No se usan para decorar, ni para nada que no sea una decisión o un riesgo.

**The Dark Text on Color Rule.** Todo relleno saturado (primario, placas, alerta) lleva texto en `deep`, nunca blanco.

## Typography

**Display Font:** Inter variable (con system-ui, sans-serif), autoalojada en `isde/fonts/`, pesos 100 a 900.

**Character:** una sola familia, trabajada con peso y tracking. Los tamaños grandes van en 800 con tracking negativo; el texto de lectura en 650 a 750. Nada en 400.

### Hierarchy
- **Display** (800, 4.6rem, 1.02, -0.04em): pantallas de apertura y cierre, centradas, máximo 15ch, `text-wrap: balance`.
- **Figure** (800, 5rem, 1, -0.04em, tabular): el porcentaje de probabilidad junto a la barra.
- **Headline** (800, 3.2rem, 1, -0.035em): nombre del destinatario en cada columna.
- **Verdict** (800, 2.1rem, -0.025em): texto de la placa del veredicto.
- **Title** (700, 1.65rem, 1.2, -0.02em): la banda del mensaje del agente, balanceada.
- **Body** (650, 1.35rem, 1.3): chips de contexto, bandeja, campos.
- **Label** (750, 1.35rem): botones, marca «límite», etiquetas de formulario (700 en tinta tenue).

### Named Rules
**The 1.35 Floor Rule.** Ningún texto baja de 1.35rem en la vista de proyector. Si no entra, se quita texto, no se achica.

**The Tabular Rule.** Todo número (porcentajes, turnos, cifras en chips) usa `font-variant-numeric: tabular-nums`.

## Layout

Una sola pantalla de altura completa (`100dvh`, ancho máximo 120rem), en una grilla de tres filas: barra superior, escenario y controles. El escenario apila la banda del mensaje a todo el ancho sobre dos columnas iguales, una por destinatario. El espacio dominante es 1.1rem: separa filas, columnas y los bloques dentro de cada columna. Relleno de página de 1.1rem vertical y 2rem lateral; paneles con 1.3rem por 1.5rem.

Las regiones son fijas: avanzar de paso cambia el contenido, no la estructura. Las piezas de cada columna (contexto, barra, veredicto) ocupan su lugar desde el principio y aparecen con opacidad, sin desplazar al resto.

Bajo 52rem la raíz pasa a 16px, las columnas se apilan, la barra ocupa una fila propia sobre el porcentaje (3rem, alineado a la izquierda), los puntos de paso se ocultan y los controles se envuelven.

## Elevation & Depth

Plano. No hay sombras en ninguna parte. La profundidad sale de tres pasos tonales (`deep` bajo `bg` bajo `surface` bajo `raise`) y de un borde de 1px en `line` alrededor de cada superficie. Lo hundido (barra, campos) va en `deep`; lo que sobresale (chips, avatar, hover) va en `raise`.

### Named Rules
**The Tonal Step Rule.** Para separar un elemento de su fondo se sube o baja un paso tonal y se agrega borde de 1px. Nunca una sombra.

## Shapes

Esquinas suaves y proporcionales al tamaño: 0.6 a 0.7rem en piezas chicas (etiqueta, chip, campo), 0.8 a 0.9rem en controles y placas, 1.1 a 1.2rem en la banda y los paneles. La barra y los puntos de paso son píldoras (radio igual a media altura). El avatar es un círculo. Los bordes punteados marcan lo provisional o vacío: la etiqueta «Caso ficticio · pesos sin calibrar» y el chip «Nada todavía».

Los iconos son SVG en línea de 24px de trazo (2.2, 2.8 en las placas), extremos redondeados, en `currentColor`, a 1.2em.

## Components

### Buttons
Sólidos, grandes y discretos salvo la acción principal.
- **Shape:** esquinas suaves (0.8rem), borde de 1px.
- **Primary:** relleno lavanda con texto `deep`, 0.7rem por 1.3rem, label 750. Un solo primario por vista («Siguiente», «Evaluar»).
- **Secondary:** superficie con borde `line` y texto en tinta.
- **Hover / Focus:** el secundario sube a `raise` y su borde a `mute`; el primario pasa a lavanda claro. Al presionar baja 1px. Foco: contorno de 3px en lavanda claro con 3px de separación. Deshabilitado al 35 % de opacidad.

### Chips
- **Style:** relieve con borde de 1px, 0.65rem, body 650; la cifra va en lavanda claro, 800, tabular.
- **State:** vacío con fondo transparente, borde punteado y tinta tenue.

### Cards / Containers
- **Corner Style:** 1.2rem en columnas, 1.1rem en la banda del mensaje.
- **Background:** `surface`.
- **Shadow Strategy:** ninguna (ver Elevation & Depth).
- **Border:** 1px en `line`.
- **Internal Padding:** 1.3rem por 1.5rem; la banda, 1rem por 1.4rem.

### Inputs / Fields
- **Style:** pozo (`deep`) con borde de 1px, 0.7rem, 0.6rem por 0.8rem, texto en tinta 600. La etiqueta va encima en tinta tenue 700.
- **Focus:** el mismo contorno lavanda claro de 3px que los botones; hover sube el borde a `mute`.

### Navigation
Barra superior: logo oficial a la izquierda (2.8rem de alto), etiqueta punteada de caso ficticio, y a la derecha el turno en tinta tenue y los puntos de paso. Cada punto es una píldora de 0.9rem en `line`; el activo se estira a 2.4rem en lavanda con la curva de la casa.

### Barra de probabilidad (signature)
Pista de 1.7rem en `deep` con borde, relleno en lavanda y una marca de límite en tinta (4px, sobresale 0.55rem arriba y abajo) con la palabra «límite» debajo. El relleno va de «antes» a «después» en 1.3s con curva exponencial (`1 - 2^(-10t)`); en el instante en que cruza el límite se vuelve rojo. El porcentaje a la derecha en Figure; sin cambio, «Sin aumento» en 1.6rem tinta tenue.

### Placa de veredicto (signature)
Placa a todo el ancho de la columna, 0.9rem, relleno semántico (verde, ámbar, rojo) con texto `deep` en Verdict y su icono. Entra con un barrido de izquierda a derecha (`clip-path`, 0.7s). Debajo, la bandeja: lo que el destinatario recibe, entre comillas latinas, o «No recibe nada» en tinta tenue.

### Motion
Una curva para todo: `cubic-bezier(.16,1,.3,1)`. El contenido nuevo sube 0.7rem (unos 12px) mientras aparece (0.55 a 0.8s). Con `prefers-reduced-motion` se apagan animaciones y transiciones y la barra salta al valor final.

## Do's and Don'ts

### Do:
- **Do** usar el azul marino del logo (`bg`) de fondo y subir de paso tonal con borde de 1px para separar superficies.
- **Do** reservar el lavanda para la marca, la acción primaria y el progreso.
- **Do** mostrar cada decisión con su color semántico y su icono, en texto `deep` sobre el relleno.
- **Do** mantener todo texto en 1.35rem o más en la vista de proyector y quitar texto antes que achicarlo.
- **Do** usar cifras tabulares en todo número.
- **Do** mantener regiones fijas y animar solo el contenido que cambia, con la curva de la casa y una subida de 0.7rem.
- **Do** marcar lo ficticio o sin calibrar a la vista, con borde punteado.

### Don't:
- **Don't** agregar sombras; la profundidad es tonal.
- **Don't** usar verde, ámbar o rojo como decoración o como acento de marca.
- **Don't** agregar un segundo color de acento ni degradados.
- **Don't** construir una fila de tarjetas chicas con métricas; el escenario son dos columnas grandes, una por destinatario.
- **Don't** agregar un modo claro.
- **Don't** usar texto blanco sobre rellenos saturados.
- **Don't** alterar la grafía «mosAIc» ni recolorear el logo oficial.
