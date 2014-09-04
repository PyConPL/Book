# Python w Chmurach
## Dariusz Aniszewski

Wyobraźmy sobię osobę związaną z branżą IT, która nie spotkała się jeszcze z terminem *chmura oblczeniowa*. 
Nie da się. Słowa *as a Service* robią ogromną karierę i cieszą się rosnacą popularnością. 
Z chmur korzysta coraz więcej użytkowników, od małych developerów po wielkie korporacje. 
Jeśli ktoś myśli, że chmury obliczeniowe nie są dla niego, najprawdopodobniej jest w błędzie. 
Jeśli ktoś uważa, że nie używa ich na codzień, również najprawdopodobniej nie ma racji. 
Serwisy takie jak Facebook albo Gmail to typowe usługi chmurowe. Dropbox i Dysk Google to niemal książkowe przykłady
chmury oferującej usługę przechowywania danych. Przykłady można mnożyć. Skupmy się jednak na tym, jak
wykorzystać *cloud computing* do rozwijania własnych Pythonowych aplikacji. Na początek jednak krótka nota historyczna. 

## Krótka historia
Mogłoby się wydawać, że chmury obliczeniowe to wynalazek ostatnich kilku lat. A jednak... Ich idea sięga końca lat 60-tych ubiegłego wieku i zakłada istnienie rozproszonych, skalowalnych systemów, dostępnych z dowolnego miejsca na świecie. Przez lata jednak niewiele się działo w tym kierunku, przynajmniej w sferze rozwiązań
dostepnych publicznie. W 1999 roku firma Salesforce zaczęła dostarczać swoje produkty przez przeglądarkę - był to 
kamień milowy i prekursor do modelu *Software as a Service*. Następny kamień położył Amazon, startując w 2002 roku
z Amazon Web Services, a 4 lata później udostępniajac usługę *Elastic Cloud Computing* (EC2) będącą udzieleniem
dostępu do maszyny wirtualnej pracującej w chmurze. Od tego dnia Internet nie był już taki sam. W 2009 roku do wyścigu
dołączył Google, a chwilę później Microsoft. Następnie nastąpił boom na różne usługi dostępne w modelu chmury obliczeniowej i trwa on po dzień dzisiejszy.

## Chmura obliczeniowa
Czym więc jest w obecnym czasie chmura? Najprościej - usługą. Usługą przechowywania plików, albo usługą 
serwisu bazodanowego. Może to być też usługa udostępnienia maszyny wirtualnej, albo przeprowadzania obliczeń.
Może to być jakakolwiek usługa, możliwa do dostarczenia przez Internet, za jaką użytkownicy będą skłonni
zapłacić. 
Obecnie chmury możemy podzielić na trzy typy:

* Infrastructure as a Service (IaaS) - w tym modelu usługą jest najczęściej maszyna wirtualna
* Platform as a Service (PaaS) - dostęp do platformy, na której możemy uruchamiać aplikacje
* Software as a Service (SaaS) - oprogramowanie dostępne przez przeglądarki

Idąc po koleji, w modelu *IaaS* klient dostaje dostęp do pewnej części infrastruktury teleinformatycznej. Najczęściej 
jest to po prostu maszyna wirtualna, ale mogą to być też np. serwery SMTP czy baza danych. Konfiguracja i instalacja 
oprogramowania spoczywa na kliencie. Model *PaaS* jest rozwinięciem infrastruktury, w której operator dostarcza już
pewne mechanizmy odciążające użytkowników z instalacji oprogramowania czy konfiguracji serwerów. Klient musi jedynie
wgrać swoją aplikację oraz wskazać plaftormie sposób jej uruchomienia. *SaaS* jest natomiast niczym innym jak 
oprogramowaniem dostępnym przez przeglądarkę. Oprogramowanie tego typu jest bardzo zróżnicowane - mogą to być pakiety biurowe, programy graficzne, księgowe i wiele innych.

