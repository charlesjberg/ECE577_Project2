# Imports
# import matplotlib
import numpy as np
import matplotlib.pyplot as plt

import time
import warnings
import matplotlib.animation as animation
# plt.rcParams['animation.ffmpeg_path'] = "C:/FFmpeg/bin/ffmpeg.exe"


# Calculating the distance between two cities
def distance_between_cities(city_a, city_b, city_dict):
    """Returns the distance between two cities"""
    a = city_dict[city_a]
    b = city_dict[city_b]
    x = a[0] - b[0]
    y = a[1] - b[1]
    return np.sqrt((x ** 2) + (y ** 2))

# Generating the first population set
def initial_population(city_list, n_population):
    """Returns the initial random population as an array"""
    population_set = []
    for pop in range(n_population):
        # Randomly generating a new solution
        init_pop = list(city_list[np.random.choice(list(range(1, n_cities)), n_cities - 1, replace=False)])
        init_pop.insert(0, starting_point)
        init_pop.append(starting_point)
        population_set.append(init_pop)
    return np.array(population_set)


# Calculating the total distance in a chromosome
def chromo_total_dist(city_list, city_dict):
    """Returs the total distance in each chromosome"""
    total = 0
    for i in range(n_cities - 1):
        a = city_list[i]
        b = city_list[i + 1]
        total += distance_between_cities(a, b, city_dict)
    return total


# Calculating the total distance of generation
def fitness_all_cities(population_set, cities_dict):
    """Returns each chromosome's fitness and stores as a list"""
    fitness_list0 = np.zeros(n_population)
    # Looping over all chromosomes to calculate the fitness
    for i in range(n_population):
        fitness_list0[i] = chromo_total_dist(population_set[i], cities_dict)
    return fitness_list0


# Parent selection for crossover
def parent_selection(population_set, fitness_list, numChildren):
    population_set = np.array(population_set)
    """Returns two chromosomes as two parents"""
    total_fit = fitness_list.sum()
    prob_list = total_fit / fitness_list / (sum(total_fit / fitness_list))
    parent_list_a2 = np.random.choice(list(range(len(population_set))), numChildren,
                                      p=prob_list)
    parent_list_a2 = population_set[parent_list_a2]
    parent_list_b = np.random.choice(list(range(len(population_set))), numChildren, p=prob_list)
    parent_list_b = population_set[parent_list_b]
    # Combining two populations set in an array
    return np.array([parent_list_a2, parent_list_b])


# For eliting, finding the best chromosome of each generation
def best_chromosome(generation):
    best = generation[0]
    for n in range(1, len(generation)):
        if chromo_total_dist(generation[n], cities_dict) < chromo_total_dist(best, cities_dict):
            best = generation[n]
    return best


# Defining a crossover rate for each chromosome
def crossover_rate(prog_a, prog_b):
    index1 = int(np.random.rand(1) * n_cities)
    index2 = int(np.random.rand(1) * n_cities)
    if index1 < index2:
        save = index2
        index2 = index1
        index1 = save
    index1 += 1
    offspring = np.empty((n_cities + 1))
    cross_over_elements = prog_a[index1:index2]
    i = 0
    j = 0
    for city in prog_b:
        if city in range(index1,index2):
            offspring[i] = cross_over_elements[j]
            j += 1

        elif city not in cross_over_elements:
            offspring[i] = prog_b[i]
        i += 1
    return offspring


# Crossover the parents
def crossover(parent_list):
    offspring_array = np.empty((numChildren, n_cities + 1));
    for i in range(parent_list.shape[1]):
        prog_a, prog_b = parent_list[0][i], parent_list[1][i]
        j = 0
        # CJ - Check to make sure parents arent the same
        while (prog_a.all == prog_b.all):
            prog_a, prog_b = parent_list[0][i], parent_list[1][j]
            j += 1
        offspring = crossover_rate(prog_a, prog_b)
        offspring_array[i, :] = offspring
    return offspring_array


# Mutate the new chromosomes for a given mutation rate
def mutation(offspring):
    probs = np.random.rand(len(offspring))
    outcome = [1 for prob in probs if prob < mutation_rate]
    num_mutation = sum(outcome)
    for k in range(num_mutation):
        a = np.random.randint(1, n_cities - 1)
        b = np.random.randint(1, n_cities - 1)
        offspring[a], offspring[b] = offspring[b], offspring[a]

    return offspring


