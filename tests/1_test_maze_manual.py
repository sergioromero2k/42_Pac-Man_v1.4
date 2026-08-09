from core.maze import Maze


def main() -> None:
    test_maze = Maze(
        walls={
            (0, 0),
            (0, 1),
            (-1, 0),
            (1, 0),
        },
        paths={
            (1, 1),
            (0, 0),
            (1, 2),
            (0, 0),
        },
        maze_height=3,
        maze_width=4
    )

    print(test_maze.is_path((0, 0)))
    print(test_maze.is_wall((999, 999)))
    print(test_maze.is_path((999, 999)))

    assert test_maze.is_path((0, 0)) is True
    assert test_maze.is_path((999, 0)) is True


if __name__ == "__main__":
    main()
