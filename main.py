# Imports
import numpy as np
import matplotlib.pyplot as plt
import time
import warnings

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
n_cities = 15
n_population = 40
mutation_rate = 0.05
generation_num = 100
# Generating coordinates for each city
coordinates_list = [[x, y] for x, y in zip(np.random.randint(0, 10, n_cities), np.random.randint(0, 10, n_cities))]
names_list = np.arange(1, len(coordinates_list) + 1)
cities_dict = {x: y for x, y in zip(names_list, coordinates_list)}
g, h = zip(*coordinates_list)


#Calculating the distance between two cities
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
        init_pop = city_list[np.random.choice(list(range(n_cities)), n_cities, replace=False)]
        population_set.append(init_pop)
    return np.array(population_set)


initial_population_set = initial_population(names_list, n_population)

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


fitness_list = fitness_all_cities(initial_population_set, cities_dict)


# Parent selection for crossover
def parent_selection(population_set, fitness_list):
    population_set = np.array(population_set)
    """Returns two chromosomes as two parents"""
    total_fit = fitness_list.sum()
    prob_list = fitness_list / total_fit
    # I am generating two population sets to get a single set with the same size of initial population
    # For the first population set, I take 3/4 of the previous population and 1/4 of random new population
    carried_children_number = int(3 * len(population_set) / 4)
    parent_list_a1 = population_set[0:carried_children_number]
    parent_list_a2 = np.random.choice(list(range(len(population_set))), len(population_set) - carried_children_number,
                                      p=prob_list, replace=False)
    parent_list_a2 = population_set[parent_list_a2]

    # For the second population set, I generate a random set

    parent_list_b = np.random.choice(list(range(len(population_set))), len(population_set), p=prob_list,
                                     replace=False)
    parent_list_a = np.concatenate((parent_list_a1, parent_list_a2), axis=0)
    parent_list_b = population_set[parent_list_b]
    # Combining two populations set in an array
    return np.array([parent_list_a, parent_list_b])


# For eliting, finding the best chromosome of each generation
def best_chromosome(generation):
    best = generation[0]
    for n in range(1, len(generation)):
        if chromo_total_dist(generation[n], cities_dict) < chromo_total_dist(best, cities_dict):
            best = generation[n]
    return best


best_chromosom = best_chromosome(initial_population_set)


# Defining a crossover rate for each chromosome
def crossover_rate(prog_a, prog_b):
    offspring = prog_a[0:int(len(prog_a) / 2)]
    for city in prog_b:
        if city not in offspring:
            offspring = np.concatenate((offspring, [city]))
    offspring = np.append(offspring, offspring[0])
    return offspring


# Crossover the parents
def crossover(parent_list, best_chromosom):
    # adding the best chromosome of the population as the first element of the population
    new_population_set = [best_chromosom]
    for i in range(parent_list.shape[1] - 1):
        prog_a, prog_b = parent_list[0][i + 1], parent_list[1][i + 1]
        offspring = crossover_rate(prog_a, prog_b)
        new_population_set.append(offspring)
    return new_population_set


# Mutate the new chromosomes for a given mutation rate
def mutation(offspring):
    for k in range(int(n_cities * mutation_rate)):
        a = np.random.randint(1, n_cities - 1)
        b = np.random.randint(1, n_cities - 1)
        offspring[a], offspring[b] = offspring[b], offspring[a]

    return offspring


def mutate_population(new_population_set):
    mutated_pop = []
    for offspring in new_population_set:
        mutated_pop.append(mutation(offspring))
    return mutated_pop


# Function to find the best score cities
def getting_new_coordinate(best_coordinate, cities_dict):
    # for i in mutated_pop:
    new_coordinate = [cities_dict[city] for city in best_coordinate]
    # new_coordinates.append(new_coordinate)
    return new_coordinate


# Running the main code for selected number of generations
bests = []
best_coordinates = []
for k in range(generation_num):
    fitness_list = fitness_all_cities(initial_population_set, cities_dict)
    bests.append(fitness_list.min())
    parent_list = parent_selection(initial_population_set, fitness_list)
    new_population_set = crossover(parent_list, best_chromosom)
    mutated_pop = mutate_population(new_population_set)
    initial_population_set = mutated_pop
    best_chromosom = best_chromosome(initial_population_set)
    initial_population_set[0] = best_chromosom
    best_coordinates.append(best_chromosom.tolist())


# Plotting the TSP of best score
plt.ion()
figure, ax = plt.subplots(figsize=(10, 8))
plot1, = ax.plot(g, h)
plt.xlabel("x-coordinate", fontsize=11)
plt.ylabel("y-coordinate", fontsize=11)
plt.title("Travel Salesman Problem with Genetic Algorithm")
res = list(set(tuple(sorted(sub)) for sub in best_coordinates))
for m in range(len(res)):
    new_coordinates = getting_new_coordinate(best_coordinates[m], cities_dict)
    aa, bb = zip(*new_coordinates)
    plot1.set_xdata(aa)
    plot1.set_ydata(bb)
    figure.canvas.draw()
    figure.canvas.flush_events()
    time.sleep(0.1)
    for i in range(len(aa)):
        plt.annotate(best_coordinates[m][i], (aa[i], bb[i]))
    plt.show()

# Plotting the best scores of each generation
plt.figure(100)
plt.plot(range(len(bests)), bests, color="skyblue")
plt.xlabel("generation")
plt.ylabel("distance")
plt.title("Minimum Total Distance at Each Generation ")
plt.xlim([0, 100])
plt.show(block=True)
