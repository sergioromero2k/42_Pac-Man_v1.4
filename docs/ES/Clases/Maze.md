## Maze
---
Se instancia 1ez por nivel.
Es **donde vive todas las preguntas relacionadas con la forma del laberinto**: qué casillas son pared, cuáles son transitables, y algunos puntos especiales(centro, esquinas) que varias otras clases necesitan consultar constantemente. Recuerda que MazeLoader es el unico que toca el formato ajeno (`A-Maze-ing`), lo demás en vuestro código solo conoce esta clase Maze.

* `walls`  todas las coordenadas del grid que son pared. (set por rendimiento) .
* `maze_width` / `maze_height` las dimensiones totales del laberinto de ese nivel.
* `is_wall` metodo mas usado de esta clase, compriueba si una coordnenada concreta está en el paredes -> Lo llama Entity.moverse cada vez que una entidad intenta deplazarse.
* `is_path` necesita saber por donde puede expandirse a la hora de calcular su proximo paso, lo opuesto a pared.
* `get_center_position()` calcula y devuelve la casilla central del maze, la usa GameState al arrancar el nivel para saber donde colocar el spawn del Player.
* `get_corners()` calcula y devuelve las 4 esquinas, los usa GameState para colocar el spawn de los 4 Ghost y las 4 SuperPacgmun.
