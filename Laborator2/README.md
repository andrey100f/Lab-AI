
<h1 align="center" style="color: #4285F4">Căutare tabu</h1>

## <span style="color: #4285F4"> Cerința problemei

1. Să se implementeze algoritmul Tabu Search pentru problema rucsacului.
2. Să se implementeze algoritmul Tabu Search pentru problema TSP. 

## <span style="color: #4285F4"> Algoritm 1 - Problema rucsacului
1. Generarea unei soluţii aleatoare - Această funcție primește o listă de obiecte și construiește o soluție asociată acestora. Pentru fiecare obiect din lista de obiecte, funcția alege aleatoriu între două valori posibile (0 sau 1) și atribuie această alegere soluției. Astfel, soluția generată este o listă de valori binare care indică o alegere arbitrară pentru fiecare obiect din lista dată. Soluția generată este apoi returnată.
```python
    def __generate_solution():
        solution = []
        for _ in range(len(self.__objects)):
            choice = random.choice([0, 1])
            solution.append(choice)
        return solution
```

2. Verificare soluție validă - Această funcție primește o soluție și evaluează dacă aceasta respectă restricțiile impuse de greutatea maximă. Parcurge fiecare obiect din soluție și calculează greutatea și valoarea totală a obiectelor incluse. Dacă greutatea totală este mai mică sau egală cu greutatea maximă permisă, funcția returnează valoarea totală a obiectelor incluse în soluție, altfel returnează 0.
```python
    def __evaluate_solution(solution):
        total_weight = 0
        total_value = 0
        for i in range(0, len(solution)):
            if solution[i] == 1:
                total_weight += self.__objects[i]["weight"]
                total_value += self.__objects[i]["value"]
   
        if total_weight <= self.__max_weight:
            return total_value
        return 0
```

3. Alegere cea mai bună soluție - Algoritmul de căutare tabu explorează spațiul soluțiilor, selectând vecinii optimi și evitând soluțiile anterioare într-un număr fix de iterații. Scopul său este să găsească o soluție de calitate superioară, evitând ciclurile și promovând diversitatea.
```python
    def execute_search(self):
        solution = self.__generate_solution()
        solution_quality = self.__evaluate_solution(solution)
        memory = []

        for _ in range(self.__iterations):
            best_neighbour = None
            best_neighbour_quality = 0
            neighbours = self.__generate_neighbours(solution)
            found = False

            for neighbour in neighbours:
                if neighbour not in memory:
                    neighbour_quality = self.__evaluate_solution(neighbour)
                    if neighbour_quality > best_neighbour_quality:
                        found = True
                        best_neighbour = neighbour
                        best_neighbour_quality = neighbour_quality

            if found is True:
                solution_quality = best_neighbour_quality
                solution = best_neighbour
                memory.append(best_neighbour)

                if len(memory) > self.__tabu_iterations:
                    memory.pop(0)

        return solution_quality
```

## <span style="color: #4285F4"> Algoritm 2 - TSP
1. Se generează un vecin al rutei curente prin inversarea poziției a două orașe aleatoare.
```python
    @staticmethod
    def generate_neighbours(solution):
        a, b = sorted(random.sample(range(len(solution)), 2))
        return solution[:a] + solution[a:b + 1][::-1] + solution[b + 1:]
```

2. Se calculează costul vecinului generat.
```python
    def __get_city_distance(self, city1, city2):
        x1, y1 = self.__cities[city1]["city_x"], self.__cities[city1]["city_y"]
        x2, y2 = self.__cities[city2]["city_x"], self.__cities[city2]["city_y"]

        return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
```

<br>
<br>

```python
    def __get_cost(self, route):
        total_cost = 0
        for i in range(len(route) - 1):
            total_cost += self.__get_city_distance(route[i], route[i + 1])

        total_cost += self.__get_city_distance(route[-1], route[0])

        return total_cost
```

