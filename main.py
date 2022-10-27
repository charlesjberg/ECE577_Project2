# Imports
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation

# import matplotlib.animation as animation
# from moviepy.editor import VideoClip
# from moviepy.video.io.bindings import mplfig_to_npimage
plot_size = 10
plot_width = 8
plot_height = 8
params = {'legend.fontsize': 'large',
          'figure.figsize': (plot_width, plot_height),
          'axes.labelsize': plot_size,
          'axes.titlesize': plot_size,
          'xtick.labelsize': plot_size * 0.75,
          'ytick.labelsize': plot_size * 0.75,
          'axes.titlepad': 25}
plt.rcParams.update(params)
plt.rcParams.update(params)
# Parameters
# n_cities = int(input("Please enter the number of the cities:"))
# n_population = int(input("Please enter the number of the cities:"))
# mutation_percent = int(input("Please enter mutation percentage:"))

# Initial Parameters
n_cities = 100
n_population = 300
mutation_rate = 0.001
elite_size = 10
# Generating coordinates for each city
coordinates_list = [[x, y] for x, y in zip(np.random.randint(0, 100, n_cities), np.random.randint(0, 100, n_cities))]
names_list = np.arange(1, len(coordinates_list) + 1)
# names_list = np.append(names_list, [names_list[0]])
# print(f"name_list {names_list}")
cities_dict = {x: y for x, y in zip(names_list, coordinates_list)}
# print(f"coordinate list {coordinates_list}")
# print(f"names list {names_list}")
# print(f"cities_dict {cities_dict}")
g, h = zip(*coordinates_list)


# print(f"gggg {g}")
# print(f"hhhh {h}")
# plt.figure(1)
# plt.plot(g, h)
# plt.plot()
# # Loop for annotation of all points
# for i in range(len(g)):
#     plt.annotate(names_list[i], (g[i], h[i]))
# plt.show()
# plt.show(block=True)

###3
# city_lists = sorted(cities_dict.items()) # sorted by key, return a list of tuples
# cities, coordinates = zip(*city_lists) # unpack a list of pairs into two tuples
# print(f"xxx {cities}")
# print(f"yyy {coordinates}")

# plt.figure(10)
# plt.plot(x, y)
# plt.show()
###


def distance_between_cities(city_a, city_b, city_dict):
    """Returns the distance between two cities"""
    a = city_dict[city_a]
    b = city_dict[city_b]
    x = a[0] - b[0]
    y = a[1] - b[1]
    return np.sqrt((x ** 2) + (y ** 2))


# print(cities_dict)

# Generating the first population set
def initial_population(city_list, n_population):
    """Returns the initial random population as an array"""
    population_set = []
    for pop in range(n_population):
        # Randomly generating a new solution
        init_pop = city_list[np.random.choice(list(range(n_cities)), n_cities, replace=False)]
        init_pop = np.append(init_pop, init_pop[0])
        population_set.append(init_pop)
        # population_set = population_set.append(population_set[0])
    return np.array(population_set)


initial_population_set = initial_population(names_list, n_population)


# initial_population_list = initial_population_set
# print(f"initial population set {initial_population_set}")
# print(f"population set length {len(initial_population_set)}")
# print(type(initial_population_set))

# Calculating the total distance in a chromosome
def chromo_total_dist(city_list, city_dict):
    """Returs the total distance in each chromosome"""
    total = 0
    for i in range(n_cities - 1):
        a = city_list[i]
        b = city_list[i + 1]
        total += distance_between_cities(a, b, city_dict)
    return total


# T
def fitness_all_cities(population_set, cities_dict):
    """Returns each chromosome's fitness and stores as a list"""
    fitness_list = np.zeros(n_population)
    # Looping over all chromosomes to calculate the fitness
    for i in range(n_population):
        fitness_list[i] = chromo_total_dist(population_set[i], cities_dict)
    return fitness_list
    # return sorted(fitness_list, reverse=True)


fitness_list = fitness_all_cities(initial_population_set, cities_dict)


# print(f"fitness list {fitness_list}")
# fitness_list = sort(fitness_list)

# Selecting parents for crossover
def parent_selection(population_set, fitness_list):
    population_set = np.array(population_set)
    """Returns two chromosomes as two parents"""
    # print(f" bakalim {type(population_set)}")
    total_fit = fitness_list.sum()
    prob_list = fitness_list / total_fit
    # print(f"prob-list {prob_list} ")
    # Notice there is the chance that a progenitor. mates with oneself
    parent_list_a = np.random.choice(list(range(len(population_set))), len(population_set), p=prob_list,
                                     replace=True)
    parent_list_b = np.random.choice(list(range(len(population_set))), len(population_set), p=prob_list,
                                     replace=True)
    # parent_list_c = population_set[3]
    # print(f"parent_list_a length {(parent_list_a)}")
    # print(f"parent_list_b length {(parent_list_b)}")
    # print(f"parent_list_c length {(parent_list_c)}")

    parent_list_a = population_set[parent_list_a]
    parent_list_b = population_set[parent_list_b]

    # print(f"parent_list_a length {(parent_list_a)}")
    # print(f"parent_list_b length {(parent_list_b)}")
    # print(len(parent_list_a))
    # print(len(parent_list_b))
    return np.array([parent_list_a, parent_list_b])


# parent_list = parent_selection(population_set, fitness_list)
# print(f"progenitor_list_length {len(parent_list[0])}")
# print(f"progenitor_list {parent_list[0][2]}")

