# Asyncio w praktyce (warsztat)

Podczas tych warsztatów nauczysz się korzystać z **asyncio** [1] na tyle, by
móc samodzielnie zaprojektować i zakodować aplikację korzystającą z jego
dobrodziejstw.

Nauka oprze się o pisanie w pełni funkcjonalnego czatu. W trakcie ćwiczeń
poznasz część biblioteki asyncio potrzebną do zrealizowania zadania, nową
składnię dla coroutines z async i await, bibliotekę **aiohttp** [2]
(klient i serwer HTTP) oraz tajniki testowania powyższych. Pisanie
testów przed kodem będzie częścią szkolenia, ale w razie potrzeby może zostać
pominięte, by nadal móc coś z niego wynieść.

Do testowania będziemy używać biblioteki **pytest** [3], ale w minimalnym
stopniu - jego nieznajomość w niczym nie będzie przeszkadzać.

Najważniejszą rzeczą, którą wyniesiecie ze szkolenia, będzie umiejętność
projektowania aplikacji opartych na asyncio. Poznacie mocne strony biblioteki
i sytuacje, w których jest odpowiednim narzędziem. Nauczycie się także unikania
najczęstszych pułapek związanych z asyncio.


```python
import asyncio
import datetime

PYCON_PL_START_DATE = datetime.date(2017, 8, 17)

loop = asyncio.get_event_loop()
asyncio_workshop = asyncio.Future()

def check_workshop_time():
    today = datetime.date.today()
    if today >= PYCON_PL_START_DATE:
        asyncio_workshop.set_result('Przyjdź na warsztat!')
    else:
        days_left = (PYCON_PL_START_DATE - today).days
        print(f'Pozostało {days_left} dni')
        loop.call_later(86400, check_workshop_time)

async def attend_pycon_pl():
    result = await asyncio_workshop
    print(result)


loop.call_later(1, check_workshop_time)
loop.run_until_complete(
    attend_pycon_pl()
)
loop.close()
```

## Dla kogo?
Szkolenie jest adresowane do osób, które programują już trochę w Pythonie
i chcą poznać jego asynchroniczną stronę. Każdy średniozaawansowany
lub ogarniający początkujący programista Pythona da sobie radę z ćwiczeniami.
Znajomość technologii frontendowych nie jest wymagana - ta część zostanie
zapewniona przez organizatora warsztatów.

## Jak się przygotować?
Potrzebny będzie Python w wersji 3.5 lub 3.6, umiejętność obsługi pip'a,
virtualenv'a i podstawowa znajomość git'a - na tyle, by móc sklonować sobie
repozytorium, utworzyć wirtualne środowisko i zainstalować zależności
potrzebne do ćwiczeń:

```bash
git clone https://github.com/Enforcer/asyncio-workshop
cd asyncio-workshop
python3.6 -m venv ve
source ve/bin/activate
pip install -r requirements.pip
```

Edytor kodu nie ma znaczenia, używajcie swojego ulubionego. W razie
wątpliwości - PyCharm Community Edition na pewno się nada.


## Kiedy warto iść w asyncio? Kiedy nie?
Pojawienie się asyncio wraz z wersją 3.4 interpretera wywołało trochę
zamieszania w świecie Pythona. Nie wszyscy programiści rozumieli, dlaczego
zostało ono dodane do biblioteki standardowej oraz czy powinni się nim
zainteresować mając działające projekty napisane chociażby w Django.

Inni zareagowali entuzjastycznie i zaadoptowali tę bibliotekę do swoich
potrzeb. Trzeba na początek powiedzieć, że asynchroniczność jest w Pythonie
już od długiego czasu. Pierwsze wydanie frameworka Twisted miało miejsce w 2002
roku, a więc aż 15 lat temu. Inny popularny framework, Tornado, jest z nami
już od 8 lat. Te projekty miały swoją niszę na rynku oprogramowania,
udostępniając programowanie sterowane zdarzeniami na długo zanim stało się to
modne za sprawą NodeJS.

