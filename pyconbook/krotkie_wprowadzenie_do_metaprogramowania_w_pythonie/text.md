# Krótkie wprowadzenie do metaprogramowania w Pythonie,
## Piotr Przymus

### Czyli o tym jak ułatwić (utrudnić) programowanie sobie i innym 

Metaprogramowanie – to dynamiczne tworzenie kodu lub modyﬁkowanie
działania uruchomionego programu. Python daje nam w tym temacie
szerokie możliwości. Krótki tutorial dla tych, którzy chcą lepiej
poznać takie techniki metaprogramowania jak dekoratory, metaklasy,
syntetycznie generowany kod czy ’monkey patching’.

### Metaprogramowanie

W tym artykule postaram się przedstawić podstawowe techniki związane z
metaprogramowaniem w Pythonie.  Za pomocą przykładów omówię
dekoratory, metaklasy, kod generowany syntetycznie oraz ’monkey
patching’. Jako że metaprogramowanie w Pythonie to bardzo rozległy
temat, pełne jego opisanie w formie jednej publikacji jest praktycznie
niemożliwe. Dlatego celem tego artykułu jest jedynie przybliżenie
niezbędnych podstaw okraszonych dużą ilością przykładów.  Niniejsza
praca stanowi usystematyzowanie informacji zebranych przeze mnie z
różnych źródeł:

* dekoratory – [7, 1],
* metaklasy – [4, 1],
* syntetyczne tworzenie kodu – [2, 9, 1],
* monkey patching – [2, 3, 5].

### Dekoratory

#### Wstęp

Zanim omówię dekoratory przypomnę podstawy związane z funkcjami w
Pythonie. Funkcje w Pythonie mogą być zwracane jako wynik innych
funkcji oraz przekazywane jako parametry innych funkcji. Jest to
konsekwencją tego, że funkcje są obiektami pierwszego rzędu – czyli
nie mają żadnych restrykcji i zachowują się jak inne obiekty.

	# --------------------------------------
	# Przykład (1) Wrapper

    def debug_wrapper(func) :

        msg = func.__name__

        def wrapper (* args, **kwargs):
            print(msg)
            return func(* args, **kwargs)
        return wrapper

    def add (x ,y):
        return x + y

    if __name__ == '__main__':
        debug_add = debug_wrapper(add)
        debug_add(1 ,1)
        print debug_add.__name__ , debug_add.__doc__ , debug_add.__module__

	# --------------------------------------
	# Przykład (2) Dekorator

    def debug_wrapper(func):
        msg = func.__name__
        def wrapper (*args ,**kwargs):
            print(msg)
            return func (*args , **kwargs)
        return wrapper 6

    @debug_wrapper
    def add(x , y ):
        return x + y 10

    if __name__ == '__main__':
        add(1 , 1)
        print add.__name__ , add.__doc__ , add.__module__


Przykład 1. pokazuje jak opakować wywołanie innej funkcji. Funkcja
debug wrapper jako argument func przyjmuje funkcję, a jako wynik
zwraca funkcję opakowującą wrapper. Funkcja wrapper wypisuje nazwę
funkcji func, a następnie zwraca wynik wywołania func. Ten prosty
przykład pokazuje podstawy działania dekoratorów.  Dekoratory to po
prostu rozszerzenie składni Pythona, które pojawiło się już w wersji
2.4, i które pozwala w wygodny sposób używać powyższej techniki. W
pewnym sensie jest to tylko tzw. lukier składniowy, który pozwala
używać nowej składni dla dobrze znanej wcześniej techniki. Jednak
dekoratory zdobyły dużą popularność i są często stosowane w wielu
projektach. Pozwalają zgrabnie wyrazić funkcjonalność, która jest
powtarzana w wielu funkcjach (np. logowanie, synchronizacja, czy
konﬁguracja mechanizmów komunikacji z bazą danych).

