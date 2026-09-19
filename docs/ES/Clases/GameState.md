## GameState
---

Se instancia 1ez por nivel, cuando termina el nivel (ganado o perdido), esa istancia se descarta y si hay siguiente nivel se crea uno nuevo.
Es el lugar donde se coordina todo lo que pasa dentro de un nivel mientras se está jugando: mover a los fantasmas, comprobar si el jugador choca con algo, ir descontando el tiempo, saber cunto se ha terminado el nivel. Con ella, la lógica estaría desperdigada entre Player, Ghost y Pacgmun por separado, y ninguna de esas clases individuales tiene la visión completa necesariapara decidir.

* `player` el jugador de la partida, el player sobrevive al cambiar de nivel(mantiene vidas y score) , así que lo más correcto sería que lo cree GameEngine una sola vez y se lo pasa a cada GameState nuevo.
* `ghosts` 4 fantasmas del nivel, se crean 0 en cada nivel nuevo.
* `pacgums`
* `current_maze_reference` el laberinto de este nivel concreto.
* `level_time_remaining` el tiempo restante que queda por nivel (subject 90-120seg).
* `update_game_frame()` Hace que cada fantasma calcula su siguiente movimiento, comprueba las 2 colisiones y descuentas su tiempo. Se llama en cada frame del juego (60veces por segundo).
* `check_player_ghost_collision()` compara la pos del player con la de cada ghost. Si coinciden: si está en modo frightened , lo marca como comido(suma puntos); si no, restar una vida al jugador (salvo que haya invecibilidad de cheat activa).
* `check_player_pacgum_collision()` compara la pos del player con la de cada pacgmun sin recoger. Si coincide, llama a `marcaRecogida()`.
* `check_level_complete()` devuelve si ya no queda ninguna pacgmun sin recoger en la lista, la señal de que el nivel está ganado.
