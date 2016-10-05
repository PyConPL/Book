# Wstęp
Przetwarzanie i składowanie informacji jest nieodłącznym elementem niemal
każdego programu komputerowego, zaś w zakresie przechowywania danych, przez
lata, bazy relacyjne wypracowały sobie pozycję niekwestionowanego lidera.
Dlatego nic dziwnego, że bardzo rozpowszechnioną praktyką przy tworzeniu
aplikacji jest jej integracja z relacyjną bazą danych.

W tym miejscu pojawia się problem niekompatybilności, gdyż twórcy aplikacji
programują w swoich językach (najczęściej imperatywno-obiektowych,
jak Python), natomiast bazy danych używają wyspecjalizowanego
(deklaratywno-opisowego) języka SQL.

Niestety, współpraca języków opartych na tak różnych paradygmatach jest trudna
i w punkcie łączenia pojawia się wiele zgrzytów. Dlatego, żeby pogodzić te dwa
światy, powstały biblioteki ORM (*Object Relational Mapping*),
których zadaniem jest likwidacja tarcia na styku przez (w skrócie) usunięcie
SQLa z kodów źródłowych aplikacji i zastąpienie go odwołaniami do biblioteki ORM.

Niniejszy artykuł ma na celu ukazanie dobrodziejstw płynących z użycia ORM
jako takiego, a także uzasadnienie dlaczego akurat tandem
SQLAlchemy+PostgreSQL jest tak godny polecenia.

# Czym jest Object Relational Mapping?
Dostęp do relacyjnych baz danych umożliwiają nam różnorakie sterowniki,
z których prawie wszystkie są zgodne z DB API 2.0 (PEP249[1]), po co więc
dodatkowa warstwa pomiędzy sterownikiem a naszym kodem?

Otóż problem polega na tym, że na SQL osadzony w kodzie Pythona składa
się zazwyczaj zlepek łańcuchów tekstowych i nawet zastosowanie wzorców
zastępowania (`?`, `%s`) w kwerendach tylko częściowo poprawia sytuację.
Wciąż musimy używać dwóch języków, które się przenikają, co z perspektywy kodu
aplikacji sprowadza się do budowania kwerend przez łączenie łańcuchów
znakowych. A to nie jest ani ładne, ani wygodne, ani też łatwe do przetestowania.

ORM pozwala na zapisanie zarówno schematu, jak i zapytań do bazy danych przy
użyciu naszego języka programowania, co jest o wiele wygodniejsze, mniej
podatne na błędy i umożliwia wykorzystanie potęgi Pythona w interakcji z bazą.
Ponadto, stosując pewne obostrzenia, można uczynić kod niezależnym
od podłączonego silnika bazy danych.

Zamiast stringowej ekwilibrystyki w stylu:

```
>>> query = 'SELECT * FROM users'
>>> if criteria:
...     query += ' WHERE name LIKE ?'
>>> cursor.execute(query, [criteria]).fetchone()
(1, "Jasiek")
```
Możemy mieć wszystko obiektowo w Pythonie, bez choćby jednego łańcucha znakowego:

```
>>> query = session.query(User)
>>> if criteria:
...     query = query.filter(User.name.like(criteria))
>>> query.first()
<User(id=1, name="Jasiek")>
```
# Dlaczego SQLAlchemy?
Bibliotek ORM dla Pythona jest całkiem sporo[2], niektóre z nich są proste
(Storm, SQLObject), inne są dobrze zintegrowane ze środowiskiem pracy
(Django ORM), a jeszcze inne są ciekawe (PonyORM). Ja jednak wybrałem
SQLAlchemy [3] ze względu na kilka cech, które w połączeniu tworzą bardzo
potężne narzędzie:

