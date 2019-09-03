# Bluetooth Low Energy z PyBluez

Bluetooth Low Energy (BLE) został wprowadzony jako część specyfikacji Bluetooth 4.0. Technologia ta umożliwia dostęp do zewnętrznych urządzeń praktycznie z każdego systemu mobilnego. Jest to technologia połączenia bezprzewodowego o niskiej przepustowości, bardzo efektywna pod względem poboru mocy i kosztów implementacji. Dzięki wyposażeniu urządzeń mobilnych w układy obsługujące technologię BLE oraz standaryzację komunikacji przez wykorzystanie Generic Attribute Profile (GATT), obserwujemy wysoki poziom adaptacji tej technologii na rynku urządzeń internetu rzeczy (IoT).


## Standard Bluetooth Low Energy
Bluetooth Low Energy został wprowadzony przez Bluetooth Special Interest Group (SIG) w czerwcu 2010 roku wraz z wersją 4.0 specyfikacji Bluetooth. Specyfikacja Bluetooth obejmuje zarówno klasyczny bluetooth (znany standard bezprzewodowy, który jest powszechnie stosowany w urządzeniach konsumenckich od wielu lat), jak i Bluetooth Low Energy (nowy, wysoce zoptymalizowany standard). Te dwa standardy komunikacji bezprzewodowej różnią się właściwie na każdej warstwie i nie są ze sobą bezpośrednio kompatybilne.

## Komunikacja w standardzie BLE
Urządzenie BLE może komunikować się w trybie rozgłoszeniowym lub połączeniowym. Tryb rozgłoszeniowy nie wymaga połączenia i pozwala na jednokierunkowe wysyłanie danych do dowolnego urządzenia skanującego znajdującego się w zasięgu. Jest to jedyna możliwość przesłania danych do więcej niż jednego urządzenia w tym samym czasie. Standardowy pakiet rozgłoszeniowy zawiera 31 bajtów, które opisują urządzenie oraz jego możliwości. Pakiet rozgłoszeniowy może również zawierać dowolne niestandardowe dane. Jeżeli rozgłaszane dane są dłuższe niż 31 bajtów, BLE umożliwia przesłanie drugiego pakietu danych (Scan Response) o tej samej długości, w odpowiedzi na żądanie urządzenia skanującego. Główną wadą komunikacji w trybie rozgłoszeniowym jest brak jakichkolwiek mechanizmów zabezpieczających komunikację [1]. 

W przypadku, gdy wymagana jest transmisja danych o długości większej niż 62 bajty lub komunikacja dwukierunkowa, urządzenia muszą nawiązać połączenie. Połączenie BLE zapewnia trwały tunel transmisyjny pomiędzy dwoma równorzędnymi urządzeniami, co czyni komunikację z natury prywatną. Aby zainicjować połączenie, urządzenie centralne (master) wyszukuje pakiet rozgłoszeniowy urządzenia peryferyjnego (slave) i wysyła żądanie nawiązania połączenia. Należy zauważyć, że role przypisane urządzeniom podczas nawiązywania połączenia nie mają wpływu na późniejszą komunikację i dane mogą być wysyłane niezależnie w obu kierunkach. Połączenia pozwalają na znacznie bardziej złożony model danych, a dzięki temu na lepszą organizację komunikacji, poprzez zastosowanie dodatkowych warstw protokołu, a dokładnie Generic Attribute Profile (GATT) [1].

Podczas nawiązywania połączenia, urządzenie peryferyjne zasugeruje "interwał połączenia" z urządzeniem centralnym. Jest to czas pomiędzy dwoma zdarzeniami transmisji danych (zdarzeniami BLE) w trakcie komunikacji urządzenia centralnego i peryferyjnego. Wartość teoretyczna waha się od 7,5 ms do 4 s (z przyrostem 1,25 ms). Ostateczna wartość tego parametru zdeterminowana jest przez urządzenie nadrzędne, jednak należy wyważyć wymaganą przepustowość oraz zużycie energii.

