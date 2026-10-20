# Decisiones de diseño - Pac-Man 42

Apuntes por día: qué se decidió, por qué, y qué se descartó. Sirve también como
repaso para la defensa.

| Día | Tema |
|---|---|
| 1 | Contratos y setup del repo |
| 2 | Config, ConfigLoader, arcade, game loop y `delta_time` |
| 3 | Maze, MazeLoader y menú |
| 4 | Entity y Player (en curso) |
| — | Decisiones abiertas |

---

# Día 1 — Contratos y setup

## Contratos primero, con type hints
- Antes de escribir lógica se definieron las clases como *stubs* con type hints
  (qué métodos tiene cada una y qué devuelven). Así los dos (core y UI) trabajan
  contra el mismo contrato.
- `make lint` ejecuta `flake8 .` y `mypy . --warn-return-any` sobre **todo el
  repo**, incluido `tests/`. Los scripts sueltos de `tests/` darán avisos y
  habrá que convertirlos en tests de `pytest` o borrarlos al final.

## Makefile
- `clean` borra solo cachés; `clean_venv` borra el entorno virtual; `fclean`
  hace las dos cosas. Antes `clean` borraba el `venv` sin querer.
- `fclean` no borra el `.whl` del generador (es parte del proyecto).
- `install` instala `flake8`, `mypy`, el `.whl` de `mazegenerator` y `arcade==3.3.3`.

---

# Día 2 — Config, ConfigLoader y ventana

## Config y ConfigLoader: dos clases separadas
- `Config` solo guarda los **8 valores del juego** (vidas, puntos, semilla, tiempo máximo, niveles, fichero de highscore). No sabe de dónde vienen.
- `ConfigLoader` lee el archivo, quita los comentarios `#`, valida cada valor y construye un `Config`. No guarda estado.
- **Motivo (responsabilidad única)**: el resto del juego depende solo de `Config` y no sabe que existe un **JSON**. Si cambia el formato del archivo, solo se toca `ConfigLoader`.
- Los valores por defecto (`DEFAULT_*`) viven en `ConfigLoader`, no en `Config`: decidir qué hacer ante un archivo roto es lógica de lectura, no de datos.
- `Config` es un `@dataclass(frozen=True)`: los valores validados no se pueden modificar tras crearse. Los datos que cambian durante la partida (como las vidas) viven en `Player`, no en `Config`.
- Con `@dataclass`, Python genera el `__init__` a partir de los campos tipados. Si se deja un `__init__` escrito a mano junto a `frozen=True`, da `FrozenInstanceError`: hay que borrarlo.
- `frozen` impide reasignar un campo, pero no modifica por dentro una lista (`levels`).

## ConfigLoader nunca lanza excepciones; MazeLoader sí
- **ConfigLoader:** si el archivo falta, está roto o un valor es inválido, avisa con `[Warning] ...`, usa el valor por defecto y **continúa**. Siempre devuelve un `Config`.
- **MazeLoader:** si el generador falla, lanza `MazeLoaderError`.
- **Motivo:** el subject (V.3) pide valor por defecto, mensaje claro y continuar. En cambio, no existe un laberinto de respaldo (no se puede escribir un generador propio), así que no hay nada razonable con lo que seguir.
- El `GameEngine` captura `MazeLoaderError` y muestra un mensaje legible. Una excepción no es lo mismo que un traceback.

## Valores por defecto y mínimos de validación
| Clave | Por defecto | Mínimo | Por qué |
|---|---:|---:|---|
| `lives` | 3 | 1 | Con 0 vidas la partida acabaría antes de empezar |
| `pacgum_points` | 10 | 0 | Los puntos no pueden ser negativos |
| `super_pacgum_points` | 50 | 0 | Igual |
| `ghost_points` | 200 | 0 | Igual |
| `seed` | 42 | 1 | `mazegenerator` solo fija la semilla si `seed > 0`; con 0 el nivel 1 sería aleatorio |
| `max_time` | 90 | 1 | Con 0 se perdería al instante |
| `levels` | `[(20, 10)] * 10` | `MIN_LEVEL_SIZE` (3, provisional) | El subject pide al menos 10 niveles |
| `highscore_filename` | `data/highscore.json` | — | — |

- `bool` es subclase de `int` en Python: `true` en el JSON no debe aceptarse como entero.
- Las claves desconocidas se ignoran (lo pide el subject).
- El config **se modificará durante la defensa**, por eso la validación importa.

