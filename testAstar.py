from func_Astar import *
import numpy as np

dim = 10
option = 0
gw = Gridworld(dim, 0.1)
print("Generated Gridworld:")
print(gw)


start = Cell(0, 0, 0, dim, None)
solution, status, explored = func_Astar(
    start, [dim-1, dim-1], gw, dim, option=option)

while solution is not None:
    gw.get_cell(solution.x, solution.y).update_flag(5)
    solution = solution.get_parent()
print("Solved GridWorld:")
print(gw)
