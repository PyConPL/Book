# Co tam, panie, w polityce? Czyli czym zaskoczył nas Python 3.4
## Marcin Bardź

Python w wersji 3.4 światło dzienne ujrzał 16 marca 2014. To wydanie nie wprowadza
żadnych zmian do samego języka, zamiast tego mamy kilka nowych bibliotek,
usprawnienia w już istniejących modułach oraz wiele ulepszeń "pod maską".

Ta pozorna stagnacja w rozwoju języka została zaplanowana oraz wprowadzona
w życie z pełną premedytacją (PEP 3003 o złowróżebnym tytule *Python Language Moratorium*)
i ma ona na celu umożliwienie "dogonienia" bazowej implementacji (CPython) przez inne
implementacje języka, takie jak Jython czy PyPy.

Brak zmian w składni nie oznacza jednak, że przeciętny pythonista nie dostanie
do rąk nowych zabawek, ciekawych narzędzi, a jego życie nie stanie się jeszcze
prostsze.

### Nowe biblioteki

Najnowsza odsłona naszego ulubionego gada raczy nas pokaźną baterią całkiem
nowych bibliotek, wśród których każdy użytkownik powinien znaleźć coś dla siebie.

#### `asyncio`

Potężna biblioteka umożliwiająca tworzenie kodu współbieżnego, przełączany
dostęp do zasobów we/wy, uruchamianie klientów/serwerów sieciowych, a to
wszystko w jednym jedynym wątku! Dla osób znających Twisted nie będzie to
nic nowego, mimo to wprowadzenie tak potężnego narzędzia do biblioteki
standardowej otwiera wiele nowych możliwości.

Szczegółowy opis biblioteki wykracza daleko poza ramy niniejszego
artykułu, dlatego wymienię tylko główne różnice pomiędzy Twisted i `asyncio`:

* `asyncio` jest prostsze i składa się z mniejszej liczby modułów. Z jednej strony
  `asyncio` nie ma wszystkich możliwości Twisted, z drugiej jednak powinno być łatwiejsze
  w użyciu i nowy użytkownik powinien móc się szybciej wdrożyć (korzystniejsza krzywa uczenia się).
* Dokumentacja `asyncio` jest przejrzysta i ułożona w sposób intuicyjny dla
  przeciętnego programisty Pythona.
* `asyncio` wspiera najnowsze wersje Pythona i potrafi wykorzystać jego
  dobrodziejstwa (np. składnię `yield from`).

#### `ensurepip`

Zaczęło się od PEP 453, który namaścił `pip` jako rekomendowane narzędzie
zarządzania bibliotekami. Gdy już PEP został zaakceptowany, należało się
więc upewnić, że użytkownik będzie miał dostęp do tego błogosławionego narzędzia.

Zasadniczo, standardowa instalacja Pythona powinna zawierać `pip` w wersji,
która była najnowszą w momencie pojawenia się RC danego wydania. Jeśli
jednak `pip` by się nam gdzieś zapodział (np. w wirtualnym środowisku), wystarczy wywołać z linii polecń:

    $ python -m ensurepip

I już mamy pewność, że `pip` jest dostępny. Co ciekawe, żeby wykonać powyższą
komendę, nie jest potrzebny dostęp do internetu, gdyż `ensurepip` przechowuje
na swoje potrzeby lokalną kopię biblioteki `pip`.

Przeciętny użytkownik może nie musieć w ogóle igrać z modułem `ensurepip`, a cały ten
cyrk wynika z faktu, że `pip` jest niezależnym projektem, posiadającym własny
cykl wydawniczy.

#### `enum`

Po wielu latach i po wielu niezależnych implementacjach, Python doczekał się
w końcu swoich własnych typów wyliczeniowych. Dzięki nim można teraz pisać
elegancki i mniej podatny na błędy kod.