Przykład 2. pozwala na osiągnięcie podobnego efektu jak przykładzie 1,
jednak używając notacji dekoratorów. Użycie dekoratora wyraża się
poprzez podanie nazwy dekoratora poprzedzonego znakiem @ bezpośrednio
przed nazwą tworzonej funkcji (w naszym przykładzie @debug_wrapper).


	# --------------------------------------
	# Przykład (3) Dekorator wraps
	
	from functools import wraps

	def debug_wrapper(func):
		msg = func.__name__

	@wraps(func)
	def wrapper(*args, **kwargs):
		print(msg)
		return func(*args, **kwargs)
	return wrapper

	@debug_wrapper
	def add(x, y):
		return x + y

	if __name__ == "__main__":
		add(1, 1) # <-- OK
		print add.__name__, add.__doc__, add.__module__ # <-- OK

	
	# --------------------------------------
	# Przykład (4) Argumenty podejście I

	from functools import wraps

    def debug(prefix=''):
        def decorate (func):
            msg = prefix + func . __name__
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(msg)
                return func(*args, **kwargs)
            return wrapper
        return decorate

    @debug(prefix='****') # <-- OK
    def add (x , y ):
        return x + y

    @debug # <-- ERROR
    def add1 (x , y):
        return x + y

    if __name__ == ’__main__’:
        add(1, 2)
        add1(1, 2)


		
	# --------------------------------------
	# Przykład (5) Argumenty podejście II

    from functools import wraps, partial

    def debug(func=None, prefix=''):
        if func is None:
            return partial(debug, prefix=prefix)

        msg = prefix + func . __name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            print(msg)
            return func(*args, **kwargs)
        return wrapper

    @debug(prefix='****') # <-- OK 13
    def add(x, y):
        return x + y

    @debug # <-- OK 17
    def add1(x, y):
        return x + y

    if __name__ == ’__main__’:
        add(1, 2)
        add1(1, 2)


#### Implementacja

Praktycznie dowolna funkcja przyjmująca jako argument inną funkcję, a
jako rezultat zwraca funkcję lub obiekt wykonywalny, może być
dekoratorem. Jednak w najprostszej implementacji, jak w przykładzie 2,
pomiędzy oryginalną funkcją, a funkcją udekorowaną będą pewne
różnice. Różnić będzie się sygnatura oraz atrybuty obiektu
funkcji. Aby uniknąć różnic opakowując funkcję, warto skopiować te
cechy z oryginalnej funkcji. Cechy te można skopiować wprost, lub
skorzystać z dekoratora wraps z modułu functools tak jak w przykładzie
3.

**Dodatkowe argumenty** Wiemy już jak tworzyć proste dekoratory – pytanie jak je rozszerzyć
tak, aby przyjmowały dodatkowe argumenty? Można spotkać co najmniej
dwa podejścia do tego problemu. 

Rozważymy je na przykładzie rozszerzającym wcześniej opisany dekorator debug o argument prefix,
który będzie dodawany przed nazwą wywoływanej funkcji. Pierwsze
rozwiązanie zostało przedstawione w przykładzie 4 i wykorzystuje
zagnieżdżone opakowywanie funkcji. To dosyć bezpośrednie podejście
tworzy najpierw funkcję dekorującą decorate (która ma dostęp do
atrybutu prefix), a ta tworzy funkcję, która jest właściwym dekoratorem
wrap. Dla lepszego zobrazowania rozważmy taki prosty przykład:

    def a(x):
        return x

W tym przypadku takie wywołanie:

    a(a)(1)

jest całkowicie prawidłowe i zwróci 1. Jednak takie podejście ma swoje
ograniczenia – nie możemy użyć dekoratora bez podania nawiasów (zobacz
linię 17 w przykładzie).

Rozwiązanie tego problemu można znaleźć w przykładzie 5, gdzie została
użyta funkcja partial z modułu functools. Funkcja partial zwróci nam
nową funkcję, w której część argumentów zostaje zamrożona. W momencie
kiedy podamy tylko argument prefix w dekoratorze
np. `@debug(prefix='***')`, zostanie zwrócona funkcja (z zamrożonym
argumentem prefix), która przyjmuje tylko jeden argument, którym
będzie dekorowana funkcja. Czyli zachowanie to odpowiada takiemu
wywołaniu `debug(prefix='***')(add)`. Jeśli nie podamy argumentu prefix,
to funkcja zachowuje się jak dekorator z przykładu 3.

