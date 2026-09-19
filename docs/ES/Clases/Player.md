## Player
---
`Player` es un tipo de Entity, se instancia. 
`Respawnear` es la acción de devolver al jugador a su posición inicial (el centro de maze) 
* **(Game over)** - morir del todo.
* **(Morir 1vez)** - pierdes vida y sigues jugando.

* `remaining_lives` empieza con el valor que diga la Config(por defecto, 3) 
* `total_score`
* `desired_direction` 
* `handle_input()`: No captura la tecla él mismo (eso es de `GameView`) solo recibe ya una `Direction` traducida y la guarda como la dirección hacia la que el jugador se mueve.
* `lose_life()`
* `respawn_at_maze_center()` devolver al jugador a `posSpawn`.
* `has_lives_remaining()`: comprueba si el jugador sigue vivo.
* `add_life()` suma 1 a vidasRestantes. Es el complemento simétrico de perderVida() (Se usa en `GameView`).
* `add_score()`