# Python w projektach sprzętowych - Piotr Maliński

## Skąd ta popularność projektów "hardware plus software"?

Nieustający rozwój technologii cyfrowych popularyzuje dostęp do Internetu, jak
i coraz lepszą dostępność różnego rodzaju urządzeń elektronicznych
podłączonych do niego. Przeciętny Kowalski nie tylko ma smarphona, ale się
z nim praktycznie nie rozstaje. Ma dostęp do Internetu poprzez sieć 3G,
jak i poprzez coraz liczniejsze hotspoty WiFi. Jako konsument zaznajomiony
z nowoczesną technologią i siecią staje się potencjalnym nabywcą kolejnych
urządzeń i cyfrowych udogodnień. Kosz na śmieci może być inteligentny i wysłać
Ci na smartphona listę produktów, które zużyłeś. Razem z inteligentną lodówką
przygotują Ci listę zakupów, a inteligentny sklep spożywczy podliczy cenę
produktów bez wyjmowania ich z koszyka. Zwykły kosz, czy lodówka to już
za mało. Nastały czasy, w których słusznie lub nie wszystko musi być w sieci,
musi być "inteligentne", "nowoczesne".

Trendy, czy moda cyfrowej rewolucji, tworzy rynek dla nowych produktów
sprzętowych, jak i daje zajęcie dla programistów nie mających wcześniej do
czynienia z takimi projektami. Inteligentna lodówka musi przecież wysyłać
gdzieś w chmurę dane tak, by aplikacja webowa, czy mobilna, mogła zadziałać
swoją magię. W tym cyfrowym wyścigu udział biorą duże firmy, jak i młode
innowacyjne startupy, więc zapotrzebowanie na software, czy protypowanie
produktów sprzętowych, jest spore i chyba na tyle ciekawe, by się tym
zainteresować.


## Miejsce dla programistów Pythona w świecie rzeczy

Produkcyjnie świat rzeczy (ang. IoT - Internet of Things),
czy internetu rzeczy, ma niewiele wspólnego
z Pythonem, czy innymi językami skryptowymi. Niemniej zanim nowy inteligentny
produkt trafi do produkcji, musi być zaprojektowany i w miarę potrzeb
połączony z usługami i aplikacjami w sieci. Potrzebne są prototypy i testy.
Zamiast zatrudniać do tego od razu programistę C/ASM ze znajomością
mikrokontrolerów ATmega, czy STM, można zaprototypować coś szybciej
z wykorzystaniem Pythona, JavaScriptu, Lua, czy także C/C++ na platformach
dla „twórców”. Arduino, czy Raspberry Pi, nie wymagają od nas znajomości
asemblera, czy niuansów mikrokontrolerów. Oferują łatwe w użyciu, dobrze
udokumentowane API i biblioteki, które można wykorzystać do protypowania
elektroniki.

Programista Pythona ma do wyboru kilka platform sprzętowych. MicroPython
dostępny jest na kilku potężnych mikrokontrolerach STM, czy też popularnym i tanim
ESP8266 z WiFi. Podobnie platforma Zerynth, który pozwala programować
w Pythonie, którego kompiluje przed wrzuceniem na mikrokontroler.
Wysokopoziomowe platformy Tinkerforge czy Phidgets także obsługują Pythona,
podobnie jak bardziej wyspecjalizowana własnościowa platforma firmy Synapse.
Jeżeli potrzebujemy większej mocy obliczeniowej, to możemy skorzystać z Raspberry
Pi i bardzo wielu innych "komputerów na płytce", czy nawet klasycznych
komputerów z procesorami x86 Intela i AMD.


## Kiedy i do czego stosować Pythona w projekcie sprzętowym?

Załóżmy na razie, że nasz projekt ma być produkowany w dużych ilościach - że to
nie będzie jedna, dwie sztuki używane lokalnie przez nas.