* **Kompletność** - bardzo wiele można zrobić przy użyciu SQLAlchemy bez uciekania się do pisania czystego SQLa. Skomplikowane kwerendy nie stanową żadnego problemu.
* **Dokumentacja** - obszerna, konkretna, z licznymi przykładami i praktycznymi przypadkami użycia [4].
* **Dojrzały projekt** - SQLAlchemy istnieje od ponad 10 lat.
* **Ciągły rozwój** - projekt jest aktywny i często aktualizowany, dzięki czemu nadąża za ciągłym rozwojem relacyjnych baz danych.
* **Mnogość obsługiwanych backendów** - bardzo szeroka gama obsługiwanych sterowników, włączając w to SQLite, dostępny bezpośrednio z biblioteki standardowej Pythona.
* **Samodzielność** - nie jest zależny od żadnych bibliotek zewnętrznych, nie wymaga też określonego frameworka do działania i dobrze się integruje z każdym typem projektu.
* **DDL i reflection** - posiada możliwość definiowania struktury danych, a także opcję automatycznego budowania obiektów na podstawie już istniejącej bazy.
* **Wygodne migracje** - dzięki dodatkowej bibliotece o nazwie `alembic`[5].
* **Elastyczność** - prawie wszystko w SQLAlchemy można skonfigurować, rozszerzyć, czy dostosować do konkretnych potrzeb.

Biblioteka SQLAlchemy zbudowana jest w oparciu o wrzorzec projektowy
*data mapper* [6], który daje programiście większą kontrolę, ale jest
też nieco trudniejszy w okiełznaniu, niż bardziej rozpowszechniony wśród ORMów
wzorzec *active record* [7].

Z tego powodu, jedyną realną wadą SQLAlchemy *może być* początkowa trudność
zrozumienia i odnalezienia się w przepastnych czeluściach dokumentacji,
jednak liczne dostępne samouczki pozwalają na stopniowe zgłębianie wiedzy,
począwszy od absolutnych podstaw, bez konieczności zrozumienia wszystkiego
naraz.

# Dlaczego PostgreSQL?
Na rynku znaleźć można ogromną różnorodność dostępnych relacyjnych baz danych,
tak więc PostgreSQL posiada wielu konkurentów. Jednakże wyróżnia się on
z tłumu dzięki połączeniu wielu pozytywnych cech:

* **Projekt (pierwotnie) akademicki** - oparty na solidnych podstawach matematyczno-algorytmicznych.
* **Ciągły rozwój** - zapewniony przez uczelnie na całym świecie, a także przez firmy prywatne, które udostępniają swoich programistów oraz szczodrze dotują projekt.
* **Bardzo wierna implementacja standardów SQL** - w przeciwieństwie do znacznej części konkurencji PostgreSQL stara się być zgodny ze standardem SQL (SQL:2011 [8]).
* **Bardzo użyteczne rozszerzenia standardu SQL** - PostgreSQL wybiega poza standard dostarczając liczne funkcjonalności, których użytkownicy pragną, jak obsługa XML i JSON, różnorodne typy indeksów, czy *full text search*.
* **Szybkość działania** - PostgreSQL błyszczy w przypadku dużych i skomplikowanych baz.
* **Powszechność** - dostępny dla wszystkich znaczących systemów operacyjnych, ponadto prawie każdy hosting WWW udostępnia PostgreSQL.
* **Mnóstwo narzędzi** - począwszy od prostych skryptów pomocniczych, na pełnowymiarowych narzędziach administracyjnych kończąc (pgAdmin [9]).
* **Open-source** - otwarty i darmowy po wsze czasy.

Jak wszystko, PostgreSQL ma też swoje wady. Chyba największą jego bolączką
jest trudność konfiguracji oraz konieczność stosowania zewnętrznych narzędzi
w celu otrzymania pewnych funkcjonalności, które inne systemy bazodanowe po prostu mają.

Na przykład, gdy obciążenie bazy rośnie i pojawia się konieczność dostawienia
dodatkowych serwerów, PostgreSQL posiada wbudowaną jedynie replikację typu
*master-slave* (wszystkie zapisy muszą być wykonane na głównym serwerze).
Natomiast, aby osiągnąć dwukierunkową replikację *multi-master*, należy już
użyć zewnętrznego narzędzia takiego jak Postgres-BDR [10].

