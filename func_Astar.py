import numpy as np
from queue import PriorityQueue

# PrioritizedItem is used to configure the priority queue
# such that it will only compare the priority, not the item
from dataclasses import dataclass, field
from typing import Any
@dataclass(order=True)
class PrioritizedItem():
    priority: int
    item: Any=field(compare=False)


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
            maze_child = maze.get_cell(child[0], child[1])
            if maze_child.flag != 1 and (child[0] * dim + child[1] not in visited):
                #here update cell of maze
                maze_child.update_gscore(currentg + 1)
                maze_child.update_parent(current)
                #child_cell = Cell(child[0], child[1], currentg + 1, dim, current)
                fringe.put(PrioritizedItem(maze_child.get_fscore(), maze_child))

                """
                print('child')
                print(str(child[0] * dim + child[1]) + ',' + str(child_f))
                """             
                
    return 'no solution'














