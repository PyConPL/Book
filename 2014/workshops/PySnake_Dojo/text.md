#PySnake Dojo - Kuba Wasielak, Grzegorz Nosek 

Zadaniem uczestników jest napisanie programu, który pokieruje wężem w zaproponowanej przez nas grze przypominającej tradycyjnego snake'a, lecz z dwoma wężami na planszy. Zadaniem węża, oprócz tradycyjnego zjadania kropek, będzie doprowadzenie do takiej sytuacji, w której wąż przeciwnika uderzy w ścianę albo w ogon któregokolwiek z węży. Początkowym zadaniem uczestników będzie stworzenie takich algorytmów poruszania wężami, w których uda im się pokonać przygotowanych przez organizatorów przeciwników. Później natomiast, wszyscy uczestnicy wezmą udział w wielkim turnieju, gdzie ich węże zmierzą się ze sobą parami, aby wyłonić najsilniejszego spośród nich.

Jako wstęp do warsztatów zapoznamy uczestników z podstawami algorytmów wyszukiwania ścieżek z wyróżnieniem algorytmu A*.

Algorytm A* operuje na grafie węzłów, w którym każdy posiada określoną wartość heurystyki, a dodatkowo posiadamy dwa wyróżnione węzły - węzeł początkowy i końcowy. Heurystyka oznacza szacunkową wartość pomiędzy danym węzłem, a naszym wyznaczonym celem. Dla przykładu, stosując algorytm A* w wyszukiwaniu optymalnej trasy pomiędzy dwoma rzeczywistymi mapami heurystyką dla każdego miasta jest geograficzna odległość pomiędzy nim samym, a celem. Tak więc odległość heurystyki dla Gdyni, podczas gdy chcemy się dostać do Sztokholmu wynosi 536 km. Heurystyka jednak nie uwzględnia faktu, że auto nie pojedzie przez Bałtyk i prawdziwa odległość może być znacznie większa.

W przypadku snake, zarówno graf jak i heurystyka zostają zredukowane do płaszczyzny punktów, z których każdy posiada odpowiednik liczbowy na osi x i osi y. Gdyby zlikwidować własny ogon i całego węża przeciwnika, algorytm znajdywania jedzenia można by sprowadzić do:

```python
	if your.x < food.x:
		go_up()
	elif your.x > food.x:
		go_down()
	elif your.y < food.y:
		go_right()
	elif your.y > food.y:
		go_left()
	else:
		munch_munch()
```

Jednak nasz graf posiada przeszkody, miejsca zabronione i niedostępne. Wracając więc do algorytmu A* : dla każdego punktu nasz wąż ma co najwyżej trzy możliwe punkty wyboru drogi. Jeżeli liczba możliwości wynosi 0, zwiastuje to szybki koniec węża. Początkiem startowym jest głowa, natomiast końcowym jedzenie. Dla każdego punktu planszy można w bardzo prosty sposób obliczyć heurystykę, a najlepiej w przestrzeni dwuwymiarowej sprawdzi się do tego twierdzenie Pitagorasa. Znając odległości punktu i jedzenia na obu osiach, x i y nie jest problemem obliczenie odległości pomiędzy tymi dwoma węzłami. Jeżeli więc jedzenie znajduje się w punkcie (22, 36), wartość heurystyki dla punktu (10, 12) będzie wynosić pierwiastek z (22-10 + 36-12), czyli 6. Sposób liczenia heurystyki jest umowny - ważne, aby był stały dla każdego punktu. Czyli zamiast faktycznej odległości liczonej za pomocą twierdzenia Pitagorasa, równie dobrze możemy liczyć sumę odległości liczonej po obu osiach, która dla powyższego przykładu będzie wynosić 36.

Tak więc zaczynając od głowy węża, dla każdego z osiągalnych punktów liczymy odległość potrzebną do pokonania tego dystansu powiększoną o wartość heurystyki danego punktu. Spośród wszystkich punktów znajdujemy ten, dla którego obliczony koszt jest najniższy. Następnie do listy osiągalnych punktów dodajemy wszystkie punkty, które są osiągalne z tego właśnie dodanego. Wracając do powyższego przykładu, w którym głowa znajduje się w punkcie (10, 12), a jedzenie w punkcie (22, 36):
 1. Osiągalne punkty wraz z odległościami od głowy węża g():
 - A (11, 12) i g(A) = 1
 - B (10, 11) i g(B) = 1
 - C (9, 12) i g(C) = 1
 są to tylko 3 punkty, ponieważ wąż oprócz głowy ma ogon i nie może zawrócić w miejscu.
 2. Dla każdego z punktów wartość heurystyki wynosi:
 - h(A) = 5.92
 - h(B) = 6.08
 - h(C) = 6.08
3. Wybrany zostaje punkt A, dla którego suma odległości i heurystyki wynosi 6.92, jednocześnie otwierając drogę na nowe punkty:
- D (11, 13) i g(D) = 2
- E (12, 12) i g(E) = 2
- F (11, 11) i g(F) = 2
4. Spośród wszystkich dostępnych punktów suma g() i h() wynosi:
- g(A) + h(A) = 7.08
- g(B) + h(B) = 7.08
- g(D) + h(D) = 7.83
- g(E) + h(E) = 7.83
- g(F) + h(F) = 8

Wybieramy więc dowolny z punktów A lub B oraz szukamy ich sąsiedztwa wraz z nową odległością potrzebną do dotarcia do tego punktu wynoszącą 3. Jeżeli jeden z nowych punktów znajduje się już w liście osiągalnych punktów, możemy go zignorować, ponieważ oznaczałoby to, że nasz wąż zacząłby robić pętlę. Kontynuujemy algorytm tak długo, aż jednym z punktów osiągalnych będzie cel. Wtedy znamy już trasę dla naszego węża.

W naszej grze jednak planszą są same węże, więc ulega ona zmianie podczas każdej tury. Pozostawia to pole do popisu dla uczestników przy programowaniu. Można postawić kilka pytań, np. jak powinien się zachować nasz wąż w sytuacji, gdy jest całkowicie odgrodzony od pożywienia? Albo czy można napisać algorytm, który zamiast poszukiwać jedzenia będzie starał się przeciąć drogę przeciwnikowi albo uwięzić go na zamkniętym obszarze planszy.

Same warsztaty będą podzielone na trzy części:

1.  Powitanie, wstęp teoretyczny, wybranie zespołów (ok. 30 minut)
2.  Pracę nad własnym algorytmem (ok. 2 godziny).
3.  Rozgrywki oraz wyłonienie zwycięzcy (ok. 30 minut)

<!-- Przeczytane: Piotr Kasprzyk -->
