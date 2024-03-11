
<h1 align="center" style="color: #4285F4">Căutare aleatoare și căutare locală</h1>

## <span style="color: #4285F4"> Cerința problemei

1. Să se implementeze o metodă de căutare aleatoare (random search) pentru problema rucsacului.
2. Să se implementeze Next Ascent Hill-Climbing pentru problema rucsacului.

## <span style="color: #4285F4"> Algoritm 1 - Random Search
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

3. Alegere cea mai bună soluție - Această funcție execută un algoritm de căutare pentru a găsi o soluție optimă pentru o problemă dată. Prin generarea repetată de soluții aleatoare și evaluarea calității acestora, funcția actualizează și menține cea mai bună soluție găsită până în acel moment. La finalul numărului specificat de iterații, funcția returnează calitatea celei mai bune soluții găsite.
```python
    def execute_search(self, iterations):
        for i in range(iterations):
            solution = self.__generate_solution()
            solution_quality = self.__evaluate_solution(solution)
            if solution_quality > self.__best_quality:
                self.__best_quality = solution_quality
        return self.__best_quality
```

## <span style="color: #4285F4"> Algoritm 2 - Next Ascent Hill-Climbing
1. Se selectează un punct aleator ***c*** (current hilltop) în spațiul de căutare.
```python
    def __generate_solution(self):
        solution = []
        for _ in range(len(self.__objects)):
            choice = random.choice([0, 1])
            solution.append(choice)
        return solution
```

2. Se consideră pe rând vecinii x ai punctului c. Dacă eval(x) este mai bun decât eval(c), atunci 
c=x și nu se mai evalueaza restul vecinilor lui c. Se continuă pasul 2 cu noul c și se consideră 
vecinii lui c mai departe (pornind din același punct din vecinătate unde s-a rămas cu vechiul 
c).
3.  Dacă nici un vecin x al punctului c nu duce la o evaluare mai bună, se salvează c și se continuă 
procesul de la pasul 1.
4. După un număr maxim de evaluări, se returnează cel mai bun c (hilltop).
<br>
 - Această funcție  primește o soluție dată sub formă de listă de valori binare și returnează o listă de soluții vecine. O soluție vecină este obținută prin invertirea valorii unei singure componente din soluția dată.
```python
    @staticmethod
    def __generate_neighbours(solution):
        neighbours = []
        for i in range(len(solution)):
            solution_copy = copy.deepcopy(solution)
            solution_copy[i] = 1 - solution_copy[i]
            neighbours.append(solution_copy)
        return neighbours
```

<br>
<br>
<br>

- Verificare soluție validă
```python
    def __evaluate_solution(self, solution):
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

- Această funcție este utilizată pentru a executa un algoritm de căutare locală, care explorează vecinătatea unei soluții pentru a găsi o îmbunătățire locală a acesteia. Se parcurge un număr specific de iterații și pentru fiecare iterație, se explorează vecinătatea soluției curente pentru a găsi o îmbunătățire locală. Dacă o îmbunătățire este găsită, soluția curentă este actualizată. În caz contrar, dacă nu s-a găsit nicio îmbunătățire după un anumit număr de vecini explorați, se generează o nouă soluție aleatoare pentru a evita blocarea într-un minim local. La final, calitatea celei mai bune soluții găsite este returnată
```python
 def execute_search(self, iterations):
        solution = self.__generate_solution()
        solution_quality = self.__evaluate_solution(solution)

        number_of_neighbours = 0

        for i in range(iterations):
            neighbours = self.__generate_neighbours(solution)

            found = False
            for neighbour in neighbours:
                number_of_neighbours += 1
                neighbour_quality = self.__evaluate_solution(neighbour)

                if neighbour_quality > solution_quality:
                    solution = neighbour
                    solution_quality = neighbour_quality
                    found = True
                    break

                if number_of_neighbours % 20 == 0 and found is False:
                    solution = self.__generate_solution()
                    solution_quality = self.__evaluate_solution(solution)

        self.__best_quality = solution_quality

        return self.__best_quality
