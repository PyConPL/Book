# Latający wąż, czyli szybkie prototypowanie sprzętu przy pomocy Pythona - Damian Gadomski

Artykuł ten dotyczy prototypowania sprzętu na platformie MicroPython. W pierwszej części omówiona została implementacja języka na mikrokontolery z rodziny ARM, dostępne biblioteki oraz pokrewny projekt pyBoard. Dokonano porównania wydajności MicroPythona względem innych popularnych platform, a także opisano budowę i zasadę działania dronów latających w zakresie umożliwiającym zrozumienie problemów, przed którymi staje sterownik lotu takiego urządzenia.

## Wstęp

Czasami zdarzają się projekty bardziej skomplikowane niż inne. Takie, gdzie nie do końca wiadomo w jaki sposób osiągnąć oczekiwany rezultat. Takie, gdzie potrzeba trochę pracy badawczej i testów, bo zagadnienie nad którym pracujemy nie ma oczywistego rozwiązania. Często też nie wiadomo jaki rezultat będzie najbardziej użyteczny i praktyczny. Chcielibyśmy wtedy mieć możliwość zrobienia prototypu, który stale będziemy ulepszać. Dobrze jeśli kolejne zmiany nie będą obarczone dużym kosztem, ich wprowadzenie będzie szybkie. Może nawet chcielibyśmy przetestować kilka algorytmów jednocześnie?

### Inteligentna łazienka

Nie musi to być od razu ogromny system, lecz po prostu, niewielki problem do rozwiązania. Przykładem może być kwestia włączania ogrzewania i wyciągu (wentylatora) w inteligentnej łazience. Po wzięciu prysznica chcielibyśmy, żeby ręcznik odwieszony na grzejnik jak najszybciej wysechł, a wentylator jak najszybciej pozbył się wilgoci z łazienki. Wbrew pozorom nie jest to takie banalne.  W jaki sposób wykryć, że ktoś wziął prysznic? Odpowiednio długo zapalone światło, podwyższona wilgotność w łazience? Jaka zmiana wilgotności świadczy o wziętym prysznicu? A może właśnie zostało rozwieszone pranie? Jak długo grzejnik powinien być włączony aby ręcznik wysechł? Jak długo powinien działać wentylator? Powinien uruchomić się od razu, czy po wyjściu z łazienki?

Chyba nalepiej zrobić prototyp, w którym później można „wyregulować” kilka parametrów, aby dostosować go idealnie do potrzeb.

## Micropython i pyBoard

Od dłuższego czasu powstają kolejne projekty, mające na celu uprościć programowanie sprzętu: Arduino, SparkCore (obecnie Particle) czy chociażby Raspberry Pi. Od ponad roku dostępny jest również MicroPython, czyli implementacja języka Python na mikrokontrolery z rodziny ARM. Projektowi temu towarzyszy pyBoard, czyli projekt prostej płytki prototypowej na której działa MicroPython.

### Język i dostępne biblioteki

MicroPython to implementacja języka Python w wersji 3.4. Co ważne, zaimplementowany został cały język. Mamy więc do dyspozycji wszystkie konstrukcje, począwszy od wyjątków, poprzez list i dict comprehensions, a na wyrażeniach lambda skończywszy.
W mikrokontroler wbudowane są również poniższe standardowe biblioteki:
 - cmath
 - gc
 - math
 - os
 - select
 - struct
 - sys
 - time

Należy wspomnieć, że bardzo dynamicznie tworzone są nowe mikrobiblioteki. Mamy do dyspozycji chociażby moduły do wyrażeń regularnych, dekodowania i kodowania JSON, kompresję zlib, i wiele więcej. Temat ten jest bardzo żywy. W momencie pisania artykułu ostatnie zmiany w repozytorium `micropython/micropython-lib` na Githubie miały miejsce kilka godzin temu.

### Część sprzętowa - moduł pyb

Poza wszystkimi rzeczami jakie możemy robić w "zwykłym" Pythonie, musi być oczywiście coś jeszcze. Najbardziej charakterystycznym modułem dla MicroPythona jest moduł `pyb`. Daje on swobodny, wysokopoziomowy dostęp do peryferiów mikrokontrolera. Dzięki niemu używanie przetworników analogowo - cyfrowych i cyfrowo analogowych, akcelerometru, serwomechanizmów, przerwań, interfejsów UART, I2C, SPI itd. jest banalnie proste i sprowadza się przeważnie do jednej czy dwóch linijek kodu.
To temu modułowi MicroPython zawdzięcza tak duży potencjał do tworzenia szybkich prototypów.
Wszelkich prostych czujników użyjemy pisząc jedną linijkę kodu, sterowanie serwomechanizmem ramienia robota to druga linijka. Zapalenie żarówki to podłączenie układu wykonawczego i trzecia linijka. Do tego trochę logiki w Pythonie i prototyp gotowy.

