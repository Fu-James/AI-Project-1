from heuristics import heuristics
from array import *
import random

class Cell():
    def __init__(self, x, y, gscore, dim, parent=None, flag=0):
        super().__init__()
        self.x = x
        self.y = y
        self.dim = dim
        self.index = x * self.dim + y
        self.update_gscore(gscore)             
        self.update_parent(parent)
        self.flag = flag

    def update_parent(self, parent):
        self.parent = parent

    def update_gscore(self, gscore: int):
        self.gscore = gscore
        self.__update_heuristics()
        self.__update_f()

    def __update_heuristics(self, option: int=0):
        self.hscore = heuristics(A=[self.dim - 1, self.dim - 1], B=[self.x, self.y], option=option)
        

    def __update_f(self):
        self.fscore = self.get_gscore() + self.get_heuristic()

    def __str__(self) -> str:
        return "Cell({})\ng(n) = {}\nh(n) = {}\nf(n) = {}".format(self.index, self.get_gscore(), self.get_heuristic(), self.fscore)

    def get_heuristic(self):
        return self.hscore

    def get_gscore(self):
        return self.gscore 

    def get_fscore(self):
        return self.fscore

    def getChildren(self):
        children = []
        if self.x - 1 >= 0:  # up
            children.append([self.x - 1, self.y])
        if self.y + 1 < self.dim:  # right
            children.append([self.x, self.y + 1])
        if self.x + 1 < self.dim:  # down
            children.append([self.x + 1, self.y])
        if self.y - 1 >= 0:  # left
            children.append([self.x, self.y - 1])
        return children

    def getIndex(self):
        return (self.index)

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
        gridworld: Gridworld as a 2-D array. Dimension is (dim) * (dim).
        0 indicates unblocked.
        1 indicates blocked.
        Gridworld is surrounded by blocked cells indicating boundaries.
        Upper left corner(Start) and lower right corner(End) are always unblocked.
        """ 
        if self.__valid_input():
            self.gridworld = [[Cell(row, col, 0, self._dim, flag=0) for col in range(self._dim)] for row in range(self._dim)]

            for row in range(self._dim):
                for col in range(self._dim):
                    if random.uniform(0, 1) < self._density:
                        self.gridworld[row][col] = Cell(row, col, 0, self._dim, flag=1)

            self.gridworld[0][0] = Cell(0, 0, 0, self._dim, flag=0)
            self.gridworld[self._dim-1][self._dim-1] = Cell(self._dim-1, self._dim-1, 0, self._dim, flag=0)

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
        if not 0 <= self._density <= 1:
            raise ValueError("Argument p should be greater than 0 and smaller than 1")
        return True

    def get_cell(self, x: int, y: int) -> Cell:
        return self.gridworld[x][y]

    def get_grid_ascii(self):
        return [[self.gridworld[row][col].flag for col in range(self._dim)] for row in range(self._dim)]

    def update_cell(self, cell: Cell, x: int, y: int) -> None:
        self.gridworld[x][y] = cell

    def __str__(self) -> str:
        gridworld = ""
        for row in self.gridworld:
            gridworld += "  ".join([str(col.flag) for col in row]) + "\n"
        return gridworld