Platformy Pythonowe, czy ogólnie wszystkie platformy do prototypowania
elektroniki, są dobre, jak sama nazwa wskazuje, do prototypowania elektroniki.
Jest to coś, o czym niektóre projekty na Kickstarterze potrafią zapomnieć. Prototypując
układ mamy możliwość szybkiego sprawdzenia niektórych komponentów oraz całości
jako funkcjonalny produkt. Prototyp umożliwia też prace nad połączeniem go
z zewnętrznym oprogramowaniem. Gdy to mamy za sobą i prototyp działa na stole,
trzeba przejść do dalszych testów - funkcjonalności, jak i pierwszych testów
w warunkach, w jakich będzie pracował końcowy produkt
(np. ujemne temperatury). Dla przykładu podam przypadek pomp infuzyjnych -
medyczne urządzenia dozujące dawki leków dla pacjentów. W zależności
od producenta spotyka się w nich dwie typy klawiatur - numeryczną, gdzie
trzeba wprowadzić poprawną ilość, oraz strzałkową, gdzie trzeba
zwiększać/zmniejszać dawkę leku, aż osiągnie się poprawną wartość. Testy
z udziałem pielęgniarek wykazały, że klawiatury strzałkowe dają mniej
niezauważonych błędów przy wprowadzaniu dawki - pielęgniarka ciągle patrzy się
na wyświetlacz próbując ustawić prawidłową wartość zamiast patrzeć się na
numeryczną klawiaturę.

Gdy mamy dopieszczony prototyp, trzeba wezwać specjalistów od mikrokontrolerów
i elektroniki, którzy takie prototypy przeleją na produkcyjne układy. W tej
fazie redukuje się koszty optymalizując dobór komponentów (dość często
nie potrzeba aż tak rozbudowanych kontrolerów, jak te używane przez np.
MicroPythona), jak i całość przelewa się na płytki PCB. To, co wyjdzie z kilku
pierwszych iteracji, to też będą w pewnym zakresie prototypy - trzeba zmontować
i przetestować, by upewnić się, czy elektronika działa poprawnie (czasami
elementy mogą być źle rozmieszczone i powodować zakłócenia). Jeżeli od razu
zamówimy kilkaset, czy więcej PCB, to zostaniemy z samymi kosztami, bo hardware
nie da się poprawić tak łatwo, jak oprogramowanie. Tworzenie sprzętu to wiele
iteracji - od płytki stykowej po kilka wersji PCB.

Specjalista od mikrokontrolerów przyda nam się także do oprogramowania
docelowego układu. Przy wysokopoziomowych platformach do prototypowania
niektóre kwestie nie są aż takie ważne - zarządzanie energią, usypianie
i wybudzanie mikrokontrolera, efektywność sterowania niektórych komponentów.
Staje się to szczególnie ważne, gdy nasz produkt ma działać na zasilaniu
bateryjnym, jak i przy doborze komponentów (np. inny, tańszy model
wyświetlacza bez biblioteki do Arduino, czy Raspberry Pi). Oszczędność
kilku/kilkunastu lub więcej złotych robi ogromną różnicę, gdy chcemy zlecić
produkcję wielu sztuk naszego urządzenia. Jeszcze większą różnicę robi dobór
części, które są dostępne w wystarczających ilościach.

W przypadku własnych projektów na niską skalę nie trzeba iść aż tak daleko,
ale zawsze warto przejść z surowego prototypu na płytce stykowej na PCB.
Istnieją serwisy, w których możemy zamówić kilka płytek naszego autorstwa.
Mając dwie trwałe płytki - jedna z mikrokontrolerem (Arduino, MicroPython),
a druga z resztą układu znacząco podnosi się trwałość i niezawodność.


## Pythonowe platformy do protypowania elektroniki

Python dostępny jest na kilku platformach, projektach związanych
z elektroniką. Tinkerforge, czy Phidgets są bardziej ukierunkowane
na prototypowanie większych i rozproszonych projektów. Zerynth stara się
oferować także narzędzia produkcyjne, natomiast mikrokontrolery z
MicroPythonem, płytki Raspberry Pi i podobne projekty skupiają się
na "mniejszej" elektronice.

