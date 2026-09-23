from mazegenerator.mazegenerator import MazeGenerator

gen = MazeGenerator(size=(5, 5), perfect=False, seed=42)
gen.generate(seed=42)
print(type(gen.maze))
print(gen.maze)
print("entry: ", gen.maze_entry)
print("exit: ", gen.maze_exit)