```

## <span style="color: #4285F4"> Tabele de date - Căutare locală

| Instanța problemei | K   | Valoare medie | Valoarea cea mai bună | Număr execuții | Timpul mediu de execuție |
|--------------------|-----|---------------|-----------------------|--------------|--------------------------|
| Inst 1             | 50  | 705.4         | 706                   | 10           | 0.0010155201             |
|                    | 60  | 684           | 713                   |              | 0.0009009361             |
|                    | 70  | 737.2         | 760                   |              | 0.0015096188             |
|                    | 80  | 722           | 722                   |              | 0.0013674021             |
|                    | 90  | 679           | 721                   |              | 0.0023579836             |
| Inst 2             | 1000 | 96607.5       | 96682                 |              | 0.0648837328             |
|                    | 2000 | 97210.4       | 97418                 |              | 0.1308402061             |
|                    | 3000 | 97063.9       | 97155                 |              | 0.1939115524             |
|                    | 4000 | 96986.3       | 97084                 |              | 0.2655649662             |
|                    | 5000 | 97013.2       | 97119                 |              | 0.3398393631             |
| Inst 3             | 500 | 4390          | 4530                  |              | 0.0255804777             |
|                    | 600 | 4382.5        | 4405                  |              | 0.0312350988             |
|                    | 700 | 4036          | 4400                  |              | 0.0389187813             |
|                    | 800 | 4344.5        | 4445                  |              | 0.0365618467             |
|                    | 900 | 4467          | 4530                  |              | 0.0461193323             |

## <span style="color: #4285F4"> Tabele de date - Next Ascent Hill-Climbing

| Instanța problemei | K    | p  | Valoare medie | Valoarea cea mai bună | Număr execuții | Timpul mediu de execuție |
|--------------------|------|----|-------------|-----------------------|--------------|--------------------------|
| Inst 1             | 50   | 5  | 502.4       | 639                   | 10           | 0.0077063084             |
|                    | 60   | 6  | 552.2       | 636                   |              | 0.0090888023             |
|                    | 70   | 7  | 556.8       | 642                   |              | 0.0099637032             |
|                    | 80   | 8  | 558.6       | 626                   |              | 0.0109998226             |
|                    | 90   | 9  | 586.9       | 639                   |              | 0.0109998226             |
| Inst 2             | 1000 | 90 | 95241.7     | 96407                 |              | 7.5760958672             |
|                    | 2000 | 80 | 94837.9     | 96046                 |              | 14.8700391769            |
|                    | 3000 | 70 | 95041.8     | 95796                 |              | 20.2221370697            |
|                    | 4000 | 60 | 94974.5     | 95684                 |              | 26.6307811975            |
|                    | 5000 | 50 | 94859.1     | 96426                 |              | 32.88627491              |
| Inst 3             | 500  | 10 | 3835        | 4355                  |              | 0.8518435478             |
|                    | 600  |    | 3884        | 4160                  |              | 1.0058594227             |
|                    | 700  |    | 3879.5      | 4315                  |              | 1.1400835037             |
|                    | 800  |    | 3884        | 4365                  |              | 1.3823083878             |
|                    | 900  |    | 3897.5      | 4215                  |              | 1.5341095924             |

## <span style="color: #4285F4"> Observații
### Tabele de date - Căutare locală
1. #### Instanța problemei Inst 1:
    - Pentru valorile de K între 50 și 90, se observă o variație în valorile medii, cu cea mai bună valoare situată între 706 și 721.
    - Timpul mediu de execuție crește oarecum proporțional cu creșterea lui K.

2. #### Instanța problemei Inst 2:
    - Cu cât K este mai mare, cu atât valorile medii și cele mai bune par a fi mai mari, iar timpul de execuție crește semnificativ odată cu creșterea lui K.

3. #### Instanța problemei Inst 3:
   - Valorile medii și cele mai bune pentru Inst 3 sunt mai mici decât cele pentru Inst 1 și Inst 2.
   - Timpul de execuție este mai mic pentru Inst 3 comparativ cu celelalte instanțe, dar este în continuare influențat de K.

<br>
<br>

### Tabele de date - Next Ascent Hill-Climbing
1. #### Instanța problemei Inst 1:
    - Valorile medii și cele mai bune sunt mai mici decât cele din tabela anterioară, dar timpul de execuție este mai mare.
    - Timpul de execuție crește odată cu creșterea lui K.

2. ##### Instanța problemei Inst 2:
    - Similar cu Inst 1, valorile medii și cele mai bune sunt mai mici decât în tabela anterioară, dar timpul de execuție este mai mare și crește odată cu creșterea lui K.

3. #### Instanța problemei Inst 3:
    - Valorile medii și cele mai bune sunt mai mici decât cele pentru Inst 1 și Inst 2.
    - Timpul de execuție este mai mare decât pentru Instanța 1 și Instanța 2 și crește odată cu creșterea lui K.

În general, se poate observa că pentru ambele metode de căutare, valorile medii și cele mai bune sunt influențate de K, iar timpul de execuție crește odată cu creșterea lui K. De asemenea, metoda Next Ascent Hill-Climbing pare să aibă timp de execuție mai mare comparativ cu metoda de căutare locală pentru aceleași valori ale lui K.

## <span style="color: #4285F4"> Concluzie
<p>În cadrul analizei algoritmilor pentru rezolvarea problemei rucsacului, s-au evidențiat două abordări distincte: căutarea aleatoare și Next Ascent Hill-Climbing. Ambele algoritmi vizează obținerea unei soluții optime sau apropiate de optim pentru problema dată, însă adoptă strategii diferite pentru atingerea acestui scop.</p>
<p>Căutarea aleatoare explorează spațiul soluțiilor prin generarea aleatoare a acestora și evaluarea lor, selectând ulterior cea mai bună soluție găsită. Este o metodă simplă și intuitivă, cu o implementare directă și ușor de înțeles.</p>
<p>Pe de altă parte, algoritmul Next Ascent Hill-Climbing își îndreaptă eforturile către localizarea unui maxim local în spațiul soluțiilor. Acesta explorează vecinătatea soluției curente și se deplasează către soluții vecine care îmbunătățesc calitatea soluției, până când nu mai există nicio îmbunătățire posibilă.</p>
<p>Comparând cele două metode, se observă că căutarea aleatoare este mai simplă și poate fi eficientă pentru probleme mai simple sau când nu este necesară o soluție foarte precisă. Pe de altă parte, Next Ascent Hill-Climbing poate fi utilă pentru probleme mai complexe și pentru situațiile în care se dorește obținerea unui maxim local.</p>
<p>În final, alegerea între aceste două algoritmi depinde de natura specifică a problemei și de cerințele exacte ale acesteia, precum și de considerentele legate de performanță și eficiență. Ambele metode pot fi utile în diverse contexte și pot fi adaptate și îmbunătățite pentru a se potrivi mai bine nevoilor individuale ale utilizatorului.</p>

## <span style="color: #4285F4"> Datele obținute după rulări
- ### Căutare aleatoare - input: rucsac-20.txt

```python
[703, 703, 706, 706, 706, 706, 706, 706, 706, 706]
[0.0010013580322265625, 0.0009675025939941406, 0.0009965896606445312, 0.0, 0.0011606216430664062, 
 0.00099945068359375, 0.0020148754119873047, 0.001012563705444336, 0.0010004043579101562,
 0.0010018348693847656]

