import random


class Evo:
    def __init__(self, population_size, mutation_probability, number_of_generations, dimensions):
        self.__population_size = population_size
        self.__mutation_probability = mutation_probability
        self.__number_of_generations = number_of_generations
        self.__dimensions = dimensions

    def __initialize_population(self):
        population = []

        for _ in range(self.__dimensions):
            individual = []
            for _ in range(self.__population_size):
                random_value = random.uniform(-5, 5)
                individual.append(random_value)
            population.append(individual)

        return population

    def __crossover(self, parent1, parent2):
        alpha = random.uniform(0, 1)
        k = random.randint(0, self.__dimensions - 1)
        child1 = []
        child2 = []

        for i in range(k):
            child1.append(parent1[i])
        for i in range(k, self.__dimensions):
            child1.append(alpha * parent2[i] + (1 - alpha) * parent1[i])

        for i in range(k):
            child2.append(parent2[i])
        for i in range(k, self.__dimensions):
            child2.append(alpha * parent2[i] + (1 - alpha) * parent1[i])

        return child1, child2

    def __mutation(self, individual):
        for i in range(self.__dimensions):
            random_value = random.uniform(0, 1)

            if random_value < self.__mutation_probability:
                individual[i] = random.uniform(-5, 5)

        return individual

    def execute_search(self):
        population = self.__initialize_population()

        for generation in range(self.__number_of_generations):
            new_population = []

            for _ in range(self.__population_size):
                parent1 = self.__selection(population)
                parent2 = self.__selection(population)

                child1, child2 = self.__crossover(parent1, parent2)

                child1 = self.__mutation(child1)
                child2 = self.__mutation(child2)

                new_population.append(child1)
                new_population.append(child2)

            population = sorted(new_population, key=lambda individual: self.__evaluate_fitness(individual))
            population = population[:self.__population_size]

        best_individual = min(population, key=lambda individual: self.__evaluate_fitness(individual))
        return self.__evaluate_fitness(best_individual)

    @staticmethod
    def __evaluate_fitness(individual):
        fitness = 0

        for gene in individual:
            fitness += (gene ** 4 - 16 * gene ** 2 + 5 * gene)
        fitness *= 0.5

        return fitness

    def __selection(self, population):
        fitness_value = min(self.__evaluate_fitness(individual) for individual in population)
        for individual in population:
            fitness_value += self.__evaluate_fitness(individual)

        selected_individual = None
        pick = random.uniform(0, fitness_value)
        current = 0

        for individual in population:
            current += self.__evaluate_fitness(individual)

            if current > pick:
                selected_individual = individual

        if selected_individual is None:
            selected_individual = min(population, key=lambda individual: self.__evaluate_fitness(individual))

        return selected_individual
