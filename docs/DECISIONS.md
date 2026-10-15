# Decisiones de diseño - Pac-Man 42
---

## Config y ConfigLoader: dos clases separadas
- `Config` solo guarda los **8 valores del juego** (vidas, puntos, semilla, tiempo máximo, niveles, fichero de highscore). No sabe de dónde vienen.
- `ConfigLoader` lee el archivo, quita los comentarios `#`, valida cada valor y construye un `Config`. No guarda estado.
- **Motivo (responsabilidad única)**: el resto del juego depende solo de `Config` y no sabe que existe un **JSON**. Si cambia el formato del archivo, solo se toca `ConfigLoader`.
- Los valores por defecto (`DEFAULT_*`) viven en `ConfigLoader`, no en `Config`: decidir qué hacer ante un archivo roto es lógica de lectura, no de datos.
- `Config` es un `@dataclass(frozen=True)`: los valores validados no se pueden modificar tras crearse. Los datos que cambian durante la partida (como las vidas) viven en `Player`, no en `Config`.

## Librería gráfica: arcade
- Elegida arcade (el subject permite "MLX or similar"). La UI del compañero ya está hecha con ella, y `arcade.View` encaja con la jerarquía de vistas del UML.
- Descartada pygame: habría obligado a reescribir las pantallas ya hechas.
- Riesgo asumido: arcade necesita OpenGL 3.3. Pendiente de probar en el ordenador donde se hará la defensa.

```sh
python3 -m venv venv
source venv/bin/activate
pip install arcade
python -c "import arcade; print(arcade.__version__); w = arcade.Window(300, 200, 'test'); print('ok'); w.close()"
```

### D-10 El movimiento se calcula con `delta_time`
- **Decisión:** `on_update(delta_time)` mueve con `velocidad * delta_time` (píxeles por segundo), no con píxeles fijos por frame.
- **Motivo:** la velocidad no depende de la tasa de refresco (60 Hz o 144 Hz).
- **Descartado:** mover por frame o por pulsación (lo que hacía el prototipo del
  compañero en `input_handler.py`).

### D-11 Punto de entrada `pac-man.py` con exactamente un argumento
- **Decisión:** `python3 pac-man.py <config.json>`. Con otro número de argumentos muestra el uso y termina, sin traceback.
- **Motivo:** lo exige el subject.

| Término | Qué es | Ejemplo |
|---|---|---|
| Píxel | Un punto de la pantalla | Tu ventana mide 960 × 640 píxeles |
| Celda (tile) | Un cuadrado del laberinto, de 32 × 32 píxeles | 960 / 32 = 30 columnas y 640 / 32 = 20 filas |
| Hz | Veces por segundo que el monitor redibuja la imagen | 60 Hz = 60 veces por segundo |
| FPS | Veces por segundo que tu programa dibuja un frame | Normalmente igual a los Hz del monitor |
| Frame | Una vuelta completa del bucle: actualizar y dibujar | A 60 FPS, un frame dura unos 0,0167 s |
| delta_time | Los segundos que pasaron desde el frame anterior | A 60 FPS vale aproximadamente 0,0167 s |


### El game loop
En cada frame, el motor hace 3 cosas, siempre en este orden:
* **Eventos:** ¿se ha pulsado una tecla? En arcade es `on_key_press`.
* **Update:** cambiar el estado del juego (posiciones, vidas, tiempo) en on_update(delta_time).
* **Draw:** pintar el estado actual en `on_draw`.

### Por qué `delta_time`
Tu cuadrado va a 160 píxeles por segundo. Compara los 2 métodos.
| FPS | Con `delta_time` (160 × dt) | Fijo de 3 px por frame |
|---:|---|---:|
| 30 | 5,33 px/frame → **160 px/s** | 90 px/s |
| 60 | 2,67 px/frame → **160 px/s** | 180 px/s |
| 144 | 1,11 px/frame → **160 px/s** | 432 px/s |

## MazeLoader
`MazeLoader` adapta el laberinto generado por la librería externa `mazegenerator` al formato utilizado por el proyecto mediante la clase `Maze`.
El proceso consiste en:
1. Generar el laberinto.
2. Interpretar las conexiones mediante bits.
3. Convertir las habitaciones y conexiones en coordenadas.
4. Separar paredes (`walls`) y caminos (`paths`).
5. Crear y devolver el objeto `Maze`.

### 1. Seed (semilla)
La `seed` es un número entero que controla la generación pseudoaleatoria del laberinto.
```python
maze_gen = MazeGenerator(size=size, perfect=False, seed=seed)
```
**Decisión:** permitir que la generación sea reproducible utilizando una semilla.
- La misma semilla y los mismos parámetros permiten obtener el mismo laberinto si el generador es determinista.
- Semillas diferentes pueden producir laberintos diferentes.
- Es útil para depurar errores, realizar pruebas y reproducir laberintos concretos.
La reproducibilidad exacta también puede depender de la versión de la librería y de su implementación.

## 2. Representación de conexiones mediante bits
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

### 3. Interpretación de las conexiones

El código utiliza:

```python
if not (bits & bit):
    neighbor = (cx + dx, cy + dy)
    paths.add(neighbor)
    walls.discard(neighbor)
```
La condición `not (bits & bit)` se cumple cuando el bit está desactivado.
Según la convención asumida por este código:
- Bit desactivado: se abre la conexión.
- Bit activado: no se abre la conexión en ese bloque.
Esta convención debe coincidir con la implementación de la librería externa y no debe darse por supuesta sin verificarla.

## 4. Desplazamientos `dx` y `dy`
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
En esta representación, el eje vertical aumenta hacia abajo.

## 5. Conversión de habitaciones a cuadrícula
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

## 6. Paredes y caminos
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

## 7. Gestión de errores

```python
class MazeLoaderError(Exception):
    """Raised when the external maze generator fails."""
```

Se define una excepción personalizada para identificar errores de generación.

```python
try:
    maze_gen = MazeGenerator(size=size, perfect=False, seed=seed)
except Exception as e:
    raise MazeLoaderError(f"Maze generation failed: {e}")
```

Esto permite presentar los errores del generador mediante una excepción propia del proyecto. El bloque `try` solo cubre la creación del generador, no las operaciones posteriores.

## 8. Resultado final

```python
return Maze(walls, paths, final_width, final_height)
```

Se devuelve un objeto `Maze` con:
- Las coordenadas de las paredes.
- Las coordenadas de los caminos.
- El ancho de la cuadrícula.
- El alto de la cuadrícula.

