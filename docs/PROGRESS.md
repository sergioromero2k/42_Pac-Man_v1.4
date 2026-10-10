# Progreso — Pac-Man 42

Última actualización: 2026-10-10 (sábado)

## Dónde estamos

Repaso del proyecto desde el Día 1, comprobando cada tarjeta con la salida
real de los comandos. Estado del tablero:

| Día | Tarjeta | Estado |
|---|---|---|
| 1 | Contratos y stubs con type hints | ✅ Done |
| 1 | Setup del repo (Makefile, flake8, mypy, .gitignore, venv) | ✅ Done |
| 1 | PROGRESS.md y DECISIONS.md | ✅ Done |
| 2 | A: Config + ConfigLoader | 🔄 In Progress |
| 2 | B: Ventana pygame con grid de prueba | 🔲 Por revisar (hay `tests/6_test_pygame.py`) |
| 2 | B: Game loop con delta time | 🔲 Por revisar |
| 3-20 | Resto de tarjetas | 🔲 Backlog (ver tablero) |

## Hecho hoy

- **Día 1 cerrado.** `mypy --strict core/` solo falla en `highscore.py`
  (módulo a medias, se arregla al escribirlo).
- Renombrado `pacgmun.py` → `pacgum.py` (errata).
- Makefile corregido:
  - `debug` usaba `pbd` → ahora `pdb`.
  - `clean` borraba el `venv` → separado en `clean`, `clean_venv` y `fclean`.
  - Quitado `rm -rf *.whl` de `fclean` (borraba el `.whl` del generador).
  - `install` ahora instala `mazegenerator-2.1.0-py3-none-any.whl`.
- `main.py` mínimo creado (carga el config e imprime vidas y niveles).
- Commit con todo lo anterior + `PROGRESS.md`.
- Git: configurado el paginador (`core.pager "less -FRX"`).
- **Día 2 A:** revisado `ConfigLoader` contra el subject (V.1, V.2, V.3).
  `levels` ya estaba arreglado. Se propuso una versión nueva con
  `_get_int`, `_get_str` y `_get_levels`.

## Pendiente inmediato (Día 2 A)

- [ ] Aplicar la nueva versión de `core/config_loader.py` (si no está ya).
- [ ] Probar 4 casos: raíz JSON que no es objeto, valores inválidos,
      archivo correcto con comentarios y clave desconocida, archivo ausente.
- [ ] `make lint` sin avisos en `config_loader.py`.
- [ ] Añadir a `docs/DECISIONS.md`: separación Config/ConfigLoader,
      ConfigLoader no lanza excepciones y MazeLoader sí, y por qué existen
      los ayudantes `_get_*`.
- [ ] Commit y push. Si todo cuadra, tarjeta A → Done.

## Hallazgos del subject (a tener en cuenta)

- **Punto de entrada:** debe llamarse `pac-man.py` y recibir **exactamente
  un argumento** (el config). Cualquier fallo → mensaje claro, nunca
  traceback. Hoy tenemos `main.py`: renombrar y actualizar `ENTRY_POINT`
  del Makefile (`run` debe pasar `config.json`).
- **V.3:** valor ausente o inválido → default, mensaje claro y continuar.
  Claves desconocidas se ignoran.
- El config **se modificará durante la defensa**: la validación importa.
- `mazegenerator` solo fija la semilla si `seed > 0`; con 0 el nivel 1
  sería aleatorio. Por eso `seed` tiene mínimo 1.
- Con menos de 14×10 el generador no puede dibujar el "42" y solo avisa.
- `GameEngine` debe capturar `MazeLoaderError` y mostrar un mensaje legible.

## Decisiones por tomar (anotar en DECISIONS.md al decidirlas)

- Formato de `levels`: ahora `[[ancho, alto], ...]`. Documentar el orden en
  el README.
- Mínimo de 10 niveles: ¿completar con defaults si el config trae menos?
- Tamaño mínimo de maze (`MIN_LEVEL_SIZE = 3` es provisional; probar con
  el generador).
- ¿Hace falta una clave `pacgum` (el subject sugiere `pacgum : 42`)?
- ¿Los 4 fantasmas se comportan igual o cada uno con su estilo? (Día 7)

## Código de Persona B (UI)

- El compañero ya envió su código por zip. Todavía **no está integrado**.
- Plan: descomprimirlo en una carpeta aparte, revisarlo y copiarlo a `ui/`.
  Commit hecho por Sergio: `feat(ui): add <módulo> from teammate`, y anotar
  en la tarjeta "entregado por zip, integrado por Sergio".
- Al revisarlo, comprobar: eje Y hacia abajo, uso del enum `Direction`,
  y que el Renderer lea los datos del core como se acordó en el Sync del Día 5.
- Ya existe `tests/6_test_pygame.py` (ventana + game loop) para las
  tarjetas B del Día 2.

## Próximos pasos (mañana)

1. Cerrar el Día 2 A (ver "Pendiente inmediato").
2. Renombrar `main.py` → `pac-man.py` con un único argumento
   (`sys.argv`) y actualizar el Makefile.
3. Revisar `tests/6_test_pygame.py` y las tarjetas B del Día 2.
4. Descomprimir y revisar el zip del compañero.
5. Día 3: repaso de `MazeLoader` y `MenuView`.
6. Después: `HighScoreManager`, `CheatManager`, `GameState`, `GameEngine`.

## Ensayo de defensa

| Pregunta | Estado |
|---|---|
| ¿Por qué `Pacgum` no hereda de `Entity`? | ⏳ Sin responder |
| ¿Composición vs agregación (GameState con Player y con Ghost)? | ⏳ Sin responder |
| ¿Por qué ConfigLoader nunca lanza excepciones y MazeLoader sí? | ✅ Respondida y corregida |
| ¿Por qué Config y ConfigLoader son dos clases? | ✅ Explicada |
| ¿Para qué `_get_int`, `_get_str`, `_get_levels` y `@staticmethod`? | ✅ Explicada |
| ¿Qué es `delta_time` y por qué mover por tiempo y no por píxeles fijos? | ⏳ Sin responder |

## Bloqueos y bugs reales (para el README)

- Errata `pacgmun.py` en el nombre del archivo (y `pacgmun_points` en una
  versión del config).
- `make clean` borraba el entorno virtual.
- `fclean` habría borrado el `.whl` del generador.
- `make install` no instalaba `mazegenerator`.
- `make debug` con `pbd` en vez de `pdb`.
- `mypy .` revisaba también los scripts sueltos de `tests/`.