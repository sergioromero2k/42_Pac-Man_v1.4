# Plan de estudio y desarrollo — Proyecto Pacman (42) — 20 días (ORIENTATIVO, NO NECESARIAMENTE ASI)

**Equipo:** Persona A (Core / Lógica de juego) · Persona B (UI / Renderizado / Packaging)

## Reparto de módulos (para no tocar los mismos archivos)

**Persona A — `core/`**
- `config.py` (parser JSON + comentarios, validación, defaults)
- `maze_loader.py` (adaptador al paquete A-Maze-ing)
- `models/player.py`, `models/ghost.py`, `models/pacgum.py`, `models/entities.py`
- `game_state.py` (máquina de estados: menu/playing/paused/gameover)
- `highscore.py` (persistencia JSON)
- `cheat.py`

**Persona B — `ui/` + `packaging/`**
- `renderer.py` / `view.py` (dibujo con MLX/pygame)
- `ui/menu.py`, `ui/hud.py`, `ui/pause_screen.py`, `ui/game_over_screen.py`
- `input_handler.py` (teclado)
- `packaging/` (script para Itch.io/Steam)

`main.py` se escribe **juntos** el día 1 (game loop mínimo) y casi no se vuelve a tocar.

---

## Flujo de Git (rama por módulo, no por persona)

Estructura de ramas sugerida:

```
main                        # siempre estable, funciona con Makefile run
 ├── dev                    # rama de integración diaria
 │    ├── feature/config-parser        (A)
 │    ├── feature/maze-loader          (A)
 │    ├── feature/player               (A)
 │    ├── feature/ghost-ai             (A)
 │    ├── feature/highscore            (A)
 │    ├── feature/cheat-mode           (A)
 │    ├── feature/renderer             (B)
 │    ├── feature/ui-menu              (B)
 │    ├── feature/ui-hud               (B)
 │    ├── feature/ui-pause-gameover    (B)
 │    └── feature/packaging            (B)
```

**Reglas prácticas:**
- `main` solo se actualiza vía merge desde `dev`, nunca directo. `dev` es donde se integra a diario.
-  **Importante:** las ramas son **por tarea, no por persona**. No hagáis "rama-A" y "rama-B" fijas donde cada uno acumula días de trabajo — eso genera un solo merge gigante al final, con conflictos grandes y difíciles de resolver. En vez de eso, cada uno va creando y **borrando** ramas continuamente, una por cada tarea pequeña.
- Cada tarea nueva = rama nueva desde `dev` (`git checkout -b feature/nombre dev`), nunca trabajéis los dos en la misma rama a la vez.
- Commits pequeños y descriptivos, prefijo por tipo: `feat:`, `fix:`, `test:`, `docs:`, `refactor:` (Conventional Commits). Facilita generar el changelog/historial para el documento de gestión.
- Pull Request obligatorio para mergear a `dev`, aunque seáis solo 2 — el otro revisa antes de aprobar (esto también os sirve como evidencia de "peer review" para la documentación de gestión del proyecto).
- `git pull --rebase` antes de empezar a trabajar cada día, para evitar historiales divergentes.
- Si dos ramas van a tocar el mismo archivo (ej. `main.py` o `game_state.py`), avisad en el chat del equipo antes de empezar — es la señal para hacer una sync rápida en vez de arriesgar un merge conflict grande.
- Borrar la rama feature en cuanto se mergea, para mantener el repo limpio.

**Extra recomendado — pre-commit hook:**
Añadid un hook simple (`.git/hooks/pre-commit` o la librería `pre-commit`) que corra `flake8` y `mypy` antes de cada commit. Así nunca llega código roto a `dev`, y os ahorra descubrir errores de lint el día 15 en vez de sobre la marcha.

**Extra recomendado — tablero Kanban:**
Usad un tablero (GitHub Projects, Trello, Notion) con columnas To Do / In Progress / Review / Done, reflejando las ramas activas. Os sirve doblemente: organización real y evidencia lista para el apartado de "Project management" del README.

**Cheatsheet de comandos — flujo diario:**