3. Se verifică dacă vecinul este o îmbunătățire față de ruta curentă și dacă nu este deja în memoria tabu.
4. Dacă condițiile sunt îndeplinite, ruta curentă și costul acesteia sunt actualizate, iar perechea de orașe este marcată ca tabu în memorie pentru un număr de iterații.
5. Memoria tabu este actualizată, reducând contorul pentru fiecare pereche de orașe.
6. Se returnează costul celei mai bune rute găsite.

```python
    def execute_search(self):
        memory = [[0] * self.__number_of_cities for _ in range(self.__number_of_cities)]

        current_route = list(range(self.__number_of_cities))
        random.shuffle(current_route)
        cost_current_route = self.__get_cost(current_route)

        for _ in range(self.__iterations):
            neighbour = self.generate_neighbours(current_route)
            city_1, city_2 = random.sample(range(self.__number_of_cities), 2)
            cost_neighbour = self.__get_cost(neighbour)

            is_tabu = memory[city_1][city_2] > 0

            if not is_tabu and cost_neighbour < cost_current_route:
                current_route = neighbour
                cost_current_route = cost_neighbour

                memory[city_1][city_2] = self.__tabu_iterations

            for i in range(self.__number_of_cities):
                for j in range(self.__number_of_cities):
                    if memory[i][j] > 0:
                        memory[i][j] -= 1

        return cost_current_route
```

<br>
<br>
<br>
<br>
<br>

## <span style="color: #4285F4"> Tabele de date - Problema rucsacului

| Instanța problemei | Număr iterații | Număr iterații tabu | Valoare medie | Valoarea cea mai bună   | Număr execuții | Timpul mediu de execuție |
|--------------------|---------------|---------------------|---------------|-------------------------|----------------|--------------------------|
| rucsac-20.txt      | 1000          | 10                  | 389.8         | 710                     | 10             | 0.09875030517578125      |
|                    | 2000          | 25                  | 513.9         | 702                     |                | 0.19565095901489257      |
|                    | 5000          | 50                  | 527.9         | 710                     |                | 1.0052310466766357       |
|                    | 8000          | 50                  | 558.6         | 626                     |                | 1.0052310466766357       |
|                    | 9000          | 75                  | 326.9         | 690                     |                | 2.0484720945358275       |
| rucsac-200.txt     | 1000          | 90                  | 105152.0      | 132220                  |                | 8.193205833435059        |
|                    | 2000          | 80                  | 65719.4       | 131813                  |                | 4.098495054244995        |
|                    | 3000          | 70                  | 91925.8       | 131939                  |                | 6.4521314144134525       |
|                    | 4000          | 60                  | 78960.4       | 132448                  |                | 6.014973211288452        |
|                    | 5000          | 50                  | 79095.4       | 132436                  |                | 4.833865094184875        |
| data.txt           | 1500          | 100                 | 5402.4        | 5434                    |                | 4.4578375816345215       |
|                    | 800           | 80                  | 5420.1        | 5434                    |                | 1.7497363805770874       |
|                    | 900           | 90                  | 5400.5        | 5408                    |                | 2.275900530815124        |
|                    | 1000          | 75                  | 5404.6        | 5422                    |                | 3.348079037666321        |
|                    | 2000          | 200                 | 5416.4        | 5434                    |                | 6.758050012588501        |

## <span style="color: #4285F4"> Tabele de date - TSP

| Instanța problemei | Număr iterații | Număr iterații tabu | Valoare medie  | Valoarea cea mai bună | Număr execuții | Timpul mediu de execuție |
|--------------------|----------------|---------------------|----------------|-----------------------|--------------|--------------------------|
| p107.tsp           | 10000          | 100                 | 56356.7100938  | 51431.1794086         | 10           | 2.8450778                |
|                    | 9000           | 100                 | 55570.4564823  | 52302.8061956         |              | 2.5611207                |
|                    | 8500           | 200                 | 58505.7066170  | 50621.3791760         |              | 2.4171511                |
|                    | 9500           | 200                 | 56577.3916400  | 50807.6903361         |              | 2.6959146                |
|                    | 10000          | 200                 | 53682.0622511  | 49199.3024040         |              | 2.8323531                |