Asynchroniczne programowanie jest szczególnie przydatne, gdy mamy do czynienia
z aplikacjami, które przez większość czasu oczekują na zakończenie
operacji I/O, a mniej czasu spędzają na obliczeniach używających intensywnie CPU. Pomysł
na podejście asynchroniczne pochodzi z bardzo prostej obserwacji - gdy program
czeka na zakończenie operacji wejścia-wyjścia, to pozostaje bezczynny.

Mechanizmem sterującym, który wykrywa sytuacje rozpoczęcia oczekiwania
na operację I/O jest pętla zdarzeń. Zawiesza ona wykonywanie kodu i przenosi
się w inne miejsce, którego operacja wejścia-wyjścia zdążyła się zakończyć.

W ten sposób maksymalizujemy wykorzystanie pojedynczego rdzenia CPU. Tak więc
od razu można odpowiedzieć na pytanie, kiedy NIE UŻYWAĆ asyncio - gdy nie mamy
wiele operacji I/O lub nie zajmują one wiele czasu wykonania programu.
Zbadanie tego faktu może zostać dokonane przy użyciu profilerów. Zwykle
_tradycyjna_ aplikacja w Django, szczególnie jeżeli już działa na produkcji,
nie odniesie najmniejszej korzyści z przepisania na asyncio. Bierze się
to stąd, że chociaż może mieć ona wielu klientów na sekundę, to jednak
poszczególne żądania będą bardzo krótkie. Nie ma potrzeby utrzymywania
długożyjących połączeń z przeglądarkami użytkowników.

Co innego w przypadku, gdy zbudowanie odpowiedzi wymaga odpytania kilku
lub kilkunastu usług wokół. W takiej sytuacji asyncio da natychmiastowe
przyspieszenie dzięki zmultipleksowaniu żądań i wykonaniu ich jednocześnie.
Na koniec musimy tylko poskładać ich wyniki. Bez asyncio naszą jedyną opcją
było użycie puli wątków, procesów lub oddelegowanie do systemu kolejkowego,
jak Celery i synchroniczne oczekiwanie na wynik. Kolejną przesłanką
za zastosowaniem asyncio jest konieczność utrzymywania długo trwających połączeń
z klientami. Idealnym przykładem jest serwer websocketów, na którym można
zbudować powiadomienia w czasie rzeczywistym do naszej aplikacji. Mówimy cały
czas o wykorzystaniu asyncio po stronie serwera, ale oczywiście można też
stworzyć asynchronicznego klienta, który będzie w stanie odbierać strumień
danych płynących po sieci (potencjalnie z kilku źródeł) i odpowiednio na nie
reagować.

Nic nie stoi na przeszkodzie, by w jednym procesie Pythona, przy użyciu jednej
pętli zdarzeń, mieć jednocześnie osadzony tak serwer jak i klienta, a nawet
po kilka z nich. Sprawia to, że asyncio świetnie nadaje się do pisania
_glue-services_ - tworów, które zapewniają pomost pomiędzy różnymi
niekompatybilnymi ze sobą usługami.


## Forma szkolenia
W trakcie tego warsztatu uczestnicy będą realizować samodzielnie zadania
na podstawie instrukcji dostarczonej w repozytorium z początkowym kodem
do dalszego rozwijania. Prowadzący przeprowadzi krótki wstęp teoretyczny
i będzie wprowadzać uczestników w każdy etap warsztatów. W trakcie wykonywania
ćwiczeń prowadzący będzie sprawdzać postępy uczestników, odpowiadać na pytania
i pomagać w razie problemów.

Instrukcja poza pewnymi informacjami teoretycznymi zawierać też będzie zadania
zorganizowane zgodnie z programem szkolenia i oznaczone trzema różnymi kolorami:

1. zielony - zakres minimum szkolenia, bez ich zrealizowania nie idź dalej
2. pomarańczowy - rozszerzenie zakresu podstawowego, łącznie z testami
3. czerwony - dla chętnych jako zadanie domowe w celu jeszcze lepszego poznania asyncio lub do wykonania w trakcie warsztatów dla zaawansowanych uczestników

W treści zadań zawarte są też podpowiedzi, ukryte do momentu aż uczestnik
nie zdecyduje się z nich skorzystać. Mogą okazać się pomocne, gdyby uczestnik
miał problem z podejściem do danego etapu lub chciał zobaczyć inny sposób
rozwiązania.

