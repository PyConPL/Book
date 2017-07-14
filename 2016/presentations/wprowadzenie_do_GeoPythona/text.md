# Krótkie wprowadzenie do GeoPythona – Małgorzata Papież

Od kilku lat, w Polsce coraz większą popularność zdobywają aplikacje oparte na wykorzystaniu *danych przestrzennych*.
To dzięki nim przestaliśmy być zależni od papierowych map i bez wychodzenia z domu możemy zobaczyć każdy zakątek Ziemi.
Co jeśli dostępne aplikacje takie jak Google Earth, Google Maps nam nie wystarczają i chcemy czegoś więcej?
Zobaczmy więc, jak wykorzystując Pythona możemy zaprojektować aplikacje
pozwalające nam na tworzenie własnych map czy przeglądanie najnowszych zdjęć satelitarnych.

## Dane przestrzenne
Rozwój technologii komputerowych w ostatnich latach sprawił, że przetwarzanie
bardzo dużej ilości danych w czasie rzeczywistym stało się możliwe.
Przyspieszenie procesów analizy dużych zbiorów danych przyczyniło się wzrostu
zainteresowania danymi przestrzennymi. Dane przestrzenne przechowują
informacje o obiekcie świata rzeczywistego biorąc pod uwagę jego położenie
przestrzenne. Oprócz informacji przestrzennej podanej w postaci szerokości
i długości geograficznej mogą zawierać również inne istotne informacje takie
jak data utworzenia, związki przestrzenne obiektów ze sobą tzw. topologię czy
właściwości danego obiektu czyli jego atrybuty. Dane przestrzenne dzieli się
na wektorowe i rastrowe. Pierwsze z nich reprezentowane są przez obiekty
geometryczne takie jak punkty, linie, powierzchnie, których kształt
i położenie definiowany jest przez współrzędne. Taki sposób reprezentacji
używany jest z racji swojej dużej dokładności, możliwości wyodrębniania
poszczególnych obiektów oraz małej pojemności plików. Do obiektów wektorowych
w rzeczywistości należą granice działek, ulice, budynki, sieci: elektryczne,
gazowe, wodne, telefoniczne itd. W modelu rastrowym dane są przechowywane
w postaci pojedynczych pikseli, w regularnej siatce pikseli. Dzięki temu
znacznie wydajniej radzi sobie z analizą i modelowaniem zjawisk zachodzących
w przestrzeni np. stanu zanieczyszczenia, opadów atmosferycznych. Niestety
wymaga dużo pamięci RAM oraz powoduje utratę części informacji.
Źródła danych przestrzennych:

* mapy i plany,
* digitalizacja i wektoryzacja papierowych map,
* odbiorniki GPS,
* zdjęcia satelitarne i lotnicze,
* pomiary geodezyjne, stacje pomiarowe i wywiady terenowe.


## Python i dane przestrzenne
Znaczna część aplikacji korzystająca z danych przestrzennych napisana została
w języku Python. Taki wybór podyktowany został możliwościami jakie daje ten
język programowania. Po pierwsze pozwala korzystać za darmo praktycznie
ze wszystkich bibliotek związanych z danymi przestrzennymi, w szczególności
z *GDAL/OGR*. Dodatkowo ułatwia pracę na danych rastrowych dzięki bibliotece
*numpy*. Graficzna biblioteka *PyQt* pozwala budować interfejsy graficzne,
które mogą być dołączane jako nakładki do istniejących już aplikacji
przestrzennych i przenoszone między systemami operacyjnymi bez potrzeby
modyfikacji ich kodu.

## GDAL/OGR
GDAL (*Geospatial Data Abstraction Library*) jest biblioteką rozwijaną przez
fundację *OSGEO* jako wolne oprogramowanie, służącą do operacji na danych
rastrowych. Zawiera w sobie również bibliotekę OGR (*Simple Features Library*)
do danych wektorowych. Obecnie obsługuje około 140 formatów danych rastrowych
oraz 80 wektorowych. Obie biblioteki napisane zostały w języku C++, ale
posiadają bindingi dla innych języków, w tym dla Pythona. Istotną rzeczą jest,
że GDAL jest tak naprawdę zbiorem odrębnych programów tzw. *utility programs*,
które możemy wywołać z linii komend. Wszystkie dostępne operacje znajdują się
na stronie biblioteki GDAL [1].

## Pierwsza aplikacja z użyciem GDAL/OGR

Aby rozpocząć pracę z biblioteką GDAL pierwszym krokiem jaki należy wykonać
jest sprawdzenie czy posiadamy zainstalowaną bibliotekę:

    import sys
    try:
      from osgeo import ogr, gdal
    except ImportError:
      sys.exit('GDAL/OGR is not installed.')

