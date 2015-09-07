# Kosmiczny Python

## Krótko o astronomii

Od wieków człowiek spoglądał w niebo i próbował dowiedzieć się czegoś
na temat tajemniczych świateł na nocnym niebie. Prehistoryczne
artefakty służące do obserwacji nieba znajdujemy na całym świecie. Dzięki
tym odkryciom możemy śmiało powiedzieć, że astronomia jest jedną z
najstarszych dziedzin nauki. Przez wieki jedynym sposobem badania
wszechświata było spoglądanie w niebo każdej nocy gołym okiem. Milowym krokiem
w badaniach kosmosu okazał się wynalazek Galileusza.

Teleskop ze szklanymi soczewkami umożliwił siegnąć głębiej wzrokiem w
nieboskłon. Mogliśmy odkryć jowiszowe księżyce oraz kolejne planety w
układzie słonecznym. Następnym krokiem w badaniu wszechświata okazało się
wynalezienie fotografii, dzięki której można było zaobserwoać wiele asteroid
poruszających się w układzie słonecznym. Najnowsza astronomia nie
może się obejść bez komputerów, a co za tym idzie również bez programowania.
Najczęściej używanym językiem programowania w astronomii jest Fortran, który
został stworzony do obliczeń numerycznych. Jego największą zaletą jest
szybkość oraz szeroki zasób dodatkowych bibliotek.

Kolejnym równie często używanym językiem programowania jest C/C++. Jako język
strukturalny, podobnie jak Fortran, jest bardzo szybki. Większość
oprogramowania wykorzystywanego obecnie w astronomii jest napisane w jednym lub
obu tych językach. Astronomowie korzystają również z programów do obliczeń
numerycznych takich jak Mathematica czy MatLab.

## Python w Astronomii

Mimo dominującej roli Fortrana i C w Astronomii coraz więcej osób korzysta do
obliczeń Pythona. Mimo, iż jest to język interpretowany, a więc dużo wolniejszy
od wcześniej wspomnianych, ma bardzo wielką zaletę, jest bardzo prosty do nauki.
Astronomowie nie mają w swoim programie nauczania wystarczającej ilości godzin
na naukę programowania, stąd Python, ze względu na swoją składnię oraz bardzo
bogatą dokumentację, jest bardzo przyjazny początkującym i zdobywa coraz więcej
zwolenników. Moduł matplotlib przypadł do gustów naukowcom i służy jako główne
narzędzie do wykreślania danych. Kolejnym atutem przemawiającym za Pythonem
jest możliwość zintegrowania z już istniejącym kodem napisanym w C/C++ lub
Fortranie.

### AstroPy

W astronomii najważniejsze są obserwacje, to dzięki nim weryfikowane są
teorie które rodzą się w umysłach fizyków i astronomów. Obserwacje polegają
głównie na detekcji fal elektromagnetycznych w całym zakresie.
Badanie światła widzialnego, które do nas dociera, odbywa się z wykorzystaniem
kamer CCD (Charge-Coupled Device). Każda kamera (również kamery CCD) ze względu
na swoją budowe emituje róznego rodzaje szumy. Aby uzyskać wartościowe zdjęcie,
które może posłużyć do badań, musimy pozbyć się tych szumów. Takie
zdjęcie/ramkeę należy jeszcze skalibrować, czyli usunąć szum termiczny (DARK),
który pojawia się podczas wykonywania zdjęcia, oraz podczas szczytywania (BIAS).
Ostatnim elementem potrzebnym do kalibracji jest FLATFIELD, czyli
zarejestrowana czułość pikseli, która jest normowana do 1 (najaśniejszy piksel).
Podsumowywując, każde zdjęcie ma 'zanieczyszczenia' które muszą zostać
usunięte, aby uzyskać wartościowe zdjęcie do dalszej analizy.
Cały proces nie jest łatwy, gdyż ramek BIAS czy FLATFIELD robi się od kilku
do kilkunastu sztuk podczas obserwacji. Pierwsze ramki są uśredniane, a drugie
sumowane, a następnie ramki są odejmowane od orginalnego zdjecia. Każde zdjęcie
ma od kilku do kilkunastu megapikseli, więc wykonanie takich redukcji ręcznie
jest niemożliwe.

Z pomocą przychodzą komputery oraz programy zewnętrzne, takie jak Gaia czy
Iraf. Wyczyszczone zdjęcia ze 'śmieci' zapisywane są w specjalnym formacie
FITS (Flexible Image Transport System). AstroPy umożliwia odczytywanie tych
plików oraz wykorzystanie do dalszej pracy.

Wykonane zdjęcie jest katalogowane, a współrzędne obiektów są zapisywane do
specjalnych katalogów. Do opisania pozycji gwiazd i planet na niebie nie
wystarczy znany wszystkim układ kartezjański, potrzeba układu współrzędnych
wzbogaconych o pomiar czasu. Układy opisane poniżej to najczęściej używane w
astronomii układy sferyczne, aby podać współrzędne obiektu najpierw taki układ
musi być dobrze zdefiniowany. Każdy z układów posiada określone koło wielkie
oraz punkt na tym kole od którego zaczynamy liczyć daną współrzędną. Drugą
wartość otrzymamy przez dodanie płaszczyzny prostopadłej do koła wielkiego.
Druga płaszczyzna wyznacza na sferze dwa bieguny, a południk początkowy to ten,
który przecina punkt początkowy.