```bash
# Al empezar una tarea nueva
git checkout dev
git pull --rebase
git checkout -b feature/nombre-tarea

# Mientras trabajas (commits pequeños y frecuentes)
git add archivo.py
git commit -m "feat: descripción corta de lo que hace"

# Al terminar la tarea
git push origin feature/nombre-tarea
# → abrir Pull Request hacia dev en GitHub
# → el compañero revisa y aprueba
# → mergear y luego borrar la rama:
git checkout dev
git pull --rebase
git branch -d feature/nombre-tarea
git push origin --delete feature/nombre-tarea

# Si dev avanzó mientras trabajabas y quieres traer esos cambios a tu rama
git checkout feature/nombre-tarea
git rebase dev
# si hay conflictos: Git te marca los archivos en conflicto
git status
# editas el archivo, quitas las marcas <<<<<<< ======= >>>>>>>
git add archivo-resuelto.py
git rebase --continue

# Ver qué cambió antes de mergear (revisión rápida)
git diff dev...feature/nombre-tarea

# Deshacer un commit local que aún no has pusheado (por si metiste la pata)
git reset --soft HEAD~1
```

**Resolviendo un conflicto de merge, paso a paso:**
1. Git te avisa qué archivo(s) tienen conflicto.
2. Abres el archivo y buscas los bloques `<<<<<<<`, `=======`, `>>>>>>>`.
3. Decidís juntos (por chat/llamada de 2 min) qué versión se queda, o combináis ambas.
4. Borras las marcas de conflicto, guardas, `git add` sobre ese archivo.
5. `git rebase --continue` (o `git commit` si era un merge normal en vez de rebase).
6. Corres los tests/lint de nuevo antes de pushear, por si el conflicto rompió algo silenciosamente.

---

## Día 1 — Kickoff (JUNTOS)
- Definir interfaces/contratos: qué métodos tiene `Ghost`, qué devuelve `MazeLoader.load()`, forma del config ya parseado. Escribirlo como stubs con type hints.
- Setup del repo: Makefile (`install`, `run`, `debug`, `clean`, `lint`), flake8, mypy, `.gitignore`, entorno virtual.
- Crear ramas de trabajo (`feature/core-*`, `feature/ui-*`).
- **Teoría:** OOP (composición vs herencia), diseño por contrato, flujo de branches en Git.

## Día 2
- **A:** `config.py` — parseo de JSON ignorando líneas `#` (y opcionalmente `//`, `/* */`), validación de claves, valores por defecto seguros.
- **B:** Setup de la librería gráfica (MLX o similar) — abrir ventana, dibujar un grid estático de prueba.
- **Teoría A:** parsing de texto, regex básico. **Teoría B:** game loop y delta time.

## Día 3
- **A:** Integrar el paquete `A-Maze-ing` asignado → `maze_loader.py`, probar con `PERFECT=False`, manejar fallos del generador sin crash.
- **B:** Esqueleto de `ui/menu.py` (Start Game / View Highscores / Instructions / Exit) — pantalla estática.
- **Teoría A:** patrón adaptador. **Teoría B:** diseño de pantallas/estados de UI.

## Día 4
- **A:** Clase base `Entity` + `Player` (movimiento en 4 direcciones, solo por corredores, colisión con paredes).
- **B:** `input_handler.py` — captura de teclado (flechas/WASD), acciones dummy.
- **Teoría A:** máquinas de estados finitos (FSM) para el game loop. **Teoría B:** patrones de manejo de eventos.

## Día 5
- **A:** `Pacgum` y `Super-pacgum` — colocación (corredores / 4 esquinas).
- **B:** `renderer.py` — dibujar maze + jugador usando las estructuras de datos de A.
- **Sync (15 min):** confirmar formato de datos del maze y del jugador.

## Día 6
- **A:** `Ghost` base — movimiento autónomo por corredores (base para el pathfinding).
- **B:** HUD (score, vidas, nivel, tiempo restante).
- **Teoría A:** BFS en grids. **Teoría B:** renderizado de overlays/HUD.

## Día 7
- **A:** Comportamiento de persecución por fantasma (target tile: Blinky persigue directo, Pinky emboscada, Inky impredecible, Clyde errático).
- **B:** Pantallas de Game Over y Victoria (UI estática).
- **Teoría A:** heurísticas de IA simples (target-tile). **Teoría B:** transiciones entre pantallas.

## Día 8
- **A:** Estado "edible"/frightened de los fantasmas + respawn tras ser comidos (timers).
- **B:** Menú de pausa (resume / volver al menú).
- **Teoría A:** timers y cooldowns en una FSM. **Teoría B:** pausar/reanudar el loop sin romper estado.

## Día 9
- **A:** Sistema de puntuación (pacgum/super-pacgum/fantasma) conectado a las colisiones.
- **B:** Conectar botones del menú a `game_state.py` (Start → Playing, etc.).
- **Sync (30 min):** cerrar juntos el contrato de `game_state.py`.

## Día 10 — Integración (JUNTOS)
- Unir lógica de A con renderizado de B: conseguir un nivel completo jugable de principio a fin.
- Cazar y arreglar bugs de integración.
- **Teoría:** debugging con `pdb`, testing de integración.

