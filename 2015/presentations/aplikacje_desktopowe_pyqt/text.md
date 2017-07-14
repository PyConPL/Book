# Aplikacje desktopowe z PyQt -  Piotr Maliński

## O co chodzi z Qt i PyQt?

Qt to potężna platforma do tworzenia aplikacji z graficznym interfejsem użytkownika. Możliwości wykorzystania Qt są bardzo duże. Możemy tworzyć aplikacje desktopowe na komputery działające pod kontrolą MS Windows, Linuksa, czy OSX. Możemy też tworzyć aplikacje na niektóre urządzenia mobilne (czy bardziej - systemy wbudowane), automaty z ekranami (dotykowymi), czy systemy digital signage i wiele więcej.

Programista Pythona ma do dyspozycji PyQt - interfejs Qt udostępniony w Pythonie. Dzięki temu możemy tworzyć aplikacje desktopowe w Pythonie bez konieczności użycia C++. Jako że pisanie prostych aplikacji w PyQt jest bardzo szybkie i łatwe, biblioteka ta może bardzo się przydać w codziennej pracy programisty jako narzędzie do tworzenia aplikacji pomocniczych. W prezentacji zajmę się zaprezentowaniem możliwych zastosowań PyQt - nie tylko dla twórców aplikacji desktopowych.

Qt i PyQt dostępne są na dwóch licencjach - GPL dla aplikacji na licencji GPL oraz płatnej, komercyjnej licencji dla aplikacji komercyjnych. Na licencji LGPL dostępna jest biblioteka PySide - interfejs biblioteki Qt zapoczątkowany przez Nokię. Niestety rozwój PySide pozostaje nieco w tyle za PyQt. W chwili pisania artykułu nie ma nadal wersji dla Qt 5 (gdzie Qt 4 nie jest już za bardzo wspierana).


## Skąd wziąć PyQt?

Na Linuksie pakiety Qt i PyQt będą dostępne w repozytorium dystrybucji. W zależności od dystrybucji pakiety mogą być mocno rozbite. W przypadku MS Windows i OSX możemy zainstalować całe SDK Qt, a następnie pasującą [paczkę PyQt][1] (dostępne są dla różnych wersji Pythona) ze strony projektu. PyQt działa zarówno z Pythonem 2 jak i 3.

Oprócz samej biblioteki mamy do dyspozycji szereg aplikacji, które mogą być przydatne. Qt Creator to IDE dla programistów Qt. Nie wspiera ono bezpośrednio Pythona i jeżeli interesuje Cię tylko Python, to Qt Creator nie jest potrzebny. Qt Designer natomiast będzie potrzebny, ta aplikacja służy do tworzenia interfejsu - rozmieszczania poszczególnych widżetów, nazywania ich i konfigurowania wyglądu. Qt Designer będzie jako oddzielny pakiet, lub razem z paczką SDK/Qt Creatorem.

Od strony Pythona potrzebne będą: `pyuic` i `pyrcc`. W przypadku rodziny Ubuntu, czy Debiana aplikacje te dostępne są w pakiecie - pyqt4-dev-tools, czy pyqt5-dev-tools. `pyuic` używamy do kompilowania interfejsów z Qt Designera do klas Pythona, natomiast `pyrcc` odpowiada za kompilowanie plików-zasobników plików statycznych (np. własnych ikon używanych w interfejsie aplikacji). To, plus sama biblioteka PyQt, wystarczy do tworzenia aplikacji.


## Jak zabrać się za programowanie w PyQt?

Tworząc aplikację z PyQt zaczynamy zazwyczaj od narysowania interfejsu w Qt Designerze. W bardzo prostych aplikacjach interfejs można stworzyć z poziomu kodu aplikacji. Mając interfejs bierzemy się za łączenie sygnałów wysyłanych przez widżety (np. kliknięto, strona została załadowała) ze slotami - metodami w naszej klasie, które będą implementować logikę aplikacji (jak kliknięto przycisk, to zrób coś).

