import matplotlib as ml
import matplotlib.pyplot as plt
from gridworld import Gridworld

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
    plt.figure(figsize=(5, 5))
    plt.imshow(gw.gridworld)
    plt.show()

if __name__ == "__main__":
    main()