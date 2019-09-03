# Jak pracować z programującymi nieprogramistami

Jacek Bzdak <jacek@logicai.io>, Magdalena Wójcik <magda@logicai.io>

## Streszczenie

W prezentacji chcemy przedstawić trudności jakie pojawiają się w
pracy na linii programiści - programujący nieprogramiści, które wynikają z naszego doświadczenia. Dotyczą one zarówno kwestii
jakości kodu, wykorzystywanych narzędzi czy środowiska pracy.
Dla każdego z problemów zaprezentujemy rozwiązania, które stosujemy w
naszej codziennej pracy. Prezentacja będzie opierała się na dwóch punktach
widzenia - programisty i Data Scientistki. Poniższy artykuł zawiera spis
technicznym zagadnień. W artykule poruszamy głównie kwestie związane z zespołem Data Science, ale w prezentacji powiemy też współpracy z innymi grupami, np. elektronikami. 

## Wstęp
### Disclaimer

1. Podane niżej pomysły sprawdzają się w "młodym" zespole w consultingowym startupie,
   który realizuje dużo małych projektów[1],
2. Relatywnie rzadko robimy projekty Big Data, większość z nich da się zrobić
   na jednej maszynie (nawet jeśli jest to “duża” instancja),
3. Jeśli masz terabajty danych i od lat tworzysz produkt możliwe, że rozwiązania te
   mogą nie być optymalne.

### Jak wygląda praca Data Scientista?

Projekty Data Science (DS) są podobne do projektów stricte programistycznych,
ale mają też swoje specyficzne elementy, które wymienimy poniżej.

 Zwykle praca przebiega następująco:

1. Rozmowa z klientem, zebranie wymagań i potrzeb, określenie jaki cel
   biznesowy ma osiągnąć model Machine Learningowy (ML);
2. Analiza i czyszczenie danych, co może zająć nawet 90% czasu całego projektu,
   jeśli dane zawierają dużo błędów i szumu; W ramach tego kroku powstają
   tzw. Transformery czyli skrypty przygotowujące dane do postaci odpowiedniej
    dla modelu ML;
3. Trenowanie modelu ML;
4. Przekazanie wyników do klienta. Wynik może być zarówno gotowym produktem, mikroserwisem Data Science, jak i raportem/prezentacją.

# Praca z Data Scientistami/kami
## Wspólne ustalenie API, które jest zrozumiałe dla obu stron
Często da się opracować API między częścią *programistyczną* oraz częścią
 *Data Sciencową*.

Ważne uwagi:

1. API musi być zrozumiałe dla wszystkich, w praktyce podlega bardzo dokładnemu
   przeglądowi kodu, i **wszyscy** muszą być pewni, że jest dobre,
2. Należy być otwartym na jego refaktoryzację.

### Co może się nie udać?
Narzucenie API zrobionego tak, żeby było “elegancko” i zgodnie z
obowiązującą modą programistyczną, bez patrzenia na przejrzystość API. 
Dla nieprogramistycznej części zespołu to przepis na ciągłe ignorowanie API
i świadczenie supportu programistycznego przy nawet prostych zmianach.

## Przeglądy kodu jako okazja do ulepszenia praktyk

Czasem przeglądy kodu są nieprzyjemne, ale w naszej firmie dbamy o to,
żeby było miło, więc przeglądy kodu *nie są* okazją do *gate keepingu*
(czyli nie służą do tego, żeby odrzucać zmiany, które nie spełniają standardów).
Przeglądy są dobrą okazją do poprawy praktyk przyjętych w firmie.

W większości projektów mamy ciągłą integrację i testy, co pozwala zarządzać
ryzykiem wprowadzenia regresji na produkcję.

Nasza procedura przeglądania kodu:

* Znajdź kilka rzeczy, których poprawa zmieni najwięcej;
* Przekonaj osobę zgłaszającą kod do tego, że proponowane poprawki pomogą,
  albo: daj się przekonać, że nie ma sensu tego robić, bo nie będzie istotnej zmiany;
* Potraktujcie poprawę kodu jako wspólną odpowiedzialność.

Przeglądamy cały kod trafiający do repozytorium, łącznie z notebookami Jupytera i
prototypowym kodem. Dbamy, żeby produkcyjny kod Pythona miał zdecydowanie wyższą wynikową jakość, niż części prototypowane.

