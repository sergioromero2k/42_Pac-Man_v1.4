## GameEngine
---
Es el objeto raiz de todo vuestro core - se crear una vez (`main.py`) y vive hasta que se cierra el programa. 
Es el que decide en que pantalla estamos o que hay que hacer ahora, delegando el trabajo pesado de jugar un nivel a `GameState` cuando corresponde. 
`GameState` hacia todo en principio, pero para representar el menú necesitara un GameState hacia todo vacios o falsos, porque al inicio no hay una partida en marcha. Eso daba a entender que `GameState` estaba haciendo 2 curros, **gestionar la app entera** y **gestionar un nivel jugandose ahora mismo.**
`GameState` estaba haciendo existe para quedarse con el 1er trabajo.

* `GameEngine.player` es quien crea el `Player`(una sola vez, al empezar la partida completa) y quien lo mantiene vivo durante todo el tiempo que ocurre la partida.
* `GameState.player`, no crea nada, simplemente recibe una referencia al mismo objeto.
* `current_state` en que fase de la app está el usuario durante un nivel concreto.
* `active_game_state` el nivel en curso, si lo hay. None cuando estas en el Menú.
* `config` la configuración cargada al arrancar, la necesita para saber cuantas vidas iniciales dar, tamaños de niveles, puntos por pacgmun.
* `change_state()` actualiza `estadoActual`. Lo llama `GameView`, ejm: apretar **ESC** pasar de **PLAYING** a **PAUSED**.
* `start_level()` pide un `Maze` nuevo a `MazeLoader` con el tamaño y `seed` correspondiente, construye `GameState` nuevo pasandole ese maze y el player que ya tenia guardado.
* `end_level()` se dispara cuando el nivel completo o la vida se acaba.
* `update()` delega el trabajo real en `gameStateActivo.actualizarJuegoFrame(deltaTime)` y comprueba si el nivel ha terminado.