**Klasy, metody, atrybuty** Przedstawiony w przykładzie 5 dekorator zadziała również w kombinacji
z metodami, co pokazane jest w przykładzie 6. Jednak jeśli danego
dekoratora chcielibyśmy użyć dla każdej metody w klasie, takie
podejście powoduje niepotrzebne powtórzenia kodu. Rozwiązaniem jest
przygotowanie dekoratora dla klas. Kod w przykładzie 9 przedstawia
dekorator, który opakuje każda metodę dekoratorem debug z poprzednich
przykładów. Podobne podejście można zastosować dla wszystkich
atrybutów klas.


**Dekorator jako argument** Ostatni przykład 7 pokazuje jak stworzyć nowy dekorator, który
powstaje poprzez złożenie dekoratorów podanych jako argumenty. Podaną
techniką można np. wykorzystać do stworzenia dekoratora dla klas,
który każdą metodę opakowuje dekoratorami podanymi w argumentach.


### Metaklasy

#### Wstęp

Zanim omówię metaklasy warto przypomnieć sobie klika rzeczy na temat
Pythonowych klas. Skoro w Pythonie funkcje to też obiekty (sekcja 2.1)
– pytanie jak w takim razie jest z klasami.

	# --------------------------------------
	# Przykład (6) Dekoratory a klasy I
	
    class Spam(object):

        @debug
        def __init__(self): pass

        @debug
        def add(self, a, b):
            return a+b


	# --------------------------------------
	# Przykład (7) Dekoratory wykorzystujące inne dekoratory

    def composed(*decs):
        def deco(f):
            for dec in reversed(decs):
                f = dec(f)
            return f
        return deco

    @composed(debugmethods, debugattr)
    class Spam(object):
        pass

	

	# --------------------------------------
	# Przykład (8) Dekoratory i metaklasy

    class debugmeta(type):
        def __new__(cls, clsname, bases, clsdict):
            clsobj = super (cls, cls).__new__(cls, clsname, bases, clsdict)
            clsobj = debugmethods(clsobj)
            clsobj = debugattr(clsobj)
            return clsobj

    class Spam(object):
        __metaclass__ = debugmeta


	# --------------------------------------
	# Przykład (9) Dekoratory a klasy II
	
    def debugattr(cls) :
        orig_getattribute = cls.__getattribute__
        def __getattribute__(self, name):
            print("Get:", name)
            return orig_getattribute(self, name)
        cls.__getattribute__ = __getattribute__
        return cls

    def debugmethods ( cls ):
        prefix = "*** %s." % (cls.__name__,)
        for name, val in vars(cls).items():
            if callable(val):
                setattr(cls, name, debug (val, prefix)) # debug zdefiniowane wczesniej
        return cls

    @debugmethods
    @debugattr
    class Spam(object):
        def __init__(self):
            self.name = ""
            pass
        def add(self, a, b):
            return a+b

    if __name__ == "__main__":
        a = Spam()
        a.add(1, 2)
        a.name = "test"