MicroPython to implementacja interpretera Pythona działająca
na mikrokontrolerze. Ma zaimplementowaną część biblioteki standardowej
i nie jest kompatybilna z większością bibliotek do klasycznego Pythona. Zaleta
mikrokontrolera z MicroPythonem jest taka, że wrzucamy do pamięci flash plik
z kodem Pythona i gotowe. Nie trzeba kompilować, a sam język jest bardzo dobry
w projektach edukacyjnych z udziałem dzieci i młodzieży. MicroPython jest
dostępny na oficjalnej płytce deweloperskiej projektu. Można go też wgrać
na ESP8266 i kilka innych mikrokontrolerów, na które został przeportowany.
Firma PyCom oferuje swoje płytki deweloperskie z MicroPythonem
(WiPy, LoPy itd.). Podobnie robi Adafruit ze swoim forkiem pod układy SAM
obecne w produktach tej firmy. Firma ST od niedawna oferuje też produkcyjny
układ SPWF04 (podobny do ESP8266) z MicroPythonem "prosto z pudełka". Płytka
edukacyjna MicroBit także go wykorzystuje. Wybór jest więc dość spory. Do wad
można zaliczyć ograniczoną ilość bibliotek do komponentów, co może utrudnić
prototypowanie.

Zerynth to komercyjna i częściowo otwarta platforma, której celem jest obsługa
projektu sprzętowego od prototypu po produkcję. Pozwala programować w Pythonie
i C, a za pomocą Zerynth VM pozwala generować gotowy firmware na produkcyjne
MCU. Do tego wsparcie dla usług w chmurze, aplikacja mobilna i aktualizacje
OTA. Na chwilę obecną trudno mi określić, na ile projekt ten jest efektywny
w tym, co twierdzi, że robi. Usługa rozwija się, niemniej popularność jest
raczej mała i przynajmniej w przypadku Pythona ograniczeni jesteśmy
dostępnością bibliotek do komponentów. Zaletą na pewno jest IDE i dodatkowe
narzędzia, wadą - vendor lockin.

Jako trzecią platformę możemy potraktować komputery, w szczególności Raspberry
Pi, które łączą komputer z zestawem GPIO i dość dużą ilością bibliotek
dla dodatkowych komponentów. Mając do dyspozycji USB, WiFi, Bluetooth,
Ethernet możemy interfejsować i komunikować się z różnoraką elektroniką
i usługami sieciowymi. USB można też wykorzystać do komunikacji szeregowej
z mikrokontrolerami. Jeżeli musimy wykorzystać sprzęt "wyższego poziomu",
np. kamerę przemysłową, to zapewne będziemy potrzebować MS Windows lub Linuksa
i API producenta dla Pythona (lub API .NET i IronPython, ew. interfejs COM
dla starszego sprzętu). Zostając w temacie kamer przemysłowych - sporo
producentów ostatnio dostarcza wsparcie dla Pythona (np. PointGrey/FLIR).
W przypadku zasilania bateryjnego należy uwzględnić, że nawet oszczędne płytki
z procesorami ARM będą pobierały znacznie więcej prądu niż mikrokontroler,
jak i nie będzie można ich aż tak efektywnie usypiać.

Oddzielną grupę stanowią projekty takie jak Tinkerforge, czy Phidgets.
Projekty te oferują wiele komponetów i płytek kontrolujących. Całość jest
zintegrowana wysokopoziomowym API dostępnym dla licznych języków. W tego typu
projektach skryptując np. silnik krokowy nie musimy implementować wysyłania
serii impulsów, tylko korzystamy z gotowej metody wykonującej określony ruch
silnika. Projekty tego typu nadają się do prototypowania większych
rozproszonych projektów sprzętowych - np. automatyzacji domu. Niekomercyjne
projekty "we własnym zakresie" też będą pasować. Ceny komponentów są wyraźnie
wyższe od masowo dostępnych (chińskich) odpowiedników, ale w cenę wliczona
jest integracja i gotowe API. Elementy montażowe to dodatkowe udogodnienie
przy prototypowaniu. Należy jednak pamiętać że to projekty zamknięte na
siebie - nie oferują zazwyczaj niskopoziomowej integracji z komponentami
spoza projektu (np. komunikacji I2C, SPI).

Czasami Pythonowe platformy mogą okazać się niewystarczające. Pośród
mikrokontrolerów najpopularniejszą platformą do prototypowania jest Arduino
wykorzystujące C. Ilość bibliotek do różnych, nawet mało popularnych
komponentów i duża społeczność sprawiają, że ta platforma może okazać się
jedyną pozwalającą stworzyć prototyp szybko i efektywnie. Dodatkową zaletą
jest szeroki wybór mikrokontrolerów - wiele firm zapewnia wsparcie w IDE
Arduino dla swoich płytek deweloperskich.