Koszty usług chmurowych są bardzo zróżnicowane i każdy operator ma swój cennik za poszczególne produkty.
Panuje jednak jedna zasada - klient jest rozliczany z używanych zasobów. Dla przykładu jeśli trzeba przeprowadzić
skomplikowane obliczenia, można utworzyć kilka maszyn wirtualnych, połączyć je w macierz i po zakończeniu obliczeń
je wyłączyć. Koszty będą generowane tylko podczas pracy tych maszyn. Jest to ogromna zaleta chmur, bez których
konieczny byłby zakup fizycznych komputerów, które byłyby wykorzystywane sporadycznie, a koszt ich zakupu i 
konserwacji znacząco przewyższałby koszty takiego samego zestawu w chmurze.

## Przygotowania
Skoro wiemy już co nieco o chmurach, czas je wykorzystać w praktyce. W chmurze możemy serwować wszelkie aplikacje
pythonowe posiadające wywołania po protokole HTTP. Możemy zatem użyć dowolnego frameworka do aplikacji internetowych,
np. Django czy Flask. Możemy również sami zaimplementować nasz serwer używając np. modułu *SimpleHTTPServer* z 
biblioteki standardowej. Dla dalszych rozważań przyjmijmy, że nasza aplikacja będzie korzystała z Django. Ta aplikacja
będzie korzystała z relacyjnej bazy danych Postgresql (choć może być też np. MySQL) i będzie umożliwiała 
użytkownikom wgrywanie plików do 30MB. Komunikację będziemy prowadzili po protokole HTTPS. Mamy wykupioną własną domenę
oraz certyfikat SSL. Spodziewamy się umiarkowanego ruchu, który z czasem będzie wzrastał. Dobrze i co dalej?

Musimy teraz wybrać typ chmury z jakiej chcemy korzystać oraz jej dostawcę. Dla naszej aplikacji rozważmy wady
i zalety modeli IaaS oraz PaaS. Jako reprezentantów obu modeli przyjmijmy: Amazon EC2 dla infrastruktury oraz Heroku
dla platformy. Sprawdźmy najpierw, jak dokładnie działają obydwa te serwisy.

### Amazon EC2
Usługa Elastic Cloud Computing jest niczym innym, jak udostępnianiem wirtualnych maszyn. Możemy zatem utworzyć maszynę
posiadającą określoną moc obliczeniową czy dysk twardy. Dodatkowo wybieramy system operacyjny, jaki ma na niej
zostać zainstalowany oraz generujemy parę kluczy RSA, potrzebnych do połaczenia się z maszyną przez SSH. Jeśli chcemy 
wykorzystać swój zestaw kluczy, możemy podać swój klucz publiczny zamiast generować nową parę. W obecnej
chwili możemy wybierać z systemów UNIXowych, np. Ubuntu, Debian, CentOS oraz Microsoft Server. Każda
maszyna przy uruchomieniu ma przyznawany publiczny adres IP, można też zarezerwować stały adres IP i przypiąć go do 
danej maszyny, wtedy pomimo restartów publiczny adres IP nie ulegnie zmianie. Po utworzeniu maszyny i przyznaniu jej 
stałego adresu musimy przystąpić do konfiguracji, czyli m.in.

* otworzyć porty 22 (SSH), 80 (HTTP), 443 (HTTPS), ewentualnie inne wedle potrzeby
* zainstalować wymagane komponenty systemowe
* zainstalować i skonfigurować niezbędne serwisy
* zainstalować wymagane paczki Pythonowe
* wgrać, skonfigurować i uruchomić naszą aplikację i wszystkie jej komponenty

Jak widać, na uruchomienie aplikacji na EC2 należy poświecić nieco czasu i pracy, jednak w zamian mamy pełną kontrolę 
nad tym, co się właściwie dzieje. Jedyne ograniczenia wynikają głównie z możliwości utworzonej maszyny.

### Heroku
Heroku jest platformą uruchomieniową dla aplikacji napisanych w różnych językach - Ruby, Python, Java, NodeJS i innych.
Heroku do swojego działania wykorzystuje wirtualizowane kontenery UNIXowe, marketingowo zwane *Dyno*. Dla uproszczenia 
można przyjąć, że jedno *Dyno* to odpowiednik jednej maszyny, choć w praktyce na jednej wirtualnej maszynie może 
istnieć wiele wyizolowanych kontenerów. Aby uruchomić aplikację na Heroku, należy poinformować platformę jak należy to zrobić. W przypadku Pythona należy wykonać dwa kroki:

