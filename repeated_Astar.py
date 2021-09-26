from func_Astar import *
from gridworld import Gridworld


class Repeated_Astar():
    """
    Create a Repeated A* agent with the given unexplored maze, dimension, start, and goal cell.
    Parameters:
    ----------
    dim : Dimension of the gridworld as a int.
    start : cell to start from.
    goal : goal cell to search for.
    maze: An (dim) * (dim) unexplored maze.

    Returns:
    -------
    agent: Unexplored Gridworld as a 2-D cell array. Dimension is (dim) * (dim).
    The knowledge of the agent increases as it explored through the maze to find path between the start and goal cell.
    """
    def __init__(self, dim: int, start: list, goal: list, maze: Gridworld, backtrack: bool = False):
        self._dim = dim
        self._start = start
        self._goal = goal
        self._maze = maze
        # Create an unblocked gridworld
        self._knowledge = Gridworld(self._dim, 0.0)
        self._backtrack = backtrack

    def backtrack(self, current: Cell) -> Cell:
        """
        This function is designed for Q8. 
        When the agent walk to the end of a hallway, it would backtrack to the other end.
        Therefore we would get to a better point restarting the A* search.
        
        Returns:
        -------
        restart_cell: Returns a cell that is not in the hallway.
        """
        trajectory_backtrack = 1
        while current.get_parent() is not None:
            blocked_neighbors_count = current.get_no_of_blocked_neighbors()
            neibors_count = current.get_no_of_neighbors()
            if 4 - neibors_count + blocked_neighbors_count >= 2:
                current = current.get_parent()
            else:
                return current, trajectory_backtrack
            trajectory_backtrack += 1
        return current, trajectory_backtrack
    
    def is_end_of_hallway(self, current: Cell) -> bool:
        """
        This function is designed for Q8.
        It returns True if the agent walk to the end of a hallway.
        Otherwise, False.
        """

        blocked_neighbors_count = current.get_no_of_blocked_neighbors()
        neibors_count = current.get_no_of_neighbors()
        if 4 - neibors_count + blocked_neighbors_count >= 3:
            return True
        else:
            return False

    def path_walker(self, path: list):
        """
        This function checks whether the path has any blocked cell. If the cell is not blocked, we will update the unexplored 
        maze and add this cell to out knowledge grid.
        
        Returns:
        -------
        blocked cell, status_string: Returns the parent of the blocked cell, if a blocked cell present in the path, along with a status string to indicate.
        If no blocked cell is found the return None.
        """
        trajectory = -1
        while path:
            trajectory += 1
            current = path.pop()
            if self._maze.get_cell(current.x, current.y).get_flag() == 1:
                return current.get_parent(), 'blocked', trajectory

            children = current.get_children()
            for child in children:
                self._knowledge.update_cell(self._maze.get_cell(child[0], child[1]), 
                                            child[0], child[1])
        return None, 'unblocked', trajectory
    
    def path_walker_backtrack(self, path: list):
        """
        This function checks whether the path has any blocked cell. If the cell is not blocked, we will update the unexplored 
        maze and add this cell to out knowledge grid.

        If the cell is blocked and the agent is at the end of a hallway, it will backtrack to the nearest exit.
        
        Returns:
        -------
        blocked cell, status_string: Returns the parent of the blocked cell, if a blocked cell present in the path, along with a status string to indicate.
        If no blocked cell is found the return None.
        """
        trajectory = -1
        while path:
            trajectory += 1
            current = path.pop()
            if self._maze.get_cell(current.x, current.y).get_flag() == 1:
                current = current.get_parent()
                if current.get_parent() is not None and self.is_end_of_hallway(current):
                    current, trajectory_backtrack = self.backtrack(current.get_parent())
                    return current, 'blocked', trajectory + trajectory_backtrack
                else:
                    return current, 'blocked', trajectory

            children = current.get_children()
            blocked_neighbors_count = 0
            for child in children:
                child_cell = self._maze.get_cell(child[0], child[1])
                self._knowledge.update_cell(child_cell, child[0], child[1])
                if child_cell.get_flag() == 1:
                    blocked_neighbors_count += 1
            current.update_no_of_neighbors(len(children))
            current.update_no_of_blocked_neighbors(blocked_neighbors_count)
        return None, 'unblocked', trajectory

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
        overall_trajectory = 0
        while True:
            goal_cell, status = func_Astar(start_cell, self._goal, self._knowledge, self._dim)
            if status == 'no_solution':
                return None, 'no_solution', overall_trajectory
            path = self.generate_path(goal_cell)
            if self._backtrack:
                start_cell, node_status, trajectory = self.path_walker_backtrack(path)
            else:
                start_cell, node_status, trajectory = self.path_walker(path)
            overall_trajectory += trajectory
            if node_status == 'unblocked':
                return self.generate_path(goal_cell), 'solution', overall_trajectory