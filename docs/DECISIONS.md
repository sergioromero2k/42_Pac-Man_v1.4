## Player
* `recibirInput(direccion: Direction) -> void `
>> Fíjate que Entity ya tiene dirActual (la dirección en la que se está moviendo ahora mismo), pero la dirección que el jugador quiere tomar en cuanto sea posible (por ejemplo, gira antes de llegar a la esquina) es un concepto ligeramente distinto en muchos Pac-Man. Puedes optar por simplificar y que sean lo mismo (recibirInput sobrescribe directamente dirActual), o añadir un atributo nuevo dirDeseada: Direction en Player si quieres ese comportamiento más fiel de "recordar hacia dónde quiero girar".

* `perderVida()`
>> Internamente decrementa vidasRestantes en 1. Aquí también una decisión pendiente: ¿este método llama él mismo a respawneaCentroMaze(), o eso lo decide quien llama (GameState) por separado? Ambas son válidas, pero tenlo claro para cuando implementes.

* `respawneaCentroMaze() -> void`. Internamente hace posActual = posSpawn (usando el atributo heredado de Entity).
* `compVida() -> boolean` — Vuelve True si vidasRestantes <= 0.

## Ghost

* `idFantasma: int`
>> Recuerda cuando hablamos de esta pieza en el diagrama: dijimos "identificador de qué fantasma es (0-3), si vas a diferenciar comportamientos tipo Blinky/Pinky/Inky/Clyde". Es decir, idFantasma debería ser simplemente un número (int, 0 a 3) que identifica cuál de los 4 fantasmas es — no un tipo llamado "comportamiento". El comportamiento en sí (cómo persigue, qué target elige) es lógica dentro de proxMovimiento(), no un dato que se guarde como atributo con ese tipo.
* `proxMovimiento(posJugador: tuple(int,int)) -> Direction` calcula hacia dónde se mueve el fantasma según su modoActual.
