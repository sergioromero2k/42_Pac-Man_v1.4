## HighScoreEntry
---
Se instancia 1vez por cada puntuación guardada, hasta 10 instancias vivas a la vez. 
Es puramente una estrucutra de datos, sin comportamiento propio no necesita leer archivos, ni validarse a sí misma de forma compleja (esa validación, recordad, vive en HighscoreManager.añadirPuntuacionNueva(), antes de crear la entrada). 
Solo necesita guardar los 2 datos.

* `username` el nombre que introdujo el jugador al terminar la partida. Ya validado antes de llegar aquí **(máx 10 caracteres, alfanumético y espacios)**, según las reglas de subject.
* `score` la puntuación final de esa partida concreta. También ya validada como entero no negativo antes de crear la entrada.
