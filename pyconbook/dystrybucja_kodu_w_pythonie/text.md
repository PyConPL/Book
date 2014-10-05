# Dystrybucja kodu w Pythonie
## Radosław Jankiewicz

Napisanie kodu nie jest ostatnim krokiem w procesie tworzenia oprogramowania.
W celu dostarczenia wytworzonego kodu wymagane jest przystosowanie go do postaci, ułatwiającej jego publikację czy instalację w docelowym środowisku.
W tym celu w Pythonie istnieje ustandaryzowany system dystrybucji wspierany przez zestaw narzędzi zawarty częściowo w bibliotece standardowej, a częściowo w postaci dodatkowych modułów.
Umożliwia on dystrybucję wykonanego kodu w postaci reużywalnych paczek, które można swobodnie opublikować w otwartym repozytorium paczek - PyPI (Python Package Index).
Omawiana prelekcja poruszać będzie zarówno proces tworzenia jak i publikacji paczek kodu w Pythonie.

### Tworzenie paczki kodu

Podstawową reużywalną jednostką w Pythonie jest moduł, który można zaimportować za pomocą wbudowanego systemu importów.
Jest to po prostu plik o rozszerzeniu .py zawierający kod napisany w Pythonie.

    Plik:
        my_module.py

    Zawartość pliku:
        def my_function():
            pass

    Instrukcja importowania funkcji z modułu:
        >>> from my_module import my_function

Moduły można z kolei grupować w paczki, które reprezentowane są przez katalogi.
Warunkiem, żeby katalog był interpretowany jako paczka jest umieszczenie w nim pliku o nazwie __init__.py.

    Struktura plików
     my_package/
       |-- __init__.py
       |-- my_module.py

    Instrukcja importowania funkcji z modułu z paczki:
        >>> from my_package.my_module import my_function


Z punktu widzenia interpretera - paczka również jest modułem, który zawiera dodatkowo atrybut __path__ przechowujący listę fizycznych ścieżek w systemie plików pod którymi przeszukiwane są moduły należące do tej paczki.
Mechanizm ten umożliwia tworzenie wspólnej przestrzeni nazw dla modułów znajdujących się fizycznie pod różnymi ścieżkami (namespace packages).
Można dzięki temu podzielić większy projekt na mniejsze paczki, pozwalając na dystrybuowanie tylko tej części z nich, która jest aktualnie wymagana.
Pozwala to również na powtórne wykorzystanie nazwy paczki, która była już wcześniej zajęta.


    Struktura plików
        my_package/
          |-- __init__.py
          |-- core
            |-- __init__.py
            |-- my_module.py


        my_package/
          |-- __init__.py
          |-- utils
            |-- __init__.py
            |-- my_module.py

    Instrukcja importowania funkcji z modułu z paczki:
        >>> from my_package.core.my_module import my_function
        >>> from my_package.utils.next_module import some_function

    Zawartość pliku my_package/__init__.py:
        from pkgutil import extend_path
        __path__ = extend_path(__path__, __name__)



### Dystrybucja paczek

W chwili obecnej współistnieje kilka narzędzi dających możliwość zarządzania dystrybucjami kodu w Pythonie:
  - distutils - jest to podstawowe narzędzie umożliwiające tworzenie dystrybucji oraz instalację paczek. Jest to moduł należący do biblioteki standardowej.
  - setuptools - biblioteka, która powstała jako rozszerzenie distutils (przez monkey-patching), niwelując jego ograniczenia oraz rozszerzając m.in. o możliwość tworzenia dystrybucji binarnych w postaci python eggs.
  - distribute - biblioteka, która powstała jako fork setuptools i miała na celu przyspieszyć rozwój tego narzędzia. Obecnie nie jest już rozwijana - została wmerge'owana z powrotem do setuptools.     
  - distutils2 - kolejna biblioteka będąca rozszerzeniem distutils. Główną zmianą, którą ze sobą niesie jest zastąpienie wykonywalnego kodu Pythona z pliku setup.py przez konfigurację statyczną w pliku setup.cfg. W planach było włączenie jej do biblioteki standardowej w Pythonie 3.3 pod nazwą packaging, jednak ostatecznie tak się nie stało.  

Żeby przygotować najprostszą dystrybucję należy stworzyć plik o nazwie setup.py, który zawierać będzie wywołanie funkcji setup (zaimportowanej z modułu distutils.core) z podstawowymi informacjami o paczce (takimi jak nazwa paczki, numer wersji, czy nazwy paczek zależnych, które mają być automatycznie zainstalowane).

    Struktura plików:
        example_dir/
          |-- setup.py
          |-- my_package
            |-- __init__.py
            |-- my_module.py


    Zawartość pliku setup.py:
        from distutils.core import setup
        setup(
            name='my_package',
            version='1.0',
            packages=['my_package',],
        )

