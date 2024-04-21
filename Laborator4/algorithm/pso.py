import random


class PSO:
    def __init__(self, particles, c1, c2, iterations, dimensions):
        self.__particles = particles
        self.__c1 = c1
        self.__c2 = c2
        self.__iterations = iterations
        self.__dimensions = dimensions

        self.__initialize_particles()

    def __initialize_particles(self):
        population = []
        for _ in range(self.__particles):
            x = []
            for _ in range(self.__dimensions):
                xi = -5 + random.uniform(0, 1) * 10
                x.append(xi)

            v = []
            for _ in range(self.__dimensions):
                vi = random.uniform(0.1, 1)
                v.append(vi)

            individual = {"x": x, "v": v, "pbest": x, "pbest_fitness": self.__evaluate_fitness(x)}
            population.append(individual)

        return population

    def __get_gbest(self, population):
        gbest = []
        gbest_fitness = float("inf")

        for particle in population:
            fitness = self.__evaluate_fitness(particle["x"])
            if fitness < gbest_fitness:
                gbest = particle["x"]
                gbest_fitness = self.__evaluate_fitness(particle["x"])

        return gbest

    def execute_search(self):
        best_individual = None

        for i in range(self.__iterations):
            population = self.__initialize_particles()
            w = i / self.__iterations

            for particle in population:
                if self.__evaluate_fitness(particle["x"]) < self.__evaluate_fitness(particle["pbest"]):
                    particle["pbest"] = particle["x"]
                    particle["pbest_fitness"] = self.__evaluate_fitness(particle["x"])

            gbest = self.__get_gbest(population)

            for particle in population:
                for j in range(len(particle["v"])):
                    particle["v"][j] = (w * particle["v"][j] +
                                        self.__c1 * random.uniform(0, 1) * (particle["pbest"][j] - particle["x"][j]) +
                                        self.__c2 * random.uniform(0, 1) * (gbest[j] - particle["x"][j]))

                for j in range(len(particle["x"])):
                    particle["x"][j] += particle["v"][j]

            if best_individual is None or self.__evaluate_fitness(gbest) < self.__evaluate_fitness(best_individual):
                best_individual = gbest

        return self.__evaluate_fitness(best_individual)

    @staticmethod
    def __evaluate_fitness(individual):
        fitness = 0

        for gene in individual:
            fitness += (gene ** 4 - 16 * gene ** 2 + 5 * gene)
        fitness *= 0.5

        return fitness
