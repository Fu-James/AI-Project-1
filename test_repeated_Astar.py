import matplotlib as ml
import matplotlib.pyplot as plt
from gridworld import Gridworld
from repeated_Astar import Repeated_Astar


def main():
    """
    A sample main function for showing how the create_gridworld function works.
    Read dimension and probabilty from user input.
    Plot the gridworld.
    """
    dim = int(input("Enter the dimension: "))
    p = float(input("Enter the probabilty: "))
    gw = Gridworld(dim, p)
    print("Initial GridWorld:")
    print(gw)
    plt.figure(num="Grid World", figsize=(8, 8), tight_layout=True)
    plt.imshow(gw.get_grid_ascii())

    agent = Repeated_Astar(dim, [0, 0], [dim-1, dim-1], gw)
    solution, status, trajectory = agent.find_path()
    if status == 'no_solution':
        print("No Solution.")
    else:
        for cell in solution:
            gw.get_cell(cell.x, cell.y).update_flag(7)
        print("Overall trajectory is:", trajectory)
        print(" Solved GridWorld:")
        print(gw)
        plt.figure(num="Solved Grid World", figsize=(8, 8), tight_layout=True)
        plt.imshow(gw.get_grid_ascii())
    plt.show()


if __name__ == "__main__":
    main()
