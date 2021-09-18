from func_Astar import *
from gridworld import Gridworld


class Repeated_Astar():
    def __init__(self, dim: int, p: float, start: list, goal: list, maze: Gridworld):
        self._dim = dim
        self._start = start
        self._goal = goal
        self._maze = maze
        # Create an unblocked gridworld
        self._knowledge = Gridworld(self._dim, 0.0)

    def path_walker(self, path: list):
        while path:
            current = path.pop()
            if self._maze.get_cell(current.x, current.y).get_flag() == 1:
                return current.get_parent()
            children = current.get_children()
            for child in children:
                self._knowledge.update_cell(self._maze.get_cell(
                    child[0], child[1]), child[0], child[1])
        return 'find the solution'

    def generate_path(self, current) -> list:
        path = []
        path.append(current)
        while current.get_parent() is not None:
            current = current.get_parent()
            path.append(current)
        return path

    def find_path(self) -> list:
        start_cell = self._knowledge.get_cell(0, 0)
        while True:
            goal_cell = func_Astar(
                start_cell, self._goal, self._knowledge, self._dim)
            if goal_cell == None:
                return None
            path = self.generate_path(goal_cell)
            start_cell = self.path_walker(path)
            if start_cell == 'find the solution':
                return self.generate_path(goal_cell)
