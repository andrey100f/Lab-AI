class RandomFileWriter:
    def __init__(self, filename, k):
        self.__filename = filename
        self.__k = k
        self.__execution_times = []
        self.__solutions = []

    def set_execution_times(self, execution_times):
        self.__execution_times = execution_times

    def set_solutions(self, solutions):
        self.__solutions = solutions

    @staticmethod
    def write_file(solution, execution_time):
        with open("results/results_random/output.txt", 'a') as file:
            file.write(f"{solution}          {execution_time}\n")

    def initial_write_file(self):
        with open("results/results_random/output.txt", 'a') as file:
            file.write("Algoritm folosit: random search\n")
            file.write(f"Fisier de intrare: {self.__filename}\n")
            file.write(f"K = {self.__k}\n")
            file.write(f"Numar rulari: 10. Rezultatele obtinute sunt:\n")
            file.write("\n")

    def final_write_file(self):
        median_execution_time = sum(self.__execution_times) / len(self.__execution_times)
        median_solution = sum(self.__solutions) / len(self.__solutions)
        max_solution = max(self.__solutions)

        with open("results/results_random/output.txt", 'a') as file:
            file.write("\n")
            file.write(f"Valoare medie obtinuta: {median_solution}\n")
            file.write(f"Valoare maxima obtinuta: {max_solution}\n")
            file.write(f"Timp de executie mediu: {median_execution_time}\n")