Okazuje się, że klasy są też obiektami pierwszego rzędu. To znaczy, że można je przypisać do zmiennej, skopiować, dodać do niej atrybuty, czy przekazać jako parametr funkcji. Skoro klasy są też obiektami, muszą być przez coś generowane. W normalnych okolicznościach kiedy użyjemy słowa kluczowego class, Python utworzy obiekt automatycznie. Ale istnieje też możliwość wpłynięcia na ten proces. Zanim do tego przejdziemy, przypomnijmy sobie działanie funkcji wbudowanej type, która wywołana z jednym argumentem zwraca typ obiektu. Przykład 12 obrazuje powyżej opisane własności. Warto zwrócić uwagę na wynik ostatniej linki kodu z tego przykładu. Okazuje się, że obiekt tworzący instancje klasy jest typu type. Co więcej, type może posłużyć do tworzenia klas. Wywołanie wygląda wtedy tak: type(nazwa klasy, krotka z klasami nadrzednymi, slownik z atrybutami). Można w ten sposób utworzyć nową klasę, podać jej atrybuty (w tym metody), stworzyć obiekt tej klasy, czy nawet dziedziczyć po niej (sprawdź szczegóły w przykładzie 10).
Podsumowując, wiemy, że klasy to też obiekty, co więcej, wiemy jak te obiekty tworzyć.
	
	# --------------------------------------
	# Przykład (10) Funkcja type
	
	def napisz_cos (self): print self.cos_nowego
	NowySpam = type("NowySpam",() ,{"cos_nowego": True, "napisz_cos": napisz_cos })
	print NowySpam
	a = NowySpam()
	print a
	a. napisz_cos()
	class NowySpam2(NowySpam): pass
	b = NowySpam2()
	b.napisz_cos()

	
	# --------------------------------------
	# Przykład (11) Funkcja type

	class debugmeta(type):
		def __new__( cls ,clsname, bases, clsdict):
			clsobj = super(cls, cls).__new__(cls, clsname, bases, clsdict)
			clsobj=debugmethods(clsobj)
			clsobj = debugattr(clsobj)
			return clsobj

	class Spam(object):
		__metaclass__ = debugmeta
		"""docstring for Spamm"""

		def __init__(self):
			pass

		def add(self,a,b):
			return a+b

	class SpamChild(Spam):
		pass

	if __name__ == "__main__":
		s = SpamChild()
		s.add(1, 2)



	# --------------------------------------
	# Przykład (12) Klasy
		
	class Spam(object):
		pass

	o = Spam() #obiekt klasy Spam
	print o

	print Spam #klasa jest obiektem który może tworzyć obiekty (instancje) klasy

	def foo(a): print a

	foo(Spam) # klasa może być przekazana jako argument

	Spam.cos_nowego="bar" #można przypisac do klay atrybut
	Spam2 = Spam # przypisać kalsę do zmiennej
	print Spam2()

	print type (1) #<type ’int’>
	print type ("1") #<type ’str’>
	print type (Spam()) #<class ’__main__.Spam’>
	print type (Spam) #<type ’type’>
	

#### Implementacja

Czym w takim razie są metaklasy? Klas używamy aby tworzyć obiekty (instancje) tej klasy. Wiemy też, że klasy też są obiektami. Metaklasy są więc tym co jest odpowiedzialne za tworzenie klas. De facto, type jest metaklasą, co więcej, Python używa jej do tworzenia wszystkich klas. Nie będzie zapewne niespodzianką, że możemy stworzyć własne metaklasy i wpłynąć przez to na sposób tworzenia klas. Python w momencie tworzenia klasy sprawdza czy został zdeﬁniowany w klasie atrybut __metaclass__, jeśli tak to wykorzysta go do stworzenia klasy, w przeciwnym razie użyje metaklasy type. Co ważne, metaklasa podlega dziedziczeniu. Zobrazuję to przykładem 11, w którym metaklasa została użyta w połączeniu z dekoratorami. Klasy Spam i SpamChild (SpamChild ze względu na dziedziczenie) tworzone są przez metaklasę debugmeta, która wykorzystuje wcześniej zdeﬁniowane dekoratory. W efekcie instancja klasy SpamChild będzie logować dostęp do swoich atrybutów (oraz metod). Nie jest to jedyny sposób tworzenia metaklas – więcej szczegółów w [4].
Wszystkich zainteresowanych szerszym zgłębieniem tematu zachęcam do zapoznania się
z artykułem [4]. Warto też przytoczyć jako przestrogę wypowiedź Tima Petersa (zobacz
[4]):

*Metaclasses are deeper magic than 99% of users should ever worry about. If
you wonder whether you need them, you don’t (the people who actually need
them know with certainty that they need them, and don’t need an explanation
about why).*

### Syntetyczne funkcje, klasy i moduły

Poprzez nazwę syntetyczny obiekt odnoszę się do istniejących obiektów, dla których niekoniecznie istnieje kod źródłowy. Na przykład może to być funkcja stworzona z dynamicznie
wygenerowanego napisu (string).

