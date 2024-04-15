<h1 align="center" style="color: #4285F4">Algoritmi evolutivi</h1>

## <span style="color: #4285F4"> Cerința problemei

1. #### Să se implementeze un algoritm evolutiv pentru problema rucsacului.
2. #### Să se implementeze un algoritm evolutiv pentru problema comis-voiajorului. 

## <span style="color: #4285F4"> Algoritm 1 - Problema rucsacului
1. #### Codificare binară - Fiecare individ din populație este reprezentat printr-un șir binar de gene, unde fiecare genă reprezintă dacă obiectul corespunzător este inclus sau nu în rucsac.

```python
    class Individual:
        def __init__(self, objects, max_weight):
            self.__genes = [random.randint(0, 1) for _ in range(len(objects))]
            self.__objects = objects
            self.__max_weight = max_weight
            self.__fitness = self.evaluate_fitness()

        def evaluate_fitness(self):
            total_weight = 0
            total_value = 0
            for i, gene in enumerate(self.__genes):
                if gene == 1:
                    total_weight += self.__objects[i]["weight"]
                    total_value += self.__objects[i]["value"]

            if total_weight <= self.__max_weight:
                return total_value
            return 0

        def get_fitness(self):
            return self.__fitness

        def set_fitness(self, fitness):
            self.__fitness = fitness

        def get_genes(self):
            return self.__genes

        def set_genes(self, genes):
            self.__genes = genes
```

<br>

2. #### Operatori specifici:
- Încrucișare (crossover): Se realizează prin amestecarea genelor a doi părinți pentru a produce doi copii. Punctul de încrucișare este ales aleatoriu, iar genele sunt schimbate între părinți la acest punct.

```python
        def __crossover(self, parent1, parent2):
        child1, child2 = self.Individual(self.__objects, self.__max_weight), 
                         self.Individual(self.__objects, self.__max_weight)

        if random.random() < self.__crossover_probability:
            crossover_point = random.randint(1, len(parent1.get_genes()) - 1)
            child1.set_genes(parent1.get_genes()[:crossover_point] + 
                             parent2.get_genes()[crossover_point:])
            child2.set_genes(parent2.get_genes()[:crossover_point] + 
                             parent1.get_genes()[crossover_point:])

        child1.set_fitness(child1.evaluate_fitness())
        child2.set_fitness(child2.evaluate_fitness())

        return child1, child2
```
 
- Mutație (mutation): Unele gene din cromozom pot suferi mutații cu o anumită probabilitate. În acest caz, o genă poate fi inversată (0 -> 1 sau 1 -> 0).

```python
        def __mutation(self, individual):
        for i in range(len(individual.get_genes())):
            if random.random() < self.__mutate_probability:
                new_genes = 1 - individual.get_genes()[i]
                individual.get_genes()[i] = new_genes

        individual.set_fitness(individual.evaluate_fitness())
```

3. #### Algoritm și parametrizare:
    - Populația inițială este generată aleator și constă dintr-un număr de indivizi specificat de population_size.
    - Algoritmul evoluează pe un număr de generații specificat de number_of_generations.
    - Probabilitatea de crossover este specificată de crossover_probability, iar probabilitatea de mutație este specificată de mutation_probability.
    - Se selectează indivizii pentru reproducere folosind selecție pe baza fitnesului.
    - Încrucișarea și mutația sunt aplicate pentru a genera o nouă populație.
    - La sfârșitul algoritmului, cel mai bun individ este selectat în funcție de valoarea fitnessului și este întoars ca rezultat.

```python
        def execute_search(self):
        population = [self.Individual(self.__objects, self.__max_weight) for _ in range(self.__population_size)]
        for generation in range(self.__number_of_generations):
            new_population = []
            while len(new_population) < self.__population_size:
                parent1 = self.__selection(population)
                parent2 = self.__selection(population)
                child1, child2 = self.__crossover(parent1, parent2)
                self.__mutation(child1)
                self.__mutation(child2)
                new_population.extend([child1, child2])
            population = sorted(new_population, key=lambda individual: individual.get_fitness(), 
                                reverse=True)[:self.__population_size]

        best_individual = max(population, key=lambda individual: individual.get_fitness())
        return best_individual.get_fitness()
```