W myśl zasady, że jedna linijka kodu znaczy więcej, niż tysiąc słów,
przedstawiam poniżej próbkę możliwości modułu:

	>>> from enum import Enum
	>>> class Osoba(Enum):
	...     ja = 1
	...     ty = 2
	...     on_ona_ono = 3
	...     ona = 3
	...     ono = 3
	... 
	>>> Osoby = Enum('Osoby', 'my wy oni_one', module=__name__)
	>>> być = {
	...     Osoba.ja: "jestem",
	...     Osoba.ty: "jesteś",
	...     Osoba.on_ona_ono: "jest",
	...     Osoby.my: "jesteśmy",
	...     Osoby.wy: "jesteście",
	...     Osoby.oni_one: "są"
	... }
	>>> for lp, lmn in zip(Osoba, Osoby):
	...     poj = "{}. {} {}".format(lp.value, lp.name, być[lp])
	...     mn = "{}. {} {}".format(lmn.value, lmn.name, być[lmn])
	...     print("{:20}{:20}".format(poj, mn))
	... 
	1. ja jestem        1. my jesteśmy
	2. ty jesteś        2. wy jesteście
	3. on_ona_ono jest  3. oni_one są
	>>> print("Myślę, więc %s" % być[Osoba.ja])
	Myślę, więc jestem
	>>> print(Osoba(3))
	Osoba.on_ona_ono
	>>> print(Osoba.ono)
	Osoba.on_ona_ono
	>>> Osoby['oni_one']
	<Osoby.oni_one: 3>


#### `pathlib`

Kolejna obszerna biblioteka, przenosząca operacje na ścieżkach i plikach z prehistorii
do świata programowania obiektowego. Moduł łączy w sobie funkcjonalności `os.path`,
`glob` oraz wielu funkcji z innych bibliotek (głównie `os`), opakowując wszystko w przepyszną
obiektową otoczkę.

Klasy biblioteki podzielone są na dwie odrębne części:

* Czyste ścieżki (*pure paths*) - umożliwiające operacje na samych ścieżkach.
* Konkretne ścieżki (*concrete paths*) - dodające jeszcze operacje we/wy.

Ponadto, moduł udostępnia dwa warianty klas, jeden dla systemów POSIXowych i
jeden dla ścieżek Windowsowych, ale zwykły zjadacz chleba do szczęścia
potrzebuje tylko jednej klasy `Path`, która reprezentuje konkretną ścieżkę
zgodną z aktualnym systemem operacyjnym.

Czasy poszukiwań potrzebnych funkcji plikowych odchodzą w niepamięć, gdyż
użycie `pathlib` jest tak wygodne i intuicyjne, że aż trudno uwierzyć, że
to cudeńko pojawiło się w bibliotece standardowej dopiero teraz.

Oto kilka przykładów użycia `pathlib`:


	>>> from pathlib import Path
	>>> p = Path('/')
	>>> p.is_dir()
	True
	>>> q = p / 'etc' / 'resolv.conf'
	>>> q
	PosixPath('/etc/resolv.conf')
	>>> q.exists()
	True
	>>> q.owner()
	'root'
	>>> with q.open() as f:
	...     print(f.readline())
	... 
	#

	>>> q.parts
	('/', 'etc', 'resolv.conf')
	>>> q.parents[1]
	PosixPath('/')
	>>> q.parents[2]
	Traceback (most recent call last):
	...
    raise IndexError(idx)
	IndexError: 2
	>>> q.name
	'resolv.conf'
	>>> q.suffix
	'.conf'
	>>> q.relative_to('/home')
	Traceback (most recent call last):
	...
	ValueError: '/etc/resolv.conf' does not start with '/home'
	>>> list(q.parent.glob('a*.conf'))
	[PosixPath('/etc/asl.conf'), PosixPath('/etc/autofs.conf')]


#### `selectors`

Moduł ten udostępnia wysokopoziomowe mechanizmy przełączania we/wy. Jest to
abstrakcyjny i w pełni obiektowy, a co za tym idzie łatwiejszy w użyciu odpowiednik
niskopoziomowej biblioteki `select`.

Trik z parą modułów służących do realizacji tego samego zadania nie
jest niczym nowym w Pythonie, zastosowano go już wcześniej do obsługi
wielowątkowości (niskopoziomowy `_thread` i wysokopoziomowy `threading`).

