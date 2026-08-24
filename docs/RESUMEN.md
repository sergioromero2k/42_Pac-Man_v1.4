## Config.py
Es un sitio donde viven, ya cargados en memoria y con tipos garantizados, todos los parámetros configurable del juego(Vidas, puntos, tiempos por nivel, ruta del highscore). Es puramente una estructura de datos, sin comportamiento propio, no sabe leer archivos ni validar nada, solo guarda lo que le dan.

## config_loader.py
ConfigLoader es la pieza, la lógica de carga, separada de los datos, siguiendo el mismo principio de responsabilidad única que aplicasteis en todo el proyecto (un archivo, un trabajo). `Config` no sabe crearse a sí mismo, alguien tiene que leer el archivo JSON, quitarle los comentarios (que no son JSON estándar), parsearlo, y comprobar que cada valor es válido antes de confiar en él.

* `_default_config()` Un atajo para construir de golpe un `Config` completo hecho enteramente de esos valor por defecto, es usa cunado algo va tan mal.
* `load_config(file_path)` intenta leer el archivo, le quita los comentarios, intenta parsear el JSON, para cada una de las 8 claves, busca en el diccionario.
* `remove_comments(content)` recorre el archivo línea por línea, descarta las que empiezan por `#` y vuelve a juntar el resto en un único texto limpio.