## <span style="color: #4285F4"> Observații
### Tabele de date - Problema rucsacului
1. #### Valorile medii și cele mai bune:
    - Diferențele semnificative dintre valorile medii și cele mai bune indică variații considerabile în performanța algoritmului pentru diferite instanțe ale problemei și setări ale parametrilor. Aceste variații pot fi rezultatul complexității diferite a problemelor sau a eficacității diferite a configurărilor algoritmului.

2. #### Impactul parametrilor algoritmului:
    - Schimbările în numărul total de iterații și numărul de iterații tabu influențează modul în care algoritmul explorează și optimizează spațiul soluțiilor. Ajustările acestor parametri pot afecta timpul și calitatea soluțiilor obținute.

3. #### Timpul de execuție:
    - Creșterea dimensiunii problemei conduce la creșterea timpului de execuție, deoarece algoritmul trebuie să exploreze un spațiu soluții mai mare. Acest lucru poate afecta practicabilitatea utilizării algoritmului pentru probleme mari sau complexe, deoarece timpul de execuție poate deveni prohibitiv.

4. #### Numărul de iterații tabu:
    - Modificările în numărul de iterații tabu influențează strategia de explorare a algoritmului și capacitatea sa de a evita ciclurile și de a explora mai bine spațiul soluțiilor. Ajustarea acestui parametru poate fi crucială pentru obținerea unor rezultate optime sau apropiate de optim într-un timp rezonabil.

### Tabele de date - TSP
1. #### Variația valorilor medii și a valorilor celei mai bune:
    - Valorile medii și cele mai bune variază semnificativ între diferitele configurații ale algoritmului pentru aceeași instanță a problemei. De exemplu, pentru instanța "p107.tsp", valorile medii și cele mai bune sunt diferite în funcție de numărul de iterații și de numărul de iterații tabu. Acest lucru indică faptul că modificarea acestor parametri poate influența semnificativ rezultatele obținute.

2. ##### Impactul parametrilor algoritmului:
    - Numărul total de iterații și numărul de iterații tabu au un impact asupra performanței algoritmului. În cazul instanței "p107.tsp", observăm că valorile medii și cele mai bune se modifică în funcție de acești parametri. De exemplu, o creștere a numărului de iterații tabu poate duce la o îmbunătățire a valorii celei mai bune, dar poate afecta timpul de execuție.

3. #### Timpul de execuție:
    - Timpul de execuție variază în funcție de numărul de iterații și de numărul de iterații tabu. În cazul instanței "p107.tsp", observăm că timpul de execuție crește odată cu creșterea acestor parametri. Acest lucru sugerează că algoritmul necesită mai mult timp pentru a efectua o căutare mai profundă sau pentru a explora un spațiu de căutare mai larg.

4. #### Numărul de iterații tabu:
    - Variația în numărul de iterații tabu poate duce la rezultate diferite pentru aceeași instanță a problemei. În cazul instanței "p107.tsp", observăm că valorile cele mai bune și cele medii se modifică atunci când se schimbă acest parametru. Alegerea unui număr optim de iterații tabu poate fi importantă pentru obținerea unei soluții de calitate superioară într-un timp rezonabil.

## <span style="color: #4285F4"> Concluzie

În cadrul acestei analize se evidențiază importanța și impactul parametrilor algoritmului Tabu Search în rezolvarea problemelor de optimizare, precum rucsacul și TSP. Variațiile în numărul total de iterații și numărul de iterații tabu influențează performanța algoritmului, afectând atât calitatea soluțiilor obținute, cât și timpul de execuție. Este crucial să se ajusteze acești parametri în funcție de specificul problemei și de cerințele de performanță, pentru a obține rezultate optime într-un timp rezonabil. Implementarea și optimizarea corespunzătoare a algoritmului Tabu Search pot oferi soluții eficiente și scalabile pentru o gamă diversă de probleme de optimizare combinatorică.

## <span style="color: #4285F4"> Datele obținute după rulări
- ### Problema rucsacului