## <span style="color: #4285F4"> Algoritm 2 - TSP
1. #### Codificare prin permutări: Fiecare individ din populație reprezintă o posibilă rută pentru problema TSP. Această rută este reprezentată printr-o permutare a orașelor, unde fiecare oraș apare o singură dată.

```python
    def __initialize_population(self):
        city_indexes = list(range(self.__number_of_cities))
        return [random.sample(city_indexes, len(city_indexes)) for _ in range(self.__population_size)]
```

2. #### Operatori specifici:
- Încrucișare (crossover): Două rute părinte sunt încrucișate pentru a crea un copil. Acest lucru se face prin selectarea aleatoare a unei secțiuni dintr-un părinte și completarea rutei copilului cu orașe lipsă din celălalt părinte.

```python
    @staticmethod
    def __crossover(parent1, parent2):
        size = min(len(parent1), len(parent2))
        start, end = sorted(random.sample(range(size), 2))
        child = [None] * size
        child[start:end] = parent1[start:end]

        current_position = end
        for city in parent2:
            if city not in child:
                if current_position >= size:
                    current_position = 0
                child[current_position] = city
                current_position += 1

        return child
```

- Mutație (mutation): Mutația constă în schimbarea pozițiilor a două orașe într-o rută cu o anumită probabilitate.

```python
    @staticmethod
    def __mutation(route):
        index1, index2 = random.sample(range(len(route)), 2)
        route[index1], route[index2] = route[index2], route[index1]
        return route
```

3. #### Algoritm si parametrizare:
- Populația inițială este generată cu dimensiunea specificată de population_size, fiecare individ fiind o rută aleatoare.
- Algoritmul rulează pe un număr de generații specificat de generations.
- Probabilitatea de mutație este dată de mutation_rate.
- Dimensiunea turneului pentru selecție este specificată de tournament_size.
- Selecția se face prin turneu, unde se aleg aleator mai mulți indivizi și se alege cel mai bun dintre aceștia.
- Se realizează crossover și mutație pentru a genera o nouă populație.
- La sfârșitul algoritmului, cea mai bună soluție (cea cu cel mai mic cost) este întoarsă ca rezultat.

```python
    def __involve_population(self):
        new_population = []
        for _ in range(self.__population_size):
            parent1 = self.__selection()
            parent2 = self.__selection()
            child = self.__crossover(parent1, parent2)

            if random.random() < self.__mutation_rate:
                child = self.__mutation(child)
            new_population.append(child)

        self.__population = new_population

    def execute_search(self):
        for _ in range(self.__generations):
            self.__involve_population()

        best_solution = min(self.__population, key=self.__get_cost)
        return self.__get_cost(best_solution)
```

## <span style="color: #4285F4"> Tabele de date - Problema rucsacului

| Instanța problemei | Dimeniune populație | Număr generații | Probabilitate mutatie | Probabilitate încrucișare | Valoare medie | Valoarea cea mai bună | Număr execuții | Timpul mediu de execuție |
|--------------------|---------------------|-----------------|-----------------------|---------------------------|---------------|-----------------------|----------------|--------------------------|
| rucsac-20.txt      | 100                 | 500             | 0.05                  | 0.8                       | 626.4         | 689                   | 10             | 0.9998892784118653       |
|                    | 150                 | 600             | 0.1                   | 0.9                       | 630.1         | 674                   |                | 2.1221488237380983       |
|                    | 80                  | 400             | 0.03                  | 0.7                       | 631.7         | 686                   |                | 0.5941206455230713       |
|                    | 120                 | 550             | 0.07                  | 0.85                      | 640.4         | 669                   |                | 1.4163198471069336       |
|                    | 200                 | 700             | 0.1                   | 0.95                      | 647.7         | 701                   |                | 3.761570191383362        |
| rucsac-200.txt     | 150                 | 1000            | 0.05                  | 0.85                      | 131524.7      | 32156                 |                | 16.360465002059936       |
|                    | 200                 | 800             | 0.1                   | 0.8                       | 131831.3      | 132678                |                | 18.42850818634033        |
|                    | 250                 | 1200            | 0.03                  | 0.9                       | 131923.2      | 132663                |                | 34.4020715713501         |
|                    | 180                 | 900             | 0.07                  | 0.7                       | 132355.0      | 132948                |                | 18.69939227104187        |
|                    | 300                 | 1500            | 0.1                   | 0.95                      | 132079.9      | 132933                |                | 56.758380722999576       |

