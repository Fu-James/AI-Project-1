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
    print(gw)
    plt.figure(num="maze", figsize=(8, 8), tight_layout=True)
    plt.imshow(gw.gridworld)

    algorithm = Repeated_Astar(dim, p, [0, 0], [dim-1, dim-1], gw)
    solution = algorithm.find_path()
    if solution == 'no solution':
        print('No solution')
    else:
        for cell in solution:
            gw.gridworld[cell.x][cell.y] = 0.5
        plt.figure(num="solution", figsize=(8, 8), tight_layout=True)
        plt.imshow(gw.gridworld)
    plt.show()            

if __name__ == "__main__":
    main()