## Generic Attribute Profile (GATT). 
Generic Attribute Profile definiuje sposób, w jaki dwa urządzenia Bluetooth Low Energy przekazują dane między sobą za pomocą koncepcji zwanych usługami (Services) i cechami (Characteristics). Lista usług wraz z ich cechami składa się na profil GATT urządzenia. GATT wykorzystuje jako warstwę transportową ogólny protokół danych BLE zwany Attribute Protocol (ATT), który jest używany do przechowywania usług, cech oraz powiązanych danych w prostej tabeli z wykorzystaniem identyfikatorów (UUID) [5]. Specyfikacja GATT definiuje również zalecenia dla wszystkich profili opartych na GATT (zaakeceptowane przez Bluetooth SIG), które obejmują precyzyjne przypadki użycia konkretnych profili, usług i cech, a dzięki temu zapewniają interoperacyjność pomiędzy urządzeniami pochodzącymi od różnych producentów. Wszystkie standardowe profile BLE są zatem oparte na GATT i muszą być z nim zgodne, aby działały prawidłowo. To czyni z GATT kluczową sekcję specyfikacji BLE, ponieważ każdy pojedynczy element danych istotny dla zastosowań lub użytkowników musi być sformatowany, opakowany i wysłany zgodnie z jego zasadami [1].

## Transakcje GATT
Urządzenie peryferyjne (GATT Sever) definiuje listę usług w oparciu o wykorzystany profil lub wymagania projektowe. Pełny wykaz oficjalnie przyjętych profili opartych na GATT jest dostępny na Bluetooth Developer Portal [2]. Usługi zdefiniowane przez profil porządkują dane w logiczne jednostki zawierające jedną lub więcej cech. Każda usługa posiada własny UUID, który może być 16 bitowy (w przypadku oficjalnie przyjętej usługi) lub 128 bitowy (dla niestandardowych usług). Lista oficjalnie przyjętych usług wraz z ich identyfikatorami również jest dostępna na Bluetooth Developer Portal [3].
Cecha, to pojedynczy punkt danych, który może w zależności od potrzeb zawierać dane proste lub złożone. Długość danych ograniczona jest do 512 bajtów przez specyfikację. Podobnie jak usługi, cechy posiadają swoje 16 lub 128 bitowe UUID i podobnie jak w poprzednich przypadkach Bluetooth Developer Portal podaje listę oficjalnie przyjętych cech [4]. Każda transakcja jest inicjowana przez urządzenie master (GATT Client), które może zażądać odczytu lub zapisu bufora danych cechy. Dostęp do cech może być ograniczony przez uprawnienia ATT, na które składają się:
- uprawnienia dostępu (none, readable, writable, readable and writable),
- uprawnienia szyfrowania (no encryption required, unauthenticated encryption required, authenticated encryption required),
- uprawnienia autoryzacji (no authorization required, authorization required) [1].

Esencją komunikacji w standardzie BLE jest manipulacja wartości zidentyfikowanych dzięki cechom zdefinowanym przez profil Generic Attribute Profile urządzenia. Wymiana danych z urządzeniami tego samego typu jest ustandaryzowana dzięki wykorzystaniu profili GATT zaakceptowanych przez SIG, co pozwala na nawiązanie komunikacji z urządzeniem do którego nie posiadmy specyfikacji i daje szerokie pole do eksploracji urządzeń BLE.


## Bibliografia
1. Robert Davidson, Akiba, Carles Cufí, Kevin Townsend - Getting Started with Bluetooth Low Energy. https://www.oreilly.com/library/view/getting-started-with/9781491900550/
2. https://www.bluetooth.com/specifications/gatt/
3. https://www.bluetooth.com/specifications/gatt/services/
4. https://www.bluetooth.com/specifications/gatt/characteristics/
5. https://learn.adafruit.com/introduction-to-bluetooth-low-energy/gatt
