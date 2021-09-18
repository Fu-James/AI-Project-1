import numpy as np
from queue import PriorityQueue

# PrioritizedItem is used to configure the priority queue
# such that it will only compare the priority, not the item
from dataclasses import dataclass, field
from typing import Any
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)


class Cell:

    def __init__(self, x, y, gscore, dim, parent):
        self.x = x
        self.y = y
        self.dim = dim
        self.index = x * self.dim + y
        self.gscore = gscore
        self.hscore = np.abs(self.dim - 1 - x) + np.abs(self.dim - 1 - y)  # to be replaced by huristic function
        self.fscore = self.gscore + self.hscore
        self.parent = parent
        # self.children = None

    def printSelf(self):
        print('print self start')
        print(self.index)
        print(self.gscore)
        print(self.hscore)
        print(self.fscore)
        print('print self end')

    def getG(self):
        return self.gscore

    def getH(self):
        return self.hscore

    def getF(self):
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
    fringe.put(PrioritizedItem(start.getF(), start))

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

        currentg = current.getG()
        children = current.getChildren()
        for child in children:

            if maze[child[0]][child[1]] != 1 and (child[0] * dim + child[1] not in visited):
                child_f = currentg + 1 + np.abs(dim - 1 - child[0]) + np.abs(dim - 1 - child[1])
                child_parent = current
                child_cell = Cell(child[0], child[1], currentg + 1, dim, child_parent)
                fringe.put(PrioritizedItem(child_f, child_cell))

                """
                print('child')
                print(str(child[0] * dim + child[1]) + ',' + str(child_f))
                """             
                
    return 'no solution'