Tak przygotowany skrypt setup.py można wywołać z jednym z poleceń w celu przygotowania dystrybucji:
  - `sdist` - generuje dystrybucję źródłową, która zawiera kod w postaci nieskompilowanej
  - `bdist_egg` - generuje dystrybucję binarną zbudowaną w postaci pliku python egg, która zawiera skompilowany kod, jest to dystrybucja nieprzenośna
  - `bdist_rpm`, `bdist_wininst`, `bdist_dumb` - inne przykładowe rodzaje dystrybucji binarnych
  - `bdist_wheel` (wymaga zainstalowania dodatkowej paczki - wheel - oraz setuptools w wersji >= 0.8.0) - dystrybucja binarna (podobnie jak egg - jest to archiwum zip) spełniająca założenia opisane w PEP-376 oraz PEP-427 - standaryzujące proces instalacji paczek. 

Standardowo dystrybucja przygotowana za pomocą distutils będzie zawierała pliki:
  - wszystkie paczki, moduły, skrypty i rozszerzenia C zadeklarowane w pliku setup.py
  - pliki o nazwie pasującej do wzorca: test/test*.py
  - pliki README, README.txt, setup.py i setup.cfg

W przypadku pozostałych zasobów, które powinny zostać zawarte w dystrybucji - należy je zadeklarować w pliku MANIFEST.in.
Przykładowy plik MANIFEST.in może mieć postać:

    include *.txt
    recursive-include examples *.txt *.py


### Repozytorium paczek

Po przygotowaniu dystrybucji przyszedł czas na jej udostępnienie.
Publiczne repozytorium paczek - PyPI (Python Package Index), znane dawniej jako Cheeseshop zawiera ogromną liczbę paczek możliwych do zainstalowania za pomocą menedżerów pakietów takich jak pip czy easy_install, a ponadto umożliwia publikację własnych paczek wraz z zestawem meta-danych je opisujących.
Jedynym warunkiem jest posiadanie konta w tym serwisie.
Publikację paczki w PyPI można wykonać w prosty sposób przy użyciu opisywanych powyżej narzędzi np. za pomocą polecenia:

    python ./setup.py register

Po zarejestrowaniu można wypychać kolejne wersje paczki za pomocą polecenia:

    python ./setup.py sdist upload

Podczas publikowania własnych dystrybucji należy starannie ją opisać za pomocą klasyfikatorów umożliwiających skuteczne wyszukanie jej przez potencjalnych użytkowników.  
Za pomocą narzędzi takich jak np. chishop, czy devpi można postawić własne repozytorium paczek dla prywatnych projektów lub kopie zapasową PyPI stanowiącą zabezpieczenie przed niedostępnością publicznego repozytorium. 


### Bezpieczeństwo

Pobranie paczki z publicznego repozytorium wiąże się z zaufaniem wobec jej autora.
Jednak nawet przy założeniu, że paczka, którą chcemy pobrać jest bezpieczna - należy wziąć pod uwagę zagrożenie potencjalnym atakiem, w którym atakujący będzie próbował dostarczyć zamiast żądanej paczki - własną, zawierającą niebezpieczny kod, który jest wykonywany podczas jej instalacji.
Z dwóch najpopularniejszych menedżerów pakietów - easy_install i pip - tylko ten drugi (i to dopiero od niedawna - od wersji 1.3) stosuje weryfikację certyfikatu ssl.
Co prawda domyślnie sprawdzana jest zgodność sumy kontrolnej MD5, jednak nie należy tego traktować jako zabezpieczenia przed sfałszowaniem ściąganego pliku, a ma zapobiegać jedynie przed jego uszkodzeniem podczas transportu.
W celu weryfikacji źródła paczki należy sprawdzić jej podpis pgp, co jednak może być dosyć problematyczne, gdyż tylko znikoma liczba paczek jest podpisana a ponadto żadne z popularnych narzędzi nie wspiera automatycznej weryfikacji podpisów.  
Należy więc być świadomym zagrożenia związanego z pobieraniem pakietów z publicznego repozytorium przy użyciu tych narzędzi. 


* [http://pythonista.net/blog/2012/paczkujemy-i-dystrybuujemy-cz-1](http://pythonista.net/blog/2012/paczkujemy-i-dystrybuujemy-cz-1)
* [http://www.mxm.dk/2008/02/python-eggs-simple-introduction.html](http://www.mxm.dk/2008/02/python-eggs-simple-introduction.html)
* [https://pypi.python.org/pypi](https://pypi.python.org/pypi)
* [http://guide.python-distribute.org/](http://guide.python-distribute.org/)
* [http://wheel.readthedocs.org/en/latest/](http://wheel.readthedocs.org/en/latest/)
* [http://www.python.org/dev/peps/pep-0427/](http://www.python.org/dev/peps/pep-0427/)
* [http://www.davidfischer.name/2012/05/signing-and-verifying-python-packages-with-pgp/](http://www.davidfischer.name/2012/05/signing-and-verifying-python-packages-with-pgp/)
