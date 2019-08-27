## Wprowadzenie

Świat enterprise to wielkie projekty, niezatapialne systemy bankowe, super wydajne platformy przetwarzające dane, znacznie więcej niż prosty sklep internetowy. Przez wiele lat świat ten był kojarzony tylko z językami silnie typowanymi, stabilność ma w nich kluczowe znaczenie. Teraz Python zyskał nową broń w walce o te super projekty - typy, nie takie “silne” ale potężne.

### Po co nam typy w wolnym świecie?

Python jest kojarzony z dużą swobodą. Możemy zrobić w nim wszystko, jak tylko nam się podoba. Jednak “Z wielką mocą wiąże się wielka odpowiedzialność”. Jeśli nasz system ma być rozwijany dłużej niż przez kilka dni, to warto skorzystać z typów i część tej odpowiedzialności zrzucić na automatyzacje. Unikniemy wtedy, znanego nam dobrze, dreszczyku emocji podczas aktualizowania produkcji. Poniższy błąd już nie pojawi się więcej w naszym monitoringu. 

    TypeError: list indices must be integers or slices, not str

Jednak tu nie chodzi tu tylko o samą stabilność. Kod, który korzysta z typowania, staje się dużo bardziej czytelny. Oczywiście nie na początku. Gdy po raz pierwszy spojrzałem na pełni typowany kod Pythona byłem przerażony. Nie byłem w stanie przeczytać co ten kod robi, tyle nowych składni, symboli, istna magia. Jednak, jak człowiek już się przyzwyczai, nie będzie powrotu. Kod z dobrym typowaniem staje się dużo przyjemniejszy do pracy. Kluczowe słowo “dobrym”. Przedstawię wam kilka zasad, jak dobrze wykorzystać typ w pythonie.

## Pierwsze kroki
### Typowanie funkcji

Zanim jednak przejdziemy do bardziej zaawansowanych tematów, zobaczmy jak wygląda typowanie. W pythonie 3.5 dostaliśmy możliwość dodawania adnotacji typów dla funkcji. 
    

    def greeting(name: str) -> str:
        return "Hello " + name

Za parametrem pojawił się dwukropek (`:`), za nim definiujemy właśnie typ. W tym przypadku jest to `str` czyli ciąg znaków. Typ wartości zwracanej możemy zdefiniować po strzałce `->`. Tu także mamy `str`.

### Typowanie zmiennych

Na samych definicjach funkcji świat się nie kończy. Dlatego też w Pythonie 3.6 dostaliśmy możliwość definiowania typów zmiennych. Składnia jest taka sama jak w przypadku argumentów funkcji. Python to przecież piękny i spójny język! 

    order_name: str = 'PyConPL!'
### Typy są leniwcami

Bardzo ważna rzecz, którą trzeba wiedzieć o typach, to że są to leniwe bestie. Same z siebie nie robią kompletnie nic. Dla uproszczenia możemy założyć, że intepreter Pythona zwyczajnie je ignoruje w czasie wykonywania kodu. Oznacza to, że możemy mieć całkowicie błędne typy i nie wpłynie to negatywnie naszą aplikację. To z jednej strony bardzo dobra wiadomość, dla osób, które chcą wdrożyć adnotacje typów w istniejącym projekcie, z drugiej jednak, może wprowadzać pewne zamieszanie ponieważ poniższy kod się wykona:

    def some_function() -> int:
        return "Hello!"
### Mypy

Jeżeli chcemy zweryfikować poprawność adnotacji musimy skorzystać z zewnętrznej biblioteki. Nie martwcie się, jest to oficjalna biblioteka i nie jest dostarczana jednocześnie z Pythonem, tylko ze względu na dynamiczny rozwój. Cały czas jest usprawniania, poprawiane są sporadyczne błędy i działa co raz szybciej. Instalujemy ją jak każdą inną bibliotekę:

    pip install mypy

