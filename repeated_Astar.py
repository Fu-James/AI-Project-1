from func_Astar import *
from gridworld import Gridworld

class Repeated_Astar():
    def __init__(self, dim: int, p: float, start: list, goal: list, maze: Gridworld):
        self._dim = dim
        self._start = start
        self._goal = goal
        self._maze = maze
        self._knowledge = [[0 for i in range(self._dim)] for j in range(self._dim)]

    def path_walker(self, path: list):
        while path:
            current = path.pop()
            if self._maze.gridworld[current.x][current.y] == 1:
                return current.parent
            children = current.getChildren()
            for child in children:
                self._knowledge[child[0]][child[1]] = self._maze.gridworld[child[0]][child[1]]
        return 'find the solution'

    def generate_path(self, current: Cell) -> list:
        path = []
        path.append(current)
        while current.parent is not None:
            current = current.parent
            path.append(current)
        return path

    def find_path(self):
        start_cell = Cell(self._start[0], self._start[1], 0, self._dim, None)
        goal_cell = func_Astar(start_cell, self._goal, self._knowledge, self._dim)
        if goal_cell == 'no solution':
            return 'no solution'
        path = self.generate_path(goal_cell)
        stop_cell = self.path_walker(path)
        if stop_cell == 'find the solution':
            return self.generate_path(goal_cell)
        while True:
            goal_cell = func_Astar(stop_cell, self._goal, self._knowledge, self._dim)
            if goal_cell == 'no solution':
                return 'no solution'
            path = self.generate_path(goal_cell)
            stop_cell = self.path_walker(path)
            if stop_cell == 'find the solution':
                return self.generate_path(goal_cell)
