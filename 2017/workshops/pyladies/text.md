# Rozdział 1. Tryb interaktywny

Warsztaty zaczniemy od wyjaśnienia w jaki sposób będziemy programowali
w Pythonie.

## Zaczynamy!

Otwórz ten link: https://repl.it/languages/python3 w osobnej karcie
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
cyfry. Istnieją tysiące znaków, jakich możesz użyć [1].

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

Poza tym mamy jeszcze 67 innych funkcji wbudowanych [2].
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


## Formatowanie stringów

W tym miejscu warto wrócić do stringów i opowiedzieć o jeszcze jednej,
bardzo przydatnej metodzie: `format`.  Służy ona do **formatowania
stringów**, czyli "wstawiania" do nich wartości zmiennych.  Spójrz na
poniższy przykład:

```python
>>> 'ala {} kota'.format('ma')
'ala ma kota'
```

Jak widzisz, wywołanie metody `format` spowodowało, że para znaków `{}`
została zastąpiona argumentami funkcji.  W podobny sposób możemy wstawić
dowolną liczbę i typ obiektów:

```python
>>> szerokosc = 110
>>> wysokosc = 50.5
>>> jednostka = 'mm'
>>> '{}x{} {}'.format(szerokosc, wysokosc, jednostka)
'110x50.5 mm'
```

