from datatypes import GameBoard

def read_rules_from_file(filename: str) -> dict[str, str]:
    """
    read_rules_from_file takes a filename as a string and reads the rule strings provided in this file.
    It stores the result in a dictionary mapping neighborhood strings to strings.

    Args:
        filename (str): The name of the file containing the rule strings.

    Returns:
        dict[str, str]: A dictionary where keys are neighborhood strings and values are the resulting state strings.
    """
    if not isinstance(filename, str) or len(filename) == 0:
        raise ValueError("filename must be a non-empty string.")

    # create a new dictionary (aka map) to store the rules
    rules: dict[str, str] = dict()

    # open and read the file
    with open(filename, "r") as file:
        giant_string = file.read()

    # parse out the file contents as a list of strings, one line at a time
    trimmed_giant_string = giant_string.strip()
    lines = trimmed_giant_string.splitlines()

    for current_line in lines:
        parts = current_line.split(":")

        # parts should have exactly two strings in it
        if len(parts) != 2:
            raise ValueError("Too many colons or not enough in rule.")

        # first part is the neighborhood string
        neighborhood_string = parts[0]

        # second part is the state of the cell in the next generation as a string
        new_state = parts[1]

        # add the current neighborhood and updated state to our rule dictionary (aka map)
        rules[neighborhood_string] = new_state

    return rules


def read_color_map_from_file(filename: str) -> dict[str, str]:
    """
    Reads a color map configuration from a txt file and returns it as a dictionary.

    Args:
        filename (str): The path to the color map file.

    Returns:
        dict[str, str]: A dictionary mapping state strings to color name strings.
        Color name values must be one of: dark_gray, white, red, green, yellow,
        orange, purple, blue, or black.
    """
    with open(filename, 'r') as f:
        giant_string = f.read()

    trimmed_giant_string = giant_string.strip()
    lines = trimmed_giant_string.splitlines()

    color_map: dict[str, str] = {}

    for line in lines:
        # each line looks like "0:dark_gray"
        parts = line.split(':')
        state = parts[0].strip()
        color = parts[1].strip()

        color_map[state] = color

    return color_map


def read_board_from_file(filename: str) -> GameBoard:
    """
    Reads a board configuration from a CSV file and returns it as a GameBoard.

    Args:
        filename (str): The path to the CSV file.

    Returns:
        GameBoard: A 2D list of strings representing the board.
    """
    if not isinstance(filename, str) or len(filename) == 0:
        raise ValueError("filename must be a non-empty string.")

    # open(filename, 'r') opens the file in read mode ('r'), returning a file object (f).
    # with ensures the file is automatically closed when the block ends — even if there’s an error.
    with open(filename, 'r') as f: 
        # first, convert the whole file to a string
        giant_string = f.read()

    # trim any space at the start or end of file
    trimmed_giant_string = giant_string.strip()

    # split the long string into multiple strings, one for each line
    lines = trimmed_giant_string.splitlines()

    # lines is a list of strings, each element is each line of the file
    board = []

    # we will iterate over each line, parse the data in each line, and build the board
    for line in lines:
        line_elements = line.split(',')
        # line_elements contains a list of strings, one for each element in the row, i.e., a bunch of "0" and "1" strings
        board.append(set_row_values(line_elements))

    return board


def set_row_values(line_elements: list[str]) -> list[str]:
    """
    Convert a list of state strings into a list of strings.

    Args:
        line_elements (List[str]): A list of strings, where each element
                                   represents a cell state.

    Returns:
        list[str]: A list of state strings parsed from the input strings.
    """
    if not isinstance(line_elements, list) or len(line_elements) == 0:
        raise ValueError("line_elements must be a non-empty list of strings.")

    current_row = []

    # parse the line and keep each element as a string
    for element in line_elements:
        val = element
        current_row.append(val)

    return current_row
