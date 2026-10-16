import sys
from pathlib import Path

from datatypes import Node
from functions import upgma
from io_util import read_matrix_from_file, write_newick_to_file


def demo():
    a = [10, 20, 30, 40]
    b = a[:2]   # working with duplicated form of the data
    print(b)

    b[0] = 99
    print("a is", a)
    print("b is", b)

    a = [Node(label = "Axolotl"), Node(label = "Blobfish")]
    b = a[:1]  # we still get copies, but we get copies of *references* to the data in a

    print(b[0].label)
    b[0].label = "Chicken"
    print("the first label of a is", a[0].label)

    # when we take a sublist (slice) of a collection of mutable objects, we get access to those objects (can change the original list)

    c = [1, 2, 3, 4, 5, 6]
    del c[1]  # c is now [1, 3, 4, 5, 6]
    del c[3]  # we removed the 5, not the 4!
    print("c is", c)


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
