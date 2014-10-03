#Pygame - gry w świecie Pythona - Łukasz Jagodziński

## Jak zacząć?

Od najmłodszych lat, każdy z nas ma do czynienia z grami planszowymi, komputerowymi, konsolowymi czy innym rodzajem gier.
W późniejszym wieku lub nawet w młodszych latach, niektórzy z nas, bądź większość, chciała stworzyć własną grę, w którą
gracze chcieliby grać. W trakcie nauki programowania nasze możliwości stworzenia gry komputerowej znacznie się zwiększały.
Na zajęciach postaramy się napisać grę w naszym ulubionym języku, przy użyciu biblioteki pygame [1].
Ale zanim to nastąpi, zaczniemy krótkim teoretycznym wstępem, abyśmy mogli podejść do tematu jak najbardziej profesjonalnie.

## Czym tak naprawdę jest gra?

Gra jest to zabawa, która ma swoje zasady, dzięki którym możemy regulować jej stan, rozgrywkę oraz wygrać lub przegrać [2].
Po zapoznaniu się z terminem słowa gra, możemy usiąść i zabrać się za przygotowanie rodzaju gry, zasad, świata czy postaci.

## I co dalej?

Jak zapewne wiecie, nie ma "przepisu" na dobrą grę, która osiągnie niesamowity sukces. Większość z nas podczas rozgrywki
chciała zmienić reguły gry czy dodać coś, co wzbogaciłoby rozgrywkę. Dowodzi to, że każdy z nas ma pomysł, który nic nie kosztuje,
a może stworzyć nową grę, czy też wzbogacić nas o doświadczenie, jak dana rzecz faktycznie zadziała i czy zadziała poprawnie.
W pewien sposób jest to wstęp do projektowania gier, czy też samej produkcji gry. Jedną z metody rozpoczęcia pracy nad grą jest
stworzenie GDD (Game Design Document) [3], czyli dokumentu opisującego funkcjonalność i opis samej gry. Następnie można sprawdzić
rozpisany dokument i zadać sobie pytanie: *Czy chcielibyśmy sami zagrać w tę grę?*, pozwoli to nam na określenie grywalności gry według
własnego uznania - *Jeżeli nie tworzymy gry, w którą chcielibyśmy zagrać, to po co w ogóle to robić?*.

## Jak to ma się w świecie gier komputerowych?

Jak powszechnie wiadomo, w grach komputerowych królują inne języki jako te, w których się je tworzy, najbardziej popularne to C++, C#, JavaScript, HTML5
czy Flash. Natomiast języki takie jak Python czy Lua, często są wykorzystywane jako języki pomocnicze do pisania szybkich skryptów, ale niestety samo
pisanie gry w tych języka często jest mniej optymalne niż w wyżej wymienionych. Język C++ jest najczęściej wykorzystywany do tworzenia silników gry
(ang. game engine) [4], a Python jest używany, aby oskryptować odpowiednie narzędzia silnika graficznego. Oczywiście dla języków Lua czy Python istnieją również silniki
czy biblioteki, aby wspomóc te języki w programowaniu gier. Istnieją odpowiednie silniki w zależności od naszych potrzeb, tj. do gier 2D i 3D.
Dla języka Python najpopularniejsze silniki zostały przedstawione na wiki Pythonowym [5]. A jeżeli chodzi o język Lua, tutaj mamy trochę gorszą sytuację, gdyż tych
silników jest mniej, a niestety nie ma ich wszystkich spisanych, prawdopodobnie przyczyną jest mniejsza popularność tego języka niż Pythona [6].
Natomiast jednym z najbardziej popularnych silników jest LOVE [7].

Na naszych zajęciach wykorzystamy bibliotekę *Pygame* [1]. Zapoznamy się z funkcjami tej biblioteki oraz spróbujemy stworzyć grę.
W trakcie warsztatów również poruszymy kwestię, jak w łatwy sposób stworzyć grę przy użyciu mechaniki oraz wykorzystania gotowych rzeczy, które
można znaleźć w sieci tj. assety (dźwięki, grafiki). Wybierzemy również jeden z rodzajów gier, na którym się skupimy i postaramy się w ciągu
kilku godzin stworzyć pierwsze arcydzieło. :)

### Rodzaje gier:
* gry rekreacyjne
* gry logiczne
* gry platformowe
* gry zręcznościowe
* gry przygodowe
* gry akcji
* gry sportowe, wyścigi
* gry fabularne (cRPG), MMORPG
* gry strategiczne
* gry symulacyjne
* survival horrory
* gry edukacyjne

### Podsumowanie

Aby napisać grę, wystarczy pomysł, mechanika oraz grafika i dźwięk. W przypadku, gdy brakuje nam umiejętności do stworzenia grafiki, muzyki czy dźwięków,
istnieją serwisy, gdzie można je pobrać i wykorzystać całkowicie za darmo. Odpowiednio stworzony dokument GDD oraz zbalansowanie świata gry, pozwoli na
stworzenie gry, która będzie grywalna. Oczywiście wszystkie elementy, z którymi się zapoznamy, nie dadzą nam możliwości stworzenia gier takich jak GTA, BattleField
czy nawet mniej znanych tytułów, ale od czegoś trzeba zacząć, a przy okazji pobawimy się językiem Python i mam nadzieję, że stworzymy w pełni funkcjonalne i grywalne
gry. Być może uda się wspólnie wypracować dzieło, którym będziemy mogli się pochwalić na następnym PyConie. :)

### Referencje

* [1] [Oficjalna strona biblioteki PyGame](http://www.pygame.org/)
* [2] [Znaczenie słowa "gra" wg wikipedii](http://pl.wikipedia.org/wiki/Gra)
* [3] [Jak stworzyć Game Design Document](http://www.gamasutra.com/view/feature/131632/creating_a_great_design_document.php)
* [4] [Co to jest silnik gry](http://en.wikipedia.org/wiki/Game_engine)
* [5] [Silniki Pythonowe](https://wiki.python.org/moin/PythonGames)
* [6] [Silniki dla lua](http://www.gamefromscratch.com/post/2012/09/21/Battle-of-the-Lua-Game-Engines-Corona-vs-Gideros-vs-Love-vs-Moai.aspx)
* [7] [Oficjalna strona Love2D](http://love2d.org/)

<!-- Przeczytane: Piotr Kasprzyk -->
