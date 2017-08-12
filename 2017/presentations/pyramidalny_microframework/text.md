# Pyramid(alny) mikroframework - Marcin Bardź

# Wstęp

Pyramid jest frameworkiem webowym rozwijanym przez inicjatywę społecznościową
Pylons Project, która za cel postawiła sobie tworzenie pythonowych technologii
webowych spełniających najwyższe standardy, takie jak 100% pokrycia w
dokumentacji i w testach, czy też wsparcie dla Pythona 2.x i 3.x. Autorzy
przyznają, że podczas tworzenia Pyramida mocno inspirowali się Zope, Pylons i
Django, a ja bym do tej listy dodał jeszcze Ruby on Rails, którym inspirowały
się wszystkie powyższe frameworki.

Teraz może wytłumaczę się z tego niedorzecznego tytułu - otóż jest to
najbardziej zwarta charakterystyka frameworka Pyramid, jaką udało mi się
wymyślić. Piramidalny to - za słownikiem PWN - "olbrzymi, kolosalny, zwykle o
pomyłce, głupstwie itp." i takie właśnie było moje wrażenie, gdy zobaczyłem
(nomen omen) Pyramid po raz pierwszy. Jest to niesamowicie rozbudowane
narzędzie, nie będące jednocześnie full-stackowym frameworkiem.

Pyramid nie jest może najpopularniejszy, ale zawsze pojawia się w
zestawieniach web frameworków i zyskał sobie uznanie starych wiarusów spod
znaku ZOPE i Plone.

Niniejszy artykuł nie jest wprowadzeniem do Pyramida - uważam, że nie ma
potrzeby powielać oficjalnego (skądinąd całkiem dobrego) tutoriala (link
w źródłach). Zamiast tego wybrałem i opisałem kilka interesujących, moim
zdaniem, cech frameworka, które wyróżniają go spośród tłumu konkurentów.

Ponadto, choć jestem wyznawcą zasady, że jedna linijka kodu znaczy więcej niż
0xFF słów, zabrakło niestety miejsca na przykłady. Dlatego moim celem będzie
zaintrygowanie czytelnika na tyle, by sam sięgnął do materiałów.

# Przytłaczający

Pierwsze spojrzenie na Pyramida może przerazić nieprzygotowanego pythonowca:
większa część "hello world" przypomina magiczne zaklęcia, a dokumentacja jest
tak obszerna, że przeczytanie samego spisu treści zajmuje parę minut. Nie mówiąc
już o tutorialu, który składa się z, bagatela, 10 rozdziałów i 52
podrozdziałów! Do tego dochodzi instalacja, która pobiera chyba połowę PyPI,
a samo spojrzenie na submoduły wywołuje zawrót głowy.

Nie jest to zachęcające pierwsze spojrzenie i z tego powodu dla wielu może być
spojrzeniem ostatnim. Przyjrzyjmy się zatem, czy rzeczywiście jest aż tak źle.

## Rozmiar

Podstawowy Pyramid zawiera aż 32 moduły, jednakże nie ma się czego bać,
gdyż całość podzielona jest na logiczne obszary, z których jedne są większe,
a inne całkiem małe (na przykład moduł `pyramid.decorator` zawiera
tylko jedną funkcję `reify()`). Taki podział bardzo ułatwia
poszukiwania i pogłębianie wiedzy, wszystko związane z danym tematem zebrane
jest w jednym miejscu.

## Dokumentacja

Jak już wspomniałem wcześniej, obszerność dokumentacji może onieśmielać -
twórcy Pyramida dbają o to, by dokumentacja była zawsze kompletna, co
przy rozmiarze frameworka przekłada się na niemały kawałek literatury.

Na szczęście w materiałach łatwo znaleźć to, czego się szuka - każdy z
czterdziestu (sic!) rozdziałów skupia się na jednym tylko zagadnieniu, dzięki
czemu nie trzeba skakać po wielu miejscach, żeby zorientować się w konkretnym
temacie.

## Dodatki (*add-ons*)

