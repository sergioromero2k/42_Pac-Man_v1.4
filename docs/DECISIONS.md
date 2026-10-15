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

### D-10 El movimiento se calcula con `delta_time`
- **Decisión:** `on_update(delta_time)` mueve con `velocidad * delta_time` (píxeles por segundo), no con píxeles fijos por frame.
- **Motivo:** la velocidad no depende de la tasa de refresco (60 Hz o 144 Hz).
- **Descartado:** mover por frame o por pulsación (lo que hacía el prototipo del
  compañero en `input_handler.py`).

### D-11 Punto de entrada `pac-man.py` con exactamente un argumento
- **Decisión:** `python3 pac-man.py <config.json>`. Con otro número de argumentos muestra el uso y termina, sin traceback.
- **Motivo:** lo exige el subject.

| Término | Qué es | Ejemplo |
|---|---|---|
| Píxel | Un punto de la pantalla | Tu ventana mide 960 × 640 píxeles |
| Celda (tile) | Un cuadrado del laberinto, de 32 × 32 píxeles | 960 / 32 = 30 columnas y 640 / 32 = 20 filas |
| Hz | Veces por segundo que el monitor redibuja la imagen | 60 Hz = 60 veces por segundo |
| FPS | Veces por segundo que tu programa dibuja un frame | Normalmente igual a los Hz del monitor |
| Frame | Una vuelta completa del bucle: actualizar y dibujar | A 60 FPS, un frame dura unos 0,0167 s |
| delta_time | Los segundos que pasaron desde el frame anterior | A 60 FPS vale aproximadamente 0,0167 s |


### El game loop
En cada frame, el motor hace 3 cosas, siempre en este orden:
* **Eventos:** ¿se ha pulsado una tecla? En arcade es `on_key_press`.
* **Update:** cambiar el estado del juego (posiciones, vidas, tiempo) en on_update(delta_time).
* **Draw:** pintar el estado actual en `on_draw`.

### Por qué `delta_time`
Tu cuadrado va a 160 píxeles por segundo. Compara los 2 métodos.
| FPS | Con `delta_time` (160 × dt) | Fijo de 3 px por frame |
|---:|---|---:|
| 30 | 5,33 px/frame → **160 px/s** | 90 px/s |
| 60 | 2,67 px/frame → **160 px/s** | 180 px/s |
| 144 | 1,11 px/frame → **160 px/s** | 432 px/s |
