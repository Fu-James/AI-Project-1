import matplotlib.pyplot as plt
from gridworld import *
from repeated_Astar import Repeated_Astar
import numpy as np
import time

def get_data(dim: int, grid_per_pass: int, increment_by: float, options: int = 0):
    """
    Main method to get probability, solvability and duration.    
    Parameters:
    ----------
    dim : Dimension of the gridworld as a int.
    dim: Dimension of grid
    grid_per_pass: No of grids per pass for a probability
    increment_by: Increment step for probability
    option: Set heuristic option

    Returns:
    -------
    probability, solvability, duration: Returns list of probability, solvability, and duration for the maze config
    """

    start = Cell(0, 0, 0, dim, None)
    goal = [dim - 1, dim - 1]
    total = 0

    # Result list to store [probability], [solvability], and [duration]
    probability = [[] for row in range(len(options))]
    solvability = [[] for row in range(len(options))]
    duration = [[] for row in range(len(options))]
    overall_trajectory = [[] for row in range(len(options))]

    for increment in np.arange(0.02, 1, increment_by):
        solved_count = [0] * len(options)
        avg_time = [[] for row in range(len(options))]
        trajectory_per_density = [0] * len(options)
        for i in range(grid_per_pass):
            total += 1
            grid = Gridworld(dim, increment)
            for index in range(len(options)):
                # Start Time
                start_time = time.process_time_ns()
                solvable, trajectory = isSolvable(start, goal, grid, dim, options[index])
                # End Time
                end_time = time.process_time_ns()
                if solvable:
                    solved_count[index] += 1
                avg_time[index].append((end_time - start_time))
                trajectory_per_density[index] += trajectory

        for index in range(len(options)):
            probability[index].append(increment)
            solvability[index].append((solved_count[index]/grid_per_pass))
            duration[index].append(np.mean(avg_time[index]))
            overall_trajectory[index].append(trajectory_per_density[index])
            print("Option: {}, completed for {:.2f} probability, {} grids were solved, Solvability: {:.2f}, avg time per grid: {:.2f}, and overall trajectory: {}".format(
                options[index], increment, solved_count[index], (solved_count[index]/grid_per_pass), np.mean(avg_time[index]), trajectory_per_density[index]))
    print("\n\nTotal ({} X {})Grids Checked: {}\n\n".format(dim, dim, total))

    return probability, solvability, duration, overall_trajectory


def isSolvable(start: Cell, goal: list, gridworld: Gridworld, dim: int, backtrack: bool):
    """
    A utility method which returns bool based on search status 
    Parameters:
    ----------
    start : Initial search point
    goal : x and y coordinate of the goal cell
    gridworld : Unexplored gridworld
    dim : Dimension of the gridworld as a int.

    Returns:
    -------
    bool: Returns bool value according to the A* search status
    """
    agent = Repeated_Astar(dim, [0, 0], [dim-1, dim-1], gridworld, backtrack)
    solution, status, trajectory = agent.find_path()
    if status == "no_solution":
        return False, trajectory
    else:
        return True, trajectory


def get_option_name(op: int) -> str:
    return "Manhattan" if op == 0 else "Euclidean" if op == 1 else "Chebyshev"


def q8(dim: list, grid_per_pass: list, increment_by: float):
    master_result = []
    for dim in dim:
        grid_result = []
        for grid_pass in grid_per_pass:
            option_result = []
            options = [False, True]
            res = get_data(dim, grid_pass, increment_by, options)
            option_result.append(res)
            probability, solvability, duration, trajectory = res
            font_style = {'family': 'serif', 'color': 'black', 'size': 12}
            min_dist = [abs(i - 0.5) for i in solvability[0]]
            half_index = min_dist.index(min(min_dist))
            args = "\nGrid Dimension: {} x {}".format(dim, dim)

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
            fig.subplots_adjust(top=0.8)
            fig.suptitle(args)

            # title = "Solvability vs Density"
            # ax1.set_title(title, fontdict=font_style)
            # ax1.set(xlabel="Density", ylabel="Solvability")

            # ax1.set_xticks(np.arange(0.0, 1.2, 0.1))
            # ax1.set_yticks(np.arange(0.0, 1.2, 0.1))
            # ax1.grid()

            # ax1.plot(probability, solvability, label='Without Backtrack')
            # ax1.plot(probability_backtrack, solvability_backtrack, label='Backtrack')
            # ax1.legend(loc="upper right")

            title = "Time vs Density"
            ax2.set_title(title, fontdict=font_style)
            ax2.set(xlabel="Density", ylabel="Time (nanoseconds)")
            ax2.set_xticks(np.arange(0.0, 1.2, 0.1))
            ax2.grid()

            ax2.plot(probability[0],
                     duration[0], label='Without Backtrack')
            ax2.plot(probability[1],
                     duration[1], label='Backtrack')
            ax2.legend(loc="upper right")

            title = "Overall Trajectory vs Density"
            ax1.set_title(title, fontdict=font_style)
            ax1.set(xlabel="Density", ylabel="Overall Trajectory")
            ax1.grid()

            ax1.plot(probability[0],
                     trajectory[0], label='Without Backtrack')
            ax1.plot(probability[1],
                     trajectory[1], label='Backtrack')
            ax1.legend(loc="upper right")

            # Add folder 'images'
            plt.savefig("images/{}_x_{}_{}_pass_{}.png".format(dim,
                dim, "With_and_without_backtrack", grid_pass))
            grid_result.append(option_result)
        master_result.append(grid_result)
    return master_result

if __name__ == "__main__":
    master_dim = [101]
    grid_per_pass = [100]
    increment_by = 0.02

    master_result = q8(master_dim, grid_per_pass, increment_by)