Podstawą programowania z PyQt4 czy PyQt5 jest [Class Reference][1] - jest to lista wszystkich klas widżetów i innych obiektów z biblioteki Qt. Pokazuje ona, w jakim module znajduje się dana klasa i, co ważniejsze, opisuje wszystkie gettery, settery i sygnały używane przez widżet. Cała logika widżetu jest ładnie widoczna, np. zwykły przycisk QPushButton ma metodę text(), do pobrania tekstu znajdującego się na przycisku. Do zmiany tego tekstu możemy użyć metody setText(). Gdy przycisk zostanie kliknięty, wyemituje on sygnał "clicked". Pod taki sygnał podpinamy własną logikę i gotowe (w pewnym uproszczeniu).

Na rynku znajdziemy też co najmniej kilka książek (w tym kilka dostępnych już otwarcie w sieci [3], [4]), szczególnie tych anglojęzycznych. Większość z nich opisuje starszą wersję biblioteki - PyQt4. W porównaniu do PyQt5, na chwilę obecną, dużych zmian nie ma. Zmieniły się moduły, z których importujemy klasy, a także dodano np. prostszą metodę łączenia sygnałów ze slotami. Tak więc mając książkę do PyQt4 można sporo z niej wykorzystać programując z PyQt5. Do tego znajdziemy w sieci sporo artykułów i poradników poświęconych PyQt. Ta biblioteka jest dość popularna i nie ma problemu ze znalezieniem osoby, która jej używa.


## Pierwsza aplikacja

Zacznijmy od aplikacji bez oddzielnie rysowanego interfejsu. Oto prosty przykład z widżetem QWebView - widżetem okna przeglądarki. Widżet ten posiada metodę `load()`, która przyjmuje adres URL i ładuje go tak, jak w normalnej przeglądarce:

    import sys

    from PyQt5.QtCore import QUrl
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebKitWidgets import QWebView

    app = QApplication(sys.argv)

    web = QWebView()
    web.load(QUrl("http://pl.pycon.org/2015/agenda.html"))
    web.show()

    sys.exit(app.exec_())

Wszystko poza QWebView można uznać za boilerplate takiej prostej aplikacji - importy i zainicjalizowanie QApplication. Odpalenie tego kodu otworzy okno, w którym załaduje się agenda PyCon PL.

W bardziej praktycznych przypadkach będziemy mieć kilka widżetów, będziemy chcieli je rozmieścić, ponazywać, czy upiększyć. Wtedy Qt Designer będzie nieodzowny. Jako prosty przykład - otwórz Qt Designer, wybierz Widget jako bazę twojego interfejsu, a następnie przeciągnij na niego przycisk (Push Button). Gdy zaznaczysz przycisk po prawej stronie, pojawią się jego ustawienia - nazwa (objectName) i ustawienia wyglądu tekstu. Ja swój nazwałem `closeButton` i zapisałem całość jako `close.ui`. Następnie skompilowałem interfejs do klasy Pythona:

    pyuic5 close.ui > close.py

Mając klasę interfejsu można ją wykorzystać. Oto boilerplate dla takiego przypadku:

    import sys
    from PyQt5 import QtWidgets

    from close import Ui_Form


    class MyForm(QtWidgets.QWidget):
        def __init__(self, parent=None):
            QtWidgets.QWidget.__init__(self, parent)
            self.ui = Ui_Form()
            self.ui.setupUi(self)


    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        myapp = MyForm()
        myapp.show()
        sys.exit(app.exec_())

Z pliku close.py importujemy nasz widget. Nie zmieniałem jego nazwy, więc domyślna to Ui_Form. Ten kod odpali nasz interfejs, ale nic się nie stanie, gdy klikniemy w przycisk. Musimy połączyć sygnał (kliknięcia) ze slotem:

    class MyForm(QtWidgets.QWidget):
        def __init__(self, parent=None):
            QtWidgets.QWidget.__init__(self, parent)
            self.ui = Ui_Form()
            self.ui.setupUi(self)

            self.ui.closeButton.clicked.connect(self._close)

        def _close(self):
            print('zamykam')
            self.close()

