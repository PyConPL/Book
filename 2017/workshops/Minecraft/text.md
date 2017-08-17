# Minecraft sterowany Pythonem

Minecraft [1] zapewnia niczym nieskrępowaną kreatywność i swobodę tworzenia.
Python jest prosty do czytania i zapisywania, daje duże możliwości tak
początkującemu, jak i zaawansowanemu programiście. Dzięki zintegrowaniu
Minecrafta z Pythonem możemy uzyskać jeszcze większą kontrolę nad Minecraftem
i tym samym wyzwolić większe pokłady kreatywności [2].

Zalety integracji Minecrafta z Pythonem są następujące:

- poznanie ukrytej magii Minecrafta - urozmaicenie gry i odkrycie jej nieznanych możliwości;
- zapoznanie się z Pythonem - dla początkujących programistów;
- nauczanie programowania, w szczególności wśród dzieci (od ok. 10 lat) i młodzieży;
- ułatwienie poruszania się i budowania w świecie Minecraft.

## Przygotowujemy środowisko

### Instalujemy

Potrzebujemy następujące programy:

- Minecraft [3] w wersji podstawowej;
- Python [4] - minimum Python 3;
- Java [5] - najlepiej ostatnia wersja;
- API Minecraft Python - pobierz Minecraft Tools dla Windows [6], MAC OS [7], Raspberry Pi [11] lub Ubuntu [8];
- Server Minecraft Spigot [9] - wersja Spigot zgodna z wersją Minecrafta.

Jeśli na komputerze mamy już Minecrafta, Pythona i Javę, należy ściągnąć,
rozpakować folder "Minecraft Tools" i zainstalować API Minecrafta poprzez
uruchomienie "Install`_`API" spośród wyodrębnionych plików. Wtedy należy
pobrać taką wersję serwera Spigot, która jest zgodna z posiadaną wersją
Minecrafta. Pobrany plik "Spigot.jar" należy podmienić w folderze "server"
w "Minecraft Tools". Wtedy można już uruchomić serwer poprzez "Start`_`server"
z folderu "Minecraft Tools". Okna serwera nie należy zamykać.



### Ustawiamy

#### Zmiana trybu przetrwania na tryb kreatywny

Jeśli pierwszy raz instalujesz Minecraft wystarczy wejść do Minecraft-Tools > server  
i otworzyć w notatniku plik "server" (plik properties), a następnie wyszukać i zmienić 
wartości następujących ustawień: 

```sh
>>> force-gamemode=true
>>> gamemode=1   
```
W przypadku problemów polecam pobrać i wkleić w folderze Minecraft-Tools > server > plugins 
następujący plik .jar: ChangeGameMode-3.5 [12]. 

W przeciwnym razie (jeśli na komputerze znajdują się już pliki logowania danego gracza) najlepiej 
zainstalować NBTExplorer [13], uruchomić i zmienić następujące ustawienia: 

saves >> <nazwa świata> >> level.dat >> data: Nb entries >> **Game Type: 1**
saves >> <nazwa świata> >> playerdata >> <player name> >> **playerGame Type: 1**



#### Usiawienie trybu multiplayer na serwerze Spigot

Należy:
1. uruchomić serwer: Minecraft-Tools > Start server
2. uruchomić Minecrafta;
3. przejść w tryb Multiplayer;
4. dodać serwer: nazwa dowolna, w adresie wpisać "localhost";
5. wejść w tryb Multiplayer poprzez utworzony serwer.


### Testujemy

Żeby przetestować połączenie serwera i API, a także tworzyć programy
współpracujące z Minecraftem, należy mieć uruchomiony serwer oraz Minecrafta
w trybie Multiplayer (z ustawionym serwerem Spigot).

W edytorze Idle wpisujemy:
```sh
>>> from mcpi.minecraft import Minecraft
>>> mc = Minecraft.create ()
```
Te 2 pierwsze łączą program z Minecraftem. Będziemy je wykorzystywać za każdym razem, gdy tworzymy nowy program. 

Jeśli po uruchomieniu programu nie pojawił się komunikat o błędzie, możemy kontynuować wpisując np.

```sh
>>> mc.player.setTilePos(0,120,0)
```
Dzięki temu poleceniu nasz bohater w Minecrafcie powinien unieść się wysoko
nad ziemię. Jeśli tak się stało, wszystko działa sprawnie.


## Misje

W Minecrafcie jest wiele przydatnych akcji, jakie można uruchomić sterując
Pythonem. Warto je znać, aby móc się szybciej i efektywniej: wybudować,
wyżywić, schronić przed wrogimi bytami czy teleportować.

### Teleportacja

Położenie w Minecrafcie można łatwo ustalić za pomocą klawisza F3.

Jeśli znamy docelowe współrzędne, można szybko teleportować się w wybrane miejsce:

```sh
x=10
y=110
y=12
mc.player.setPos (x, y, z)
```

W ten sposób można np. szybko uciec przed zombie w bezpieczne miejsce - jak
wnętrze domu, jeśli wcześniej znamy jego współrzędne.

Jeśli chcemy np. "obejść" znane sobie miejsca, tj. przenieść się gdzieś,
rozejrzeć się i przenieść znów w inne miejsce, przydatna będzie funkcja
*sleep*. Żeby ją wykorzystać, musimy dodać do programu moduł *time* poprzez:

```sh
>>> import time
```

Wtedy możemy wykorzystać funkcję *sleep*
```sh
>>> time.sleep (5)
```
żeby przenieść się w wybrane miejsce na 5 sekund, a następnie wybrać w kolejne miejsce:
```sh
mc.player.setPos (10, 110, 12)
time.sleep (5)
mc.player.setPos (20, 110, 50)
```