Możliwości metody `format` nie kończą się na zwykłym wstawianiu wartości
do stringa.  [Dokumentacja Pythona](https://docs.python.org/3.6/library/string.html#formatspec)
w szczegółach opisuje tę funkcję.  Warto przyjrzeć się choćby przykładom,
które tam zamieszczono.

:snake: Zobacz co się stanie, jeżeli liczba argumentów metody `format`
będzie __mniejsza__ niż liczba wystąpień `{}` w stringu.


## :pushpin: Podsumowanie

W tym rozdziale:

* poznaliśmy funkcję `print` oraz metodę `format`.

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


## Wycinki list

Czasami operując na liście chcielibyśmy używać tylko jej fragmentu, np.
10 pierwszych elementów, albo elementy od drugiego do piątego.  Python
jest przygotowany na taką sytuację: umożliwia utworzenie *wycinka*
listy (ang. *slice*).  Aby stworzyć wycinek należy wpisać nazwę listy,
a następnie w nawiasach kwadratowych indeksy pierwszego i ostatniego
wycinka elementu odzielone dwukropkiem.

Przykładowo, zwrócenie fragmentu listy od drugiego do czwartego elementu
będzie wyglądało tak:

```python
>>> l = [1, 2, 3, 4, 5, 6, 7]
>>> l[1:4]
[2, 3, 4]
```

Pamiętaj, że indeksy listy zaczynając się od zera, a element o indeksie
końcowym (w tym wypadku: `5`) nie zostanie dołączony do wycinka.

Możemy też pominąć indeks początkowy.  W takim wypadku Python zwróci
wszystkie elementy od początku:

```python
>>> l[:5]
[1, 2, 3, 4, 5]
```

Jeżeli pominiemy indeks końcowy, dostaniemy wszystkie elementy do końca
listy:

```python
>>> l[2:]
[3, 4, 5, 6, 7]
```

Jeżeli indeks końcowy będzie liczbą ujemną, to pozycja ostatniego elementu
wycinka będzie liczona od końca listy:

```python
>>> l[:-1]
[1, 2, 3, 4, 5, 6]
>>> l[:-2]
[1, 2, 3, 4, 5]
```

Co ciekawe, wycinki możemy tworzyć również ze stringów:

```python
>>> s = 'ala ma kota'
>>> s[2:8]
'a ma k'
```

:snake: Zobacz co się stanie, jeżeli indeks początkowy będzie liczbą
ujemną, lub jeżeli indeks końcowy będzie większy niż długość listy.


## :pushpin: Podsumowanie

W tym rozdziale:

* dowiedzieliśmy się czym są listy, jak je definiować i jak odnosić się
do poszczególnych elementów listy,
* poznaliśmy najważniejsze metody list,
* dowiedzieliśmy się, w jaki sposób używać na listach funkcji wbudowanych
`len`, `sum`, `max`, `min` oraz `sorted`.

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


### Metoda `split`

Możemy również iterować po słowach.  Służy do tego metoda `split`:

```python
for slowo in 'ala ma kota':
    print(slowo)
```

Tak na prawdę metoda `split` ma dużo szersze zastosowanie.  Jeżeli
podamy jej jako argument jakiś znak, wtedy string zostanie podzielony
w miejscach występowania tego znaku:

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


## `range`

W tym miejscu warto wspomnieć o funkcji wbudowanej `range`.  Przyjmuje
ona jako argumenty dwa integery: początek i koniec przedziału liczbowego,
który zwraca.  Możemy następnie iterować po takim przedziale i wówczas
elementami będą kolejne liczby całkowite:

```python
for liczba in range(10, 20):
    print(liczba)
```

W powyższym przykładzie wypisujemy liczby całkowite od 10 do 19.  Liczba,
którą podaliśmy jako koniec przedziału nie jest w nim uwzględniona.

Co ciekawe, możemy podać tylko jeden argument, który wtedy jest traktowany
jako koniec przedziału, zaś za początek przyjmuje się liczbę 0.  Kolejny
przykład pokazuje jak wypisać liczby od 0 do 99:

```python
for liczba in range(100):
    print(liczba)
```

:snake: Napisz funkcję, która przyjmie jeden argument o nazwie `limit`
i zwróci listę wartości od 0 do `limit` podniesionych do kwadratu.


## :pushpin: Podsumowanie

W tym rozdziale:

* poznaliśmy pojęcia *iteracja* oraz *pętla*,
* nauczyliśmy się korzystać w pętli `for`,
* dowiedzieliśmy się, że pętla `for` działa także na stringach, oraz że
stringi posiadają metodę `split`,
* poznaliśmy funkcję wbudowaną `range`.

# Rozdział 11. Krotki

W tym rozdziale:

* dowiesz się czym jest **krotka**.


## Krotka

Czytając kod programów napisanych w Pythonie bardzo szybko natkniesz się
na coś z pozoru bardzo podobnego do listy:

```python
waluty = ('EUR', 'PLN', 'USD')
```

Powyższy przykład to definicja **krotki**.  Na pierwszy rzut oka różni się
ona od listy tylko na tym, że zamiast nawiasów kwadratowych ma okrągłe.
Jednak krotka posiada jedną istotną cechę, która odróżnia ją od listy:
nie można jej modyfikować.  Oznacza to, że do raz utworzonej krotki nie
można dodawać elementów, usuwać ich, ani nawet zmieniać.  Dlatego też nie
znajdziemy w krotce metod `append` ani `remove`.  Za to z powodzeniem
możemy odnosić się do poszczególnych elementów używając ich indeksów:

```python
>>> waluty[1]
'PLN'
```

Oznacza to, że możemy również iterować po krotce pętlą `for`.  Jeśli zaś
przekażemy krotkę do funkcji `len`, to dostaniemy liczbę jej elementów.

:snake: Napisz funkcję, która jako argument przyjmie krotkę i zwraca
listę, która zawiera dokładnie takie same elementy.


## Zastosowanie krotek

Z pozoru krotka może się wydawać czymś zupełnie zbędnym.  Po co nam taka
lista, której nie można modyfikować?  Otóż w wielu przypadkach potrzebujemy
dokładnie czegoś takiego.  Dobrym przykładem jest właśnie zbiór nazw walut.
Wyobraźmy sobie, że piszemy program do przeliczania wartości pieniężnych
między różnymi walutami.  W naszym programie będą zmieniały się kursy,
ale same waluty będą cały czas takie same.  Dlatego możemy je zdefiniować
w krotce, tym samym chroniąc się przed modyfikacją zbioru walut, co byłoby
niepożądane.  Nawet jeżeli w przyszłości będziemy chcieli dodać kolejną
walutę, łatwiej będzie wydać nową wersję programu niż ryzykować modyfikację
zbioru, który powinien pozostać niezmieniony.

Podobnych przykładów jest więcej i czytając kod różnych programów szybko
przekonasz się, że krotki przydają się częściej niż mogło by się wydawać.


## :pushpin: Podsumowanie

W tym rozdziale:

* dowiedzieliśmy się czym jest krotka i jakie operacje możemy na niej
wykonywać.

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

# Rozdział 12. Prawda i fałsz

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
o dalszym przebiegu naszego programu.  W tym celu używamy **instrukcji
warunkowej** `if`:

```python
if temperatura > 30.0:
    print('Uf jak gorąco!')
```

Struktura tej instrukcji jest bardzo prosta: po słowie `if` wpisujemy
warunek, następnie dwukropek i w kolejnych liniach, po wcięciu, instrukcje,
które zostaną wykonane jeżeli warunek będzie prawdziwy (mówimy: jeżeli
warunek zostanie spełniony).

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


## Prawdziwość obiektów, funkcja `bool`

Warunek nie musi być porównaniem.  Każdy typ obiektu w jakiś sposób
definiuje prawdziwość.  Na przykład pusta lista to fałsz, a lista z co
najmniej jednym jednym elementem to prawda.

Aby przekonać się jaką wartość w rozumieniu logiki reprezentuje dany
obiekt, możemy posłużyć się funkcją zbudowaną `bool`.  Przyjmuje ona jeden
argument - dowolny obiekt - i zwraca jego wartość logiczną: `True` lub
`False`.

```python
>>> bool([])
False
>>> bool([1, 2, 3])
True
```

:snake: Dla każdego z następujących typów odszukaj wartość, dla której
funkcja `bool` zwróci `True` i taką dla której zwróci `False`: string,
krotka, integer, float.

Ponieważ każdy obiekt można rozważać w kategorii "prawdziwości", każdym
obiektem możemy posłużyć się w instrukcji `if`:

```python
if imie and nazwisko and len(haslo) > 5:
    print('Podano prawidłowe dane')
```

:snake: Napisz funkcję, która jako argument przyjmie listę i zwróci `True`
jeżeli wszystkie elementy na tej liście są prawdziwe, albo `False` jeżeli
przynajmniej jeden element nie jest prawdziwy.


## :pushpin: Podsumowanie

W tym rozdziale:

* nauczyliśmy się sprawdzać prawdziwość wyrażeń,
* poznaliśmy intrukcję `if`, która może zmienić przebieg programu gdy
określone wyrażenie jest prawdziwe.

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

# Rozdział 13. Słowniki

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

# Rozdział 14. `None`

W tym rozdziale:

* dowiesz się czym jest **`None`**.


## `None`

W Pythonie istnieje jedna szczególna wartość, która nie reprezentuje
żadnego dotąd poznanego typu: **`None`**.  Nie jest to liczba, string, ani
nic innego co poznasz ucząc się tego języka.  `None` to unikalna wartość,
która reprezentuje osobny typ.  Powstała po to, żeby programista mógł
zdefiniować "nic".  Po co?  Okazuje się, że są sytuacje, w których chcesz
wprost zaznaczyć, że dana operacja nie zwróciła żadnej istotnej informacji.
W takich sytuacjach możesz użyć wartości `None`. Zwróć uwagę, że sam fakt
posłużenia się tą wartością jest na tyle wyjątkowy, że sugeruje, że
zaistniały jakieś szczególne okoliczności.

Przykładem użycia `None` może być dzielenie przez 0.  Jak wiemy, taka
operacja matematyczna jest niedozwolona.  Teraz wyobraźmy sobie, że piszemy
funkję, która przyjmuje jako argumenty dwie liczby i zwraca wynik
dzielenia jednej przez drugą.

```python
def podziel(dzielna, dzielnik):
    return dzielna / dzielnik
```

Co się stanie gdy argument `dzielnik` będzie równy `0`?  Otrzymamy błąd:

```python
>>> podziel(3, 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in podziel
ZeroDivisionError: division by zero
```

Aby temu zapobiec, możemy przed wykonaniem dzielenia sprawdzić wartość
argumentu i w razie potrzeby zwrócić `None`, sygnalizując, że nie możemy
obliczyć wyniku:

```python
def podziel(dzielna, dzielnik):
    if dzielnik == 0:
        return None
    return dzielna / dzielnik
```

Teraz z łatwością możemy rozpoznać kiedy funkcja napotkała niestandardowe
wywołanie:

```python
>>> wynik = podziel(4, 2)
>>> print(wynik)
2.0
>>> wynik = podziel(5, 0)
>>> print(wynik)
None
```


## Domyślna wartość funkcji

Napiszmy prostą funkcję, która przyjmuje argument i wypisuje go na ekran:

```python
def wypisz(obiekt):
    print(obiekt)
```

Wywołanie funkcji spowoduje oczekiwane skutki:

```python
>>> wypisz(123)
123
>>> wypisz('ala ma kota')
ala ma kota
```

Widzimy, że ciało funkcji zostało wykonane, jednak jaka wartość została
zwrócona?  Innymi słowy: co się dzieje, jeżeli nie użyjemy instrukcji
`return`?  Odpowiedź brzmi: funkcja zwróci `None`.

```python
>>> rezultat = wypisz('abc')
abc
>>> print(rezultat)
None
```

Tak samo dzieje się, jeżeli użyjemy instrukcji `return` nie podając jej
żadnej wartości:

```python
def wypisz(obiekt):
    print(obiekt)
    return
```

Efekt będzie taki sam jak wtedy gdy nie użyjemy `return`:

```python
>>> rezultat = wypisz(3.14)
3.14
>>> print(rezultat)
None
```

Za takim zachowaniem nie kryje się żadna magia: po prostu twórcy Pythona
przyjęli, że domyślnie funkcja zwraca "nic", a wartość taka będzie
reprezentowana przez `None`.


## Operator `is`

Skoro wiemy, że funkcje mogą zwracać `None`, to w jaki sposób z tego
skorzystać?  Możemy na przykład sprawdzić zwróconą wartość w instrukcji
`if`:

```python
def imie_nazwisko(imie, nazwisko):
    if imie != '' and nazwisko != '':
        return imie + ' ' + nazwisko

def nazwa_uzytkownika(imie, nazwisko, email):
    pelne_nazwisko = imie_nazwisko(imie, nazwisko)
    if pelne_nazwisko == None:
        return email
    else:
        return pelne_nazwisko
```

W powyższym przykładzie funkcja `nazwa_uzytkownika` zwraca pełną nazwę
użytkownika na podstawie jego imienia, nazwiska i adresu email.  Jeżeli
imię i nazwisko są dane, to zwracane jest pełne nazwisko, w przyciwnym
wypadku zwrócony zostanie tylko adres email.  Sprawdzenie czy pełne
nazwisko jest podane zostało zapisane w instrukcji
`if pelne_nazwisko == None`.

Instrukcja `if zmienna == None` jest poprawna, jednak w ogólnym przypadku
może nie zawsze działać.  Dzieje się tak, ponieważ tworząc bardziej
zaawansowane struktury danych w Pythonie (co nie będzie omówione podczas
tych warsztatów), możemy zmienić zachowanie porównania, w efekcie wpływając
na wynik zwracany przez operator `==`.  Możemy wybrnąć z tej sytuacji
stosując zamiast tego **operator `is`**:

```python
if pelne_nazwisko is None:
    return email
```

W ten sposób nasz kod będzie niewrażliwy na modyfikacje zachowania
operatora `==`.

Kiedy zatem używać `is`?  Używaj tego operatora zawsze kiedy porównujesz
wartość do `None`.  Póki co nie będzie to robiło różnicy, ale dzięki temu
nabędziesz dobrego nawyku, który w przyszłości okaże się przydatny.

:snake: Napisz funkcję, która jako argument przyjmuje listę i zwróci
również listę, na której znajdą się wszystkie elementy z argumentu,
z wyjątkiem wartości równych `None`.


## :pushpin: Podsumowanie

W tym rozdziale:

* poznaliśmy `None`,
* dowiedzieliśmy się, że porównując wartości do `None` należy stosować
operator `is`.

# Rozdział 15. Pętla `while`

W tym rozdziale:

* nauczysz posługiwać się pętlą `while`.


## Pętla `while`

Wiesz już czym jest pętla oraz znasz jedną z nich: `for`.  Teraz poznasz
drugą, jednocześnie ostatnią jaka istnieje w Pythonie: `while`.  Jej
struktura jest jeszcze prostsza od poprzedniej:

```python
licznik = 1
while licznik < 10:
    print(licznik)
    licznik = licznik + 1
```

Definicję pętli zaczynamy słowem `while`, następnie definiujemy warunek,
a po drukropku, w kolejnych linijkach i po wcięciu, wypisujemy instrukcje,
które będą wykonywane tak długo jak warunek będzie prawdziwy.

Zwróć uwagę, że jeżeli zdefiniujemy warunek, który zawsze będzie prawdziwy,
wtedy pętla będzie wykonywana w nieskończoność:

```python
while 1 == 1:
    print('.')
```

:snake: Napisz funkcję, która przyjmie listę jako argument i wypisze
wszystkie jej elementy przy użyciu pętli `while`.

## :pushpin: Podsumowanie

W tym rozdziale:

* poznaliśmy pętlę `while`.

# Rozdział 16. Biblioteka standardowa

W tym rozdziale:

* dowiesz się czym jest **biblioteka standardowa**,
* poznasz najważniejsze **moduły** biblioteki standardowej.


## Biblioteka

W programowaniu posługujemy się pojęciem **biblioteka**, które oznacza
zbiór programów i narzędzi do ich budowania, które możemy wykrzystać
pisząc własne programy.  Przykładem biblioteki może być zbiór funkcji
metematycznych (np. trygonometrycznych), do których możemy odwołać się
w naszym kodzie zamiast definiować je samodzielnie.


## Moduły

W Pythonie biblioteki programistyczne są dostępne poprzez **moduły**.
Moduł to po prostu kod umieszczony na dysku, w miejscu w którym
Python może go odnaleźć.  Może to być kod napisany w Pythonie, ale
są sposoby na pisanie modułów w innych językach programowania.  Python
znajdzie taki kod jeżeli zostanie on umieszczony w jednym z określonych
z góry katalogów.

Każdy może napisać własny moduł do Pythona.  W internecie znajdziemy
tysiące modułów, które różne osoby i firmy udostępniają.  Możemy je pobrać
i używać ich do pisania programów.  Możemy też tworzyć własne moduły
i dzielić się nimi z innymi użytkownikami.

Aby skorzystać z modułu musimy **zaimportować** jego nazwę.  Robimy to
instrukcją `import`.  Gdy moduł jest już zaimportowany, możemy używać
funkcji i zmiennych, które zostały w nim zdefiniowane.  Robimy to wpisując
nazwę modułu, a następnie, po kropce, nazwę obiektu.

W poniższym przykładzie importujemy moduł o nazwie `math` i wywołujemy
funkcję `sqrt`, która zwraca pierwiastek kwadratowy z podanej liczby:

```python
import math
print(math.sqrt(9))
```

## Biblioteka standardowa Pythona

Poza modułami, które użytkownicy sami mogą pisać, istnieje zbiór modułów,
który zawsze jest dostępny w Pythonie. Ten zbiór nazywamy **biblioteką
standardową**.  Znajdziemy w nim dziesiątki modułów, a w nich narzędzia
do komunikacji sieciowej, obsługi różnych formatów plików, obliczeń
matematycznych etc.

Biblioteka standardowa jest obszernie udokumentowana na [oficjalnej
stronie Pythona](https://docs.python.org/3/library/index.html).


## Najważniejsze moduły

Omówienie całej biblioteki standardowej to zadanie na co najmniej kilka
tygodni, dlatego podczas tych warsztatów wspomnimy tylko o kilku
najbardziej popularnych modułach.


### [`math`](https://docs.python.org/3/library/math.html)

Moduł `math` zawiera kilkadziesiąt funkcji matematycznych, które mogą
okazać się pomocne przy prostych obliczeniach.  Poniżej opisaliśmy kilka
z nich.

Funkcje `ceil` i `floor` zwracają wartości zaokrąglone odpowiednio
w dół i w górę:

```python
>>> math.ceil(3.5)
4
>>> math.floor(3.5)
3
```

Funkcja `sqrt` zwraca pierwiastek kwadratowy z danej liczby:

```python
>>> math.sqrt(25)
5.0
```

`pi` oraz `e` reprezentują wartości stałych matematycznych:

```python
>>> math.pi
3.141592653589793
>>> math.e
2.718281828459045
```

:snake: Napisz funkcję, która zwróci wartość pola powierzchni koła
o zadanym promieniu (według wzoru `PI * r^2`, gdzie `r` to promień).


### [`datetime`](https://docs.python.org/3/library/datetime.html)

Moduł `datetime` to podstawowe narzędzie do pracy z datami i czasem.
Zawiera obiekty `date`, `datetime` oraz `timedelta`, które reprezentują
odpowiednio datę, datę i czas oraz różnicę w czasie.

Aby otrzymać dzisiejszą datę należy wywołać metodę `today` na obiekcie
`date`:

```python
>>> datetime.date.today()
datetime.date(2017, 8, 13)
```

Otrzymany w ten sposób obiekt zawiera trzy **atrybuty**: `year`, `month`
oraz `day`, czyli odpowiednio rok, miesiąc i dzień.

```python
>>> dzisiaj = datetime.date.today()
>>> dzisiaj.year
2017
>>> dzisiaj.month
8
>>> dzisiaj.day
13
```

Metoda `now` na obiekcie `datetime` zwróci nam datę i godzinę, którą mamy
w tej chwili.  Poza atrybutami `year`, `month` oraz `day` posiada także
`hour`, `minute`, `second` i `microsecond`, czyli godzinę, minutę, sekundę
i mikrosekundę.

```python
>>> teraz = datetime.datetime.now()
>>> teraz
datetime.datetime(2017, 8, 13, 18, 53, 13, 366193)
>>> teraz.hour
18
>>> teraz.minute
53
>>> teraz.second
13
>>> teraz.microsecond
366193
```

Oba typy obiektów możemy wypisać na ekran w czytelnym formacie:

```python
>>> print(dzisiaj)
2017-08-13
>>> print(teraz)
2017-08-13 18:53:13.366193
```

Chcąc utworzyć reprezentację dowolnego momentu w czasie, wystarczy
wywołać `date` lub `datetime` i podać kolejno `year`, `month`, `day`,
`hour`, `minute`, `second`, `microsecond`:

```python
>>> print(datetime.date(2010, 5, 10))
2010-05-10
>>> print(datetime.datetime(2020, 11, 23, 15, 7, 30))
2020-11-23 15:07:30
```

:snake: Zobacz co się stanie jeżeli spróbujesz utworzyć obiekt `date`
z miesiącem spoza zakresu od 1 do 12 lub datę, która nie istnieje, np.
31 kwietnia.

:snake: Zobacz co się stanie jeżeli spróbujesz utworzyć obiekt `datetime`
z godziną, minutą lub sekundą o wartosci spoza dopuszczalnego zakresu
(np. godzina 26).

Jeżeli chcemy zobaczyć różnicę w czasie między dwoma obiektami typu
`datetime`, możemy je po prostu odjąć od siebie:

```python
>>> a = datetime.datetime(2017, 8, 16, 17, 00)
>>> b = datetime.datetime(2017, 8, 16, 19, 00)
>>> roznica = b - a
>>> roznica
datetime.timedelta(0, 7200)
>>> roznica.seconds
7200
```

W powyższym przykładzie otrzymaliśmy obiekt `timedelta`, który posiada
atrybut `seconds` o wartości równej liczbie sekund pomiędzy `a` i `b`.

Jeżeli różnica jest większa niż jedna doba, to zostanie ona podzielona
na dwie wartości: `seconds` i `days`, czyli sekundy i dni.

```python
>>> c = datetime.datetime(2017, 8, 16, 17, 00)
>>> d = datetime.datetime(2017, 8, 18, 15, 00)
>>> roznica = d - c
>>> roznica.seconds
79200
>>> roznica.days
1
```

Jeżeli do daty `c` dodamy jeden dzień i 79200 sekund, to otrzymamy `d`.

:snake: Napisz funkcję, która przyjmuje dwie daty jako argumenty.
Jeżeli druga data jest mniejsza od pierwszej, funkcja powinna zwrócić
`None`.  W przeciwnym wypadku funkcja powinna zwrócić liczbę sekund
dzielącą obie daty.  Zwróć uwagę, że różnica może być większa niż jedna
doba.  W takim wypadku liczbę dni należy zamienić na sekundy.


### [`random`](https://docs.python.org/3/library/random.html)

Moduł `random` służy do wykonywania operacji, których wynik jest losowy:
generowania liczb losowych, losowego wybierania obiektów z danego zakresu,
itd.

Funkcja `randint` przyjmuje dwa integery jako argumenty i zwraca losowo
wybraną liczbę całkowitą, której wartość znajduje się pomiędzy argumentami.

```python
>>> random.randint(1, 100)
9
>>> random.randint(1, 100)
44
```

Funkcja `choice` przyjmuje jako argument dowolną sekwencję (listę, krotkę,
string) i zwraca losowo wybrany element:

```python
>>> random.choice('ala ma kota')
'm'
>>> random.choice([9, 7, 5, 3])
7
>>> random.choice(('pycon', 'pl', '2017'))
'pl'
```

:snake: Napisz funkcję, która przyjmie jako argument dowolną sekwencję
i zwróci *krotkę* z trzema losowo wybramymi z niej elementami.


### [`json`](https://docs.python.org/3/library/json.html)

Moduł `json` pozwala zapisywać obiekty Pythona (słowniki i listy) jako
string w formacie JSON (*JavaScript Object Notation*), który jest
powszechnie używany np. w serwisach internetowych do wymiany danych między
przeglądarką a serwerem.

Żeby zapisać obiekt do stringa należy wywołać funkcję `dumps`:

```python
>>> json.dumps({'miejsce': 'Ossa', 'data': '2017-08-16'})
'{"miejsce": "Ossa", "data": "2017-08-16"}'
>>> json.dumps([2017, 8, 16])
'[2017, 8, 16]'
```

Do zamiany stringa na słownik lub listę służy funkcja `loads`:

```python
>>> json.loads('{"miejsce": "Ossa", "data": "2017-08-16"}')
{'miejsce': 'Ossa', 'data': '2017-08-16'}
>>> json.loads('[2017, 8, 16]')
[2017, 8, 16]
```

## Co dalej?

Wyżej wymieniliśmy tylko kilka najbardziej popularnych modułów, więc
zachęcamy do zapoznania się z resztą biblioteki standardowej.  Warto
zacząć od oficjalnej dokumentacji, ale w internecie znajdziemy mnóstwo
artykułów poświęconych stosowaniu biblioteki standardowej na co dzień.
Oczywiście nie trzeba znać jej w całości żeby swobodnie programować
w Pythonie.  Wiele z tych modułów ma bardzo specyficzne zastosowania
i większość programistów nigdy z nich nie korzysta.  Warto natomiast
pamiętać, że jeżeli trafisz na jakiś nowy problem, to dobrze jest najpierw
przejrzeć bibliotekę standardową w poszukiwaniu modułu, który może okazać
się pomocny.


## :pushpin: Podsumowanie

W tym rozdziale:

* dowiedzieliśmy się czym jest **biblioteka standardowa** i jak z niej
korzystać,
* poznaliśmy moduły `math`, `datetime`, `random` i `json`.


---


# Podsumowanie

Dobiegamy do końca kursu, ale to jeszcze nie koniec warsztatów!  Mentorzy
mają dla Ciebie jeszcze garść zadań.  Możesz też skorzystać z okazji
i zadać mentorom tyle pytań na ile tylko starczy czasu - między innymi
dlatego zorganizowaliśmy te warsztaty!


## O czym nie powiedzieliśmy

Niestety czas na warsztaty jest organiczony, więc i zakres tematów jakie
poruszyliśmy nie jest wyczerpujący.  Znasz już podstawy Pythona.  Możesz
już samodzielnie pisać programy, a czytanie cudzych nie będzie już takie
trudne.  Jednak na tym etapie często trafisz na kod, którego nie
zrozumiesz.  A może już teraz wiesz o tematach, które wydają się
interesujące, ale nie wiesz jak zacząć.  Dlatego przygotowaliśmy dla Ciebie
listę zagadnień, którą możesz potraktować jako kontynuację tych warsztatów.
Nie jest to wyczerpująca lista tematów, ale na pewno pomoże Ci jeszcze
lepiej poznać Pythona.  W każdym punkcie umieściliśmy odnośnik do strony,
która wyjaśnia dany temat.

* [Jeszcze więcej o wyjątkach i obsługiwaniu ich](https://docs.python.org/3.6/tutorial/errors.html)
* [Klasy, czyli programowanie zorientowane obiektowo](https://docs.python.org/3.6/tutorial/classes.html)
* [Dekoratory](https://docs.python.org/3/glossary.html#term-decorator)
* [Generatory](https://docs.python.org/3/glossary.html#index-17)
* [Listy składane](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
* [Zbiory](https://docs.python.org/3/tutorial/datastructures.html#sets)


## Na koniec... `dir`

Kończąc pokażemy Ci jeszcze jedną, bardzo przydatną funkcję wbudowaną.
Nazywa się `dir`, przyjmuje jako argument dowolny obiekt i zwraca listę
nazw wszystkich metod i atrybutów tego obiektu:

```python
>>> d = {'a': 1}
>>> dir(d)
['__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
```

W powyższym przykładzie rozpoznasz na pewno kilka znajomych nazw, np.
`items` czy `values`, ale jak widzisz słowniki oferują znacznie więcej.
Zwróć uwagę na nazwy zaczynające i kończące się podwójnym znakiem
podkreślenia.  W taki sposób są nazywane atrybuty i metody, które nie są
przeznaczone dla użytkowników obiektu.  Zazwyczaj są to rzeczy używane
tylko wewnątrz danego obiektu.  Oczywiście tak czy inaczej można z nich
korzystać - po prostu zazwyczaj nie będą dla nas przydatne, więc warto
zainteresować się pozostałymi nazwami.

Co teraz zrobić z taką listą?  Jeżeli jakaś nazwa wydaje się oczywista,
możemy po prostu spróbować jej użyć - w najgorszym wypadku otrzymamy
komunikat o błędzie wyjaśniający co zrobiliśmy źle.  Możemy też - i to
polecamy - użyć funkcji `help`, która wyświetli dokumentację danego
obiektu:

```python
help(d.update)
```



Dziękujemy za udział w warsztatach!  Jeszcze raz zachęcamy do rozmowy
z mentorami - chętnie odpowiedzą na wszystkie pytania i wyjaśnią
niezrozumiałe tematy.

Jeżeli masz uwagi do tego kursu, podziel się nimi pisząc do autorów,
albo przekaż je mentorom.  Twoje zdanie jest dla nas bardzo ważne!

![programming is fun again](https://imgs.xkcd.com/comics/python.png)
# Warsztaty PyLadies / PyCon PL 2017

Witaj na warsztatach PyLadies! Podczas tego kursu nauczysz się programować
w języku **Python** od podstaw. Aby zacząć nie potrzebujesz nic instalować,
nie jest wymagana żadna znajomość programowania czy informatyki. Wystarczy
przeglądarka internetowa i chęć zdobywania wiedzy!


## Czego uczą te warsztaty

Ten kurs nauczy Cię tworzyć własne programy w Pythonie. Poznasz podstawy
tego języka, oraz dowiesz się jak w przyszłości poszerzyć wiedzę, aby
samodzielnie tworzyć coraz ciekawsze rzeczy. Dzięki tym warsztatom
zrozumiesz Pythona na poziomie, który pozwoli Ci pisać przydatne narzędzia
oraz zgłębiać bardziej zaawansowane aspekty tego języka.

Podsumowując: Twoja przygoda z programowaniem zaczyna się właśnie tutaj!


## Legenda

Zanim zaczniemy, zapoznaj się z oznaczeniami, które zostały użyte na
kolejnych stronach kursu.

:snake: oznacza miejsce, w którym dajemy Ci do wykonania jakieś zadanie.
Jeżeli instrukcje nie są jasne, lub zadanie sprawia Ci kłopoty - poproś
o pomoc mentora.

:pushpin: to podsumowanie rozdziału. Zanim przejdziesz dalej, upewnij się,
że rozumiesz wszystkie wymienione tam tematy. Jeśli masz jakiekolwiek
wątpliwości - zapytaj mentora. Nie sugeruj się innymi - właśnie po to
robimy podsumowanie, żeby upewnić się, że każdy zrozumiał dany rozdział.

**Pogrubionym tekstem** wyróżniliśmy istotne słowa i zwroty. Warto je
zapamiętać, aby łatwiej przyswoić kolejne rozdziały.

`W taki sposób` oznaczyliśmy przykładowy kod programów.


## Mentorzy

Nasz zespół mentorów jest tutaj dla Ciebie! Jeżeli masz pytania, cokolwiek
jest niejasne albo nie wiesz jak wykonać jakieś zadanie - poproś kogoś
z nas o pomoc. Chętnie odpowiemy, opowiemy i pomożemy Ci zrozumieć każdy
temat. Nie krępuj się: my równeż kiedyś zadawaliśmy pytania i właśnie
dzięki temu sami możemy teraz na nie odpowiadać.


## Spis treści

1. [Tryb interaktywny](./01_tryb_interaktywny.md)
2. [Tekst](./02_tekst.md)
3. [Funkcja `help`](./03_help.md)
4. [Liczby](./04_liczby.md)
5. [Błędy](./05_bledy.md)
6. [Zmienne](./06_zmienne.md)
7. [Funkcje](./07_funkcje.md)
8. [Funkcja `print`](./08_funkcja_print.md)
9. [Listy](./09_listy.md)
10. [Pętla `for`](./10_for.md)
11. [Krotki](./11_krotki.md)
12. [Prawda i fałsz](./12_prawda_i_falsz.md)
13. [Słowniki](./13_slowniki.md)
14. [`None`](./14_none.md)
15. [Pętla `while`](./15_petla_while.md)
16. [Biblioteka standardowa](./16_biblioteka_standardowa.md)
17. [Podsumowanie](./17_podsumowanie.md)


## Bibliografia

1. https://pl.wikipedia.org/wiki/Unikod
2. https://docs.python.org/3/library/functions.html
