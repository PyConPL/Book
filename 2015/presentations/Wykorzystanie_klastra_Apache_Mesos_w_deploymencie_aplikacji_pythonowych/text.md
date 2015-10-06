# Wykorzystanie klastra Apache Mesos w deploymencie aplikacji pythonowych - Kamil Warguła

Dzisiejsze aplikacje internetowe poddawane są zróżnicowanemu obciążeniu w
ciągu tygodni, dni, a nawet godzin. Wykorzystanie zasobów jest ważną kwestią
w utrzymywaniu aplikacji i panowaniu nad budżetem.

W tym artykule chciałbym przedstawić, jak w łatwy sposób można wykorzystać
potencjał klastra Apache Mesos do deployowania aplikacji pythonowych.

Klaster Apache Mesos przykrywa warstwą abstrakcji zasoby takie jak
procesor, pamięć, przestrzeń dyskowa. Dzięki temu użytkownik, który
zleca poprzez framework [1] (w naszym przypadku będzie to Marathon [2])
uruchomienie procesu na klastrze, nie potrzebuje się martwić, na jakim
serwerze zostanie on uruchomiony, oraz nie musi dbać o to, co się stanie
w przypadku awarii jednego serwera w klastrze, o wszystko zadba Mesos.

## Przygotowanie aplikacji

W celu zademonstrowania deploymentu na klaster Mesos zbudujmy prostą
aplikację, która będzie wystawiała REST API. Poniżej
fragment pliku `api.py` [3]:

    import falcon
    import json


    class ExampleResource:
        def on_get(self, req, resp):
            data = {'foo': 'bar'}
            resp.body = json.dumps(data)

    api = falcon.API()
    api.add_route('/', ExampleResource())

W powyższym fragmencie wykorzystany został framework Falcon [4]
do napisania aplikacji WSGI, która w połączeniu z serwerem Gunicorn pozwoli
serwować nasze API.

Do przygotowania paczki z naszą aplikacją wykorzystamy narzędzie PEX [5],
które dostarczy nam wirtualne środowisko Pythona wraz zależnościami w
postaci jednego wykonywalnego pliku. Aby zbudować takie środowisko, należy
wykonać następujące polecenie:

    pex -r <(printf "falcon==0.3.0\ngunicorn==19.3.0") -o app.pex

Dopełnieniem procesu przygotowania naszej aplikacji jest spakowanie
pliku `app.pex` oraz `api.py` do archiwum `tar.gz`:

    tar -zcvf app.tar.gz api.py rest_app.pex


## Deployment aplikacji

Wcześniej przygotowane archiwum z naszą aplikacją musi być dostępne
poprzez protokół HTTP. Aby to zrobić, możemy wykorzystać wbudowany w Pythona
serwer HTTP.

Proces uruchomienia naszej aplikacji na klastrze jest bardzo prosty,
a mianowicie jedyne, co musimy zrobić, to wysłać do Marathona request do REST API
zawierający opis naszej aplikacji. Powinien on zawierać takie dane jak:
nazwa aplikacji, komenda, która uruchomi naszą aplikację, liczbę instancji,
wielkość zasobów takich jak CPU oraz RAM, oraz lokalizacja paczki z aplikacją.
Poniżej przykładowa zawartość opisująca aplikację:

    {
        "id":"rest_app",
        "cmd":"./app.pex api.py -p $PORT0",
        "cpus":0.5,
        "instances":1,
        "mem":128,
        "uris":[
            "http://10.141.141.10:8000/app.tar.gz"
        ]
    }

Komenda, która została wykorzystana do uruchomienia aplikacji, zawiera
zmienną środowiskową `$PORT0`, jest to zmienna określająca port przydzielony
automatycznie przez Marathona, pod którym zostanie zbindowana nasza aplikacja.

Marathon po otrzymaniu informacji o definicji aplikacji przystąpi do procesu
deploymentu. Zdefiniowana przez nas paczka zostanie pobrana na serwer
slave w klastrze Mesos, rozpakowana, a następnie zostanie uruchomiona komenda
zawarta w definicji aplikacji.

Informację o wszystkich uruchomionych aplikacjach na klastrze Mesos możemy
zobaczyć w interfejsie Marathona dostępnym poprzez stronę WWW,
a także za pomocą REST API [6] wystawionego pod zasobem `/v2/apps`.

W przypadku wystąpienia awarii serwera, na którym uruchomiony jest nasz program,
Marathon automatycznie przystąpi do procesu redeploymentu naszej aplikacji na
innym serwerze wchodzącym w skład klastra Mesos. Dzięki temu mechanizmowi
w automatyczny sposób możemy uzyskać odporną na awarie infrastrukturę
naszej aplikacji.

## Skalowanie manualne

Liczba użytkowników każdej aplikacji z czasem rośnie. Zarządzanie dużą liczbą
instancji aplikacji staje się kłopotliwe oraz czasochłonne.
Z pomocą przychodzi nam możliwość skalowania naszej aplikacji na klastrze
Mesos. Uruchomienie 10, czy 100 instancji aplikacji sprowadza się tylko do dwóch
kliknięć w interfejsie WWW Marathona, lub do wysłania requesta pod
zasób naszej aplikacji dostępny poprzez REST API. Jest to wygodny i bardzo
szybki sposób na obsłużenie dużej liczby użytkowników.

