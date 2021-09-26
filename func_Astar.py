from queue import PriorityQueue
from gridworld import Cell, Gridworld

# PrioritizedItem is used to configure the priority queue
# such that it will only compare the priority, not the item
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedItem():
    priority: int
    item: Cell = field(compare=False)


def func_Astar(start: Cell, goal: list, maze: Gridworld, dim: int) -> Cell:
    """
    Create a cell.
    Parameters:
    ----------
    start : Initial search point
    goal : x and y coordinate of the goal cell
    maze : Unexplored gridworld
    dim : Dimension of the gridworld as a int.

    Returns:
    -------
    cell, status_string: Returns cell if goal node is found along with a status string.
    """
    fringe = PriorityQueue()
    fringe.put(PrioritizedItem(start.get_fscore(), start))

    visited = set()
    trajectory = [start.get_index()]

    while not fringe.empty():
        current = fringe.get().item
        if current.get_index() in visited:
            continue
        visited.add(current.get_index())
        trajectory.append(current.get_index())

        if [current.x, current.y] == goal:
            return current, 'solution', [visited, trajectory]

        currentg = current.get_gscore()
        children = current.get_children()

        for child in children:
            maze_child = maze.get_cell(child[0], child[1])
            if maze_child.get_flag() != 1 and (child[0] * dim + child[1] not in visited):
                c = Cell(child[0], child[1], (currentg + 1),
                         dim, parent=current)
                fringe.put(PrioritizedItem(
                    c.get_fscore(), c))

    return None, 'no_solution', [visited, trajectory]