## Día 11
- **A:** `highscore.py` — persistencia JSON, top 10, validación de nombre (máx 10 car., alfanumérico+espacios) y puntuación.
- **B:** Pantalla de "introducir nombre" en Game Over/Victoria.
- **Teoría A:** manejo robusto de I/O (archivo corrupto o ausente). **Teoría B:** UX de inputs de texto custom.

## Día 12
- **A:** Progresión de niveles (≥10 niveles, seed=42 en nivel 1, random después, límite de tiempo, mantener score/vidas entre niveles).
- **B:** Mostrar highscores en el menú principal; refinar HUD con nivel/tiempo.
- **Teoría A:** RNG con semilla. **Teoría B:** binding de datos dinámicos en UI.

## Día 13
- **A:** Cheat mode (invencibilidad, skip de nivel, congelar fantasmas, vidas extra, velocidad) — flags/hooks en el core.
- **B:** Atajos de teclado del cheat mode + indicador visual de que está activo.
- **Teoría (ambos):** cómo exponer flags de debug sin romper el flujo normal.

## Día 14
- **A:** Repaso de manejo de errores en config/maze/highscore (nunca traceback, siempre mensaje claro + fallback).
- **B:** Pulido visual (colores, fuentes, animaciones, "vibe" del juego).
- **Teoría:** buenas prácticas de excepciones; principios básicos de UI/UX.

## Día 15
- **A:** Tests unitarios (pytest) del core, cubriendo edge cases.
- **B:** Plan de pruebas manuales de la UI.
- **Ambos:** pasar `flake8` y `mypy --strict`, corregir todo.
- **Teoría:** pytest básico, matices de mypy strict.

## Día 16 — Playtesting (JUNTOS)
- Jugar de principio a fin: ≥10 niveles, timeout de nivel, config corrupto, fallo del generador, perder todas las vidas, ganar el juego.
- Arreglar todos los bugs encontrados.

## Día 17
- **A:** Docstrings (PEP 257) en todo `core/`.
- **B:** Docstrings en `ui/` + preparar script de empaquetado (PyInstaller / butler para Itch.io).
- **Teoría:** empaquetado de apps Python para distribución.

## Día 18
- **Ambos:** Empaquetar y subir a Itch.io/Steam como build privada/no listada. Probar el build empaquetado de principio a fin.

## Día 19
- **Ambos:** Redactar `README.md` completo (primera línea en cursiva con logins, Descripción, Instrucciones, Recursos + uso de IA, Configuración, Highscore, Maze Generation, Implementation, Arquitectura, Project Management con link a la carpeta de gestión).
- Completar documentos de gestión de proyecto (Gantt/Kanban, seguimiento real vs plan, análisis de riesgos, organización del equipo, plan de test de aceptación, conflictos/bloqueos).

## Día 20 — Repaso final (JUNTOS)
- Releer el subject línea por línea como checklist.
- Ensayar la defensa: cada uno debe poder explicar **también** el módulo del otro (te pueden preguntar cualquier cosa).
- Preparar mentalmente el "recode" (pequeña modificación en vivo durante la evaluación).
- Día de buffer para últimos arreglos.

---

### Notas clave
- Los días de "Sync" no son opcionales: si os saltáis la sincronización de interfaces, es cuando aparecen los conflictos de Git.
- Si vais con retraso, el **Día 10** (integración) es el punto de control natural para replanificar el resto.
- No escribáis vuestro propio generador de laberintos — está prohibido explícitamente en el subject.

### Extras que os pueden ahorrar dolores de cabeza
- **Daily de 5-10 min** (aunque sea por chat de voz/texto): qué hice ayer, qué haré hoy, qué me bloquea. No hace falta que sea presencial ni largo, pero mantiene sincronizados los contratos entre módulos.
- **Checklist antes de mergear una feature:** ¿pasa flake8? ¿pasa mypy? ¿tiene docstrings? ¿tiene al menos un test si es lógica del core? ¿rompe algo en `dev`?
- **Un documento vivo de "decisiones técnicas"** (puede ser un `DECISIONS.md` en la carpeta de gestión): cada vez que elegís algo importante (ej. "usamos heurística greedy en vez de A* para los fantasmas"), anotadlo con una línea del porqué. Os sirve para el README y para defender el proyecto sin titubear.
- **Grabad o anotad los bloqueos reales** que surjan (ej. "el paquete A-Maze-ing no traía tal método") — es contenido directo para la sección "Summary of any blocking points" que pide el subject.