Programista otrzymuje do ręki (między innymi) klasę `DefaultSelector`, która
jest abstrakcją najbardziej efektywnej implementacji selektora dla danej
platformy, a dzięki wspólnej klasie bazowej `BaseSelector`, dostępny
jest jednolity interfejs obsługi, co przekłada się na czytelny, niezależny
od platformy kod, bez niepotrzebnych klauzul `if`.

#### `statistics`

Tym modułem twórcy Pythona starają się uszczęśliwić statystyków, księgowych,
maklerów oraz wszystkich pozostałych im podobnych. Znajdziemy tu funkcje liczące
średnią, medianę, odchylenie standardowe i kilka innych tajemniczych rzeczy
pokroju wariancji.

Wśród wszystkich tych funkcji, na szczególną uwagę zasługuje `mode()`,
wyszukująca najczęściej występujący element w dyskretnym zbiorze danych (lub
rzucająca wyjątkiem `StatisticsError`, jeśli takiego elementu nie ma).
Funkcja `mode()` bywa przydatna nie tylko księgowym i może czasem
zaoszczędzić kilka linijek kodu.

Moduł zapewne będzie się jeszcze rozwijał, obrastając w nowe funkcje, gdyż na
chwilę obecną zawiera tylko niewielki wycinek tego, co dla dobra ludzkości
wymyślili statystycy.

#### `tracemalloc`

Ostatnia na liście, ale zdecydowanie warta uwagi biblioteka, która pozwala na tworzenie
migawek (*snapshot*) alokowanych bloków pamięci oraz przetwarzanie ich na różne sposoby.

Moduł udostępnia trzy rodzaje informacji:

* Traceback miejsca alokacji obiektu.
* Statystyki przydzielonej pamięci (dla pliku, dla linii kodu).
* Porównywanie migawek w celu wykrycia wycieków.

Poniższy plik (nazwałem go `t.py`) pokazuje przykładowe użycie niektórych
funkcji biblioteki:


	01  import tracemalloc
	02
	03  tracemalloc.start()
	04
	05  a = 'A'*1000000
	06  b = 'ź'*1000000
	07  c = list(range(1000000))
	08  d = set(range(1000000))
	09  e = {_: None for _ in range(1000000)}
	10
	11  snap = tracemalloc.take_snapshot()
	12  top = snap.statistics('lineno')
	13  for stat in top[:5]:
	14      print(stat)
	15
	16  f = list(range(1000000))
	17  g = c + f
	18
	19  snap2 = tracemalloc.take_snapshot()
	20  top2 = snap2.compare_to(snap, 'lineno')
	21  print()
	22  for stat in top2[:2]:
	23      print(stat)


A tak wygląda efekt uruchomienia powyższego pliku:


	$ python3.4 t.py
	t.py:9: size=74.7 MiB, count=999744, average=78 B
	t.py:8: size=58.7 MiB, count=999745, average=62 B
	t.py:7: size=35.3 MiB, count=999746, average=37 B
	t.py:6: size=1953 KiB, count=1, average=1953 KiB
	t.py:5: size=977 KiB, count=1, average=977 KiB

	t.py:16: size=35.3 MiB (+35.3 MiB), count=999745 (+999745), average=37 B
	t.py:17: size=15.3 MiB (+15.3 MiB), count=1 (+1), average=15.3 MiB


Wszystko jest widoczne jak na dłoni, litera `ź` zajmuje więcej miejsca niż `A`,
jednak to wszystko nic w porównaniu z rozmiarem słownika. Tego rodzaju dane mogą
być nieocenione przy debugowaniu oraz podczas optymalizacji kodu.

Na koniec muszę ostrzec, że `tracemalloc` dość mocno spowalnia wykonywanie
programu, więc po pierwsze -- żeby otrzymać wyniki czasem trzeba uzbroić się w cierpliwość,
a po drugie -- nie należy stosować `tracemalloc` w środowisku produkcyjnym.

### Inne, co ciekawsze zmiany

#### Tryb izolowany

Pythona można teraz uruchomić z parametrem `-I`, który odcina interpreter
od `site-packages`, jak i od wszelkiego dostępu do zewnętrznych bibliotek.
Użycie tego trybu jest zalecane przy zastosowaniu Pythona w skryptach systemowych.

