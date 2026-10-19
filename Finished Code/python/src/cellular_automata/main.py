import sys
import pygame
from custom_io import read_board_from_file, read_rules_from_file, read_color_map_from_file
from functions import play_automaton
from drawing import draw_game_boards
from animate import animate_surfaces

def main():
    print("Cellular automata!")

    if len(sys.argv) < 7:
        raise ValueError(
            "Usage: python main.py neighborhood_type rule_file initial_board_file output_file cell_width num_gens [color_map_file]"
        )

    neighborhood_type = sys.argv[1]  # "vonNeumann" or "Moore"
    rule_file = sys.argv[2]  # where are rule strings found?
    initial_board_file = sys.argv[3]  # my starting GameBoard file name
    output_file = sys.argv[4]  # where to draw the final MP4 video boards
    cell_width = int(sys.argv[5])  # how many pixels wide should each cell be?
    num_gens = int(sys.argv[6])  # how many generations to play the automaton?

    if len(sys.argv) > 7:
        color_map_file = sys.argv[7]
        color_map = read_color_map_from_file(color_map_file)

        print("Color map in successfully!")

    else: 
        color_map: dict[str, str] = {
            "0": "dark_gray",
            "1": "white",
            "2": "red",
            "3": "green",
            "4": "yellow",
            "5": "orange",
            "6": "purple",
            "7": "blue",
            "8": "black",
        }

    print("Parameters read in successfully!")

    rules = read_rules_from_file(rule_file) # dictionary of strings to strings representing the rules

    print("Rules read. Reading in board.")

    initial_board = read_board_from_file(initial_board_file)

    print("Board read in successfully. Ready to simulate the automaton.")

    pygame.init()

    boards = play_automaton(initial_board, num_gens, neighborhood_type, rules)

    print("Drawing automata generations to surfaces.")

    surfaces = draw_game_boards(boards, cell_width, color_map)

    print("Converting surfaces to .mp4 video.")

    video_path = f"{output_file}.mp4"
    animate_surfaces(surfaces, video_path)

    print("Success! MP4 video produced.")

    pygame.quit()

if __name__ == "__main__":
    main()