## <span style="color: #4285F4"> Tabele de date - Problema rucsacului

| Instanța problemei | Dimeniune populație | Număr generații | Probabilitate mutatie | Număr turnee | Valoare medie      | Valoarea cea mai bună | Număr execuții | Timpul mediu de execuție |
|--------------------|---------------------|-----------------|-----------------------|--------------|--------------------|-----------------------|----------------|--------------------------|
| p107.tsp           | 150                 | 800             | 0.05                  | 10           | 52727.30608492149  | 50440.371368153144    | 10             | 66.9789130449295         |
|                    | 200                 | 1000            | 0.03                  | 7            | 47963.381421410435 | 46724.42839542163     |                | 82.56451382637024        |
|                    | 180                 | 900             | 0.07                  | 12           | 49645.303729975494 | 48056.41520348328     |                | 104.42193691730499       |
|                    | 250                 | 1200            | 0.04                  | 8            | 50384.43058484791  | 49428.05046940206     |                | 135.93924987316132       |
|                    | 170                 | 850             | 0.06                  | 15           | 48953.61758606186  | 48049.06050232596     |                | 116.0670039176941        |

## <span style="color: #4285F4"> Observații
### Tabele de date - Problema rucsacului

1. #### Valoare medie și cea mai bună: 
   - Se observă că în general, valorile medii și cele mai bune sunt destul de apropiate, ceea ce sugerează că algoritmul evolutiv produce soluții relativ consistente și că valorile bune nu sunt extrem de rare.

2. #### Dimensiunea populației și numărul de generații: 
   - Există o variație în performanța algoritmului în funcție de dimensiunea populației și numărul de generații. În general, o creștere a dimensiunii populației și a numărului de generații pare să conducă la o valoare mai bună pentru soluția cea mai bună, dar aceasta poate crește și timpul de execuție.
   
3. #### Probabilitatea de mutație și încrucișare: 
   - Valorile optime pentru acești parametri pot varia în funcție de problemă. În general, o probabilitate moderată de mutație și o probabilitate mai mare de încrucișare pot ajuta la explorarea spațiului soluțiilor mai eficient.

4. #### Timpul de execuție: 
   - Se observă că timpul de execuție crește odată cu creșterea dimensiunii populației și a numărului de generații. Acest lucru este de așteptat, deoarece algoritmii evolutivi necesită o evaluare repetată a populației și a funcției fitness.
   
5. #### Variabilitatea rezultatelor între rulări: 
   - Pentru fiecare set de parametri, este important să se ia în considerare variabilitatea rezultatelor între rulări diferite ale algoritmului. Este posibil ca unele configurații să fie mai sensibile la variabilitate decât altele.

### Tabele de date - TSP

1. #### Valoare medie și cea mai bună: 
   - Se observă că valoarea medie și cea mai bună a funcției obiectiv sunt relativ apropiate în fiecare configurație de parametri. Acest lucru sugerează că algoritmul evolutiv a fost capabil să genereze soluții de calitate în mod consistent.
   
2. #### Dimensiunea populației și numărul de generații: 
   - Există o variație a dimensiunii populației și a numărului de generații între diferite configurații. În general, creșterea dimensiunii populației și a numărului de generații poate duce la o îmbunătățire a valorii celei mai bune.
   
3. #### Probabilitatea de mutație și numărul de turnee: 
   - Probabilitatea de mutație și numărul de turnee par să fie parametri importanți în determinarea performanței algoritmului. Valorile alese pentru acești parametri variază între configurații și pot influența calitatea soluției.
   
