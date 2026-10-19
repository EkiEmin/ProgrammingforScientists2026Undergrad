from datatypes import GameBoard

def play_automaton(
    initial_board: GameBoard,
    num_gens: int,
    neighborhood_type: str,
    rules: dict[str, str]
) -> list[GameBoard]:
    """
    Simulate a cellular automaton for a given number of generations.

    Args:
        initial_board (GameBoard): The starting configuration of the automaton.
        num_gens (int): The number of generations to simulate.
        neighborhood_type (str): Either "Moore" or "vonNeumann".
        rules (dict[str, str]): A mapping from neighborhood strings to next-state.

    Returns:
        list[GameBoard]: A list of GameBoard objects of length num_gens + 1,
        representing the automaton's progression from the initial board
        through each generation.
    """
    # TODO: implement
    pass


def update_board(current_board: GameBoard, neighborhood_type: str, rules: dict[str, str]) -> GameBoard:
    """
    Update a GameBoard for one generation according to the given rules and neighborhood type.

    Args:
        current_board (GameBoard): The current state of the automaton.
        neighborhood_type (str): Either "Moore" or "vonNeumann".
        rules (dict[str, str]): A mapping from neighborhood strings to next-state

    Returns:
        GameBoard: The new board after applying the automaton rules for one generation.
    """
    # TODO: implement
    pass


def update_cell(board: GameBoard, r: int, c: int,
                neighborhood_type: str,
                rules: dict[str, str]) -> str:
    """
    update_cell takes a GameBoard along with row and column indices, 
    a neighborhood type, and a rule map. 
    It returns the state of the cell at this row and column 
    in the next generation.
    """
    # TODO: implement
    pass


def neighborhood_to_string(current_board: GameBoard, r: int, c: int, neighborhood_type: str) -> str:
    """
    neighborhood_to_string takes as input a GameBoard, row and column indices,
    and a neighborhood type as a string.
    It returns a string formed of the central square followed by its neighbors
    according to the neighborhood type indicated.

    Args:
        current_board (GameBoard): The game board.
        r (int): Row index of the cell.
        c (int): Column index of the cell.
        neighborhood_type (str): Either "Moore" or "vonNeumann".

    Returns:
        str: A string encoding the central cell and its neighbors' states.
    """
    # TODO: implement
    pass


def initialize_board(num_rows: int, num_cols: int) -> GameBoard:
    """
    Initialize a GameBoard with the given number of rows and columns.

    Args:
        num_rows (int): Number of rows.
        num_cols (int): Number of columns.

    Returns:
        GameBoard: A num_rows x num_cols board filled with "0" values.
    """
    if not isinstance(num_rows, int) or num_rows <= 0:
        raise ValueError("num_rows must be a positive integer.")
    if not isinstance(num_cols, int) or num_cols <= 0:
        raise ValueError("num_cols must be a positive integer.")

    board: GameBoard = [] # declaring board

    for _ in range(num_rows):
        row = ["0"] * num_cols
        board.append(row)

    return board


def count_rows(board: GameBoard) -> int:
    """
    Count the number of rows in a GameBoard.

    Args:
        board (GameBoard): A 2D list of strings representing the game state.

    Returns:
        int: Number of rows in the board.
    """
    if not isinstance(board, list):
        raise ValueError("board must be a list.")

    return len(board)


def count_columns(board: GameBoard) -> int:
    """
    Count the number of columns in a GameBoard.

    Args:
        board (GameBoard): A 2D list of strings representing the game state.

    Returns:
        int: Number of columns in the board.

    Raises:
        ValueError: If the board is not rectangular.
    """
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty 2D list.")
    if len(board) == 0:
        raise ValueError("Error: no rows in GameBoard.")

    return len(board[0])


def assert_rectangular(board: GameBoard) -> None:
    """
    Check whether a GameBoard is rectangular.

    Args:
        board (GameBoard): The game board.

    Raises:
        ValueError: If the board has no rows or if its rows are not the same length.
    """
    if len(board) == 0:
        raise ValueError("Error: no rows in GameBoard.")

    first_row_length = len(board[0])

    # range over rows and make sure that they have the same length as first row
    for row in board:
        if len(row) != first_row_length:
            raise ValueError("Error: GameBoard is not rectangular.")


def in_field(board: GameBoard, i: int, j: int) -> bool:
    """
    Check if the indices (i, j) are within the bounds of the board.

    Args:
        board (GameBoard): The game board (2D list of strings).
        i (int): Row index.
        j (int): Column index.

    Returns:
        bool: True if (i, j) is inside the board, False otherwise.
    """
    # parameter checks
    if not isinstance(board, list) or len(board) == 0:
        raise ValueError("board must be a non-empty GameBoard.")
    if not isinstance(i, int) or not isinstance(j, int):
        raise ValueError("i and j must be integers.")

    if i < 0 or j < 0:
        return False
    if i >= count_rows(board) or j >= count_columns(board):
        return False

    # if we survive to here, then we are on the board
    return True