### Wydajność

Kompilacja kodu dla MicroPythona jest wieloetapowa, w ostatnim etapie domyślnie generowany jest bajtkod, który jest później uruchamiany na wbudowanej w MicroPythona maszynie wirtualnej. Takie jest zachowanie domyślne, zoptymalizowane względem zajętości pamięci RAM, której na mikrokontrolerze jest niewiele. Możliwa jest jednak zmiana domyślnego emitera kodu na natywny oraz natywny z optymalizacją (nazwany `viper`). Aby użyć niedomyślych emiterów wystarczy zastosować dekoratory, odpowiednio: `@micropython.native` i `@micropython.viper`. Kod metody pozostaje bez zmian, jedynie dekorator jest informacją dla kompilatora.

Aby zobrazować różnice w szybkości działania i zajętości pamięci przy użyciu trzech powyższych emiterów, weźmy metodę która ma zapalić i zgasić diodę LED milion razy. Wyniki to:
 - domyślny bajtkod: 44 bajty pamięci, czas 10,4 sekund
 - natywny: 126 bajtów pamięci, czas 6,3 sekundy
 - „viper”: 114 bajtów pamięci, czas 5,0 sekundy

Dla porównania, odpowiedni kod napisany w C na Arduino (16MHz) wykonuje się około 7 sekund, a na Raspberry Pi (700MHz) około 300 ms. Natomiat odpowiedni kod napisany w Pythonie również na Raspberry Pi wykonuje się niespełna 20 sekund!

Podandto istnieje czwarty emiter przydatny dla krytycznych fragmentów, który pozwala pisać wstawki bezpośrednio w assemblerze. Niestety nie ma możliwości pisania wstawek w języku C.

## Drony latające

Mikrośmigłowce wielowirnikowe zwane potocznie dronami czy quadrokopterami stały się w ostatnim czasie bardzo popularne w wielu zastosowaniach. Bezzałogowe statki powietrzne swoje początki zawdzięczają celom militarnym, ale dzięki stabilności i łatwości kontroli dronów wielowirnikowych, urządzenia te zyskują popularność w zastosowaniach cywilnych, jak na przykład kinematografia.

### Budowa dronów i fizyka silników

Klasycznym, najczęściej spotykanym wielowirnikowcem jest quadrokopter o symetrycznych ramionach. W centrum konstrukcji znajdują się wszelkie czujniki, moduły łączności bezprzewodowej i mikroprocesorowy sterownik lotu. Do centralnej części urządzenia przymocowane są cztery symetrycznie rozstawione ramiona o identycznej długości. Na końcu każdego z ramion znajduje się silnik elektryczny poruszający śmigłem.

Parametrem każdego silnika jest jego ciąg oraz moment obrotowy. Ciąg charakteryzuje siłę równoległą do osi obrotu śmigła, jaką silnik jest w stanie wytworzyć. Moment obrotowy zaś, definiuję siłę jaka będzie obracać silnik wokół osi obrotu śmigła. Obie te składowe należy wziąć pod uwagę przy analizie sił działających na mikrośmigłowiec, aby zagwarantować stabilny lot. W szczególności, nie zrównoważony moment obrotowy będzie "obracał" dronem wokół pionowej osi.

W urządzeniach latających, zbudowanych w oparciu o wiele silników wytwarzających ciąg przeciwstawny sile grawitacji, istnieje możliwość zrównoważenia momentów obrotowych poprzez odpowiednie dobranie kierunków obrotu poszczególnych silników. W typowym quadrokopterze silniki na sąsiadującyh ramionach powinny obracać się w przeciwnych kierunkach. Dzięki takiemu ustawieniu momenty obrotowe silników znoszą się, ponieważ dla każdego kierunku obrotu mamy taką samą liczbę silników.

### Fizyczne podstawy sterowania lotem. 

W klasycznym quadrokopterze sterowaniu podlegają cztery silniki. 
Wysokość urządzenia nad powierzchnią ziemi można sterować równomiernie zwiększając moc każdego z silników. 
Obracanie następuje przy zwiększeniu mocy dwóch przeciwległych silników i zmniejszeniu dwóch pozostałych. Dzięki temu sumaryczny ciąg pozostanie bez zmian i powstanie niezerowy moment obrotowy, który obróci urządzenie.
Nachyleniem urządzenia względem płaszczyzny ziemi steruje się zwiększając moc jednego z silników, nieznacznie obniżając przy tym pozostałych.

