## Config
---

Se instancia 1vez, al arrancar el programa, esto es puramente estructura de datos, sin métodos.
Lee el JSON y os devuelve el objeto Config ya construido, ese objeto ese queda en GameEngine durante toda la vida de la aplicación, consultadonlo cada vez que necesita un valor. Un JSON externo porque el juego nos pide que sea configurable (números de vidas puntos por cada cosa, tamaños de niveles, etc), sin tener que tocar código para cambiar esos valores. Config es la representación, ya en memoria y ya validada, de todos esos parámetros.

* `lives` vidas iniciales del jugador(por defecto 3).
* `pacgmun_points` puntos que suma comer una pacgmun normal.
* `super_pacgmun_points` puntos que suma comer una super-pacgmun.
* `ghost_points` puntas que suma comer un fantasma en modo frightened.
* `seed` la semilla para el generador de laberintos, usada para que el 1er nivel sea siempre el mismo maze.
* `max_time` segundos limite por nivel, el valor de partida para tiempoRestanteNivel en cada GameState nuevo.
* `levels` la lista de tamaños de maze, uno por nivel (width, height) sueltos, precisamente para soportar múltiples niveles con tamaños distintos.
* `high_score_filename` la ruta del JSON donde se guarda el ranking que le pasareís a HighscoreManager.