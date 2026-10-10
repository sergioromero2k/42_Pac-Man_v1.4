# Decisiones de diseño - Pac-Man 42
---

Se trabaja directamente sobre `main` (decisión consciente, ver DECISIONS.md).
Decisión registrada en DECISIONS.md: ConfigLoader NUNCA lanza excepción,
a diferencia de MazeLoader.
Decisión en DECISIONS.md: flag `is_super` en vez de subclase SuperPacgum.

## Arquitectura general
- `Entity` como clase base de `Player` y `Ghost` (comparten posición, dirección, sprite, referencia al maze, spwan, y los métodos `move()`/`respawn()`).
- `Pacgum` NO hereda de `Entity`: no se mueve ni colisiona con paredes, así que heredar todo el paquete de **Entity** sería innecesario. Es una clase independiente con flag `is_super` (Opción B) en vez de una subclase `SuperPacgum` (Opción A).

## Conveción de ejes (todo el proyecto)
- Arriba/Norte = **y-1**, Abajo/Sur = **y+1** (como en pantalla, no como en matemáticas).
- Fijada en `DIRECTION_DELTAS` (core/enums.py) y respetada también en `MazeLoader` al convertir el bitmask del generador externo.

## Patrón "incializar internamente, no como parámetro"
- Para datos que nunca tienen sentido pedido desde fuera al crear el objeto: `desired_direction` (Player), `target_position` (Ghost), `was_collected` (Pacgum). Siempre se inicializan a su valor por defecto dentro del propio `__init__`.

## Movimiento por frame, no por tecla
- `Player.handle_input()` solo guarda la dirección deseada.
- Es `GameState` (en el game loop) quien llama a `move()` en cada frame, para un movimiento fluido y constante, como el `Pac-Man` original.
gi