# Duet PostgreSQL + SQLAlchemy
Razem, te dwa potężne narzędzia stają się bazodanowym *wunderwaffe* -
uzupełniają się idealnie, jak w przykładnym związku, a ich możliwości w sumie
daleko wybiegają poza funkcje każdego z osobna.

Warto tutaj wspomnieć o fakcie, że SQLAlchemy wspiera wiele rozszerzeń
PostgreSQL, dając użytkownikowi coś więcej, niż tylko warstwę abstrakcji
pomiędzy programem a bazą. Jednakże, jeżeli skorzystamy z tych dodatkowych
funkcji, tracimy jeden z atutów ORMa, a mianowicie niezależność od konkretnego
silnika bazy danych.

## Ten trzeci
Żeby połączyć SQLAlchemy z bazą danych potrzebny jest jeszcze jeden element,
a mianowicie sterownik bazy danych dla Pythona. SQLAlchemy współpracuje
z wieloma sterownikami (różne silniki nazywane są dialektami), w przypadku
PostgreSQL największe możliwości daje biblioteka `psycopg2` [11].

Połączenie z bazą w SQLAlchemy nawiązujemy podając odpowiedni ciąg znaków je opisujący:

    >>> from sqlalchemy import create_engine
    >>> engine = create_engine(
    ...     'postgresql+psycopg2://user:passwd@host:port/dbname'
    ... )

# ORM w praktyce
Po tym przydługim wstępie teoretycznym czas na praktykę. Poniżej, drogi
czytelniku, znajdziesz kilka przykładów użycia SQLAlchemy, z których część
pokaże unikalne możliwości, jakie daje ORM w połączeniu z bazą PostgreSQL.

## Definiowanie tabel
Tabele można definiować w sposób deklaratywny, tworząc klasy, gdzie kolumny
bazodanowe reprezentowane są przez atrybuty:

    >>> from sqlalchemy.ext.declarative import declarative_base
    >>> from sqlalchemy import Column, Integer, Text

    >>> Base = declarative_base()
    >>> class User(Base):
    ...     __tablename__ = 'users'
    ...     id = Column(Integer, primary_key=True)
    ...     name = Column(Text)

Powyższy zapis przedstawia tabelę, której SQL wyglądałby mniej więcej tak:

    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name TEXT
    );

Co więcej, SQLAlchemy potrafi stworzyć dla nas tabele na podstawie
zadeklarowanych klas, wystarczy jedna linijka:

    >>> Base.metadata.create_all(engine)

## Odwzorowanie struktury bazy
Z drugiej strony, jeśli istnieje już baza danych, to SQLAlchemy potrafi
stworzyć dla nas odpowiednie obiekty na podstawie obiektowego schematu tabel:

    >>> from sqlalchemy import MetaData
    >>> meta = MetaData()
    >>> meta.reflect(bind=engine)
    >>> users_table = meta.tables['users']

## Manipulacja rekordami
Prawie wszystkie operacje związane z codziennym użytkowaniem bazy wymagają
użycia sesji:

    >>> from sqlalchemy.orm import sessionmaker
    >>> Session = sessionmaker(bind=engine)
    >>> session = Session()

Mając już obiekt sesji możemy tworzyć rekordy:

    >>> new_user = User(name='jan')
    >>> session.add(new_user)

Odpytywać bazę:

    >>> users = session.query(User).filter_by(name='jan')
    >>> list(users)
    [<User(name='jan')>]

Modyfikować dane:

    >>> users[0].name = 'jasiek'

Nie należy jednak zapominać o zatwierdzaniu zmian:

    >>> session.commit()

A gdy już czegoś nie potrzebujemy, wystarczy powiedzieć:

    >>> session.delete(new_user)
    >>> session.query(User).filter_by(name='jasiek').count()
    0