# Find the best chromosome of the generation
def best_chromosome(generation):
    best = generation[0]
    for n in range(1, len(generation)):
        if chromo_total_dist(generation[n], cities_dict) < chromo_total_dist(best, cities_dict):
            best = generation[n]
    return best


best_chromosom = best_chromosome(initial_population_set)


# print(f"best {best}")


# Selecting crossover rates
def mate_progenitors(prog_a, prog_b):
    """Returns the child after crossover"""
    offspring = prog_a[0:52]

    for city in prog_b:
        if city not in offspring:
            offspring = np.concatenate((offspring, [city]))
    offspring = np.append(offspring, offspring[0])
    # print(f"offspring {offspring}")

    return offspring


# Crossover the parents
def crossover(parent_list, best_chromosom):
    # print(f" parentt list {parent_list} ")
    new_population_set = [best_chromosom]
    for i in range(parent_list.shape[1] - 1):
        prog_a, prog_b = parent_list[0][i], parent_list[1][i]
        # print(f" progax {prog_a} and progb {prog_b}")
        offspring = mate_progenitors(prog_a, prog_b)
        # print(f"cocuklar {offspring}")
        # offspring = np.append(offspring, offspring[0])
        new_population_set.append(offspring)
    return new_population_set


# new_population_set = crossover(parent_list)
# print(f" new population {new_population_set[0]}")


# Mutate the new chromosomes for a given mutation rate
# It does not mutate the first and the last cities
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


# mutated_pop = mutate_population(new_population_set)
# print(f" mutated {mutated_pop[0]}")
# print(len(mutated_pop))


# print(f"new coordinates {new_coordinates}")

# anim = animation.FuncAnimation(figure, getting_new_coordinate, frames=1000,
#                                interval=20, blit=True)
# anim.save("TLI.gif", writer='imagemagick',fps=60)
# aa, bb = zip(*new_coordinates)
# plt.figure(3)
# plt.plot(aa, bb, mutated_pop[0])
# for i in range(len(aa)):
#     plt.annotate(mutated_pop[0][i], (aa[i], bb[i]))
# plt.show()
# plt.plot()
#

# Stopping
best_solution = [-1, np.inf, np.array([])]
bests = []

global mutated_pop
for k in range(n_population):
    # if i % 100 == 0:
    #     print(i, fitness_list.min(), fitness_list.mean())
    fitness_list = fitness_all_cities(initial_population_set, cities_dict)
    # elited = fitness_list.sort()
    # elited = elited.fetch(10)
    # print(f"best chromosomes {best_chromosom}")
    bests.append(fitness_list.min())

    # print(f"best solutions {bests}")
    # print(len(bests))
    # Saving the best solution
    # parent_list = parent_selection(population_set, fitness_list)
    # initial_population_set[0] = best_chromosome
    parent_list = parent_selection(initial_population_set, fitness_list)
    # print(f"parent list {parent_list}")
    new_population_set = crossover(parent_list, best_chromosom)
    # print(f"new_population_set {new_population_set}")
    mutated_pop = mutate_population(new_population_set)
    # print(f"mutated population {mutated_pop}")
    # print(type(mutated_pop))
    initial_population_set = mutated_pop
    # print(f"bu ne {initial_population_set}")

    # initial_population_list = [l.tolist() for l in initial_population_set]
    new_list = list(map(list, initial_population_set))
    # print(type(new_list))
    # print(f"ew list {new_list}")

    best_chromosom = best_chromosome(initial_population_set)
    # best_coordinate[k] = best_chromosom
print(bests)
# initial_population_set[0] = best_chromosome

# initial_population_set = np.array(new_population_set)
# initial_population_set[0] = best_chromosome()
# initial_population_set = np.array(initial_population_set)

# print(f"initial_population_set {initial_population_set}")
# print(type(initial_population_set))
# initial
# bests.append(best_solution[1])
# if fitness_list.min() < best_solution[1]:
#     best_solution[0] = k
#     best_solution[1] = fitness_list.min()
#     best_solution[2] = np.array(new_population_set)[fitness_list.min() == fitness_list]
#     print(f"best sol {best_solution[1]}")

# print(f"best num {best_solution}")
# bests.append(best_solution[0])
# print(f"bests {bests}")
plt.ion()
figure, ax = plt.subplots(figsize=(10, 8))
plot1, = ax.plot(g, h)
plt.xlabel("x-coordinate", fontsize=11)
plt.ylabel("y-coordinate", fontsize=11)
plt.title("Travel Salesman Problem with Genetic Algorithm")
# Extracting new coordinates
new_coordinates = []


# def getting_new_coordinate(best_coordinate, cities_dict):
#     # for i in mutated_pop:
#     # I am just running the first 10 generation for illustration purposes
#     for m in range(10):
#         new_coordinate = [cities_dict[city] for city in best_coordinate[m]]
#         new_coordinates.append(new_coordinate)
#         aa, bb = zip(*new_coordinates)
#         plot1.set_xdata(aa)
#         plot1.set_ydata(bb)
#         figure.canvas.draw()
#         figure.canvas.flush_events()
#         time.sleep(0.1)
#         # plt.figure()
#         # plt.plot(aa, bb, mutated_pop[m])
#         # plt.pause(0.05)
#         for i in range(len(aa)):
#             plt.annotate(mutated_pop[m][i], (aa[i], bb[i]))
#     plt.show()
#     return new_coordinates
# new_coordinates = getting_new_coordinate(best_coordinate,cities_dict)


plt.figure(100)
plt.plot(range(len(bests)), bests, color="skyblue")
plt.xlabel("generation")
plt.ylabel("distance")
plt.title("Minimum Total Distance at Each Generation ")
# plt.show()
plt.show(block=True)
