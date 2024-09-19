import random
import matplotlib.pyplot as plt

# Define parameters
population_size = 100
generations = 50
mutation_rate = 0.01
adaptation_benefit = 0.1
genome_length = 10

# Individual with a simple genome consisting of a list of alleles (0 or 1)
class Individual:
    def __init__(self, genome=None):
        if genome is None:
            self.genome = [random.choice([0, 1]) for _ in range(genome_length)]
        else:
            self.genome = genome

    def fitness(self):
        # Fitness is the sum of beneficial alleles
        return sum(self.genome) / len(self.genome) + random.uniform(-adaptation_benefit, adaptation_benefit)

def reproduce_sexual(parent1, parent2):
    # Crossover and mutation
    crossover_point = random.randint(1, len(parent1.genome) - 1)
    child_genome = parent1.genome[:crossover_point] + parent2.genome[crossover_point:]
    
    # Apply mutations
    for i in range(len(child_genome)):
        if random.random() < mutation_rate:
            child_genome[i] = 1 if child_genome[i] == 0 else 0
            
    return Individual(genome=child_genome)

def reproduce_asexual(parent):
    # Clone parent and apply mutations
    child_genome = parent.genome[:]
    for i in range(len(child_genome)):
        if random.random() < mutation_rate:
            child_genome[i] = 1 if child_genome[i] == 0 else 0
            
    return Individual(genome=child_genome)

def simulate(reproduction_method):
    population = [Individual() for _ in range(population_size)]
    avg_fitness_over_time = []

    for generation in range(generations):
        # Evaluate fitness of population
        fitness_scores = [ind.fitness() for ind in population]
        avg_fitness = sum(fitness_scores) / population_size
        avg_fitness_over_time.append(avg_fitness)

        # Select individuals for reproduction (tournament selection)
        new_population = []
        for _ in range(population_size):
            if reproduction_method == 'sexual':
                parent1, parent2 = random.choices(population, weights=fitness_scores, k=2)
                child = reproduce_sexual(parent1, parent2)
            else:  # asexual
                parent = random.choices(population, weights=fitness_scores, k=1)[0]
                child = reproduce_asexual(parent)
            new_population.append(child)
        population = new_population

    return avg_fitness_over_time

def plot_results(avg_fitness_sexual, avg_fitness_asexual):
    plt.plot(avg_fitness_sexual, label='Sexual Reproduction')
    plt.plot(avg_fitness_asexual, label='Asexual Reproduction')
    plt.xlabel('Generation')
    plt.ylabel('Average Fitness')
    plt.title('Spread of Beneficial Adaptations: Sexual vs Asexual Reproduction')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    avg_fitness_sexual = simulate('sexual')
    avg_fitness_asexual = simulate('asexual')
    plot_results(avg_fitness_sexual, avg_fitness_asexual)
