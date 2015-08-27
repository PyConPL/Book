# Locust.io - nowoczesne narzędzie do load testów - Jacek Nosal


## Wprowadzenie


Testowanie obciążenia aplikacji webowych to temat bardzo złożony, który nabiera
na znaczeniu, jeżeli pod uwagę weźmiemy skalowalne architektury. Dzisiejszy
użytkownik wymaga. Coraz częściej spotyka się statystyki, które pokazują jak
wiele użytkowników rezygnuje ze skorzystania z danej aplikacji, jeżeli czasy 
odpowiedzi są wyższe niż pewien (niski) próg. Im szybsze odpowiedzi, tym więcej
użytkowników wejdzie na naszą stronę (ponieważ szybciej będą w stanie ocenić 
czy znajduje się na niej to, czego szukają). Typowy odwiedzający nie dba również
o stronę techniczną, bo po prostu się an tym nie zna. Aplikacja może cachować
dużo danych, autoscalować się, zepewniać failover - to wszystko nie ma wielkiego
znaczenia jeżeli jest po prostu wolne. Naturalnym wydaje się więc posiadanie
możliwości symulacji dużego ruchu, który sprawdzi możliwości naszej aplikacji 
i pokaże jak cały stack sprawuje się gdy zostanie "nawiedzony" przez tysiące
użytkowników jednocześnie. 


Spośród wielu dostępnych narzędzi na rynku, jedno wyróżnia się szczególnie -
locust.io. Po pierwsze: napisane jest w Pythona. Po drugie: do jego obsługi
wykorzystujemy Pythona. Po trzecie: jak większość frameworków jest niesamowicie
elastyczny i stworzony tak, żeby zmiana coreowych funkcjonalności nie wydawała
się czymś magicznym.


## Locust.io


Locust to lekkie narzędzie, które umożliwia stworzenie w Pythonie scenariuszy
do interakcji z aplikacją, które będą użyte do symulacji użytkowników końcowych.
Narzędzie potrafi symulować praktycznie dowolną liczbę znajdujących się
w osobnych sesjach użytkowników.

Od strony technicznej narzędzie to spójne połączenie flaska, geventa oraz pyzmq.
Całość została tak zaprojektowana, żeby umożliwić rozdystrybuowanie testów na 
kilka maszyn.


Do zalet locusta należą:

* możliwość pisania scenariuszy testowych w Pythonie
* skalowalność
* panel webowy do kontrolowania procesu testowania
* możliwość do przetestowania każdego systemu (nie tylko tych, opierających
 się na HTTP)


Narzędzie to rozwiązuje jeszcze jeden problem: proces testowania jest po prostu
nudny i żmudny. Większość rozwiązań jest konfigurowana przez skomplikowane xmle
bądź udostępnia 'tępe' panele webowe, które pozwalają nam wyklikać różne akcje,
jakie zostaną zasymulowane. W przypadku locusta wszystko sprowadza się do Pythona
i napisania skryptu, który wszystko kontroluje, czyli, innymi słowy, typowego
programistycznego zadania :-).



Instalacja locusta sprowadza się do zainstalowania jednej paczki:

```python
pip install locustio
```

Cała logika testowa znajduję się w pliku *locustfile.py*, który po wpisaniu 
komendy *locust* jest użyty do skonfigurowania środowiska.


Komponenty:

* Locust oraz HttpLocust
* TaskSet
* Event


*Locust* to klasa, której obecność w pliku locustfile.py jest wymagana,
żeby locust poprawnie się uruchomił. Instancje tej klasy reprezentują
użytkowników systemu (symulacja ruchu dla 5000 użytkowników spowoduje 5000 
instancji klasy Locust). Jeżeli nasz serwis działa na podstawie protokołu
HTTP to możemy wykorzystać klasę *HttpLocust*, która dodatkowo zapewni
obsługę sesji czy ciasteczek.


*TaskSet* to nic innego jak kolekcja zadań (które mogą być funkcjami bądź
klasami), która będzie nieprzerwanie wykonywana przez instancję klasy Locust.



## Scenariusze testowe


Wspomniany *TaskSet* służy jako scenariusz testowy - jest to zestaw definicji
operacji, jakie może wykonać użytkownik takich jak:

* nawigacja do podstrony
* zatwierdzenie formularza
* wyszukanie czegoś
* zalogowanie / wylogowanie
* w praktyce: jakiejkolwiek akcji, którą może wykonać użytkownik naszego serwisu

Bardzo prosty *locustfile.py*, który posłuży do przeprowadzenia symulacji 
wejścia na stronę główną, zalogowania i wyszukania produktu może wyglądać 
na przykład tak:

```python
from locust import HttpLocust, TaskSet, task


class MyCustomBehaviourTaskSet(TaskSet):

    @task(1)
    def get_index(l):
        l.client.get('/')

    @task(3)
    def search_something(l):
        l.client.get('/?q=%s' % 'sth', name='/?q=[query]')

    @task(3)
    def login(l):
        l.client.get("auth", params={}, verify=False, timeout=120)


class MyCustomScenarioUser(HttpLocust):
    task_set = MyCustomBehaviourTaskSet
    min_wait = 1000
    max_wait = 5000
```



## Jak to wygląda w praktyce i co dalej


Locust idealnie nadaje się do sprawdzania serwisów działających nie tylko w oparciu
o protokół HTTP. Poniżej znajduje się klient nanomsg działający na socketach
REQ <-> REP. Kod byłby o wiele krótszy, gdybyśmy korzystali z jednej z gotowych
bibliotek dostarczających klasy klienckie. Podpięcie całości pod locusta sprowadza się
do owrapowania metody odpowiadającej za wysyłanie requestów do serwisu i wysłanie
odpowiednich zdarzeń do locusta, które posłużą za metryki. Następnie tworzymy własną
klasę NanomsgLocust reprezentującą użytkownika, który jest klientem serwisu
działającego na nanomsg i gotowe. Całość prezentuje się następująco:


```python
import json
import time
import nanomsg

from locust import Locust, events, task, TaskSet


class SteroidSocket(nanomsg.Socket):

    def send_json(self, msg, flags=0, **kwargs):
        msg = json.dumps(msg, **kwargs).encode('utf8')
        self.send(msg, flags)

    def recv_json(self, buf=None, flags=0):
        msg = self.recv(buf, flags)
        return json.loads(msg)


class NanomsgClient(object):
    socket_type = nanomsg.REQ
    default_send_timeout = 100

    def __init__(self, address, **kwargs):
        self.address = address
        self.setup()

    def get_socket(self):
        return SteroidSocket(self.socket_type)

    def setup(self):
        self.socket = self.get_socket()
        self.socket.connect(self.address)
        self.socket._set_send_timeout(self.default_send_timeout)

    def get(self, msg):
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


class NanomsgLocust(Locust):

    def __init__(self, *args, **kwargs):
        super(NanomsgLocust, self).__init__(*args, **kwargs)
        self.client = NanomsgClient(self.address)


class NanomsgUser(NanomsgLocust):
    address = "tcp://127.0.0.1:5001"
    min_wait = 100
    max_wait = 1000

    class task_set(TaskSet):

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