Najczęściej stosowane układy odniesienia to horyzontalny, godzinowy,
równonocny, ekliptyczny oraz galaktyczny. Podstawowym układem jest układ
horyzontalny, tutaj kołem wielkim jest płaszczyzna horyzontu. Biegunami w tym
układzie będzie zenit i nadir. Współrzędnymi układu współrzędnych horyzontalnych
to Azymut astronomiczny \bf{A}, mierzony w stopniach
($0^{\circ}$-$360^{\circ}$) oraz  wysokość \b{h} podawana w zakresie
[$-90^{\circ}$-$90^{\circ}$].

Kolejny układ współrzędnych wykorzystywany w astronomii nazywa się
godzinowy. Współrzędne to kąt godzinny \b{t} mierzony w godzinach
($0^{h}$-$24^{h}$). Deklinacja $\delta$ to druga współrzędna podawana jest w stopniach
w zakresie [$-90^{\circ}$-$90^{\circ}$]. Są one zdefiniowane dzięki kołu wielkiemu
przechodzącemu przez równik niebieski. Bieguny tego układu będą się pokrywać z
osią obrotu ziemi.

Układ współrzędnych równikowych równonocnych jest zdefiniowany jak godzinowy z
tą różnicą, że punktem początkowym jest punkt barana, a współrzędne to
deklinacja $\delta$ [$-90^{\circ}$-$90^{\circ}$] oraz rektascencja
$\alpha$ mierzona jako kąt godzinny w przedziale 0^{h}, 24^{h}.

Koło wielkie, po którym pozornie porusza się Słońce to ekliptyka, i jest on
podstawowym kołem w układzie ekliptycznym. Długość ekliptyczna $\lambda$
oraz szerokość ekliptyczna $\Beta$ są liczone w stopniach
(0^{\circ}, 360^{\circ}).

Ostatnim układem będzie galaktyczny, jak łatwo się domyślić podstawową
płaszczyzną będzie płaszczyzna galaktyki. I podobnie jak w ekliptycznym układzie
mamy tutaj długość i szerokość galaktyczną [$-90^{\circ}$-$90^{\circ}$].

Wszystkie układy mają swoje mocne i słabe strony, jeden jest zależny od ruchu
obrotowego Ziemi, inny od Słońca. Ponadto instrumenty obserwacyjne są również
tak wykonywane, aby śledziły obiekty w jednym z powyższych układów. Stąd
współrzędne obiektów astronomicznych są zapisywane w różnych systemach, dlatego
też trzeba współrzędne przetransformować do innego układu, który
będzie bardziej przydatny na danym instrumencie. Takie transformacje są również
dostępne w module AstroPy.

### MatPlotLib

Jest to moduł do rysowania wykresów, które tak często pojwaiają się w
publikacjach. Biblioteka umożliwia rysowanie bardzo prostych w $2D$ lini,
diagramów, aż po bardziej skomplikowane histogramy i kontury. Dołaczona jest również
biblioteka do wykresów $3D$, dzięki której wykreślimy atraktory, powierzchnie i
wiele innych. Jednocześnie mamy wpływ na wszystkie elementy wykresów od opisów,
przez osie, wielkość podziałki na osiach. Możemy wprowadzać wzory matematyczne,
manipulować czcionką, wykreślać kilka a nawet kilkanaście wykresów. Na jednym
obrazku możemy łączyć wykresy gęstości $2D$ z histogramami $1D$. Matplotlib daje
nam naprawde bardzo dużo swobody w tworzeniu różnorakich wykresów.

### AUTO

Bifurykacja (rozdwojenie) jest to zjawisko skokowej zmiany własności modelu
matematycznego, przy drobnej nawet zmianie parametrów. W mechanice nieba jednej
z dziedzin astronomi bifurykacja następuje wtedy, gdy zmienia się liczba
rozwiązań równania różniczkowego, podczas zmian parametru równania. Rozdwojenie
przedstawione na wykresie pozwala na wykrycie zachowań okresowych od
chaotycznych. Dla takich przypadków zostało stworzone oprogramowanie o nazwie
AUTO. AUTO jesto hybrydą Fortrana i Pythona, która jest wstanie wyznaczać punkty
bifurykacji, wyznaczać stabilne i niestabilne rodziny periodycznych rozwiązań
zwyczajnych równań róźniczkowych.

Model Matematyczny oraz równania różniczkowe
zapisujemy w Pythonie, również wszelkie ustawienia dotyczące sposobu obliczeń
znajdują się w postaci listy. Obliczenia wykonywane są natomiast we
Fortranie na podstawie danych zapisanych wcześniej.

## Zakończenie

Niniejszy tekst niech posłuży jako słowniczek, odnośnik który ma za zadanie
w najprostszy sposób wyjaśniać poszczególne zagadnienia o których będzie mowa
podczas prezentacji. Mam nadzieje, że po przeczytaniu, słuchacz będzie miał
większą świadomość o czym jest prezentacja.

## Bibiografia

[1] Astronomia - https://pl.wikipedia.org/wiki/Astronomia
[2] Układy współrzędnych w astronomii - http://www.astro.amu.edu.pl/~jopek/JopekTJ/Dydaktyka/A_Sf/2014-15/Prezentacje/wyklad_03.pdf
[3] Astropy - http://docs.astropy.org/
[4] Matplotlib - http://matplotlib.org/
[5] Bifurikacja - http://zasoby1.open.agh.edu.pl/dydaktyka/matematyka/c_fraktale_i_chaos/chaos.php?rozdzial=2
[6] AUTO - http://cmvl.cs.concordia.ca/auto/
[7] Notatki z wykładów astronomicznych.
