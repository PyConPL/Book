# Mechanizm importowania w języku Python
## Konrad Hałas

Instrukcja import znana jest każdemu programiście piszącemu kod w Pythonie. Była to najprawdopodobniej jedna z pierwszych poznanych konstrukcji składniowych podczas uczenia się naszego ulubionego języka. Jednak czy zdajemy sobie sprawę co dzieje się pod maską intepretra gdy używamy słowa kluczowego import? Ogólnie znanych faktów jest kilka: instrukcja import pozwala na nam na ładowanie innych modułów do naszego kodu oraz przypisywaniu ich do zmiennych. Dzięki jej istnieniu możemy dzielić nasz projekt na mniejsze części oraz zarządzać połączeniami między nimi. Jednak to tylko efektt jej działania. Maszyneria odpowiedzialna za proces importowania w Pythonie to dość skomplikowanym systemem, jednak dającym się ujarzmić. Co ważniejsze - system ten jest w pełni rozszerzalny z poziomu języka. Zapoznanie się z jego budową pomoże nam lepiej zrozumieć sam język oraz rządzące nim prawa. Znając możliwości systemu importowania, nie damy się zaskoczyć niemożliwymi na pierwszy rzut oka zachowaniami projektów, które właśnie owy system modyfikują. Zanim jednak przejdziemy do pisania własnych rozszerzeń, spójrzmy jak wygląda proces importowania od strony składniowej.

W gramatyce języka Python 3.3 instrukcja import zdefiniowana jest w następujący sposób:

	import_stmt: import_name | import_from
	import_name: 'import' dotted_as_names
	import_from: ('from' (('.' | '...')* dotted_name | ('.' | '...')+)
				  'import' ('*' | '(' import_as_names ')' | import_as_names))
	import_as_name: NAME ['as' NAME]
	dotted_as_name: dotted_name ['as' NAME]
	import_as_names: import_as_name (',' import_as_name)* [',']
	dotted_as_names: dotted_as_name (',' dotted_as_name)*
	dotted_name: NAME ('.' NAME)*

Analizując powyższą definicję można dojść do wniosku, że programista chcący zaimportować inny moduł może to zrobić na kilka sposobów. Zakładając, że posiadamy pakiet spam z modułem eggs w środku, możliwości są następujące:

	import spam
	import spam as bacon
	import spam.eggs
	from spam import eggs
	from spam import eggs as bacon
	from .spam import eggs 
	from . import eggs 

Tych kilka przykładów w wystarczającym stopniu pokazuje instrukcję import od strony składniowej. Do dyspozycji mamy takie warianty jak: proste importowanie, importowanie z pakietu przy użyciu pełnej nazwy kwalifikowanej lub instrukcji from-import, importowanie wraz z przypisaniem do innej nazwy oraz importowanie relatywne. Wszystkie z wymienionych wariantów muszą być obsługiwane przez system importów w języku Python.

Zacznijmy od najprostszego wariantu - posiadamy moduł spam i chcemy go zaimportować. Nasza instrukcja import będzie wyglądać następująco:

	import spam

Pierwszym krokiem jaki zostanie wykonany po napotkaniu takiego wyrażenia, będzie sprawdzenie czy importowany moduł nie został załadowany już wcześniej. Świadczyć o tym może obecność odpowiedniego wpisu w słowniku sys.modules. Słownik ten jest swojego rodzaju mechanizmem cache pierwszego poziomu dla systemu importów. Mapuje on nazwy modułów na ich instancje. W naszym wypadku zostanie sprawdzone istnienie klucza "spam". Jeżeli moduł spam nie był wcześniej zaimportowany, nie będzie go w słowniku sys.modules. W innym wypadku do lokalnej zmiennej spam zostanie przypisana wartość wyrażenia sys.modules[‘spam’], 

