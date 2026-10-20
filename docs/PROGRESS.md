# Progreso — Pac-Man 42

Última actualización: 2026-10-20 (martes)

## Dónde estamos

Repaso del proyecto día a día, comprobando cada tarjeta con la salida real de
los comandos antes de pasarla a Done. Estado del tablero:

| Día | Parte | Tarjeta | Estado |
|---|---|---|---|
| 1 | A y B | Contratos, stubs con type hints, setup del repo, docs | ✅ Done |
| 2 | A | Config + ConfigLoader | ✅ Done |
| 2 | B | Ventana arcade con grid de prueba (#5) y game loop con delta time (#6) | ✅ Done |
| 3 | A | MazeLoader (adaptador de A-Maze-ing) | ✅ Done |
| 3 | B | Menú principal estático (`ui/menu.py`) | ✅ Done |
| 4 | A | `Entity` + `Player` (movimiento, colisión) y bug de puntos de aparición | 🔄 In Progress |
| 4 | B | `input_handler.py` (teclado → `Direction`) | 🔲 Pendiente (falta el archivo del compañero) |
| 5-20 | — | Resto de tarjetas | 🔲 Backlog (ver tablero) |

## Hecho hasta ahora

- **Día 1:** Makefile corregido (`pdb`, `clean`/`clean_venv`/`fclean`, `.whl` del
  generador), `pacgum.py` renombrado, `mypy --strict core/` limpio salvo el
  módulo `highscore.py` (a medias).
- **Día 2 A:** `Config` es un `@dataclass(frozen=True)`; `ConfigLoader` nunca
  lanza excepciones (aviso + valor por defecto + continuar), con ayudantes
  `_get_int`, `_get_str`, `_get_levels`. Probado con archivo ausente, JSON roto,
  raíz que no es objeto, valores inválidos y claves desconocidas.
- **Día 2 B:** se elige **arcade 3.3.3** (el compañero ya programó la UI con
  arcade). Ventana de prueba con bucle basado en `delta_time` verificado con
  `make run`.
- **Punto de entrada:** `pac-man.py` con exactamente un argumento (el config);
  con otro número de argumentos muestra el uso, sin traceback.
- **Día 3 A:** `MazeLoader` expande cada celda del generador a una casilla impar
  (2n+1). Las celdas con valor 15 (el "42") se tratan como muro sólido.
  Cualquier fallo del generador sale como `MazeLoaderError` encadenado.
  Comprobado: misma semilla = mismo laberinto, `seed=0` = aleatorio, todos los
  caminos conectados, `(20, 10)` da 41x21 casillas, 408 caminos y 453 muros.
- **Día 3 B:** menú adaptado del compañero con type hints y objetos
  `arcade.Text` (sin el aviso de rendimiento de `draw_text`).
- Todo commiteado y subido a `main`.

## En curso: Día 4 A

Cambios a aplicar y probar:

- [ ] `Maze`: añadir `_nearest_path` y usarlo en el centro y en las esquinas
      (el centro y las 4 esquinas calculados a mano caen en muro).
- [ ] `Entity.move`: asignar `current_direction` solo si el movimiento se
      realiza (si no, Pac-Man se queda parado mirando al muro).
- [ ] `Player`: `speed`, `update(delta_time)`, `_step()` y `respawn()` que
      borra la dirección pedida.
- [ ] Prueba por terminal: `spawn (19, 10) is path: True` y `wall entries: 0`.
- [ ] Commit y tarjetas a Done (bug de `Maze` y `Entity` + `Player`).

## Hallazgos del subject (a tener en cuenta)

- **Punto de entrada:** `pac-man.py` con exactamente un argumento. Cualquier
  fallo → mensaje claro, nunca traceback.
- **V.3:** valor ausente o inválido → default, mensaje claro y continuar.
  Claves desconocidas se ignoran.
- **V.4:** el generador se usa tal cual, sin modificarlo; el loader se adapta a
  su interfaz; `PERFECT=False`; si falla, manejar el error con limpieza.
- El config **se modificará durante la defensa**: la validación importa.
- `mazegenerator` solo fija la semilla si `seed > 0`; con 0 el nivel 1 sería
  aleatorio. Por eso `seed` tiene mínimo 1.
- Con menos de 14x10 celdas el generador no puede dibujar el "42" y solo avisa.
- `GameEngine` debe capturar `MazeLoaderError` y mostrar un mensaje legible.

## Decisiones por tomar (anotar en DECISIONS.md al decidirlas)

- `MIN_LEVEL_SIZE` (ahora 3, provisional). Propuesta: 14x10, lo mínimo que
  admite el "42". Con tamaños como (2, 2) o (3, 3) el generador no falla pero
  salen laberintos inservibles.
- Mínimo de 10 niveles: ¿completar con defaults si el config trae menos?
- ¿Hace falta una clave `pacgum` en el config (el subject sugiere `pacgum : 42`)?
- Tamaño de ventana frente al laberinto: 20x10 celdas del generador son 41x21
  casillas (1312x672 px a 32 px/casilla), más que la ventana de 960x640.
  Calcular casilla y ventana desde el nivel (Día 5, con el Renderer).
- ¿Los 4 fantasmas se comportan igual o cada uno con su estilo? (Día 7)
- El `Player` sobrevive entre niveles pero cada nivel tiene un `Maze` distinto:
  hace falta una forma de darle el laberinto en cada nivel (al hacer `GameState`).
- `DIRECTION_DELTAS[Direction.NONE]` debe valer `(0, 0)`.

## Código de Persona B (UI)

El compañero envió su código por zip. Se integra pieza a pieza, adaptando con
type hints y sin copiar `game_state.py`, `models/player.py`, `main.py` ni
`data/highscores.txt`.

| Pieza | Estado |
|---|---|
| `ui/menu.py` | ✅ Integrado y adaptado (Día 3 B) |
| `input_handler.py` | 🔲 Día 4 B: solo debe traducir teclas a `Direction` |
| `renderer.py` | 🔲 Día 5: reescribir contra las estructuras del core (eje Y: arcade crece hacia arriba, el core hacia abajo) |
| HUD, Game Over, Victoria, Pausa | 🔲 Días 6-8 |

Commits hechos por Sergio con mensaje `feat(ui): ... from teammate` y nota
"entregado por zip, adaptado e integrado por Sergio" en la tarjeta.

## Ensayo de defensa

| Pregunta | Estado |
|---|---|
| ¿Por qué `Pacgum` no hereda de `Entity`? | ⏳ Sin responder |
| ¿Composición vs agregación (GameState con Player y con Ghost)? | ⏳ Sin responder |
| ¿Por qué ConfigLoader nunca lanza excepciones y MazeLoader sí? | ✅ Respondida |
| ¿Por qué Config y ConfigLoader son dos clases? | ✅ Explicada |
| ¿Para qué `_get_int`, `_get_str`, `_get_levels` y `@staticmethod`? | ✅ Explicada |
| ¿Qué es `delta_time` y por qué mover por tiempo y no por píxeles fijos? | 🔄 Explicada, falta contestar con mis palabras |
| ¿Por qué `draw()` del menú ya no recibe ancho y alto? | ⏳ Sin responder |
| `MazeLoader`: ¿qué hace `if not (bits & bit)`? ¿por qué el `try` solo envuelve la creación del generador? | ⏳ Sin responder (tarjeta de repaso, Día 5) |
| ¿Qué es el patrón adaptador y qué significan los bits 1/2/4/8/15? | ⏳ Tarjeta de repaso, Día 5 |
| ¿Por qué `Entity.move` solo cambia la dirección si el movimiento se realiza? | ⏳ Sin responder |

## Pendiente y verificaciones

- Probar arcade en un ordenador de 42 (necesita OpenGL 3.3) y preguntar al
  compañero su versión (`pip show arcade`).
- Lint de todo el repo (`flake8 .` + `mypy . --warn-return-any`), incluyendo
  `tests/`: convertir los scripts útiles en tests de `pytest` y borrar el resto.
  Se deja para el último día.
- Traducir `PROGRESS.md` y `DECISIONS.md` al inglés al final.
- Tarjeta de repaso del `MazeLoader` (etiqueta `ensayar`, Día 5).
- Trabajamos los dos sobre `main`: hacer `git pull` antes de empezar cada día.

## Bloqueos y bugs reales (para el README)

- Errata `pacgmun.py` en el nombre del archivo (y `pacgmun_points` en una
  versión del config).
- `make clean` borraba el entorno virtual; `fclean` habría borrado el `.whl`
  del generador; `make install` no instalaba `mazegenerator`; `make debug` con
  `pbd` en vez de `pdb`.
- `mypy .` revisa también los scripts sueltos de `tests/`.
- Config con `__init__` manual y `frozen=True` → `FrozenInstanceError`.
- El punto de entrada se llamó `main.py`; el subject exige `pac-man.py`.
- Las celdas del "42" (valor 15) salían como casillas de camino aisladas: 18
  pacgums imposibles de comer en un 20x10. Corregido en el `MazeLoader`.
- Centro y esquinas del `Maze` caían en muro tras la expansión 2n+1.
- `Entity.move` cambiaba la dirección aunque chocara con un muro.
- `arcade.draw_text` lanza un `PerformanceWarning` en cada ejecución; se
  sustituyó por objetos `arcade.Text`.