### Stawianie bloków

W Minecrafcie każdy typ bloku ma swój ID, a pełna lista bloków dostępnych
w Minecrafcie jest na [10]. Znając ID bloku oraz współrzędne,
gdzie chcemy dany blok postawić, możemy w szybki sposób go umieścić
w danym miejscu.

```sh
mc.setBlock (10, 110, 12, 103)
```
W powyższym przypadku postawiliśmy arbuza (kod 103).

### Szybkie budowanie

To, co jest nam od początku potrzebne w świecie Minecraft, to odpowiednie
schronienie. Dlatego zazwyczaj pierwszy dzień w grze przeznaczamy na budowę
domu. Jest to szczególnie istotne w trybie przetrwanie, gdzie dom stanowi
schronienie przed wrogimi bytami, jak np. zombie.

Do tworzenia jednego bloku wykorzystaliśmy funkcję *setBlock ()*,
a do budowania większych bloków użyjemy funkcji *setBlocks ()*,
która pozwoli nam stworzyć prostopadłościan.

```sh
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

W ten sposób utworzony prostopadłościan jest pełny w środku. Teraz trzeba
stworzyć mniejszy prostopadłościan zbudowany z bloków powietrza
poprzez zmniejszenie argumentów wcześniej zbudowanego prostopadłościanu o 1. 
Następnie, podobnie (poprzez zastąpienie bloków bruku blokami powietrza) 
w odpowiednich miejscach mozna zrobić miejsce na drzwi.

Istotne jest to, że w powyższym przykładzie użyliśmy funkcji *getPos ()*,
która zwraca współrzędne jako wartości rzeczywiste, w przeciwieństwie
do funkcji *getTilePos ()*, która zwraca współrzędne jako liczby całkowite.

### Posadź sobie drzewo... albo cały las 

Drzewo do drewno i liście. Nie musisz sadzić sadzonek i czekać aż urośnie.
Wystarczy użyć funkcji _setBlock()_ albo _setBlocks()_. 
Zdefiniuj funkcję, żeby móc szybko sadzić kolejne drzewa.

```sh
def growTree(x, y, z):
    _// Write your code to make a tree here_
pos = mc.player.getTilePos()
x = pos.x
y = pos.y
z = pos.z
growTree(x + 1, y, z)
```


### Sprawdź, jak daleko od domu jesteś

Czasami przechadzając się po świecie w Minecraft możesz zastanawiać się, 
jak daleko odszedłeś/ odeszłaś od domu. Na szczęście możesz użyć koordynatów domu 
aby sprawdzić, jak daleko od niego się znajdujesz.

```sh
import math
homeX = -53.853
homeZ = 203.597
pos = mc.player.getTilePos()
x = pos.x
z = pos.z
distance = math.sqrt((homeX - x) ** 2 + (homeZ - z) ** 2)
mc.postToChat(distance)
```
Informacja wyświetli się w czacie Minecraftu, który można wyświetlić używając "t".


### Sprawdź, czy dany blok jest tym, co myślisz

Czasami ciężko powiedzieć, na jaki typ bloku patrzymy. Czy mogę to zjeść?
Możesz sprawdzić, czy dany blok jest faktycznie tym czym podejrzewasz, że jest,
używając operatorów logicznych.

```sh
from mcpi import block
melon = 103
block = mc.getBlock(-19, 77, 153)
noMelon = block != melon
mc.postToChat ("To nie jest melon: " + str(noMelon))
```


### Chroń swój świat

Czasami można zniszczyć więcej niż by się chciało. Aby uczynić świat "niezmiennym" (eng. immutable), czyli uniemożliwić rozbijanie bloków, uzyjemy specjalnej funkcji oraz warunku i polecenia przekazywanego w czacie.

```sh
answer = input("Do you want blocks to be immutable? Y/N”)
if  answer == „Y”:
    mc.setting("world_immutable", True)
    mc.postToChat("World is immutable")
else:
    mc.setting("world_immutable", False)
    mc.postToChat("World is mutable")
```

### Zbuduj schody do nieba


Wykorzystaj pętlę _while_ żeby zbudować schody do nieba.

```sh
pos = mc.player.getTilePos()
x, y, z = pos.x, pos.y, pos.z
stairBlock = 53
step = 0
while step < 10:
mc.setblock(x + step, y + step, z, stairBlock)
step += 1
```

Takie same schody możesz zrobyc wykorzystując pętlę _for_. 

Wykorzystując pętle możesz budować szybciej. Spróbuj teraz zbudować piramidę 
wykorzystując dowolną z pętli, jakie znasz.



## Bibliografia

1. Minecraft - gamepedia. https://minecraft-pl.gamepedia.com/
2. Craig Richardson. Nauka programowania z Minecraftem. PWN, Warszawa, 2016.
3. https://minecraft.net/en-us/download/
4. https://www.python.org/downloads/
5. https://www.java.com/en/download/
6. https://sourceforge.net/projects/python-with-minecraft-windows/
7. https://sourceforge.net/projects/python-with-minecraft-mac/
8. https://github.com/py3minepi/py3minepi
9. https://getbukkit.org/spigot
10. http://minecraft-pl.gamepedia.com/Wartości`_`danych
11. https://dev.bukkit.org/projects/raspberryjuice
12. https://dev.bukkit.org/projects/bw2801
13. http://www.minecraftforum.net/forums/mapping-and-modding/minecraft-tools/1262665-nbtexplorer-nbt-editor-for-windows-and-mac