Kiedy już zainstalujemy mypy możemy uruchomić komendę sprawdzającą nasz kod:

    ➜ mypy our_test_code.py
    our_test_code.py:2: error: Incompatible return value type (got "str", expected "int")

Dopiero uruchomienie `mypy` sprawdza poprawność naszych typów. W odpowiedzi dostajemy listę wszystkich błędów, które należy poprawić w naszym kodzie. Na całe szczęście otrzymujemy także podpowiedzi jakich typów powinniśmy byli użyć.

Ponieważ typy są leniwe, a jedyną metodą na ich weryfikacje jest uruchamianie mypy, dobrze jest włączyć to sprawdzanie w proces naszych testów. Możemy skonfigurować zarówno tox, jak i pytest do sprawdzania spójności typów za pomocą mypy.

## Jak żyć w zgodzie z typami
### Zbyt ogólne typy

Na początku korzystania z typowania w pythonie zaczęliśmy dodawać adnotacje do istniejącego kodu, bez wprowadzania większych modyfikacji. To oczywiście dobre podejście, nie chcemy robić dwóch rewolucji w kodzie w jednej chwili. Jednak popełniliśmy z tego powodu jeden znaczący błąd. W wielu przypadkach nasze typy wyglądały tak:

    def get(order_id: int) -> dict:
        ...

Co taki słownik, jako wartość zwracana, mówi nam o pobieranym elemencie? Poza tym, że to słownik, to niewiele. May dokładnie zero informacji o tym jakich kluczy możemy się spodziewać w tym słowniku. Nie wiemy jakie pola są wymagane, a jakie opcjonalne. Co gorsza, nie mamy także nad tym kontroli. W tym słowniku możemy dodać dowolny, błędy z punktu biznesowego, klucz i wszystko będzie “ok”.

Możemy poprawić czytelność tego kodu prostym zabiegiem. Wykorzystując alias

    from typing import Dict, Union
    Order = Dict[str, Union[int, str]]
        
    def get(order_id: int) -> Order:
        ...

Teraz na pierwszy rzut oka wiemy czego możemy się spodziewać po naszym słowniku. Powinien zawierać klucze i wartości związane z zamówieniem. “Powinien”, ale wcale nie musi. Alias zwiększył czytelność naszego kodu, ale nadal nie mamy kontroli nad tym co dokładnie znajduje się w naszym słowniku.
Zmierzamy powoli do pierwszego wniosku. Słownik nie jest najlepszym typem z jakiego możemy skorzystać. Jeżeli chcemy znacząco zwiększyć bezpieczeństwo naszej aplikacji powinniśmy skorzystać z konstrukcji, które mają sztywno określone pola, np klasy. Jednak tworzenie dużej ilości klas, tylko do przechowywania danych, w Pythonie nie jest należy do najprzyjemniejszych. Na szczęście mamy kilka ciekawych możliwości:

1. dataclasses - dostępne w standardowej bibliotece od pythona 3.7
2. attrs - zewnętrzna biblioteka, robi to co dataclasses, plus znacznie więcej
3. pydantic - kolejna biblioteka, jej zaletą jest wsparcie dla dataclasses

Zobaczmy jak będzie wyglądać nasz prosty kod z wykorzystaniem dataclasses:

    @dataclass
    class Order:
        id: int
        name: str
    
    def get(order_id: int) -> Order:
        ...

Definicja funkcji wygląda dokładnie tak samo, jednak tym razem zamiast słownika będziemy zwracać obiekty klasy Order. To już będzie wymagało od nas pewnych zmian w kodzie, jednak zyskujemy pewność co do pól dostępnych w naszym zamówieniu. Nie możemy niczego przez przypadek dodać, ani też zapomnieć o jednym z pól. Co jednak najprzyjemniejsze w codziennej praktyce, nie musimy przeszukiwać setek linijek kodu, żeby sprawdzić jak wygląda zamówienie.

### Dom dla aliasów

