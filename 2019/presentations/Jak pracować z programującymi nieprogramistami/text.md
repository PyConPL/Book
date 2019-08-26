# Jak pracować z programującymi nieprogramistami

Jacek Bzdak <jacek@logicai.io>, Magdalena Wójcik <magda@logicai.io>

## Streszczenie

W prezentacji chcemy przedstawić przeszkody jakie pojawiają się w
pracy na linii programiści - programujący nieprogramiści. Dotyczą one zarówno kwestii
jakości kodu, wykorzystywanych narzędzi czy środowiska pracy.
Dla każdego z problemów zaprezentujemy rozwiązania, które stosujemy w
naszej codziennej pracy. Prezentacja będzie opierała się na dwóch punktach
widzenia - programisty i Data Scientistki. Poniższy artykuł zawiera spis
technicznym zagadnień.

## Wstęp
### Disclaimer

1. Podane niżej pomysły sprawdzają się w "młodym" teamie w consultingowym startupie,
   robiącym dużo małych projektów[1],
2. Relatywnie rzadko robimy projekty Big Data, większość z nich da się zrobić
   na jednej maszynie (nawet jeśli jest to “duża” instancja),
3. Jeśli masz terabajty danych i od lat tworzysz produkt możliwe, że rozwiązania te
   mogą nie być optymalne,

### Jak wygląda praca Data Scientista?

Projekty Data Science (DS) są podobne do projektów stricte programistycznych,
ale mają też swoje specyficzne elementy. Zwykle przebiega to mniej więcej tak:

1. rozmowa z klientem, zebranie wymagań i potrzeb, określenie jaki cel
   biznesowy ma osiągnąć model,
2. analiza i czyszczenie danych, co może zająć nawet 90% czasu całego projektu,
   jeśli dane zawierają dużo błędów i szumu; W ramach tego kroku powstają
   tzw. Transformery czyli skrypty przygotowujące dane do postaci odpowiedniej
    dla modelu ML,
3. trenowanie modelu ML,
4. Przekazanie wyników do klienta,

# Praca z Data Scientistami
## Wspólne ustalenie API które jest zrozumiałe dla obu stron
Często da się opracować API między częścią *programistyczną* oraz częścią
 *data scienceową*.

Ważne uwagi:

1. API musi być zrozumiałe dla wszystkich, w praktyce podlega bardzo dokładnemu
   przeglądowi kodu, i **wszyscy** muszą być pewni, że jest dobre;
2. Należy być otwartym na jego refaktoryzację;

### Co może się nie udać?
Narzucenie API zrobionego tak, żeby było “elegancko” i zgodnie z
obowiązującą modą programistyczną, bez patrzenia na przejrzystość API
dla nieprogramistycznej części zespołu. To przepis na ciągłe ignorowanie API
i świadczenie supportu programistycznego przy nawet najtrywialniejszych zmianach.

## Przeglądy kodu jako okazja do ulepszenia praktyk

Czasem przeglądy kodu są nieprzyjemne, ale w naszej firmie dbamy,
żeby było miło, więc przeglądy kodu *nie są* okazją do *gate keepingu*
(czyli nie służą do tego, żeby odrzucać zmiany, które nie spełniają standardów).
Przeglądy są dobrą okazją poprawy do praktyk w firmie.

W większości projektów mamy ciągłą integrację i testy, co pozwala zarządzać
ryzykiem wprowadzenia regresji na produkcję.

Nasza procedura przeglądania kodu:

* Znajdź kilka rzeczy, których poprawa zmieni najwięcej;
* Przekonaj osobę zgłaszającą kod do tego, że proponowane poprawki pomogą,
  albo: daj się przekonać że nie są warte świeczki;
* Potraktujcie poprawę jako wspólną odpowiedzialność;

Przeglądamy cały kod trafiający do repozytorium, łącznie z notebookami jupytera i
prototypowym kodem, natomiast produkcyjny kod pythona ma zdecydowanie wyższą wynikową
jakość.

## Brak “silo mentality”

Mentalność silosu to sytuacja, w której dwa zespoły nie dzielą się informacjami
i współpracują tylko na podstawie formalnych procedur[2].

Sytuacja, w której nad projektem pracuje jeden team zawierający i DS,
i programistki\ów jest fajna. Wymusza to naukę z obu stron.

## Wdrożenia

Do wdrożeń używamy dockera[3], pozwala bezpiecznie zapakować
wszystkie zależności oraz wytrenowany model (kolejne wersje modelu wydawane są
jako kolejne wersje obrazu).

Pozwala też na bardzo łatwe wdrożenie u klienta.

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
zależnościami (np. Bibliotekami algebraicznymi). Jest czasem wygodny i bardzo
lubiany przez Data Scientistki\ów, ale nie używamy go we wdrożeniach, ponieważ
przypinanie zależności jest w nim mało praktyczne.

Świetnie działa Continuous Deployment, szczególnie, że nie każdy w zespole ma
chęć i skonfigurowane środowisko do robienia deploymentów ręcznych lub/i
automatycznych.

## Jupyter notebook

Jupyter[6] jest interaktywnym webowym środowiskiem, w którym można pisać
kod i od razu obserwować jego wyniki. Jeśli go nie znasz, zainstaluj i
zacznij używać do prototypowania (nie tylko w Data Science!).

Świetnie się w nim pisze prototypowy kod kod Data Science ponieważ:
* Blisko kodu można umieścić wynik jego działania (wykresy, statystyki itp.);
* Niektóre kroki obliczeniowe mogą trwać godzinami (trenowanie modelu)
  a jupyter cachuje ich wyniki;