### Czujniki

Aby sterowanie lotem urządzenia było możliwe niezbędne jest posiadanie informacji o stanie w jakim obecnie pojazd się znajduje. Z takiego punktu widzenia koniecznym jest wykorzystanie poniższych czujników przy konstrukcji koptera:
 - Żyroskop – pozwala mierzyć położenie kątowe co pozwoli ocenić pod jakim kątem do płaszczyzny ziemi znajduje się urządzenie.
 - Akcelerometr – pozwala mierzyć przyspieszenie (we wszystkich trzech wymiarach), wspomaga pracę żyroskopu
 - Barometr – pozwala zmierzyć zmianę wysokości. Jako, że ciśnienie powietrza maleje wraz z wysokością możliwa jest ocena zmiany wysokości na jakiej znajduje się urządzenie. Dostępne są barometry pozwalające na pomiary z dokładnością do dziesiątek centymetrów
 - Magnetometr – pozwala zmierzyć pole magnetyczne a tym samym ustalić położenie statku powietrznego względem kierunków świata. Jest niezbędny do stabilizacji ruchu obrotowego urządzenia.

### Regulatory

Dane zebrane ze wszystkich czujników muszą zostać odpowiednio przetworzone, aby mogły zostać wykorzystane do sterowania lotem wielowirnikowca. Mamy tutaj do czynienia z pętlą sprzężenia zwrotnego. Wskazania czujników odpowiadają pewnemu stanowi, chcąc np. przechylić drona, zmieniamy moc silników, co skutkuje zmianą położenia urządzenia, a więc też zmianą wskazań czujników. Problemem jest znalezienie algorytmu, który tak dobierze moc silników, aby jak najszybciej osiągnąć zamierzony stan.

Klasycznym rozwiązaniem tego problemu jest regulator PID. Na początku obliczamy różnicę pomiędzy stanem obecnym, a oczekiwanym (np. wysokości statku powietrznego nad poziomem ziemi) i nazywamy ją błędem. Wyjście regulatora jest sumą trzech składowych:
 - P (proporcjonalnej) – jest to proste przemnożenie błędu przez stałą Kp. Różnica pomiędzy stanem obecnym a oczekiwanym.
 - I (całkowej) – przemnożenie całki błędu po czasie przez stałą Ki. Zadaniem tej części jest akumulowanie błędów z „przeszłości” tzn. kompensowanie stałych błędów.
 - D (różniczkowej) – przemnożenie pochodnej błędu po czasie przez stałą Kd. Część różniczkująca jest szczególnie wrażliwa na nagłe zmiany błędu. Przyspiesza osiągnięcie zadanego położenia zwiększając szybkość reakcji.

Kluczowe znaczenie dla stabilności lotu i odpowiedniej reakcji urządzenia jest poprawne dobranie parametrów Kp, Ki i Kd. Jest to problem trudny, dla którego nie istnieją proste algorytmy. Współczynniki te dobiera się doświadczalnie, pamiętając o ich znaczeniu.

## Podsumowanie

Dzięki łatwości z jaką można zacząć pracę z MicroPythonem, szeregiem wysokopoziomowych bibliotek do obsługi sprzętu oraz prostym (w porównaniu do C) w użyciu językiem MicroPython wydaje się być idealną platformą do tworzenia prototypów sprzętu. Nie bez znaczenia pozostaje również maksymalnie uproszczony „deployment” - zaprogramowanie układu oraz dostępna konsola REPL.

Na pewno układ ten nie jest rozwiązaniem wszystkich sprzętowych problemów, ale warto mieć świadomość możliwości jakie ze sobą niesie.

### Źródła

* Damien George “MicroPython – Python for microconterollers” \hyphenatedurl{http://micropython.org/}
* Kick Starter - Micro Python: Python for microcontrollers \hyphenatedurl{https://www.kickstarter.com/}
* Jake Edge Micro "Python on the pyboard" \hyphenatedurl{http://lwn.net}
* Damien George "The 3 different code emitters" Update #4 on \hyphenatedurl{https://www.kickstarter.com}
* Lauren Orsini „Why Copters Are The Next Big Thing In Robotics” \hyphenatedurl{http://readwrite.com}
* Oscar Liang „Quadcopter PID Explained and Tuning” \hyphenatedurl{http://blog.oscarliang.net}
* Naresh Kumar Thanigaivel „Building a Quadcopter” \hyphenatedurl{http://unmannedmulticopter.blogspot.com}
