# Twoja wirtualna piaskownica dzięki narzędziu Vagrant
## Piotr Banaszkiewicz 

Vagrant jest narzędziem zapewniającym programistom takie same środowiska do pracy,
niezależnie od komputera. Można uznać, że jest to taki `virtualenv`, tylko na
innym poziomie --- bo nie obejmuje samych pakietów pythonowych, lecz cały system
operacyjny. Vagrant do działania wykorzystuje VirtualBoxa, także może zostać
zainstalowany na praktycznie dowolnym systemie operacyjnym.

### Jak działa Vagrant?

Vagrant (http://vagrantup.com/) tworzy wirtualną maszynę VirtualBox
z przygotowanego wcześniej obrazu (zwanego boksem), konfiguruje jej ustawienia,
a na końcu uruchamia na niej specjalne skrypty, za pomocą których można
zainstalować serwery HTTP, pocztowe, baz danych, skonfigurować użytkowników
--- w zasadzie można wszystko.

### Zastosowania

Dzięki Vagrantowi programiści mogą mieć wiele wirtualnych maszyn dla różnych
projektów. Nie muszą się przejmować zależnościami, bibliotekami, frameworkami,
systemami baz danych, serwerami. Nie potrzebują pamiętać o włączaniu, wyłączaniu
czy przełączaniu odpowiednich systemów czy nawet różnych wersji danego
oprogramowania.

Programiści pracujący w zespołach mogą mieć identyczne środowiska pracy,
niezależne od ich osobistych preferencji co do systemu operacyjnego
i zainstalowanego oprogramowania. Każdy członek zespołu będzie miał biblopteki
w tej samej wersji, co jego koledzy.

Firmy mogą bardzo łatwo i szybko ustawić środowisko pracy na nowym komputerze
nowego pracownika. A gdy aplikacja, nad którą pracują, wykorzystuje dużo
różnych serwerów (np. jeden dla baz danych, jeden dla aplikacji, jeden dla
cache'u), nie trzeba kupować dedykowanych serwerów, bo wszystko może zostać
uruchomione na laptopie programisty.

### Pierwsze kroki programisty

Zakładając, że mamy przygotowany wcześniej odpowiedni box
wraz z odpowiednimi skryptami, uruchomienie może wyglądać następująco:

    $ git clone git://github.com/YourCompany/project-vagrantsetup.git
    $ cd project-vagrantsetup
    $ vagrant up

i wirtualna maszyna po chwili będzie działać.

Każda maszyna do uruchomienia potrzebuje pliku ``Vagrantfile``, w którym
konfiguruje się takie ustawienia, jak:

* zmiana konfiguracji maszyny (ilość pamięci RAM, procesorów, akceleracja sprzętowa,
  itd.);
* nazwa sieciowa;
* wykorzystywany box, czyli wcześniej przygotowany obraz systemu;
* foldery współdzielone z hostem;
* interfejsy sieciowe;
* tzw. przepis, czyli informacje o skryptach wywoływanych po uruchomieniu
  maszyny.

Gdy jest konieczność uruchomienia wielu różnych maszyn (na przykład serwery PostgreSQL, Redis,
Django), można je wszystkie zdefiniować w jednym pliku
``Vagrantfile``. Uruchamianie wygląda wtedy tak:

    $ vagrant up postgres
    $ vagrant up redis
    $ vagrant up django

W tym artykule, dla uproszczenia, wszystkie przykłady będą dotyczyły konfiguracji z jedną
maszyną.

Najpopularniejsze komendy wykorzystywane w pracy z Vagrantem to:

* ``vagrant ssh [nazwa]``: uruchamia połączenie SSH do działającej maszyny
  wirtualnej,
* ``vagrant halt [nazwa]``: wyłącza maszynę wirtualną,
* ``vagrant suspend [nazwa]``: wstrzymuje maszynę wirtualną,
* ``vagrant resume [nazwa]``: wznawia pracę maszyny wirtualnej. Wznowienie jest
  również możliwe po restarcie hosta, ale ja miałem problemy ze
  spójnością logów po wznowieniu, więc częściej po prostu wyłączałem maszynę,
* ``vagrant reload [nazwa]``: przeładowanie ustawień, jeśli zostały zmienione,
* ``vagrant provision [nazwa]``: ponowne zastosowanie przepisu.

### Programowanie a foldery współdzielone

Domyślna konfiguracja maszyn Vagranta zawiera definicję folderu współdzielonego
``/vagrant``. Za pomocą takich folderów współdzielonych można rozwijać
oprogramowanie korzystając z narzędzi dostępnych na hoście i uruchamiać je na
maszynie wirtualnej.

Zwyczajowo oprogramowanie w Pythonie pisze się w przy użyciu mechanizmu "virtualenv", często
z wykorzystaniem "buildout". W przypadku korzystania z Vagranta nie jest
konieczne, bo zawsze dostajemy odseparowane środowisko wirtualne.
Można wtedy polegać na pakietach systemowych, zamiast na PyPI.

### Okiem menedżera: tworzenie i konfiguracja własnych boksów

Vagrant na swoich stronach domyślnie udostępnia tylko kilka boksów Ubuntu,
dlatego powstał projekt `veewee <https://github.com/jedi4ever/veewee/>`_ mający
na celu ułatwienie tworzenia własnych boksów.

Veewee działa w ten sposób, iż pobiera obraz ISO wybranej przez nas
dystrybucji, instaluje jako maszynę wirtualną VirtualBoxa, a na koniec może ją
zapaczkować (utworzyć ``Vagrantfile``?).

W Ubuntu domyślnie nie ma pakietu ``veewee``, trzeba go zainstalować z Ruby
gemów:

    $ sudo gem install veewee

Przy okazji zainstaluje to najnowszą wersję Vagranta, wobec czego nie ma
potrzeby korzystania z jego pakietu systemowego.

Po wykonaniu poniższych komend wyświetlona zostanie lista dystrybucji, które
mogą zostać wykorzystane jako bazowy system do stworzenia boksa. W lipcu 2012
lista zawierała nie tylko popularne Linuksy, ale także FreeBSD, Solarisa,
a nawet i Windows.

    $ mkdir nowy_box ; cd nowy_box
    $ vagrant basebox templates

Aby zacząć tworzyć nowy box, należy wybrać jego szablon i nazwę (na
przykładzie Ubuntu Server 12.05):

    $ vagrant basebox define 'nasza_nazwa' 'ubuntu-12.05-server-i386'

Zostanie utworzony katalog ``definitions/nasza_nazwa`` z plikami określającymi
konfigurację:

* ``definition.rb``: ustawienia
* ``postinstall.sh``: plik wykonywany po zainstalowaniu systemu
* ``preseed.cfg``: plik zmieniający proces instalacji systemu

Polecam zmienić ścieżkę do obrazu ISO w pliku ``definition.rb`` tak, żeby
skorzystać z naszych polskich
`serwerów lustrzanych Ubuntu <https://launchpad.net/ubuntu/+cdmirrors/>`_.

Kolejnym krokiem jest zbudowanie całego systemu:

    $ vagrant basebox build 'nasza_nazwa'

Veewee pobierze ISO, stworzy maszynę wirtualną i na niej zainstaluje pobrany
system. Cała operacja może zająć trochę czasu, w zależności od prędkości łącza
internetowego i sprawności komputera hosta.

Po zainstalowaniu systemu, można go wstępnie skonfigurować, np. zainstalować
pakiety, z których chcemy korzystać. Nie jest to jednak zalecane, gdyż powinno
się korzystać z "przepisu". Przyda się on podczas uruchamiania projektu "na
produkcji".

    $ sudo apt-get install postgresql python-virtualenv nginx

Na koniec warto sprawdzić poprawność stworzonego systemu, zapaczkować go
i dodać do Vagranta:

    $ vagrant basebox validate 'nasza_nazwa'
    $ vagrant basebox export 'nasza_nazwa'
    $ vagrant box add 'nasza_nazwa' 'nasza_nazwa.box'

Gotowe! Obraz wirtualnej maszyny można teraz wykorzystywać wszędzie. Warto
jednak jeszcze przygotować sobie plik ``Vagrantfile`` i cały przepis.

Wydając polecenie ``vagrant init 'nasza_nazwa'`` w danym katalogu zostanie
utworzony plik ``Vagrantfile``. Plik ten zawiera bardzo dużo komentarzy, więc
jego zmiana nie będzie trudna dla nikogo.

Bardzo ważnym aspektem jest --- już wiele razy wspomniany --- przepis, zwany
w konfiguracji Vagranta: ``provision``. To ustawienie określa sposoby
interpretowania instrukcji instalacji i konfiguracji dodatkowego
oprogramowania. Kilka znanych aplikacji, które służą do tego celu, a które
wspiera Vagrant, to Chef (solo i serwer) oraz Puppet (zwykły i serwer). W tym
przykładzie posłużę się Chefem solo.

Chef instaluje oprogramowanie bazując na "książkach kucharskich" (cookbooks).
Listę popularnych, stworzonych przez użytkowników książek można znaleźć
`tutaj <http://community.opscode.com/cookbooks>`_.

Niektóre książki mają wymagane zależności, które nie są opisane na wspomnianej
stronie. Można je jednak często znaleźć na stronach źródeł (czyli zazwyczaj na
serwisie internetowym Github).

Konfiguracja ``Vagrantfile`` dla naszego przykładu, Chefa, Postgresa
i Nginxa:

    Vagrant::Config.run do |config|
        config.vm.box = "ubuntu"
        config.vm.network :hostonly, "192.168.33.10"
        config.vm.provision :chef_solo do |chef|
            chef.cookbooks_path = "recipes/cookbooks"
            chef.add_recipe "nginx"
            chef.add_recipe "postgresql91"
        end
    end

W katalogu z ``Vagrantfile`` należy utworzyć katalog ``recipes/cookbooks``,
a w nim rozpakować recepty wymagane przez Postgresa i Nginxa:
``build-essential``, ``nginx``, ``ohai``, ``openssl``, ``postgresql``,
``postgresql91``, ``runit``.

Po uruchomieniu ``vagrant up`` maszyna wirtualna zostanie utworzona
(bazując na naszym obrazie, który stworzyliśmy wcześniej), skonfigurowana,
a wybrane pakiety zostaną automatycznie zainstalowane.

### Przydatne linki

* Vagrant: http://vagrantup.com/
* Dokumentacja Vagranta: http://vagrantup.com/v1/docs/index.html
* VirtualBox: https://www.virtualbox.org/
* Veewee: https://github.com/jedi4ever/veewee/
* Chef: http://www.opscode.com/chef/
* Chef Cookbooks: http://community.opscode.com/cookbooks
* Slajdy z prezentacji (dostępne po konferencji):
  http://staff.osuosl.org/~pbanaszkiewicz/PyConPL2012/
