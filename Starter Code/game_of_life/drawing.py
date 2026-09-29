import pygame
from datatypes import GameBoard


def draw_game_board(board: GameBoard, live_color: tuple[int, int, int], dead_color: tuple[int, int, int], cell_width: int, scaling_factor: float = 0.8) -> pygame.Surface:
    """
    Draws a Game of Life board to a pygame.Surface object.

    Parameters:
    - board: 2-D list of booleans (True = alive, False = dead)
    - live_color: RGB color tuple for live cells
    - dead_color: RGB color tuple for dead cells
    - cell_width: width and height in pixels of each cell
    - scaling_factor: multiplier applied to the cell radius when drawing

    Output:
    - pygame.Surface representing the drawn board.
    """
    width = cell_width * len(board[0])
    height = cell_width * len(board)
    surface = pygame.Surface((width, height))

    surface.fill(dead_color)

    radius = scaling_factor * (cell_width / 2)

    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col]:
                x = col * cell_width + cell_width / 2
                y = row * cell_width + cell_width / 2

                pygame.draw.circle(surface, live_color, (int(x), int(y)), int(radius))

    return surface


def draw_game_boards(boards: list[GameBoard], live_color: tuple[int, int, int], dead_color: tuple[int, int, int], cell_width: int, scaling_factor: float = 0.8) -> list[pygame.Surface]:
    """
    Draws each GameBoard in a list to its own pygame.Surface object.

    Parameters:
    - boards: list of GameBoard objects
    - live_color: RGB color tuple for live cells
    - dead_color: RGB color tuple for dead cells
    - cell_width: width and height in pixels of each cell
    - scaling_factor: multiplier applied to the cell radius when drawing

    Output:
    - list of pygame.Surface objects, one per board.
    """
    canvases = []
    for board in boards:
        canvases.append(draw_game_board(board, live_color, dead_color, cell_width, scaling_factor))
    return canvases
