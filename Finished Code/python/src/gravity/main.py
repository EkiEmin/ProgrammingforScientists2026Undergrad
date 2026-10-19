"""
CLI entry point for the gravity simulation.

Usage:
    python main.py <scenario_name> <num_gens> <time_step> <canvas_width> <drawing_frequency>

Example:
    python main.py jupiter_moons 1000 60 1500 10

This will read:   data/jupiter_moons.txt
and write video:  output/jupiter_moons.mp4
"""

import sys
import pygame
from custom_io import read_universe
from gravity import simulate_gravity
from drawing import animate_system
from animate import animate_surfaces

def main():
    print("Building a gravity simulator.")

    # Expect 5 user arguments (plus program name)
    if len(sys.argv) != 6:
        raise ValueError(
            "Error: incorrect number of command line arguments. Five desired."
        )

    scenario = sys.argv[1]

    # establish input file and output prefix
    input_file = f"data/{scenario}.txt"
    video_path = f"output/{scenario}.mp4"

    # Parse CLI arguments
    num_gens = int(sys.argv[2])
    time_step = float(sys.argv[3])
    canvas_width = int(sys.argv[4])
    drawing_frequency = int(sys.argv[5])

    print("Command line arguments read!")

    # Read initial universe
    initial_universe = read_universe(input_file)

    print("Simulating gravity now.")

    time_points = simulate_gravity(initial_universe, num_gens, time_step)

    print("Gravity simulation complete.")

    print("Rendering frames.")
    surfaces = animate_system(time_points, canvas_width, drawing_frequency)
    print("Frames drawn.")

    print("Encoding MP4 video.")
    animate_surfaces(surfaces, video_path)
    print("Success! MP4 video produced.")

    print("Animation finished! Exiting normally.")

if __name__ == "__main__":
    main()