Zacznę od omówienia przykładu 13, w którym z napisu (string) tworzona jest funkcja. Za pomocą exec wykonujemy kod podany jako parametr, a efekt jego działania zapisujemy w słowniku d, który będzie pełnił rolę tymczasowej przestrzeni nazw. Następnie przypisujemy do zmiennej spam obiekt odpowiadający w słowniku kluczowi ’spam’. W tym przypadku użyliśmy stałego literału, ale moglibyśmy wygenerować odpowiedni kod dynamicznie. Kolejny przykład 14 wykorzystuje techniki opisane w sekcji 3.1. Dokładniej, klasę można stworzyć poprzez odpowiednie wywołanie type. W tym przykładzie jedyna różnica jest taka, że metody klasy pochodzą z literału.

Ostatni przykład 15 obrazuje syntetyczne tworzenie modułów. Zaczynamy od stworzenia nowego modułu wykorzystując moduł new. Następnie dodajmy do nowo utworzonego modułu atrybut SyntetycznaKlasa (klasa pochodzi z wcześniejszego przykładu). Sam moduł dopisujemy do słownika modułów sys.modules. Ważna uwaga: możemy w ten sposób nadpisać/podmienić istniejący w interpreterze moduł. Następnie czyścimy przestrzeń nazw i ładujemy nasz nowy syntetyczny moduł.

Można znaleźć kilka zastosowań dla syntetycznych obiektów takich jak tworzenie: języków
domenowych (Domain-specyﬁc languages), frameworków GUI, ORM (obiektowo relacyjne
mapowanie), czy Monkey Patching (o którym poniżej).


	# --------------------------
	# Przykład (13) Funkcje syntetyczne
	
	d = {} # nasz nowy namespace
	exec "def spam(x): return x" in d
	spam = d["spam"]
	print spam(1)


	
	# --------------------------
	# Przykład (14) Klasy syntetyczne
	
	d = {}
	exec """def spam(self): print ’spam’\n
	def morespam(self): print ’morespam’
	""" in d
	
	SyntetycznaKlasa = type ("SyntetycznyKlasa", (), d)
	s = SyntetycznaKlasa()
	s.spam()
	s.morespam()



	# --------------------------
	# Przykład (15) Moduły syntetyczne

	import new , sys

	nowy_modul = new.module ("SyntetycznyModul", "Opis")
	nowy_modul.SyntetycznaKlasa = SyntetycznaKlasa
	sys.modules["SyntetycznyModul"] = nowy_modul

	del new, sys, nowy_modul, SyntetycznaKlasa

	import SyntetycznyModul

	s = SyntetycznyModul.SyntetycznaKlasa()
	s.spam ()
	s.morespam ()


### Monkey patching

Kod, który rozszerza lub modyﬁkuje istniejące obiekty w czasie działania nazywamy MonkeyPatch. MonkeyPatching jest spotykany w wielu językach dynamicznie typowanych. 

Zasadne jest pytanie, po co to robić. Modyﬁkowanie obiektów w trakcie działania znacząco zaciemnia obraz tego co się dzieje, a podobny cel można uzyskać na wiele innych sposobów (zdeﬁniowanie klasy dziedziczącej lub inne). Jednak są przypadki, w których tego typu techniki są uzasadnione. Przykładowo, gdy piszemy testy kodu, który wchodzi w interakcję z zewnętrznymi systemami (np. z bazą danych), wtedy możemy poprzez odpowiednią podmianę funkcji np. zablokować komunikację z bazą. Inne uzasadnione przypadki to sytuacje gdy korzystamy z zewnętrznych bibliotek, których działanie jest nie do końca zgodne z tym czego oczekujemy lub po prostu jest błędne. Wtedy w prosty sposób możemy podmienić kłopotliwy fragment. Oczywiście moglibyśmy uzyskać podobny efekt poprzez dziedziczenie lub napisanie wrapera, lub poprawienie kodu zewnętrznej biblioteki. Jednak nie zawsze jest to możliwe lub zasadne. Może to powodować tworzenie niepotrzebnego kodu (szczególnie gdy następne wydanie biblioteki ma naprawiać kłopotliwy kod). Bywają też sytuacje gdy nie mamy dostępu do kodu źródłowego – np. bindingi z zewnętrznej biblioteki napisanej w C i dostarczonej w już skompilowanej postaci. W takich sytuacjach napisanie prostego wrappera jest o wiele wygodniejsze. Dobrym przykładem jest nałożenie poprawki na używaną bibliotekę tak aby w komunikacji były wykorzystane np. eventlety. Monkey Patching modułów praktycznie został omówiony w przykładzie 15. Poprzez odpowiednie nadpisanie słownika sys.modules możemy podmienić cały moduł na inny (np. wygenerowany syntetycznie) lub podmienić poszczególne komponenty w module np. funkcje. Jednak wszelkie tego typu zmiany muszą być wykonane zanim jakikolwiek inny moduł załaduje modyﬁkowany/podmieniany moduł.