## Ayudantes `_get_int`, `_get_str` y `_get_levels`
- **Decisión:** la lectura de cada clave pasa por un ayudante con su valor por defecto y su mínimo.
- **Motivo (DRY):** la validación vive en un solo sitio. Añadir una clave nueva (por ejemplo `bonus_time`) son tres cambios: un campo en `Config`, una constante `DEFAULT_` y una llamada a `_get_int`.
- `@staticmethod`: método que vive dentro de la clase pero no usa `self`. Se llama como `ConfigLoader.load_config(...)` sin crear un objeto.

## Librería gráfica: arcade
- Elegida arcade (el subject permite "MLX or similar"). La UI del compañero ya está hecha con ella, y `arcade.View` encaja con la jerarquía de vistas del UML.
- Descartada pygame: habría obligado a reescribir las pantallas ya hechas.
- Versión fijada: `arcade==3.3.3`.
- Riesgo asumido: arcade necesita OpenGL 3.3 (depende de la GPU y los drivers, no se descarga). Pendiente de probar en un ordenador de 42.

```sh
python3 -m venv venv
source venv/bin/activate
pip install arcade==3.3.3
python -c "import arcade; print(arcade.__version__); w = arcade.Window(300, 200, 'test'); print('ok'); w.close()"
```

## Punto de entrada `pac-man.py` con exactamente un argumento
- **Decisión:** `python3 pac-man.py <config.json>`. Con otro número de argumentos muestra el uso y termina, sin traceback.
- **Motivo:** lo exige el subject. Antes se llamaba `main.py`.

## Vocabulario del game loop
| Término | Qué es | Ejemplo |
|---|---|---|
| Píxel | Un punto de la pantalla | Tu ventana mide 960 × 640 píxeles |
| Celda (tile) | Un cuadrado del laberinto, de 32 × 32 píxeles | 960 / 32 = 30 columnas y 640 / 32 = 20 filas |
| Hz | Veces por segundo que el monitor redibuja la imagen | 60 Hz = 60 veces por segundo |
| FPS | Veces por segundo que tu programa dibuja un frame | Normalmente igual a los Hz del monitor |
| Frame | Una vuelta completa del bucle: actualizar y dibujar | A 60 FPS, un frame dura unos 0,0167 s |
| delta_time | Los segundos que pasaron desde el frame anterior | A 60 FPS vale aproximadamente 0,0167 s |

## El game loop
En cada frame, el motor hace 3 cosas, siempre en este orden:
* **Eventos:** ¿se ha pulsado una tecla? En arcade es `on_key_press`.
* **Update:** cambiar el estado del juego (posiciones, vidas, tiempo) en `on_update(delta_time)`.
* **Draw:** pintar el estado actual en `on_draw`.

Update decide qué pasa y draw solo lo pinta: nada se mueve dentro de `on_draw`.

## El movimiento se calcula con `delta_time`
- **Decisión:** `on_update(delta_time)` mueve con `velocidad * delta_time` (píxeles por segundo), no con píxeles fijos por frame.
- **Motivo:** la velocidad no depende de la tasa de refresco (60 Hz o 144 Hz). Regla: distancia = velocidad × tiempo.
- **Descartado:** mover por frame o por pulsación (lo que hacía el prototipo del
  compañero en `input_handler.py`).

### Por qué `delta_time`
Tu cuadrado va a 160 píxeles por segundo. Compara los 2 métodos.

| FPS | Con `delta_time` (160 × dt) | Fijo de 3 px por frame |
|---:|---|---:|
| 30 | 5,33 px/frame → **160 px/s** | 90 px/s |
| 60 | 2,67 px/frame → **160 px/s** | 180 px/s |
| 144 | 1,11 px/frame → **160 px/s** | 432 px/s |

La línea clave de la ventana de prueba:
```python
self.marker_x = (self.marker_x + MARKER_SPEED * delta_time) % WINDOW_WIDTH
```
- `MARKER_SPEED * delta_time` es lo que avanza en este frame.
- El `%` devuelve el resto de dividir entre el ancho: al salir por la derecha reaparece por la izquierda.

---

# Día 3 — Maze, MazeLoader y menú

## Maze
* `self` - Hace referencia al propio objeto.
* `walls` - Conjunto de coordenadas de las paredes.
* `paths` - Conjunto de coordenadas de los caminos transitables.
* `maze_width` - Ancho del laberinto (en casillas).
* `maze_height` - Alto del laberinto (en casillas).
------------------------------------------------------------------------------------------------------------
* `is_wall(pos)`: comprueba si una posición es una pared.
* `is_path(pos)`: comprueba si una posición es transitable.
* `get_center_position()`: devuelve la casilla transitable más cercana al centro.
* `get_corners()`: devuelve las casillas transitables más cercanas a las cuatro esquinas.
**La idea principal:** esta clase no crea ni resuelve el laberinto por sí misma. Almacena su estructura y proporciona métodos para consultar sus posiciones.