Po nieudanej próbie ze słownikiem sys.modules, mechanizm importowania sięga po listę `sys.meta_path`. Elementami tej listy są obiekty znane w nomenklaturze jako "findery" - potrafią one odpowiedzieć na jedno pytanie: "czy wiesz jak znaleźć dany moduł?" W tym celu każdy z nich musi implementować metodę find_module, przyjmującą dwa parametry: nazwę modułu oraz listę ścieżek. Nazwa moduły to pełna nazwa kwalifikowana. W naszym wypadku będzie to łańcuch znaków "spam". Drugim parametrem jest lista ścieżek pakietu z którego importowany jest dany moduł, najczęściej zawiera ona jeden element. Lista ta jest dłuższa tylko w wypadku pakietów przestrzeni nazw, które nie będą tutaj omawiane. Gdy importowany jest moduł najwyższego poziomu, tak ja w naszym przykładzie, drugi parametr przyjmuje wartość None. Metoda `find_module` powinna zwrócić "loader" (o którym opowiemy zaraz) gdy "finder" potrafi znaleźć dany moduł lub None w przypadku przeciwnym. System importów w Pythonie iteruje po liście sys.meta_path i wywołuje na każdym z elementów metodę find_module, aż do momentu gdy jeden z finderów zwrócić coś innego niż None. W przypadku negatywnej odpowiedzi wszystkich finderów i osiągnięcia końca listy, generowany jest wyjątek ImportError.

Poniżej znajduje się prosty przykład "findera", który jedynie wypisuje na standardowe wyjście próbę znalezienia loadera dla zadanego modułu:

	class PrintFinder:

		def find_module(self, name, path):
			print(‘Try to find module {} with path {}.’.format(name, path))
			return None

W celu aktywowania "findera" PrintFinder musimy dodać instancję tej klasy do listy sys.meta_path, najlepiej na jej początek, aby był to pierwszy odpytywany finder:

	>>> sys.meta_path.insert(0, PrintFinder())

Zobaczmy zatem czym poskutkuje próba wykonania wspomnianej instrukcji import:

	>>> import spam
	Try to find module spam with path None.

Tak jak zakładaliśmy - metoda find_module została wywołana z parametrami "spam" oraz None. Gdyby jednak spam był pakietem z modułem eggs w środku zobaczylibyśmy następującą sekwencję:

	>>> import spam.eggs
	Try to find module spam with path None
	Try to find module spam.eggs with path ['./spam']

Eksperyment ten obrazuje nam bardzo ważny fakt - podczas próby importowania podmodułu, importowana jest także pakiet do którego dany moduł należy. Dlatego też najpierw na standardowym wyjściu zobaczyliśmy próbę znalezienia loadera dla pakietu spam, a dopiero później dla modułu spam.eggs. Drugie wywołanie metody `find_module` otrzymało także jako parametr jednoelementową listę ścieżek pakietu do którego należy dany moduł. Podobną sekwencję wywołań metody find_module uzyskalibyśmy korzystając z instrukcji from spam import eggs. Jedyne różnica to zmienna jaką będziemy mieli dostępną w zasięgu po wywołaniu instrukcji import - w pierwszym wypadku będzie to spam z atrybutem eggs (czyli spam.eggs) a w drugim samo eggs.

Zanim przejdziemy do tworzenia własnego loadera, zobaczmy jakie findery domyślnie znajdują się na liście sys.meta_path.

	>>> sys.meta_path
	[_frozen_importlib.BuiltinImporter,
	 _frozen_importlib.FrozenImporter,
	 _frozen_importlib.PathFinder]

Pierwszy z nich, BuiltinImporter, odpowiedzialny jest za obsługę modułów wbudowanych. Klasa ta jest jednocześnie finderem i loaderem. Tego typu klasy nazywane są w nomenklaturze importerami - stąd suffix *Importer w nazwie. W takim wypadku metoda find_module w przypadku pozytywnej odpowiedzi na pytanie "czy wiem jak znaleźć dany moduł?" zwraca instancję na rzecz której została wywołana, czyli self.

