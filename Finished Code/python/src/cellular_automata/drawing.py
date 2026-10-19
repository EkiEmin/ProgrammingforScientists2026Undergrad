import pygame
from datatypes import GameBoard
from functions import count_rows, count_columns

def draw_game_boards(boards: list[GameBoard], cell_width: int, color_map: dict[str, str], scaling_factor: float=0.8) -> list[pygame.Surface]:
    """
    Draw game boards to Pygame surfaces.

    Args:
        boards (list[GameBoard]): A list of rectangular GameBoard objects.
        cell_width (int): The width (in pixels) of each cell in the image.
        color_map (dict[str, str]): A mapping from each state to a color name.
        scaling_factor (float): default = 0.8, amount to scale each radius by

    Returns:
        list[pygame.Surface]: A list of Pygame Surface objects corresponding to each GameBoard,
        where each cell is drawn with the specified width and height.
    """
    surfaces: list[pygame.Surface] = []

    for board in boards:
        current_surface = draw_game_board(board, cell_width, color_map, scaling_factor)
        surfaces.append(current_surface)

    return surfaces


def draw_game_board(current_board: GameBoard, cell_width: int, color_map: dict[str, str], scaling_factor: float=0.8) -> pygame.Surface:
    """
    Draw a rectangular GameBoard onto a new Pygame Surface.

    Args:
        current_board (GameBoard): The game board to be drawn.
        cell_width (int): The width (and height) in pixels of each cell in the board.
        color_map (dict[str, str]): A mapping from each state to a color name.
        scaling_factor (float): default = 0.8, amount to scale each radius by

    Returns:
        pygame.Surface: A Pygame Surface object representing the visual rendering
        of the given GameBoard.
    """
    # declare surface
    width = count_columns(current_board) * cell_width
    height = count_rows(current_board) * cell_width
    surface = pygame.Surface((width, height))

    # convert each color name to its RGB tuple
    colors: dict[str, tuple[int, int, int]] = {
        "dark_gray": (60, 60, 60),
        "white": (255, 255, 255),
        "red": (239, 71, 111),
        "green": (6, 214, 160),
        "yellow": (255, 255, 0),
        "orange": (255, 165, 0),
        "purple": (160, 32, 240),
        "blue": (17, 138, 178),
        "black": (0, 0, 0),
    }

    # fill the background with the color of state "0"
    surface.fill(colors[color_map["0"]])

    radius = scaling_factor * cell_width / 2

    for i in range(len(current_board)):
        for j in range(len(current_board[i])):
            val = current_board[i][j]

            # make sure that the color map has a color for this state
            if val not in color_map:
                raise ValueError(f"Error: Out of range value {val} in board when drawing board.")

            # the background already has the color of state "0"
            if val != "0":
                # set the circle's center
                x = j * cell_width + cell_width // 2
                y = i * cell_width + cell_width // 2

                # draw circle and fill it in
                pygame.draw.circle(surface, colors[color_map[val]], (x, y), int(radius))

    return surface
