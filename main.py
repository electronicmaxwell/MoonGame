import numpy as np
from itertools import zip_longest, permutations
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

TICK_PARAM_KWARGS = {
    'axis': 'both',
    'which': 'both',
    'bottom': False,
    'left': False,
    'labelbottom': False,
    'labelleft': False
}

YES_NO_DICT = {
    'yes': True,
    'y': True,
    'ok': True,
    'okay': True,
    'no': False,
    'n': False
}

CUSTOM_COLORMAP1 = ListedColormap(['#0f0f0f', '#474c52', '#2fa2a8', '#67bf67', '#faec23'])
CUSTOM_COLORMAP2 = ListedColormap(['#0f0f0f', '#474c52'])


def main():
    print('''Welcome to the Moon Game!
You are a scientist at Nasa working working on a moon rover. 
It is programmed to collect and study stones.
Your task? Simple. Collect all of the stones from the moons surface!''')
    fake_prompts(0)
    print('''Now don\'t get ahead of yourself. 
Right now we\'re still in the R&D phase of this robot.
As such you get to decide how big the moon is.
In future sessions we will be able to adjust more parameters.''')

    # creates first moon
    n_stones = 2
    _, moon = get_moon(n_stones)
    print('\n\n\n\n\n\n\n\n')

    # displays first moon
    fake_prompts(1)
    visualise_moon(moon)

    # finds and creates shortest path
    fake_prompts(2)
    coordinate_path, total_distance = lazy_algorithm(moon, n_stones)
    plot_path_cute(moon, coordinate_path, total_distance)

    # creates a moon where the lazy algorithm clearly doesn't create the shortest path for 5 stones
    fake_prompts(3)
    n_stones = 5
    lazy_distance = 64
    optimal_distance = 64
    while not optimal_distance + 5 < lazy_distance:
        moon = np.array([0] * (8 * 8 - n_stones) + [1] * n_stones)
        np.random.shuffle(moon)
        moon = np.reshape(moon, (-1, 8))
        lazy_path, lazy_distance = lazy_algorithm(moon, n_stones)
        optimal_path, optimal_distance = optimal_algorithm(moon, n_stones)

    # visualises the second moon
    fake_prompts(4)
    visualise_moon(moon)

    # display the clearly not optimal path
    fake_prompts(5)
    plot_path_cute(moon, lazy_path, lazy_distance)

    # display the optimal path
    fake_prompts(6)
    plot_path_cute(moon, optimal_path, optimal_distance)

    # decides whether game will be continued
    is_continue = end_game(0)
    while is_continue:
        # if player decides to continue the game they enter a sort of 'new game plus' where they have more control
        # over the game. They get to decide five parameters: number of stones, size of the moon, pathing algorithm,
        # starting location, and color of the rover
        print('''Welcome to free play mode!
In this mode you will get to control many more aspects of the moon than in the main game.
Let's begin!''')
        # sets number of stones
        n_stones = get_n_stones()
        # initialise moon
        moon_size, moon = get_moon(n_stones)
        # choose algorithm
        algo = get_algorithm()
        # set starting location
        starting_location = get_starting_location(moon_size)
        # set rover color
        new_color_map = get_rover_color()

        # visualise moon
        fake_prompts(7)
        visualise_moon(moon)

        # create path depending on algorithm chosen
        if algo == 'lazy':
            coordinate_path, total_distance = lazy_algorithm(moon, n_stones, starting_location)
        else:
            coordinate_path, total_distance = optimal_algorithm(moon, n_stones, starting_location)

        # plot path
        fake_prompts(8)
        plot_path_cute(moon, coordinate_path, total_distance, new_color_map)

        # Player decides if they want to create another moon. If no then the script ends. If yes code returns to
        # the top of the while loop
        is_continue = end_game(1)

    print('Thanks for Playing! Have a great day :0')