def mutate_population(new_population_set):
    mutated_array = np.empty((num_chromosomes, n_cities + 1));
    i = 0
    for offspring in new_population_set:
        mutated_array[i, :] = mutation(offspring)
        i += 1
    return mutated_array


# Function to find the best score cities
def getting_new_coordinate(best_coordinate, cities_dict):
    # for i in mutated_pop:
    new_coordinate = [cities_dict[city] for city in best_coordinate]
    # new_coordinates.append(new_coordinate)
    return new_coordinate


warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

plot_size = 8
plot_width = 5
plot_height = 5
params = {'legend.fontsize': 'large',
          'figure.figsize': (plot_width, plot_height),
          'axes.labelsize': plot_size,
          'axes.titlesize': plot_size,
          'xtick.labelsize': plot_size * 0.75,
          'ytick.labelsize': plot_size * 0.75,
          'axes.titlepad': 25}
plt.rcParams.update(params)
plt.rcParams.update(params)

# Initial Parameters
n_cities = 10
n_population = 40
num_chromosomes = n_population;
mutation_rate = 1 / (n_cities * 3)
generation_num = 1000
# CJ
numChildren = round(n_population * .9);
starting_point = 1;
# Generating coordinates for each city
coordinates_list = [[x, y] for x, y in zip(np.random.rand(n_cities) * 100, np.random.rand(n_cities) * 100)]
names_list = np.arange(1, len(coordinates_list) + 1)
cities_dict = {x: y for x, y in zip(names_list, coordinates_list)}
g, h = zip(*coordinates_list)

initial_population_set = initial_population(names_list, n_population)
fitness_list = fitness_all_cities(initial_population_set, cities_dict)
best_chromosom = best_chromosome(initial_population_set)

# Running the main code for selected number of generations
bests = []
best_coordinates = []
best_coordinates.append(best_chromosom.tolist())
video_frame = 0
for k in range(generation_num):
    fitness_list = fitness_all_cities(initial_population_set, cities_dict)
    # CJ
    ranking = np.argsort(fitness_list)
    bests.append(fitness_list.min())
    print(str(k) + " " + str(fitness_list.min()))
    parent_list = parent_selection(initial_population_set, fitness_list, numChildren)
    offspring_after_crossover = crossover(parent_list)
    new_population_set = np.concatenate(
        (initial_population_set[ranking[0:(num_chromosomes - numChildren)], :], offspring_after_crossover), axis=0)
    mutated_pop = mutate_population(new_population_set)
    initial_population_set = mutated_pop
    best_chromosome_check = best_chromosome(initial_population_set)
    if best_coordinates[video_frame] != best_chromosome_check.tolist():
        video_frame += 1
        best_coordinates.append(best_chromosome_check.tolist())

print(len(best_coordinates))
# Plotting the TSP of best score
plt.ion()
fig, ax = plt.subplots(figsize=(5, 5))
plot1, = ax.plot(g, h)
plt.xlabel("x-coordinate", fontsize=11)
plt.ylabel("y-coordinate", fontsize=11)
plt.title('Travelling Salesman Problem with Genetic Algorithm', fontsize=11)


# Animation
def animate(m):
    # for m in range(1, video_frame):
    new_coordinates = getting_new_coordinate(best_coordinates[m], cities_dict)
    aa, bb = zip(*new_coordinates)
    plt.scatter(aa, bb)
    plot1.set_xdata(aa)
    plot1.set_ydata(bb)
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.1)
    for i in range(len(aa)):
        plt.annotate(best_coordinates[m][i], (aa[i], bb[i]))
    # plt.show()


anim = animation.FuncAnimation(fig, animate, frames=len(best_coordinates),
                               interval=5)
# saving to m4 using ffmpeg writer
writervideo = animation.FFMpegWriter(fps=5)
f = r"C:\Users\savas\PycharmProjects\TSP_with_GA_CJ\TSPmap.mp4"
anim.save(f, writer=writervideo)
plt.close()

# Plotting the best scores of each generation
plt.figure(100)
plt.plot(range(len(bests)), bests, color="skyblue")
plt.xlabel("generation")
plt.ylabel("distance")
plt.title("Minimum Total Distance at Each Generation ")
plt.xlim([0, generation_num])
plt.show(block=True)
