from dataclasses import dataclass

# three things: distance matrix alias,
# node declaration,
# tree declaration


@dataclass
class Node:
    """
    Represents a node in a phylogenetic tree.

    Attributes:
        label (str): species name for leaves, ancestor name for internal nodes
        age (float): represents its "age" from the leaves
        child1: the first child node, or None if it doesn't exist
        child2: the second child node, or None if it doesn't exist
    """

    label: str = "Unlabeled"
    age: float = 0.0
    child1: 'Node | None' = None
    child2: 'Node | None' = None

    def is_leaf(self) -> bool:
        """
        Method that returns true if given node is a leaf and false otherwise.
        """
        #TODO: Implement
        pass

    def count_leaves(self) -> int:
        """
        Count the number of leaf nodes in the subtree rooted at this node.
        """
        #TODO: Implement
        pass

    def to_newick_ages(self) -> str:
        """
        Recursively serialize this subtree to Newick with branch lengths,
        where each branch length = parent.age - child.age.

        Returns:
            Newick string for this subtree (no trailing semicolon).
        """
        if self.is_leaf():
            return self.label

        left = ""
        right = ""

        if self.child1 is not None:
            branch_length1 = max(self.age - self.child1.age, 0.0)
            left = f"{self.child1.to_newick_ages()}:{branch_length1:.6f}"

        if self.child2 is not None:
            branch_length2 = max(self.age - self.child2.age, 0.0)
            right = f"{self.child2.to_newick_ages()}:{branch_length2:.6f}"

        return f"({left},{right})"


# alias declarations

DistanceMatrix = list[list[float]]

Tree = list[Node]