def get_moon(n_stones):
    moon_size = input("How big is your fake moon (5, 6, 7, or 8)? ")
    # Check that moon size is an integer
    if moon_size.isnumeric():

        # Convert to integer
        moon_size = int(moon_size)

        # Check that moon size is between 5 and 8
        if 5 <= moon_size <= 8:
            # Create a 1D NumPy array with the correct number of stones and empty spots
            moon = np.array([0] * (moon_size * moon_size - n_stones) + [1] * n_stones)
            # Shuffle the array to randomise the locations of the stones
            np.random.shuffle(moon)
            # Convert to square 2D array to have a square moon surface
            moon = np.reshape(moon, (-1, moon_size))

            # Return the moon size and the generated moon surface
            return moon_size, moon

        else:
            # If moon size is too small or too large, rerun function to get new input
            print("**YOUR INPUT MUST BE 5, 6, 7, OR 8**")
            return get_moon(n_stones)

    else:
        # If moon size is not an integer, rerun function to get new input
        print("**YOUR INTEGER WAS NOT AN INPUT**")
        return get_moon(n_stones)


def get_n_stones():
    # Performs the same function as get_moon but for the number of stones
    n_stones = input('How many stones must the robot collect? ')
    if n_stones.isnumeric():
        n_stones = int(n_stones)
        if 2 <= n_stones <= 8:
            return n_stones
        else:
            print('**THE ROBOT MUST COLLECT AT LEAST 2 AND AT MOST 8 STONES**')
            return get_n_stones()
    else:
        print('**YOUR INPUT MUST NOT BE AN INTEGER**')
        return get_n_stones()


def get_algorithm():
    algo = input('Would you like to use the lazy or optimal algorithm? ').strip().lower()
    if algo == 'lazy' or algo == 'optimal':
        return algo
    else:
        print('PLEASE INPUT \'lazy\' OR \'optimal\'')
        return get_algorithm()


def get_starting_location(moon_size):
    col = input('What column would you like to start on? ')
    row = input('What row would you like to start on? ')
    for elem in [col, row]:
        if elem.isnumeric():
            if 0 <= int(elem) <= moon_size - 1:
                continue
            else:
                print('**YOU HAVE ENTERED A ROW OR COLUMN THAT DOESN\'EXIST**')
                print(f'**BOTH MUST BE BETWEEN (AND INCLUDING) 0 AND {moon_size - 1}**')
                return get_starting_location(moon_size)
        else:
            print('**ONE OF YOUR INPUTS WAS NOT AN INTEGER**')
            return get_starting_location(moon_size)

    return (int(row), int(col))


def get_rover_color():
    print('Your rover can be red, orange, purple, yellow, or brown.')
    color = input('What color would you like your rover to be? ').strip().lower()
    if color in ['red', 'orange', 'yellow', 'purple', 'brown']:
        return ListedColormap(['#0f0f0f', '#474c52', '#2fa2a8', '#67bf67', color])
    else:
        print("**YOU MUST SELECT 'red', 'orange', 'yellow', 'purple', or 'brown'**")
        return get_rover_color()