Oto prosty przykład obsługi sygnałów i slotów. Po kliknięciu przycisku `closeButton` odpali się nasz slot - `_close`, który wykona swoją logikę.


## Dystrybucja aplikacji PyQt

Aplikacje napisane z pomocą PyQt mogą bez problemu działać na popularnych desktopowych systemach operacyjnych, ale będą też wymagać zainstalowania całego środowiska developerskiego. Na szczęście da się "zamrozić" nasze aplikacje do wersji niezależnej - czy to za pomocą py2exe, czy py2app. W przypadku systemu Windows nieduża aplikacja wraz z dołączonymi bibliotekami Pythona i PyQt da co najmniej 10-15 MB aplikację.

Od pewnego czasu istnieje także pyqtdeploy - aplikacja do dystrybucji aplikacji PyQt na Windows, Linuksa, OSX, a także Androida i iOS. Jeżeli interesuje was Tizen (Maemo), czy Sailfish OS, to PyQt jest też tam obecne. Także Windows RT / Windows Phone 8, czy Blackberry 10 / QNX są listowane jako wspierane. Niemniej w przypadku systemów mobilnych nie wszystko musi być dostępne, czy działać tak samo jak w wersji desktopowej (szczególnie wygląd interfejsu).

PyQt dostępna jest też na Raspberry Pi i praktycznie każdym innym mini komputerze na płytce. Takie zestawienie może przydać się, gdy tworzymy rozwiązania digital signage, czy automaty z graficznym interfejsem wystawianym użytkownikowi.


## Konkurencja

PyQt, czy wspomniane PySide nie są jedynymi bibliotekami do tworzenia aplikacji z graficznym interfejsem. W bibliotece standardowej Pythona znajdziemy `tk` - znacznie prostszą bibliotekę, której interfejs graficzny może wyglądać nie za ciekawie,  niemniej jest dostępna i działa. Z zewnętrznych bibliotek mamy też PyGTK, wxPython i Pythoncard, czy biblioteki bardziej wyspecjalizowane jak PyGame, czy Kivy.

Jak dla mnie, PyQt jest bardzo dobrą biblioteką i dlatego jakiś czas temu wybrałem ją zamiast innych. Przenośność między platformami, czytelny sposób programowania, czy spora grupa programistów pracujących nad rozwojem Qt to duże atuty. Niemniej Twój projekt może mieć wymagania, które lepiej spełnić może inna biblioteka.


## Co dalej?

Qt i PyQt implementują znacznie więcej niż widżety interfejsu. Dostajemy np. obsługę wątków, dostęp do baz danych, do usług systemowych jak drukowanie i wiele więcej. Do tego kod powinien być przenośny pomiędzy różnymi systemami operacyjnymi, więc możliwości są duże - czy to w ramach tworzenia prostych aplikacji pomocniczych, czy po większe projekty desktopowych aplikacji. Zobacz, jakie klasy są dostępne na Class Reference, a przekonasz się, jaki zbiór funkcjonalności ukryty jest w PyQt.

Jeżeli biblioteka ta zainteresowała Ciebie, to zacznij od przerobienia kilku prostych aplikacji, zapoznaj się z podstawowymi widżetami i sposobem ich działania. Zrób prosty edytor tekstowy, prostą przeglądarkę i temu podobne. W sieci znajdziesz sporo pomocnych materiałów, a w księgarniach kilka książek. Lista dyskusyjna PyQt też oferuje szybką i skuteczną pomoc. Na [mojej stronie][5] znajdziesz wiele poradników do PyQt4 (w miarę możliwości będę aktualizował je do PyQt5).

* [1] Strona PyQt https://www.riverbankcomputing.com/software/pyqt/intro
* [2] Class Reference PyQt5 http://pyqt.sourceforge.net/Docs/PyQt5/class_reference.html
* [3] Rapid GUI Programming with Python and Qt http://www.qtrac.eu/pyqtbook.html
* [4] GUI Programming with Python: QT Edition https://www.commandprompt.com/community/pyqt/
* [5] Poradniki PyQt4 http://www.python.rk.edu.pl/w/p/pyqt/