## Brak “silo mentality”

Mentalność silosu[2] to sytuacja, w której dwa zespoły nie dzielą się informacjami
i współpracują tylko na podstawie formalnych procedur.

Sytuacja, w której nad projektem pracuje jeden team zawierający i DS,
i programistki\ów jest dobra, ponieważ wymusza to naukę z obu stron.

## Wdrożenia

Do wdrożeń używamy dockera[3], pozwala to bezpiecznie “zapakować”
wszystkie zależności oraz wytrenowany model (kolejne wersje modelu wydawane są
jako kolejne wersje obrazu).

Taka metoda pozwala też na bardzo łatwe wdrożenie u klienta.

Zależności projektu instalujemy standardowo za pomocą polecenia
``pip``. Generujemy pliki zawierające dokładnie wersje wszystkich zależności
(również zależności tranzytywnych). Używamy do tego narzędzi
``pip-tools``[4]. Pip-tools zawiera polecenie ``pip-compile``,
które generuje plik z zamrożonymi zależnościami, tak wygenerowany plik można
zainstalować za pomocą ``pip install -r``. Dzięki temu podczas instalacji
projektu nie ma potrzeby używania niestandardowych narzędzi (co upraszcza istotnie
cały proces).

Do wdrożeń nie używamy Anacondy[5]. Anaconda to manager pakietów, który
instaluje typowe paczki Data Science, wraz z ich wszystkimi skompilowanymi
zależnościami (np. bibliotekami algebraicznymi). Jest czasem wygodny i bardzo
lubiany przez Data Scientistki\ów, ale nie używamy go we wdrożeniach, ponieważ
“przypinanie” zależności jest w nim mało praktyczne.

Świetnie działa Continuous Deploymen. Jest on szczególnie istotny w teamie w którym nie każdy ma chęć i umiejętności robienia wdrożeń. 

## Jupyter notebook

Jupyter[6] jest interaktywnym webowym środowiskiem, w którym można pisać
kod i od razu obserwować jego wyniki. Jeśli go nie znasz, zainstaluj i
zacznij używać do prototypowania (nie tylko w Data Science!).

Świetnie się w nim pisze prototypowy kod Data Science ponieważ:
* Blisko kodu można umieścić wynik jego działania (wykresy, statystyki itp.);
* Niektóre kroki obliczeniowe mogą trwać godzinami (np. trenowanie modelu)
  a Jupyter cechuje ich wyniki;
* Niektóre notebooki liczą godzinami, więc wygodnie jest mieć gotowy zrenderowany raport,
  który można pokazać innym (wyniki i wykresy są w pliku z notebookiem).

Jupytera można użyć też do bardzo wygodnej i efektywnej pracy na zdalnych
maszynach (patrz: “Praca na instancjach”).

Dlaczego notebooki są czasem mało fajne:

* Pliki, których używa Jupyter do przechowywania notebooków nie są czytelne
  dla ludzi. Technicznie są plikami JSON zawierającymi kod każdej komórki
  i wynikami zrealizowanych obliczeń.
  Ten format danych nie nadaje się do tworzenia diff/PR;
* Nie można ich wdrożyć na produkcję (sprawdzić czy nie Netflix)[7];
* Wspierają pisanie ad-hocowego throw-away code (patrz: “Throw-away code”);

### Przeglądy kodu a Jupyter

* Używamy wtyczki ``jupytext``[8], która do plików notebooka (``*.ipynb``)
  Dodaje siostrzane pliki ``*.py`` (które potem można otworzyć w dowolnym IDE oraz Jupyterze);
* Pliki notatników (``*.ipynb``) nie trafiają do repozytorium, chyba że zawierają wartościowe
  wyniki (tj. pliki ``*.ipynb`` ignorowane i trzeba je ręcznie dodać);
* Commitowane notebooki podlegają normalnemu przeglądowi kodu w postaci ``*.py``
  (aczkolwiek rozumiemy, że nie wszystkie wymogi jakości mają w nich sens);

## Biblioteka Pandas
Pandas[9] jest często używane z Jupyterem, pozwala na
eksploracyjne przeglądanie danych, wykonywanie przekształceń i agregacji,
podobnie jak w SQL.