def fake_prompts(n_prompt):
    # Fake prompts that give the player an illusion of choice. Prompts are there to progress the story. The function
    # matches user input to YES_NO_DICT. Will run indefinitely unless yes, y, ok, or okay are inputted,
    prompts = {
        0: 'Are you ready to begin? ',
        1: '''We are about to visualise the moon.
Its surface will appear in black and stones will appear in gray.
Now listen to these instructions carefully. 
A new window will appear with a representation of the moon.
When you are done analysing the moon, close this window to continue.
Are you ready to see the moon? ''',
        2: '''What a pretty moon!
Can you see the smallest path?
We will now calculate it together, step by step :)
The rover's current position will appear in yellow.
The path it has taken will appear in blue.
Collected stones will appear in green.
Close the first window that appears to continue with the program.
Please *DO NOT CLOSE* the second blank window that appears. 
Just click back to the terminal or the program will not run properly.
Type yes when you are ready to begin the rover's journey. ''',
        3: '''Wow that was fast! You found the quickest path!
Think you can find the quickest path with more stones? ''',
        4: '''We are about to visualise the new moon.
We have automatically set the size of the moon to 8 and the number of stones to 5.
Again, you must close the window to continue.
Are you ready to see the new moon? ''',
        5: '''Let\'s find the shortest path again together.
Please *DO NOT CLOSE* the second blank window that appears. 
Just click back to the terminal or the program will not run properly.
Ready? ''',
        6: '''Hmmm...
That doesn't seem right...
There is definitely a shorter path!
Please *DO NOT CLOSE* the second blank window that appears. 
Just click back to the terminal or the program will not run properly.
Type yes when you think you have found it :) ''',
        7: 'Are you ready to see the moon? ',
        8: '''We are about to visualise the path.
Please *DO NOT CLOSE* the second blank window that appears. 
Just click back to the terminal or the program will not run properly.
Are you ready to see the path? '''
    }

    ipt = input(prompts[n_prompt]).strip().lower()
    if ipt in YES_NO_DICT:
        if not YES_NO_DICT[ipt]:
            print('**SORRY! WE LIED. YOU HAVE NO CHOICE. YOUR INPUT MUST BE YES >:)')
            return fake_prompts(n_prompt)
    else:
        print('**YOUR INPUT MUST BE YES OR NO**')
        return fake_prompts(n_prompt)
    print('\n\n\n\n\n\n\n\n')


def end_game(n_prompt):
    # Thanks player for completing the main story. Offers an additional mode to play. Outputs true or false.
    prompts = {
        0: '''Thanks for all your help!
NASA commends you and will name a moon rover after you :D
The main game is now over.
However! You can continue playing the free play mode for as long as you like.
In this mode you can design your own moon and robot.
Would you like to try it out? ''',
        1: '''Would you like to play again? '''
    }
    is_continue = input(prompts[n_prompt]).strip().lower()
    if is_continue in YES_NO_DICT:
        print('\n\n\n\n\n\n\n\n')
        return YES_NO_DICT[is_continue]
    else:
        print('**YOUR INPUT MUST BE YES OR NO**')
        return end_game(n_prompt)


def visualise_moon(moon):
    # Visualises the moon as a color array. Turns unique values in a numpy array into colors.
    plt.imshow(moon, cmap=CUSTOM_COLORMAP2)
    plt.show(block=False)
    plt.pause(100000)
    plt.clf()


def distance_between_nodes(node1, node2):
    # Finds the distance between any two coordinate pairs
    return abs(node1[0]-node2[0]) + abs(node1[1]-node2[1])


def find_nodes(moon, n_stones):
    # Returns a list of the locations of all stones on the moon
    locations = np.where(moon == 1)
    return [(locations[0][i], locations[1][i]) for i in range(n_stones)]


def create_coordinate_path(node_path):
    # Function is inputted a list of nodes. Elements in the list are in the order they will be visited.
    # i.e. node_path[0] is the starting point, node_path[1] is the next destination, ...
    # Function outputs a coordinate path connecting all the points
    node_path_copy = node_path.copy()
    coordinate_path = []

    # Elements from node_path_copy are removed as they are used. While statement ensures a path between all points is
    # made while avoiding errors
    while len(node_path_copy) > 1:
        # Take the first and second elements of node_path_copy. Find their column and row.
        node1, node2 = node_path_copy[0], node_path_copy[1]
        node1_col, node1_row = node1[1], node1[0]
        node2_col, node2_row = node2[1], node2[0]

        # Decides whether the path goes left or right. if col values are equal then nothing happens
        if node1_col < node2_col:
            for i in range(node1_col, node2_col + 1):
                coordinate_path.append((node1_row, i))
        elif node1_col > node2_col:
            for i in range(node1_col, node2_col - 1, -1):
                coordinate_path.append((node1_row, i))

        # Decides whether path goes up or down. if row values are equal then nothing happens
        if node1_row < node2_row:
            for i in range(node1_row, node2_row + 1):
                coordinate_path.append((i, node2_col))
        elif node1_row > node2_row:
            for i in range(node1_row, node2_row - 1, -1):
                coordinate_path.append((i, node2_col))

        # Remove the first element of the list. This allows the function to iterate through all sequential pairs of nodes
        node_path_copy.pop(0)

    # Removes any duplicates that occur when creating the coordinate path
    coordinate_path = [coord1 for coord1, coord2 in zip_longest(coordinate_path, coordinate_path[1:]) if coord1 != coord2]
    return coordinate_path


