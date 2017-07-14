# Inteligentny dom - technologie komunikacji między urządzeniami - Krzysztof Czarnota

System zarządzania inteligentnym budynkiem wymaga sprawowania kontroli nad urządzeniami zainstalowanymi w obiekcie. Sprawna i odporna na błędy komunikacja jest niezbędna w celu realizacji tego zadania. Niestety, różnorodna charakterystyka wykorzystywanych urządzeń utrudnia zastosowanie jednego standardu komunikacji.

Poniżej przedstawiony został przegląd wybranych interfejsów i protokołów komunikacyjnych spotykanych w urządzeniach automatyki budynkowej wraz z krótkim opisem podstawowych cech i zastosowań danego rozwiązania.

## UART
UART (Universal Asynchronous Receiver and Transmitter) to interfejs przeznaczony do nawiązania komunikacji z urządzeniem poprzez port szeregowy. Komunikacja odbywa się przez dwie jednokierunkowe linie TX oraz RX. Dane wysyłane są asynchronicznie w postaci ramek. Ramka danych definiuje długość danych, obecność bitu parzystości oraz ilość bitów stopu. Format ten zapewnia podstawową kontrolę błędów. Nawiązanie komunikacji wymaga używania tego samego formatu ramki i prędkości transmisji przez oba urządzenia. Interfejs typowo obsługuje prędkości transmisji od 110 do 115200 bodów. Maksymalna długość przewodu łączącego urządzenia wynosi nawet 100 m i spada wraz ze wzrostem prędkości transmisji [1, 2].

Jest to jeden z najbardziej podstawowych i najczęściej stosowanych interfejsów ze względu na jego łatwość użycia oraz uniwersalność. W przypadku urządzeń automatyki budynkowej interfejs ten będzie często spotykany w bardziej zaawansowanych sterownikach urządzeń (sterowniki ogrzewania, sterowniki instalacji solarnej, centrale alarmowe).

## SPI
SPI (Serial Peripheral Interface) to bardzo popularny interfejs komunikacji synchronicznej pomiędzy systemami mikroprocesorowymi a układami peryferyjnymi w konfiguracji master-slave. Komunikacja odbywa się z wykorzystaniem trzech linii: MOSI (Master Output Slave Input), MISO (Master Input Slave Output) oraz SCLK (Serial CLocK). Podłączenie jednocześnie wielu urządzeń jest możliwe dzięki dodatkowej linii SS (Slave Select). Magistrala ta umożliwia połączenie urządzeń na niewielkie odległości. Typowo są to urządzenia mieszczące się na jednej płytce drukowanej. Sam interfejs SPI definiuje tylko sygnały niezbędne do jego realizacji, nic nie mówiąc o formacie wymienianych danych, który zależy od urządzenia peryferyjnego. Prędkość transmisji zależna jest od częstotliwości sygnału SCLK, która może wynosić nawet kilka MHz [1, 3].

Komunikacja za pomocą interfejsu SPI najczęściej spotykana jest w urządzeniach peryferyjnych stosowanych w systemach wbudowanych, takich jak: karty SD, pamięci EEPROM, przetworniki ADC/DAC, czy też wyświetlacze ciekłokrystaliczne.

## I2C
I2C (Inter-Integrated Circuit) to dwukierunkowa magistrala służąca do synchronicznego przesyłania danych w urządzeniach elektronicznych. Komunikacja odbywa się z wykorzystaniem dwóch dwukierunkowych linii SDA – (Serial Data Line) oraz SCL (Serial Clock Line). Ze względu na swoją budowę interfejs ten nadaje się do komunikacji na małe odległości (do kilkunastu cm). Każde urządzenie I2C ma swój unikalny 7-bitowy adres. Pierwsze 4 bity określają identyfikator urządzenia. Jest on nadawany przez producenta układu i umożliwia zorientowanie się co do typu urządzenia (pamięć, przetwornik I2C, zegar). Pozostałe 3 bity to fizyczny adres urządzenia. Najmłodszy bit adresu służy do wyboru typu następnej operacji (odczyt lub zapis). Prędkość komunikacji może odbywać się w dwóch trybach: standardowym (100 kHz) i szybkim (400 kHz) [1, 3].

Interfejs I2C znajduje zastosowanie w układach peryferyjnych, gdy prostota i niski koszt są ważniejsze od wysokich prędkości transmisji. Magistralę I2C znajdziemy w układach takich jak: termometry, czujniki ciśnienia, mierniki przyśpieszenia czy też zegary czasu rzeczywistego.

