from datatypes import GameBoard

def play_automaton(initial_board: GameBoard, num_gens: int, neighborhood_type: str, rules: dict[str, str]) -> list[GameBoard]:
    """
    Simulate a cellular automaton for a given number of generations.

    Args:
        initial_board (GameBoard): The starting configuration of the automaton.
        num_gens (int): The number of generations to simulate.
        neighborhood_type (str): Either "Moore" or "vonNeumann".
        rules (dict[str, str]): A mapping from neighborhood strings to next-state strings.

    Returns:
        list[GameBoard]: A list of GameBoard objects of length num_gens + 1,
        representing the automaton's progression from the initial board
        through each generation.
    """
    # parameter checks
    if not isinstance(initial_board, list) or len(initial_board) == 0:
        raise ValueError("initial_board must be a non-empty GameBoard.")
    if not isinstance(num_gens, int) or num_gens < 0:
        raise ValueError("num_gens must be a non-negative integer.")
    if neighborhood_type not in ["Moore", "vonNeumann"]:
        raise ValueError("neighborhood_type must be 'Moore' or 'vonNeumann'.")
    if not isinstance(rules, dict):
        raise ValueError("rules must be a dictionary.")

    boards = []
    boards.append(initial_board)

    for _ in range(num_gens):
        boards.append(update_board(boards[-1], neighborhood_type, rules))

    return boards


def update_board(current_board: GameBoard, neighborhood_type: str, rules: dict[str, str]) -> GameBoard:
    """
    Update a GameBoard for one generation according to the given rules and neighborhood type.

    Args:
        current_board (GameBoard): The current state of the automaton.
        neighborhood_type (str): Either "Moore" or "vonNeumann".
        rules (dict[str, str]): A mapping from neighborhood strings to next-state strings.

    Returns:
        GameBoard: The new board after applying the automaton rules for one generation.
    """
    # parameter checks
    if not isinstance(current_board, list) or len(current_board) == 0:
        raise ValueError("current_board must be a non-empty GameBoard.")
    if neighborhood_type not in ["Moore", "vonNeumann"]:
        raise ValueError("neighborhood_type must be 'Moore' or 'vonNeumann'.")
    if not isinstance(rules, dict):
        raise ValueError("rules must be a dictionary.")

    # first, create a new board corresponding to the next generation. All cells will have state 0.
    num_rows = count_rows(current_board)
    num_cols = count_columns(current_board)
    new_board = initialize_board(num_rows, num_cols)

    # iterate through all cells of current_board and update each one into new_board
    for r in range(num_rows):
        for c in range(num_cols):
            new_board[r][c] = update_cell(current_board, r, c, neighborhood_type, rules)

    return new_board


def update_cell(board: GameBoard, r: int, c: int,
                neighborhood_type: str,
                rules: dict[str, str]) -> str:
    """
    Determine next-state string for cell (r, c) using rules and neighborhood type.

    Args:
        board (GameBoard): Current state of the automaton.
        r (int): Row index of the cell to update.
        c (int): Column index of the cell to update.
        neighborhood_type (str): Either "Moore" or "vonNeumann".
        rules (dict[str, str]): A mapping from neighborhood strings to next-state strings.

    Returns:
        str: next state for the cell.
    """
    # consult the neighborhood of board[r][c] and convert to a string
    neighborhood = neighborhood_to_string(board, r, c, neighborhood_type)

    # is that neighborhood in the rule set? I hope so!
    if neighborhood in rules:
        return rules[neighborhood]

    # default case: return "0"
    return "0"


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
    # parameter checks
    if not isinstance(current_board, list) or len(current_board) == 0:
        raise ValueError("current_board must be a non-empty GameBoard.")
    assert_rectangular(current_board)
    if not isinstance(r, int) or not isinstance(c, int):
        raise ValueError("r and c must be integers.")
    if not in_field(current_board, r, c):
        raise ValueError("(r, c) must be inside the board.")
    if neighborhood_type not in ("Moore", "vonNeumann"):
        raise ValueError('neighborhood_type must be "Moore" or "vonNeumann".')

    # Initialize the neighborhood string with the current cell value
    neighborhood = current_board[r][c]

    # Set neighbor_cells to the absolute coordinates of each neighbor
    if neighborhood_type == "Moore":
        neighbor_cells = [
            (r-1, c-1), (r-1, c), (r-1, c+1),
            (r, c+1),
            (r+1, c+1), (r+1, c), (r+1, c-1),
            (r, c-1),
        ]
    elif neighborhood_type == "vonNeumann":
        neighbor_cells = [(r-1, c), (r, c+1), (r+1, c), (r, c-1)]

    # Iterate over neighbor_cells to construct the neighborhood string
    for x, y in neighbor_cells:
        if in_field(current_board, x, y):
            neighborhood += current_board[x][y]
        else:  # default case
            neighborhood += "0"

    return neighborhood


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
