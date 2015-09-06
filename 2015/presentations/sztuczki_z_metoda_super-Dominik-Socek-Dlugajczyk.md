# Temat: Sztuczki z metodą super()
# Autor: Dominik "Socek" Długajczyk
Jest jedna funkcjonalność Pythona, której wszyscy używają bardzo często, acz szczątkowo, gdyż panuje opinia iż nadużywanie jej może doprowadzić do nieokreślonego działania aplikacji. Tą funkcjonalnością jest wielodziedziczenie. Postaram się w kilku słowach pokazać jak działa "Method Resolution Order" w Pythonie (wybaczcie, nie znalazłem dobrego tłumaczenia tej nazwy). Postaram się wam pokazać jak można użyć "super()", aby zamockować i przetestować przykładową klasę.

Zacznijmy jednak od teorii. W programowaniu panuje przekonanie, że wielodziedziczenie jest złe, gdyż może występować "the diamond problem", czyli sytuacja, w której klasa dziedziczy po dwóch klasach, a te dwie klasy dziedziczą po jednej i tej samej. Gdybyśmy w takiej sytuacji (powiedzmy w C++) we wszystkich klasach zaimplementowali taką samą metodę, to język nie wiedziałby w jakiej kolejności wykonać dane metody.  W W Pythonie ten problem nie występuje dzięki algorytmowi "C3 linearization", który został wykorzystany do implementacji MRO.*. Wprowadzono go w wersji 2.3 (new style classes) oraz w językach Perl 5 i Parrot. Niestety nie są znane mi inne języki, które by implementowały ten algorytm.

Dodatkowym atutem Pythona jest fakt, iż wywołanie metody rodzica, jest jawne w metodzie potomka. Dzięki temu, można kod rodzica uruchomić nie tylko przed wywołaniem własnej metody, ale na przykład w środku. Daje nam to większą władzę oraz naprawdę duże pole do manewru.
![graph.new.png](graph.new.png)

Weźmy pod uwagę tą specyficzną sytuację (wyciągniętą z jednego mojego projektu). Jest to hierarchia dziedziczenia jednej klasy i jej rodziców. Liczby w nawiasach określają numerek w liście wywołania, który dostajemy dzięki MRO.

OrdersListController dziedziczy po Controller. Tutaj jest jeszcze wszystko zrozumiałe. Jednak Controller dziedziczy już po 4 klasach (w kolejności):
 * Requestable
 * FanstaticController
 * FormskitController
 * FlashMessageController

Tutaj wprawdzie jest już zastosowane dziedziczenie po wielu klasach bazowych, jednak MRO w takiej sytuacji jeszcze nie pokazuje swoich możliwości. To co dzieje się głębiej już jest sednem użycia "C3 linearization". FlashMessageController jest 5. w kolejności, co kończy listę bezpośrednich rodziców klasy Controller. To, że BaseController ma numerek 6 wymaga już niestety trochę większego zastanowienia. Nie będę się nawet starał tłumaczyć czemu akurat tak to zostało obliczone (gdyż ten temat bardzo dobrze opisał na swojej prelekcji Raymond Hettinger, twórca implementacji MRO. Prelekcja nazywa się "Super considered super!"*).
![graph.new.png](graph.new.png)

Tym diagramem chciałem natomiast pokazać, iż w Pythonie nie występuje "the diamond problem". Jest jeszcze jedna bardzo ważna cecha tego algorytmu: dziecko nigdy nie wie która metoda zostanie wykonana, gdy użyjemy super(). Zwróćcie proszę uwagę na klasę FanstaticController (z numerkiem 3). Dziedziczy ona jedynie po klasie BaseController, a nic nie wie o klasie FormskitController (z numerkiem 4), która będzie wykonana zaraz po niej. Jest tak tylko dlatego, że klasa Controller dziedziczy po tych dwóch klasach.