1. dostarczyć plik **requirements.txt** z wylistowanymi paczkami pythonowymi jakie muszą zostać zainstalowane
2. dostarczyć plik **Procfile** w którym podamy komendę uruchamiającą aplikację, np. ```web: python manage.py runserver 0.0.0.0:$PORT```

Aby plafroma Heroku mogła sprawnie i bezobsługowo działać, narzucone są pewne ograniczenia:

* ulotny system plików - jeśli w trakcie działania naszej aplikacji coś zostanie zapisane na dysk, w momencie jej 
restartu będzie bezpowrotnie utracone. Jest to bardzo ważne ograniczenie, które należy mieć w świadomości już na etapie projektowania aplikacji.
* 30 sekundowy timeout - jeśli nasza aplikacja nie wyrobi się w ciągu 30 sekund z rozpoczęciem wysyłania odpowiedzi, 
Dyno Manager zwróci status 503. Należy mieć na uwadze, że pomimo wysłania statusu błędu, Dyno będzie ciągle
przetwarzać zapytanie, w tym przeprowadzać rozpoczęte operacje na bazie danych, co może prowadzić do niespójności.
* 512MB pamięci operacyjnej - jeśli aplikacja potrzebuje dużej ilości pamięci operacyjnej, Heroku nie jest najlepszym
wyborem - po przekroczeniu 512MB Heroku zacznie używać pliku wymiany (SWAP), co drastycznie wpłynie na wydajność.
* usypianie dyno - jeśli nasza aplikacja wykorzystuje tylko jedno Dyno i w ciagu godziny nie było wykonane żadne zapytanie, Dyno zostaje uśpione. Uśpione Dyno nie pracuje, więc jeśli zostanie wysłane do niego zapytanie to Dyno Manager musi je najpierw wybudzić, co powoduje, że pierwsze zapytania mogą mieć dłuższy czas oczekiwania na odpowiedź.

Niewątpliwym plusem Heroku jest natomiast minimalna ilość pracy jaką należy wykonać, aby uruchomić aplikację. Dodatkowo Heroku oferuje bardzo dużo dodatków, np.

* bazy danych: relacyjne i NoSQL
* monitoring
* analiza wydajności
* agregowanie i przeszukiwanie logów
* i wiele innych

Te dodatki są de facto powiązanymi usługami chmurowymi, którymi możemy rozwijać naszą aplikację. 

Aplikacje na Heroku mają swoje własne domeny w postaci `<nazwa-aplikacji>.herokuapp.com` działające zarówno po HTTP 
jak i HTTPS. Dostajemy również repozytorium Git, służące do wgrywania kolejnych wersji.

## Wybór chmury
Skoro wiemy już czym charakteryzują się EC2 i Heroku, nadszedł czas na wybranie najbardziej pasującej usługi. W tym
celu dokonajmy konfrontacji wymagań naszej aplikacji z możliwościami serwisów.

### Wsparcie dla Django
Zarówno Heroku jak i EC2 mają wsparcie dla aplikacji korzystających z frameworka Django. Przy EC2 należy poświęcić 
więcej czasu na instalację i konfigurację systemu niż ma to miejsce na Heroku, gdzie musimy tylko dostarczyć plik
requirements.txt (który prawdopodobnie i tak mamy) i Procfile. Na EC2 sami musimy zainstalować paczki pythonowe wraz 
z wymaganymi pakietami systemowymi.

### Baza danych Postgresql
W kwestii bazy danych sytuacja jest bardziej zawiła, ale oba serwisy umożliwiają nam jej obsługę. Wybierając ofertę
Amazona mamy do wyboru dwie opcje. Pierwszą jest instalacja serwera bazodanowego na tej samej maszynie, na której
działa nasza aplikacja. Drugą opcją jest skorzystanie z dedykowanej bazom danych usługi *Amazon Relational Database 
Service* - **RDS**. Wybór wariantu nie jest prosty - w przypadku instalacji na tej samej maszynie będziemy mieli 
problemy ze skalowalnością, ale korzystając z RDS generujemy dodatkowe koszta w przypadku używania tylko jednej 
instancji EC2 dla obsługi naszej aplikacji.