GDAL nie jest dołączany do standardowej biblioteki modułów Pythona. Warto
jednak przed jego instalacją sprawdzić czy nie posiadamy już zainstalowanej
wersji, gdyż GDAL z racji swojej dużej użyteczności i popularności jest często
instalowany razem z innymi programami (Google Earth, QGis, ArcGIS). Tych,
którzy nie posiadają GDAL, odsyłam na stronę [2], na której krok po kroku
wytłumaczone zostało jak zainstalować bibliotekę na różnych systemach.

Zacznijmy od najprostszego przykładu prezentującego w jaki sposób następuje
odczyt danych rastrowych:

    from osgeo import ogr, gdal
    dataset = gdal.Open('test.tif', gdal.GA_ReadOnly)
    if dataset is None:
        print 'File not open!'


Z modułu GDAL należy wywołać metodę `Open` ze ścieżką dostępu jako parametrem
(najlepiej w postaci bezwzględnej). Drugi parametr określa sposób otwarcia
pliku. Domyślnie parametr ten ustawiony jest na odczyt rastra, dlatego
`gdal.GA_ReadOnly` może być pominięte. Mając wczytanego rastra możemy dokonać
sprawdzenia takich wartości jak ilość kanałów `RasterCount`, ilość wierszy
`RasterXSize`, ilość kolumn `RasterYSize`, z których składa się raster.

    dataset = gdal.Open('test.tif')

    bands = dataset.RasterCount
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    print 'Number of bands: ', bands
    print 'X: ', cols
    print 'Y: ', rows

Więcej niż jeden kanał w rastrze oznacza, że dane z tego samego położenia
zostały zarejestrowane w różnych zakresach promieniowania. Możemy również
sprawdzić podstawowe statystyki dotyczące każdego kanału.

    for band in range(bands):
        print 'Band no.: ', band
        srcband = dataset.GetRasterBand(band)
        if srcband:
            stats = srcband.GetStatistics(True, True)
            print 'Min: %.3f'%stats[0]
            print 'Max: %.3f'%stats[1]

Teraz spróbujmy otworzyć plik wektorowy. Przed otwarciem pliku ustawiamy
sterownik `Driver`, który jest obiektem odpowiadającym za poprawne wczytanie
odpowiedniego typu danych. Ważne jest również by przy pierwszym otwarciu pliku
ustawić prawa dla sterownika, w zależności od tego czy chcemy odczytywać czy
zapisywać dane. Domyślnym prawem jest prawo do odczytu oznaczane zerem.
Jedynka oznacza możliwość modyfikacji pliku i jego ponownego zapisu. Nie
wszystkie wspierane przez OGR formaty posiadają opcję zapisu. Metoda Open
zwraca obiekt zwany źródłem danych:

    from osgeo import ogr
    driver = ogr.GetDriverByName('ESRI Shapefile')
    datasource = driver.Open('test.shp', 0)

Źródło danych składa się z warstw, które pobieramy za pomocą funkcji
`GetLayer`. Najbardziej podstawowy format wektorowy Shapefile posiada tylko
jedną warstwę, dlatego użycie indeksu oznaczającego numer warstwy jest
opcjonalne. Przy pozostałych formatach ustawienie indeksu jest obowiązkowe.
W celu sprawdzenia liczby warstw możemy wywołać następującą funkcję:

    numLayer = datasource.GetLayerCount()

Po pobraniu warstwy jesteśmy w stanie odczytać podstawowe informacje
o obiektach w niej zawartych. Możemy sprawdzić z ilu obiektów składa się
warstwa `GetFeatureCount`. Najważniejsze jednak jest to, że możemy pobrać
każdy obiekt po to, by móc odczytać jego geometrię, nazwę, oraz wartości jakie
w sobie przechowuje:

    datasource = driver.Open('test.shp', 0)
    for feat in range(numLayer):
        layer = datasource.GetLayerByIndex(feat)
        print 'Layer name: ', layer.GetName()
        numfeat = layer.GetFeatureCount()
        print 'Number of features:  ', numfeat

Jak widzimy, odczyt danych wektorowych jest bardziej skomplikowany i dobranie
się do struktury danych wymaga przejścia przez kilka poziomów, co przy bardzo
dużej ilości danych powoduje opóźnienia.

## Ale skąd te dane?

W podanych przykładach korzystaliśmy z przykładowych danych rastrowych
i wektorowych. Jest to próbny zestaw danych, który jest ściągany podczas
instalacji aplikacji do danych przestrzennych korzystających z GDAL. Pisanie
własnej aplikacji wymaga od nas jednak rzeczywistych danych dostosowanych do
naszych potrzeb. Oto kilka źródeł z których możemy pobierać bezpłatnie
potrzebne nam dane:

* Centralny Ośrodek Dokumentacji Geodezyjnej i Kartograficznej [3],
* Centralna Baza Danych Geologicznych [4],
* Geoportal 2 [5],
* OpenStreetMap [6],
* USGS [7],
* ESA/Sentinel [8].

## Wizualizacja danych

Odczyt danych i ich analiza to jednak nie wszystko. Aby nasza aplikacja miała
możliwość podglądu danych potrzebujemy biblioteki graficznej. O ile
z wyświetleniem rastrów nie mamy problemów (możemy do ich wyświetlenia użyć
dowolnej graficznej biblioteki Pythona, np. PyQt) o tyle wyświetlenie wektorów
jest bardziej problematyczne. Podobnie jak w przypadku rastrów możemy
skorzystać z gotowych komponentów graficznych wbudowanych w bibliotekę PyQt
np. *QPainter* do rysowania obiektów. Niestety rozwiązanie to ma jedna wadę.
Nie sprawdza się dla wektorów mających powyżej kilku tysięcy wierzchołków. Dla
porównania, wyświetlenie konturu jednego województwa zajmuje ułamki sekund,
wyświetlenie całej mapy Polski z konturami wszsytkich województw zajmuje już
kilkanaście sekund. Z pomocą przychodzą biblioteki dedykowane do wizualizacji
danych wektorowych. Jedną z nich jest *matplotlib* wraz z rozszerzeniem
*Basemap*. Jest on odpowiednikiem znanego z Matlaba narzędzia zwanego Mapping
Toolbox. Jego główną zaletą jest to, że sam dokonuje odwzorowania
kartograficznego czyli transformacji współrzędnych geograficznych
na współrzędne rysunku. Dodatkowo zawiera sporo funkcji ułatwiających
rysowanie danych przestrzennych m.in. rysowanie równoleżników, południków,
rysowanie i wygładzanie granic i wybrzeży. Minusem jest jednak słabo opisana
dokumentacja.

## Pozostałe biblioteki przestrzenne

Wspomniane *GDAL/OGR* nie jest jedyną biblioteką wspomagającą przetwarzanie
danych przestrzennych. Obecnie dostępnych darmowo mamy kilkanaście bibliotek,
szczególnie do manipulacji danymi wektorowymi. Z nich najbardziej znane
to Fiona i Shapely. Obie są typowymi bibliotekami Pythona, które pozwalają
na odczyt danych wektorowych, tworzenie nowych geometrii, sprawdzanie
poprawności geometrii oraz wszelkiego rodzaju operacje geometryczne. Prosty
odczyt danych wektorowych za pomocą biblioteki Fiona:

    import fiona
    data = fiona.open('test.shp')
    print 'Ilość obiektów w warstwie: ', len(data)

    rec = next(data)
    print rec.keys()
    print rec['geometry']['type']
    print rec['properties']

## Podsumowanie

Wybór odpowiedniej biblioteki jest w znacznym stopniu zależny od stopnia
zaawansowania operacji, które będą wykonywane w projektowanej aplikacji.
Pod tym względem niewątpliwie liderem jest GDAL/OGR, który dostarcza najwięcej
gotowych funkcjonalności. Niemniej GDAL/OGR może być problematyczny ze względu
na fakt, że jego struktura oparta jest na C++. Fiona i Shapely opierają się
na standardach Pythona m.in. korzystając z plików, słowników czy iteratorów,
co przyspiesza pracę i zmniejsza prawdopodobieństwo popełnienia błędu.

## Bibliografia

1. Strona GDAL z listą wszystkich operacji: http://www.gdal.org/gdal`_`utilities.html
2. Instalacja GDAL/OGR:\crlf http://www.gis.usu.edu/~chrisg/python/2009/install.html
3. Centralny Ośrodek Dokumentacji Geodezyjnej i Kartograficznej:\crlf
http://www.codgik.gov.pl/index.php/darmowe-dane.html
4. Centralna Baza Danych Geologicznych: http://baza.pgi.gov.pl/
5. Geoportal: http://www.geoportal.gov.pl/web/guest/DOCHK
6. OpenStreetMap: http://download.geofabrik.de/
7. USGS: http://earthexplorer.usgs.gov/
8. ESA/Sentinel: https://scihub.copernicus.eu/dhus/#/home
9. Systemy GIS:\crlf http://wazniak.mimuw.edu.pl/images/9/9a/Systemy`_`mobilne`_`wyklad`_`8.pdf
10. Dane przestrzenne: http://www.igik.edu.pl/pl/a/Dane-przestrzenne-def
11. Wykorzystanie języka Python w GIS: http://gis-support.pl/wykorzystanie-jezyka-programowania-python-w-quantum-gis/