4. #### Timpul de execuție: 
   - Timpul mediu de execuție crește odată cu creșterea dimensiunii populației, a numărului de generații și a numărului de turnee. Acest lucru este de așteptat, deoarece o creștere a acestor parametri poate duce la o creștere a complexității algoritmului.
   
5. #### Variabilitatea rezultatelor între rulări: 
   - Este important să se ia în considerare variabilitatea rezultatelor între diferitele rulări ale algoritmului. Pentru fiecare set de parametri, este posibil să existe o variație în valorile celei mai bune, ceea ce ar putea indica sensibilitatea algoritmului la alegerile aleatoare sau la parametrii specifici.

## <span style="color: #4285F4"> Concluzie

Această analiză oferă o prezentare cuprinzătoare a algoritmilor evolutivi în rezolvarea a două probleme combinatorice: rucsacul și problema comis-voiajorului (TSP).
Pentru problema rucsacului, am implementat un algoritm evolutiv folosind o codificare binară a soluțiilor, împreună cu operatorii specifici de încrucișare și mutație. Am analizat, de asemenea, tabelele de date asociate rulărilor algoritmului pentru diferite instanțe ale problemei rucsacului, evidențiind impactul parametrilor asupra performanței și timpului de execuție.
Pentru problema TSP, am prezentat o implementare a algoritmului evolutiv utilizând o codificare prin permutări, împreună cu operatorii specifici de încrucișare și mutație. Am examinat, de asemenea, tabelele de date pentru diferite instanțe ale problemei TSP, evidențiind influența parametrilor asupra performanței și timpului de execuție.

## <span style="color: #4285F4"> Datele obținute după rulări
- ### Problema rucsacului