Na Heroku sprawa jest rozwiązana za nas. Baza danych dostępna jest jako dodatek, a my musimy jedynie wybrać plan cenowy. Na początek wystarczy plan darmowy, ale posiada on limit 10 000 wierszy. Po przekroczeniu tej ilości baza przestanie dodawać nowe rekordy i będziemy zmuszeni do zmiany planu na płatny.

### Wgrywanie plików do 30 MB
To jest kluczowy punkt w specyfikacji wymagań. Umożliwienie wgrania plików przez użytkowników oznacza, że musimy je gdzieś przechowywać, a ich rozmiar będzie rósł wraz z ilością użytkowników. Jeśli pamiętamy ograniczenia zarówno 
EC2 jak i Heroku, dochodzimy do wniosku, że żadne z nich nam nie wystarczy. Jeśli wybierzemy EC2 to prędzej czy później 
wyczerpie nam się miejsce na dysku. W przypadku Heroku system plików jest ulotny, więc wgrane pliki są nietrwałe. 
Rozwiązaniem obydwu problemów będzie skorzystanie z kolejnej usługi - *Amazon Secure Storage Service* (Amazon **S3**).
Ta usługa jest również polecana przez Heroku do przechowywania plików. S3 jest, jak nazwa mówi, usługą przechowywania 
plików, w której miejsce jest nieograniczone. Rozliczani jesteśmy z ilości danych, jakie przechowujemy oraz transferu. 
Do wgrywania plików na S3 możemy użyć modułu `boto`.

### Obsługa HTTPS na własnej domenie.
Obydwa serwisy umożliwiają bezpieczną komunikację. Na EC2 należy wgrać certyfikaty na serwer WWW i odpowiednio go 
skonfigurować. Niestety na Heroku, chcąc korzystać z HTTPS z własną domeną, poza wgraniem certyfikatów jesteśmy zmuszeni do dokupienia dodatku *SSL Endpoint* w cenie 20$/miesiąc.

### Skalowalność
Skalowalność jest bardzo ważnym aspektem aplikacji, obydwa serwisy oferują wsparcie. Tak samo, jak w przypadku innych 
wymagań, zapewnienie skalowalności na EC2 jest bardziej złożone i wymaga dodania maszyny typu *Load Balancer* 
oraz utworzenia żądanej ilości maszyn z pracującą aplikacją. Na Heroku można zmienić ilość używanych Dynos korzystając z przeglądarki i ustawiając żądaną ilosć w konfiguracji aplikacji.

### Konkluzja
Obydwa serwisy jak najbardziej nadają się do serwowania aplikacji pythonowych, a ich różnice wynikają w dużej mierze z 
wyboru modelu, w jakich pracują. W ogólnym rozliczeniu EC2 w modelu IaaS będzie wypadało korzystniej pod kątem 
miesięcznych opłat, lecz będzie wymagało większych nakładów na konfiguracje i utrzymanie systemu. Heroku jest wygodniejsze w obsłudze, jednak w środowisku produkcyjnym zapewne będzie droższe od EC2.

## Podsumowanie
Jak widać wybór serwisu chmurowego dla naszej aplikacji nie jest sprawą prostą i wymaga bardzo indywidualnego 
podejścia. Pod uwagę należy wziąć zarówno obecne wymagania funkcjonalne i pozafunkcjonalne oprogramowania, perspektywy rozwoju oraz budżet jakim dysponujemy.

### Źródła

* http://www.citeworld.com/article/2114518/cloud-computing/saas-top-50-list.html - artykuł wymieniający serwisy chmurowe
używane na codzień.
* http://www.computerweekly.com/feature/A-history-of-cloud-computing - historia chmur obliczeniowych
* https://aws.amazon.com/marketplace/search?page=1&category=2649367011 - dostępne systemy na EC2
* https://devcenter.heroku.com/categories/language-support - języki programowania wspierane na Heroku
* https://devcenter.heroku.com/articles/dynos - co to jest Dyno
* https://addons.heroku.com/ - dodatki do Heroku
* Wykorzystanie technologii chmury obliczeniowej do zwiększenia zasięgu oprogramowania desktopowego - praca dyplomowa magisterska, autor mgr inż. Dariusz Aniszewski, promotor dr inż. Piotr Helt