### Bug corregido: puntos de aparición en muro (Día 4)
- Tras la expansión 2n+1 las casillas de camino están en coordenadas impares y el borde exterior es siempre muro. Calcular el centro (`ancho // 2`, `alto // 2`) y las esquinas como en una cuadrícula normal daba **muro**: en un 20x10 (41x21 casillas) las 4 esquinas y el centro `(20, 10)` eran muro.
- **Decisión:** un ayudante `_nearest_path(target)` devuelve la casilla de `paths` más cercana (distancia Manhattan, con desempate fijo para que sea siempre la misma). Se usa para el centro y para las esquinas.
- Resultado: el centro del 20x10 con semilla 42 pasa de `(20, 10)` (muro) a `(19, 10)` (camino).
- El "42" ocupa el centro del laberinto: por eso se busca el camino **más cercano** y no un punto exacto.

## MazeLoader
`MazeLoader` adapta el laberinto generado por la librería externa `mazegenerator` al formato utilizado por el proyecto mediante la clase `Maze`.

Es un **adaptador**: el juego pide lo que necesita y el loader traduce a la interfaz del generador, que no se puede modificar (el subject, V.4, dice que el loader se adapta al paquete y no al revés).

El proceso consiste en:
1. Generar el laberinto (siempre con `perfect=False`, que quita los callejones sin salida y es lo que necesita Pac-Man).
2. Interpretar las conexiones mediante bits.
3. Convertir las habitaciones y conexiones en coordenadas.
4. Separar paredes (`walls`) y caminos (`paths`).
5. Crear y devolver el objeto `Maze`.

### Seed (semilla)
La `seed` es un número entero que controla la generación pseudoaleatoria del laberinto.
```python
maze_gen = MazeGenerator(size=size, perfect=False, seed=seed)
```
**Decisión:** permitir que la generación sea reproducible utilizando una semilla.
- La misma semilla y los mismos parámetros permiten obtener el mismo laberinto si el generador es determinista.
- Semillas diferentes pueden producir laberintos diferentes.
- Es útil para depurar errores, realizar pruebas y reproducir laberintos concretos.
La reproducibilidad exacta también puede depender de la versión de la librería y de su implementación.

**Comprobado con `mazegenerator 2.1.0`:**
- Misma semilla (42) dos veces → laberinto idéntico.
- `seed=0` → aleatorio (el generador solo fija la semilla si `seed > 0`).
- Según el subject, el nivel 1 usa una semilla fija (la del config) y los siguientes se generan aleatorios (`seed=0`).

## Representación de conexiones mediante bits
La librería representa las conexiones de cada habitación mediante un número entero. Cada bit corresponde a una dirección.
```python
BIT_DELTAS = [
    (1, 0, -1),   # Arriba
    (2, 1, 0),    # Derecha
    (4, 0, 1),    # Abajo
    (8, -1, 0)    # Izquierda
]
```
Cada tupla tiene el formato:

`(bit, dx, dy)`

- `bit`: identifica la dirección que se quiere comprobar.
- `dx`: desplazamiento horizontal.
- `dy`: desplazamiento vertical.

| Dirección | Bit | Binario | dx | dy |
|---|---:|---|---:|---:|
| Arriba | 1 | `0001` | 0 | -1 |
| Derecha | 2 | `0010` | 1 | 0 |
| Abajo | 4 | `0100` | 0 | 1 |
| Izquierda | 8 | `1000` | -1 | 0 |

Se utilizan potencias de 2 para que cada dirección tenga un bit independiente. Esto permite combinar varias direcciones en un único entero sin perder información.

### Interpretación de las conexiones

El código utiliza:

```python
if not (bits & bit):
    neighbor = (cx + dx, cy + dy)
    paths.add(neighbor)
    walls.discard(neighbor)
```
La condición `not (bits & bit)` se cumple cuando el bit está desactivado.
Convención **verificada en el código del generador** (`mazegenerator 2.1.0`):
- Bit activado = **hay muro** en ese lado. Por ejemplo, la fila de arriba del laberinto vacío vale `1` (muro al norte) y la columna izquierda `8` (muro al oeste).
- Bit desactivado = no hay muro: se abre la conexión.

