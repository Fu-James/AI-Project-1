from func_Astar import *
from gridworld import Gridworld


class Repeated_Astar():
    """
    Create a Repeated A* agent with the given unexplored maze, dimension, start, and goal cell.
    Parameters:
    ----------
    dim : Dimension of the gridworld as a int.
    p : Probability that each cell would be blocked as a float. (0 < p < 1).
    start : cell to start from.
    goal : goal cell to search for.
    maze: An (dim) * (dim) unexplored maze.

    Returns:
    -------
    agent: Unexplored Gridworld as a 2-D cell array. Dimension is (dim) * (dim).
    The knowledge of the agent increases as it explored through the maze to find path between the start and goal cell.
    """

    def __init__(self, dim: int, p: float, start: list, goal: list, maze: Gridworld):
        self._dim = dim
        self._start = start
        self._goal = goal
        self._maze = maze
        # Create an unblocked gridworld
        self._knowledge = Gridworld(self._dim, 0.0)

    def path_walker(self, path: list):
        """
        This function checks whether the path has any blocked cell. If the cell is not blocked, we will update the unexplored 
        maze and add this cell to out knowledge grid.

        Returns:
        -------
        blocked cell, status_string: Returns the blocked cell if present in the path along with a status string to indicate.
        If no blocked cell is found the return None.
        """
        while path:
            current = path.pop()
            if self._maze.get_cell(current.x, current.y).get_flag() == 1:
                return current.get_parent(), 'blocked'
            children = current.get_children()
            for child in children:
                self._knowledge.update_cell(self._maze.get_cell(
                    child[0], child[1]), child[0], child[1])
        return None, 'unblocked'

    def generate_path(self, current) -> list:
        """
        This function will help the agent to find the path between current and their parent cell.

        Returns:
        -------
        path: Returns a path between the current cell and it's parent until the hightes hierarchical parent is found.
        """
        path = []
        path.append(current)
        while current.get_parent() is not None:
            current = current.get_parent()
            path.append(current)
        return path

    def find_path(self):
        """
        Main function which will help the agent to find the path between start and goal cell.

        Returns:
        -------
        path, status_string: Returns a path between the start and goal node if found, otherwise will return None.
        The status string indicates if the solution is found or not.
        """
        start_cell = Cell(self._start[0], self._start[1], 0, self._dim, None)
        while True:
            goal_cell, status = func_Astar(
                start_cell, self._goal, self._knowledge, self._dim)
            if status == 'no_solution':
                return None, 'no_solution'
            path = self.generate_path(goal_cell)
            start_cell, node_status = self.path_walker(path)
            if node_status == 'unblocked':
                return self.generate_path(goal_cell), 'solution'
