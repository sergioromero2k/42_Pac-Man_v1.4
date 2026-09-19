## Pacgmun
---
Es la representación del coleccionable básico del juego **(las bolitas que Pac-Man va comiendo)**. 
No necesita moverse ni chocar con nada. 
Se instancian muchas veces la mayoria de los pasillos tienen una.

* `is_super` distingue si es una bolita normal o una de las 4 gradnes de las esquinas. 
* `pos` donde esta colocada dentro del maze, una vez colocada no hace falta distinguir.
* `was_collected` si ya ha sido comida por el jugador o no.
* `point_value` cuantos puntos suma al ser recogida distintos si es normal o super
* `mark_as_collected()` la acción de ser comida, solo cambia a yaFueRecogida a True y devuelve True la primera vez que se llama; si ya estaba recogida, no hace nada y devuelve False. Esto protege contra el caso raro de que, por algún bug de detección de colisión, se llame dos veces en el mismo frame así nunca sumas puntos de más por la misma pacgum.
* `get_point_value()` le dice a quién la recogió normalmente GameState, en comprobarColisionJugadorPacgmun cuántos puntos sumar al marcador.