Poza podstawowym frameworkiem mamy jeszcze całą rodzinkę dodatków,
zarówno tworzonych i utrzymywanych w ramach Pylons Project (około 100 sztuk),
jak i niezależnych. Daje to sumę około 350 pakietów w PyPI.

Dodatki są bardzo zróżnicowane, od prostych typu `paginate`, przez rozszerzenia
funkcjonalności jak `pyramid_jinja2` czy `pyramid_ldap`, a na wielkich
aplikacjach (CMS, platforma dla mikroserwisów itp.) kończąc.

## Ciągły i nieubłagany rozwój

Od momentu powstania Pyramid rozwija się w stałym, szybkim tempie - kolejna
wersja pojawia się około dwóch razy w roku, przynosząc nowe funkcjonalności
i usprawnienia. Autorzy nie boją się dokonywać poważnych zmian, jeśli są
to zmiany na lepsze, co czasem może skutkować tym, że nasz projekt po
aktualizacji nagle staje się przestarzały, a w dłuższej perspektywie przestaje
działać z nowo wydaną wersją Pyramida.

Ponadto twórcy Pyramida nie poddają się zjawisku *not-invented-here*, czyli
uporczywej implementacji wszystkiego od zera tylko po to, aby pozbyć się
zależności od "obcych" bibliotek. Na przykład jedną z ciekawszych zmian
między Pyramidem 1.7 a 1.8 była rezygnacja z rozwijanego przez długi czas
mechanizmu *scaffoldów* (szablonów automatyzujących np. tworzenie nowego
projektu) na rzecz popularnej biblioteki zewnętrznej `cookiecutter`. Pociągało
to za sobą poważne zmiany zarówno w kodzie, jak i w dokumentacji oraz testach
(pamiętamy - 100% pokrycia). Jednakże praca została wykonana, a bilans zysków
i strat był na pewno dodatni.

## Zależności

Pomimo licznych zewnętrznych bibliotek wymaganych do funkcjonowania
(dla wersji 1.9 naliczyłem ich 11 plus drugie tyle, żeby odpalić "Hello World!")
Pyramid działa stabilnie i nie widać
zgrzytów między modułami. Wynika to po części z tego, że większość zależności
należy do Pylons Project, zaś niektóre moduły zewnętrzne były pierwotnie
częścią Pyramida i zostały "oderwane" od frameworka po to, by umożliwić ich
niezależne wykorzystanie (twórcy stawiają na otwartość).

Najbardziej integralną zależnością Pyramida jest `WebOb` - biblioteka
opakowująca żądania HTTP w środowisku WSGI, używana w wielu innych projektach
(jak choćby TurboGears, czy Google App Engine) i będąca częścią Pylons Project.

# Totalna swoboda

Pyramid bardzo mało narzuca programiście, dając mu swobodę wyboru, z którą
wielu nie wie co zrobić. Z jednej strony mamy nieskrępowaną wolność kodowania,
która pozwala rozwinąć skrzydła programiście, a także umożliwia pracę
z ulubionymi bibliotekami. Z drugiej jednak strony programista może poczuć
się zawieszony w próżni, nie wiedząc w jaki sposób zaimplementować daną
funkcjonalność.

## Struktura projektu

Pyramid nie zakłada jedynej słusznej struktury projektu - dopuszczalne są
zarówno aplikacje jednoplikowe, jak i rozbudowane, wielomodułowe. W praktyce
jednak, w dokumentacji i w szablonach (`cookiecutters`) zastosowany jest układ
plików, który sprawdza się w większości zastosowań.

## Baza danych

Pyramid nie jest w żaden sposób zależny od jakiejkolwiek bazy danych i zostawia
użytkownikowi decyzję o użyciu bazy i o jej rodzaju. Nie oznacza to, że
programista pozostawiony jest samemu sobie - istnieją oficjalne szablony
projektów współpracujące z SQLAlchemy i z ZODB. Ponadto w PyPI można znaleźć
wsparcie dla Cassandry, Redisa, MongoDB i wielu innych.

## Szablony (*templates*)