Kolejnym importerem jest FrozenImporter - jego zadaniem jest importowanie modułów typu "frozen". W dużym skrócie są to moduły połączone wraz z interpreterem w postać binarną, które mogą być uruchamiane na maszynach nie posiadających Pythona.

Ostatnim elementem listy `sys.meta_path` jest klasa PathFinder. Z jej nazwy można wywnioskować, że finder ten obsługuje moduły, których lokalizację można określić ścieżką. To tutaj najczęściej zatrzymuje się wywoływana przez nas instrukcja import i to ten finder daje najczęściej pozytywną odpowiedź. Funkcjonalność klasy PathFinder jest całym podsystemem wewnątrz omawianego systemu importów i nie zostanie on opisany w ramach niniejszego artykułu. Warto wspomnieć jednak, że klasa ta działa w oparciu o listę sys.path oraz korzysta z kolejnego poziomu finderów umieszczonych na liście sys.path_hooks. Cachem dla systemu importów opartych o ścieżki jest słownik `sys.path_importer_cache`. Teraz jednak przyjrzyjmy się bliżej loaderom - czyli obiektom zwracanym przez elementy z listy sys.meta_path.

Jak sama nazwa wskazuje, loader, czyli obiekt zwrócony jako wynik metody `find_module`, odpowiedzialny jest za ładowanie modułów. W celu załadowania modułu system importów wywołuje na nim metodę load_module przyjmującą jeden argument - pełną kwalifikowaną nazwę modułu. Metoda ta powinna zwrócić obiekt modułu lub rzucić wyjątek ImportError w przypadku gdy nie może tego zrobić.

Metoda load_module wygląda prosto tylko na pierwszy rzut oka. Zadanie które jej powierzono powinna wykonać w ściśle określony sposób. Po pierwsze musi ona sprawdzić czy w słowniku sys.modules nie znajduje się już moduł, który zadano jej załadować. Jeżeli tak, wersja modułu z sys.modules powinna zostać użyta do dalszych operacji. Zachowanie takie jest konieczne w przypadku przeładowywania modułu przy pomocy funkcji imp.reload. Jeżeli nie istnieje element dla danego modułu w sys.modules, powinien on zostać tam dodany. Co ważne, operacja dodania powinna zostać przeprowadzona przed wykonaniem kodu ładowanego modułu. Rozwiązanie takie pomaga uniknąć nieskończonej rekurencji w przypadku gdy ładowany moduł - pośrednio lub bezpośrednio - ładuje sam siebie. Obiekt umieszczany w słowniku sys.modules powinien być instancją klasy types.ModuleType.

Loader ma za zadanie ustawienie także następujących wartości w ramach obiektu modułu:
__file__ - plik z którego dany moduł został załadowany. Wartość ta nie jest wymagana, jednak loader może ją ustawić jeżeli ma to sens dla rozpatrywanego modułu. 
__name__ - nazwa modułu. Wartość ta nie jest wymagana, jednak jej ustawienie jest zalecane. W przypadku tworzenia modułu przy użyciu klasy types.ModuleType wartość ta jest ustawiana automatycznie. 
__path__ - lista ścieżek dla danego pakietu. Wartość ta musi zostać ustawiona jeżeli moduł jest pakietem. Lista ta może być pusta, jeżeli istnienie jej elementów nie ma sensu w przypadku rozpatrywanego modułu.
__package__ - pakiet do którego należy dany moduł lub pusty łańcuch znaków w przypadku modułów najwyższego poziomu. Wartość ta nie jest wymagana.
__loader__ - loader, który załadował dany moduł. Wartość ta musi zostać ustawiona. Wykorzystywana jest on głównie na potrzeby introspekcji i przeładowywania modułów.

Po ustawieniu tych wartości loader powinien wykonać załadowany kod w przestrzeni nazw stworzonego modułu.