def lazy_algorithm(moon, n_stones, starting_node=(0, 0)):
    # Function creates a path between all stones. It is called lazy because it simply looks at the closest
    # stone without thinking about the optimal path. Returns a list of coordinates to travel and distance of the path.
    nodes = find_nodes(moon, n_stones)

    node_path = [starting_node]
    total_distance = 0
    # While loop finds the distance between every node in nodes and the last entry in node_path. It selects the node
    # with the smallest distance to the last entry in node_path. Then it takes this node, appends it to node_path,
    # removes it from nodes, and adds the distance to total_distance. This is repeated until nodes is empty
    while nodes:
        distances = [distance_between_nodes(node_path[-1], node) for node in nodes]
        smallest_distance = min(distances)

        node_path.append(nodes.pop(distances.index(smallest_distance)))
        total_distance += smallest_distance

    # creates coordinate path
    coordinate_path = create_coordinate_path(node_path)

    return coordinate_path, total_distance


def optimal_algorithm(moon, n_stones, starting_node=(0, 0)):
    # imagine 4 stones, [A, B, C, D], must be collected. this function creates all permutations of this list, appends
    # the starting point to the front of the list (i.e. every possible path that connects every stone). it finds the
    # distance of every path and selects the shortest one. This will guarantee find the shortest path every time but is
    # very computationally taxing for any amount of stones above 8.
    stone_nodes = find_nodes(moon, n_stones)
    shortest_distance = np.Inf
    shortest_path = []
    for permutation in permutations(stone_nodes):
        path = [starting_node] + list(permutation)
        distance = sum([distance_between_nodes(node, path[i+1]) for i, node in enumerate(path[:-1])])
        if distance < shortest_distance:
            shortest_distance = distance
            shortest_path = path

    coordinate_path = create_coordinate_path(shortest_path)

    return coordinate_path, shortest_distance


def plot_path_cute(moon, coordinate_path, total_distance, color_map=CUSTOM_COLORMAP1):
    # function creates a pretty plot of the coordinate path
    moon_copy = moon.copy().astype(np.float32)

    # initialises figure. number of axes needed varies from moon to moon so this ensures there will always be enough
    # axes
    n_fig_rows_cols = int(np.ceil((total_distance + 1) ** 0.5))
    fig, _ = plt.subplots(ncols=n_fig_rows_cols, nrows=n_fig_rows_cols, figsize=(9, 9))

    for i, coord in enumerate(coordinate_path):
        # checks whether current coordinate is a stone
        is_stone = True if moon[coord] == 1 else False
        # marks current position (displays yellow on graph)
        moon_copy[coord] = 4

        # plots a color array of current step
        fig.axes[i] = fig.axes[i].imshow(moon_copy, cmap=color_map)
        # removes x and y ticks, makes the graph look more visually pleasing
        fig.axes[i].tick_params(**TICK_PARAM_KWARGS)

        # titles current step depending on whether a stone i found
        if is_stone:
            fig.axes[i].set_title(f'Stone Found!')
        else:
            fig.axes[i].set_title(f'Step {i + 1}')

        # updates current coordinate so that is shows up green if a stone is found and blue if no stone is found in the
        # next graph
        moon_copy[coord] = 3 if is_stone else 2

    # removes extra axes
    for ax in fig.axes[total_distance + 1:]:
        fig.delaxes(ax)

    # displays figure
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(100000)
    plt.clf()


# Start the program by calling the main() function
if __name__ == "__main__":
    main()