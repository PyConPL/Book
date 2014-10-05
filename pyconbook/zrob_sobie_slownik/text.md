# Zrób sobie słownik
## Szymon Pyżalski

Niektórzy programiści Pythona zdają się nie zauważać możliwości, jakie im daje
model obiektowy. Tymczasem w wielu sytuacjach stworzenie klasy emulującej klasę
wbudowaną daje możliwość znacznego zwiększenia czytelności kodu, a
także wykorzystania pewnych wbudowanych mechanizmów. Poniższy samouczek pokaże, jak stworzyć obiekt zachowujący się jak słownik, który zamiast w pamięci
przechowuje dane w relacyjnej bazie danych. Zapoznamy się z magicznymi
atrybutami obiektów, a także z wprowadzonymi od wersji języka Python 2.6
abstrakcyjnymi klasami bazowymi (abc).

### Przygotowanie

Przedstawione poniżej zadania napisane są w Pythonie w wersji 3.3 i korzystają z bazy danych SQLite3.
Interfejs SQLite3 znajduje się w bibliotece standardowej, dzięki czemu nie ma potrzeby instalowania
dodatkowych paczek.

Tworzymy bazę danych z jedną tabelą:

    $ sqlite3 litedict.db 
    sqlite>CREATE TABLE dictvals (
       ...>    dict_id VARCHAR,
       ...>    key VARCHAR,
       ...>    value VARCHAR,
       ...>    PRIMARY KEY (dict_id, key)
       ...>);

Każdy słownik będzie posiadał swoje losowe id. Będzie on zdolny przechowywać
dowolne łańcuchy znaków w formie par klucz-wartość. 

Wstawiamy do tabeli dane:


    sqlite> INSERT INTO dictvals VALUES ('bedevere', 'title', 'Sir');
    sqlite> INSERT INTO dictvals VALUES ('bedevere', 'name', 'Bedevere');
    sqlite> INSERT INTO dictvals VALUES ('bedevere', 'nickname', 'the Wise');
    sqlite> INSERT INTO dictvals VALUES ('galahad', 'title', 'Sir');
    sqlite> INSERT INTO dictvals VALUES ('galahad', 'name', 'Galahad');
    sqlite> INSERT INTO dictvals VALUES ('galahad', 'nickname', 'the Pure');

### Słownik w wersji tylko do odczytu

Aby nasz słownik wspierał odczyt danych za pomocą nawiasów kwadratowych,
musimy zaimplementować metodę ``__getitem__``:

    class LiteDict():
        """Dictionary storing the values in sqlite3 database."""

        def __init__(self, id=None):
            self.id = id or ''.join(
                (random.choice(string.ascii_lowercase) for i in range(8)))
        
        def _connect(self):
            conn = sqlite3.connect(DB_NAME)
            return conn, conn.cursor()

        def __getitem__(self, key):
            conn, cursor = self._connect()
            cursor.execute(
                'SELECT value FROM dictvals WHERE dict_id = ? AND key = ?;',
                (self.id, key))
            rows = cursor.fetchall()
            if rows:
                return rows[0][0]
            else:
                raise KeyError('No such key: {0}'.format(key))
 
Testujemy działanie nowej metody:


    >>> from litedict import LiteDict
    >>> l = LiteDict('galahad')
    >>> l['title']
    'Sir'
    >>> l['age']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "litedict.py", line 33, in __getitem__
        raise KeyError('No such key {0}'.format(key))
    KeyError: 'No such key: age'


Wydaje się działać. Czy jednak rzeczywiście stworzyliśmy pełnoprawne pythonowe
mapowanie?

### Używamy abc


W celu wykorzystania abstrakcyjnych klas bazowych dodajemy do naszego skryptu linijkę:

    from collections.abc import Mapping

i podmieniamy definicję klasy na:

    class LiteDict(Mapping):

Ponownie testujemy tworzenie słownika:

    >>> from litedict import LiteDict
    >>> l = LiteDict('galahad')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: Can't instantiate abstract class LiteDict with abstract methods __iter__, __len__

Tym razem nie działa - definicja klasy ``Mapping`` w języku Python zakłada, że będzie ona
miała zaimplementowane jeszcze metody ``__iter__`` i ``__len__``. Zobaczmy dlaczego:

    >>> from collections.abc import Mapping
    >>> Mapping.__mro__
    (<class 'collections.abc.Mapping'>, 
	 <class 'collections.abc.Sized'>, 
	 <class 'collections.abc.Iterable'>, 
	 <class 'collections.abc.Container'>, 
	 <class 'object'>)

Jak widać, klasa ``Mapping`` jest potomkiem następujących klas:

* ``Container`` - wszystko, na czym możemy użyć operatora ``is``;
* ``Iterable`` - wszystko, po czym możemy iterować w pętli ``for``;
* ``Sized`` - to co ma rozmiar i na czym można wykonać ``len()`` (nie każdy
  iterator ma długość, są też leniwe, a nawet nieskończone).

Oznacza to, że klasa ta powinna posiadać cechy wszystkich swoich przodków dodając
jednocześnie możliwość pobierania wartości po kluczu. 