### La celda `15` es el "42"
- `15 = 1 + 2 + 4 + 8`: los cuatro muros cerrados. El generador marca así las celdas que forman el "42".
- **Decisión:** el loader salta esas celdas (`if bits == 15: continue`), de modo que son muro sólido.
- **Por qué importa:** antes del arreglo se añadía su centro a `paths` aunque estuviera rodeado de muros. En un 20x10 salían 426 casillas de camino en vez de 408: **18 casillas aisladas** dentro del "42", imposibles de alcanzar. Si ahí se colocaran pacgums, el nivel no se podría ganar.
- Comprobación: con el arreglo, el 100 % de los caminos están conectados (408 de 408).

## Desplazamientos `dx` y `dy`
Los bits identifican qué dirección se comprueba, mientras que `dx` y `dy` permiten calcular la coordenada vecina.
```python
neighbor = (cx + dx, cy + dy)
```
Por ejemplo, si la posición actual es `(3, 3)` y se comprueba la derecha:

```python
dx = 1
dy = 0
neighbor = (3 + 1, 3 + 0)  # (4, 3)
```
Los desplazamientos utilizados son:
- Arriba: `(0, -1)`.
- Derecha: `(1, 0)`.
- Abajo: `(0, 1)`.
- Izquierda: `(-1, 0)`.
En esta representación, el eje vertical aumenta hacia abajo (igual que `Direction`). Ojo: en **arcade** el eje Y crece hacia arriba, y alguien tiene que convertir entre los dos (`Renderer.grid_to_pixel`).

## Conversión de habitaciones a cuadrícula
El **generador trabaja con habitaciones**, mientras que el proyecto utiliza una cuadrícula que también contiene las posiciones de las conexiones.
Por ello, las dimensiones finales se calculan así:
```python
final_width = room_width * 2 + 1
final_height = room_height * 2 + 1
```
Las coordenadas de cada habitación se calculan mediante:
```python
cx = 2 * rx + 1
cy = 2 * ry + 1
```

Las habitaciones quedan en coordenadas impares y las posiciones intermedias representan las conexiones.
Por ejemplo, una habitación situada en `(0, 0)` se coloca en `(1, 1)` en la cuadrícula final.

Ejemplo mínimo: una fila de 2 habitaciones conectadas (`#` muro, `.` camino):
```
#  #  #  #  #
#  .  .  .  #      habitación A = columna 1, hueco = columna 2, habitación B = columna 3
#  #  #  #  #
```
- El borde exterior (fila 0, columna 0 y última) siempre es muro.
- Los huecos entre habitaciones están en coordenadas pares; si no hay muro entre dos habitaciones, el hueco pasa a ser camino.

**Consecuencia importante:** un 20x10 de habitaciones son **41x21 casillas** (1312x672 px a 32 px por casilla), más grande que la ventana actual de 960x640. El tamaño de casilla y de ventana tendrá que calcularse desde el nivel (Día 5, con el Renderer).

## Paredes y caminos
Se utilizan dos conjuntos de coordenadas:

```python
walls = {(x, y) for x in range(final_width)
         for y in range(final_height)}

paths: set[tuple[int, int]] = set()
```

**Decisión:** inicializar todas las posiciones como paredes y eliminar las que deban ser transitables.
Para cada habitación:
```python
paths.add((cx, cy))
walls.discard((cx, cy))
```

Para cada conexión abierta:

```python
paths.add(neighbor)
walls.discard(neighbor)
```

Así, las habitaciones y conexiones abiertas pasan a formar parte de `paths`, mientras que las posiciones restantes permanecen en `walls`.

`discard()` se utiliza para eliminar una coordenada sin provocar un error si no existe en el conjunto.

## Fallos del generador: `MazeLoaderError`
- El `try` envuelve **solo la creación del `MazeGenerator`**: ahí es donde el generador puede fallar (por ejemplo con tamaño `(0, 0)`, `(-1, 5)` o `(20, 0)`), y cualquier excepción sale como `MazeLoaderError`.
- Se encadena con `raise ... from e` para conservar la causa original (sin eso el traceback dice "durante el manejo de la excepción anterior ocurrió otra", que confunde).
- Si el resultado no tiene ningún camino (`if not paths`), también lanza `MazeLoaderError`. Pasa, por ejemplo, con tamaño `(1, 1)`.
- Con menos de **14x10** habitaciones el generador no puede dibujar el "42": solo imprime un aviso y sigue. Con tamaños como `(2, 2)` o `(3, 3)` no falla, pero el laberinto es inservible con 4 fantasmas en las esquinas (ver decisiones abiertas).