Ponieważ jeden listing wart jest więcej niż tysiąc słów, przyjrzyjmy się prostemu przykładowi. Poniżej został przedstawiony importer, czyli obiekt będący jednocześnie finderem oraz loaderem. Jego zadanie jest proste: za każdym razem gdy odnotowana zostanie próba zaimportowania modułu o podanej nazwie, moduł ten powinien zostać stworzony dynamicznie. Importer powinien także wykonać w ramach przestrzeni nazw stworzonego modułu kod, przekazany jako łańcuch znaków podczas tworzenia instancji importera.

	import sys
	import types


	class DynamicImporter:

		def __init__(self, name, code):
			self.name = name
			self.code = code

		def find_module(self, name, path):
			if name == self.name:
				return self
			else:
				return None

		def load_module(self, name):
			if name in sys.modules:
				module = sys.modules[name]
			else:
				module = types.ModuleType(name)
				sys.modules[name] = module
			module.__loader__ = self
			exec(self.code, module.__dict__)
			return module


Przykład użycia stworzonego importera:

	>>> sys.meta_path.insert(0, DynamicImporter('spam', 'eggs = True'))
	>>> import spam
	>>> spam
	<module 'spam' (<DynamicImporter object at 0x105a55450>)>
	>>> spam.eggs
	True

Pokrótce omówmy działanie klasy DynamicImporter. Podczas tworzenia jej instancji, klasa ta przyjmuje dwa argumenty - name i code. Pierwszy z nich to nazwa modułu na jaki ma zareagować nasz importer. Drugim parametrem jest łańcuch znaków, który powinien być poprawnym składniowo kodem języka Python. Metoda `find_module` składa się z prostej instrukcji warunkowej, sprawdzającej czy nazwa modułu, który ma być załadowany równa jest self.name. W takim wypadku zwracana jest instancja na rzecz której została wywołana metoda find_module, czyli self. W przeciwnym wypadku zwracana jest wartość None. Metoda load_module sprawdza czy importowany moduł nie znajduje się już w słowniku sys.modules, jeżeli tak, zostanie on wykorzystany ponownie. Gdy w sys.modules nie ma szukanej wartości rozpoczyna się proces tworzenia modułu. Moduł jest instancją klasy types.ModuleType stworzoną przy wykorzystaniu parametru oznaczającego nazwę modułu. Stworzony moduł dodawany jest do słownika sys.modules, czyli cache wszystkich załadowanych modułów. Kolejnym krokiem jest ustawienie odpowiednich wartości w obiekcie modułu. W naszym wypadku jest to tylko __loader__, ponieważ pozostałe atrybuty nie mają w rozpatrywanym przykładzie sensu (tzn. __file__, __path__, __package__). Przed zwróceniem modułu, dostarczony do klasy DynamicImporter kod (self.code), wykonywany jest (exec) w jego przestrzeni nazw (module.__dict__).

Przedstawiony importer ma oczywiście jedynie walory demonstracyjne. Sensownym przykładem, którego wytłumaczenie musiałoby zająć niestety o wiele więcej miejsca i mogłoby zaciemnić istotę problemu, byłby np. importer ładujący modułu ze wskazanego adresu URL z wykorzystaniem protokołu HTTP.

W ten sposób dotarliśmy do końca opisu systemu importowania w Pythonie. Wiemy już, że umieszczając instancję klasy implementującej odpowiednie metody (`find_module` i `load_module`) na liście sys.meta_path możemy przejąć kontrolę nad mechanizmem kryjącym się za instrukcją import. 

* [http://docs.python.org/3/reference/import.html](http://docs.python.org/3/reference/import.html) - dokumentacja systemu importowania
* [http://www.python.org/dev/peps/pep-0302/](http://www.python.org/dev/peps/pep-0302/) - PEP opisujący system importowania
* [http://docs.python.org/3/reference/grammar.html](http://docs.python.org/3/reference/grammar.html) - gramatyka języka

