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


# implementation fo breadth-first search algorithm
def bfs(initial_state, possible_actions=actions):
    frontier = []
    # initialising the frontier list with the initial state.
    # each state is a tuple made of the maze and the list of actions that led there
    frontier.append((np.copy(initial_state), []))
    start = time.time()

    # keep searching while there is elements in the frontier
    while frontier:
        # we treat the frontier as a queue, so we remove the first element of the list
        state = frontier.pop(0)
        if is_goal_state(state[0]):
            return state

        for action in possible_actions:
            if validate_action(state[0], action):
                new_state = apply_action(state[0], action)
                new_actions = state[1].copy()
                new_actions.append(action)
                # add the new state to the frontier
                frontier.append((new_state, new_actions))

                end = time.time()
                if end-start > 10:
                    raise TimeoutError("Execution is taking too long to terminate.")


# implementation fo depth-first search algorithm
def dfs(initial_state, possible_actions=actions):
    if possible_actions is None:
        possible_actions = actions
    frontier = []
    frontier.append((np.copy(initial_state), []))

    start = time.time()

    while frontier:
        # we treat the frontier as a stack, so we remove the last element of the list
        state = frontier.pop()

        if is_goal_state(state[0]):
            return state

        for action in possible_actions:
            if validate_action(state[0], action):
                new_state = apply_action(state[0], action)
                new_actions = state[1].copy()
                new_actions.append(action)
                frontier.append((new_state, new_actions))

        end = time.time()
        if end - start > 10:
            raise TimeoutError("Execution is taking too long to terminate.")


def main():
    maze = generate_maze(8)
    prettify_maze(maze)
    solution = dfs(maze)
    apply_actions(maze, solution[1], print_actions=True)
    print(f"plan found: {str(solution[1])}")


main()