Aliasy nie sprawdziły się nam do uzyskania odpowiedniej kontroli przy zwracaniu złożonych danych. Zamiast aliasowanych słowników wykorzystaliśmy, lepsze, bardziej dopasowane do sytuacji klasy. Czy to oznacza, że aliasy są bezużyteczne? Nie! Aliasy są nam bardzo potrzebne i bez nich typowanie często byłoby męczarnią. Najlepszym przykładem są testy naszej aplikacji. 

Czy testy też powinny być typowane? Tak! Początkowo, w projekcie w którym zaczęliśmy dodawać typowanie, testy z nich nie korzystały. Jednak po pierwszym błędzie w testach, który spowodował problemy na produkcji, stwierdziliśmy jednogłośnie, że testy też powinny być typowane.

Wracając jednak do aliasów, wyobraźmy sobie fixture z pytest, które zwraca nam statyczne dane w formie prostych implementacji interfejsów domeny (więcej w temacie interfejsów domeny na mojej prezentacji). Zwracana wartość takiego fixture będzie wyglądać następująco:

    Tuple[IOrderRepository, IProductRepository, IClientRepository]

Mając kilkanaście testów korzystających z tego fixture stracimy jakąkolwiek widoczność tego co się dzieje.

    def test_add_product_increases_order_total_cost(
        prepare_repositories=Tuple[IOrderRepository, IProductRepository, IClientRepository]
    ) -> None:
        ....
    def test_add_product_increases_order_items_count(
        prepare_repositories=Tuple[IOrderRepository, IProductRepository, IClientRepository]
    ) -> None:
        ....

Niemal połowę deklaracji naszego testu zajmują typy. Korzystając z nich w taki sposób można się bardzo szybko zniechęcić. Jednak aliasy mogą uratować czytelność naszego kodu.

    StaticRepositories = Tuple[
        IOrderRepository, IProductRepository, IClientRepository
    ]
    
    def test_add_product_increases_order_total_cost(
        prepare_repositories=StaticRepositories
    ) -> None:
        ....
    def test_add_product_increases_order_items_count(
    prepare_repositories=StaticRepositories
    ) -> None:
        ....

Od razu lepiej! Aliasy świetnie się sprawdzają do poprawy czytelności naszego kodu. Nie tylko zajmuje on miej miejsca, ale staje się bardziej ekspresyjny, mówi sam za siebie.

### Z typami pod górkę

Wprowadzając typy do istniejącego, rozwijanego wiele lat projektu, możecie natknąć się z sytuacją, że napisanie dobrych adnotacji będzie bardzo trudne. To kolejna zaleta typowania! Przy każdym takim kawałku kodu powinna się wam zapalić czerwona lampka. To będzie alarm i jednocześnie znak, że czas na mały refactoring w tym miejscu. Wyobraźmy sobie typ zwracanej wartości tej “pięknej” funkcji:

    def book_meeting(customer_type):
        if customer_type == "regular":
            return {}
        elif customer_type == "vip":
            yield from (x for x in range(10))
        return None

Przy sześciu linijkach od razu widać, że ten kod jest straszny. Jednak, po 10 latach rozwijania projektu, zawsze znajdzie się taka magiczna funkcja, która ma 300 linii i efektywnie robi coś równie ohydnego jak powyższy przykład. Dzięki typowaniu, będziemy mogli łatwo namierzyć takie podejrzane, niezbyt rozsądnie zaplanowane fragmenty.

## Czy powinienem zacząć korzystać z typów w Pythonie?

Tak! Nie tylko poprawiają czytelność, ale także znacząco poprawiają stabilność naszego kodu. Jeśli będziemy rozwijać nasz projekt dłużej niż przez miesiąc, to warto.

## Źródła
[Mypy](https://mypy.readthedocs.io/)

[Pydantic](https://pydantic-docs.helpmanual.io/)

[Attrs](https://www.attrs.org/)

[migawka.it](http://migawka.it/)

