# Python w łaziku marsjańskim? - Michał Barciś

Już od ponad dwóch lat pracujemy wspólnie z zespołem Continuum z Uniwersytetu
Wrocławskiego nad prototypem łazika marsjańskiego Aleph1. W tym czasie
rozważaliśmy wiele rozwiązań i różnych technologii, a ostatecznie duża część
robota została zaprogramowana w Pythonie. Podczas prezentacji opowiem o samym
łaziku oraz o drodze, którą przebyliśmy w czasie tworzenia go, ale w tym artykule
chciałbym trochę poszerzyć ten temat i przedstawić przegląd najciekawszych
zastosowań tego języka programowania. Wspomnę tutaj o wielu bibliotekach oraz
technologiach, których nie będę dokładnie opisywał - zainteresowany czytelnik
na pewno bez problemu znajdzie więcej informacji na ich temat w Internecie.

# Mocne strony

Jeszcze kilka lat temu, gdy poruszany był temat Pythona, częstą reakcją było
"To ten język, w którym pisze się skrypty, nadaje się to do czegokolwiek
innego?", "Poza szkołami nie ma miejsca dla Pythona, to dobry język tylko
dla początkujących", albo nawet, ze zdziwieniem, "To w Pythonie da się napisać
aplikację okienkową?".

Podczas pracy w STX Next zauważyłem jednak, że coraz częściej nawet nasi klienci
zdają sobie sprawę z tego, że Python to nie tylko aplikacje Internetowe, czy
proste skrypty służące do zarządzania serwerami. Dostarczane rozwiązania muszą
być wielośrodowiskowe, a aplikacja Internetowa nie może już tylko działać
w przeglądarce - ma rozpoznawać obrazy z kamery, analizować zbierane dane,
wizualizować je w czasie rzeczywistym [1], a czasami nawet ostatecznie włączyć
światło albo otworzyć zamek w drzwiach. Na szczęście praktycznie w każdej
z tych dziedzin możemy korzystać z lubianej
i znanej technologii - z języka Python [2][3][4].

## Serwisy Internetowe

Serwisy internetowe są typowym obszarem zastosowania języka Python [5].
Django, Pylons, Flask i wiele innych [6] sprawiają, że gdy już uporamy się z problemem,
który framework wybrać, samo tworzenie oprogramowania to pestka. Jednak według
mnie, głównym atutem Pythona na stronach internetowych jest łatwość integrowania
go z innymi usługami, które często udostępniają API w tych samych technologiach.
Dzięki temu nasza strona internetowa staje się już tylko "frontendem" do dużo
bardziej złożonych zastosowań.

## Aplikacje desktopowe

Coraz szybciej odchodzą w niepamięć, ponieważ prawie wszystko można już zrobić
w przeglądarce Internetowej. Wciąż jednak czasami preferujemy "natywne" aplikacje,
a Python sprawdza się w nich świetnie - szczególnie wtedy, kiedy aplikacja
często wchodzi w interakcję z użytkownikiem. Dzięki pakietom takim jak Tkinter,
wxPython czy PyQt tworzenie aplikacji jest szybkie i przyjemne, a interfejs
użytkownika dobrze integruje się z systemem operacyjnym.

Jednak chyba największą zaletą Pythona w aplikacjach desktopowych jest używanie
go jako narzędzia do rozszerzeń i skryptowania rozwiązań. Blender, vim i wiele
innych właśnie w ten sposób z powodzeniem wykorzystuje Pythona.

## DevOps i skrypty

Python jako język skryptowy z wbudowanym REPL (ang. read-eval-print loop)
i wieloma jego zamiennikami takimi
jak IPython, bpython, ptpython naturalnie nadaje się do zarządzania systemem
operacyjnym i plikami. Dodatkowo pakiety takie jak Plumbum [7] zapewniają, że znając
Pythona, już nigdy więcej nie będziemy musieli pisać skryptów w Bashu.

## Gry komputerowe

Co prawda raczej ciężko o duże tytuły napisane w 100% w Pythonie, jednak właśnie
ten język bardzo często wykorzystywany jest do tworzenia scenariuszy i skryptów
sterujących przebiegiem gry, które nie wymagają wysokiej wydajności i szybkości
działania. Dzięki temu scenarzyści mogą szybko i skutecznie tworzyć wciągające
światy i postaci.

## Nauczanie maszynowe

Dla mnie dużym zdziwieniem było jakim cudem właśnie w tej dziedzinie Python
zdobył taką dużą popularność. Jednak już po pierwszym projekcie zrozumiałem, że
to dzięki możliwości łatwego i dobrze ustandaryzowanego przetwarzania danych
z niewielkim narzutem pamięciowym. Dodatkowo biblioteki takie jak NumPy
umożliwiają szybkie wykonywanie operacji arytmetycznych na tych danych. Wiele
algorytmów nauczania maszynowego można sprowadzić do operacji na macierzach.
Tam, gdzie mimo to wydajność jest problemem, stosuje się silniki pisane na
przykład w C/C++ i udostępniające API do Pythona, dzięki czemu możemy szybko
i wydajnie eksperymentować na modelach.