### Problemy
Główną wadą tej biblioteki jest trzymanie wszystkiego w pamięci RAM co,
po prostu, nie zadziała dla dużych zbiorów danych. Często dobrym rozwiązaniem
jest wrzucenie skryptu z Pandasem na dużą instancję, bo koszt maszyny jest
szybko przewyższony przez oszczędności wynikające ze zwiększonej efektywności programistki/ty.

Pandas ma też czasem nieintuicyjną charakterystykę wydajnościową - rozwiązaniem
jest testowanie wydajności każdego Transformera niezależnie i przepisywanie kodu
będącego wąskim gardłem.

## Testowanie kodu

Automatyczne testowanie kodu jest bardzo przydatnym narzędziem w projektach DS.

Warto testować:

* Każdy Transformer danych, ponieważ ew. błędy (np. wycieki danych)
  najczęściej znajdują się tutaj, a nie w modelu, a błędy wprowadzone podczas
  obróbki danych są bardzo trudne do znalezienia.
* Warto zrobić "smoke testy"[11] całego procesu przetwarzania danych,
  czyli: uruchamiamy proces z danymi wejściowymi w dobrym formacie
  i patrzymy czy wychodzą dane w dobrym formacie.

Automatyczne testowanie samych modeli ma bardzo ograniczony sens,
przestrzeń wyników generowanych przez model jest bardzo duża i nie da się przetestować
wszystkich warunków brzegowych. Zapewnienie poprawnego działania modelu
jest odpowiedzialnością osoby, która go przygotowuje.

Poniżej typowe problemy, które można napotkać przy budowaniu modeli, które
są trudne do automatycznego testowania:

1. Model może mieć bardzo wysoką dokładność ze względu na wyciek w danych.
   Na przykład może bardzo dobrze zdiagnozować raka na podstawie tego,
   że pacjent w historii choroby ma długi pobyt w szpitalu onkologicznym;
2. Model może działać poprawnie, ale mieć uprzedzenia, np. rasowe, albo do płci.

## Praca na instancjach

Algorytmy DS zużywają dużo pamięci RAM (czasem setki GB), a czasem potrzebują
kart graficznych. Nie zawsze da się je uruchomić lokalnie, a szczególnie z
Zadowalającą wydajnością.

### Problemy

Dużym problemem jest konfiguracja zdalnej instancji,
osoby z Data Science nie zawsze czują się komfortowo z Linuxem i
często konfiguracja, która intuicyjnie powinna być szybka, zajmuje np. cały dzień.

Najprawdopodobniej rozwiążemy to poprzez standaryzację szablonu projektu,
tak by postawienie instancji zawsze wymagało pobrania repozytorium,
pobrania danych i napisania ``docker-compose up``.

### Rozwiązanie modelowe

Jak najwięcej należy zrobić bez zdalnej maszyny. W praktyce 90% problemów
da się wychwycić sprawdzając model na małej próbce danych.
W praktyce cały kod Pythona powstaje lokalnie.

W takim wypadku cały model sprawdzany jest na instancji na pełnych danych,
czasem mamy automatyczne skrypty, które tworzą instancję,
pobierają dane i sprawdzają działanie modelu. Czasem po prostu kod jest
uruchamiany na maszynie, a jakość modelu sprawdzana jest ręcznie za pomocą Jupytera.

# Take away

Zanim zaczniesz proponować rozwiązania nieprogramistkom/nieprogramistom,
musisz 3 razy dobrze upewnić się co i jak robią. Procesy muszą z jednej
strony zapewniać stabilną pracę, a z drugiej nie mogą być przeszkodą i utrudnieniem.

Nietypowe rozwiązania wprowadzane przez nieprogramistów z reguły mają swój dobry powód.

[1]: https://logicai.io/
[2]: https://zapier.com/blog/organizational-silos/
[3]: https://www.docker.com/
[4]: https://github.com/jazzband/pip-tools
[5]: https://www.anaconda.com/
[6]: https://jupyter.org/
[7]: https://medium.com/netflix-techblog/notebook-innovation-591ee3221233
[8]: https://github.com/mwouts/jupytext
[9]: https://pandas.pydata.org/
[10]: http://philipmgoddard.com/modeling/sklearn_pipelines
[11]: https://en.wikipedia.org/wiki/Smoke_testing_(software)

