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
            return current

        currentg = current.get_gscore()
        children = current.get_children()

        for child in children:
            maze_child = maze.get_cell(child[0], child[1])
            if maze_child.get_flag() != 1 and (child[0] * dim + child[1] not in visited):
                maze_child.update_gscore(currentg + 1)
                maze_child.update_parent(current)
                fringe.put(PrioritizedItem(
                    maze_child.get_fscore(), maze_child))

    return None
