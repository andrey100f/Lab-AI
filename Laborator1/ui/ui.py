import time

from search.nahc import NAHC
from search.random_search import RandomSearch
from ui.file_writer.nahc_file_writer import NAHCFileWriter
from ui.file_writer.random_file_writer import RandomFileWriter


class UI:
    def __init__(self, filename):
        self.__k = 50
        self.__p = 5

        self.__filename = filename
        self.__random_search = RandomSearch(filename)
        self.__nahc = NAHC(filename)
        self.__execution_times = []
        self.__solutions = []

        self.__random_file_writer = RandomFileWriter(filename, self.__k)
        self.__nahc_file_writer = NAHCFileWriter(filename, self.__k, self.__p)

    def show_menu(self):
        while True:
            print("(1) Cautare aleatorie.")
            print("(2) Cautare locala - NAHC.")
            print("(x). Exit")

            user_choice = input("Dati optiunea: ")

            if user_choice == "1":
                self.__solutions = []
                self.__execution_times = []

                self.__random_file_writer.initial_write_file()

                for i in range(10):
                    start_time = time.time()
                    solution = self.__random_search.execute_search(self.__k)
                    end_time = time.time()
                    execution_time = end_time - start_time

                    self.__solutions.append(solution)
                    self.__execution_times.append(execution_time)
                    self.__random_file_writer.write_file(solution, execution_time)

                self.__random_file_writer.set_solutions(self.__solutions)
                self.__random_file_writer.set_execution_times(self.__execution_times)
                self.__random_file_writer.final_write_file()

                print("Datele au fost scrise in fisier...")
            elif user_choice == "2":
                self.__solutions = []
                self.__execution_times = []

                self.__nahc_file_writer.initial_write_file()

                for i in range(10):
                    start_time = time.time()
                    solution = self.__nahc.execute_search(self.__k, self.__p)
                    end_time = time.time()
                    execution_time = end_time - start_time

                    self.__solutions.append(solution)
                    self.__execution_times.append(execution_time)
                    self.__nahc_file_writer.write_file(solution, execution_time)

                self.__nahc_file_writer.set_solutions(self.__solutions)
                self.__nahc_file_writer.set_execution_times(self.__execution_times)
                self.__nahc_file_writer.final_write_file()

                print("Datele au fost scrise in fisier...")
            elif user_choice == "x":
                break
            else:
                print("Optiune gresita... Reincercati")

