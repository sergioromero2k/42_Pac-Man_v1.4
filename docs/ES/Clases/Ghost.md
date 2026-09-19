## Ghost
---
Ghost necesita todo lo básico de Entity.
Se instancia 4veces. Ghost necesita decidir su propio movimiento sin que nadie lo controle desde fuera. 
Ghost se mueve por el mismo. 
Cada instancia es completamente independiente: tiene su propio `modoActual`, su propia `posObjetivo`, y calcula su propio movimiento cada vez.

* `current_mode` define en que estado de comportamiento esta el fantasma ahora mismo chase(persiguiendo), huyendo(frightened), eaten(ya comido y volviendo a su esquina).
* `ghost_id` - Sirve para identifcar cual de los 4 fantasmas es.
* `target_position` - La casilla concreta hacia la que el fantasma está intentando llegar ahora mismo, es el resulado de aplicarle la heurística de cada fantasma. (Perseguir directo, emboscar por delante, etc).
* `get_next_move` - Este es el método principal de esta clase, la IA en sí. Recibe dónde esta el jugador ahora mismo lo necesita para persegurilo o para huir de él, según `modoActual`, y devuelve la dirección a la que el fantasma debería moverse a continuacion.
Internamente es donde vive la lógica de "si estoy en chase, calculo la direcciçon que me acerca más a posObjetivo, si estoy en frightened, la que me aleja.
* `respawn()`
* `change_mode()` actualiza modoActual, lo llama GameState en 2 momentos cuando el jugador come un super-pacgmun y cuando un fanstama concreto es tocado en ese estado.