## Menú (Día 3 B)
- `MainMenu` es una clase simple (opciones, opción seleccionada y dibujo). Por ahora no es un `arcade.View`: se convertirá cuando se integre la clase base `View` del UML.
- **Cambios respecto al código del compañero:**
  - `arcade.draw_text` → objetos `arcade.Text` creados una vez. `draw_text` lanza un `PerformanceWarning` ("extremely slow") en cada ejecución.
  - El constructor recibe `(width, height)` y las posiciones se calculan **una sola vez**; por eso `draw()` ya no necesita parámetros.
  - Type hints y constantes (`OPTIONS`, colores, tamaños).
  - `move_up` / `move_down` con `%` para dar la vuelta.
- La tarjeta pedía una pantalla estática; las teclas (↑ ↓ ENTER) son un extra del diseño del compañero y por ahora solo imprimen la opción elegida.

---

# Día 4 — Entity y Player (en curso)

## Entity
`Entity` **representa a cualquier entidad** que se mueve dentro de un laberinto, por ejemplo, el jugador o un enemigo. Permite moverla, consultar su posición, obtener su sprite y devolverla a su posición inicial (`spawn_position`).
* **Direction** es un `Enum` que representa las direcciones posibles, como `UP`, `DOWN`, `LEFT`, `RIGHT` y `NONE`.
* **DIRECTION_DELTAS**: es un diccionario que indica cuánto cambia la posición al moverse en cada dirección. `NONE` debe valer `(0, 0)`, si no, `move(Direction.NONE)` da `KeyError`.
* **Maze**: es la clase que representa el laberinto.

### `Entity.move` solo cambia la dirección si el movimiento se realiza
- **Problema:** si la dirección se asigna antes de comprobar el muro, al pulsar "izquierda" con un muro a la izquierda Pac-Man se queda parado mirando al muro, en vez de seguir en la dirección que llevaba.
- **Decisión:** `current_direction = direction` va **dentro del `if`** (solo si `is_path(destino)`).

## Player: dirección deseada y dirección actual
Pac-Man guarda la dirección que **quiere** (`desired_direction`, lo que pulsó el jugador) y la que **lleva** (`current_direction`). En cada paso:
1. Intenta ir en la dirección deseada. Si no hay muro, gira.
2. Si no puede, sigue en la que llevaba.
3. Si tampoco puede, se queda parado.

Es una pequeña **máquina de estados**: un objeto está en un estado y solo cambia con transiciones definidas, sin cascadas de `if` sueltos.

El teclado no mueve a Pac-Man directamente: el handler traduce una pulsación a una *intención* y la lógica del core decide si se puede cumplir.

## Movimiento por casillas y por tiempo
- El movimiento es por **casillas**, no por píxeles: Pac-Man avanza una casilla cada `1 / speed` segundos (`speed` en casillas por segundo, 8 por defecto).
- `update(delta_time)` acumula el tiempo transcurrido y da tantos pasos como quepan. Es el mismo principio del Día 2 (velocidad × tiempo): a 30, 60 o 144 FPS se recorre la misma distancia por segundo (comprobado: 9 casillas en 2 s en los tres casos).
- `min(delta_time, 0.1)`: limita el tiempo por frame para que un tirón (arrastrar la ventana, un lag) no le haga saltar varias casillas de golpe.
- `Player.respawn()` también borra `desired_direction` y el acumulador; si no, tras perder una vida Pac-Man reanudaría solo la última tecla pulsada.

## Comprobación
- 20.000 pasos con teclas aleatorias: **0 entradas en un muro**.
- `respawn_at_maze_center()` coloca al jugador en un camino (`(19, 10)` en el 20x10 con semilla 42).

---

# Decisiones abiertas

| Decisión | Propuesta | Cuándo |
|---|---|---|
| `MIN_LEVEL_SIZE` (hoy 3, provisional) | 14x10, lo mínimo en que cabe el "42" | Día 5 |
| Menos de 10 niveles en el config | Completar con valores por defecto y avisar | Pendiente |
| ¿Clave `pacgum` en el config? (el subject sugiere `pacgum : 42`) | Revisar el subject | Pendiente |
| Tamaño de ventana y de casilla según el nivel | Calcular desde las dimensiones del nivel | Día 5 (Renderer) |
| Fantasmas: ¿todos iguales o cada uno con su estilo? | Cada uno con su objetivo | Día 7 |
| `Player` vive entre niveles pero cada nivel tiene un `Maze` distinto | Darle el laberinto en cada nivel (al hacer `GameState`) | Día 9 o antes |
| Convertir `MainMenu` en `arcade.View` | Con la clase base `View` | Día 5 |