## 1-Wire
1-Wire to interfejs stworzony do łączenia urządzeń na duże odległości (nawet do kilkuset metrów), przy czym transmisja odbywa się stosunkowo wolno. Interfejs do komunikacji wykorzystuje tylko jedną dwukierunkową linię danych. Urządzenia slave podłączone do tego interfejsu mogą posiadać własne zasilanie lub mogą być zasilane bezpośrednio z linii danych, wykorzystując zasilanie pasożytnicze. Interfejs zakłada istnienie na magistrali tylko jednego urządzenia master i dowolnej liczby urządzeń slave. Urządzenia slave identyfikowane są przy pomocy unikalnego 8-bajtowego identyfikatora, nadawanego urządzeniu w czasie produkcji. Urządzenia slave same nie wykazują żadnej aktywności, a wszelkie transfery na magistrali inicjowane są przez urządzenie master. Typowa prędkość komunikacji to 16 kbps [1, 3].

Interfejs 1-Wire jest typowo wykorzystywany do komunikacji pomiędzy niewielkimi i niedrogimi urządzeniami, takimi jak: termometry cyfrowe, czujniki meteorologiczne czy zamki elektroniczne (iButton).

## Modbus
Modbus jest prostym i niezawodnym protokołem zapewniającym komunikację między wieloma urządzeniami w architekturze master-slave. Jest to obecnie standard otwarty, który znalazł szerokie zastosowanie systemach automatyki, zarówno przemysłowej jak i domowej. Komunikacja odbywa się przeważnie przez interfejs szeregowy (RS232, RS485, UART), ale istnieje również wariant protokołu nazwany Modbus TCP, który zapewnia komunikację przez sieć TCP/IP. Komunikacja może odbywać się w dwóch trybach: znakowym (ASCII) oraz binarnym (RTU). Urządzenie zdalne widziane jest jako 16-bitowe rejestry. Protokół definiuje funkcje odpowiedzialne za odczyt i zapis danych na urządzeniu. Zapewnia także diagnostykę, potwierdzenie wykonania rozkazów oraz sygnalizację błędów [4].

Protokół Modbus jest standardem komunikacyjnym wspieranym przez cały szereg producentów sterowników i innych urządzeń wykorzystywanych nie tylko w automatyce. Komunikację za pomocą tego protokołu możemy nawiązać z urządzeniami takimi jak: sterowniki pieca, pompy ciepła, centrale wentylacyjne czy sterowniki solarne.

## KNX
KNX (Standard KONNEX) to standard komunikacji dla automatyki budynkowej, który umożliwia wspólną komunikację pomiędzy wszystkimi odbiornikami energii elektrycznej w budynku. KNX jest systemem rozproszonym. Każdy element podłączony do instalacji wyposażony jest w procesor i elementy niezbędne do jego samodzielnej pracy [5].

System KNX opcjonalnie zapewnia zdalny dostęp do wszystkich instalacji w budynku. Bardzo często stosowany jest w hotelach do sterowania oświetleniem, ogrzewaniem, wentylacją i innymi urządzeniami znajdującymi się w budynku.

## LonTalk
LonTalk (Local Operating Network) to protokół wykorzystywany do komunikacji węzłów w rozproszonym systemie automatyki LonWorks. System LonWorks składa się niezależnych urządzeń zwanych węzłami, które posiadają zdolność komunikowania się ze sobą po wspólnym medium. Protokół LonTalk jest standardem otwartym i można zaimplementować go w dowolnym urządzeniu. Pojedyncze węzły posiadają własną inteligencję i mogą przetwarzać różne programy niemal niezależnie od siebie, jednak wszystkie udostępniają informacje urządzeniom z innych obszarów. Wymiana danych jest sterowana zdarzeniowo [6].

Ze względu na swoją złożoność LonWorks nadaje się do realizacji wielu zadań z zakresu automatyki budynkowej, takich jak na przykład kontrola dostępu, układy HVAC, sygnalizacja przeciwpożarowa, sterowanie oświetleniem i pracą wind.

## M-Bus
M-Bus (Meter-Bus) jest europejskim standardem opracowanym do przesyłania wskazań z przyrządów pomiarowych. Standard zapewnia obsługę kilkuset urządzeń podłączonych do magistrali o długości wynoszącej nawet kilka kilometrów. Transmisja danych jest odporna na błędy, ale stosunkowo wolna. Prędkość przesyłania danych waha się w granicach od 300 do 9600 bodów. Protokół zakłada niezbyt częste odczytywanie mierzonych wartości [7].

Zgodnie ze swoim przeznaczeniem protokół M-Bus stosowany jest w różnych miernikach znajdujących się w instalacjach domowych, takich jak: liczniki energii elektrycznej, gazomierze i ciepłomierze.