## Relacje
Tworzenie relacji sprowadza się do jej zadeklarowania w tabeli podrzędnej:

    >>> from sqlalchemy import ForeignKey
    >>> from sqlalchemy.orm import relationship

    >>> class Note(Base):
    ...     __tablename__ = 'notes'
    ...     id = Column(Integer, primary_key=True)
    ...     note = Column(Text, nullable=False)
    ...     user_id = Column(Integer, ForeignKey(User.id))
    ...     user = relationship(User, back_populates="notes")

Jeśli relacja ma być obustronna, modyfikujemy też rodzica:

    >>> User.notes = relationship(
    ...     Note, order_by=Note.id, back_populates="user")

Od tej pory relacje zachowują się jak zwykłe struktury pythonowe:

    >>> mr_x = User(name="Mr. X")
    >>> note1 = Note(note="Notatka 1", user=mr_x)
    >>> note2 = Note(note="Notatka 2")
    >>> mr_x.notes.append(note2)
    >>> session.add(mr_x)
    >>> session.commit()

## Kwerendy
Zapytania SQL za sprawą alchemii zmieniają się w programowanie obiektowe:

    >>> query = session.query(User)
    >>> query.order_by(User.id).first()
    <User(id=1, name='jasiek')>

Kwerenda jest wielokrotnego użytku i można ją modyfikować:

    >>> query2 = query.filter(User.name.ilike('mr%'))
    >>> query2.first()
    <User(id=2, name='Mr. X')>
    >>> query2.count()
    1

Podzapytania to nie problem:

    >>> subquery = session.query(Note).filter(Note.user_id == User.id)
    >>> query3 = query.filter(subquery.exists())
    >>> query3.count()
    1

## Konstruowanie SQL
Nawet SQLAlchemy, mimo iż potężny, ma swoje ograniczenia i mogą zdarzyć się
kwerendy, których nie da się zapisać przy użyciu funkcji ORMa. W takiej
sytuacji dostajemy jeszcze ostatnią deskę ratunku - konstruktor wyrażeń SQL.
Jest to zestaw niskopoziomowych funkcji, pozwalający na precyzyjne tworzenie
zapytań SQL, gdzie magia ORMa już nie działa tak dobrze, ale za to możliwości
są niemal nieograniczone.

    >>> from sqlalchemy.sql import table, column
    >>> user_table = table('users',
    ...     column('id', Integer),
    ...     column('name', String)
    ... )
    >>> str(users_table.select())
    SELECT users.id, users.name
    FROM users
    >>> str(
    ...    users_table.update()
    ...        .where(users_table.c.id == 1)
    ...        .values(name="jean")
    ... )
    UPDATE users SET name=:name WHERE users.id = :id_1

# Cuda od PostgreSQL
Praktycznie wszystko co opisano powyżej, można było wykonać na dowolnym
silniku bazy danych i PostgreSQL nie był do tego konieczny. Jednakże
SQLAlchemy daje użytkownikowi dostęp do wielu unikalnych funkcji Postgresa,
takich jak:

* **Sekwencje** - wsparcie dla samodzielnych sekwencji, jak i dla typu liczbowego `SERIAL`.
* **INSERT/UPDATE/DELETE zwracające wartości** - możliwe jest pobranie wartości kolumn dla operacji na pojedynczych wierszach.
* **Upsert** - nowinka z PostgreSQL 9.5, obsługa `INSERT ... ON CONFLICT`.
* **Full text search** - funkcje ułatwiające pracę z danymi `TSVECTOR`, `TSQUERY` oraz operatorem `@@`.
* **... FROM ONLY ...** - interakcja z wbudowanym w PostgreSQL dziedziczeniem tabel.
* **Rozbudowane indeksy** - indeksy cząstkowe, operatory, typy (B-Tree, Hash, GiST, GIN), `CONCURRENTLY`.
* **Dodatkowe typy danych** - `ARRAY`, `JSON`/`JSONB`, `HSTORE`, `ENUM`, `...RANGE`, `MACADDR`.
* **Constraints** - klauzula `EXCLUDE`.
* **Dodatkowe opcje połączenia** - opcja ustawienia poziomu izolacji transakcji (*isolation level*) oraz możliwość użycia serwerowych kursorów (*server side cursors*) w wywołaniu `create_engine()`.

