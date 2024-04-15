import time

from algorithm.rucsac import Rucsac
from algorithm.tsp import TSP
from ui.file_writer import OutputFileWriter


class UI:
    def __init__(self):
        self.__rucsac = None
        self.__tsp = None

        self.__execution_times = []
        self.__solutions = []

        self.__rucsac_file_writer = OutputFileWriter("config/rucsac/data1.txt",
                                                     "results/rucsac.txt")
        self.__tsp_file_writer = OutputFileWriter("config/tsp/data.tsp", "results/tsp.txt")

    def show_menu(self):
        while True:
            print("(1) Problema rucsacului.")
            print("(2) TSP.")
            print("(X) Iesire")

            user_choice = input("Dati optiunea: ")

            if user_choice == "1":
                population_size = int(input("Dati dimensiunea populatiei: "))
                number_of_generations = int(input("Dati numarul de generatii: "))
                crossover_probability = float(input("Dati probabilitatea de crossover: "))
                mutation_probability = float(input("Dati probabilitatea de mutatie: "))

                self.__rucsac = Rucsac("config/rucsac/data2.txt", population_size, number_of_generations,
                                       crossover_probability, mutation_probability)

                self.__solutions = []
                self.__execution_times = []

                self.__rucsac_file_writer.set_input(200, 700, 0.95)
                self.__rucsac_file_writer.initial_write_file()

                for i in range(10):
                    start_time = time.time()
                    solution = self.__rucsac.execute_search()
                    end_time = time.time()
                    execution_time = end_time - start_time

                    self.__solutions.append(solution)
                    self.__execution_times.append(execution_time)
                    self.__rucsac_file_writer.write_file(solution, execution_time)

                self.__rucsac_file_writer.set_solutions(self.__solutions)
                self.__rucsac_file_writer.set_execution_times(self.__execution_times)
                self.__rucsac_file_writer.final_write_file()

                print("Datele au fost scrise in fisier...")
            elif user_choice == "2":
                population_size = int(input("Dati dimensiunea populatiei: "))
                number_of_generations = int(input("Dati numarul de generatii: "))
                tournament_size = int(input("Dati dimensiunea turneului: "))
                mutation_probability = float(input("Dati probabilitatea de mutatie: "))

                self.__tsp = TSP("config/tsp/data.tsp", population_size, number_of_generations,
                                 mutation_probability, tournament_size)
                self.__solutions = []
                self.__execution_times = []

                self.__execution_times = []

                self.__tsp_file_writer.set_input(170, 850, 0.06)
                self.__tsp_file_writer.initial_write_file()

                for i in range(10):
                    start_time = time.time()
                    solution = self.__tsp.execute_search()
                    end_time = time.time()
                    execution_time = end_time - start_time

                    self.__solutions.append(solution)
                    self.__execution_times.append(execution_time)
                    self.__tsp_file_writer.write_file(solution, execution_time)

                self.__tsp_file_writer.set_solutions(self.__solutions)
                self.__tsp_file_writer.set_execution_times(self.__execution_times)
                self.__tsp_file_writer.final_write_file()

                print("Datele au fost scrise in fisier...")
            elif user_choice == "X":
                break
            else:
                print("Optiune invalida. Incercati din nou...")