Zauważmy, że klasa nie zabrania nam stworzenia subklasy nie implementującej koniecznych metod. Dopiero
próba instancjacji takiej klasy daje błąd. Możemy więc dowolnie poszerzać
drzewo abstrakcyjnych klas, ale nie wolno nam tworzyć ich instancji.
Dodajmy więc funkcjonalności iteratora i rozmiaru i zobaczmy, co dostaniemy
w zamian:

    def __iter__(self):
        conn, cursor = self._connect()
        cursor.execute(
            'SELECT key FROM dictvals WHERE dict_id = ?;', (self.id,))
        rows = cursor.fetchall()
        for row in rows:
            yield row[0]
        
    def __len__(self):
        conn, cursor = self._connect()
        cursor.execute(
            'SELECT COUNT(*) FROM dictvals WHERE dict_id = ?;', (self.id,))
        rows = cursor.fetchall()
        return rows[0][0]

Dodanie powyższych metod wystarcza do poprawnego utworzenia obiektu klasy ``LiteDict``:

    >>> from litedict import LiteDict
    >>> l = LiteDict('galahad')

Klasa abstrakcyjna, jak widać, jest zaimplementowana poprawnie.

    >>> len(l)
    3
    >>> list(l)
    ['title', 'name', 'nickname']

Zarówno funkcjonalności iteratora jak i pomiaru długości działają, a ponadto
po zaimplementowaniu trzech metod, otrzymaliśmy całą ich kolekcję:

    >>> from litedict import LiteDict
    >>> l = LiteDict('galahad')
    >>> l.get('title')
    'Sir'
    >>> l.get('age')
    >>> list(l.values())
    ['Sir', 'Galahad', 'the Pure']
    >>> list(l.items())
    [('title', 'Sir'), ('name', 'Galahad'), ('nickname', 'the Pure')]

### No to jeszcze tylko zapis...


W celu uzyskania w pełni funkcjonalnej klasy dodamy jeszcze zapis i usuwanie:

    def __setitem__(self, key, value):
        conn, cursor = self._connect()
        cursor.execute(
            'REPLACE INTO dictvals VALUES (?, ?, ?)', (self.id, key, value))
        conn.commit()

    def __delitem__(self, key):
        conn, cursor = self._connect()
        cursor.execute('DELETE FROM dictvals where dict_id = ? AND key = ?;', (
            self.id, key))
        conn.commit()

Dodanie powyższych metod upoważnia nas do zmiany klasy bazowej naszego obiektu
z ``Mapping`` na ``MutableMapping``. Nacieszmy się teraz naszym obiektem:

    >>> del l['title']
    >>> list(l.items())
    [('name', 'Galahad'), ('nickname', 'the Pure')]
    >>> l['nickname'] = 'the Dirty'
    >>> l['title'] = 'Knight'
    >>> list(l.items())
    [('name', 'Galahad'), ('nickname', 'the Dirty'), ('title', 'Knight')]
    >>> l.update({'nickname': 'the Pure', 'location': 'castle Anthrax', 'title': 'Sir'})
    >>> list(l.items())
    [('location', 'castle Anthrax'), ('name', 'Galahad'), ('nickname', 'the Pure'), ('title', 'Sir')]
    >>> l.pop('location')
    'castle Anthrax'
    >>> list(l.items())
    [('name', 'Galahad'), ('nickname', 'the Pure'), ('title', 'Sir')]

Jak widać w powyższych przykładach, nasz obiekt po zaimplementowaniu jedynie pięciu metod staje się pod
względem zachowania w zasadzie nieodróżnialny od wbudowanego obiektu ``dict``.
``LiteDict`` możemy używać zamiennie z normalnym słownikiem
i każda logika działająca dla jednego zadziała i dla drugiego.  

### Ale nie podoba mi się...

Skoro wszystkie metody naszego API zaimplementowane są za
pomocą pięciu metod, to na przykład wywołanie metody ``update`` przedstawione w powyższym przykładzie będzie
wykonywać wykonywać trzykrotny ``commit`` do bazy danych. Będzie to najprawdopodobniej niewydajne. 
Na szczęście nie jesteśmy w żaden sposób skazani na implementacje jakie dostarczają nam klasy ``abc``. Jeśli chcemy możemy sami
zaimplementować tę metodę:

    def update(self, other=None, **kwargs):
        data = []
        if other:
            for k, v in other.items():
                data.append((self.id, k, v))
        for k, v in kwargs.items():
            data.append((self.id, k, v))
        conn, cursor = self._connect()
        cursor.executemany('REPLACE INTO dictvals VALUES (?, ?, ?)', data)
        conn.commit()

Od tego momentu nasz słownik ma tę samą funkcjonalność co powyżej, ale masowy ``update``
kilku kluczy wykona się wydajniej - bez wielokrotnego *commitowania*.

### Rada na koniec

Oczywiście nie każda okazja jest dobra, żeby rzucać się w wir nadpisywania
magicznych metod. Zawsze trzeba zadać sobie kluczowe pytanie "czy semantyka
użycia mojej biblioteki stanie się dzięki temu czytelniejsza?". Jeśli jednak
odpowiedź na to będzie twierdząca - nie bójmy się trochę pogrzebać we wnętrzu
naszego ukochanego języka.
