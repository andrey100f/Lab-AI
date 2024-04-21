class PSOFileWriter:
    def __init__(self, output_filename):
        self.__output_filename = output_filename

        self.__execution_times = []
        self.__solutions = []
        self.__particles = 0
        self.__iterations = 0
        self.__c1 = 0
        self.__c2 = 0
        self.__dimensions = 0

    def set_input(self, particles, iterations, c1, c2, dimensions):
        self.__particles = particles
        self.__iterations = iterations
        self.__c1 = c1
        self.__c2 = c2
        self.__dimensions = dimensions

    def set_execution_times(self, execution_times):
        self.__execution_times = execution_times

    def set_solutions(self, solutions):
        self.__solutions = solutions

    def write_file(self, solution, execution_time):
        with open(self.__output_filename, 'a') as file:
            file.write(f"{solution}          {execution_time}\n")

    def initial_write_file(self):
        with open(self.__output_filename, 'a') as file:
            file.write("Algoritm folosit: PSO\n")
            file.write(f"Numar particule = {self.__particles}\n")
            file.write(f"c1 = {self.__c1}\n")
            file.write(f"c2 = {self.__c2}\n")
            file.write(f"Numar iteratii = {self.__iterations}\n")
            file.write(f"Numar de dimensiuni: {self.__dimensions}\n")
            file.write(f"Numar rulari: 10. Rezultatele obtinute sunt:\n")
            file.write("\n")

    def final_write_file(self):
        median_execution_time = sum(self.__execution_times) / len(self.__execution_times)
        median_solution = sum(self.__solutions) / len(self.__solutions)
        max_solution = min(self.__solutions)

        with open(self.__output_filename, 'a') as file:
            file.write("\n")
            file.write(f"Valoare medie obtinuta: {median_solution}\n")
            file.write(f"Valoare maxima obtinuta: {max_solution}\n")
            file.write(f"Timp de executie mediu: {median_execution_time}\n")
            file.write("\n")
