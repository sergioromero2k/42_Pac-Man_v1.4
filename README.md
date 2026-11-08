# 42_Pac-Man
---

```
core/
├── __init__.py
├── enums.py                  # Direction, ModoFantasma, EstadoJuego, TiposFlags
├── maze.py                   # Maze
├── maze_loader.py            # MazeLoader
├── config.py                 # Config
├── config_loader.py          # ConfigLoader
├── highscore.py              # HighscoreManager, EntradaHighscore
├── cheat_manager.py          # CheatManager
├── game_state.py             # GameState
├── game_engine.py            # GameEngine
└── models/
    ├── __init__.py
    ├── entity.py              # Entity
    ├── player.py              # Player
    ├── ghost.py                # Ghost
    └── pacgum.py                # Pacgum
```
Explicacion de subject_v1.5 - Hasta Mandatory part


| Lo que usas (Arcade) | Equivalente en MLX | ¿Vale? |
|---|---|---|
| `arcade.Window(...)` | `mlx_init` + `mlx_new_window` | Sí |
| `arcade.run()` | `mlx_loop` | Sí |
| `on_update` | `mlx_loop_hook` | Sí |
| `on_key_press` | `mlx_key_hook` o `mlx_hook` | Sí |
| `self.clear()` | `mlx_clear_window` | Sí |
| `self.close()` | `mlx_destroy_window` | Sí |
| `arcade.Text(...).draw()` | `mlx_string_put` | Sí (MLX no centra: hay que calcular la x) |
| `draw_line`, `draw_lrbt_rectangle_filled` | Ninguno (solo `mlx_pixel_put` e imágenes) | No |
| `arcade.View` | Ninguno (MLX no tiene pantallas) | Dudoso |