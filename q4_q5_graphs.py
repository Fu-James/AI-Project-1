import matplotlib.pyplot as plt
from gridworld import Gridworld
from func_Astar import *
import numpy as np
import time


def get_data(dim: int, grid_per_pass: int, increment_by: float, option: int):
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
    visited = []
    trajectory = []

    for increment in np.arange(0.01, 1.0, increment_by):
        solved_count = 0
        avg_time = []
        visi = []
        traj = []
        for i in range(grid_per_pass):
            total += 1
            grid = Gridworld(dim, increment, option=option)
            # Start Time
            start_time = time.process_time_ns()
            status, explored = isSolvable(start, goal, grid, dim)
            if status:
                solved_count += 1
            end_time = time.process_time_ns()
            # End Time
            visi.append(len(explored[0]))
            traj.append(len(explored[1]))
            avg_time.append((end_time - start_time))
        probability.append(increment)
        solvability.append((solved_count/grid_per_pass))
        duration.append(np.mean(avg_time))
        visited.append(np.mean(visi))
        trajectory.append(np.mean(traj))
        print("Completed for {:.2f} probability, {} grids were solved, Solvability: {:.2f}, and avg time per grid: {:.2f}".format(
            increment, solved_count, (solved_count/grid_per_pass), np.mean(avg_time)))

    print("\n\nTotal ({} X {})Grids Checked: {}\n\n".format(dim, dim, total))

    return probability, solvability, duration, visited, trajectory


def isSolvable(start: Cell, goal: list, gridworld: Gridworld, dim: int) -> bool:
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
    solution, status, explored = func_Astar(start, goal, gridworld, dim)
    if status == "no_solution":
        return False, explored
    else:
        return True, explored


def get_option_name(op: int) -> str:
    return "Manhattan" if op == 0 else "Euclidean" if op == 1 else "Chebyshev"


def q4(dim: list, grid_per_pass: list, increment_by: float):
    master_result = []
    for dim in dim:
        grid_result = []
        for grid_pass in grid_per_pass:
            option_result = []
            for op in range(3):
                res = get_data(dim, grid_pass, increment_by, option=op)
                option_result.append(res)
                probability, solvability, duration, visited, trajectory = res
                font_style = {'family': 'serif', 'color': 'black', 'size': 12}
                min_dist = [abs(i - 0.5) for i in solvability]
                half_index = min_dist.index(min(min_dist))
                args = "\nGrid Dimension: {} x {}\nHeuristic: {} Distance".format(
                    dim, dim, get_option_name(op))

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
                fig.subplots_adjust(top=0.8)
                print(args)
                fig.suptitle(args)

                title = "Solvability vs Density"
                ax1.set_title(title, fontdict=font_style)
                ax1.set(xlabel="Density", ylabel="Solvability")

                ax1.set_xticks(np.arange(0.0, 1.2, 0.1))
                ax1.set_yticks(np.arange(0.0, 1.2, 0.1))
                ax1.grid()

                ax1.axvline(x=probability[half_index],
                            color='gray', linestyle='--')
                ax1.axhline(y=solvability[half_index],
                            color='gray', linestyle='--')
                ax1.plot(probability, solvability)

                title = "Time vs Density"
                ax2.set_title(title, fontdict=font_style)
                ax2.set(xlabel="Density", ylabel="Time (nanoseconds)")
                ax2.set_xticks(np.arange(0.0, 1.2, 0.1))
                ax2.grid()

                ax2.axvline(x=probability[half_index],
                            color='gray', linestyle='--')
                ax2.axhline(y=duration[half_index],
                            color='gray', linestyle='--')
                ax2.plot(probability, duration)

                # Add folder 'images'
                filename = "images/{}_x_{}_{}_pass_{}.png".format(
                    dim, dim, get_option_name(op), grid_pass)
                plt.savefig(filename)
            grid_result.append(option_result)
        master_result.append(grid_result)
    return master_result


def q5(dim: int, grid_per_pass: int, option1, option2, option3):
    probability_op1, solvability_op1, duration_op1, visited_op1, trajectory_op1 = option1
    probability_op2, solvability_op2, duration_op2, visited_op2, trajectory_op2 = option2
    probability_op3, solvability_op3, duration_op3, visited_op3, trajectory_op3 = option3

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


def create_visited_trajectory(option1, option2, option3):
    probability_op1, solvability_op1, duration_op1, visited_op1, trajectory_op1 = option1
    probability_op2, solvability_op2, duration_op2, visited_op2, trajectory_op2 = option2
    probability_op3, solvability_op3, duration_op3, visited_op3, trajectory_op3 = option3

    barWidth = 0.25
    font_style = {'family': 'serif', 'color': 'black', 'size': 12}
    fig = plt.subplots()
    plt.title("Number of Cells Visited and Trajectory Lenght",
                fontdict=font_style)

    min_dist_op1 = [abs(i - 0.5) for i in solvability_op1]
    half_index_op1 = min_dist_op1.index(min(min_dist_op1))

    min_dist_op2 = [abs(i - 0.5) for i in solvability_op2]
    half_index_op2 = min_dist_op2.index(min(min_dist_op2))

    min_dist_op3 = [abs(i - 0.5) for i in solvability_op3]
    half_index_op3 = min_dist_op3.index(min(min_dist_op3))

    op1 = [visited_op1[half_index_op1], trajectory_op1[half_index_op1]]
    op2 = [visited_op2[half_index_op2], trajectory_op2[half_index_op2]]
    op3 = [visited_op3[half_index_op3], trajectory_op3[half_index_op3]]

    br1 = np.arange(len(op1))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    plt.bar(br1, op1, width=barWidth,
            edgecolor='grey', label='Manhattan')
    plt.bar(br2, op2, width=barWidth,
            edgecolor='grey', label='Euclidean')
    plt.bar(br3, op3, width=barWidth,
            edgecolor='grey', label='Chebyshev')

    # Adding Xticks
    plt.ylabel('Cells', fontdict=font_style)
    plt.xticks([r + barWidth for r in range(len(op1))],
                ['Visited', 'Trajectory'])

    plt.legend(loc="upper right")
    plt.grid()
    filename = "images/{}_x_{}_{}_pass_{}.png".format(
        master_dim[i], master_dim[i], "Visited_Trajectory", grid_per_pass[j])
    plt.savefig(filename)
    

def split_list(result: list, split_by: float = 2.0) -> list:
    return result[:len(result)//split_by]


if __name__ == "__main__":
    master_dim = [101]
    grid_per_pass = [10, 50, 100]
    increment_by = 0.01

    master_result = q4(master_dim, grid_per_pass, increment_by)

    for i, dim in enumerate(master_result):
        for j, gpass in enumerate(dim):
            option1, option2, option3 = master_result[i][j]
            q5(master_dim[i], grid_per_pass[j], option1, option2, option3)
            create_visited_trajectory(option1, option2, option3)
