# Decisiones de diseño - Pac-Man 42
---

## Config y ConfigLoader: dos clases separadas
- `Config` solo guarda los **8 valores del juego** (vidas, puntos, semilla, tiempo máximo, niveles, fichero de highscore). No sabe de dónde vienen.
- `ConfigLoader` lee el archivo, quita los comentarios `#`, valida cada valor y construye un `Config`. No guarda estado.
- **Motivo (responsabilidad única)**: el resto del juego depende solo de `Config` y no sabe que existe un **JSON**. Si cambia el formato del archivo, solo se toca `ConfigLoader`.
- Los valores por defecto (`DEFAULT_*`) viven en `ConfigLoader`, no en `Config`: decidir qué hacer ante un archivo roto es lógica de lectura, no de datos.
- `Config` es un `@dataclass(frozen=True)`: los valores validados no se pueden modificar tras crearse. Los datos que cambian durante la partida (como las vidas) viven en `Player`, no en `Config`.

## Librería gráfica: arcade
- Elegida arcade (el subject permite "MLX or similar"). La UI del compañero ya está hecha con ella, y `arcade.View` encaja con la jerarquía de vistas del UML.
- Descartada pygame: habría obligado a reescribir las pantallas ya hechas.
- Riesgo asumido: arcade necesita OpenGL 3.3. Pendiente de probar en el ordenador donde se hará la defensa.

```sh
python3 -m venv venv
source venv/bin/activate
pip install arcade
python -c "import arcade; print(arcade.__version__); w = arcade.Window(300, 200, 'test'); print('ok'); w.close()"
```

## Errores: ConfigLoader no lanza excepciones, MazeLoader sí
- Criterio: ¿existe un valor de reserva razonable cuando algo falla?
- Config: sí. Ante un valor ausente o inválido se usa su valor por
  defecto, se avisa con un mensaje claro y el juego continúa (lo pide el
  subject, V.3).
- Maze: no. El subject prohíbe escribir nuestro propio generador, así que
  no se puede fabricar un laberinto de reserva. `MazeLoader` lanza
  `MazeLoaderError`.
- Lanzar una excepción no es lo mismo que mostrar un traceback: `GameEngine`
  debe capturar `MazeLoaderError`, mostrar un mensaje legible y decidir si
  salta el nivel o cierra el juego.
- Validar bien el config no evita que el generador falle: son dos fuentes
  de error independientes.


