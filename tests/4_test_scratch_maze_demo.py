# scratch_maze_demo - SOLO PARA ENTENDER EL CONCEPTO, NO ES CÓDIGO DEL PROYECTO

original_maze = [
    [9, 3],
    [12, 6],
]

room_width = 2
room_height = 2

print("=== OPCION 1: matriz original, tal cual da el generadoro ===")
for row in original_maze:
    print(row)
print(
    f"Tamaño: {room_width}x{room_height} - pero cada celda es una 'habitación',")
print("no podemos usar Entity.move()/is_wall() directamente sobre esto. \n")

final_width = 2*room_width+1
final_height = 2*room_height+1

grid = [['#' for _ in range(final_width)] for _ in range(final_height)]

for ry in range(room_height):
    for rx in range(room_width):
        bits = original_maze[ry][rx]
        cx, cy = 2*rx+1, 2*ry+1
        grid[cy][cx] = "."

        if not (bits & 1):
            grid[cy - 1][cx] = "."
        if not (bits & 2):
            grid[cy][cx + 1] = "."
        if not (bits & 4):
            grid[cy + 1][cx] = "."
        if not (bits & 8):
            grid[cy][cx - 1] = "."

print(f"===OPCIÓN 2: grid final {final_width}*{final_height} ===")

for row in grid:
    print(" ".join(row))