* Niektóre notebooki liczą się godzinami, więc wygodnie jest mieć gotowy raport,
  który można pokazać innym;

Jupytera można użyć też do bardzo wygodnej i efektywnej pracy na zdalnych
maszynach (patrz: “Praca na instancjach”).

Dlaczego notebooki są czasem mało fajne:

* Pliki których używa jupyter do przechowywania notebooków nie są czytelne
  dla ludzi. Technicznie są plikami JSON zawierającymi kod każdej komórki
  i wynikami zrealizowanych obliczeń.
  Ten format danych nie nadaje się do tworzenia diff/PR;
* Nie wrzucisz ich na produkcję (sprawdzić czy nie Netflix)[7];
* Wspierają pisanie ad-hocowego throw-away code (patrz: “Throw-away code”);

### Przeglądy kodu a jupyter

* Używamy wtyczki ``jupytext``[8], która do plików notebooka (``*.ipynb``)
  dodaje pliki ``*.py`` (które potem można otworzyć w jupyterze);
* Pliki notatników nie trafiają do repozytorium, chyba że zawierają wartościowe
  wyniki (tj. pliki ``*.ipynb`` ignorowane i trzeba je ręcznie dodać);
* Commitowane notebooki podlegają normalnemu przeglądowi kodu w postaci ``*.py``
  (aczkolwiek rozumiemy że nie wszystkie wymogi jakości mają w nich sens);

## Biblioteka Pandas
Pandas[9] jest często używane z Jupyter Notebookiem, pozwala na
eksploracyjne przeglądanie danych, wykonywanie przekształceń i agregacji,
podobnie jak w SQL.

### Problemy
Główną wadą tej biblioteki jest trzymanie wszystkiego w pamięci RAM co,
po prostu, nie zadziała dla dużych zbiorów danych. Często dobrym rozwiązaniem
jest wrzucenie skryptu z Pandasem na dużą instancję, bo koszt maszyny jest
szybko przewyższony przez oszczędności ze zwiększonej efektywności programistki/ty.

Pandas ma czasem też nieintuicyjną charakterystykę wydajnościową - rozwiązaniem
jest testowanie wydajności każdego transformera niezależnie i przepisywanie kodu
będącego wąskim gardłem.

## Testowanie kodu

Automatyczne testowanie kodu jest bardzo przydatnym narzędziem w projektach DS.

Warto testować:

* Każdy trasnformer danych, ponieważ ew. bugi (np. wycieki danych)
  najczęściej znajdują się tutaj, a nie w modelu, a błędy wprowadzone podczas
  obróbki danych są bardzo trudne do znalezienia.
* Warto zrobić "smoke testy"[11] całego procesu przetwarzania danych,
  czyli: uruchamiamy proces z danymi wejściowymi w dobrym formacie
  i patrzymy czy wychodzą dane w dobrym formacie.

Automatyczne testowanie samych modeli ma bardzo ograniczony sens,
przestrzeń stanu wewnętrznego modelu jest bardzo duża i nie da się przetestować
wszystkich warunków brzegowych. Zapewnienie poprawnego działania modelu
jest odpowiedzialnością osoby która go przygotowuje.

Poniżej typowe problemy które można spotkać przy budowaniu modeli które
są trudne to automatycznego testowania:

1. Model może mieć bardzo wysoką dokładność ze względu na wyciek w danych.
   Na przykład może bardzo dobrze diagnozować raka na podstawie tego,
   że pacjent w historii choroby ma długi pobyt w szpitalu onkologicznym.
2. Model może działać poprawnie, ale mieć uprzedzenia, np. rasowe, albo do płci.
   Takie modele należy również poprawiać.

## Praca na instancjach

Algorytmy DS zużywają dużo pamięci RAM (czasem setki gb) a czasem potrzebują
kart graficznych. Nie zawsze da się je uruchomić lokalnie, a szczególnie z
odpowiednią wydajnością.

### Problemy

Dużym problemem jest konfiguracja zdalnej instancji,
osoby z Data Science nie zawsze czują się komfortowo z Linuxem i
często konfiguracja, która intuicyjnie powinna być szybka, zajmuje np. cały dzień.

Najprawdopodobniej rozwiążemy to poprzez standaryzację szablonu projektu,
tak żeby postawienie instancji zawsze wymagało pobrania repozytorium,
pobrania danych i napisania ``docker-compose up``.

### Rozwiązanie modelowe

Jak najwięcej należy zrobić bez zdalnej maszyny, w praktyce 90% problemów
da się wychwycić sprawdzając model na małej próbce danych.
W praktyce cały kod Pythona powstaje lokalnie.

W takim wypadku cały model walidowany jest na instancji na pełnych danych,
czasem mamy automatyczne skrypty które tworzą instancję,
pobierają dane i walidują działanie modelu. Czasem po prostu kod jest
uruchamiany na maszynie, a jakość modelu sprawdzana jest ręcznie za pomocą Jupytera.

# Take away

Zanim zaczniesz proponować rozwiązania nieprogramistom,
musisz 3 razy dobrze dowiedzieć się co i jak robią. Procesy muszą z jednej
strony zapewniać stabilną pracę, a z drugiej nie mogą być przeszkodą i utrudnieniem.

Nietypowe rozwiązania wprowadzane przez nieprogramistów z reguły mają dobry powód.

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
