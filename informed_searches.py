import numpy as np
import time


def generate_maze(size):
    # create an empty maze with walls = 1 and paths = 0
    maze = np.ones((size, size), dtype=int)

    maze[1:-1, 1:-1] = np.random.choice([0, 1], size=(size - 2, size - 2), p=[0.7, 0.3])

    start = (np.random.randint(1, size - 1), np.random.randint(1, size - 1))
    exit = (np.random.randint(1, size - 1), np.random.randint(1, size - 1))

    maze[start] = 2
    maze[exit] = 3

    return maze


# here the numbers are replaces with Xs and o E for visual purposes
def prettify_maze(maze):
    if not type(maze) is np.ndarray:
        return "this is not a maze"
    for row in maze:
        for element in row:
            if element == 0:
                print(" ", end=' ')
            elif element == 1:
                print("X", end=' ')
            elif element == 2:
                print("o", end=' ')
            elif element == 3:
                print("E", end=' ')
            else:
                print(element, end=' ')
        print()


actions = ["UP", "LEFT", "DOWN", "RIGHT"]

# this controls the behavior of an action
def apply_action(maze, action):
    x, y = np.where(maze == 2)
    pr = x[0]
    pc = y[0]
    movement_tuple = (0, 0)
    if action == "UP":
        movement_tuple = (-1, 0)
    elif action == "DOWN":
        movement_tuple = (1, 0)
    elif action == "LEFT":
        movement_tuple = (0, -1)
    elif action == "RIGHT":
        movement_tuple = (0, 1)

    if action in actions:
        # if the action leads into a wall do not move
        if maze[pr + movement_tuple[0], pc + movement_tuple[1]] == 1:
            return None
        else:
            new_maze = np.copy(maze)
            new_maze[pr + movement_tuple[0], pc + movement_tuple[1]] = 2
            new_maze[pr, pc] = 0
            return new_maze


def validate_action(maze, action):
    return type(apply_action(maze, action)) is np.ndarray


# this applies the series of actions inputted
def apply_actions(maze, actions, print_actions=False):
    new_maze = np.copy(maze)
    if print_actions:
        prettify_maze(maze)

    for action in actions:
        if validate_action(new_maze, action):
            new_maze = apply_action(new_maze, action)
            if print_actions:
                print("\nACTION:", action)
                prettify_maze(new_maze)
        else:
            return None

    return new_maze


# here we define the goal state
def is_goal_state(state):
    return not 3 in state

# checks if there is no 3 because that means it is being overwritten by the person (2)


# implementation of A* search

cost_per_move = 1


# the g cost depends on the number of actions
def compute_g(state):
    return len(state[1])*cost_per_move


# the h cost is calculated as the manhattan distance between
# the location of the agent in the state and the location of the exit
def compute_h(state):
    if is_goal_state(state[0]):
        return 0
    x,y = np.where(state[0] == 2)
    a,b = np.where(state[0] == 3)

    pr = x[0]
    pc = y[0]
    er = a[0]
    ec = b[0]
    manhattan_distance = (abs(pr-er)+abs(pc-ec))*cost_per_move
    return manhattan_distance


def astar_no_redundant(initial_state, possible_actions=actions):
    frontier = []
    # initialise the frontier with the initial status
    # each state is a tuple, with the maze as the first element,
    # and the list of actions that led there as the second
    frontier.append((np.copy(initial_state),[]))

    start = time.time()

    # keep searching while we have elements in the frontier,
    # or until the goal state is reached

    # this is the list of maze configurations for states we have already explored
    visited_mazes = []

    while frontier:
        # instead of popping the first/last element (as per uninformed search)
        # we search for the element with the lowest f cost (g+h)

        state_index = 0
        state = frontier[state_index]

        for i in range(1, len(frontier)):
            if ((compute_g(frontier[i]) + compute_h(frontier[i])) < (compute_g(state) + compute_h(state))):
                state = frontier[i]
                state_index = i

        state = frontier.pop(state_index)

        redundant = False
        for visited_maze in visited_mazes:
            if np.all(np.array(visited_maze) == np.array(state[0])):
                redundant = True

        if not redundant:
            visited_mazes.append(state[0])
            if is_goal_state(state[0]):
                return state

            for action in possible_actions:
                # if the action is applicable in the given state
                if validate_action(state[0], action):
                    # apply the action
                    new_state = apply_action(state[0], action)
                    new_actions = state[1].copy()
                    new_actions.append(action)
                    # add the new state in the frontier
                    frontier.append((new_state, new_actions))

            # while not always necessary, it is a good idea in practice
            # to limit the execution of a potentially non-terminating
            # algorithm. For example by limiting the time it has available
            # before forcing it to terminate
            end = time.time()
            if end - start > 2:
                raise TimeoutError("Execution is taking too long to terminate.")


def main():
    maze = generate_maze(20)
    prettify_maze(maze)
    solution = astar_no_redundant(maze)
    apply_actions(maze, solution[1], print_actions=True)
    print(f"plan found: {str(solution[1])}")

main()