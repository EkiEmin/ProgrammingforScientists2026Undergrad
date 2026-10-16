from datatypes import Node, Tree, DistanceMatrix

def upgma(mtx: DistanceMatrix, species_names: list[str]) -> Tree:
    """
    Build a phylogenetic tree using the UPGMA algorithm.

    Given a distance matrix and species names, iteratively merges the closest
    clusters and updates the matrix using cluster-size-weighted averages.
    The resulting tree has `n` leaves (the species) and `n-1` internal nodes.

    Args:
        mtx (DistanceMatrix): Square symmetric matrix of pairwise distances.
        species_names (list[str]): Names of the species, in the same order as `mtx`.

    Returns:
        Tree: A list of `Node` objects representing the full UPGMA tree.
              Conventionally, the last node (index -1) is the root.
    """
    assert_square_matrix(mtx)
    assert_same_number_species(mtx, species_names)

    # we now know that the matrix is square, and that the number of rows is equal to the number of species
    num_leaves = len(mtx)

    # make a tree containing 2n-1 total nodes, where the leaves are going to get labeled with species names
    t = initialize_tree(species_names)

    # clusters refer to the first num_leaves nodes in tree
    clusters = t[:num_leaves]  # is this OK? Should this make *new* nodes? No! It makes copies of the keys to the locker that contains the leaves

    # perform the engine of UPGMA with n-1 total steps
    # range over all the internal nodes and perform 1 step
    for p in range(num_leaves, 2*num_leaves-1):
        # find minimum element of matrix
        row, col, min_val = find_min_element(mtx)

        # set the age of current node (t[p])
        t[p].age = min_val/2.0

        # connect current node into its children
        t[p].child1 = clusters[row]  # this means update child 1 of current node to be the reference to the node in clusters[row] ... NOT "make a new node"
        t[p].child2 = clusters[col]

        # add a row and column to the matrix

        cluster_size_1 = t[p].child1.count_leaves()
        cluster_size_2 = t[p].child2.count_leaves()

        mtx = add_row_col(row, col, cluster_size_1, cluster_size_2, mtx)

        # delete the old rows/columns that are no longer needed

        mtx = delete_row_col(mtx, row, col)

        # create a new cluster referring to the new node
        clusters.append(t[p])

        # delete the two clusters that we joined together
        clusters = delete_clusters(clusters, row, col)

    # return the tree
    return t


def assert_square_matrix(mtx: DistanceMatrix) -> None:
    """
    Validate that a distance matrix is square.

    Args:
        mtx (DistanceMatrix): The matrix to validate.

    Raises:
        ValueError: If the matrix is empty or not square.
    """
    num_rows = len(mtx)
    if num_rows == 0:
        raise ValueError("Empty matrix given.")
    
    # idea: range over all rows, and each row should have length == num_rows
    for i in range(num_rows):
        if len(mtx[i]) != num_rows:
            raise ValueError("Error: non-square matrix given.")
        
    # if we make it here, we know the matrix is square.


def assert_same_number_species(mtx: DistanceMatrix, species_names: list[str]) -> None:
    """
    Validate that the number of species matches the matrix dimension.

    Args:
        mtx (DistanceMatrix): Square distance matrix.
        species_names (list[str]): Species labels.

    Raises:
        ValueError: If their sizes do not match.
    """
    if len(mtx) != len(species_names):
        raise ValueError("Error: number of rows in matrix not equal to # species.")


