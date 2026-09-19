## HighScoreManager
---

Se instancias 1vez, dentro de `GameEngine` y se usa en 2 momentos al arrancar el juego (mostrar el ranking en el menú) y cada vez que termina una partida con una puntuación nueva que registrar. El subject exige un ranking persistencia,  la puntuación de una partida tiene que sobrevivir aunque cierres el programa por completo, así que hace falta algo que sepa leer y escribir en disco, no solo mantener datos en memoria mientras el programa está corriendo.

`EntradaHighscore` es el dato puro(nombre + puntuación de una entrada), y `HighscoreManager` es quien sabe gestionar la colección completa de esas entradas - cargarlas, guardarlas, mantenerlas ordenadas y limitadas a 10.

* `rutaArchivo` ruta al archivo JSON donde se guarda el ranking.
* `entradas` la colección de puntuaciones actuales, cada una con sus nombres de usuarios y su core. Se rellena al llamar a cargarDesdeDisco().

* `cargarDesdeDisco()` lee el archivo en `rutaArchivo`, parsea su contenido y rellena entradas. Si el archivo no existe, está corrupto, o tiene formato inválido, deja entradas como lista vacia en vez de crashear (Lo pide el subject V.5).
* `guardarDisco()` el proceso inverso: escrbe el contenido actual de entradas al archivo en `rutaArchivo`, sobreescribiendo lo que hubiera antes.
* `añadirPuntuacionNueva()` se llama al terminar una partida, valida que username cumpla reglase del subject y que score sea un entero no negativo; si todo es válido, crea un EntradaHighscore nueva, la añade a entradas, llama internamente a mantenerSoloTop10() para recortar si hace falta, y devuelve True.
* `mantenerSoloTop10()` método privado (por eso el - en vez de +) ordena entradas de mayor a menor puntuación y descarta todo lo que sobrepase las 10 primeras. Se llama automáticamente desde dentro de `añadirPuntuacionNueva()`, nunca hace falta llamarlo desde fuera de la clase.

