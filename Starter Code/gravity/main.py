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

if __name__ == "__main__":
    main()
