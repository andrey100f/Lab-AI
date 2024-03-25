import math
import random


class TSP:
    def __init__(self, filename, iterations, tabu_iterations):
        self.__iterations = iterations
        self.__tabu_iterations = tabu_iterations
        self.__cities = []
        self.__number_of_cities = 0

        self.__config_from_file(filename)

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

    def __get_cost(self, route):
        total_cost = 0
        for i in range(len(route) - 1):
            total_cost += self.__get_city_distance(route[i], route[i + 1])

        total_cost += self.__get_city_distance(route[-1], route[0])

        return total_cost

    def execute_search(self):
        memory = [[0] * self.__number_of_cities for _ in range(self.__number_of_cities)]

        current_route = list(range(self.__number_of_cities))
        random.shuffle(current_route)
        cost_current_route = self.__get_cost(current_route)

        for _ in range(self.__iterations):
            neighbour = self.generate_neighbours(current_route)
            city_1, city_2 = random.sample(range(self.__number_of_cities), 2)
            cost_neighbour = self.__get_cost(neighbour)

            is_tabu = memory[city_1][city_2] > 0

            if not is_tabu and cost_neighbour < cost_current_route:
                current_route = neighbour
                cost_current_route = cost_neighbour

                memory[city_1][city_2] = self.__tabu_iterations

            for i in range(self.__number_of_cities):
                for j in range(self.__number_of_cities):
                    if memory[i][j] > 0:
                        memory[i][j] -= 1

        return cost_current_route

    def __get_city_distance(self, city1, city2):
        x1, y1 = self.__cities[city1]["city_x"], self.__cities[city1]["city_y"]
        x2, y2 = self.__cities[city2]["city_x"], self.__cities[city2]["city_y"]

        return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

    @staticmethod
    def generate_neighbours(solution):
        a, b = sorted(random.sample(range(len(solution)), 2))
        return solution[:a] + solution[a:b + 1][::-1] + solution[b + 1:]