#### Nowy format `pickle` i `marshal`

Python 3.4 wprowadza nowe formaty dla `pickle` i `marshal` (odpowiednio 4 i 3).

W przypadku `pickle` rozwiązanych zostało wiele problemów występujących w
poprzednich wersjach protokołu, a także poprawiona została wydajność.
Tradycyjnie już, w celu zapewnienia wstecznej kompatybilności, nowy format
`pickle` nie jest domyślnym, tak więc żeby go użyć,
należy jawnie określić wersję protokołu, najlepiej (też tradycyjnie już) używając stałej
`pickle.HIGHEST_PROTOCOL`.

Jeśli chodzi o `marshal`, to dzięki uniknięciu powielania niektórych obiektów,
zmniejszył się rozmiar plików `.pyc` (i `.pyo`), a co za tym idzie, spadła
ilość pamięci zajmowanej przez moduły wczytane z tychże plików.

#### *Single-dispatch* w `functools`

W module `functools` pojawił się niepozorny dekorator `singledispatch()`,
który pozwala na zdefiniowanie funkcji generycznej, posiadającej różną
implementację w zależności od typu argumentu.

Bez wdawania się w dywagacje, poniższy przykład powinien rzucić nieco światła
na to, ile dobrego kryje się za tą mętną definicją:


	>>> from collections.abc import Sequence
	>>> from functools import singledispatch
	>>> @singledispatch
	... def fun(arg):
	...     print("Łapię całą resztę, tym razem był to", type(arg))
	... 
	>>> @fun.register(int)
	... @fun.register(float)
	... def _(arg):
	...     print("Mamy numerek!")
	... 
	>>> @fun.register(Sequence)
	... def _(arg):
	...     print("Sekwencja o długości ", len(arg))
	... 
	>>> @fun.register(tuple)
	... def _(arg):
	...     print("Nie lubię tupli!")
	... 
	>>> fun(11)
	Mamy numerek!
	>>> fun("tekścik")
	Sekwencja o długości  7
	>>> fun([1, 3, 5])
	Sekwencja o długości  3
	>>> fun((3, 4))
	Nie lubię tupli!
	>>> fun(set())
	Łapię całą resztę, tym razem był to <class 'set'>


#### Poprawa bezpieczeństwa

Nowy, bezpieczny, algorytm hashowania, obsługa TLS v1.1 i v1.2, możliwość
pobierania certyfikatów z Windows system cert store, obsługa serwerowego SNI
(Server Name Indication), bezpieczniejsze deskryptory plików. To tylko niektóre
z licznych zmian, wpływających korzystnie na bezpieczeństwo nowego Pythona.

### Podsumowanie

Python 3.4 zdaje się być bardzo dobrym wydaniem, pomimo braku (a może dzięki brakowi?)
zmian w składni. Wprowadza on szereg usprawnień oraz oddaje w ręce użytkownika
kilka bardzo dobrych bibliotek wbudowanych, które z pewnością znajdą sobie
miejsce w wielu plikach z rozszerzeniem `.py`.

Zarówno nowi użytkownicy, jak i starzy wyjadacze znajdą coś dla siebie w tym
wydaniu, a dzięki praktycznie pełnej kompatybilności wstecz, nowy Python nie powinien
też nastręczać problemów przy aktualizacji<sup>*</sup>.

<sup>*</sup> Oczywiście chodzi o aktualizację z Pythona 3.3 ;)

### Źródła

* https://docs.python.org/3/whatsnew/3.4.html - oficjalny dokument "what's new"
  dla Pythona 3.4.
* https://mail.python.org/pipermail/python-ideas/ - lista mailingowa
  wyznaczająca nowe kierunki rozwoju Pythona.
* http://hg.python.org/cpython/ - repozytorium zawierające źródła
  (oraz nader ciekawe commit-logi) Pythona.
* http://legacy.python.org/dev/peps/ - propozycje usprawnień Pythona.

<!-- Przeczytane: Piotr Kasprzyk -->
