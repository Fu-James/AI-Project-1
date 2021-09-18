import numpy as np
from queue import PriorityQueue
from heuristics import heuristics

# PrioritizedItem is used to configure the priority queue
# such that it will only compare the priority, not the item
from dataclasses import dataclass, field
from typing import Any
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)


class Cell():
    def __init__(self, x, y, gscore, dim, parent):
        super().__init__()
        self.x = x
        self.y = y
        self.dim = dim
        self.index = x * self.dim + y
        self.update_g(gscore)             
        self.parent = parent
        # self.children = None

    def update_g(self, gscore: int):
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


def func_Astar(start, goal, maze, dim):

    fringe = PriorityQueue()
    fringe.put(PrioritizedItem(start.get_fscore(), start))

    visited = set()

    trajectory = [start.getIndex()]

    while not fringe.empty():
        current = fringe.get().item
        if current.getIndex() in visited:
            continue
        visited.add(current.getIndex())
        trajectory.append(current.getIndex())

        """
        print('-----')
        print('current')
        print(current.getIndex())
        """

        if [current.x, current.y] == goal:
            return current

        currentg = current.get_gscore()
        children = current.getChildren()

        for child in children:
            if maze[child[0]][child[1]] != 1 and (child[0] * dim + child[1] not in visited):
                child_cell = Cell(child[0], child[1], currentg + 1, dim, current)
                fringe.put(PrioritizedItem(child_cell.get_fscore(), child_cell))

                """
                print('child')
                print(str(child[0] * dim + child[1]) + ',' + str(child_f))
                """             
                
    return 'no solution'














