from array import *
import random

def __valid_input(dim: int, p: float):
    """
    Raises an exception if the input is not valid.
    Valid parameter should be a int dim and a float p, which 0 < p < 1.
    Parameters:
    ----------
    dim : Dimension of the gridworld as a int.
    p : Probability that each cell would be blocked as a float. (0 < p < 1).

    Returns:
    -------
    valid_input : True
    """
    if not isinstance(dim, int):
        raise TypeError("Argument dim expected to be a int")
    if not isinstance(p, float):
        raise TypeError("Argument p expected to be a float")
    if not dim > 0:
        raise ValueError("Argument dim should be greater than 0")
    if not 0 < p < 1:
        raise ValueError("Argument p should be greater than 0 and smaller than 1")
    return True

def gridworld(dim, p):
    """
    Create a gridworld with the given dimension and probabilty.
    Parameters:
    ----------
    dim : Dimension of the gridworld as a int.
    p : Probability that each cell would be blocked as a float. (0 < p < 1).

    Returns:
    -------
    gridworld: Gridworld as a 2-D array. Dimension is (dim + 2) * (dim + 2).
    -1 indicates unblocked.
    1 indicates blocked.
    Gridworld is surrounded by blocked cells indicating boundaries.
    Upper left corner(Start) and lower right corner(End) are always unblocked.
    """ 
    if __valid_input(dim, p):
        gridworld = [[-1 for i in range(dim+2)] for j in range(dim+2)]

        for j in range(1, dim+1):
            for i in range(1, dim+1):
                if random.uniform(0, 1) > p:
                    gridworld[i][j] = 1

        gridworld[0][0] = gridworld[dim+1][dim+1] = -1
        return gridworld