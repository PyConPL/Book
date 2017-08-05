# Minecraft sterowany Pythonem

Minecraft zapewnia niczym nieskrępowaną kreatywność i swobodę tworzenia. Python jest prosty do czytania i zapisywania, daje duże możliwości tak początkującemu, jak i zaawansowanemu programiście. Dzięki zintegrowaniu Minecrafta z Pythonem możemy uzyskać jeszcze większą kontrolę nad Minecraftem i tym samym wyzwolić większe pokłady kreatywności.


Dlaczego warto?

  - Poznanie ukrytej magii Minecrafta - urozmaicenie gry i odkrycie jej nieznanych możliwości
  - Zapoznanie się z Pythonem - dla początkujących programistów
  - Nauczanie programowania, w szczególności wśród dzieci (od ok. 10 lat) i młodzieży
  - Ułatwienie poruszania się i budowania w świecie Minecraft.

## Startujemy

Co jest potrzebne:
  - [Minecraft] - Minecraft w wersji podstawowej
  - [Python] - minimum Python 3
  - [Java] - najlepiej ostatnia wersja
  - API Minecraft Python - pobierz  Minecraft Tools dla [Windows], [MAC OS], [Rapsberry Pi lub Ubuntu]
  - [Server Minecraft Spigot] - wersja Spigot zgodna z wersją Minecrafta

Jeśli na komputerze mamy już Minecrafta, Pythona i Javę, należy ściągnąć, rozpakować folder "Minecraft Tools" i zainstalować API Minecrafta poprzez uruchomienie "Install`_`API" spośród wyodrębnionych plików. Wtedy należy pobrać taką wersję serwera Spigot, która jest zgodna z posiadaną wersją Minecrafta. Pobrany plik "Spigot.jar" należy podmienić w folderze "server" w "Minecraft Tools". Wtedy można już uruchomić serwer poprzez "Start`_`server" z folderu "Minecraft Tools". Okna serwera nie należy zamykać.

Wtedy wystarczy już tylko:
1) Uruchomić Minecrafta, 
2) Przejść w tryb Multiplayer,
3) Dodać serwer: nazwa dowolna, w adresie wpisać "localhost"
4) Wejść w tryb Multiplayer poprzez utworzony serwer.

### Testujemy

Żeby przetestować połączenie serwera i API, a także tworzyć programy współpracujące z Minecraftem, należy mieć uruchomiony serwer oraz Minecrafta w trybie Multiplayer (z ustawionym serwerem Spigot).

W edytorze Idle wpisujemy:
```sh
>>> from mcpi.minecraft import Minecraft
>>> mc = Minecraft.create ()
```
Te 2 pierwsze łączą program z Minecraftem. Jeśli po uruchomieniu programu nie pojawił się komunikat o błędzie, możemy kontynuować wpisując np.

```sh
>>> mc.player.setTilePos(0,120,0)
```
Dzięki temu poleceniu nasz bohater w Minecrafcie powinien unieść się wysoko nad ziemię. Jeśli tak się stało, wszystko działa sprawnie.

## Misje

W Minecrafcie jest wiele przydatnych akcji, jakie można uruchomić sterując Pythonem. Warto je znać, aby móc się szybciej i efektywniej: wybudować, wyżywić, schronić przed wrogimi bytami czy teleportować.

### Teleportacja

Położenie w Minecrafcie można łatwo ustalić za pomocą klawisza F3.

Jeśli znamy docelowe współrzędne, można szybko teleportować się w wybrane miejsce:

```sh
from mcpi.minecraft import Minecraft
mc = Minecraft.create ()
x=10
y=110
y=12
mc.player.setPos (x, y, z)
```

W ten sposób można np. szybko uciec przed zombie w bezpieczne miejsce - jak wnętrze domu, jeśli wcześniej znamy jego współrzędne.

Jeśli chcemy np. "obejść" znane sobie miejsca, tj. przenieść się gdzieś, rozejrzeć się i przenieść znów w inne miejsce, przydatna będzie funkcja *sleep*. Żeby ją wykorzystać, musimy dodać do programu moduł *time* poprzez:

```sh
>>> import time
```

Wtedy możemy wykorzystać funkcję *sleep*
```sh
>>> time.sleep (5)
```
żeby przenieść się w wybrane miejsce na 5 sekund, a następnie wybrać w kolejne miejsce:
```sh
from mcpi.minecraft import Minecraft
mc = Minecraft.create ()
mc.player.setPos (10, 110, 12)
time.sleep (5)
mc.player.setPos (20, 110, 50)
```

### Stawianie bloków

W Minecrafcie każdy typ bloku ma swój ID. Pełną listę bloków dostępnych w Minecrafcie znajdziesz tu: [Lista bloków]. Znając ID bloku oraz współrzędne, gdzie chcemy dany blok postawić, możemy w szybki sposób go umieścić w danym miejscu.

```sh
from mcpi.minecraft import Minecraft
mc = Minecraft.create ()
mc.setBlock (10, 110, 12, 103)
```
W powyższym przypadku postawiliśmy arbuza (kod 103). 

### Szybkie budowanie

To, co jest nam od początku potrzebne w świecie Minecraft, to odpowiednie schronienie. Dlatego zazwyczaj pierwszy dzień w grze przeznaczamy na budowę domu. Jest to szczególnie istotne w trybie przetrwanie, gdzie dom stanowi schronienie przed wrogimi bytami, jak np. zombie.

Do tworzenia jednego bloku wykorzystaliśmy funkcję *setBlock ()*, a do budowania większych bloków użyjemy funkcji *setBlocks ()*, która pozwoli nam stworzyć prostopadłościan.

```sh
from mcpi.minecraft import Minecraft
mc = Minecraft.create ()
poz = mc.player.getPos ()
x = poz.x
y = poz.y
z = poz.z
szer = 10
wys = 5
dlug = 6
typBloku = 4
powietrze = 0
mc.setBlocks (x,y,z,x+szer, y+wys, z+dlug, typBloku)
```

W ten sposób utworzony prostopadłościan jest pełny w środku. Teraz trzeba stworzyć mniejszy prostopadłościan zbudowany z bloków powietrza poprzez zmniejszenie argumentów wcześniej zbudowanego prostopadłościanu o 1. 

Istotne jest to, że w powyższym przykładzie użyliśmy funkcji *getPos ()*, która zwraca współrzędne jako wartości rzeczywiste, w przeciwieństwie do funkcji *getTilePos ()*, która zwraca współrzędne jako liczby całkowite. 

## Źródła:
  -   [Minecraft - gamepedia]
  -   "*Nauka programowania z Minecraftem*" - autor: Craig Richardson, Warszawa, 2016.


   [Minecraft]: <[https://minecraft.net/en-us/download/]>
   [Python]: <https://www.python.org/downloads/>
   [Java]: <https://www.java.com/en/download/>
   [Windows]: <https://sourceforge.net/projects/python-with-minecraft-windows/>
   [MAC OS]: <https://sourceforge.net/projects/python-with-minecraft-mac/files/?source=navbar>
   [Rapsberry Pi lub Ubuntu]: <https://github.com/py3minepi/py3minepi>
   [Rapsberry Juice]: <https://dev.bukkit.org/projects/raspberryjuice>
   [Server Minecraft Spigot]: <https://getbukkit.org/spigot>
   [Lista bloków]: <http://minecraft-pl.gamepedia.com/Warto%C5%9Bci_danych>
   [Minecraft - gamepedia]: <http://minecraft-pl.gamepedia.com/Warto%C5%9Bci_danych>