Nie zdziwi cię czytelniku fakt, że i w tym miejscu panuje pełna swoboda.
Dostępne są oficjalne integracje z Jinja2, Chameleonem i Mako, a także wiele
nieoficjalnych - do wyboru, do koloru. Dzięki mechanizmowi *rendererów*
używanie szablonów jest proste i przyjemne.

### Formularze

Tworzenie i walidacja formularzy nie jest częścią Pyramida, ale z pomocą
przychodzi nam Pylons Project i biblioteka `deform`. Ponadto wśród oficjalnych
dodatków możemy znaleźć jeszcze `WTForms`.

# *Killer features*

Po tych wszystkich przytłaczających informacjach czas przejść do
przyjemniejszych tematów. Poniżej przedstawiam najciekawsze, moim zdaniem,
elementy Pyramida, które niekoniecznie są unikalne i niepowtarzalne, ale
obecność ich wszystkich w jednym frameworku czyni go bardzo potężnym.

## Widoki

Widok to kawałek kodu powiązany z konkretną ścieżką aplikacji. W Pyramidzie
może to być zwykła funkcja albo klasa bądź obiekt posiadający metodę
`__call__()`. Ostatecznym celem widoku jest utworzenie obiektu typu `Response`
i zwrócenie go jako wynik wywołania funkcji.

## Konfiguracja

Pyramid, poza imperatywnym mechanizmem konfiguracji (funkcje typu `add_view()`),
udostępnia także bardzo wygodny deklaratywny mechanizm, oparty na dekoratorach.
Dzięki temu, zamiast wspomnianego `add_view()`, wystarczy dodać przed naszą
funkcją widoku dekorator `@view_config()`, który zostanie odnaleziony podczas
startu aplikacji.

Dzięki bibliotece `Venusian` (należącej oczywiście do Pylons Project)
aplikacja może zostać przeskanowana pod kątem konfiguracji zaszytej w rozsianych
po całym kodzie dekoratorach. Dzięki takiemu podejściu konfiguracja znajduje
się razem z powiązanym z nią kodem i w razie zmian nie ma konieczności
dokonywania zmian w dwóch miejscach. Minusem jest to, że skanowanie
konfiguracji wykonywane jest od nowa przy każdym uruchomieniu aplikacji,
co może opóźnić nieco jej start.

## Traversal

Pyramid posiada dwa (a jakże) mechanizmy służące do mapowania adresu URL na kod
aplikacji. Pierwszy z nich, zwany *URL Dispatch*, to klasyczny *routing* i jest
podobny do mechanizmów obecnych w innych frameworkach, a co za tym idzie
nudny - tworzymy listę mapującą wzorce ścieżki (wyrażenia regularne) na widoki.

Drugi mechanizm nazywa się *Traversal* i wykradziony został z ZOPE. Opiera się
on na tworzeniu drzewiastej struktury obiektów reprezentujących zasoby.
Przypomina to rozgałęzioną strukturę katalogów na dysku albo zagnieżdżone
pythonowe słowniki.

Poszukiwanie zasobu rozpoczyna się od rozbicia ścieżki na części oddzielone
znakiem `/`. Następnie tworzony jest zasób początkowy (`root`) i podawany
jest do niego pierwszy segment ścieżki (jak w słowniku: `root[path[0]]`).
Jeśli operacja się powiedzie (czyli zasób zachowuje się jak słownik i zwraca wartość
dla podanego klucza), to otrzymaną wartość traktujemy tak samo jak `root` i
idziemy rekurencyjnie w głąb.

W momencie, gdy skończą nam się części ścieżki albo gdy nie uda się pobrać
zasobu podrzędnego, algorytm przejścia dobiega końca, a jego wynikiem jest
ostatni (najbardziej zagnieżdżony) z uzyskanych zasobów.

W następnym kroku poszukiwane są widoki skojarzone ze znalezionym zasobem.
Oczywiście nic się nie marnuje i jeśli pozostał jeszcze jakiś
nieprzetrawersowany fragment ścieżki, to zostanie on przekazany do funkcji
widoku. Co więcej, istnieje jeszcze jedna opcja - możemy stworzyć kilka widoków
skojarzonych z tym samym zasobem, różniących się tylko nazwą. W takiej
sytuacji pierwszy nieskonsumowany fragment ścieżki jest traktowany jako nazwa
widoku (często jest to nazwa w stylu: `show`, `edit`, `delete`).

