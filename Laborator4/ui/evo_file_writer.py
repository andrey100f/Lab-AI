class EvoFileWriter:
    def __init__(self, output_filename):
        self.__output_filename = output_filename

        self.__execution_times = []
        self.__solutions = []
        self.__population_size = 0
        self.__generations = 0
        self.__mutate_probability = 0
        self.__dimensions = 0

    def set_input(self, population_size, generations, mutate_probability, dimensions):
        self.__population_size = population_size
        self.__generations = generations
        self.__mutate_probability = mutate_probability
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
            file.write("Algoritm folosit: algoritm evolutiv\n")
            file.write(f"Dimensiune populatie = {self.__population_size}\n")
            file.write(f"Numar generatii = {self.__generations}\n")
            file.write(f"Probabilitate de mutatie: {self.__mutate_probability}\n")
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