## Obsługa JSON/JSONB
Ograniczona objętość artykułu nie pozwoli na szczegółowe opisanie wszystkich
unikalnych funkcjonalności, jednak znajdzie się jeszcze miejsce na małą próbkę
możliwości na przykładzie natywnego wsparcia dla JSONa.

PostgreSQL od wersji 9.2 udostępnia dwa typy danych do przechowywania JSONa -
`JSON` (typ tekstowy, zachowujący dokument w całości) i `JSONB` (binarny,
zachowujący logiczną strukturę dokumentu). Typ binarny daje większe
możliwości, gdyż można go dowolnie kwerendować i indeksować oraz umożliwia
użycie kilku przydatnych funkcji i operatorów.

SQLAlchemy natywnie wspiera JSONa (w ramach dialektu), mapując go na pythonowe
typy wbudowane (listy, słowniki), dlatego używanie JSONa jest niezmiernie
proste i intuicyjne.

    >>> from sqlalchemy.dialects.postgresql import JSONB
    >>> class Response(Base):
    ...     __tablename__ = 'responses'
    ...     id = Column(Integer, primary_key=True)
    ...     data = Column(JSONB)
    ...
    >>> data = {
    ...     'status':200,
    ...     'body': {
    ...         'items': [1, 2, 3],
    ...         'took': 0.93
    ...     }
    ... }
    >>> resp = Response(data=data)
    >>> session.add(resp)
    >>> session.commit()
    >>> db_resp = session.query(Response) \
    ...     .filter(Response.data['status'].astext == '200') \
    ...     .filter(Response.data.has_key('body')) \
    ...     .one()
    >>> db_resp.data['body']['items']
    [1, 2, 3]

# Podsumowanie
W dzisiejszych czasach stosowanie narzędzi ORM jest powszechne, a Python w tej
kwestii ma nam do zaoferowania perełkę w postaci SQLAlchemy. W połączeniu
z dobrą relacyjną bazą danych, jaką niewątpliwie jest PostgreSQL, możemy
tworzyć nowoczesne, przejrzyste, uniwersalne i łatwe w utrzymaniu aplikacje
bazodanowe, zapominając o smutnych czasach, gdy SQL musiał mieszać się z kodem
Pythona.

# Bibliografia
1. Specyfikacja DB API 2.0. https://www.python.org/dev/peps/pep-0249/
2. Porównanie ORMów. http://pythoncentral.io/sqlalchemy-vs-orms/
3. Strona domowa SQLAlchemy. http://www.sqlalchemy.org
4. Dokumentacja SQLAchemy. http://docs.sqlalchemy.org/en/latest/
5. Zestaw narzędzi do migracji baz danych. http://alembic.zzzcomputing.com/en/latest/
6. Wzorzec projektowy, na którym opiera się SQLAlchemy. https://en.wikipedia.org/wiki/Data`_`mapper`_`pattern
7. Popularny wzorzec projektowy wśród ORMów. https://en.wikipedia.org/wiki/Active`_`record`_`pattern
8. Zbiór linków do strzępków dokumentacji standardu SQL. http://modern-sql.com/standard
9. Narzędzie administracyjne dla PostrgeSQL. https://www.pgadmin.org
10. Narzędzie do dwukierunkowej replikacji PosgreSQL. https://2ndquadrant.com/en/resources/bdr/
11. Najpopularniejszy sterownik PostgreSQL dla Pythona. http://initd.org/psycopg/
