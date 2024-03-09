import time

from search.nahc import NAHC
from search.random_search import RandomSearch


class UI:
    def __init__(self, filename):
        self.__random_search = RandomSearch(filename)
        self.__nahc = NAHC(filename)
        self.__execution_times = []

    def show_menu(self):
        while True:
            print("(1) Cautare aleatorie.")
            print("(2) Cautare locala - NAHC.")
            print("(x). Exit")

            user_choice = input("Dati optiunea: ")

            if user_choice == "1":
                iterations = int(input("Dati numarul de iteratii: "))

                start_time = time.time()
                solution = self.__random_search.execute_search(iterations)
                end_time = time.time()
                execution_time = end_time - start_time

                self.__execution_times.append(execution_time)

                print(f"Solutia este: {solution}")
                print(f"Timp de executie: {execution_time}")
            elif user_choice == "2":
                iterations = int(input("Dati numarul de iteratii: "))
                max_iterations = int(input("Dati numarul maxim de iteratii: "))

                start_time = time.time()
                solution = self.__nahc.execute_search(iterations, max_iterations)
                end_time = time.time()
                execution_time = end_time - start_time

                self.__execution_times.append(execution_time)

                print(f"Solutia este: {solution}")
                print(f"Timp de executie: {execution_time}")

            elif user_choice == "x":
                self.__write_to_file()
                break
            else:
                print("Optiune gresita... Reincercati")

    def __write_to_file(self):
        with open("results/results_random/result_3.txt", 'a') as file:
            file.write(str(self.__execution_times))
            file.write("\n")