Warto tutaj dodać, że choć *traversal* zachowuje się jakby wchodził w głąb
zagnieżdżonych słowników, to same zasoby słownikami być nie muszą (i
zwykle nie są). Jak już zdążyli nas przyzwyczaić twórcy Pyramida, także
w tej kwestii mamy całkowitą swobodę - wystarczy, że stworzymy klasę z metodą
`__getitem__`, która na przykład pobierze dane z bazy i już mamy nasz zasób.

Brzmi skomplikowanie i takie jest w istocie, ale korzyści z zastosowania
*traversala* mogą być bardzo znaczące. Przede wszystkim struktura zasobów
ma charakter drzewiasty i znacznie lepiej niż płaski *routing* odzwierciedla
strukturę adresu URL. Ponadto, *traversal* nie jest podatny na trudne
w wykryciu błędy wewnątrz wyrażeń regularnych, ani też nie jest wrażliwy
na kolejność wpisów. Po trzecie, bardzo łatwo dodać nową funkcjonalność do
takiej struktury, tworząc nową gałąź w odpowiednim miejscu
istniejącego drzewa, co nigdy nie wpływa to na pozostałe zasoby.

Początkującym (a także zaawansowanym) amatorom *traversala* może pomóc
malutka biblioteczka o nazwie `TraversalKit`, która dostarcza klasę bazową
dla zasobu oraz ułatwia tworzenie drzewa zasobów.

## Brak pierwiastka magicznego

Pyramid stawia przejrzystość na pierwszym miejscu, dlatego próżno w nim szukać
magii składniowej w stylu `py.test` czy `SQLAlchemy`. Z jednej strony może to
zniechęcać początkującego użytkownika (nic się samo nie wyczaruje), ale tę
cechę docenią bardziej doświadczeni programiści, gdyż framework nie blokuje
twórcy swoimi, z definicji ograniczonymi, DSLami. Odsuwa to także groźbę "walki
z frameworkiem", która często pojawia się w większych projektach.

Jedynym odstępstwem od zasady "niemagiczności" jest wspomniana wcześniej
deklaratywna konfiguracja.

# Ciekawostki

Na koniec zebrałem garść ciekawostek dotyczących Pyramida, przedstawionych
w maksymalnie skondensowanej formie.

**Początki** - pierwotnie Pylons Project pracował nad web frameworkiem o nazwie
Pylons, jednakże po wydaniu wersji 1.0 podjęto odważną decyzję i zamiast
tworzyć go dalej wzięto na warsztat bibliotekę `repoze.bfg`, skupiając
wysiłki na jej rozwijaniu. Na koniec zmieniono nazwę na bardziej chwytliwą
i tak oto powstał Pyramid. Jest to chyba najdobitniejszy przykład
pragmatycznego podejścia programistów Pylons Project.

**Pliki statyczne** - w przeciwieństwie do większości frameworków, w Pyramidzie
nie musimy się obawiać serwowania plików statycznych bezpośrednio przez
aplikację. Mamy do dyspozycji liczne narzędzia pomagające nam w tym zadaniu,
jest też wbudowany *cache buster*.

**Waitress** - to stworzony przez Pylons Project prosty (ale w pełni
funkcjonalny) serwer WSGI, który może być z powodzeniem używany z aplikacjami
Pyramida. Jego podstawową cechą jest przenośność i łatwość zastosowania
zarówno w środowisku developerskim, jak i produkcyjnym.

**Interfejsy** - budowa wewnętrzna Pyramida w znacznym stopniu opiera się na
interfejsach z biblioteki `zope.interface`. Może to początkowo powodować
pewną awersję, bo kod troszkę "śmierdzi" Javą, ale twórcy wiedzieli co robią
i nie przeciągnęli struny - hierarchia klas jest bardzo prosta i niezbyt głęboka,
dlatego trudno się w niej pogubić.

