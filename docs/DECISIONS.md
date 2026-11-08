# Decisiones de diseño - Pac-Man 42

## ¿Por qué dos clases y no una?

Cada clase hace una sola cosa:
* `Config` son solo los datos. El resto del juego depende de ella y no sabe que existe un archivo ni un JSON.
* `ConfigLoader` sabe leer, limpiar y validar. Si mañana el formato cambia a otro, solo tocas el loader.

Con una sola clase, el `Config` se leería a sí mismo y tendría una mitad de datos y otra de lógica de archivos. Eso también complica los tests, porque para crear un `Config` de prueba tendrías que pasar por un archivo. Y en la defensa te pueden pedir cambiar la validación sin tocar los datos. Para un proyecto de este tamaño es mejor separarlas.

