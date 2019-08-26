# Streszczenie

Artykuł opisuje nowości, jakie przynosi Python w wersji 3.8, kładąc szczególny
nacisk na konsekwencje wprowadzenia operatora przypisania, który to stał się
kością niezgody wewnątrz pythonowej społeczności. Postaram się też spojrzeć
na rozwój Pythona w szerszej perspektywie i zastanowić się nad jego
bliższą oraz dalszą przyszłością.

# Wprowadzenie

Python nieustannie zmienia się i ewoluuje - przez ponad ćwierć wieku istnienia,
przeobraził się nie do poznania, dojrzał i ogromnie się rozwinął.
Zaczynał jako niszowa alternatywa do skryptów powłoki, dziś jest
popularnym i wszechstronnym językiem ogólnego przeznaczenia o szerokim
wachlarzu zastosowań.

Drogę tę przebył głównie dzięki mądrym decyzjom społeczności pod przewodnictwem
Guido von Rossuma, społeczności która czuwała, by rozwój Pythona odbywał się zawsze we
właściwym kierunku.

I wtedy, gdy wszystko szło tak dobrze, pojawił się PEP 572 - czyli złowrogi
operator przypisania, który podzielił społeczność do tego stopnia, że sam
Ojciec Założyciel postanowił zejść z tronu i zrzekł się swojej funkcji BDFL
(_Benevolent Dictotor For Life_), pozostawiając swoje dziecko oraz społeczność
samym sobie.

Od tego czasu minął już rok, a na dniach wydany zostanie Python 3.8, w którym
premierę będzie miał operator przypisania. Jaka przyszłość czeka osieroconego
Pythona? Czy jest to punkt zwrotny w życiu naszego ulubionego języka? Czy
społeczność poradzi sobie z brzemieniem odpowiedzialności? Na żadne z
powyższych pytań nie odpowiem w niniejszym artykule, ale postaram się
przedstawić kilka faktów i spekulacji związanych z najnowszym Pythonem.

# Kość niezgody, czyli PEP 572

Operator przypisania `:=` (_walrus operator_, ang. _walrus_ = mors) ma na celu
uproszczenie kodu przez umożliwienie przypisywania wartości do zmiennych
wewnątrz wyrażeń.
Istnieje on w wielu językach, choćby w tych C-podobnych, gdzie niewątpliwie
wyrządził wiele szkód. Wersja pythonowa ma być bezpieczniejsza, gdyż używa
dedykowanego symbolu (`:=`), odróżniającego operator od instrukcji przypisania
(`=`), ponadto dość mocno ograniczone są miejsca, gdzie operator może być on użyty.

Oto kilka przykładów zastosowania operatora przypisania zaczerpniętych z PEP 572:

```python
# Obsługa wyrażeń regularnych
if (match := pattern.search(data)) is not None:
    x = match.group(1)

# Pętla trudna do napisania w inny sposób
while chunk := file.read(8192):
   process(chunk)

# Ponowne wykorzystanie kosztownych obliczeń
[y := f(x), y**2, y**3]

# Współdzielenie wyrażenia w filtrze i w rezultacie dopełnienia
filtered_data = [y for x in data if (y := f(x)) is not None]
```

Wygląda to ładnie i zgrabnie, ale największymi kontrowersjami związanymi z
"morsem" są możliwość niewłaściwego użycia i potencjalne zaciemnienie kodu.
Przyjrzyjmy się więc mniej ładnym przykładom:

```python
(x := 1)  # Nawias wymagany, równoważne z: x = 1
(x = (y := (z := 1)))  # Ekwiwalent: x = y = z = 1
(x := 1, 2)  # Wartość x wynosi 1, ':=' ma wyższy priorytet, niż ','
(x := (1, 2))  # Tym razem x = (1, 2)
f(p=(x := 1))  # To proste: x = 1; f(p=x)
(a.b := 1)  # Nie działa
(a[1] := 1)  # Też nie działa
```

Jak widać, kod nie zawsze zyskuje na czytelności, a funkcjonowanie nowego operatora potrafi
czasem zaskakiwać i niewątpliwie wprowadzi do języka nową kategorię trudnych do wyłapania
błędów.
Dodatkową kwestią jest fakt, że zmienne są definiowane w nadrzędnej przestrzeni
nazw, prowadząc do jej zaśmiecenia, co może prowadzić na przykład do
niezamierzonego nadpisania wartości zmiennej.
Ponadto, pojawiła się alternatywna składnia, częściowo duplikująca już
istniejącą funkcjonalność, co jest jawnie sprzeczne z przykazaniami Zen
Pythona.

Z drugiej strony czasem nasz "mors" potrafi drastycznie zwiększyć czytelność
kodu przez likwidację sztucznych zagnieżdżeń.
Oto przykład z biblioteki standardowej, z pliku `copy.py`. Wersja "tradycyjna":

```python
reductor = dispatch_table.get(cls)
if reductor:
    rv = reductor(x)
else:
    reductor = getattr(x, "__reduce_ex__", None)
    if reductor:
        rv = reductor(4)
    else:
        reductor = getattr(x, "__reduce__", None)
        if reductor:
            rv = reductor()
        else:
            raise Error(
                "un(deep)copyable object of type %s" % cls)
```

Oraz wersja usprawniona dzięki operatorowi przypisania:

```python
if reductor := dispatch_table.get(cls):
    rv = reductor(x)
elif reductor := getattr(x, "__reduce_ex__", None):
    rv = reductor(4)
elif reductor := getattr(x, "__reduce__", None):
    rv = reductor()
else:
    raise Error("un(deep)copyable object of type %s" % cls)
```

