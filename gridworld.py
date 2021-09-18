from array import *
import random

class Gridworld():
    def __init__(self, dim:int, p: float) -> None:
        super().__init__()
        self._dim = dim
        self._density = p
        """
        Create a gridworld with the given dimension and probabilty.
        Parameters:
        ----------
        dim : Dimension of the gridworld as a int.
        p : Probability that each cell would be blocked as a float. (0 < p < 1).

        Returns:
        -------
        gridworld: Gridworld as a 2-D array. Dimension is (dim + 2) * (dim + 2).
        0 indicates unblocked.
        1 indicates blocked.
        Gridworld is surrounded by blocked cells indicating boundaries.
        Upper left corner(Start) and lower right corner(End) are always unblocked.
        """ 
        if self.__valid_input():
            self.gridworld = [[1 for i in range(self._dim)] for j in range(self._dim)]

            for j in range(self._dim):
                for i in range(self._dim):
                    if random.uniform(0, 1) > self._density:
                        self.gridworld[i][j] = 0

            self.gridworld[0][0] = self.gridworld[self._dim-1][self._dim-1] = 0

    def __valid_input(self):
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
        if not isinstance(self._dim, int):
            raise TypeError("Argument dim expected to be a int")
        if not isinstance(self._density, float):
            raise TypeError("Argument p expected to be a float")
        if not self._dim > 0:
            raise ValueError("Argument dim should be greater than 0")
        if not 0 < self._density < 1:
            raise ValueError("Argument p should be greater than 0 and smaller than 1")
        return True

    def __str__(self) -> str:
        gridworld = ""
        for row in self.gridworld:
            gridworld += "  ".join([str(col) for col in row]) + "\n"
        return gridworld