## Program szkolenia
1. Wstęp teoretyczny (10 minut)
   1. czym jest asyncio
   2. kiedy warto stosować asyncio?
   3. przegląd dostępnych narzędzi i bibliotek
   4. testowanie aplikacji z asyncio - złote zasady
2. Wprowadzenie do projektu (5 minut)
   1. Przedstawienie zawartości repozytorium
   2. Pożądany zakres funkcjonalności na koniec szkolenia

3. Moduł 1 - czat ogólny (1 godzina 15 minut)
   1. Obsługa przychodzącej wiadomości
   2. Wysłanie wiadomości do pozostałych użytkowników czatu
   3. Zabezpieczenie przed sytuacją, gdy jeden z użytkowników rozłączy się w trakcie przekazywania wiadomości
   4. Oznaczanie obecności na czacie
   5. Statystyki czatu
   6. Przechowanie historii czatu dla nowych uczestników

(przerwa - 15 minut)

4. Moduł 2 - prywatne pokoje (45 minut)
   1. Zakładanie pokoju
   2. Zapraszanie do środka uczestników
   3. Wchodzenie do pokoju przez listę
   4. Możliwość opuszczania pokoju
   5. Automatyczne usuwanie pokoju po wyjściu z niego ostatniego uczestnika

5. Moduł 3 - prywatne wiadomości (45 minut)
   1. Możliwość rozpoczęcia konwersacji z innym użytkownikiem
   2. Dynamiczne tworzenie pokoi z zachowaniem historii konwersacji
   3. Możliwość dołączenia kolejnego uczestnika do prywatnej rozmowy i utworzenie w ten sposób dynamicznie nowego pokoju

6. Podsumowanie


### Komentarz do modułu I
W tej części uczestnicy zapewnią minimum funkcjonalności, jaką powinna mieć
aplikacja czatowa - obsługę wspólnego dla wszystkich pokoju czatowego. Jest
to najważniejsza część warsztatu - to tu zostaną podłożone podwaliny
pod kolejne części, uczestnicy zrozumieją czym jest pętla zdarzeń i jak unikać
jej blokowania.

### Komentarz do modułu II
Druga część wzbogaci rozwijany projekt o możliwość rozpoczynania prywatnych
rozmów i dynamicznie zarządzanych pokoi prywatnych. Ujawni to więcej ciekawych
problemów typu _race conditions_, a przecież o to chodzi - by nauczyć się
wykrywać i zabezpieczać takie sytuacje.

### Komentarz do modułu III
Ostatnia część skupia się na dodaniu kolejnej, częstej funkcjonalności -
prywatnych wiadomości. Chociaż mierzyć się będziemy z tymi samymi problemami,
co wcześniej, to jest _znikający_ użytkownicy, to jednak rozwiązanie jakie
chcemy osiągnąć będzie zgoła inne - nie tylko chcemy pozbyć się wyjątków
związanych z błędami przy próbie wysyłania wiadomości na martwy websocket,
ale także zapewnić integralność danych. Jeżeli użytkownika nie było w momencie
wysyłania do niego wiadomości, to chcielibyśmy aby miał możliwość jej
odczytania później.


## Co robić dalej po szkoleniu?

Zdecydowanie polecam zapoznanie się z pierwszymi trzema pozycjami
z bibliografii, począwszy od książki Luciano Ramalho [4]. Powinno to dać dalszą,
solidną porcję wiedzy potrzebną do projektowania aplikacji opartych
na asyncio.

Liczba bibliotek i narzędzi kompatybilnych z asyncio rośnie z czasem.
Większość z nich można znaleźć w dedykowanym repozytorium bibliotek i rozszerzeń [5].

## Bibliografia

1. asyncio. https://docs.python.org/3/library/asyncio.html
2. aiohttp. https://aiohttp.readthedocs.io/en/stable/
3. pytest. https://docs.pytest.org/
4. Luciano Ramalho. Fluent Python, rozdział 18.
5. awesome-asyncio. https://github.com/timofurrer/awesome-asyncio
