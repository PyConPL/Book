# Locust.io - nowoczesne narzędzie do load testów - Jacek Nosal


## Wprowadzenie


Testowanie obciążenia aplikacji webowych to temat bardzo złożony, który nabiera
na znaczeniu, jeżeli pod uwagę weźmiemy skalowalne architektury. Coraz częściej
spotyka się statystyki, które pokazują jak wielu użytkowników rezygnuje ze
skorzystania z danej aplikacji, jeżeli czasy odpowiedzi są wyższe niż pewien
(niski) próg. Im szybsze odpowiedzi, tym więcej użytkowników wejdzie na naszą
stronę (ponieważ szybciej będą w stanie ocenić czy znajduje się na niej to,
czego szukają).

* Google analizując ruch w internecie stwierdziło, że pół sekundowe opóźnienie
w ładowaniu strony skutkuje spadkiem ruchu na poziomie 20%
* Amazon podczas A/B testów zauważył, że wzrost czasów odpowiedzi o 100 ms
skutkował w ich przypadku spadkiem sprzedaży na poziomie 1% (co w przypadku
tak dużej firmie jest znaczącą wartością)


Typowy odwiedzający nie dba również o stronę techniczną, bo po
prostu się an tym nie zna. Aplikacja może cachować dużo danych, autoskalować się,
zepewniać failover - to wszystko nie ma wielkiego znaczenia jeżeli jest po prostu
wolne. Naturalnym wydaje się więc posiadanie możliwości symulacji dużego ruchu,
który sprawdzi możliwości naszej aplikacji i pokaże jak cały stos sprawuje się
gdy zostanie "nawiedzony" przez tysiące użytkowników jednocześnie.


Spośród wielu dostępnych narzędzi na rynku, jedno wyróżnia się szczególnie -
locust.io. Po pierwsze: napisane jest w Pythonie. Po drugie: do jego obsługi
wykorzystujemy Pythona. Po trzecie: jak większość frameworków jest niesamowicie
elastyczne i stworzone tak, żeby podmiana podstawowych komponentów była
transparentna i łatwa dla programisty.


## Locust.io


Locust to lekkie, open sourcowe narzędzie, które umożliwia stworzenie w Pythonie
scenariuszy do interakcji z aplikacją, które będą użyte do symulacji użytkowników
końcowych. Narzędzie potrafi symulować praktycznie dowolną liczbę znajdujących się
w osobnych sesjach użytkowników.

Od strony technicznej narzędzie to spójne połączenie flaska, geventa oraz pyzmq,
które na pojedynczej maszynie doskonale nadają się do symulowania tysięcy użytkowników.
Jeżeli jednak chcielibyśmy zwiększyć ruch do setek tysięcy bądź milionów jednoczesnych
wizyt, to istnieje możliwość uruchomienia testów rozłożonych na wiele maszyn.


Do zalet locusta należą:

* możliwość pisania scenariuszy testowych w Pythonie
* skalowalność
* panel webowy do kontrolowania procesu testowania
* możliwość przetestowania każdego systemu (nie tylko tych, opierających
 się na HTTP)


Narzędzie to rozwiązuje jeszcze jeden problem: upraszcza proces planowania
i przeprowadzania testów obciążeniowych. Większość rozwiązań jest konfigurowana
przez skomplikowane xml-e. bądź udostępnia 'tępe' panele webowe, które pozwalają
nam wyklikać różne akcje, jakie zostaną zasymulowane. W przypadku locusta wszystko
sprowadza się do Pythona i napisania skryptu, który wszystko kontroluje, czyli,
innymi słowy, typowego programistycznego zadania.



Instalacja locusta sprowadza się do zainstalowania jednej paczki:

```python
pip install locustio
```

Cała logika testowa znajduję się w pliku *locustfile.py*, który po wpisaniu 
komendy *locust* jest użyty do skonfigurowania środowiska.


```python
locust -f locustfile.py
```

Po uruchomieniu środowiska możemy przystąpić do konfiguracji testu. Do tego celu
locust dostarcza panel webowy dostępny standardowo pod adresem *localhost:8089*,
w którym zostaniemy poproszeni o podanie liczby użytkowników oraz hatch rate -
parametru, który odpowiada za częstotliwość przyrostu liczby użytkowników na sekunde
aż do osiągnięcia zadanej liczby. Przykładowo podanie liczb 1000 i 50 skutkuje
dwudziestosekundową 'rozgrzewką' do właściwej symulacji dla tysiąca użytkowników.