## Z-Wave
Z-Wave to bezprzewodowy protokół umożliwiający stworzenie zdalnie sterowanej sieci urządzeń w topologii mesh. Twórcą oraz właścicielem technologii jest duńska firma Zensys. Wykorzystanie protokołu wymaga przynależności do stowarzyszenia Z-Wave Alliance. Technologia wykorzystuje różne częstotliwości w zależności od regionu świata i pracuje w paśmie od 865 do 956 Mhz. Każde urządzenie (z wyjątkiem urządzeń zasilanych bateryjnie) podłączone do sieci jest również przekaźnikiem sygnału dla innych urządzeń, co znacznie zwiększa zasięg sieci. Przed nawiązaniem komunikacji nowe urządzenie musi zostać dołączone do sieci przez proces parowania z głównym kontrolerem. Każda sieć Z-Wave posiada swój 4-bajtowy identyfikator, który zapisywany jest w urządzeniach podczas parowania. Pojedyncze urządzenia identyfikowane są poprzez 1-bajtowy identyfikator, który musi być unikalny w danej sieci. Protokół został zaprojektowany tak, aby zapewniać niezawodną transmisję małych pakietów danych z niskimi opóźnieniami. Przepustowość wynosi 40 kb/s w układach serii 200 lub 200 kb/s w układach serii 400.

Protokół Z-Wave jest stosowany w szerokiej gamie urządzeń przeznaczonych dla inteligentnych budynków takich jak: włączniki ścienne, żarówki, termostaty, rolety, siłowniki okien czy sterowniki centralnego ogrzewania.

## ZigBee
ZigBee to protokół bezprzewodowej transmisji danych w sieciach typu mesh działających w paśmie 868 MHz, 915 MHz lub 2,4 GHz. Charakteryzuje się niewielkim poborem energii oraz niską prędkością transmisji.
Wyróżniamy trzy typy urządzeń ZigBee:
* koordynator (ZC) - jest to węzeł początkowy sieci, do którego przyłączają się inne urządzenia, w sieci może występować tylko jedno takie urządzenie,
* router (ZR) - przekazuje dane z innych urządzeń lub routerów,
* urządzenie końcowe (ZED) - przesyła dane do routera, do którego jest przyłączone [9].

Standard ZigBee wykorzystywany jest w urządzeniach, które wysyłają mało danych oraz wymagają długiego czasu pracy na zasilaniu bateryjnym. Typowe zastosowanie znajduje on w różnego rodzaju czujnikach (dymu, zalania, otwarcia okien) i inteligentnych przełącznikach (świtała, rolet).

## Wifi
Wifi to standard przeznaczony do budowy bezprzewodowych sieci komputerowych. Urządzenia pracują w paśmie częstotliwości 2,4 GHz lub 5 GHz. Powszechność urządzeń wykorzystujących standard wifi spowodowała, że technologia ta została wykorzystana także w urządzeniach automatyki budynkowej.

Ze względu na spore zapotrzebowanie na energię wsparcie dla komunikacji wifi oferowane jest przeważnie w urządzeniach na stałe podłączonych do zasilania, takich jak inteligentne żarówki czy sterowniki centralnego ogrzewania. Technologia ta jest także często wykorzystywana w projektach hobbystycznych za sprawą taniego i łatwo dostępnego modułu wifi ESP8266.

## Podsumowanie
Przedstawione powyżej technologie stanowią tylko część rozwiązań stosowanych w urządzeniach automatyki domowej. Rynek inteligentnych domów oraz internetu rzeczy rozwija się bardzo dynamicznie, co powoduje powstawanie coraz to nowych standardów. Producenci systemów oraz urządzeń preferują własne rozwiązania, starając się zagarnąć jak największą część rynku dla siebie. Powyższe czynniki oraz różnorodność wymagań nie sprzyjają pojawieniu się spójnego standardu komunikacji urządzeń automatyki domowej. Niemniej opisane rozwiązania posiadają już bardzo silną pozycję na rynku, a ich znajomość na pewno ułatwi odnalezienie się w gąszczu wykorzystywanych interfejsów i protokołów komunikacyjnych.

## Bibliografia
1. Tomasz Francuz - Język C dla mikrokontrolerów AVR. Od podstaw do zaawansowanych aplikacji: http://helion.pl/ksiazki/jezyk-c-dla-mikrokontrolerow-avr-od-podstaw-do-zaawansowanych-aplikacji-tomasz-francuz,jcmikr.htm
2. Interfejs UART: https://en.wikipedia.org/wiki/Universal_asynchronous_receiver/transmitter
3. Magistrale szeregowe: http://www.epanorama.net/links/serialbus.html
4. Protokoł Modbus: http://www.modbus.org
5. System KNX: https://www.knx.org/
6. System LonWorks: https://en.wikipedia.org/wiki/LonWorks
7. Magistrala M-Bus: http://www.m-bus.com
8. Protokół Z-wave: http://www.z-wave.com
9. Protokół ZigBee: http://www.zigbee.org
