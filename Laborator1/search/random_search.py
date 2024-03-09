import random


class RandomSearch:
    def __init__(self, filename):
        self.__objects = []
        self.__max_weight = 0
        self.__number_of_objects = 0
        self.__best_quality = 0
        self.__solutions = []

        self.__config_from_file(filename)

    def __config_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.__number_of_objects = int(lines[0])

            lines = [line.strip() for line in lines if line.strip()]

            for line in lines[1:-1]:
                parts = line.split()
                object_id = int(parts[0])
                weight = int(parts[1])
                value = int(parts[2])
                self.__objects.append({"id": object_id, "weight": weight, "value": value})

            self.__max_weight = int(lines[-1])

    def __evaluate_solution(self, solution):
        total_weight = 0
        total_value = 0
        for i in range(0, len(solution)):
            if solution[i] == 1:
                total_weight += self.__objects[i]["weight"]
                total_value += self.__objects[i]["value"]

        if total_weight <= self.__max_weight:
            return total_value
        return 0

    def __generate_solution(self):
        solution = []
        for _ in range(len(self.__objects)):
            choice = random.choice([0, 1])
            solution.append(choice)
        return solution

    def execute_search(self, iterations):
        for i in range(iterations):
            solution = self.__generate_solution()
            solution_quality = self.__evaluate_solution(solution)
            if solution_quality > self.__best_quality:
                self.__best_quality = solution_quality

        self.__solutions.append(self.__best_quality)
        self.__write_file()

        return self.__best_quality

    def __write_file(self):
        with open("results/results_random/result_3.txt", 'a') as file:
            file.write(str(self.__solutions))
            file.write("\n")