**Sesje** - jak na Pyramida przystało, do dyspozycji mamy kilka silników sesji.
Dostępne od ręki są to tylko nieszyfrowane sesje ciasteczkowe
(podpisywane lub nie), ale w oficjalnych rozszerzeniach znajdziemy szyfrowane
sesje oparte o PyNaCl albo serwerowe, używające Redisa. Jeśli powyższe
rozwiązania nam nie pasują, zawsze możemy stworzyć własną klasę sesji
implementując interfejs `ISession`.

**Uwierzytelnianie** - Pyramid obsługuje liczne metody uwierzytelniania
(od *basic auth*, przez rozwiązania z ciasteczkami, aż po cięższy oręż typu
LDAP). Oczywiście nie ma przeszkód, żeby stworzyć własny autentykator,
wystarczy zaimplementować interfejs `IAuthenticationPolicy`.

**Autoryzacja** - w pakiecie podstawowym mamy do dyspozycji tylko jeden
mechanizm autoryzacji oparty o listy ACL, który jest wszechstronny, acz nie
najłatwiejszy w użyciu. Na szczęście istnieje wiele dodatków, które powiększają
ilość opcji w tym zakresie, a poza tym dość łatwo można stworzyć samemu
autorską autoryzację (na pewno zgadłeś, że wystarczy zaimplementować interfejs
`IAuthorizationPolicy`).

**Debug Toolbar** - to przepotężne narzędzie bardzo pomagające w diagnozowaniu
błędów w naszej aplikacji. Wystarczy je otworzyć w zakładce przeglądarki, by
otrzymać wszelkie informacje na temat żądań HTTP, nagłówków, wydajności,
logów, a nawet zapytań do bazy danych.

**Tweens** - Pyramid posiada możliwość "wciśnięcia" kodu pomiędzy zapytanie
a naszą aplikację. Brzmi to trochę jak *middleware* WSGI, z tą różnicą, że
*tween* uruchamiany jest w kontekście aplikacji, gdzie ma dostęp
do jej stanu wewnętrznego. W taki właśnie sposób zaimplementowany jest m.in.
Debug Toolbar.

**Generowanie URLi** - Pyramid potrafi tworzyć URLe na podstawie tras
(*routes*), dzięki czemu możemy uniknąć topornego i bardzo podatnego na błędy
ręcznego "klejenia" adresów.

**Szybkość** - pomimo złożonej funkcjonalności Pyramid okazuje się być
całkiem szybki, rozstawiając po kątach znaczną część liczącej się konkurencji.
Nie wykazuje się też nadmierną zasobożernością, dzięki czemu utrzymanie
aplikacji jest względnie tanie.

# Podsumowanie

Pyramid, dzięki połączeniu wielu elementów, tworzy bardzo spójne i
wszechstronne środowisko do tworzenia aplikacji webowych. Po wykonaniu
pierwszych trudnych kroków staje się wygodny w użyciu i nad wyraz intuicyjny.
Bardzo dobrze nadaje się zarówno do małych projektów, jak i do wielkich
aplikacji, a jego szybkość i niezawodność powodują, że jest tani w utrzymaniu.

Dlatego też mam nadzieję, że moim tekstem zachęciłem Cię do przyjrzenia się
(może ponownego) temu niedocenionemu frameworkowi, jakim jest Pyramid.

## Bibliografia

1. Pyramid strona domowa. https://trypyramid.com
2. Pylons Project. https://pylonsproject.org
3. Dokumentacja Pyramida. https://docs.pylonsproject.org/projects/pyramid/\crlf
    en/latest/
4. Projekty rozwijane przez Pylons Project. https://pylonsproject.org/projects.html
5. Oficjalne dodatki (*add-ons*). https://trypyramid.com/\crlf
    resources-extending-pyramid.html
6. Strona domowa `WebOb`, wrappera WSGI używanego przez Pyramid.\crlf
    https://webob.org
7. Przewodnik po Pyramidzie. https://docs.pylonsproject.org/projects/pyramid/\crlf
    en/latest/quick`_`tour.html
