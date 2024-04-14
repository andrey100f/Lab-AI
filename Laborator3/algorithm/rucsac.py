import random


class Rucsac:
    def __init__(self, filename, population_size, number_of_generations, crossover_probability, mutation_probability):
        self.__population_size = population_size
        self.__number_of_generations = number_of_generations
        self.__crossover_probability = crossover_probability
        self.__mutate_probability = mutation_probability

        self.__objects = []
        self.__max_weight = 0
        self.__number_of_objects = 0

        self.__config_from_file(filename)

    class Individual:
        def __init__(self, objects, max_weight):
            self.__genes = [random.randint(0, 1) for _ in range(len(objects))]
            self.__objects = objects
            self.__max_weight = max_weight
            self.__fitness = self.evaluate_fitness()

        def evaluate_fitness(self):
            total_weight = 0
            total_value = 0
            for i, gene in enumerate(self.__genes):
                if gene == 1:
                    total_weight += self.__objects[i]["weight"]
                    total_value += self.__objects[i]["value"]

            if total_weight <= self.__max_weight:
                return total_value
            return 0

        def get_fitness(self):
            return self.__fitness

        def set_fitness(self, fitness):
            self.__fitness = fitness

        def get_genes(self):
            return self.__genes

        def set_genes(self, genes):
            self.__genes = genes

    def __config_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.__number_of_objects = int(lines[0])

            lines = [line.strip() for line in lines if line.strip()]

            for line in lines[1:-1]:
                parts = line.split()
                object_id = int(parts[0])
                value = int(parts[1])
                weight = int(parts[2])
                self.__objects.append({"id": object_id, "weight": weight, "value": value})

            self.__max_weight = int(lines[-1])

    def __selection(self, population):
        max_value = sum(individual.get_fitness() for individual in population)
        pick = random.uniform(0, max_value)
        current = 0

        for individual in population:
            current += individual.get_fitness()
            if current > pick:
                return individual

    def __crossover(self, parent1, parent2):
        child1, child2 = self.Individual(self.__objects, self.__max_weight), self.Individual(self.__objects, self.__max_weight)

        if random.random() < self.__crossover_probability:
            crossover_point = random.randint(1, len(parent1.get_genes()) - 1)
            child1.set_genes(parent1.get_genes()[:crossover_point] + parent2.get_genes()[crossover_point:])
            child2.set_genes(parent2.get_genes()[:crossover_point] + parent1.get_genes()[crossover_point:])

        child1.set_fitness(child1.evaluate_fitness())
        child2.set_fitness(child2.evaluate_fitness())

        return child1, child2

    def __mutation(self, individual):
        for i in range(len(individual.get_genes())):
            if random.random() < self.__mutate_probability:
                new_genes = 1 - individual.get_genes()[i]
                individual.get_genes()[i] = new_genes

        individual.set_fitness(individual.evaluate_fitness())

    def execute_search(self):
        population = [self.Individual(self.__objects, self.__max_weight) for _ in range(self.__population_size)]
        for generation in range(self.__number_of_generations):
            new_population = []
            while len(new_population) < self.__population_size:
                parent1 = self.__selection(population)
                parent2 = self.__selection(population)
                child1, child2 = self.__crossover(parent1, parent2)
                self.__mutation(child1)
                self.__mutation(child2)
                new_population.extend([child1, child2])
            population = sorted(new_population, key=lambda individual: individual.get_fitness(), reverse=True)[:self.__population_size]

        best_individual = max(population, key=lambda individual: individual.get_fitness())
        return best_individual.get_fitness()
