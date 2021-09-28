from queue import PriorityQueue
from heuristics import heuristics
from queue import SimpleQueue
from func_Astar import *
from Q6Q7_function import *

def func_BFS(start: Cell, goal: list, maze, dim: int, processed) -> Cell:
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
    fringe = SimpleQueue()
    fringe.put(start)

    visited = set()
    #set is implemented as a hash table in Python
    #We can expect to lookup/insert/delete in O(1) average

    while not fringe.empty():
        current = fringe.get()
        if current.get_index() in visited:
            continue
        visited.add(current.get_index())
        processed = processed + 1

        if [current.x, current.y] == goal:
            return current, 'solution', processed

        children = current.get_children()

        for child in children:
            #maze_child = maze.get_cell(child[0], child[1])
            if maze[child[0], child[1]] != 1 and (child[0] * dim + child[1] not in visited):
                c = Cell(child[0], child[1], 0, dim, current)
                fringe.put(c)

    return None, 'no_solution', processed


def fun_repeated_BFS(initial_maze, dim ):

    start_cell = Cell(0, 0, 0, dim, None)
    knowledged_maze = np.zeros([dim, dim])
    discovered_maze = np.ones([dim, dim])
    processed = 0

    while True:
        # planning path using A*
        goal_cell, status, processed = func_BFS(start_cell, [dim - 1, dim - 1], knowledged_maze, dim, processed)
        if status == 'no_solution':
            return 'no_solution', 0, discovered_maze, processed
        # get the path planned by A*, reverse order
        path = generate_path(goal_cell)

        # check and update knowledge
        isBlock = False
        while path and isBlock is False:
            current = path.pop()
            # if one cell along the path is blocked, then replanning
            if initial_maze[current.x, current.y] == 1:
                knowledged_maze[current.x, current.y] = 1
                start_cell = current.get_parent()
                isBlock = True
            # if the current cell is not blocked, then update neighbour knowledge
            else:
                discovered_maze[current.x, current.y] = 0
                children = current.get_children()
                for child in children:
                    if initial_maze[child[0], child[1]] == 1:
                        knowledged_maze[child[0], child[1]] = 1
                    else:
                        discovered_maze[child[0], child[1]] = 0
        # if there is no block along the path, then it is a solution
        if isBlock is False:
            trajectory = generate_path(goal_cell)
            return 'solution', len(trajectory), discovered_maze, processed






def fun_repeated_BFS_Q7(initial_maze, dim ):

    start_cell = Cell(0, 0, 0, dim, None)
    knowledged_maze = np.zeros([dim, dim])
    discovered_maze = np.ones([dim, dim])
    processed = 0

    while True:
        # planning path using A*
        goal_cell, status, processed = func_BFS(start_cell, [dim - 1, dim - 1], knowledged_maze, dim, processed)
        if status == 'no_solution':
            return 'no_solution', 0, discovered_maze, processed
        # get the path planned by A*, reverse order
        path = generate_path(goal_cell)

        # check and update knowledge
        isBlock = False
        while path and isBlock is False:
            current = path.pop()
            # if one cell along the path is blocked, then replanning
            if initial_maze[current.x, current.y] == 1:
                knowledged_maze[current.x, current.y] = 1
                start_cell = current.get_parent()
                isBlock = True
            # if the current cell is not blocked, then update neighbour knowledge
            else:
                discovered_maze[current.x, current.y] = 0

        # if there is no block along the path, then it is a solution
        if isBlock is False:
            trajectory = generate_path(goal_cell)
            return 'solution', len(trajectory), discovered_maze, processed




def fun_repeated_BFS_test(initial_maze, dim ):

    start_cell = Cell(0, 0, 0, dim, None)
    knowledged_maze = np.zeros([dim, dim])
    discovered_maze = np.ones([dim, dim])
    processed = 0

    while True:
        # planning path using A*
        goal_cell, status, processed = func_BFS(start_cell, [dim - 1, dim - 1], knowledged_maze, dim, processed)
        if status == 'no_solution':
            return 'no_solution', [], discovered_maze, processed, knowledged_maze
        # get the path planned by A*, reverse order
        path = generate_path(goal_cell)

        # check and update knowledge
        isBlock = False
        while path and isBlock is False:
            current = path.pop()
            # if one cell along the path is blocked, then replanning
            if initial_maze[current.x, current.y] == 1:
                knowledged_maze[current.x, current.y] = 1
                start_cell = current.get_parent()
                isBlock = True
            # if the current cell is not blocked, then update neighbour knowledge
            else:
                discovered_maze[current.x, current.y] = 0
                children = current.get_children()
                for child in children:
                    if initial_maze[child[0], child[1]] == 1:
                        knowledged_maze[child[0], child[1]] = 1
                    else:
                        discovered_maze[child[0], child[1]] = 0
        # if there is no block along the path, then it is a solution
        if isBlock is False:
            trajectory = generate_path(goal_cell)
            return 'solution', trajectory, discovered_maze, processed, knowledged_maze



def fun_repeated_BFS_tracking(initial_maze, dim ):

    start_cell = Cell(0, 0, 0, dim, None)
    knowledged_maze = np.zeros([dim, dim])
    discovered_maze = np.ones([dim, dim])
    processed = 0

    while True:
        print('-----------start of one loop-----------------')
        print(knowledged_maze)
        # planning path using A*
        print('-------starting point----')
        print(start_cell.x)
        print(start_cell.y)
        print(start_cell.get_gscore())
        print(start_cell.get_heuristic())
        goal_cell, status, processed = func_BFS(start_cell, [dim - 1, dim - 1], knowledged_maze, dim, processed)
        print('-----------after run one A*-----------------')
        if status == 'no_solution':
            print('-----------no solution from A*-----------------')
            return 'no_solution', [], discovered_maze, processed, knowledged_maze
        # get the path planned by A*, reverse order
        path = generate_path(goal_cell)

        # check and update knowledge
        isBlock = False
        print('-------check planned path----------------')
        while path and isBlock is False:
            current = path.pop()
            # if one cell along the path is blocked, then replanning
            if initial_maze[current.x, current.y] == 1:
                print('-------planned path is blocked----------------')
                knowledged_maze[current.x, current.y] = 1
                start_cell = current.get_parent()
                isBlock = True
            # if the current cell is not blocked, then update neighbour knowledge
            else:
                discovered_maze[current.x, current.y] = 0
                children = current.get_children()
                for child in children:
                    if initial_maze[child[0], child[1]] == 1:
                        knowledged_maze[child[0], child[1]] = 1
                    else:
                        discovered_maze[child[0], child[1]] = 0
            print('---------------end of planned path-----------')
        # if there is no block along the path, then it is a solution
        if isBlock is False:
            print('-------return solution----------------')
            trajectory = generate_path(goal_cell)
            return 'solution', trajectory, discovered_maze, processed, knowledged_maze
        print('-----------end of one loop-----------------')