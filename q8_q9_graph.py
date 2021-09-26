import matplotlib.pyplot as plt
from gridworld import *
from repeated_Astar import Repeated_Astar
import numpy as np
import time

def get_data(dim: int, grid_per_pass: int, increment_by: float, backtrack: bool):
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
    probability = []
    solvability = []
    duration = []
    overall_trajectory = []
    probability_backtrack = []
    solvability_backtrack = []
    duration_backtrack = []
    overall_trajectory_backtrack = []

    for increment in np.arange(0.01, 1, increment_by):
        solved_count = 0
        solved_count_backtrack = 0
        avg_time = []
        avg_time_backtrack = []
        total_trajectory = 0
        total_trajectory_backtrack = 0
        for i in range(grid_per_pass):
            total += 1
            grid = Gridworld(dim, increment)
            # Without backtrack
            # Start Time
            start_time = time.process_time_ns()
            solvable, trajectory = isSolvable(start, goal, grid, dim, False)
            # End Time
            end_time = time.process_time_ns()
            if solvable:
                solved_count += 1
            avg_time.append((end_time - start_time))
            total_trajectory += trajectory

            # With backtrack
            # Start Time
            start_time = time.process_time_ns()
            solvable, trajectory_backtrack = isSolvable(start, goal, grid, dim, True)
            # End Time
            end_time = time.process_time_ns()
            if solvable: 
                solved_count_backtrack += 1
            avg_time_backtrack.append((end_time - start_time))
            total_trajectory_backtrack += trajectory_backtrack

        probability.append(increment)
        solvability.append((solved_count/grid_per_pass))
        duration.append(np.mean(avg_time))
        overall_trajectory.append(total_trajectory)
        print("Without backtracking, completed for {:.2f} probability, {} grids were solved, Solvability: {:.2f}, avg time per grid: {:.2f}, and overall trajectory: {}".format(
            increment, solved_count, (solved_count/grid_per_pass), np.mean(avg_time), total_trajectory))

        probability_backtrack.append(increment)
        solvability_backtrack.append((solved_count_backtrack/grid_per_pass))
        duration_backtrack.append(np.mean(avg_time_backtrack))
        overall_trajectory_backtrack.append(total_trajectory_backtrack)
        print("With backtracking, completed for {:.2f} probability, {} grids were solved, Solvability: {:.2f}, avg time per grid: {:.2f}, and overall trajectory: {}".format(
            increment, solved_count_backtrack, (solved_count_backtrack/grid_per_pass), np.mean(avg_time_backtrack), total_trajectory_backtrack))

    print("\n\nTotal ({} X {})Grids Checked: {}\n\n".format(dim, dim, total))

    return probability, solvability, duration, overall_trajectory, probability_backtrack, solvability_backtrack, duration_backtrack, overall_trajectory_backtrack


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
            res = get_data(dim, grid_pass, increment_by, True)
            option_result.append(res)
            probability, solvability, duration, trajectory, probability_backtrack, solvability_backtrack, duration_backtrack, trajectory_backtrack = res
            font_style = {'family': 'serif', 'color': 'black', 'size': 12}
            min_dist = [abs(i - 0.5) for i in solvability]
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

            ax2.plot(probability,
                     duration, label='Without Backtrack')
            ax2.plot(probability_backtrack,
                     duration_backtrack, label='Backtrack')
            ax2.legend(loc="upper right")

            title = "Overall Trajectory vs Density"
            ax1.set_title(title, fontdict=font_style)
            ax1.set(xlabel="Density", ylabel="Overall Trajectory")
            ax1.grid()

            ax1.plot(probability,
                     trajectory, label='Without Backtrack')
            ax1.plot(probability_backtrack,
                     trajectory_backtrack, label='Backtrack')
            ax1.legend(loc="upper right")

            # Add folder 'images'
            plt.savefig("images/{}_x_{}_{}_pass_{}.png".format(dim,
                dim, "With_and_without_backtrack", grid_pass))
            grid_result.append(option_result)
        master_result.append(grid_result)
    return master_result


def q5(dim: int, grid_per_pass: int, option1, option2, option3):
    probability_op1, solvability_op1, duration_op1 = option1
    probability_op2, solvability_op2, duration_op2 = option2
    probability_op3, solvability_op3, duration_op3 = option3

    font_style = {'family': 'serif', 'color': 'black', 'size': 12}

    args = "\nGrid Dimension: {} x {}".format(dim, dim)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.subplots_adjust(top=0.8)
    fig.suptitle(args)

    title = "Solvability vs Density"
    ax1.set_title(title, fontdict=font_style)
    ax1.set(xlabel="Density", ylabel="Solvability")

    ax1.set_xticks(np.arange(0.0, 1.2, 0.1))
    ax1.set_yticks(np.arange(0.0, 1.2, 0.1))
    ax1.grid()

    ax1.plot(probability_op1, solvability_op1, label='Manhattan Distance')
    ax1.plot(probability_op2, solvability_op2, label='Euclidean Distance')
    ax1.plot(probability_op3, solvability_op3, label='Chebyshev Distance')
    ax1.legend(loc="upper right")

    title = "Time vs Density"
    ax2.set_title(title, fontdict=font_style)
    ax2.set(xlabel="Density", ylabel="Time (nanoseconds)")
    ax2.set_xticks(np.arange(0.0, 1.2, 0.1))
    ax2.grid()

    ax2.plot(probability_op1,
             duration_op1, label='Manhattan Distance')
    ax2.plot(probability_op2,
             duration_op2, label='Euclidean Distance')
    ax2.plot(probability_op3,
             duration_op3, label='Chebyshev Distance')
    ax2.legend(loc="upper right")

    plt.savefig("images/{}_x_{}_{}_pass_{}.png".format(dim,
                dim, "ALL", grid_per_pass))


if __name__ == "__main__":
    master_dim = [101]
    grid_per_pass = [100]
    increment_by = 0.02

    master_result = q8(master_dim, grid_per_pass, increment_by)

    # for i, dim in enumerate(master_result):
    #     for j, gpass in enumerate(dim):
    #         option1, option2, option3 = master_result[i][j]
    #         q5(master_dim[i], grid_per_pass[j], option1, option2, option3)