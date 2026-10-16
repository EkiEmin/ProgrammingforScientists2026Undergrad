import sys
from pathlib import Path

from functions import upgma
from io_util import read_matrix_from_file, write_newick_to_file


def main() -> None:
    if len(sys.argv) != 3:
        raise ValueError("Error: incorrect number of command line arguments. Usage: main.py <input_file> <output_dir>")

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    species_names, matrix = read_matrix_from_file(input_file)

    tree = upgma(matrix, species_names)

    output_filename = Path(input_file).stem + ".nwk"
    write_newick_to_file(tree, output_dir, output_filename)
    print(f"Tree written to {output_dir}/{output_filename}")


if __name__ == "__main__":
    main()