```python
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/rucsac/data1.txt
   Dimensiune populatie = 100
   Numar generatii = 500
   Probabilitate de mutatie: 0.05
   Probabilitate de incrucisare: 0.8
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   599          1.0034830570220947
   646          0.9940037727355957
   611          1.0047736167907715
   633          1.0029208660125732
   600          1.0320525169372559
   658          0.9912521839141846
   689          0.9991247653961182
   587          0.9919121265411377
   659          0.9854133129119873
   582          0.9939565658569336
   
   Valoare medie obtinuta: 626.4
   Valoare maxima obtinuta: 689
   Timp de executie mediu: 0.9998892784118653
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/rucsac/data1.txt
   Dimensiune populatie = 150
   Numar generatii = 600
   Probabilitate de mutatie: 0.1
   Probabilitate de incrucisare: 0.9
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   631          2.139044761657715
   624          2.122554063796997
   618          2.108004093170166
   625          2.1071579456329346
   621          2.1168129444122314
   642          2.1113791465759277
   641          2.123065948486328
   636          2.13079833984375
   589          2.126185417175293
   674          2.1364855766296387
   
   Valoare medie obtinuta: 630.1
   Valoare maxima obtinuta: 674
   Timp de executie mediu: 2.1221488237380983
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/rucsac/data1.txt
   Dimensiune populatie = 80
   Numar generatii = 400
   Probabilitate de mutatie: 0.03
   Probabilitate de incrucisare: 0.7
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   649          0.6118056774139404
   616          0.590174674987793
   657          0.5940492153167725
   584          0.5918381214141846
   682          0.5955612659454346
   686          0.5935587882995605
   650          0.5888044834136963
   565          0.5953388214111328
   598          0.5882775783538818
   630          0.5917978286743164
   
   Valoare medie obtinuta: 631.7
   Valoare maxima obtinuta: 686
   Timp de executie mediu: 0.5941206455230713
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/rucsac/data1.txt
   Dimensiune populatie = 120
   Numar generatii = 550
   Probabilitate de mutatie: 0.07
   Probabilitate de incrucisare: 0.85
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   664          1.4452803134918213
   642          1.4134087562561035
   652          1.4041452407836914
   645          1.405646562576294
   669          1.4048714637756348
   639          1.4088726043701172
   640          1.4342589378356934
   633          1.41790771484375
   592          1.4122707843780518
   628          1.4165360927581787
   
   Valoare medie obtinuta: 640.4
   Valoare maxima obtinuta: 669
   Timp de executie mediu: 1.4163198471069336
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/rucsac/data1.txt
   Dimensiune populatie = 200
   Numar generatii = 700
   Probabilitate de mutatie: 0.1
   Probabilitate de incrucisare: 0.95
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   592          3.7711634635925293
   683          3.778599500656128
   611          3.753607749938965
   636          3.72934889793396
   641          3.7713980674743652
   701          3.7485978603363037
   686          3.75091814994812
   618          3.8005220890045166
   635          3.7375054359436035
   674          3.774040699005127
   
   Valoare medie obtinuta: 647.7
   Valoare maxima obtinuta: 701
   Timp de executie mediu: 3.761570191383362
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/rucsac/data1.txt
   Dimensiune populatie = 200
   Numar generatii = 700
   Probabilitate de mutatie: 0.05
   Probabilitate de incrucisare: 0.85
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   131466          15.590557098388672
   131801          16.434511423110962
   131030          16.34345579147339
   131455          16.684589385986328
   131715          16.605935096740723
   131142          16.54843282699585
   131282          15.906180381774902
   131881          15.61572813987732
   132156          16.62604308128357
   131319          17.24921679496765
   
   Valoare medie obtinuta: 131524.7
   Valoare maxima obtinuta: 132156
   Timp de executie mediu: 16.360465002059936
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/rucsac/data1.txt
   Dimensiune populatie = 200
   Numar generatii = 700
   Probabilitate de mutatie: 0.1
   Probabilitate de incrucisare: 0.8
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   132315          17.868011713027954
   131734          17.053463459014893
   131259          18.680991649627686
   131927          19.064636945724487
   131806          19.395692348480225
   132002          19.617587327957153
   131458          18.121642351150513
   132678          17.353469371795654
   131281          17.99161195755005
   131853          19.137974739074707
   
   Valoare medie obtinuta: 131831.3
   Valoare maxima obtinuta: 132678
   Timp de executie mediu: 18.42850818634033
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/rucsac/data1.txt
   Dimensiune populatie = 200
   Numar generatii = 700
   Probabilitate de mutatie: 0.03
   Probabilitate de incrucisare: 0.9
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   131258          35.20501351356506
   132543          34.524916887283325
   131558          33.03598427772522
   132663          34.84184241294861
   131190          33.62112832069397
   132178          35.19812297821045
   131591          33.29501557350159
   131618          34.4257607460022
   132592          36.335171699523926
   132041          33.53775930404663
   
   Valoare medie obtinuta: 131923.2
   Valoare maxima obtinuta: 132663
   Timp de executie mediu: 34.4020715713501
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/rucsac/data1.txt
   Dimensiune populatie = 200
   Numar generatii = 700
   Probabilitate de mutatie: 0.07
   Probabilitate de incrucisare: 0.7
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   132305          17.156240701675415
   132148          18.63343048095703
   132686          19.165507316589355
   131847          19.327374696731567
   132028          19.2628390789032
   132385          19.260897397994995
   132722          19.037328243255615
   132064          18.745243310928345
   132948          18.1112539768219
   132417          18.29380750656128
   
   Valoare medie obtinuta: 132355.0
   Valoare maxima obtinuta: 132948
   Timp de executie mediu: 18.69939227104187
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/rucsac/data1.txt
   Dimensiune populatie = 200
   Numar generatii = 700
   Probabilitate de mutatie: 0.1
   Probabilitate de incrucisare: 0.95
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   131866          56.728564977645874
   132033          57.14550709724426
   132093          55.614903926849365
   132019          58.91666626930237
   131810          56.42019844055176
   131556          57.07795214653015
   132428          56.91691255569458
   131991          56.11074113845825
   132070          56.68339920043945
   132933          55.96896147727966
   
   Valoare medie obtinuta: 132079.9
   Valoare maxima obtinuta: 132933
   Timp de executie mediu: 56.758380722999576
```

