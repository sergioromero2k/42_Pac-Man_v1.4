## Entity
---

* `current_position` donde esta la entidad ahora mismo, como coordenada (fila, columna) dentro del grid del laberinto.
* `current_direction`: hacia qué dirección se está moviendo o mirando ahora mismo.
* `sprite_id`: Un identificador (no la imagen en sí) de qué apariencia visual le corresponde.
* `maze_reference` una referencia al objeto `Maze` actual.
* `spawn_position` posición fija donde nace la entidad.

* `move()`:
* `get_position()`: devuelve la posición actual. Lo usa, sobretodo, GameState para comprobar colisiones entre entidades.
* `get_sprite()`: devuelve el identificador de sprite actual. Este es el punto de conexión con el renderer.
* `respawn()`:  devuelve la entidad a su posSpawn, y probablemente resetea a dirActual a parado.