Czy Python potrzebował PEP 572? Trudno powiedzieć, ale na pewno konsekwencje
wojny wokół tego dokumentu są bardzo poważne i wpłyną długofalowo na przyszłość
języka.

# Co ponadto w wersji 3.8?

Nowy Python, to nie tylko PEP 572 - mamy szereg zmian, zarówno w samym języku,
jak i w bibliotece standardowej. Poniżej pokrótce omówię niektóre z nich.

## Argumenty wyłącznie pozycyjne

Moduły Pythona napisane w C już od dawna mają możliwość wymuszenia użycia
argumentów funkcji wyłącznie przez ich nazwę, jak i wyłącznie pozycyjnych.
Dla modułów napisanych w Pythonie te możliwości były ograniczone i nieraz
zmuszały twórców bibliotek do manualnej weryfikacji już w ciele funkcji.

W Pythonie 3.0 pojawiła się możliwość deklaracji parametrów wyłącznie
nazwanych przez wstawienie `*` do listy argumentów - wszystkie parametry
po prawej stronie gwiazdki wymagały podania ich nazwy przy wywołaniu.
Oto przykład:

```python
def f(a, b, *, c):
    pass

f(1, 2, c=3)  # OK
f(a=1, b=2, c=3)  # OK
f(1, 2, 3)  # BŁĄD!
```

Jednakże wszystkie agrumenty przed `*` mogły być użyte zarówno pozycyjnie, jak
i przez nazwę, co nie zawsze było zachowaniem pożądanym. Dlatego PEP 570
wprowadza nowy symbol `/` w liście argumentów, oddzielający parametry
wyłącznie pozycyjne (po jego lewej) od tych pozycyjno/nazwanych (po prawej).
Tak więc w Pythonie 3.8 możemy już napisać:


```python
def f(a, /, b, *, c):
    pass

f(1, 2, c=3)  # OK
f(a=1, b=2, c=3)  # BŁĄD!
f(1, 2, 3)  # BŁĄD!
```

Co więcej, zapis używający `*` i `/` pojawia się już od jakiegoś czasu w
dokumentacji samego Pythona, jak i w niektórych bibliotekach (`numpy`).
Spójrzmy co nam powie `help()` dla paru funkcji wbudowanych.
Rozszyfrowanie zapisu nie powinno stanowić trudności dla uważnego czytelnika:

```python
>>> help(len)
len(obj, /)
...
>>> help(sorted)
sorted(iterable, /, *, key=None, reverse=False):
...
```

## Równoległy cache dla skompilowanych plików

Kolejnym miłym usprawnieniem w Pythonie 3.8 jest możliwość wyrzucenia
skompilowanych plików (`__pycache__`) z katalogów kodu źródłowego.
Służy do tego nowa zmienna środowiskowa `PYTHONPYCACHEPREFIX` i parametr
wiersza poleceń `-X pycache_prefix`.

## Znak `=` w łańcuchach formatujących

Nowy modyfikator f-łańcuchów produkuje zapis w postaci `nazwa=wartość` i może
oszczędzić nieco czasu programistom:

```python
>>> a = 1
>>> f"{a=}"  # Samoopisująca się wartość
'a=1'
>>> f"{(mors:=1)=}"  # O to też zadbano
'(mors:=1)=1'
```

## Pickle - protokół w wersji 5

W nowej wersji protokołu wprowadzono wsparcie dla zewnętrznych buforów
(ang. _out-of-band_), pomocnych przy przetwarzaniu wielordzeniowym i
wielomaszynowym. Umożliwia ono optymalizację przesyłu danych przez eliminację
niepotrzebnych kopii danych w pamięci, a także daje możliwość zastosowania
specjalizowanych algorytmów kompresji.

## Pozostałe zmiany

Poza tym, co widoczne, mamy do czynienia ze szeregiem zmian niezauważalnych
dla przeciętnego użytkownika (PEP 578, PEP 587, PEP 590), drobnych poprawek
składni, małych, ewolucyjnych zmian w bibliotekach oraz mnóstwem optymalizacji.

# Python 3.8 - hit, czy shit?

Czy operator przypisania zmieni wiele w Pythonie? Prawdopodobnie nie,
największa zmiana z nim związana już się dokonała, kiedy to zaszczuty Guido
postanowił usunąć się w cień. Czy będę używać nowego operatora? Oczywiście,
że tak! My programiści jesteśmy z natury leniwi, więc każda zaoszczędzona
linijka to czysty zysk.

Poza nieszczęsnym "morsem", wersja 3.8 nie wprowadza żadnych rewolucyjnych
zmian, wpisując się w przemyślany i stabilny schemat rozwoju Pythona.
Wszystkie wdrożone modyfikacje idą ku większej prostocie, spójności i
szybkości języka. Dlatego też jestem spokojny o przyszłość naszego ulubionego
cyfrowego gada.

# Żródła

* <https://docs.python.org/3.8/whatsnew/3.8.html> Co nowego w Pythonie 3.8
* <https://www.python.org/dev/peps/pep-0572/> PEP 572 - Assignment Expressions
* <https://www.python.org/dev/peps/pep-0570/> PEP 570 - Python Positional-Only Parameters
* <https://www.python.org/dev/peps/pep-0574/> PEP 574 - Pickle protocol 5 with out-of-band data
* <https://www.mail-archive.com/python-committers@python.org/msg05628.html> \[python-committers\] Transfer of power
