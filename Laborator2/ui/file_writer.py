class OutputFileWriter:
    def __init__(self, input_filename, output_filename, iterations, tabu_iterations):
        self.__input_filename = input_filename
        self.__output_filename = output_filename
        self.__iterations = iterations
        self.__tabu_iterations = tabu_iterations
        self.__execution_times = []
        self.__solutions = []

    def set_execution_times(self, execution_times):
        self.__execution_times = execution_times

    def set_solutions(self, solutions):
        self.__solutions = solutions

    def write_file(self, solution, execution_time):
        with open(self.__output_filename, 'a') as file:
            file.write(f"{solution}          {execution_time}\n")

    def initial_write_file(self):
        with open(self.__output_filename, 'a') as file:
            file.write("Algoritm folosit: tabu search\n")
            file.write(f"Fisier de intrare: {self.__input_filename}\n")
            file.write(f"Numar iteratii = {self.__iterations}\n")
            file.write(f"Iteratii tabu: {self.__tabu_iterations}\n")
            file.write(f"Numar rulari: 10. Rezultatele obtinute sunt:\n")
            file.write("\n")

    def final_write_file(self):
        median_execution_time = sum(self.__execution_times) / len(self.__execution_times)
        median_solution = sum(self.__solutions) / len(self.__solutions)
        max_solution = max(self.__solutions)

        with open(self.__output_filename, 'a') as file:
            file.write("\n")
            file.write(f"Valoare medie obtinuta: {median_solution}\n")
            file.write(f"Valoare maxima obtinuta: {max_solution}\n")
            file.write(f"Timp de executie mediu: {median_execution_time}\n")
            file.write("\n")
