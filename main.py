#import required libraries
import random
import matplotlib.pyplot as plt

# define item values and weights
value = [442,525,511,593,546,564,617]
weight = [41,50,49,59,55,57,60]

# pair values and weights into item tuples
items = zip(value,weight)
items = list(items)

# configuration parameters
weight_limit = 170
population_size = 30
generation_limit = 50
mutation_rate = 0.5

# create a binary genome for an individual
def create_genome(items):
    genome = []
    for i in range(len(items)):
        genome.append(random.randint(0,1))  # 0 means item not picked, 1 means picked
    return genome

# create initial population of random genome
def create_population(size):
    population = []
    for i in range (size):
        population.append(create_genome(items))
    return population

# fitness function to evaluate genome based on value and weight limit  
def fitness(genome):
    total_value = 0
    total_weight = 0
    for gene,(value,weight) in zip(genome,items):
        if gene==1:
            total_value += value
            total_weight += weight
    if total_weight > weight_limit:
        return 0  # discard overweight solutions
    else:
        return total_value
    
# selection using tournament method
def select(population):
    tournament = random.sample(population, 4)
    tournament.sort(key=fitness)
    return tournament[3]  # return best of 4

# crossover function to mix genes of parents
def crossover(parent1,parent2):
    if len(parent1) == len(parent2):
        p = random.randint(1,len(parent1)-2)  # pick crossover point
        child1 = parent1[:p] + parent2[p:]
        child2 = parent2[:p] + parent1[p:]
    return child1,child2

# mutation flips bits in the genome with certain probability
def mutate(genome):
    for i in range(len(genome)):
        if random.random() < mutation_rate:
            genome[i] = 1-genome[i]  # flip bit
    return genome

# main genetic algorithm
def genetic_algorithm():
    population = create_population(population_size)
    best_fitness_pergen = []  # to track best fitness per generation
    gen_num = 0
    
    for i in range(generation_limit):
        new_population = []
        population.sort(key=fitness, reverse=True)  # sort descending
        new_population.append(population[0])  # elitism: carry forward best
        new_population.append(population[1])
        while len(new_population) < population_size:
            parent1 = select(population)
            parent2 = select(population)
            child1,child2 = crossover(parent1,parent2)
            new_population.append(mutate(child1))
            if len(new_population) <= population_size:
                new_population.append(mutate(child2))
        population = new_population
        gen_num +=1
        best_genome = max(population, key=fitness)
        print(gen_num, best_genome, fitness(best_genome))
        best_fitness_pergen.append(fitness(best_genome))  # store best fitness

    # plot the best fitness per generation
    plt.plot(best_fitness_pergen)
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title("Knapsack Problem using Genetic Algorithm")
    plt.grid(True)
    plt.show()

    # return best solution found
    best_solution = max(population, key=fitness)
    return(best_solution,fitness(best_solution))

# run the algorithm and print the result
solution,value = genetic_algorithm()
print("Best solution: ",solution)
print("Best value: ",value)
