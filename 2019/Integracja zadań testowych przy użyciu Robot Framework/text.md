#Integracja zadań testowych przy użyciu Robot Framework

### Krzysztof Synak, Mateusz Kotas

 

## Wprowadzenie

Najgorszą częścą pracy w korporacji jest dla wielu kwestia papierologii i biurokratyzacji. Pewnie, fajnie jest potestować,
a jeszcze fajniej coś zepsuć; sprawić, że jakość się poprawiła. Ale zawsze dochodzimy do momentu, w którym należy rozliczyć
się z postępów. A to "pozamykać zadania", a to dostarczyć kluczowe wskaźniki wydajności; a to po prostu stworzyć raporty
testowe. W pewnym momencie jednak dochodzimy do wniosku, ze wszystko to są powtarzalne czynności, które równie dobrze może wykonać robot.

A tester może się skupić na testowaniu.
## Problem
Po zatrudnieniu całej gamy barwnych i zdolnych ludzi, zauważyliśmy narastającą ich niechęć do "klepania". Klepanie
definiowaliśmy na wiele sposobów, czy to klepanie raportów testowych, czy klepanie tych samych testów. Skończył się
w końcu natłok zadań związany z budowaniem nowych narzędzi, zaczęło się _zwyczajne życie_.

### Powtarzalne, nudne zadania
Nordea Bank jest silnie sformalizowaną firmą, która stara się zażegnać biurokratyczne podejście, jednakże póki co, fakty
są faktami -- papiery muszą się zgadzać! Plany testowe, raporty testowe, składowanie przypadków testowych... wszystkie
testalia zostaly już omówione i zarządzone. Pozostaje tylko wypełnić. To nie są zadania dla młodych, ambitnych i żywych
specjalistów.

### Złe rozłożenie aktywności
Jak to zwykle bywa w papierologicznych środowiskach, okazało się, że testerzy wykonują kawał dobrej roboty... który nie
jest testami. Wystawianie nowych wersji produktów zaczęło się opóźniać, błędy wykrywane dopiero po fakcie, ale według
papierów wszystko jest perfekcyjne.

### Niewyróżniające się na rynku stanowisko

Przez powyżej opisane sytuacje, szybko okazało się, że nawet rekrutacja nie do końca wykazuje się sukcesami. Uczciwe
stawianie sprawy dotyczącej biurokracji i zadań testera odstręczało niektórych, a innych nie zachęcało -- przecież takich
miejsc pracy jest wiele.

## Rozwiązania
Zdecydowaliśmy się wykorzystać narzędzia obecne i nieobecne dotąd w Nordei do zautomatyzowania i uatrakcyjnienia naszej
pracy i wyników naszej pracy. Jak wiadomo, nie tylko dane się liczą, ale również czytelna i atrakcyjna ich prezentacja.
Do osiągnięcia tego celu zaprzęgnęliśmy wszystkich naszych inżynierów. Zmieniliśmy język używany do określania naszego
zespołu. Po wydaniu pierwszego narzędzia, oficjalnie już nie byliśmy testerami, tylko *inżynierami jakości*.

### Automatyzacja za wszelką cenę
Zdecydowaliśmy się podejść do sprawy kompleksowo. Każde zadanie, które trzeba było wykonać więcej niż raz, w ten sam
sposób, sprowadziliśmy do postaci algorytmu. Każdy dokument opisaliśmy przy pomocy jinja2. Żeby wszystkie te automatyzacje
były dostępne, stworzyliśmy portal testera, prezentujący proste wizualizacje danych oraz pozwalający na wywołanie funkcji
samo-pracujących.
 
### Szeroki wybór narzędzi
"Rynek", o ile możemy tak nazwać zbiór narzędzi dostępnych za darmo dla każdego użytkownika, oferuje ogromną liczbę
narzędzi, które można -- a czasem trzeba -- wykorzystać do automatyzacji procesów w firmie. Narzędzia zarówno płatne
i te bezpłatne, roznią sę często tylko odrobiną pracy koniecznej do włożenia. Do wdrożenia procesów ciągłej integracji,
można użyć wielu bezpłatnych narzędzi, które w niczym nie ustępują płatnym opcjom. GitLabCI, TeamCity, Jenkins są równie
użyteczne co Bamboo i GitLab. Można wykorzystywać Bitbucket od Atlassiana, a można po prostu postawić
instancję Gita. Można użyć SonarQube, ale też można bez problemu oprogramować darmowe, proste narzędzia badające
pokrycie kodu.

### Rozwój własnych narzędzi
Ale to nie koniec! Przecież jako programści -- tym bardziej Pythona -- możemy tworzyć własne narzędzia. Możemy tworzyć
narzędzia do obsługi tych narzedzi. Niejako rekurencyjnie tworząc karuzelę automatyzacji, można osiągnąć cel
najwłaściwszy dla czasów czwartej rewolucji przemysłowej - ograniczenia ludzkiego wkładu do pracy kreatywnej. Przy
odpowiednim nakładzie pracy na etapie projektowania tych narzędzi, może się okazać, że bardzo wielu aktywności nie
trzeba monitorować ręcznie. Pokrycie historyjek, informacja o koniecznych przeglądach, badanie jakości kodu...
to wszystko da się zrobić automatycznie przy użyciu własnych narzędzi bądź własnych konfiguracji. Portale informacyjne,
proste aplikacje okienkowe; często przy niedużym nakładzie pracy można otrzymać narzedzia pożądane w firmie nawet poza
naszym zespołem.

