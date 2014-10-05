# Packaging Python applications
## Piotr Banaszkiewicz

### Wstęp

Deployment aplikacji napisanych w Pythonie (a zwłaszcza aplikacji webowych) od
zawsze był problemem.  Na przestrzeni lat powstało wiele rozwiązań tego
problemu -- o różnych poziomach skuteczności i wymagających od programistów
wiedzy z zakresu zarządzania systemami operacyjnymi.

W tym artykule zostały przedstawione rozwiązania problemów pakowania
i dystrybucji aplikacji Pythonowych, które powinny pomóc głównie przy
aplikacjach webowych.  Pamiętajmy jednak, że każdy projekt jest inny, przez co
nie istnieje rozwiązanie uniwersalne.


### Rozwiązania historyczne

#### Jajka

Python Eggs to nie jest rozwiązanie problemu dystrybucji i instalacji pakietów.
"Jajka" to tylko i wyłącznie inna forma "importable" w Pythonie.

Owszem, odpowiednie ich użycie pozwala sprawnie zarządzać zależnościami
projektu, ale to nie jest jedyna rzecz, której projekty wymagają.  Poza
zależnościami Pythonowymi istnieją nieraz zależności systemowe (bazy danych,
serwery cache'u, etc.).

Natomiast zdecydowanym plusem jajek jest możliwość instalacji pakietów
binarnych.

Jeśli twój projekt nie korzysta z eggs, spróbuj ich uniknąć.  Obecnie są dużo
lepsze sposoby zarządzania pakietami Python'a.

#### Buildout

Ten system pozwala nie tylko na instalację pakietów (jajek) Pythonowych, ale
również na wstępną konfigurację.  I to także zależności niezwiązanych
z Pythonem.

Chociaż brzmi to bardzo fajnie, to stosowanie Buildouta wymaga dodatkowych
zależności zainstalowanych w systemie użytkownika.  I dobrej konfiguracji.

#### Fabric

Mimo iż Fabric służy do wykonywania pewnych poleceń na wielu hostach, może
zostać wykorzystany także jako narzędzie do deploymoentu.

Fabric jest bardzo uniwersalny, więc sposoby instalacji projektu mogą bardzo
się od siebie różnić.  Przykładowe:

1) tworzenie virtualenv'a lokalnie i ściąganie paczek (zależności) projektu
2) budowanie paczek lokalnie i wysyłanie ich na serwery, gdzie są instalowane
3) uruchamianie na serwerach ściągania projektu i instalowania zależności
   lokalnie

Wady tych rozwiązań są następujące:

* rozwiązanie **1)** nie różni się niczym od zwykłego Makefile'a.  Po co więc
  korzystać z dodatkowej zależności w postaci Fabrica?
* rozwiązanie **2)** wymaga jednakowej architektury serwerów.  Jest to bardzo
  trudne do uzyskania (jednakowe ścieżki, jednakowe architektury, jednakowe
  wersje zależności)
* rozwiązanie **3)** jest niezwykle powolne i wielokrotnie wymaga obecności
  gcc & co. na serwerach.

Istnieją bardziej eleganckie rozwiązania, stąd też odradzam Fabrica.

#### Paczki Pythona zainstalowane w systemie

Za każdym razem kiedy pisany przez Ciebie projekt da się zainstalować poprzez
zwykłe

    $ python setup.py install

na świecie jeden kotek jest ratowany przed śmiercią.

Obecnie standardem jest pisanie pliku ``setup.py`` z sekcją
``install_requires``, na przykład w ten sposób

    from setuptools import setup

    setup(
        ...
        install_requires=open('requirements.txt').read().splitlines(),
        ...
    )

Dzięki czemu nie musisz mieć dwóch list z zależnościami.

Instalowanie paczek Pythonowych w całym systemie nie jest zalecane. Samo
wymaganie praw administratora do instalacji projektu jest złe w 99% przypadków.


### Rozwiązania nowożytne

#### Środowiska wirtualne

TAK! Separacja, izolacja: to jest to, co programiści lubią najbardziej.
Utrzymywanie systemu "czystego" od zależności różnych projektów, automatyzacja
instalacji zależności i tak dalej... Jeśli jeszcze nie stosujesz virtualenv'a,
robisz coś źle.

Niestety, środowiska wirtualne Pythona są *przywiązane* do konkretnej ścieżki
w konkretnym systemie operacyjnym.  I nic tego nie zmieni (nawet
``virtualenv --relocatable``).  Problematyczne są również pliki binarne, które
w takim środowisku się znajdują.

Koniecznie, koniecznie wykorzystuj środowiska wirtualne w swoim projekcie,
jeśli jeszcze tego nie robisz.

#### Vagrant

