import time
import matplotlib.pyplot as plt

from algorithm.evo import Evo
from algorithm.pso import PSO
from ui.evo_file_writer import EvoFileWriter
from ui.pso_file_writer import PSOFileWriter


class UI:
    def __init__(self):
        self.__evo = None
        self.__pso = None

        self.__execution_times = []
        self.__solutions = []

        self.__evo_file_writer = EvoFileWriter("results/evo.txt")
        self.__pso_file_writer = PSOFileWriter("results/pso.txt")

    def show_menu(self):
        while True:
            print("(1) Algoritm evolutiv.")
            print("(2) Algoritm PSO.")
            print("(x) Iesire")

            user_choice = input("Dati optiunea: ")

            if user_choice == "1":
                population_size = int(input("Dati dimensiunea populatiei: "))
                number_of_generations = int(input("Dati numarul de generatii: "))
                mutation_probability = float(input("Dati probabilitatea de mutatie: "))

                self.__evo = Evo(population_size, mutation_probability, number_of_generations, 2)

                self.__solutions = []
                self.__execution_times = []

                self.__evo_file_writer.set_input(population_size, number_of_generations, mutation_probability, 2)
                self.__evo_file_writer.initial_write_file()

                fitness_values = []
                for i in range(10):
                    start_time = time.time()
                    solution = self.__evo.execute_search()
                    fitness_values.append(self.__evo.get_fitness_values())
                    end_time = time.time()
                    execution_time = end_time - start_time

                    self.__solutions.append(solution)
                    self.__execution_times.append(execution_time)
                    self.__evo_file_writer.write_file(solution, execution_time)

                self.__evo_file_writer.set_solutions(self.__solutions)
                self.__evo_file_writer.set_execution_times(self.__execution_times)
                self.__evo_file_writer.final_write_file()

                self.__plot_fitness_values(fitness_values)
                print("Datele au fost scrise in fisier...")
            elif user_choice == "2":
                particles = int(input("Dati numarul de particule: "))
                iterations = int(input("Dati numarul de iteratii: "))
                c1 = float(input("Dati c1: "))
                c2 = float(input("Dati c2: "))

                self.__pso = PSO(particles, c1, c2, iterations, 10)
                self.__solutions = []
                self.__execution_times = []

                self.__pso_file_writer.set_input(particles, iterations, c1, c2, 10)
                self.__pso_file_writer.initial_write_file()

                for i in range(10):
                    start_time = time.time()
                    solution = self.__pso.execute_search()
                    end_time = time.time()
                    execution_time = end_time - start_time

                    self.__solutions.append(solution)
                    self.__execution_times.append(execution_time)
                    self.__pso_file_writer.write_file(solution, execution_time)

                self.__pso_file_writer.set_solutions(self.__solutions)
                self.__pso_file_writer.set_execution_times(self.__execution_times)
                self.__pso_file_writer.final_write_file()

                print("Datele au fost scrise in fisier...")
            elif user_choice == "x":
                break
            else:
                print("Optiune invalida. Reincercati...")

    @staticmethod
    def __plot_fitness_values(fitness_values):
        plt.figure(figsize=(10, 5))
        for i, value in enumerate(fitness_values):
            plt.plot(value, label=f'Test {i + 1}')
        plt.title("Fitness values")
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.legend()
        plt.grid(True)
        plt.show()
