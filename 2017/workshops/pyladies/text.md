# Rozdział 1. Tryb interaktywny

Warsztaty zaczniemy od wyjaśnienia w jaki sposób będziemy programowali
w Pythonie.

## Zaczynamy!

Otwórz [ten link](https://repl.it/languages/python3) w osobnej karcie
przeglądarki.

Jeżeli zobaczysz okienko z prośbą o założenie konta, zamknij je klikając
w "x".

Strona którą widzisz jest podzielona na dwie części:

* z lewej strony, na białym tle, jest **edytor** tekstu,
* z prawej strony widać **tryb interaktywny**.

Edytor pozwala stworzyć cały kod programu, a następnie uruchomić go przez
wciśnięcie przycisku "play" (lub kombinacją klawiszy Ctrl + Enter).
Jeżeli program wypisze jakiś tekst, to zobaczymy go w oknie trybu
interaktywnego.

Tryb interaktywny działa zupełnie inaczej: czeka na wpisanie polecenia,
a gdy wciśniesz Enter, wykonuje je i wypisuje jego wynik.  W ten sposób
możesz programować i od razu oglądać rezultaty.

Praca z trybem interaktywnym jest wygodna, kiedy chcesz przetestować
działanie pojedynczej operacji lub kiedy nie masz pewności jakie operacje
chcesz wykonać.  Jeżeli już wiesz jaki program chcesz napisać, wtedy
łatwiej jest skorzystać z edytora.

Jest jeszcze jedna ważna różnica między trybem interaktywnym a edytorem:
tryb interaktywny po wykonaniu operacji zawsze wypisze jej wynik.  Edytor
zrobi to tylko jeżeli mu wydamy takie polecenie (poprzez instrukcję
`print`, o której opowiemy później).

Póki co będziemy korzystali z **trybu interaktywnego**, ponieważ będziemy
uczyli się pojedynczych instrukcji i oglądali ich rezultaty.  Nie bój się
eksperymentować z różnymi wariantami tych poleceń, w najgorszym wypadku
Python poinformuje Cię, że wpisanego kodu nie można wykonać.

## Znak zachęty

W przykładach kodu, które znajdziesz w kolejnych rozdziałach, wielokrotnie
zobaczysz ciąg znaków `>>>`.  Jest to **znak zachęty**.  Używamy go aby
odróżnić tekst, który należy wpisać w trybie interaktywnym od tekstu, który
interpreter Pythona sam wypisuje.  Jeżeli w jakiejś linijce przykładu
zobaczysz znak zachęty, to znaczy, że wszystko co następuje po znaku należy
wpisać w trybie interaktywnym, a następnie wcisnąć Enter.  Samego znaku
zachęty nie wpisujemy!

## :pushpin: Podsumowanie

W tym rozdziale:

* otworzyliśmy stronę `repl.it`, na której możemy programować w edytorze
lub **trybu interaktywnego** Pythona,
* dowiedzieliśmy się jak wygląda **znak zachęty** i że pokazuje nam kod,
który należy wpisać w trybie interaktywnym.

---

# Rozdział 2. Tekst

W tym rozdziale:

* dowiesz się czym jest `string` i co można z nim zrobić,
* nauczysz się pisać programy, które wyświetlają tekst.

## String

Niemal każdy program generuje jakiś tekst.  Aplikacje na smartfonach
pokazują komunikaty o odebranych wiadomościach.  Aplikacje webowe zwracają
treść stron internetowych.  Serwery zapisują na dysku informacje o tym jak
przebiega ich działanie.  Tekst to podstawa komunikacji między komputerem
a człowiekiem.  Właśnie dlatego naukę programowania zaczniemy od operacji
na tekście, lub, jak mówimy w żargonie programistycznym, na **stringach**.

String, czyli łańcuch znaków, to po prostu ciąg liter, cyfr, kropek,
przecinków etc. Żeby w Pythonie zdefiniować string, po prostu umieść jakiś
tekst między znakami `'` (pojedynczy apostrof):

```python
>>> 'PyLadies 2017'
```

W powyższym stringu znalazły się duże i małe litery, odstęp (spacja) oraz
cyfry.  Istnieją [tysiące znaków](https://pl.wikipedia.org/wiki/Unikod)
jakich możesz użyć.

:snake: Zanim przejdziesz dalej spróbuj samodzielnie utworzyć stringi
z następującymi informacjami: Twoje imię i nazwisko, nazwa miejscowości
z której pochodzisz, tytuł Twojego ulubionego filmu lub książki.


## Apostrofy

Przykład, którym posłużyliśmy się przed chwilą, pokazuje string ujęty
w pojedyncze apostrofy, czyli `'`.  Jeżeli chcesz, możesz używać znaku
`"`.  Dla Pythona nie ma to żadnego znaczenia.  Ważne jest natomiast,
aby z obu stron stringa znalazł się taki sam apostrof: jeżeli zaczynasz
podwójnym, musisz zakończyć podwójnym.  Tak samo z pojedynczym.


## Operacje na stringach

Teraz, kiedy już umiesz zdefiniować stringa, spróbujmy wykonać na nim
jakąś operację.  Przez "operację" rozumiemy przekształcenie jednego
stringa na inny string, na przykład:

```python
>>> 'Kubuś Puchatek'.lower()
'kubuś puchatek'
```

(Zwróć uwagę na brak spacji wokół kropki!)

W tym przykładzie wykonaliśmy dwie operacje: zdefiniowaliśmy stringa
`'Kubuś Puchatek'` oraz **wywołaliśmy metodę** `lower`.  Metoda to po
prostu operacja jaką można wykonać na jakimś obiekcie.  W tym przypadku
obiektem jest nasz string, a metoda powoduje stworzenie nowego stringa,
w którym wszystkie wielkie litery zostały zastąpione małymi.

String w Pythonie posiada wiele innych metod, na przykład:

* `upper` - przeciwieństwo `lower`,
* `title` - zamienia każdą pierwszą literę każdego wyrazu z małej na
wielką,
* `strip` - usuwa spacje z lewej i prawej strony stringa (jeżeli
istnieją).

:snake: Teraz wypróbuj te metody w taki sposób, żeby zobaczyć efekty ich
działania.  Przetestuj je na stringach, które tworzyliśmy w poprzednim
zadaniu.


## Do czego służą operacje na stringach?

Pisząc programy często musimy sobie radzić ze stringami, które pochodzą
ze źródeł na które nie mamy wpływu.  Na przykład informacje z formularza
wypełnionego przez użytkownika, albo dane odczytane z pliku.
We wszystkich tych przypadkach przetwarzamy stringi, o których strukturze
nic nie wiemy.  Operacje pomagają nam przekształcić stringi na jednolitego
formatu, albo wyszukać w nich jakieś informacje.

Dobrym przykładem jest imię i nazwisko.  Wyobraź sobie, że tworzysz
program, który pobiera od użytkownika jego imię i nazwisko.  Chcesz
zapisać te dane w formacie `Imię Nazwisko`, czyli tak, aby każde ze słów
zaczynało się wielką literą.  Problem polega na tym, że użytkownik może
wpisać `jan kowalski`, albo `JAN KOWALSKI`.  W obu przypadkach dostaniesz
stringi w innym formacie niż się spodziewasz.  Możesz sobie z tym poradzić
używając metody `title`, która obie te wartości zamieni na `Jan Kowalski`.


## Operacje z argumentami

Niektóre operacje wymagają podania dodatkowych opcji.  Na przykład:

```python
>>> 'Kubuś Puchatek'.find('Pu')
6
```

Metoda `find` wyszukuje w stringu podany łańcuch i zwraca numer znaku, w
którym ten łańcuch się zaczyna.  Zwróć uwagę, że znaki numerowane są od
zera:

```
K u b u ś   P u c h ...
0 1 2 3 4 5 6 7 8 9 ...
```

Wywołaliśmy metodę `find` podając jej stringa `'Pu'`.  Taki łańcuch
znajduje się wewnątrz stringa `'Kubuś Puchatek'` i zaczyna się od znaku
numer 6, dlatego tą liczbę zobaczyliśmy na ekranie.

Wartości, które musimy podać wywołując metodę (np. `'Pu'` z przykładu)
nazywamy **argumentami**.  Niektóre metody nie przyjmują żadnych
argumentów, ale są też takie, które wymagają podania jednego lub więcej.
Jeżeli metoda przyjmuje wiele argumentów, to muszą być oddzielone od
siebie przecinkami.


## `find`, `replace`, `count`

Nie będziemy teraz przechodzili przez wszystkie metody jakie posiada
string, ale trzy z nich warto poznać już na samym początku.

### `find`

`find` jako argument przyjmuje string i szuka go w stringu na jakim
wywołaliśmy operację.  Jeżeli łańcuch zostanie znaleziony, otrzymujemy
numer znaku od którego się zaczyna.  W przeciwnym wypadku dostaniemy `-1`.

Ta metoda jest przydatna na przykład kiedy szukamy jakieś frazy i chcemy
się przekonać czy dany string ją zawiera.

```python
>>> 'Anna Nowak'.find('Nowak')
5
>>> 'Jan Kowalski'.find('Nowak')
-1
>>> 'Tomasz Nowak'.find('Nowak')
7
```

Zwróć uwagę, że wielkość liter ma znaczenie:

```python
>>> 'Prosiaczek'.find('Pro')
0
>>> 'Prosiaczek'.find('pro')
-1
>>> 'prosiaczek'.find('Pro')
-1
```

### `replace`

`replace` przyjmuje dwa argumenty: stringi `a` i `b`.  Kiedy wywołamy tę
metodę na stringu, to wszystkie wystąpienia łacucha `a` zostaną zastąpione
łańcuchem `b`.

Przykładowo, możesz zastąpić wszystkie spacje znakiem `-`:

```python
>>> 'Ala ma kota'.replace(' ', '-')
'Ala-ma-kota'
```

Albo zastąpić całe wyrazy:

```python
>>> 'Ala ma kota'.replace('kota', 'psa')
'Ala ma psa'
```

Innym przykładem użycia tej metody jest usunięcie ze stringa jakiegoś
znaku.  Możesz to zrobić podając pusty string jako drugi argument:

```python
>>> 'Jan Kowalski'.replace('Kowalski', '')
'Jan '
```
### `count`

`count` przyjmuje jeden string jako argument i zwraca liczbę wystąpień
tego łańcucha w stringu na jakim wykonaliśmy operację.

Metoda ta przydaje się, kiedy na przykład chcemy sprawdzić czy jakaś
fraza powtarza się więcej niż raz w danym stringu:

```python
>>> 'Ala ma kota'.count('ma')
1
>>> 'Ala ma kota, a Ola ma psa'.count('ma')
2
```

:snake: Zdefiniuj kilka stringów i na każdym z nich wywołaj każdą z
powyższych metod.  Upewnij się, że rozumiesz jak działają, a w razie
wątpliwości poproś o pomoc mentora.


## Długość stringa, funkcja `len`

Jedną z najbardziej przydatnych operacji jaką możemy wykonać na stringu
jest sprawdzenie jego długości.  Na przykład chcemy sprawdzić czy nie
jest zbyt długi, albo chcemy sprawdzić który z dwóch stringów jest
dłuższy.  Tutaj z pomocą przychodzi funkcja `len`:

```python
>>> len('Kubuś Puchatek')
14
```

Zwróć uwagę, że `len` nie jest metodą, czyli nie stosujemy notacji
`obiekt.metoda()`.  Dzieje się tak, ponieważ sprawdzenie długości
jakiegoś obiektu (w tym przypadku: stringa) jest na tyle popularną
operacją, że w Pythonie stworzono osobną funkcję która ją wykonuje.

:snake: Sprawdź długość Twojego imienia i nazwiska. Zobacz jaką długość
ma pusty string, czyli `''`.


## :pushpin: Podsumowanie

W tym rozdziale:

* dowiedzieliśmy się czym jest string,
* poznaliśmy znaczenie słów **metoda** oraz **argument**,
* nauczyliśmy się najważniejszych metod jakie można wywołać na stringu,
* poznaliśmy funkcję `len`, która zwraca długość stringa.

---

# Rozdział 3. Funkcja `help`

W tym rozdziale:

* poznasz funkcję `help`.


## Pomoc w Pythonie

Nawet najlepszy programista nigdy nie zapamięta wszystkich funkcji i metod
jakie oferuje Python.  W trakcie tego szkolenia poznasz ich wiele, ale
za kilka dni zapomnisz jak działają.  Nie przejmuj się, twórcy Pythona
pomyśleli o tym...


## Dokumentacja metod w Pythonie

Każda metoda zdefiniowana w Pythonie posiada **dokumentację**, która
w kilku słowach opisuje jej działanie.  Aby przeczytać tę dokumentację,
należy wywołać funkcję `help`, na przykład:

```python
>>> help('jakiś string'.find)
Help on built-in function find:

find(...)
    S.find(sub [,start [,end]]) -> int

    Return the lowest index in S where substring sub is found,
    such that sub is contained within S[start:end].  Optional
    arguments start and end are interpreted as in slice notation.

    Return -1 on failure.
```

Dokumentacja pokazuje wszystkie argumenty jakie przyjmuje dana metoda,
informuje jakiego typu wynik jest zwracany oraz w skrócie wyjaśnia co
ta metoda robi.  Dzięki temu możemy ją sobie bardzo szybko przypomnieć.

Zwróć uwagę, że w tym przykładzie nie otworzyliśmy nawiasu przy nazwie
metody `find`, a co za tym idzie, nie podaliśmy jej żadnych argumentów.
W ten sposób zamiast wywołać tę metodę, po prostu posłużyliśmy się jej
nazwą.  Kiedy przekażemy taką nazwę do funkcji `help`, Python pokaże nam
dokumentację danej metody.

:snake: Użyj funkcji `help` i przeczytaj dokumentację do metod `replace`
i `count` oraz do funkcji `len`.


## :pushpin: Podsumowanie

W tym rozdziale:

* poznaliśmy funkcję `help` i dowiedzieliśmy się, że warto jej używać
wtedy, kiedy nie rozumiemy jakiejś metody lub nie pamiętamy jak działa.


---

# Rozdział 4. Liczby

W tym rozdziale:

* dowiesz się czym jest *integer* oraz *float*,
* nauczysz się wykonywać operacje arytmetyczne na liczbach.

## Liczby całkowite

Aby zdefiniować liczbę całkowitą (**integer**) po prostu wpisz ją nie wstawiając spacji
między cyfry:

```python
>>> 2017
2017
```

Liczby możemy dodawać i odejmować:

```python
>>> 20 + 17
37
>>> 2 + 0 + 1 + 7
10
>>> 20 - 17
3
>>> 20 - 1 - 7
12
```

...mnożyć i dzielić:

```python
>>> 20 * 17
340
>>> 20 / 17
1
```

...podnosić do potęgi:

```python
>>> 201 ** 7
13254776280841401
```

...albo sprawdzić resztę z dzielenia:

```python
>>> 20 % 17
3
```

Wszystkie te operacje możemy dowolnie łączyć:

```python
>>> 20 / 2 + 17 * 3
61
```

Jeżeli chcemy mieć większą kontrolę na kolejnością wykonywania działań, możemy
posłużyć się nawiasami okrągłymi:

```python
>>> (20 * (2 + 17)) / 3
126
```

:snake: Spróbuj samodzielnie wykonać kilka działań arytmetycznych.

## Liczby rzeczywiste

Wszystkie powyższe operacje możemy wykonywać również na liczbach rzeczywistych
(**float**, zmiennoprzecinkowych):

```python
>>> 2.5 * 2.0
5.0
>>> 7 / 2.0
3.5
>>> 6.7 + 0.3 - 2.5
4.5
>>> 1.0 / 3
0.3333333333333333
```

Zwróć uwagę, że wynik operacji będzie zawierał część dziesiętną, tylko jeżeli
przynajmniej jeden z argumentów jest liczbą rzeczywistą. W przeciwnym wypadku
część ułamkowa zostanie pominięta, a w rezultacie otrzymamy liczbę całkowitą:

```python
>>> 5 / 2
2
>>> 5 / 2.0
2.5
>>> 5.0 / 2
2.5
>>> 5.0 / 2.0
2.5
```

:snake: Czy wiesz kiedy Python zwróci *float* a kiedy *integer*? Upewnij się,
sprawdź różne kombinacje liczb i działań.

## Operatory i ich kolejność

Znaki, których używamy do wykonywania działań (`+`, `*` itd.) nazywamy **operatorami**.
Każdy operator ma swój priorytet, co oznacza, że jeżeli w jednym działaniu użytych
jest kilka różnych operatorów (np. `2 + 1 * 3`), to Python najpierw obliczy te, które
mają wyższy priorytet.

Przykładowo, w takim działaniu:

```python
>>> 4 + 10 * 6
```

najpierw zostanie wykonane mnożenie, a dopiero potem dodawanie, czyli rezultatem będzie `64`.

Poniższa tabelka prezentuje operatory oraz ich znaczenie. Kolejność wierszy odpowiada
priorytetowi, czyli na samej górze jest operator z najwyższym priorytetem, a na dole
z najniższym.

Operatory | Znaczenie
--------- | ---------
`+`, `-`  | Dodawanie, odejmowanie
`*`, `/`, `//`, `%` | Mnożenie, dzielenie, dzielenie całkowite, modulo
`**` | Potęgowanie

## :pushpin: Podsumowanie

W tym rozdziale:

* dowiedzieliśmy się jak definiować liczby całkowite (*integer*) i zmiennoprzecinkowe (*float*),
* poznaliśmy najważniejsze operatory matematyczne i ich priorytety.

---

# Rozdział 5. Błędy

W tym rozdziale:

* dowiesz się czym są **wyjątki**,
* nauczysz się czytać komunikaty o błędach.

## Wyjątki

Tworząc programy nigdy nie jesteśmy w stanie przewidzieć wszystkich
sytuacji jakie mogą się wydarzyć.  Czasami stanie się coś, czego się nie
spodziewaliśmy, a czasami po prostu użyjemy języka w nieprawidłowy sposób.
Na każdą taką sytuację Python zareaguje zgłaszając błąd.  Dzięki temu
dowiemy się na czym polegała nasza pomyłka i będziemy mogli poprawić kod
programu, żeby uniknąć tego samego problemu w przyszłości.

Słowa "błąd" czy "problem" są bardzo ogólne, ponieważ mogą dotyczyć rzeczy
na które jako programiści nie mamy wpływu.  Dlatego posługujemy są terminem
**wyjątek**.  Oznacza on sytuację, w której Python zatrzymał wykonywanie
programu, ponieważ napotkał *wyjątkową* sytuację, której sam nie potrafił
obsłużyć.  Mówi się, że program **rzucił wyjątek**.  Kiedy tak się stanie,
rolą programisty jest dostosowanie programu w taki sposób, aby
w przyszłości podobna sytuacja nie skutkowała zatrzymaniem.

Czym są wyjątkowe sytuacje o których wspomnieliśmy?  Może to być próba
wykonania operacji, której Python nie potrafi zrealizować, na przykład
dodanie liczby do tekstu.  Albo błąd "za mało miejsca na dysku twardym"
podczas zapisywania jakiegoś pliku.  Nie sposób wymienić wszystkie takie
możliwości - z czasem poznasz zestaw najczęściej występujących wyjątków
i nauczysz się przewidywać jakie operacje mogą skutkować rzuceniem wyjątku.

## Jak czytać wyjątki

Spróbujmy wywołać wyjątek, dodając tekst do liczby:

```python
>>> 123 + 'ala ma kota'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

Jak widzisz, zamiast zwrócić wynik operacji, Python zgłosił wyjątek.
Przeczytajmy go linijka po linijce.

* Na samym początku widzimy zawsze wiadomość
`Traceback (most recent call last):`.  Słowem "Traceback" określa się listę
operacji, których wykonanie spowodowało błąd.  W tym przypadku wykonana
została tylko jedna operacja (dodawanie), ale w przyszłości spotkasz się
z sytuacjami, w których wyjątek został rzucony w skutek wykonania całego
ciągu poleceń.  Python zawsze pokazuje cały traceback, aby programista
mógł zrozumieć co poszło nie tak.  Zdanie `most recent call last`
informuje, że ostatnia operacja na liście została wykonana najpóźniej
spośród wszystkich.
* `File "<stdin>", line 1, in <module>` to właśnie traceback. W naszym
przypadku jest to tylko jedna linijka.  Widzimy tutaj opis miejsca,
w którym wystąpił błąd: `File <stdin>`, co oznacza po prostu "standardowe
wejście" (*standard input*), jak określa się sposób wprowadzania informacji
do komputera z użyciem samego tekstu.  Oznacza to tyle, że błąd powstał
w trybie interaktywnym.
* Ostatnia linijka zawiera najważniejszą informację, czyli bezpośrednią
przyczynę błędu.  Zaczyna się od typu wyjątku.  W tym przypadku to
`TypeError`.  Typ można rozumieć jako kategorię: nie mówi on czego
dokładnie dotyczył błąd, ale pozwala zaklasyfikować różne wyjątki, aby
łatwiej byłe je zrozumieć.  `TypeError` oznacza niepoprawne użycie jakiegoś
typu, w tym przypadku typów *integer* i *string*.  Dalej widzimy szczegóły
błędu: operator dodawania został użyty na liczbie całkowitej (*integer*)
oraz łańcuchu znaków (*string*), co nie jest dozwolone.

Tworząc bardziej zaawansowane programy spotkasz się z jeszcze dłuższymi
komunikatami o błędach.  Nie zniechęcaj się tym: każdy wyjątek sprowadza
się do tylko jednej niepoprawnej operacji, a traceback, nieważne jak długi,
pomoże Ci zlokalizować przyczynę niepowodzenia.  Jeżeli mimo wszystko nie
będziesz w stanie zrozumieć dlaczego Twój program przestał działać, wklej
ostatnią linijkę komunikatu do wyszukiwarki internetowej.  Jest bardzo
możliwe, że ktoś już kiedyś spotkał się z takim problemem i znalazł
rozwiązanie.

:snake: Wywołaj błędy i przeczytaj ze zrozumieniem wyjątki spowodowane
następującymi operacjami: dzielenie przez zero; wywołanie na dowolnym
stringu metody, która nie istnieje; wykonanie kodu, który nie ma sensu
(możesz wpisać losowy ciąg znaków).

## :pushpin: Podsumowanie

W tym rozdziale:

* dowiedzieliśmy się czym jest wyjątek i jak czytać jego treść.

---

# Rozdział 6. Zmienne

W tym rozdziale:

* dowiesz się czym jest **zmienna**, jak ją zdefiniować i jak jej używać.


## Zmienna

W poprzednich rozdziałach wykonywaliśmy różne operacje: definiowaliśmy
stringi, mnożyliśmy liczby itd.  Każda z tych operacji zwracała jakiś
wynik, który od razu był wypisywany na ekran.  Tekst i liczby, które
w ten sposób tworzyliśmy, trafiały do pamięci komputera tylko na chwilę
i zaraz po wyświetleniu były z niej usuwane.  W związku z tym w kolejnych
operacjach nie mogliśmy wykorzystać wyników z operacji poprzednich.

Aby poradzić sobie z problemem przechowania wyniku operacji, używamy
**zmiennych**.  Zamiast tłumaczyć jak działają zmienne, najlepiej popatrzeć
na przykład:

```python
>>> x = 7
>>> x
7
>>> 5 + x
12
```

Przeanalizujmy co wydarzyło się w powyższym przykładzie.  Na początku
**zdefiniowaliśmy zmienną**, czyli przypisaliśmy wynik jakiejś operacji
do nazwy.  W tym przypadku operacją jest po prostu definicja liczby `7`,
natomiast nazwą jest `x`.  Od tego momentu mogliśmy używać **zmiennej**
`x` w kolejnych operacjach.  Jeżeli po prostu wpiszemy jej nazwę, wtedy
otrzymamy jej **wartość**.  Możemy też posłużyć się nią w innej operacji,
na przykład dodając ją do innej liczby.

Definiując zmienne możemy posługiwać się innymi zmiennymi:

```python
>>> a = 10
>>> b = 5
>>> c = a + b
>>> c
15
```

Oczywiście w realnym przypadku zmienne nazywamy w taki sposób, aby
mówiły nam co oznaczają:

```python
>>> cena_netto = 120
>>> podatek_vat = cena_netto * 0.23
>>> cena_brutto = cena_netto + podatek_vat
>>> cena_brutto
147.6
```


## Przypisanie

Operację `zmienna = wartość` nazywamy **przypisaniem**.  W wyniku
przypisania Python tworzy *zmienną*, która otrzymuje *wartość*.  Jeżeli
wartość jest operacją (np. dodawaniem), to najpierw jest obliczany jej
rezultat, a nawstępnie zostaje on przypisany do zmiennej.


## Nazwy zmiennych

Tworząc zmienną musimy najpierw wymyślić dla niej nazwę.  Przede wszystkim
powinna ona wprost mówić jakie jest znaczenie zmiennej.  Dzięki temu, tak
jak w powyższym przykładzie, będziemy mogli z łatwością zrozumieć kod
programu.

Poza tym Python narzuca ograniczenia na znaki, jakich możemy użyć w nazwie
zmiennej.  Dozwolone znaki to:

* litery od `a` do `z` (małe) oraz od `A` do `Z` (duże),
* cyfry,
* znak `_` (podkreślenie).

Wszystkie pozostałe znaki są niedozwolone. Co istotne, nazwa nie może
zaczynać się od cyfry!

:snake: Utwórz zmienne `imie` oraz `nazwisko`, przypisz do nich swoje imię
i nazwisko.  Następnie na ich podstawie utwórz zmienną `imie_nazwisko`,
która będzie zawierała imię i nazwisko oddzielone spacją.

:snake: Zobacz co się stanie, kiedy spróbujesz stworzyć zmienną, której
nazwa zaczyna się od cyfry.


## Zmiana wartości zmiennej

W każdej chwili możemy zmienić wartość zmiennej:

```python
>>> x = 'Ala ma kota'
>>> x
'ala ma kota'
>>> x = 'kot ma Alę'
>>> x
'kot ma Alę'
>>> x = x + '.'
>>> x
'kot ma Alę.'
```

## Zmienne i metody

W poprzednich rozdziałach wywoływaliśmy różne metody, np. `find` lub
`title`.  Zwróć uwagę, że metody, które możesz wykonać bezpośrednio
na obiekcie, możesz też wykonać na zmiennej:

```python
>>> imie_nazwisko = 'jan kowalski'
>>> imie_nazwisko
'jan kowalski'
>>> imie_nazwisko.title()
'Jan Kowalski'
>>> imie_nazwisko
'jan kowalski'
>>> imie_nazwisko = imie_nazwisko.title()
>>> imie_nazwisko
'Jan Kowalski'
```


## :pushpin: Podsumowanie

W tym rozdziale:

* dowiedzieliśmy się czym jest zmienna, jak ją definiować i jak jej używać.

---

# Rozdział 7. Funkcje

W tym rozdziale:

* nauczysz się definiować **funkcje**.


## Czym jest funkcja

Dotychczas dowiedzieliśmy się czym jest *string*, *integer* i *float*, oraz
jak używać zmiennych do przechowywania wartości pomiędzy operacjami.
Dzięki temu możemy napisać program, który wykona jakieś operacje na danych,
na przykład przetworzy tekst, lub coś obliczy, a następnie wypisze wynik
na ekran.  Im bardziej zaawansowane problemy będziemy chcieli rozwiązać
naszym programem, tym bardziej skomplikowany będzie jego kod.

Jednym ze sposobów na pisanie bardziej zrozumiałego kodu jest definiowanie
funkcji.  **Funkcja** to wydzielony zbiór instrukcji, który możemy
wielokrotnie wykonać w programie.  **Definicja funkcji** to sposób w jaki
opisujemy, które operacje mają być zawarte w funkcji.

Przykładowo, poniższa funkcja liczbę podniesioną do kwadratu:

```python
def kwadrat(liczba):
    wynik = liczba ** 2
    return wynik
```

Linijka zaczynająca się od słowa `def` to **nagłówek funkcji**.  Składa się
z następujących elementów:

* słowo `def`,
* **nazwa** funkcji (w tym przykładzie to `kwadrat`),
* **lista argumentów** ujęta w nawiasy okrągłe (tutaj mamy jeden argument
`liczba`, ale możemy ich podać wiele, oddzielając je przecinkami),
* dwukropek.

Zwróć uwagę na spacje! W całym nagłówku odstęp jest tylko między słowem
`def` a nazwą funkcji. Gdyby funkcja miała wiele argumentów oddzielonych
przecinkami, to moglibyśmy wstawić spacje obok przecinków, aby poprawić
czytelność kodu. Poza tymi dwoma przypadkami, w nagłówku nie powinno więcej
spacji.

W kolejnych linijkach po nagłówku mamy **ciało funkcji**.  Są to po prostu
instrukcje, które zostaną wykonane kiedy użyjemy funkcji.  W powyższym
przykładzie ciało zawiera dwie operacje: podniesienie do kwadratu wartości
zmiennej `liczba` i przypisanie jej do zmiennej `wynik`, oraz zwrócenie
wartości zmiennej `wynik`.  **Zwrócenie** to określenie jaka wartość ma
być wynikiem danej funkcji.  Służy do tego słowo `return`.  Jeżeli wpiszemy
po nim nazwę zmiennej, to jej wartość będzie wynikiem.  Możemy także
zwrócić rezultat nie przypisując do wcześniej do zmiennej:

```python
def kwadrat(liczba):
    return liczba ** 2
```


## Praca z edytorem

Zanim zdefiniujesz swoją pierwszą funkcję, zatrzymajmy się na chwilę.  Jak
dotąd wszystkie operacje wykonywaliśmy w trybie interaktywnym, gdzie
wpisywaliśmy kod, wciskaliśmy Enter i dostawaliśmy wynik.  Gdy zaczniemy
pracować z funkcjami takie podejście może okazać się uciążliwe.  Dużo
wygodniej będzie teraz przejść do **edytora**.

Od tej pory każdy przykład, który nie będzie zaczynał się od `>>>` należy
rozumieć jako kod wpisany w edytorze i uruchomiony przyciskiem "run".


## Definicja i wywołanie funkcji

Przepisz teraz do edytora kod funkcji zapisany poniżej.  Zwróć szczególną
uwagę na **wcięcia**.  Każda linijka ciała funkcji musi zaczynać się od
wcięcia.  Co istotne, wszystkie te wcięcia **muszę mieć taką samą
szerokość**.  Oznacza to, że jeżeli w pierwszej linijce zrobisz wcięcie
na dwie spacje, to wszystkie pozostałe linijki aż do końca funkcji też
muszą mieć wcięcie na dwie spacje.  Jak zauważysz, edytor sam zrobi
wcięcie kiedy po wpisaniu nagłówka wciśniesz Enter.  Jeżeli by tego nie
zrobił, wtedy najłatwiej jest robić wcięcia klawiczem Tab.

```python
def kwadrat(liczba):
    wynik = liczba ** 2
    return wynik
```

Wciśnij teraz przycisk "run".  Jeżeli w oknie trybu interaktywnego nie
zauważysz żadnego błędu, będzie to oznaczało, że funkcja została prawidłowo
zdefiniowana.  Teraz możemy ja wywołać w trybie interaktywnym:

```python
>>> kwadrat(5)
25
>>> kwadrat(3) + kwadrat(1)
10
```

Jak widzisz, aby wywołać funkcję, wystarczy wpisać jej nazwę, po czym
w nawiasach wpisać wartość argumentu.  Jeżeli argumentów jest wiele, to
należy je oddzielić przecinkami.

:snake: Zdefiniuj funkcję o nazwie `pole_kola`, która przyjmuje argument
`promien` i zwraca wartość równania `(promien * 3.14) ** 2`.  Wywołaj ją
w oknie trybu interaktywnego.

:snake: Wywołaj funkcję `pole_kola` bez argumentu: `pole_kola()`. Czy
rozumiesz treść wyjątku jaki został rzucony?

:snake: Wywołaj funkcję `pole_kola` z dwoma argumentami: `pole_kola(2, 3)`.
Porównaj treść wyjątku do błędu z poprzedniego zadania.


## Argumenty

Funkcja nie musi posiadać żadnych argumentów, w takim wypadku nawiasy
w nagłówku zostawiamy puste:

```python
def funkcja():
    return 123
```

Jak już wspomnieliśmy, funkcje mogą przyjmować więcej niż jeden argument:

```python
def suma(a, b):
    return a + b


def osoba(imie, nazwisko, tytul):
    imie_nazwisko = imie + ' ' + nazwisko
    return tytul + ' ' + imie_nazwisko.title()
```

Takie funkcje wywołujemy podobnie jak te z jednym argumentem:

```python
>>> funkcja()
123
>>> suma(100, 45)
145
>>> suma(100, -20)
80
>>> osoba('jan', 'KOWALSKI', 'doktor')
'doktor Jan Kowalski'
```

:snake: Napisz funkcję `cena_brutto`, która przyjmuje argumenty
`cena_netto` oraz `vat` i zwraca wartość netto obliczoną według wzoru
`netto * (1 + vat)`.

:snake: Napisz funkcję `imie_nazwisko`, która przyjmuje argumenty `imie`
oraz `nazwisko` i zwraca stringa z imieniem i nazwiskiem oddzielonymi
spacją.  Upewnij się, że każde słowo w stringu zaczyna się od wielkiej
litery (użyj metody `title`).  Następnie napisz funkcję `lubi`,
z argumentami `imie`, `nazwisko` oraz `co` i wywołana w ten sposób:
`lubi('jan', 'kowalski', 'KALAFIORY')` zwróci stringa
`'Jan Kowalski lubi kalfiory'`.  Pisząc funkcję `lubi` użyj funkcji
`imie_nazwisko`.


## Funkcje wbudowane

Poza funkcjami, które sami możemy zdefiniować, istnieją funkcje, które
zawsze są dostępne w interpreterze Pythona.  Nazywamy je **funkcjami
wbudowanymi**.  Przykładem jest funkcja `len`, o której mówiliśmy w jednym
z poprzednich rozdziałów:

```python
>>> len('python')
6
```

Poza tym mamy jeszcze [67 innych funkcji wbudowanych](https://docs.python.org/3/library/functions.html).
Część z nich poznasz w kolejnych rozdziałach, a kilka innych opisaliśmy
poniżej.

### `str`

Przyjmuje jako argument dowolny obiekt i zwraca jego reprezentację jako
string:

```python
>>> str(2017)
'2017'
```

:snake: Zamień na string liczbę ujemną.

:snake: Zobacz co się stanie, jeżeli jako argument przekażesz do `str`
tekst.


### `int`

Przyjmuje jako argument dowolny obiekt i zamienia go na integer:

```python
>>> int(' 123 ')
123
```

:snake: Zobacz co się stanie, gdy przekażesz do funkcji `int` liczbę
z częścią ułamkową (float), np. `3.14`.

:snake: Zobacz co się stanie, jeśli przekażesz do `int` stringa, w którym
nie ma żadnej liczby.

:snake: Zobacz co sie stanie, kiedy przekażesz do `int` stringa, w którym
są zarówno litery jak i cyfry, np. `Ala ma 2 koty`.


### `float`

Przyjmuje jako argument dowolny obiekt i zamienia go na float:

```python
>>> float('3.14')
3.14
```

:snake: Zobacz jak zachowa się funkcja `float`, gdy wywołasz ją z:
integerem, stringiem z samymi literami, stringiem z samymi cyframi.


## :pushpin: Podsumowanie

W tym rozdziale:

* dowiedzieliśmy się czym jest funkcja, jak ją definiować i wywoływać,
* poznaliśmy funkcje wbudowane `str`, `int` oraz `float`.

---

# Rozdział 8. Funkcja `print`

W tym rozdziale:

* poznasz funkcję wbudowaną `print`.


## Wypisywanie tekstu na ekran

Gdy korzystaliśmy z trybu interaktywnego i chcieliśmy wypisać coś na ekran,
wystarczyło wpisać jakieś wyrażenie i wcisnąć Enter:

```python
>>> 2 + 2
4
>>> x = 'PyLadies'
>>> x
'PyLadies'
```

Mogliśmy tak robić, ponieważ w ten sposób działa tryb interaktywny:
wykonuje operację i wyświetla jej wynik.  Jednak zazwyczaj programy
w Pythonie są bardziej złożone i często zdarza się, że chcemy zobaczyć
więcej niż tylko ostateczny wynik.  Na przykład gdy piszemy program, który
przetwarza plik tekstowy i chcemy, żeby dla każdej linijki tekstu wypisał
coś na ekran.  W takim wypadku z pomocą przychodzi funkcja wbudowana
`print`.


## `print`

Funkcja ta przyjmuje dowolną liczbę argumentów i wypisuje wszystkie na
ekran, oddzielając je spacjami:

```python
>>> print(2017)
2017
>>> print('PyCon PL', 2017)
PyCon PL 2017
```

Do `print` można przekazywać również zmienne:

```python
>>> temperatura = 24
>>> print('Temperatura:', temperatura, 'stopnie Celsjusza')
Temperatura: 24 stopnie Celsjusza
```

:snake: Napisz funkcję, która przyjmuje argument `rok_urodzenia`, wypisuje
tekst `Masz X lat`, gdzie `X` to wiek w roku 2017, oraz zwraca ten wiek.


## :pushpin: Podsumowanie

W tym rozdziale:

* poznaliśmy funkcję `print`.

---


# Rozdział 8. Listy

W tym rozdziale:

* dowiesz się czym są **listy**,
* poznasz metody `append`, `pop`, `count`, `remove` i `index`,
* poznasz funkcje wbudowane `sum`, `max`, `min` oraz `sorted`.

## Lista

Listy towarzyszą nam na co dzień.  Kiedy chcemy posłuchać muzyki,
odtwarzamy playlistę.  W sklepie spoglądamy na listę zakupów.  Szukając
czegoś w internecie, przeglądamy listę wyników.

Jeśli pomyślimy o tym dłużej, zauważymy, że w formie listy można
zaprezentować wiele innych zjawisk i rzeczy: zbiór książek w bibliotece,
wydarzenia z jakiegoś okresu, zadania do wykonania, kolejka samochodów
na stacji benzynowej itd.  Lista to w programowaniu bardzo ważne pojęcie,
bo pozwala w prosty sposób opisać zbiór obiektów, które są ułożone w jakimś
porządku: alfabetycznym, chronologicznym, losowym etc.  Listy w Pythonie
to potężne, a równocześnie proste narzędzie, którego używa się niemal na
każdym kroku.

Aby zdefiniować listę, należy wypisać obiekty (stringi, integery)
oddzielone przecinkami w nawiasach kwadratowych:

```python
>>> kolory = ['niebieski', 'czerwony', 'zielony', 'czarny']
>>> print(kolory)
['niebieski', 'czerwony', 'zielony', 'czarny']
```

W taki sposób definiujemy pustą listę:

```python
>>> l = []
>>> print(l)
[]
```

Możemy odwołać się do poszczególnych elementów listy wpisując jej nazwę
po czym, w nawiasach kwadratowych, numer elementu (**indeks**).  Pamiętaj,
że numeracja zaczyna się od zera!

```python
>>> print(kolory[0])
niebieski
>>> print(kolory[2])
zielony
```

Chcąc otrzymać ostatni element na liście, możemy użyć indeksu `-1`:

```python
>>> print(kolory[-1])
czarny
```

**Indeksy ujemne** to sposób na dostęp do elementów listy "od końca":

```python
>>> print(kolory[-2])
zielony
>>> print(kolory[-3])
czerwony
```

Możemy dowolnie mieszać typy elementów na liście:

```python
>>> liczby = ['jeden', 2, 'trzy', 4, 5]
```

Lista może zawierać w sobie również inne listy:

```python
>>> odcienie_czerwieni = ['karmazynowy', 'czerwony', 'bordowy']
>>> kolory = ['zielony', odcienie_czerwieni, 'niebieski']
>>> print(kolory)
['zielony', ['karmazynowy', 'czerwony', 'bordowy'], 'niebieski']
```

:snake: Napisz funkcję `element`, która przymuje dwa argumenty, listę oraz
numer indeksu (integer) i zwraca element listy znajdujący się pod podanym
indeksem.

:snake: Napisz funkcję `ostatni_element`, która jako argument przyjmuje
listę i zwraca jej ostatni element.  Użyj w niej funkcji `element`.


## Metody listy

Listy, podobnie jak stringi mają wiele przydatnych metod.  Poniżej
znajdziesz opis kilku najbardziej przydatnich z nich.


### `append`

Ta metoda służy do dodawania elementu do listy:

```python
>>> liczby = [1, 3]
>>> print(liczby)
[1, 3]
>>> liczby.append(5)
>>> print(liczby)
[1, 3, 5]
>>> liczby.append(7)
>>> print(liczby)
[1, 3, 5, 7]
```

:snake: Napisz funkcję, która jako argument przyjmuje listę i dodaje na
jej końcu taki sam element jaki jest na samym jej początku.


### `pop`

Metoda `pop` nie przyjmuje żadnych argumentów, a zwraca ostatni element
lity, jednocześnie usuwając go z niej:

```python
>>> litery = ['a', 'b', 'c', 'd']
>>> print(litery)
['a', 'b', 'c', 'd']
>>> litery.pop()
'd'
>>> print(litery)
['a', 'b', 'c']
>>> litery.pop()
'c'
>>> litery.pop()
'b'
>>> print(litery)
['a']
```

:snake: Napisz funkcję, która usuwa z listy dwa ostatnie elementy, po czym
dodaje do niej ten element, który na samym początku był ostatni.


### `count`

`count` przyjmuje jako argument jeden dowolny obiekt i zwraca liczbę
wystąpień tego obiektu na liście:

```python
>>> oceny = [4, 3, 3, 5, 2, 3, 5, 4, 2, 4, 5, 4, 3, 3]
>>> oceny.count(3)
5
>>> oceny.count(4)
4
>>> oceny.count(2)
2
```

### `remove`

Metoda `remove` przyjmuje jako argument dowolny obiekt i usuwa go z listy.
Jeżeli obiekt występuje na liście wielokrotnie, to tylko jego pierwsze
wystąpienie jest usuwane:

```python
>>> liczby = [10, 20, 25, 20, 10, 15]
>>> liczby.remove(20)
>>> print(liczby)
[10, 25, 20, 10, 15]
>>> liczby.remove(20)
>>> print(liczby)
[10, 25, 10, 15]
>>> liczby.remove(10)
>>> print(liczby)
[25, 10, 15]
```

:snake: Sprawdź co się stanie jeżeli spróbujemy usunąć element, którego
nie ma na liście.

:snake: Napisz funkcję, która przyjmuje dwa argumenty: listę oraz dowolny
inny obiekt.  Funkcja powinna usunąć z listy pierwsze wystąpienie tego
obiektu, a następnie dodać go na końcu listy.  Funkcja powinna zwrócić
liczbę wystąpień tego elementu na liście.


### `index`

`index` przyjmuje jeden obiekt jako argument i zwraca numer pozycji na
jakiej ten obiekt znajduje się na liście:

```python
>>> litery = ['r', 't', 'b', 'w', 'h']
>>> litery.index('t')
1
>>> litery.index('h')
4
```

:snake: Sprawdź co się stanie jeżeli spróbujemy pobrać indeks elementu,
którego nie ma na liście.


## Listy i funkcja `len`

Podobnie jak w przypadku stringów, długość listy możemy sprawdzić funkcją
wbudowaną `len` :

```python
>>> litery_nazwiska = ['K', 'o', 'w', 'a', 'l', 's', 'k', 'i']
>>> print(len(litery_nazwiska))
8
```


## Funkcje wbudowane `sum`, `min`, `max` i `sorted`

Istnieje kilka funkcji wbudowanych, które pomagają nam w pracy z listami.
Tutaj opiszemy część z nich.

Pierwsze trzy są najbardziej pomocne gdy operujemy na listach, których
wszystkie elementy są liczbami.  `sum` zwraca sumę wszystkich elementów,
`min` zwraca element o najmniejszej wartości, a `max` ten o największej
wartości:

```python
>>> pomiary = [2, 4.25, 5.30, 3]
>>> sum(pomiary)
14.55
>>> min(pomiary)
2
>>> max(pomiary)
5.3
```

:snake: Napisz funkcję, która jako argument przyjmuje listę i wypisuje na
ekran element o największej wartości oraz liczbę wystąpień tego elementu
na liście.

Kolejna funkcja to `sorted`, która przyjmuje listę, a zwraca posortowaną
kopię tej listy:

```python
>>> wyniki = [45.5, 47.2, 35.8, 41.0, 33.3]
>>> posortowane_wyniki = sorted(wyniki)
>>> print(posortowane_wyniki)
[33.3, 35.8, 41.0, 45.5, 47.2]
>>> print(wyniki)
[45.5, 47.2, 35.8, 41.0, 33.3]
```

:snake: Napisz funkcję, która jako argument przyjmie listę, posortuje ją,
a następnie zwróci jej ostatni element.  (W ten sposób otrzymamy własną
wersję funkcji `max`!)


## :pushpin: Podsumowanie

W tym rozdziale:

* dowiedzieliśmy się czym są listy, jak je definiować i jak odnosić się
do poszczególnych elementów listy,
* poznaliśmy najważniejsze metody list,
* dowiedzieliśmy się, w jaki sposób używać na listach funkcji wbudowanych
`len`, `sum`, `max`, `min` oraz `sorted`.


---

# Rozdział 10. Pętla `for`

W tym rozdziale:

* dowiesz się czym jest **iteracja** i **pętla**,
* poznasz pętlę `for`.


## Iteracja

Kiedy operujemy na liście, bardzo często chcemy "przejść" po wszystkich
jej elementach po kolei i na każdym z nich wykonać jakąś operację.  Takie
"przejście" nazywamy **iteracją**.  W Pythonie, aby otrzymać każdy element
listy po kolei, możemy oczywiście użyć indeksów:

```python
>>> daty = ['15/07/2017', '16/07/2017', '17/07/2017']
>>> print(daty[0])
15/07/2017
>>> print(daty[1])
16/07/2017
>>> print(daty[2])
17/07/2017
```

Jednak takie podejście jest niewygodne kiedy lista jest bardzo długa.
A co gdy w ogóle nie wiemy na jak długiej liście działamy?  Te problemy
można rozwiązać za pomocą **pętli**, czyli instrukcji, która wykonuje
podane operacje dopóki jakiś warunek nie zostanie spełniony.  Z użyciem
pętli możemy na przykład iterować, czyli wykonywać operacje na kolejnych
elementach listy, dopóki nie dojdziemy do jej końca.

## Pętla `for`

Pętle mają wiele zastosowań, ale iteracja jest jednym z najczęściej
spotykanych.  Dlatego Python posiada pętlę `for`, która służy właśnie do
tego. Spójrzmy na taki przykład:

```python
godziny_odjazdu = ['7:30', '13:45', '16:10']
for godzina in godziny_odjazdu:
    print(godzina)
```

Przepisz do edytora powyższy kod i wykonaj go.  W oknie trybu
interaktywnego zobaczysz, że funkcja `print` została wykonana dla każdego
elementu na liście, wypisując go na ekran.  Stało się tak, ponieważ Python
przeszedł po wszystkich elementach listy `godziny_odjazdu` i dla każdego
z nich przypisał jego wartość do zmiennej `godzina` i wykonał operację
`print`.

Definicja pętli zaczyna się od słowa `for`, następnie należy podać nazwę
zmiennej, do której będą przypisywane wartości kolejnych elementów, dalej
wpisujemy słowo `in`, nazwę listy oraz dwukropek.  W kolejnych linijkach
znajdują się operacje, które zostaną wykonane dla każdego elementu.
Pamiętaj, że przed każdą operacją musi się znaleźć jednakowe wciącie
w kodzie.  Ich szerokość nie ma znaczenia, ważne żeby były takie same.

Jeżeli pętla znajduje się wewnątrz funkcji, to wcięcie wewnątrz `for`
należy powiększyć o szerokość wcięcia funkcji:

```python
def wypisz_elementy(lista):
    for element in lista:
        print(element)
```

:snake: Napisz funkcję, która jako argument przyjmie listę liczb i wpisze
na ekran wartość każdej z nich podniesioną do kwadratu.

:snake: Napisz funkcję, który przyjmie listę stringów i zwróci nową listę,
na której znajdą się wszystkie te stringi pisane wielkimi literami
(użyj metody `upper`).


## `for` i stringi

Pętla `for` jest bardzo elastyczna: możesz jej użyć również na stringu.
W takim wypadku jej elementami będą poszczególne litery:

```python
for litera in 'ala ma kota':
    print(litera)
```

:snake: Napisz funkcję, która jako argument przyjmie string i wypisze każdą
jego literę wraz z liczbą wystąpień tej litery w stringu (użyj metody
`count`).


## Metoda `split`

String posiada metodę `split`, która rodziela go w miejscach wystąpienia
danego znaku i zwraca listę stringów, które powstały w ten sposób:

```python
>>> s = '2015,2016,2017'
>>> s.split(',')
['2015', '2016', '2017']
```

Jeżeli nie przekażemy żadnego argumentu, to string zostanie rozdzielony
w miejscach spacji:

```python
>>> 'ala ma kota'.split()
['ala', 'ma', 'kota']
```

:snake: Napisz funkcję, która jako argument przyjmuje string i wypisuje
wszystkie jego słowa, każde w osobnej linijce.


## :pushpin: Podsumowanie

W tym rozdziale:

* poznaliśmy pojęcia *iteracja* oraz *pętla*,
* nauczyliśmy się korzystać w pętli `for`,
* dowiedzieliśmy się, że pętla `for` działa także na stringach, oraz że
stringi posiadają metodę `split`.


---

# Rozdział 11. Prawda i fałsz

W tym rozdziale:

* poznasz pojęcia "prawda" i "fałsz" oraz ich reprezentację w Pythonie:
`True` i `False`,
* poznasz **instrukcję warunkową** `if`, która pozwala zmienić przebieg
programu jeżeli określony warunek zostanie spełniony.


## Prawda, fałsz i warunek

Programy jakie dotąd pisaliśmy składały się z operacji, które Python
wykonywał jedna po drugiej.  Gdy jedna instrukcja została pomyślnie
zrealizowana, program przechodził do wykonania kolejnej.

Pisząc kolejne programy szybko przekonasz się, że taki scenariusz nie
zawsze będzie Ci odpowiadał, ponieważ często chcemy, żeby jakieś operacje
zostały wykonane tylko gdy zostanie spełniony pewien warunek.

Na przykład: mamy listę liczb i chcemy przejść po jej elementach, wypisując
tylko te nieparzyste.  W takim przypadku warunkiem wypisania liczby na
ekran jest "liczba jest niepatrzysta".

Języki programowania pozwalają definiować takie warunki i sprawdzać je.
Wynikiem takiego sprawdzenia jest **prawda** lub **fałsz**.  Prawda oznacza
sytuację w której warunek został spełniony.  Przeciwieństwem jest fałsz.
Przykładowo wynikiem warunku "żyrafa to ptak" jest fałsz, a wynikiem dla
"Ziemia nie jest płaska" jest prawda.


## Warunki w Pythonie, `True` i `False`

W Pythonie mamy do dyspozycji szereg operatorów, które pozwalają nam
sprawdzać prawdziwość wyrażeń.  Możemy na przykład porównywać wartości.
Służy do tego operator `==`:

```python
>>> 1 == 2
False
>>> (2 + 2) == (2 * 2)
True
```

Odwrotnością operatora `==` jest `!=`:

```python
>>> 'ala' != 'Ala'
True
>>> [1, 2] != [1, 2]
False
```

Możemy również sprawdzać czy jedna wartość jest większa lub mniejsza od
drugiej:

```python
>>> 100 > 70
True
>>> 70 > 100
False
>>> 
```

Operatory `>` i `<` można mieszać z `=`, w ten sposób tworząc warunek
"większy lub równy" i "mniejszy lub równy":

```python
>>> 3 >= 2
True
>>> 2 >= 2
True
>>> 1 >= 2
False
```

Zwróć uwagę, że w jednym wyrażeniu można użyć wielu operatorów:

```python
>>> 1 <= 2 < 3 <= 3 < 4
True
```

Ponadto możemy zaprzeczyć całemu wyrażeniu pisząc na początku `not`:

```python
>>> not 1 == 1
False
>>> not 1 == 2
True
```

Oczywiście w każdym przypadku wartości wpisane wprost możemy zastąpić
zmiennymi.


## Porównywanie stringów

Znając matematykę intuicyjnie rozumiemy w jaki sposób Python porównuje
ze sobą liczby.  Ale w jaki sposób porównywane są stringi?  Odpowiedź jest
prostsza niż mogło by się wydawać: alfabetycznie.  Litery znajdujące się
dalej w alfabecie są "większe" od tych wcześniejszych.  Poza tym litery
małe są "większe" od tych dużych.

```python
>>> 'A' < 'B' < 'a' < 'b'
True
```

Co ze stringami, które mają więcej niż jeden znak?  Są one porównywane
znak po znaku, dopóki któryś z nich nie będzie się różnił, albo dopóki
jeden ze stringów będzie dłuższy.  W tym drugim przypadku większy będzie
ten string który ma więcej znaków.

```python
>>> 'a' < 'ala'
True
>>> 'ala' == 'ala'
True
>>> 'ala' < 'ala ma kota'
True
```


## Operator `in`

Poza dotychczas omówionymi operatorami, jest jeszcze jeden, szczególnie
przydatny kiedy pracujemy z listami.  Operator `in` zwraca `True` jeżeli
dany element znajduje się na liście:

```python
>>> 'Basia' in ['Tomek', 'Magda', 'Karol', 'Basia']
True
>>> 12 in [10, 20, 30, 40]
False
```


## Instrukcja warunkowa `if`

Sprawdzanie czy jakieś wyrażenie jest prawdziwe nie miałoby żadnego sensu
gdybyśmy nie mogli w jakiś sposób na tej podstawie podjąć decyzji
o przebiegu naszego programu.  W tym celu używamy **instrukcji warunkowej**
`if`:

```python
if temperatura > 30.0:
    print('Uf jak gorąco!')
```

Struktura tej instrukcji jest bardzo prosta: po słowie `if` wpisujemy
warunek, następnie dwukropek i w kolejnych liniach, po wciąciu, instrukcje,
które zostaną wykonane jeżeli warunek będzie prawdziwy (mówimy: jeżeli
zostanie spełniony).

:snake: Napisz funkcję, która przyjmuje argumenty `element` i `lista`
i jeżeli dany element znajduje się na liście, to zwraca jego pozycję
(użyj metody `index`), w przeciwnym wypadku zwraca `-1`.

:snake: Napisz funkcję `iloraz`, która przyjmuje argumenty `dzielna`
i `dzielnik`. Jeżeli dzielnik jest różny od zera, funkcja powinna zwrócić
wynik dzielenia.  W przeciwnym wypadku powinna wypisać komunikat o błędzie.


## `if ... else` oraz `elif`

Do instrukcji `if` możemy dopisać drugą część, która zostanie wykonana
tylko jeżeli warunek nie będzie spełniony:

```python
if godzina <= godzina_odjazdu:
    print('Godzina odjazdu:', godzina_odjazdu)
else:
    print('Przepraszamy za opóźnienie')
```

Zwróć uwagę na wcięcia w kodzie: `if` oraz `else` są na tym samym
"poziomie".

Jeżeli chcemy, możemy w ramach jednej instrukcji `if` sprawdzić kilka
alternatywnych warunków, jeżeli poprzednie okażą się nieprawdziwe:

```python
if 5 <= godzina < 12:
    print('rano')
elif godzina == 12:
    print('południe')
elif 12 < godzina < 17:
    print('popołudnie')
elif 17 < godzina < 20:
    print('wieczór')
else:
    print('noc')
```

:snake: Napisz funkcję, która porównuje dwie liczby.  Jako argumenty
powinna przyjmować liczby `a` i `b`.  Jeżeli `a` jest większe od `b`
powinna zwrócić 1, jeżeli liczby są równe `0`, a jeżeli `a` jest mniejsze
od `b`, `-1`.  Dodatkowo, w zależności od wyniku porównania, funkcja
powinna wypisać jeden z komunikatów: `a < b`, `a == b` lub `a > b`.


## Łączenie warunków

Czasami będziemy chcieli wykonać jakieś operacje tylko jeżeli spełnionych
zostanie kilka warunków jednocześnie.  W takim wypadku możemy użyć
operatora `and`:

```python
if substancja == 'woda' and temperatura > 100:
    stan_skupienia = 'para wodna'
```

Gdybyśmy chcieli, żeby operacja została wykonana jeżeli przynajmniej jeden
z kilku warunków zostanie spełniony, to należy użyć operatora `or`:

```python
if produkt == 'sok' or produkt == 'herbata'
    cena = 4.50
```

Operatory `or` i `and` można łączyć w jednym wyrażeniu.


## :pushpin: Podsumowanie

W tym rozdziale:

* nauczyliśmy się sprawdzać prawdziwość wyrażeń,
* poznaliśmy intrukcję `if`, która może zmienić przebieg programu gdy
określone wyrażenie jest prawdziwe.


---


# Rozdział 12. Słowniki

W tym rozdziale:

* dowiesz się czym jest **słownik**, **klucz** oraz **wartość**,
* nauczysz się definiować słowniki oraz wykonywać na nich operacje,
* poznasz najczęściej spotykane zastosowania słowników.


## Czym jest słownik

Wiele sytuacji z jakimi spotkasz się pisząc programy będzie można opisać
jako zbiór kluczy i wartości im odpowiadających.  Przykładem z codziennego
życia jest encyklopedia, gdzie kluczami są różne hasła, a wartościami
są definicje tłumaczące te hasła.  Można pójść dalej i powiedzieć, że
internet to zbiór adresów (np. `pl.pycon.org`) oraz stron WWW, które się
pod nimi kryją.

Takie spojrzenie na otaczającą nas rzeczywistość jest bardzo wygodne,
bo pozwala opisać złożone zjawiska w systematyczny, łatwy do zrozumienia
sposób.  Dlatego też wiele języków programowania oferuje narzędzia do
tworzenia tego typu struktur.  W przypadku Pythona są to **słowniki**.

Słownik (*dictionary*, w skrócie *dict*), to zbiór **kluczy** oraz
odpowiadających im **wartości**.  Nazwa "słownik" nie jest przypadkowa,
nawiązuje do formuły w której zbiorowi słów przypisujemy ich definicje.


## Definicja słownika

Słownik definiujemy poprzez wypisanie par klucz-wartość, oddzielonych
przecinkami, ujmując całość w nawiasy klamrowe.  Każda para to dwie
wartości oddzielone dwukropkiem.

```python
wiek = {'Marcin': 23, 'Agata': 17, 'Marta': 46}
```

Aby stworzyć pusty słownik wystarczą puste nawiasy klamrowe:

```python
d = {}
```

Wartości w słowniku nie muszą być tego samego typu, jedna może być liczbą,
kolejna stringiem itd.:

```python
d = {'liczba': 123, 'inna liczba': 12.34, 'lista': ['Ala ma kota']}
```

Klucze mogą być również liczbami:

```python
d = {15: 'Ala ma kota', 'Kot ma alę': 3.14}
```

Słownik też może być elementem listy:

```python
l = [{'a': 1, 'b': 2}, 3, 4]
```

Kiedy wypiszemy słownik na ekran, zobaczymy całą jego zawartość:

```python
>>> d = {'a': ['x', 9, 'z'], 'b': 2, 'c': 'Ala ma kota'}
>>> print(d)
{'a': ['x', 9, 'z'], 'b': 2, 'c': 'Ala ma kota'}
```


## Operacje na słownikach

Kiedy zdefiniujemy słownik, możemy na nim wykonać szereg operacji.


### Pobieranie wartości elementu

Aby otrzymać wartość dla danego klucza należy wpisać nazwę słownika,
a następnie, w nawiasach kwadratowych, nazwę klucza:

```python
>>> d = {'a': 1, 'b': 2}
>>> print(d['a'])
1
>>> print(d['a'] + d['b'])
3
```

:snake: Zobacz co się stanie jeżeli pobierzesz wartość dla klucza, który
nie istnieje w słowniku.

:snake: Napisz funkcję, która przyjmie dwa argumenty, listę słowników
oraz klucz i zwróci listę wartości znajdujących się pod tym kluczem
z każdego słownika na liście.


### Definiowanie elementu

W każdej chwili możemy zdefiniować wartość klucza w słowniku.  Żeby to
zrobić należy odwołać się do danego klucza i przypisać do niego wartość:

```python
>>> d = {'a': 1}
>>> d['b'] = 2
>>> d[5] = ['lista', 'elementów']
>>> print(d)
{'a': 1, 'b': 2, 5: ['lista', 'elementów']}
>>> print(d[5])
['lista', 'elementów']
```

Jeżeli dany klucz już istnieje, jego wartość zostanie nadpisana:

```python
>>> d = {'a': 1}
>>> print(d['a'])
1
>>> d['a'] = 2
>>> print(d['a'])
2
```


### Usuwanie elementu

Możemy usunąć dowolny klucz słownika posługując się instrukcją `del`:

```python
>>> d = {'a': 1, 'b': 2}
>>> del d['a']
>>> print(d)
{'b': 2}
```

:snake: Zobacz co się stanie jeżeli spróbujesz usunąć klucz, który nie
istnieje w słowniku.


### Iterowanie po kluczach i wartościach

W jednym z poprzednich rozdziałów mówiliśmy o iteracji w kontekście listy,
czyli o "przechodzeniu" po jej elementach.  Używaliśmy w tym celu pętli
`for`.  Jeżeli wykonamy tę samą operację na słowniku, to przejdziemy po
jego kluczach:

```python
for klucz in slownik:
    print(klucz)
```

:snake: Napisz funkcję, która przyjmuje jako argument słownik i przechodzi
po jego kluczach, wypisując każdy z nich.

W podobny sposób możemy iterować po samych wartościach słownika.  Służy
do tego metoda `values`:

```python
lista_startowa = {1: 'Puchatek', 2: 'Prosiaczek', 3: 'Tygrysek'}
for zawodnik in lista_startowa.values():
    print(zawodnik)
```

:snake: Napisz funkcję, która przyjmuje jako argument słownik i zwraca
sumę wszystkich wartości słownika.  Zakładamy, że wartości zawsze są
liczbami.

Słownik posiada również metodę `items`, dzięki której możemy iterować
jednocześnie po kluczach i wartościach słownika:

```python
lista_startowa = {1: 'Puchatek', 2: 'Prosiaczek', 3: 'Tygrysek'}
for numer_startowy, zawodnik in lista_startowa.items():
    print(numer_startowy, ':', zawodnik)
```

Zwróć uwagę, że tym razem w pętli `for` zdefiniowaliśmy dwie zmienne:
`numer_startowy` i `zawodnik`.  Nie jest to nic specyficznego dla słownika,
ale kolejna właściwość tej pętli.  Jeżeli pętla przechodzi po liście,
której wszystkie elementy są sekwencjami (czyli listami lub krotkami),
to możemy od razu **rozpakować** wszystkie elementy tych sekwencji do
zmiennych:

```python
lista = [['a', 'Arbuz', 'Anglia'], ['b', 'Banan', 'Brazylia']]
for litera, owoc, panstwo in lista:
    print(owoc)
```

W naszym przypadku pierwszym elementem każdej sekwencji jest klucz,
a drugim wartość dla tego klucza.

:snake: Napisz funkcję, która przyjmie dwa argumenty, słownik oraz wartość
i zwróci nazwę klucza, którego wartość jest równa wartości z argumentu.


## Zagnieżdżanie słowników

Wartością w słowniku może być dowolny obiekt, również inny słownik.
Dzięki temu możemy w prosty sposób tworzyć złożone struktury danych:

```python
>>> auto = {}
>>> auto['kolor'] = 'czerwony'
>>> auto['silnik'] = {'pojemność': 1600, 'moc': 130}
>>> print(auto)
{'kolor': 'czerwony', 'silnik': {'pojemność': 1600, 'moc': 130}}
```


## "Długość" słownika

Kiedy po raz pierwszy wspomnieliśmy o funkcji `len`, powiedzieliśmy, że
służy ona do sprawdzania długości obiektów.  Każdy typ obiektu (string,
lista, etc.) może inaczej rozumieć pojęcie długości.  W przypdku stringów
chodzi o liczbę znaków, w przypadku list o liczbę elementów itd.
Słowniki również mają swoją "długość": jest to liczba kluczy.

```python
>>> print(auto)
{'kolor': 'czerwony', 'silnik': {'pojemność': 1600, 'moc': 130}}
>>> len(auto)
2
```


## Do czego możemy wykorzystać słowniki

Słownik jest bardzo uniwersalną strukturą danych, przez co ma wiele
zastosowań:

* reprezentacja obiektów i ich atrybutów (jak w powyższym przykładzie),
* mapowanie jednych wartości na inne (jak w prawdziwym słowniku),
* przechowywanie wielu powiązanych ze sobą wartości w jednym miejscu
(np. klucze to tytuły filmów, a wartości to ich reżyserowie).

:snake: Wybierz jedno z powyższych zastosowań słownika.  Napisz funkcję
`ustaw`, która przyjmuje trzy argumenty, słownik, klucz oraz wartość i
ustawia w słowniu daną wartość pod danym kluczem.  Napisz funkcję
`pobierz`, która przyjmuje dwa argumenty, słownik oraz klucz i zwraca
wartość słownika pod danym kluczem.  Stosując te funkcje wypełnij słownik
danymi adekwatnymi dla wybranego zastosowania i pobierz te dane.


## :pushpin: Podsumowanie

W tym rozdziale:

* nauczyliśmy się tworzyć słowniki i wykonywać na nich operacje, między
innymi iterowanie,
* dowiedzieliśmy się, że funkcja `len` zwraca liczbę kluczy w słowniku,
* poznaliśmy najczęściej spotykane zastosowania słowników.
