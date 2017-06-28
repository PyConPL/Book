# Python w projektach sprzętowych - Piotr Maliński

## Skąd ta popularność projektów "hardware plus software"?

Nieustający rozwój technologii cyfrowych popularyzuje dostęp do Internetu jak i coraz lepszą dostępność różnego rodzaju urządzeń elektronicznych. Przeciętny Kowalski nie tylko ma smarphona, ale się z nim praktycznie nie rozstaje. Ma dostęp do Internetu poprzez sieć 3G jak i poprzez coraz liczniejsze hotspoty WiFi. Jako konsument zaznajomiony z nowoczesną technologią i siecią staje się potencjalnym nabywcą kolejnych urządzeń i cyfrowych udogodnień. Kosz na śmieci może być inteligenty i wysłać Ci na smartphona listę produktów, które zużyłeś. Razem z inteligentą lodówką przygotują Ci listę zakupów, a inteligenty sklep spożywczy podliczy cenę produktów bez wyjmowania ich z koszyka. Zwykły kosz, czy lodówka to już za mało. Nastały czasy, w których słusznie lub nie wszystko musi być w sieci, musi być "inteligentne", "nowoczesne".

Trendy, czy moda cyfrowej rewolucji tworzy rynek dla nowych produktów sprzętowych jak i daje zajęcie dla programistów nie mających wcześniej do czynienia z takimi projektami. Inteligenta lodówka musi przecież wysyłać gdzieś w chmurę dane tak by aplikacja webowa, czy mobilna mogła zadziałać swoją magię. W tym cyfrowym wyścigu udział biorą duże firmy jak i młode innowacyjne startupy więc zapotrzebowanie na software, czy protypowanie produktów sprzętowych jest spore i chyba na tyle ciekawe by się tym zainteresować.


## Miejsce dla programistów Pythona w świecie rzeczy

Produkcyjnie świat rzeczy, czy internetu rzeczy ma niewiele wspólnego z Pythonem czy innymi językami skryptowymi. Niemniej zanim nowy inteligenty produkt trafi do produkcji musi być zaprojektowany i w miarę potrzeb połączony z usługami i aplikacjami w sieci. Potrzebne są prototypy i testy. Zamiast zatrudniać do tego od razu programistę C/ASM ze znajomością mikrokontrolerów Atmega czy STM można zaprototypować coś szybciej z wykorzystaniem Pytona, JavaScriptu, Lua, czy C/C++ na platformach dla twórców. Aruino czy Raspberry Pi nie wymagają od nas znajomości asemblera, czy niuansów mikrokontrolerów. Oferują łatwe w użyciu, dobrze udokumentowane API i biblioteki, które można wykorzystać do protypowania elektroniki.

Programista Pythona ma do wyboru kilka platform sprzętowych. MicroPython dostępny jest na kilku potężnych mikrokontrolerach STM czy popularnym i tanim ESP8266 z WiFi. Podobnie platforma Zerynth, który pozwala programować w Pythonie, którego kompiluje przed wrzuceniem na mikrokontroler. Wysokopoziomowe platformy Tinkerforge czy Phidgets także obsługują Pythona, podobnie jak bardziej wyspecjalizowana własnościowa platforma firmy Synapse. Jeżeli potrzebujemy większej mocy obliczeniowej możemy skorzystać z Raspberry Pi i bardzo wielu innych "komputerów na płytce", czy nawet klasycznych komputerów z procesorami x86 Intela i AMD.


## Kiedy i do czego stosować Pythona w projekcie sprzętowym?