Request, dzięki któremu zeskalujemy naszą aplikację, powinien być typu `PUT`
oraz musi zostać wysłany pod zasób `/v2/apps/` wraz z nazwą naszej aplikacji.
W naszym przypadku będzie to `/v2/apps/rest_app`.
Zawartość przesłanego żądania wygląda następująco:

    {
        "instances":10
    }

Marathon po otrzymaniu takiego żądania przystąpi do procesu uruchomienia
zadeklarowanej przez nas liczby instancji na klastrze. Nie musimy się martwić,
na jakich serwerach zostanie uruchomiona nasza aplikacja, wszystko stanie się
automatycznie bez naszej ingerencji.

## Skalowanie automatyczne

Serwer pełniący role slave'a, będący częścią klastra Mesos, udostępnia informację
o aktualnym wykorzystaniu zasobów przez aplikacje, które zostały na nim
uruchomione. Dane te są dostępne poprzez REST API pod zasobem
`/monitor/statistics.json`.

Przykładowe dane dotyczące uruchomionej aplikacji:

    {
        executor_id: "app-new.0d85b86a-4f60-11e5-9031-56847afe9799",
        framework_id: "20150827-194534-16842879-5050-1219-0001",
        statistics: {
            cpus_limit: 0.2,
            cpus_system_time_secs: 91.05,
            cpus_user_time_secs: 11.32,
            mem_limit_bytes: 50331648,
            mem_rss_bytes: 100966400,
            timestamp: 1441047277.2822
        }
    },

Zużycie zasobów przez nasze aplikacje zazwyczaj nie jest równomierne w ciągu
doby. Podczas dnia możemy potrzebować większej liczby instancji, aby sprostać
dużej liczbie użytkowników, zaś w nocy przy małym ruchu większość instancji
będzie się nudzić. Zbierając metryki dotyczące zużycia zasobów przez nasze
instancje aplikacji uruchomionych na klastrze Mesos, jesteśmy w stanie
automatycznie zarządzać liczbą instancji.

Możemy stworzyć prosty mechanizm autoskalowania, który, w oparciu o zebrane
metryki zużyć naszej aplikacji, zdecyduje o dołożeniu dodatkowych instancji,
tak aby sprostać dużej liczbie użytkowników.

Pseudokod mechanizmu autoskalowania:

    MIN_INSTANCES_COUNT = 4
    MAX_INSTANCES_COUNT = 100

    # wykrywamy sytuację, w której 90% naszych instancji jest obciążona,
    # i zwiększamy liczbę wszystkich instancji o 2 pod warunkiem,
    # że nie osiągnęliśmy maksymalnej liczby instancji.

    if overloaded_instances >= 0.9 * total_instances:
        total_instances += 2
        if total_instances <= MAX_INSTANCES_COUNT:
            scale_app(instances_count=total_instances)

    # wykrywamy sytuację, w której tylko 50% naszych instancji jest obciążona,
    # i wtedy zmniejszamy całkowitą liczbę o 2 pod warunkiem,
    # że nie osiągnęliśmy maksymalnej liczby instancji.

    elif overloaded_instances <= 0.5 * total_instances:
        total_instances -= 2
        if total_instances >= MIN_INSTANCES_COUNT:
            scale_app(instances_count=total_instances)

Powyższy pseudokod przedstawia sytuację, w której, w zależności od liczby
obciążonych instancji aplikacji, możemy automatycznie zwiększyć lub zmniejszyć
ich liczbę poprzez wysłanie odpowiedniego requesta do Marathona.

Dobranie odpowiednich wartości parametrów sterujących procesem
autoskalowania nie jest rzeczą łatwą, lecz metodą prób i błędów jesteśmy
w stanie znaleźć optymalne dla nas wartości.


## Podsumowanie

Klaster Apache Mesos w połączeniu z Marathonem umożliwa szybkie i wygodne
deployowanie aplikacji napisanych w Pythonie. Dzięki niemu możemy w łatwy
sposób zarządzać liczbą instancji, a także zasobami używanymi przez
aplikacje, a wszystko to dzięki prostocie działania i możliwościom
przeprowadzania wszystkich operacji poprzez REST API.


## Referencje

* [1] Mesos Framework Development Guide \hyphenatedurl{http://mesos.apache.org/documentation/latest/app-framework-development-guide/}
* [2] Marathon framework \hyphenatedurl{https://mesosphere.github.io/marathon/}
* [3]  \hyphenatedurl{https://gist.github.com/quamilek/4fd1f246feb6149dd1dd} - kod źródłowy pliku `api.py`
* [4] Falcon framework http://falconframework.org
* [5] PEX library https://github.com/pantsbuild/pex
* [6] Marathon REST API \hyphenatedurl{https://mesosphere.github.io/marathon/docs/rest-api.html}

## Źródła

* Apache Mesos http://mesos.apache.org/
* Marathon framework https://mesosphere.github.io/marathon/
* PEX library documentation https://pex.readthedocs.org/en/stable/