O Vagrancie mówiłem na PyConie PL w 2012 roku [prezentacja].
W skrócie: ten program ułatwia automatyzację wirtualnych maszyn.  Po co komuś wirtualne maszyny?

Jeśli twój projekt to coś więcej niż aplikacja statycznego bloga, potrzebujesz
zapewne:

* systemu baz danych
* systemu cache'u
* innych rozwiązań nieściśle związanych z Pythonem

Wszystko to musisz albo zainstalować na swoim komputerze (i później żonglować
wersjami, jeśli pracujesz nad różnymi projektami), albo zainstalować na
wirtualnych maszynach, które będą służyły tylko do jednego celu.

Dlatego Vagrant jest tak bardzo przydatny.

Ale niestety wymaga konfiguracji provisionera, obecnie: Chef-solo, Puppet lub
Ansible (którego uwielbiamy, bo jest Pythonowy).

Jeśli Twój projekt rozwija się dynamicznie, Vagrant stanie się dla Ciebie
wybawieniem.

#### Pakiety systemowe

Hynek Schlawack napisał świetny artykuł [Python Application Deployment with Native Packages] [artykul] o instalowaniu aplikacji w środowiskach wirtualnych z pakietów
**.deb**.

Idea jest taka: tworzysz u siebie środowisko wirtualne, instalujesz do niego
swój projekt, a następnie pakujesz to wszystko do pakietu systemowego.

I wszystko byłoby fajnie, gdyby nie problemy z virtualenv'em.  O ile Hynek
najwyraźniej poradził sobie w przypadku deb-ów, o tyle rpm-y są bardzo
[problematyczne] (packaging a virtualenv: really not relocatable).

TL;DR: bardzo duże korzyści, ale bardzo dużo wysiłku (i hacków).  Raczej nie
musisz z tego korzystać, o ile nie masz farmy serwerów.


### Rozwiązania rodem z przyszłości

...ale niedalekiej.

#### wheels

``wheel`` to koło ratunkowe dla programistów.  Co to jest i z czym to zjeść?
Zacznę od końca: z najnowszymi ``setuptools`` (0.9+) i ``pip`` (1.4+).

Sam wheel to format instalacyjnych archiwów dla pakietów Pythona zaproponowany
w [PEP 427].

Gdy stworzysz wersję ``.whl`` swojego projektu, zainstaluje się on w mgnieniu
oka.  A jeśli będzie zawierał coś kompilowanego, to żadna ponowna kompilacja
nie będzie potrzebna.

Dzięki temu Pythonowe zależności binarne (*compilable*) będziesz mógł
zainstalować bez obecności kompilatora.  I, co równie ważne, będziesz mógł to
zrobić bardzo szybko.

Minusy?  Należy przygotować koła dla wszystkich wspieranych przez ciebie
platform (Ubuntu, Debian, Fedora, MacOSX, wersje 32b i 64b...).  No i wymgane
są dość "świeże" wersje ``setuptools`` oraz ``pip`` (dobra informacja: możesz
je łatwo zaktualizować ze środka virtualenv'a).

Bardzo pomocny jest artykuł Hynka Schlawacka ([Sharing Your Labor of Love:
PyPI Quick And Dirty] [artykul2]).

#### Linux containers i Docker

Docker to taki Vagrant, tylko nie dla maszyn wirtualnych, a dla kontenerów
w Linuksie.  Kontenery te to odchudzone maszyny wirtualne -- nie tylko zajmują
mniej miejsca, ale też wymagają mniej pamięci operacyjnej i mniej czasu
procesora.

Minusy?  Jest to rozwiązanie tak świeże i niesprawdzone, że może zawierać sporo
błędów.  Dodatkowo, aby odpalić Dockera na innych niż Linux systemach
operacyjnych konieczne jest zastosowanie... maszyny wirtualnej.  Na przykład
poprzez Vagranta.

Więcej informacji o Dockerze: https://www.docker.io/

Oficjalny tutorial: https://www.docker.io/gettingstarted/ (Getting started)

### Na koniec

Mam nadzieję, że przybliżyłem ci tematykę instalacji i deploymentu aplikacji
Pythonowych.  Liczę, że (jeśli tego jeszcze nie robiłeś) zaczniesz pisać
``setup.py`` dla swoich projektów i budować *wheele*, bo to jest standard
w świecie Pythona.


[prezentacja]: https://speakerdeck.com/pbanaszkiewicz/your-own-sandbox-thanks-to-vagrant
[artykul]: http://hynek.me/articles/python-app-deployment-with-native-packages/
[artykul2]: http://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
[problematyczne]: http://www.alexhudson.com/2013/05/24/packaging-a-virtualenv-really-not-relocatable/
[PEP 427]: http://www.python.org/dev/peps/pep-0427/