[631, 642, 642, 702, 702, 702, 702, 702, 702, 713]
[0.0, 0.0016145706176757812, 0.0009980201721191406, 0.0, 0.0010037422180175781, 
 0.0009980201721191406, 0.003408670425415039, 0.0, 0.0, 0.000986337661743164]

[635, 657, 760, 760, 760, 760, 760, 760, 760, 760]
[0.001005411148071289, 0.000982046127319336, 0.00099945068359375, 0.005530357360839844, 
 0.0010628700256347656, 0.000997781753540039, 0.0010030269622802734, 0.0010080337524414062, 
 0.0010023117065429688, 0.0015048980712890625]

[722, 722, 722, 722, 722, 722, 722, 722, 722, 722]
[0.0009160041809082031, 0.002234935760498047, 0.0010018348693847656, 0.0019991397857666016,
 0.001993894577026367, 0.0015065670013427734, 0.0010542869567871094, 0.0009648799896240234, 
 0.001003265380859375, 0.0009992122650146484]

[600, 616, 616, 632, 721, 721, 721, 721, 721, 721]
[0.0019979476928710938, 0.00099945068359375, 0.0065195560455322266, 0.0009965896606445312, 
 0.0010085105895996094, 0.0009996891021728516, 0.000946044921875, 0.0010073184967041016, 
 0.000997781753540039, 0.00810694694519043]
```

- ### Căutare aleatoare - input: rucsac-200.txt

```python
[96365, 96404, 96657, 96657, 96657, 96657, 96657, 96657, 96682, 96682]
[0.06941747665405273, 0.06206226348876953, 0.06226706504821777, 0.06368184089660645, 
 0.07608294486999512, 0.06271815299987793, 0.06354355812072754, 0.061554908752441406, 
0.0628669261932373, 0.06464219093322754]

