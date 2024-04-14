import random
import math


class TSP:
    def __init__(self, filename, population_size, generations, mutation_rate, tournament_size):
        self.__population_size = population_size
        self.__generations = generations
        self.__mutation_rate = mutation_rate
        self.__tournament_size = tournament_size

        self.__cities = []
        self.__number_of_cities = 0

        self.__config_from_file(filename)
        self.__population = self.__initialize_population()

    def __config_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.__number_of_cities = int(lines[0])

            lines = [line.strip() for line in lines if line.strip()]

            for line in lines[1:]:
                parts = line.split()
                city_id = int(parts[0])
                city_x = int(parts[1])
                city_y = int(parts[2])

                self.__cities.append({"id": city_id, "city_x": city_x, "city_y": city_y})

    def __get_city_distance(self, city1, city2):
        x1, y1 = self.__cities[city1]["city_x"], self.__cities[city1]["city_y"]
        x2, y2 = self.__cities[city2]["city_x"], self.__cities[city2]["city_y"]

        return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    def __initialize_population(self):
        city_indexes = list(range(self.__number_of_cities))
        return [random.sample(city_indexes, len(city_indexes)) for _ in range(self.__population_size)]

    def __get_cost(self, route):
        total_cost = 0
        for i in range(len(route) - 1):
            total_cost += self.__get_city_distance(route[i], route[i + 1])

        total_cost += self.__get_city_distance(route[-1], route[0])

        return total_cost

    def __selection(self):
        tournament = random.sample(self.__population, self.__tournament_size)
        fitness = min(tournament, key=self.__get_cost)
        return fitness

    def __involve_population(self):
        new_population = []
        for _ in range(self.__population_size):
            parent1 = self.__selection()
            parent2 = self.__selection()
            child = self.__crossover(parent1, parent2)

            if random.random() < self.__mutation_rate:
                child = self.__mutation(child)
            new_population.append(child)

        self.__population = new_population

    def execute_search(self):
        for _ in range(self.__generations):
            self.__involve_population()

        best_solution = min(self.__population, key=self.__get_cost)
        return self.__get_cost(best_solution)

    @staticmethod
    def __crossover(parent1, parent2):
        size = min(len(parent1), len(parent2))
        start, end = sorted(random.sample(range(size), 2))
        child = [None] * size
        child[start:end] = parent1[start:end]

        current_position = end
        for city in parent2:
            if city not in child:
                if current_position >= size:
                    current_position = 0
                child[current_position] = city
                current_position += 1

        return child

    @staticmethod
    def __mutation(route):
        index1, index2 = random.sample(range(len(route)), 2)
        route[index1], route[index2] = route[index2], route[index1]
        return route
