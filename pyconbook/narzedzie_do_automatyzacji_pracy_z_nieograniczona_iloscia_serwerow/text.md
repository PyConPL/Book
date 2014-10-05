# Narzędzie do automatyzacji pracy z nieograniczoną ilością serwerów
## Marek Glijer

Automatyzacja zmian w plikach konfiguracyjnych przydaje się zawsze, kiedy dysponujesz więcej niż jedną maszyną produkcyjną lub instancją aplikacji. Dzięki zastosowaniu narzędzia, które samo rozpropaguje zmiany, unikniesz trywialnych, uciążliwych i trudnych do diagnozowania błędów. Zwłaszcza w przypadku pracy pod presją czy w trybie 24/7. W tym materiale postaram się opisać jak powinno wyglądać takie narzędzie, dlaczego warto przygotować je samemu i jakie wymierne korzyści przyniesie Twojej firmie.

Warto pisać narzędzia. Idea zastępowania ludzkiej, powtarzalnej pracy, w której problemy są dobrze zdefiniowane nie jest nowa. Pomimo tego niektórzy administratorzy i programiści rzadko korzystają z udogodnień automatyzacji. Taki stan determinuje często brak chęci inwestowania własnego czasu w coś, co nie stanowi z pozoru żadnej wartości dodanej, nie jest produktem, za który klient gotów będzie zapłacić, a nietechniczny menedżer – docenić. To mylne przekonanie, gdyż w czasach kiedy systemy informatyczne rozrastają w niespotykanym dotąd tempie, pewnego dnia może być za późno na pisanie ambitnych narzędzi automatyzacyjnych. Należy oczywiście pamiętać o zachowaniu proporcji i relatywizmu, aby – jak często piszą – „nie strzelać z armaty do muchy”. Jeśli jesteś w momencie, w którym monotonia zjada Twój dzienny harmonogram zadań choćby w małym stopniu, to doskonała okazja na napisanie środowiska automatyzacji. Przy okazji tego artykułu skupimy się na automatyzacji pracy administratora, programisty, wdrożeniowca czy deploy-managera.

Warto pisać narzędzia, nie tylko z lenistwa, ale przede wszystkim dla celów bezpieczeństwa. Dobrze napisany i regularnie testowany kod nie ma prawa się pomylić. A nawet najlepszy inżynier to „tylko” człowiek. Z góry ustalony algorytm jest po prostu pewniejszy.

### Cel

Nasz projekt ma być prostym narzędziem do automatyzacji propagacji konfiguracji  opierającej się o pliki tekstowe (dowolnego formatu). Dodatkowo powinno potrafić propagować komendy systemowe do wykonania. To nie może być nic skomplikowanego, gdyż samo zadanie jest dość trywialne. Gdybyśmy przekazywali je młodszemu administratorowi / programiście, powiedzielibyśmy mniej więcej: - Proszę, oto nowy plik konfiguracyjny dla programu X, zrób tak, aby znalazł się na wszystkich naszych maszynach. Po wgraniu go na serwer zrestartuj usługę X.

### „It's a trap!”

Nie trudno przewidzieć czyhające na nas pułapki. Kilka najbardziej oczywistych:

1. Problemy z bezpieczeństwem. Ktoś mógłby użyć naszego narzędzia jako świetnego pomocnika w przeprowadzeniu ataku. Filtrowanie żądań, autoryzacja i konfiguracja firewalli na maszynach powinny skutecznie zabezpieczyć naszą architekturę przed omyłkowym czy też nieautoryzowanym użyciem narzędzia automatyzującego pracę.
2. Single-point-of-failure. Jeśli nagle coś stanie się z maszyną, z której zazwyczaj przeprowadzaliśmy operacje administracyjne – nie będziemy mogli efektywnie zarządzać serwerami. Dlatego też oprogramowanie do automatyzacji powinno być pozbawione tej wady i działać niezależnie na wszystkich maszynach. Dzięki temu rozwiążemy też problem związany z długim czasem propagacji.
3. Podział węzłów. Chcesz zarządzać automatycznie serwerami, ale tylko niektóre z nich mają część wspólną? Powinniśmy założyć, że pliki konfiguracyjne będą różne w zależności od konkretnych podgrup serwerowych. Zakładając, że wszystkie Twoje środowiska produkcyjne, na których chcesz wykorzystywać ten automat działają dokładnie tak samo – będziesz mieć jedną podgrupę. Jeśli jednak Twoje serwery można byłoby podzielić na usługi, których utrzymywaniem się zajmują np. WWW, bazy danych, obliczenia, storage czy backup – wówczas do każdej z tych grup możesz przyporządkować sobie odpowiednie węzły, aby później móc łatwo rozesłać nowy plik konfiguracyjny do wydzielonego obszaru Twojego ekosystemu.
4. Wykonywanie poleceń. Po podmianie pliku konfiguracyjnego większość aplikacji wymaga ponownego uruchomienia. Dlatego też nasze narzędzie będzie mogło rozprowadzić żądanie o wykonanie komend, które należą do białej listy (np. można wykonać ponowne uruchomienie, ale nie można zatrzymać). Taka biała lista także powinna być przechowywana bez struktury z Single-point-of-failure.

### Własne rozwiązanie w Pythonie

Prosty zestaw skryptów w Pythonie, które będą zwięzłe i dostosowane do Twoich potrzeb to idealne rozwiązanie. Każdy programista czy administrator będzie w stanie zobaczyć jak funkcjonuje to narzędzie i dostosować je do ciągle zmieniających się wymagań (dołożyć nowy serwer do grupy, dołożyć nowy typ operacji synchronizującej, zmodyfikować obecne). Wykorzystując Twisted jako framework do komunikacji będziemy w stanie napisać wersję zerową (działający proof-of-concept) w kilkanaście minut. Jak powinno to działać?

Na każdym węźle jest dokładna kopia narzędzia. Komenda wysyłająca może wyglądać banalnie, np. tak:
python admin-robot.py send <configuration_file> <group> 

Węzeł służy zarówno do propagacji konfiguracji jak i do odbioru (nasłuchu) zmian pojawiających się na innych serwerach. Każda zmiana jest zapisywana tak, aby można było łatwo prześledzić modyfikacje konkretnych plików konfiguracyjnych w ekosystemie. Dodatkowo dobrze byłoby zaplanować mechanizm synchronizacji, aby każdy nowy węzeł mógł pobrać sobie automatycznie najnowsze wersje plików konfiguracyjnych kiedy tylko zostanie dołączony do grupy (obsługa tzw. „zimnego startu” nowego serwera).

### Korzyści

1. Każdy administrator / programista, który będzie miał uprawnienia do wykorzystywania narzędzia, będzie mógł przeprowadzać bezpieczne interwencje na środowisku produkcyjnym ograniczając do niezbędnego minimum czynnik ludzki.
2. Można wykonywać synchronizację szybciej niż najszybszy administrator.
3. Mamy dostęp do dzienników - kto dokonał jakich zmian, na jakich serwerach i w jakim czasie.
4. Narzędzie jest na tyle małe i proste, że pozwala na bardzo szybkie wprowadzanie modyfikacji i dostosowywanie do zmieniających się warunków w całym ekosystemie informatycznym przedsiębiorstwa.
5. Można za jego pomocą łatwo wycofywać wprowadzone zmiany, tworzyć lustra konfiguracji i efektywnie nimi zarządzać.
6. Skalowanie bez znacznego zwiększania kosztów administracji będzie bardzo proste.


[http://twistedmatrix.com](http://twistedmatrix.com)
[http://zookeeper.apache.org](http://zookeeper.apache.org)
