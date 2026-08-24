# Días de Persona A — estado real vs plan original

| Día | Tarea prevista | Estado real |
|---|---|---|
| **Día 1** | Kickoff: contratos, setup del repo | ✅ Hecho (con mucho más detalle del previsto — diagrama UML completo) |
| **Día 2** | `config.py` — parser JSON | ✅ Hecho (`Config` + `ConfigLoader` completos) |
| **Día 3** | `maze_loader.py` — integración A-Maze-ing | **Aquí estás ahora mismo** |
| **Día 4** | `Entity` + `Player` (movimiento, colisión) | ✅ Hecho |
| **Día 5** | `Pacgum`/`Super-pacgum` | ✅ Hecho (como clase única con flag `is_super`) |
| **Día 6** | `Ghost` base — movimiento autónomo | ✅ Hecho |
| **Día 7** | Comportamiento de persecución (chase) | ✅ Hecho (dentro de `get_next_move()`) |
| **Día 8** | Frightened/eaten + timers de respawn |  Parcial — `change_mode()`/`respawn()` están, pero **falta la lógica de timers** (cuánto dura el frightened y cuándo vuelve a chase automáticamente). Esto vive en `GameState`, aún no empezado |
| **Día 9** | Sistema de puntuación |  **Falta un detalle** — se decidió mover `total_score` a `Player`, pero nunca se añadió el método `add_score()`/`sumar_puntos()` en `player.py`. Es un cabo suelto que hay que cerrar |
| **Día 10** | Integración (JUNTOS) | Pendiente — depende de tener `GameState`/`GameEngine` |
| **Día 11** | `HighscoreManager` | Pendiente |
| **Día 12** | Progresión de niveles | Pendiente (parte de `GameState`/`GameEngine`) |
| **Día 13** | Cheat mode (`CheatManager`) | Pendiente |
| **Día 14-20** | Error handling, tests, playtesting, docstrings, packaging, README, repaso final | Pendiente |