[96539, 97019, 97019, 97019, 97418, 97418, 97418, 97418, 97418, 97418]
[0.1289680004119873, 0.1298816204071045, 0.12747406959533691, 0.13235807418823242, 
 0.12903547286987305, 0.1423037052154541, 0.12675809860229492, 0.12890934944152832, 
 0.13282465934753418, 0.12988901138305664]

[96785, 96785, 96984, 97155, 97155, 97155, 97155, 97155, 97155, 97155]
[0.19243955612182617, 0.1965465545654297, 0.188720703125, 0.1965794563293457, 
 0.18993020057678223, 0.196549654006958, 0.19482827186584473, 0.1931755542755127, 
 0.19063377380371094, 0.19971179962158203]

[96413, 96931, 96931, 97084, 97084, 97084, 97084, 97084, 97084, 97084]
[0.2588615417480469, 0.28011035919189453, 0.26353883743286133, 0.26602888107299805, 
 0.2654561996459961, 0.2749521732330322, 0.26419925689697266, 0.2695503234863281, 
 0.2619004249572754, 0.251051664352417]

[96845, 96935, 96935, 97035, 97035, 97035, 97035, 97039, 97119, 97119]
[0.3437051773071289, 0.32431578636169434, 0.33649277687072754, 0.35177111625671387, 
 0.349562406539917, 0.35671210289001465, 0.33809590339660645, 0.3387725353240967, 
 0.328080415725708, 0.3308854103088379]
```

- ### Căutare aleatoare - input: data.txt

```python
[4125, 4240, 4265, 4270, 4440, 4440, 4530, 4530, 4530, 4530]
[0.02546405792236328, 0.02626657485961914, 0.031476497650146484, 0.025333166122436523, 
 0.025472402572631836, 0.025538921356201172, 0.02303600311279297, 0.022248268127441406, 
 0.02435302734375, 0.02661585807800293]

[4330, 4330, 4330, 4405, 4405, 4405, 4405, 4405, 4405, 4405]
[0.03577542304992676, 0.02912116050720215, 0.03090667724609375, 0.03403973579406738, 
 0.0300905704498291, 0.03153705596923828, 0.02973151206970215, 0.03151369094848633, 
 0.030251741409301758, 0.029383420944213867]

[4120, 4250, 4250, 4250, 4250, 4380, 4380, 4380, 4400, 4400]
[0.03157997131347656, 0.0500030517578125, 0.043404340744018555, 0.045593976974487305, 
 0.04073023796081543, 0.03512716293334961, 0.03391718864440918, 0.03607797622680664, 
 0.03379559516906738, 0.03895831108093262]

[4315, 4315, 4315, 4315, 4315, 4330, 4330, 4330, 4435, 4445]
[0.0379948616027832, 0.04153585433959961, 0.037804603576660156, 0.041341543197631836, 
 0.041124820709228516, 0.042504072189331055, 0.03879356384277344, 0.0, 0.041699886322021484, 
 0.04281926155090332]

[4275, 4285, 4465, 4465, 4530, 4530, 4530, 4530, 4530, 4530]
[0.04569840431213379, 0.05823826789855957, 0.04715275764465332, 0.04313516616821289, 
 0.04519510269165039, 0.043764352798461914, 0.04632401466369629, 0.043291568756103516, 
 0.04425811767578125, 0.04413557052612305]
```

- ### Căutare locală - Next Ascent Hill-Climbing - input: rucsac-20.txt

```python
[491, 485, 525, 439, 549, 639, 393, 613, 504, 386]
[0.006725788116455078, 0.008872032165527344, 0.005697965621948242, 0.008628606796264648, 
 0.007592201232910156, 0.008915185928344727, 0.0060079097747802734, 0.00917363166809082, 
 0.007523059844970703, 0.007926702499389648]

[487, 632, 479, 636, 505, 454, 543, 533, 625, 628]
[0.00951242446899414, 0.009765625, 0.008629560470581055, 0.008363962173461914, 
 0.00957036018371582, 0.009275674819946289, 0.008621692657470703, 0.008829355239868164, 
 0.009556770324707031, 0.008762598037719727]

[536, 577, 575, 540, 536, 575, 485, 470, 632, 642]
[0.010504484176635742, 0.010841608047485352, 0.010099411010742188, 0.008754730224609375, 
 0.008405447006225586, 0.010506868362426758, 0.007837533950805664, 0.010935783386230469, 
 0.011312007904052734, 0.010439157485961914]