def add_row_col(row: int, col: int, cluster_size1: int, cluster_size2: int, mtx: DistanceMatrix) -> DistanceMatrix:
    """
    Append a new row and column for the merged cluster.

    Uses the idea that if we merge clusters with sizes s1, s2 corresponding to indices row/col of the matrix, then the distance from new cluster to cluster k is

    (s1 * D(k, row) + s2*D(k, col))/(s1 + s2)

    Args:
        row (int): Index of the first cluster to merge (row < col).
        col (int): Index of the second cluster to merge.
        cluster_size1 (int): Leaf count of the first cluster.
        cluster_size2 (int): Leaf count of the second cluster.
        mtx (DistanceMatrix): The current distance matrix.

    Returns:
        DistanceMatrix: The matrix with one new row and column added.
    """
    num_rows = len(mtx)

    # idea: make a new row and then I'll fill in the other values
    new_row = [0.0]*(num_rows+1)  #we'll worry about the extra column values later
    for r in range(len(new_row)-1):
        # I don't need to set new_row[row] or new_row[col]
        if r != row and r != col:
            new_row[r] = (cluster_size1 * mtx[r][row] + cluster_size2 * mtx[r][col])/(cluster_size1 + cluster_size2)
    
    # do two things: append this row to matrix and add the extra values with symmetry
    mtx.append(new_row)

    # now set the missing values due to symmetry (don't need to set bottom right)
    for r in range(num_rows):  # num_rows = original n
        mtx[r].append(new_row[r])

    return mtx


def delete_clusters(clusters: list[Node], row: int, col: int) -> list[Node]:
    """
    Remove two merged clusters from the cluster list.

    Args:
        clusters (list[Node]): The active cluster list.
        row (int): Index of the first cluster to remove (row < col).
        col (int): Index of the second cluster to remove.

    Returns:
        list[Node]: The updated cluster list.
    """
    del clusters[col]
    del clusters[row]
    # always delete the element with higher index first!

    return clusters


def delete_row_col(mtx: DistanceMatrix, row: int, col: int) -> DistanceMatrix:
    """
    Remove two rows and columns from the distance matrix.

    Args:
        mtx (DistanceMatrix): The current distance matrix.
        row (int): Row/column index of the first cluster (row < col).
        col (int): Row/column index of the second cluster.

    Returns:
        DistanceMatrix: The matrix with two rows and columns removed.
    """
    # remember: col > row

    # first, delete 2 rows
    del mtx[col]
    del mtx[row]

    # then, n-2 rows left; range over all of these rows and remove the elements at indices row and col (col first)
    num_rows = len(mtx)   # now n -2
    for r in range(num_rows):
        del mtx[r][col]
        del mtx[r][row]

    return mtx


def find_min_element(mtx: DistanceMatrix) -> tuple[int, int, float]:
    """
    Scan the upper triangle of mtx for the minimum value.

    Args:
        mtx (DistanceMatrix): A square distance matrix (at least 2x2).

    Returns:
        tuple[int, int, float]: (row, col, min_val) where row < col.

    Raises:
        ValueError: If the matrix has only one row or column.
    """
    if len(mtx) <= 1 or len(mtx[0]) == 1:
        raise ValueError("Matrix isn't large enough.")
    
    row = 0
    col = 1
    min_val = mtx[row][col]

    # range over values of the matrix, and any time I find a smaller value, I update these values 
    for r in range(len(mtx)-1):
        for c in range(r+1, len(mtx[r])):
            if mtx[r][c] < min_val:
                row, col, min_val = r, c, mtx[r][c]

    # nice exercise: write a function that asserts that mtx is a distance matrix (non-negative values, symmetric across main diagonal, have the triangle ineq.)

    return row, col, min_val


def initialize_tree(species_names: list[str]) -> Tree:
    """
    Allocate all 2n - 1 nodes for a tree with n leaves.

    Args:
        species_names (list[str]): Names for the n leaf nodes.

    Returns:
        Tree: A Tree of labeled leaves followed by labeled internal nodes.
    """
    num_leaves = len(species_names)

    t: Tree = []

    # let's give the tree 2*n-1 total nodes
    for i in range(2*num_leaves - 1):
        new_node = Node()  # default age = 0
        t.append(new_node)

        # we give it a label too 
        if i < num_leaves:
            t[i].label = species_names[i]
        else:
            # internal node, so we're just going to label it with i
            t[i].label = f"Ancestor Species: {i}"

    return t