Dodatkowo, społeczność wytworzyła wiele darmowych narzędzi umożliwiających łatwą
pracę z dużą ilością danych. Od bibliotek służących do wizualizacji, takich jak
matplotlib, poprzez łatwą prezentację danych w Jupyter Notebook (kiedyś IPython
Notebook), aż po frameworki do pracy z danymi takie jak Pandas, czy
scikit-learn [8].

## Mikrokontrolery i automatyka

O dziwo, nawet przy bardzo niskopoziomowym programowaniu coraz częściej słyszy
się o Pythonie - a to głównie za sprawą projektu MicroPython [9], który umożliwia
uruchamianie kodu Pythona na systemach wbudowanych. Czy ma to sens, czy od
takich systemów nie oczekuje się raczej szybkości, niezawodności, wykorzystania
każdego cyklu procesora? Według mnie ma - nawet najmniejsze procesory są coraz
bardziej wydajne i często potrzebują wykonać tylko najprostsze operacje, np.
odebrać pakiet z sieci i włączyć światło. Chcielibyśmy móc tego typu urządzenia
programować szybko i być pewni, że logika przez nie wykonywana zgadza się z tym,
co oczekujemy i właśnie to jest nam w stanie zapewnić krótki i przejrzysty kod
w Pythonie.

## Robotyka

To chyba jedno z najciekawszych zastosowań Pythona i z roku na rok coraz
bardziej popularnych, co widać na przykład po szybkim rozwoju projektu ROS [10]
(Robot Operating System), który jest swoistym frameworkiem do tworzenia różnych
wysoce zautomatyzowanych urządzeń i systemów. Roboty to nie tylko niskopoziomowy
kod często wymagający pracy w czasie rzeczywistym oraz maksymalnego
wykorzystania zasobów. W każdym robocie jest jakaś część logiki odpowiedzialna
za podejmowanie wysokopoziomowych decyzji, takich jak na przykład wybór miejsca,
do którego robot ma się przemieścić, czy który przycisk wcisnąć. Python
doskonale się do tego nadaje - zazwyczaj nie są to operacje wymagające pracy
w czasie rzeczywistym, a świetna integracja z systemami do nauczania maszynowego
umożliwia pełne wykorzystanie zasobów. Dodatkowo dużo łatwiej w Pythonie
stworzyć prototyp, na podstawie którego wyodrębnione zostaną komponenty, które
należy przepisać np. do C w celu poprawy wydajności.

# A kiedy Python może nie wystarczyć?

Python nie zawsze będzie idealnym rozwiązaniem. Najczęściej
przywoływanym problemem są aplikacje czasu rzeczywistego, szczególnie te
wymagające bardzo szybkich odpowiedzi. I faktycznie, raczej nie użyłbym tego
języka podczas programowania regulatora silników dużych prędkości, jednak
w momencie, gdy mówimy o decyzjach podejmowanych w setnych sekundy, czemu nie?
Garbage collector zawsze można wyłączyć w kluczowych momentach, a dzisiejsze
procesory często mają bardzo duży zapas mocy obliczeniowej. W ostateczności nasz
program można traktować jako prototyp, który pozwoli nam łatwo znaleźć miejsca
wymagające optymalizacji, albo po prostu za szablon aplikacji stworzonej
w innej technologii.

Python może również nie sprawdzić się w programach, które wymagają dużej ilości
obliczeń - symulacje, silniki gier komputerowych, dekodowanie danych. Na
szczęście w takim wypadku zawsze możemy wyodrębnić krytyczne części kodu
i zrealizować je w innej technologii.

Podsumowując, wszechstronność Pythona jest wyjątkowo mocną cechą tego języka
i warto z niej korzystać - w końcu możemy tworzyć zupełnie nowe rzeczy i rozwijać
nasze zainteresowania w wielu dziedzinach w technologii, którą już dobrze znamy
i lubimy, dzięki czemu próg wejścia jest znacznie mniejszy.

## Bibliografia

1. Python success stories. https://www.python.org/about/success/usa/
2. Python i aplikacje czasu rzeczywistego.\crlf https://stackoverflow.com/a/15011981/540717
3. Lista aplikacji. https://wiki.python.org/moin/Applications
4. Lista aplikacji. https://en.wikipedia.org/wiki/List`_`of`_`Python`_`software
5. Python i web development. https://worthwhile.com/blog/2016/07/19/django-python-advantages/
6. Frameworki webowe w Pythonie. https://wiki.python.org/moin/WebFrameworks
7. Plumbum. http://plumbum.readthedocs.io/
8. SciKit learn. http://scikit-learn.org/
9. MicroPython. https://micropython.org/
10. ROS. http://www.ros.org/