Przykład 16 pokazuje jak podmienić metodę na poziomie klasy, tak aby każda nowa instancja tej klasy korzystała z nowej metody. W tym celu musimy użyć MethodType z modułu types. Wywołanie ma następującą formę: MethodType(nowa metoda, obiekt, klasa). Jeśli nie podamy obiektu, metoda będzie związana z obiektem dopiero w momencie utworzenia nowego obiektu.

Natomiast w przykładzie 17 podmieniamy metodę konkretnej instancji – w tym przypadku podajemy instancję obiektu do MethodTypes.


	
	# --------------------------
	# Przykład (16) Monkey Patching Klasy

	import types
	
	class Spam(object):
		def __init__(self):
			self.x = "X"

		def foo(self):
			print "stara metoda", self.x

	def foo2(self):
		print "nowa metoda", self.x

	Spam.foo = types.MethodType(foo2, None, Spam)
	s1 = Spam()
	s1.foo() # <-- "nowa metoda"


	
	# --------------------------
	# Przykład (17) Monkey Patching Obiektu
	
	def foo3(self):
		print "kolejna metoda", self.x

	s2 = Spam()
	s2.foo = types.MethodType(foo3, s2, Spam)

	s1.foo() # <-- "nowa metoda"
	s2.foo() # <-- "kolejna metoda"


### Podsumowanie

Było to krótkie wprowadzenie do metaprogramowania. Krótkie – oznacza, że w zamierzeniu artykułu było nakreślić przedstawione tematy, a nie w pełni je omówić. Zainteresowanych zachęcam do dalszych eksperymentów (polecam bibliograﬁę). Wiele z tych technik jest niezbędnych przy tworzeniu bibliotek czy frameworków. Pomimo że metaprogramowanie w Pythonie daje nam ogromne możliwości, to należy używać go z rozwagą. Często techniki tu opisane mogą znacząco zaciemnić kod, a w konsekwencje utrudnić jego utrzymanie.


### Literatura

* [1] David Beazley. Python 3 metaprogramming. Presented at PyCon’2013, Santa Clara, CA, http://www.dabeaz.com, 2013.
* [2] Walker Hale. Python metaprogramming for mad scientists and evil geniuses. PyCon US’2012, Santa Clara, CA, http://www.youtube.com/watch?v=Adr_QuDZxuM, 2012.
* [3] http://stackoverﬂow.com/. Monkeypatch python class. stackoverflow.com/questions/3765222/monkey-patch-python-class, 2013.
* [4] http://stackoverﬂow.com/. What is a metaclass in python? http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python, 2013.
* [5] http://stackoverﬂow.com/. What is monkeypatching? stackoverflow.com/questions/5626193/what-is-monkey-patching, 2013.
* [6] http://stackoverﬂow.com/. What’s the diﬀerence between eval, exec, and compile in python? http://stackoverflow.com/questions/2220699/whats-the-difference-between-eval-exec-and-compile-in-python, 2013.
* [7] Kent S. Johnson. Decorators. http://kentsjohnson.com/kk/00001.html, 2006.
* [8] Alex Martelli. Python dependency injection. http://www.aleax.it/ytpydi.pdf,2008.
* [9] Armin Ronacher. Be careful with exec and eval in python. http://lucumr.pocoo.org/2011/2/1/exec-in-python/, 2011.