## Wynik działań
Po tych wszystkich wzniosłych hasłach, przyszedł czas na weryfikację aktywności automatyzacyjno-wytwórczych.
Zainwestowawszy czas "nieużytków", czyli kiedy tak czy siak nie była potrzebna praca okołoprojektowa, stworzyliśmy
zestaw narzędzi, które w niedalekiej przyszłości poskutkowały znaczącymi oszczędnościami pieniędzy i zyskami w jakości
i zadowoleniu tak klientów wewnętrznych jak i nas jako wytwórców.

### Zadowolony zespół
Zespół testerski szybko odnalazł sie w nowej sytuacji. Wkrótce samo wytwarzanie narzędzi testowych/automatyzujących
stało się jedną z zanęt do pracy z nami. Mając zawsze w niedalekiej perspektywie możliwość zaprezentowanie czegoś
wytworzonego własnymi rękami usprawniło i umiliło same prace testerskie, zachęcając do tworzenia coraz bardziej użytecznych
testów i narzędzi okołotestowych.

### Zadowolony klient
W związku ze zwiększonym zadowoleniem testerów i zwiększeniem ich wydajności, zadowoleni stali się także nasi klienci,
właściciele produktów i kierownicy projektów zauważyli, że po zmniejszeniu nakładu czasowego na wytwarzanie papierów,
sama treść tych papierów stała się dużo lepsza, obszerniejsza i bardziej celowa.

### Narzędzia rozprzestzenione na cała firmę
Nie minęło dużo czasu, nim zaczęli nas odwiedzać pracownicy z całkiem innych działów firmy. Byli zainteresowani bazą
bibliotek, narzędzi i mechanizmów automatyzacyjnych. Zjawiali się ze swoimi pomysłami, ale i pomagali - i pomagają -
rozwijać istniejące narzędzia. Stworzony przez nas portal do generacji raportów i planów testów, wykorzystujący dane
z Jiry, został przyjęty do realizacji jako narzędzie obowiązujące w całej firmie, wraz z przydzieleniem konkretnego
budżetu na rozwój.

### Przyśpieszenie dostarczania i podwyższenie jakości
Dzięki zautomatyzowanym procesom dostępnym na tzw. _klik_, znacząco zwiększyła się przepustowość zespołu testerskiego.
Mimo, że część czasu każdego z inżynierów była poświęcona na rozwój wspólnych narzędzi, i tak odnotowano wzrost liczby
znalezionych błędów i usprawnień w projektach. Testy przestały opóźniać publikację nowych wersji oprogramowania, bo znikła
potrzeba "klepania" raportów co sprint.

### Firma nie odnotowała kosztu
A co najważniejsze w tym wszystkim, firma nie odnotowała żadnego (dodatkowego) kosztu. Wykorzystane narzędzia były darmowe,
albo uprzednio zakupione przez Nordeę. Czas wykorzystany na rozwój automatyzacji był i tak czasem "straconym". Tj. zamiast
oczekiwania na coś, zabieraliśmy się za usprawnienia.

## Zrób to sam!
W każdym zespole można zrobić to co my. Rozwój odpowiednio zaprojektowanych narzędzi zawsze przyniesie oszczędności
w długim okresie czasu. Mimo że my użyliśmy części płatnych narzędzi, wcale nie jest to konieczne.

### Bezkosztowe narzędzia
W zasadzie każde platne narzędzie ma swój darmowy odpowiednik. Bitbucket - GitLab, Bamboo - TeamCity itd. Do tego
dochodzi cała masa narzedzi po prostu darmowych, takich jak Argo, Ansible czy zwykły Python. Wykorzystanie tych
możliwości pozwala na uzyskanie zysków bez żadnego wkładu finansowego. Nie jest również żadnym problemem, a jest prostym
sposobem na uzyskanie pochwał to, że można użyć ich do analityki (np. Grafana), by badać co się właściwie dzieje. Można
również traktować istniejące narzędzia w firmie jako "darmowe" i na podstawie ich rozszerzonych często możliwości, a
przynajmniej przy wykorzystaniu wsparcia technicznego, rozwijać ekosystem narzędziowy w wymagane strony.

### Grywalizacje
Zachętą do regularnego kontrybuowania do wspólnych narzędzi może być wykorzystanie technik grywalizacyjnych, które u nas
skończyły się również implementacją całego systemu do obsługi "gry", co znowu było nie dość, że rozwinięciem obecnych
narzędzi, to jeszcze niejako nagrodą za uczestnictwo (zamiast kolejnych testów big data, mały sklepik internetowy).

### To się opłaca każdemu
Najważniejsze w tym wszystkim jest to, że każdej firmie opłaca się stworzyć własny ekosystem przy użyciu darmowych
narzędzi. Wprowadzenie CI/CD jest często oczywiste, ale nie zawsze oczywistym jest to, że w te mechanizmy można i należy
wpleść odpowiedzialności testerskie. W ten sposób, obok automatycznego wykonywania testów programisty i raportowania
nowych wersji, nagle okazuje się, że kosztem kilku dni poza normalnymi obowiązkami pracowniczymi, można zautomatyzować
wszystko. A potem skupić sie na tej fajnej robocie.

## Źródła
* [Python](https://www.python.org)
* [Jenkins](https://jenkins.io)
* [Argo](https://blog.argoproj.io/tagged/workflow-automation)
* [Ansible](https://www.ansible.com)
* [Narzędzia Atlassian](https://www.atlassian.com/)
* [Cenniki GitLab](https://about.gitlab.com/pricing/)