Jeżeli nie wystarcza nam pojedyncza maszyna, w prosty sposób możemy zaprząc
do współpracy inne środowiska: wystarczy uruchomić locusta w trybie master
na jednym z nich oraz w trybie slave na pozostałych:


Master:
```python
locust -f locustfile.py --master
```

Slave:
```python
locust -f locustfile.py --slave --master-host=<adres-ip-mastera>
```

Maszyna w trybie master nie przeprowadza symulacji, a jedynie zbiera statystyki
z maszyn w trybie slave oraz udostępnia interfejs webowy z podglądem całego procesu.


Komponenty:

* Locust oraz HttpLocust
* TaskSet
* Event hooks


*Locust* to klasa, której obecność w pliku locustfile.py jest wymagana,
żeby locust poprawnie się uruchomił. Instancje tej klasy reprezentują
użytkowników systemu (symulacja ruchu dla 5000 użytkowników spowoduje 5000 
instancji klasy Locust). Jeżeli nasz serwis działa na podstawie protokołu
HTTP to możemy wykorzystać klasę *HttpLocust*, która dodatkowo zapewni
obsługę sesji oraz ciasteczek.


*TaskSet* to nic innego jak kolekcja zadań (które mogą być funkcjami bądź
klasami), która będzie nieprzerwanie wykonywana przez instancję klasy Locust.


*Event hooks* to zdarzenia, które służą do komunikacji z locustem w celu
zbierania statystyk dotyczących żądań i odpowiedzi. Do dyspozycji mamy:

* request_success
* request_failure
* locust_error
* report_to_master
* slave_report
* hatch_complete
* quitting


## Scenariusze testowe


Wspomniany *TaskSet* służy jako scenariusz testowy - jest to zestaw definicji
operacji wykonywanych przez użytkownika, takich jak:

* nawigacja do podstrony
* interakcja z formularzem webowym
* przeprowadzenie operacji wyszukiwania
* zalogowanie / wylogowanie
* w praktyce: jakiejkolwiek akcji, którą może wykonać użytkownik naszego serwisu

Bardzo prosty *locustfile.py*, który posłuży do przeprowadzenia symulacji 
wejścia na stronę główną, zalogowania i wyszukania produktu może wyglądać 
na przykład tak:

```python
from locust import HttpLocust, TaskSet, task


class MyCustomBehaviourTaskSet(TaskSet):

    # Klasa reprezentująca zestaw zadań jaki ma zostać
    # wykonany przez użytkownika

    @task(1)
    def get_index(l):
        l.client.get('/')

    @task(1)
    def search_something(l):
        l.client.get('/?q=%s' % 'query')

    @task(1)
    def submit_form(l):
        l.client.post('/submit/form/', data='form-data')


class MyCustomScenarioUser(HttpLocust):
    # Klasa reprezentująca użytkownika systemu, który ma wykonać
    # zdefiniowany zestaw zadań: MyCustomBehaviourTaskSet
    # względem serwisu bazującego o protokół HTTP
    task_set = MyCustomBehaviourTaskSet
    min_wait = 1000
    max_wait = 5000
```


Nie pozostaje nam nic innego, jak uruchomić locust:

```python
locust -f locustfile.py --host=http://host.pl
```


## Jak to wygląda w praktyce i co dalej


Locust idealnie nadaje się do sprawdzania serwisów działających nie tylko w oparciu
o protokół HTTP. Poniżej znajduje się klient nanomsg działający na socketach
REQ <-> REP. Kod byłby o wiele krótszy, gdybyśmy korzystali z jednej z gotowych
bibliotek dostarczających klasy klienckie. Podpięcie całości pod locusta sprowadza się
do zmodyfikowania metody odpowiadającej za wysyłanie requestów do serwisu i wysłaniu
odpowiednich zdarzeń do locusta, które posłużą za metryki. Następnie tworzymy własną
klasę NanomsgLocust reprezentującą użytkownika, który jest klientem serwisu
działającego na nanomsg i gotowe. Całość prezentuje się następująco:


```python
# -*- coding: utf-8 -*-
import json
import time
import nanomsg

from locust import Locust, events, task, TaskSet


class MySocket(nanomsg.Socket):
    # Klasa dziedzicząca po nanomsg.Socket, dokładająca
    # dwie metody send_json oraz recv_json, które ułatwiają
    # pracę z tym formatem

    def send_json(self, msg, flags=0, **kwargs):
        msg = json.dumps(msg, **kwargs).encode('utf8')
        self.send(msg, flags)

    def recv_json(self, buf=None, flags=0):
        msg = self.recv(buf, flags)
        return json.loads(msg)


class NanomsgClient(object):
    # Właścicwy klient nanomsg, pracujący w trybie komunikacji
    # REQ - REP (request - response)
    # więcej informacji o trybach komunikacji można znaleźć
    # w oficjalnej dokumentacji: http://nanomsg.org/

    socket_type = nanomsg.REQ

    # timeout dla operacji wysyłania, ustawiony w milisekundach
    default_send_timeout = 100

    def __init__(self, endpoint, **kwargs):
        self.endpoint = endpoint
        self.setup()

    def setup(self):
        # utworzenie i połączenie gniazda pod wskazany w __init__
        # endpoint oraz konfiguracja timeoutu
        self.socket = MySocket(self.socket_type)
        self.socket.connect(self.endpoint)
        self.socket._set_send_timeout(self.default_send_timeout)

    def get(self, msg):
        # metoda wysyła zserializowaną do formatu json
        # wiadomość i czeka na odpowiedź z serwisu, dodatkowo
        # wysyłając informację o czasacj requestu do locusta
        # poprzez użycie komponentu Event
        start_time = time.time()
        
        try:
            self.socket.send_json(msg)
            result = self.socket.recv_json()
            print result
        except nanomsg.NanoMsgAPIError as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="nanomsg",
                name=msg.get('executable', ''),
                response_time=total_time,
                exception=e
            )
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type="nanomsg",
                name=msg.get('executable', ''),
                response_time=total_time,
                response_length=0
            )

    def close(self):
        self.socket.close()


class NanomsgUser(Locust):
    endpoint = "tcp://127.0.0.1:5001"

    # Parametry reprezentujące (w milisekundach) minimalny
    # i maksylany czas jaki użytkownik powinien odczekać przed
    # wykonaniem kolejnego zadania.

    min_wait = 100
    max_wait = 1000

    def __init__(self, *args, **kwargs):
        # Przeładowujemy __init__ i podajemy naszą klasę
        # klienta, która będzie użyta do komunikacji z serwisem
        # działającym na nanomsg przez locusta.

        super(NanomsgUser, self).__init__(*args, **kwargs)
        self.client = NanomsgClient(self.endpoint)

    class task_set(TaskSet):
        # Zestaw zadań, jakie ma wykonać symulowany użytkownik
        # będzie to wysłanie dwóch wiadomości json do serwisu.

        # Zadania tworzymy poprzez dekorator @task
        # podając mu opcjonalnie wskaźnik wykonania
        # decydujący o tym jak często, w kontekście do innych
        # takie zadanie wykonywać

        @task(1)
        def ping(self):
            self.client.get({'executable': 'ping'})

        @task(1)
        def pong(self):
            self.client.get({'executable': 'pong'})

```

Wnioski nasuwają się same - locust nie ogranicza się do pracy wyłącznie z serwisami
wspierającymi protokół HTTP. Testowanie architektur mikroserwisów korzystających
z Rabbitmq (nameko), Zeromq (lymph) czy nanomsg (nanoservice, omnomnom) jest
banalnie prostym zadaniem. W kontekście samych mikroserwisów locust idealnie
nadaje się do znajdywania elementów będących bottleneckiem naszej aplikacji,
znajdywania single point of failure czy też sprawdzanie jak nasza architektura
poradzi sobie, gdy jeden z serwisów przestanie być responsywny lub całkowicie
padnie.



## Bibliografia / użyteczne linki


1. [Locust.io: Dokumentacja](http://docs.locust.io/en/latest/)
2. [Ian Molyneaux: The Art of Application Performance Testing](http://shop.oreilly.com/product/9780596520670.do)
3. [http://www.uvd.co.uk/blog/load-testing-vote-for-policies-with-locust-io/](http://www.uvd.co.uk/blog/load-testing-vote-for-policies-with-locust-io/)
4. [http://software.danielwatrous.com/load-testing-alternatives-for-large-scale-web-applications/](http://software.danielwatrous.com/load-testing-alternatives-for-large-scale-web-applications/)
5. [http://abhishek-tiwari.com/post/performance-testing-as-a-first-class-citizen](http://abhishek-tiwari.com/post/performance-testing-as-a-first-class-citizen)
6. [http://blog.codinghorror.com/performance-is-a-feature/](http://blog.codinghorror.com/performance-is-a-feature/)