```python
Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data1.txt
Numar iteratii = 1000
Iteratii tabu: 10
Numar rulari: 10. Rezultatele obtinute sunt:

710          0.09622907638549805
645          0.10733652114868164
0          0.09911894798278809
635          0.09791111946105957
680          0.09691405296325684
0          0.0993809700012207
593          0.1002500057220459
635          0.0976254940032959
0          0.09645938873291016
0          0.09627747535705566

Valoare medie obtinuta: 389.8
Valoare maxima obtinuta: 710
Timp de executie mediu: 0.09875030517578125

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data1.txt
Numar iteratii = 2000
Iteratii tabu: 25
Numar rulari: 10. Rezultatele obtinute sunt:

641          0.19341611862182617
595          0.19540047645568848
685          0.19811773300170898
0          0.1927626132965088
702          0.1949005126953125
569          0.19451355934143066
698          0.19581985473632812
0          0.197098970413208
593          0.19761180877685547
656          0.1968679428100586

Valoare medie obtinuta: 513.9
Valoare maxima obtinuta: 702
Timp de executie mediu: 0.19565095901489257

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data1.txt
Numar iteratii = 5000
Iteratii tabu: 50
Numar rulari: 10. Rezultatele obtinute sunt:

633          1.0262532234191895
710          1.0207569599151611
678          1.0120892524719238
628          1.0145723819732666
663          1.0110797882080078
622          1.0146782398223877
0          0.9580943584442139
0          0.9703149795532227
679          1.007908821105957
666          1.0165624618530273

Valoare medie obtinuta: 527.9
Valoare maxima obtinuta: 710
Timp de executie mediu: 1.0052310466766357

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data1.txt
Numar iteratii = 8000
Iteratii tabu: 50
Numar rulari: 10. Rezultatele obtinute sunt:

0          1.9429879188537598
0          1.9581241607666016
663          1.9981846809387207
0          1.937669038772583
690          2.0999302864074707
0          2.0702953338623047
683          2.1322152614593506
586          2.1366586685180664
0          2.0895633697509766
647          2.1190922260284424

Valoare medie obtinuta: 326.9
Valoare maxima obtinuta: 690
Timp de executie mediu: 2.0484720945358275

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data1.txt
Numar iteratii = 9000
Iteratii tabu: 75
Numar rulari: 10. Rezultatele obtinute sunt:

0          3.038950204849243
583          3.1665995121002197
624          3.080070972442627
698          3.0764541625976562
0          3.037330389022827
548          3.0274853706359863
691          3.031325101852417
0          2.9334187507629395
710          3.041685104370117
698          3.0270559787750244

Valoare medie obtinuta: 455.2
Valoare maxima obtinuta: 710
Timp de executie mediu: 3.0460375547409058

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data2.txt
Numar iteratii = 1000
Iteratii tabu: 90
Numar rulari: 10. Rezultatele obtinute sunt:

131695          8.355234861373901
130810          8.456541776657104
130414          8.47107219696045
0          8.2930588722229
132220          8.033105850219727
131061          7.866136312484741
131924          8.104143857955933
131741          8.151685953140259
0          8.09805965423584
131655          8.103018999099731

Valoare medie obtinuta: 105152.0
Valoare maxima obtinuta: 132220
Timp de executie mediu: 8.193205833435059

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data2.txt
Numar iteratii = 2000
Iteratii tabu: 80
Numar rulari: 10. Rezultatele obtinute sunt:

0          3.9523534774780273
131612          3.919863224029541
0          4.023026466369629
0          4.123641014099121
0          4.020509243011475
0          4.226733446121216
131133          4.169024229049683
131813          4.255748748779297
131192          4.151668548583984
131444          4.1423821449279785

Valoare medie obtinuta: 65719.4
Valoare maxima obtinuta: 131813
Timp de executie mediu: 4.098495054244995

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data2.txt
Numar iteratii = 3000
Iteratii tabu: 70
Numar rulari: 10. Rezultatele obtinute sunt:

130941          6.398402214050293
0          6.4887213706970215
131341          6.42028284072876
0          6.482431173324585
131933          6.3584089279174805
130636          6.383695363998413
0          6.409343957901001
131939          6.722402095794678
130904          6.500302314758301
131564          6.357323884963989

Valoare medie obtinuta: 91925.8
Valoare maxima obtinuta: 131939
Timp de executie mediu: 6.4521314144134525

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data2.txt
Numar iteratii = 4000
Iteratii tabu: 60
Numar rulari: 10. Rezultatele obtinute sunt:

0          5.878014802932739
130406          6.00905704498291
132107          6.185466527938843
0          6.045996904373169
131642          5.972116470336914
131194          5.940763235092163
0          6.088552236557007
132448          6.009718894958496
0          5.962660074234009
131807          6.0573859214782715

Valoare medie obtinuta: 78960.4
Valoare maxima obtinuta: 132448
Timp de executie mediu: 6.014973211288452

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data2.txt
Numar iteratii = 5000
Iteratii tabu: 50
Numar rulari: 10. Rezultatele obtinute sunt:

0          4.875694513320923
132436          4.806027173995972
131412          4.965473651885986
0          5.012241363525391
130527          4.75596809387207
132336          4.797791242599487
0          4.750830888748169
132314          4.758443355560303
0          4.782165050506592
131929          4.834015607833862

Valoare medie obtinuta: 79095.4
Valoare maxima obtinuta: 132436
Timp de executie mediu: 4.833865094184875

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data3.txt
Numar iteratii = 1500
Iteratii tabu: 100
Numar rulari: 10. Rezultatele obtinute sunt:

5409          4.641579866409302
5434          4.500981092453003
5407          4.472340106964111
5377          4.445517063140869
5407          4.415407419204712
5394          4.420781373977661
5393          4.425315856933594
5406          4.421192646026611
5404          4.4066572189331055
5393          4.428603172302246

Valoare medie obtinuta: 5402.4
Valoare maxima obtinuta: 5434
Timp de executie mediu: 4.4578375816345215

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data3.txt
Numar iteratii = 800
Iteratii tabu: 80
Numar rulari: 10. Rezultatele obtinute sunt:

5422          1.7650625705718994
5434          1.7363500595092773
5422          1.7763981819152832
5434          1.7468037605285645
5409          1.750678300857544
5409          1.7584848403930664
5421          1.7331998348236084
5421          1.7317917346954346
5434          1.756049394607544
5395          1.7425451278686523

Valoare medie obtinuta: 5420.1
Valoare maxima obtinuta: 5434
Timp de executie mediu: 1.7497363805770874

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data3.txt
Numar iteratii = 900
Iteratii tabu: 90
Numar rulari: 10. Rezultatele obtinute sunt:

5395          2.3031697273254395
5408          2.3529398441314697
5395          2.365339994430542
5407          2.3229708671569824
5393          2.2991480827331543
5394          2.2806386947631836
5408          2.254908561706543
5406          2.188333511352539
5392          2.197941541671753
5407          2.1936144828796387

Valoare medie obtinuta: 5400.5
Valoare maxima obtinuta: 5408
Timp de executie mediu: 2.2759005308151243

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data3.txt
Numar iteratii = 1000
Iteratii tabu: 75
Numar rulari: 10. Rezultatele obtinute sunt:

5422          3.4056930541992188
5389          3.404829502105713
5405          3.3842082023620605
5380          3.3154125213623047
5377          3.3234195709228516
5405          3.337252140045166
5422          3.3161957263946533
5407          3.3351635932922363
5419          3.3450963497161865
5420          3.3135197162628174

Valoare medie obtinuta: 5404.6
Valoare maxima obtinuta: 5422
Timp de executie mediu: 3.348079037666321

Algoritm folosit: tabu search
Fisier de intrare: config/rucsac/data3.txt
Numar iteratii = 2000
Iteratii tabu: 200
Numar rulari: 10. Rezultatele obtinute sunt:

5420          6.614280700683594
5419          6.552063941955566
5407          6.543187141418457
5406          6.621881008148193
5419          6.957437992095947
5434          7.00201940536499
5421          6.711101055145264
5422          6.897815227508545
5409          6.984920263290405
5407          6.695793390274048

Valoare medie obtinuta: 5416.4
Valoare maxima obtinuta: 5434
Timp de executie mediu: 6.758050012588501
```

