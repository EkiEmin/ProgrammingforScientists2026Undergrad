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
    # TODO: implement
    pass