Ta konkretna funkcjonalność daje nam bardzo ciekawą możliwość. Mieliście kiedyś problem o nazwie "jak zmockować funkcję super()?". Czyli w testach chcecie wykonać kod z jednej klasy, ale nie chcecie wykonywać kodu rodziców. Można to zrobić bardzo prosto: wybierzmy klasę do testów, w tym przypadku "OrdersListController". Następnie tworzymy klasę MockedOrderListController, która będzie dziedziczyłą po tych samych klasach co OrderListController. A następnie robimy pustą klasę OrdersListControllerEx, która dziedziczy po OrdersListController oraz MockedOrderListController (w tej kolejności). Dzięki czemu najpierw zostanie wykonana metoda z klasy OrdersListController, a potem MockedOrderListController. W samym MockedOrderListController po prostu nie wywołujemy metody super(), dzięki czemu nie zostanie wykonany żaden kod rodziców.

Niestety taka sztuczka ma sens tylko w testach, gdyż wtedy wiemy dokładnie jaką klasę blokujemy i jak MRO się zachowa (oraz jak struktura się zmienii). Jeśli byśmy chcieli jeszcze raz podziedziczyć po wielu klasach, to hierarchia MRO może ulec zmianie i nasz kod przestanie działać. Tak samo nie możemy zablokować kodu konkretnej klasy w hierarchii, już nie mówiąc o tym, że trzeba by przepisać wszystkie te klasy, po których nasza klasa będzie dziedziczona, aby zmienić strukturę dziedziczenia (co jest niewykonalne, gdyż nigdy nie wiemy co będzie dziedziczyło po naszej klasie).

Wiedząc to wszystko bardzo łatwo będzie nam teraz zrozumieć po co w argumentach metody super trzeba podać aktualną klasę oraz aktualny obiekt. Czyli:

```super(OrdersListController, self)```

Pierwszym argument jest miejsce w liście MRO, drugie jest to obiekt od której lista się zaczyna. Na przykład: "self" może być typu OrdersListController, jeśli stworzyliśmy obiekt tej klasy, natomiast jeśli zrobiliśmy klasę która tylko dziedziczy po OrdersListController, to self będzie typu tej nowej klasy. Dlatego użycie super w tej formie nie ma sensu:
```super(self.__class__, OrderListController)```

Zauważyłem jakiś czas temu, że bardzo często używam super() na początku każdej metody. Chciałem zatem zrobić dekorator @superme, który by wykonywał super za mnie. Nie udało mi się to, gdyż dekoratory działają w dość prosty sposób. Dekoratory jest to funkcja, która bierze funkcję i zwraca inną funkcję. Jeśli zrobimy dekorator na metodzie, to w klasie wyciągniemy tę metodę i wystawimy nową. Jeśli spróbujemy w tej nowej funkcji użyć super, to wszystko powinno grać. Jeśli natomiast spróbujemy użyć super na metodzie, której rodzic ma metodę pod dekoratorem, to używając super nie dostaniemy naszej upragnionej metody, lecz funkcję zwróconą przez dekorator. Czyli mając coś takiego:

```
def superme(fun):
    def wrapper(*args, **kwargs):
        return fun(*args, **kwargs)
    return wrapper


class One(object):

    @superme
    def method(self):
        pass


class Two(One):

    def method(self):
        print(super(Two, self).method)

Two().method()
```

Wklasie Two.method, pod super().method nie dostaniemy One.method, tylko coś w rodzaju: "<bound method Two.wrapper of <__main__.Two object at 0x7f2116f7b048>" Mając Two.method albo One.method, możemy dostać się do klasy w której ta metoda została zdefiniowana. Mając już klasę, możemy użyć metody super(), gdyż mamy pełną listę MRO (dzięki self), oraz miejsce w hierarchii (dzięki klasie). Mając funkcję wrapper nie jesteśmy w stanie (a przynajmniej ja nie znam sposobu) dostać się do klasy, na której ten wrapper został założony.

Jak widzicie tutaj, funkcjonalność metody super() nie jest taka prosta jak może się wydawać, jednak trzeba ją poznać i zrozumieć, aby nie strzelić sobie w stopę przy jej użyciu. Mam nadzieję, że tym artykułem zachęciłem was do głębszego poznania wielokrotnego dziedziczenia i eksperymentowania z tą częścią języka Python.

## Źródła
* https://en.wikipedia.org/wiki/C3_linearization
* https://www.youtube.com/watch?v=EiOglTERPEo