- ### TSP

```python
Algoritm folosit: tabu search
Fisier de intrare: config/tsp/data.tsp
Numar iteratii = 0
Iteratii tabu: 0
Numar rulari: 10. Rezultatele obtinute sunt:

51431.17940867871          2.9147260189056396
54214.95107368278          2.8388280868530273
53459.43723573226          2.905231237411499
52032.486257729          2.832479476928711
53660.37865961295          2.835160255432129
54290.7833707432          2.821065664291382
65396.73236027859          2.8238465785980225
66028.56373293651          2.8341240882873535
55977.88716448159          2.823261022567749
57074.70167491242          2.822056531906128

Valoare medie obtinuta: 56356.710093878806
Valoare maxima obtinuta: 66028.56373293651
Timp de executie mediu: 2.845077896118164

Algoritm folosit: tabu search
Fisier de intrare: config/tsp/data.tsp
Numar iteratii = 0
Iteratii tabu: 0
Numar rulari: 10. Rezultatele obtinute sunt:

52302.80619567555          2.6047475337982178
54069.80173501648          2.5930635929107666
54209.22741102893          2.5530078411102295
54057.76393758788          2.5425240993499756
53644.091384038074          2.546781063079834
58866.017199426205          2.550985336303711
57121.66253411236          2.5614986419677734
52395.41254066692          2.5560200214385986
59106.556294776055          2.550248384475708
59931.22559145856          2.55233097076416

Valoare medie obtinuta: 55570.45648237869
Valoare maxima obtinuta: 59931.22559145856
Timp de executie mediu: 2.5611207485198975

Algoritm folosit: tabu search
Fisier de intrare: config/tsp/data.tsp
Numar iteratii = 0
Iteratii tabu: 0
Numar rulari: 10. Rezultatele obtinute sunt:

52358.92844964662          2.403346061706543
57223.27363760309          2.3950037956237793
68849.52768769408          2.3893136978149414
50621.379176043025          2.4562416076660156
65011.810006428124          2.3888356685638428
55724.193896455894          2.399559736251831
54316.4688596085          2.4169623851776123
68913.60997562755          2.4085018634796143
57368.81752284855          2.407569169998169
54669.05695836846          2.5061774253845215

Valoare medie obtinuta: 58505.70661703239
Valoare maxima obtinuta: 68913.60997562755
Timp de executie mediu: 2.417151141166687

Algoritm folosit: tabu search
Fisier de intrare: config/tsp/data.tsp
Numar iteratii = 0
Iteratii tabu: 0
Numar rulari: 10. Rezultatele obtinute sunt:

54128.59382152417          2.6767117977142334
55555.14486510926          2.6958227157592773
55951.391594449204          2.6636741161346436
64657.36483987279          2.6690495014190674
54348.90124018894          2.665588140487671
56463.222398549646          2.6724517345428467
65097.57109578113          2.661221742630005
52660.471209532145          2.907907485961914
50807.690336122956          2.674306631088257
56103.56499896333          2.6724131107330322

Valoare medie obtinuta: 56577.39164000936
Valoare maxima obtinuta: 65097.57109578113
Timp de executie mediu: 2.695914697647095

Algoritm folosit: tabu search
Fisier de intrare: config/tsp/data.tsp
Numar iteratii = 0
Iteratii tabu: 0
Numar rulari: 10. Rezultatele obtinute sunt:

54880.752339939965          3.004229784011841
54887.556861596655          2.816688299179077
49199.302404013026          2.8285555839538574
52900.36167614592          2.822951316833496
53984.299386010454          2.821786403656006
52630.04596333591          2.8181116580963135
54499.624416905004          2.7788267135620117
50617.40936387038          2.798164129257202
56112.6944231586          2.8129913806915283
57108.575676937835          2.8212263584136963

Valoare medie obtinuta: 53682.062251191375
Valoare maxima obtinuta: 57108.575676937835
Timp de executie mediu: 2.8323531627655028
```
