#Aplikacje webowe dla początkujących - Python 3 i Pyramid web framework - Marcin Lulek

Krótkie wprowadzenie do tworzenia aplikacji internetowych w
Pythonie 3 oraz frameworku Pyramid. W trakcie warsztatu będziemy
implementowali aplikację typu blog.
Pod koniec uczestnicy posiądą podstawową wiedzę z zakresu tworzenia
szablonów, pracy z bazą danych, routingu, logiki biznesowej (widoków),
uwierzytelnienia użytkowników oraz uprawnień do zasobów.

Dodatkowo wykorzystamy biblioteki do sprawdzania danych formularzy
oraz biblioteki do stronicowania wpisów w naszym blogu.

## Podstawowe założenia odnośnie bibliotek użytych podczas warsztatów

* Użyjemy SQLAlchemy jako warstwę ORM
* Szablony Mako będą odpowiadały za wygenerowanie kodu HTML
* Routing logiki biznesowej będzie realizowany za pomocą mechanizmu URL Dispatch
* Za stronicowanie danych będzie odpowiedzialna biblioteka webhelpers2
* Tworzenie i sprawdzenie poprawności formularzy będzie obsłużone przez bibliotekę WTForms


## Plan warsztatów

### Wstęp

Punktem wyjścia będzie użycie standardowego szkieletu aplikacji `alchemy`
a w końcowym efekcie uzyskamy małą aplikacja o strukturze pozwalającej
rozwinięcie w pełnoprawną aplikację o strukturze przyjaznej rozwojowi aplikacji.

### Modele danych

Poznamy SQLAlchemy ORM i stworzmy podstawowe obiekty reprezentujące naszego bloga,
dodamy "serwisy" zajmujące się wyszukaniem pozczególnych wierszy:

* Dowiemy się jak SQLAlchemy zarządza transakcjami w bazie oraz sesjami
* Utworzymy modele danych
* Zaktualizujemy skrypt tworzący naszą bazę danych oraz domyślne dane


### Routing oraz podstawowe widoki aplikacji

Czas połączyć bazę z naszą aplikacją w logiczną całość.

* Stworzymy podstawowe ścieżki URL po których nasza aplikacja będzie zwracała rożne odpowiedzi
* Stworzymy widoki powiązane z tymi ścieżkami
* W widokach utworzymy logikę biznesową powiązaną z naszymi modelami danych
* Dodamy formularze oraz walidację danych POST w widokach do tworzenia i edycji wpisów na blogu

### Uwierzytelnianie i uprawnienia

Mamy już w pełni działającą aplikację ale każdy może zmieniać i tworzyć nowe wpisy na naszym blogu. Najwyższy czas
wprowadzić uwierzytelnianie użytkowników oraz sprawdzane uprawnień do zasobów.

* Wprowadzimy mechanizm logowania i uwierzytelniania odwiedzających za pomocą `auth_tkt`
* Sprawdzimy uprawnienia do wykonania operacji na stronie przez prostą implementację ACL dla zalogowanych użytkowników.
