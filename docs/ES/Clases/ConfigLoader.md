## ConfigLoader
---
`Config` es pasiva, no hace na más que guardar. Pero alguien tiene que hacer ese trabajo: abrir el JSON, quitarle los comentarios (que no son JSON estándar), parsearlo, comprobar que cada clave tiene un valor válido, y si algo falla, usar un valor por defecto en vez de crashear. `ConfigLoader` existe para ser exactamente ese "alguien" - la lógica de carga, separada de los datos en sí.

* `load_config()` recibe la ruta al archivo JSO, y hace todo el proceso: lee el contenido del archivo, le pasa el texto a `remove_comments()` para limpiarlo, parsea JSON resultante, valida cada clave (Si falta o es inválida, usa el valor por defecto correspondiente, sin crashear).
* `remove_comments()` metodo auxiliar interno, recibe el texto crudo tal cual viene del archivo, y devuelve ese mismo texto pero sin las líneas que empiecen por #, dejandolo listo para que `json.loads()` pueda pasearlo sin fallar.