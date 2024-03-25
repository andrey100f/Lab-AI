import time

from algorithm.rucsac import Rucsac
from algorithm.tsp import TSP
from ui.file_writer import OutputFileWriter


class UI:
    def __init__(self):
        self.__iterations = 0
        self.__tabu_iterations = 0

        self.__rucsac = None
        self.__tsp = None

        self.__execution_times = []
        self.__solutions = []

        self.__rucsac_file_writer = OutputFileWriter("config/rucsac/data3.txt",
                                                     "results/rucsac.txt", self.__iterations,
                                                     self.__tabu_iterations)
        self.__tsp_file_writer = OutputFileWriter("config/tsp/data.tsp", "results/tsp.txt",
                                                  self.__iterations, self.__tabu_iterations)

    def show_menu(self):
        while True:
            print("(1) Problema rucsacului.")
            print("(2) Problema comis-voiajorului.")
            print("(X) Iesire")

            user_choice = input("Dati optiunea: ")

            if user_choice == "1":
                self.__iterations = int(input("Dati numarul de iteratii: "))
                self.__tabu_iterations = int(input("Dati numerul de iteratii tabu: "))

                self.__rucsac = Rucsac("config/rucsac/data3.txt",
                                       self.__iterations, self.__tabu_iterations)

                self.__solutions = []
                self.__execution_times = []

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
                self.__iterations = int(input("Dati numarul de iteratii: "))
                self.__tabu_iterations = int(input("Dati numerul de iteratii tabu: "))

                self.__tsp = TSP("config/tsp/data.tsp", self.__iterations,
                                 self.__tabu_iterations)

                self.__solutions = []
                self.__execution_times = []

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
            elif user_choice == "x":
                break
            else:
                print("Optiune gresita... Reincercati")
