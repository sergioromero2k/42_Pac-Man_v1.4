# Progreso — Pac-Man 42

## Core (Persona A) — estado actual

| Módulo | Estado |
|---|---|
| core/enums.py | ✅ Hecho |
| core/maze.py | ✅ Hecho |
| core/models/entity.py | ✅ Hecho |
| core/models/player.py | ✅ Hecho |
| core/models/ghost.py | ✅ Hecho |
| core/models/pacgum.py | ✅ Hecho |
| core/config.py | ✅ Hecho |
| core/config_loader.py | ✅ Hecho |
| core/maze_loader.py | ✅ Hecho |
| core/highscore.py | 🔲 En progreso — esqueleto listo, faltan 4 métodos |
| core/cheat_manager.py | 🔲 Pendiente |
| core/game_state.py | 🔲 Pendiente |
| core/game_engine.py | 🔲 Pendiente |

## UI (Persona B) — estado actual
- Diagrama UML cerrado (View base + GameView/MenuView/PauseView/FinishView + Renderer)
- Código: no empezado todavía

## Próximos pasos
1. Cerrar HighScoreManager (load_from_disk, save_to_disk, add_new_score, keep_only_top_10)
2. CheatManager
3. GameState / GameEngine
4. Empezar a integrar código de Persona B (recibido por zip, sin Git de su parte)