- ### TSP

```python
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/tsp/data.tsp
   Dimensiune populatie = 150
   Numar generatii = 800
   Probabilitate de mutatie: 0.05
   Dimensiunea turneului: 10
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   57212.25181954206          69.78454399108887
   54628.143874218236          68.37256336212158
   52929.82342003655          67.32363414764404
   52515.06535657027          64.83530735969543
   52445.45458253373          67.1115791797638
   52251.3332852899          67.63183212280273
   52153.11858118114          67.62812852859497
   51985.995858998416          64.95693707466125
   50711.50270269142          66.7570059299469
   50440.371368153144          65.38759875297546
   
   Valoare medie obtinuta: 52727.30608492149
   Valoare maxima obtinuta: 50440.371368153144
   Timp de executie mediu: 66.9789130449295
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/tsp/data.tsp
   Dimensiune populatie = 200
   Numar generatii = 1000
   Probabilitate de mutatie: 0.03
   Dimensiunea turneului: 7
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   52781.328243657146          85.2541971206665
   49638.92163053083          81.78220629692078
   48420.656545899874          82.59607577323914
   48144.29210244016          82.17726874351501
   46971.64199092159          83.38962960243225
   46779.260118968195          81.32447075843811
   46724.42839542163          81.45643138885498
   46724.42839542163          80.03636074066162
   46724.42839542163          84.60656929016113
   46724.42839542163          83.02192854881287
   
   Valoare medie obtinuta: 47963.381421410435
   Valoare maxima obtinuta: 46724.42839542163
   Timp de executie mediu: 82.56451382637024
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/tsp/data.tsp
   Dimensiune populatie = 180
   Numar generatii = 900
   Probabilitate de mutatie: 0.07
   Dimensiunea turneului: 12
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   55716.20638703658          104.20761609077454
   52198.56997171227          102.64014172554016
   50598.149595973366          102.13737368583679
   49166.0907309541          102.02504301071167
   48491.94459666217          105.36601257324219
   48056.41520348328          106.76005578041077
   48056.41520348328          104.74189710617065
   48056.41520348328          105.19562649726868
   48056.41520348328          107.19746208190918
   48056.41520348328          103.9481406211853
   
   Valoare medie obtinuta: 49645.303729975494
   Valoare maxima obtinuta: 48056.41520348328
   Timp de executie mediu: 104.42193691730499
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/tsp/data.tsp
   Dimensiune populatie = 250
   Numar generatii = 1200
   Probabilitate de mutatie: 0.04
   Dimensiunea turneului: 8
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   54230.27022832371          133.9689235687256
   51916.18958978679          133.13003182411194
   50724.85936708205          131.28531336784363
   50061.17858436666          139.6531810760498
   49985.918115858105          135.02295517921448
   49797.06278337546          138.2072594165802
   49472.413784600125          138.10408926010132
   49428.05046940206          134.89803218841553
   49297.202583083395          136.8369104862213
   48931.16034260083          138.28580236434937
   
   Valoare medie obtinuta: 50384.43058484791
   Valoare maxima obtinuta: 49428.05046940206
   Timp de executie mediu: 135.93924987316132
   
   Algoritm folosit: algoritm evolutiv
   Fisier de intrare: config/tsp/data.tsp
   Dimensiune populatie = 170
   Numar generatii = 850
   Probabilitate de mutatie: 0.06
   Dimensiunea turneului: 15
   Numar rulari: 10. Rezultatele obtinute sunt:
   
   53482.14070987614          115.16522145271301
   50238.690346100164          116.23645067214966
   48536.31288072215          114.59764266014099
   48477.87664894548          118.54968452453613
   48425.45917931948          116.02525734901428
   48179.45408635132          114.00480508804321
   48049.06050232596          117.37790727615356
   48049.06050232596          116.51332902908325
   48049.06050232596          114.39777517318726
   48049.06050232596          117.80196595191956
   
   Valoare medie obtinuta: 48953.61758606186
   Valoare maxima obtinuta: 48049.06050232596
   Timp de executie mediu: 116.0670039176941
```