[540, 596, 571, 591, 501, 541, 551, 626, 483, 586]
[0.008661508560180664, 0.011237382888793945, 0.010885000228881836, 0.01229715347290039, 
 0.01303410530090332, 0.011409997940063477, 0.011669158935546875, 0.009610176086425781, 
 0.009685039520263672, 0.011508703231811523]

[616, 524, 639, 614, 627, 566, 563, 535, 597, 588]
[0.013687849044799805, 0.01235818862915039, 0.011694908142089844, 0.011635065078735352, 
 0.014309883117675781, 0.013084888458251953, 0.008727550506591797, 0.012824296951293945, 
 0.013640642166137695, 0.013966798782348633]
```

- ### Căutare locală - Next Ascent Hill-Climbing - input: rucsac-200.txt

```python
[94327, 94701, 96407, 95184, 94836, 95678, 95419, 95537, 95345, 94983]
[7.583603143692017, 7.492041110992432, 7.521956205368042, 7.556069612503052, 7.565741300582886, 
 7.567385196685791, 7.700906991958618, 7.565669298171997, 7.612159252166748, 7.595426559448242]

[94396, 94061, 94746, 95483, 95330, 95148, 95189, 93141, 96046, 94839]
[14.765504837036133, 14.84268569946289, 14.870755910873413, 14.862594842910767, 15.123399019241333, 
 14.824321031570435, 14.911580085754395, 14.845507621765137, 14.78399395942688, 14.870048761367798]

[94292, 95418, 95295, 95028, 95796, 94779, 95141, 95452, 94912, 94305]
[19.53816795349121, 19.610151052474976, 19.3837993144989, 20.083648204803467, 20.895093202590942, 
 20.112459182739258, 22.17279839515686, 19.599242210388184, 21.30254602432251, 19.523465156555176]

[95459, 95187, 94068, 94396, 95684, 95046, 94324, 95400, 95653, 94528]
[25.36744713783264, 28.32005262374878, 25.824613094329834, 26.541137218475342, 25.996625423431396, 
 27.466912746429443, 27.47807216644287, 25.69524621963501, 27.62353801727295, 25.99416732788086]

[93994, 93578, 96136, 95666, 94770, 94114, 94863, 96426, 95402, 93642]
[32.54341506958008, 31.946589946746826, 33.51964020729065, 32.32368016242981, 31.932111024856567, 
 33.967756509780884, 34.325979709625244, 34.39712858200073, 32.0243124961853, 31.88213539123535]
```

- ### Căutare locală - Next Ascent Hill-Climbing - input: data.txt

```python
[4355, 3960, 3705, 3510, 3715, 3955, 3720, 3815, 3680, 3935]
[0.8988058567047119, 0.8727450370788574, 0.912905216217041, 0.9012467861175537, 0.8403606414794922, 
 0.813143253326416, 0.8161330223083496, 0.8202989101409912, 0.8236205577850342, 0.819176197052002]

[3900, 3905, 3705, 3835, 3870, 3980, 3850, 3830, 3805, 4160]
[0.9844675064086914, 0.9970920085906982, 1.037736415863037, 1.0430777072906494, 0.998741865158081, 
 0.9873723983764648, 1.0298571586608887, 1.0219275951385498, 0.9751632213592529, 0.9831583499908447]

[4315, 3860, 3695, 3830, 3800, 3835, 3740, 3960, 4075, 3685]
[1.1337945461273193, 1.1441617012023926, 1.151052713394165, 1.1870055198669434, 1.1375067234039307, 
 1.122297763824463, 1.1348519325256348, 1.1378231048583984, 1.1257195472717285, 1.1266214847564697]

[3665, 4035, 4095, 4365, 3900, 3610, 3860, 3755, 3825, 3730]
[1.422633171081543, 1.4210340976715088, 1.38832426071167, 1.3527851104736328, 1.3384931087493896, 
 1.387444019317627, 1.3269000053405762, 1.3916919231414795, 1.3780834674835205, 1.4156947135925293]

[3930, 3880, 3890, 3935, 4215, 3600, 4170, 3705, 3730, 3920]
[1.585845708847046, 1.6206226348876953, 1.4615023136138916, 1.5221459865570068, 1.4667320251464844, 
 1.497502088546753, 1.4660394191741943, 1.570694923400879, 1.5192487239837646, 1.6307621002197266]
```
