# Werkzeug - debugowanie aplikacji internetowych w sytuacjach ekstremalnych
## Marcin Karkocha

Opowieści o sytuacjach, kiedy wszystko działa aż do momentu wgrania tego na serwer produkcyjny, usłyszysz praktycznie od każdego programisty webowego. Jest to standard wykraczający poza bariery języków programowania. Istnieją jednak narzędzia, którymi możemy się wspomóc w takich momentach. Nieodłącznym pomocnikiem programisty języka Python będzie Werkzeug i jego interaktywna konsola błędów dla aplikacji webowych. Aby jednak z niej w pełni skorzystać, powinniśmy poznać biblioteki, które będą przydatne w pracy z nią, m.in. inspect oraz pytrace.

### Tak to się zaczęło

Jesteś dumny ze swojego kodu, właśnie skończyłeś pracować nad dużym modułem. Wszystko wydaje się działać dobrze, napisałeś sporo testów. Mógłbyś się tym wręcz chwalić, gdyż masz zarówno testy jednostkowe, jak i integracyjne. Osoby, które robiły przeglądy twojego kodu, chwaliły cię za zastosowane rozwiązania. Testerzy wielokrotnie zapewniali, że wszystko działa jak należy. Nadszedł moment, kiedy twój kod trafi na serwer produkcyjny, jesteś podniecony, ponieważ mówimy o bardzo ważnej funkcjonalności w serwisie, z którego korzysta dziennie kilkaset tysięcy ludzi. Dodatkowo w poniedziałek zaczyna się upragniony urlop. Kod trafia na produkcję, a testerzy siadają do sprawdzenia, czy wszystko jest w porządku. Niestety serwis nie działa, błąd wygląda jakby nie pochodził z naszego kodu, choć nic poza kodem nie uległo zmianie. Myślisz sobie: “no to po urlopie”.

Znasz ten scenariusz? Brzmi znajomo, prawda?
Niestety takich błędów nie możemy uniknąć, a jedynie minimalizować szanse na ich powstanie poprzez odpowiednie dobranie środowisk testowych itd.
Co jednak, kiedy pomimo dołożenia wszelkich starań na etapie powstawania kodu, opisana powyżej sytuacja ma miejsce?

Na ratunek programistom webowym pracującym w języku Python przychodzi Werkzeug wraz z jego interaktywną konsolą debugowania. Sam Werkzeug jest bardzo minimalistycznym narzędziem służącym do budowania aplikacji internetowych. Zbudowano na nim choćby micro-framework Flask. Nas jednak interesuje jedno z narzędzi, które wchodzą w skład Werkzeuga, a mianowicie debugger, który możemy podłączyć do dowolnej aplikacji działającej w oparciu o WSGI.

### Werkzeug - jak to właściwie działa

Zasada działania debuggera jest prosta. W sytuacji, kiedy włączamy go do aplikacji przy pomocy WSGI, tak naprawdę staje się on pośrednikiem między aplikacją a serwerem. Może zatem przejmować wszystkie informacje płynące z niej, a zatem i to co interesuje nas najbardziej, czyli błędy. Jako że staje się elementem środowiska uruchomieniowego aplikacji, to jest w stanie zbierać takie informacje jak stacktrace’y (na czym bazuje przecież idea debugowania post-mortem). Daje mu to również możliwość wysyłania do aplikacji komend, w naszym przypadku pisanych w Pythonie, które będą wykonywać się w kontekście aplikacji.

Na stronie z błędem wygenerowanej przez Werkzeug, mamy więc wyświetlony kompletny stacktrace, w którym możemy z dowolnego kroku na stosie wywołań wyciągnąć informacje o zmiennych środowiskowych i zacząć wykonywać własny kod przez konsolę w danym kontekście.

### Werkzeug i co dalej?

To tyle w temacie Werkzeuga, który sam z siebie jest niezwykle prostym narzędziem, co zresztą może sugerować jego kod, gdybyśmy się mu przyjrzeli.

Jednak to nie koniec możliwości, jakie ze sobą niesie. Możemy przecież używać innych bibliotek oferowanych przez bogate przecież środowisko paczek dla Pythona. Są w nim również narzędzia, które mogą przydać się w debugowaniu jak np. inspect, natto, pytrace.

Na początku biblioteki, które dostarczne są z samym Pythonem. Pierwsze z fajnych narzędzi to znajdująca się w bibliotece sys funkcja settrace, dzięki której możemy do wykonywanych na stosie wywołań operacji doczepić własną funkcję np. monitorującą przychodzące parametry, czy też zwracającą jakieś informacje w konkretnym przypadku.

Kolejne tym razem moduły, które dostajemy wraz z samym Pythonem, to code oraz inspect, które we współpracy ze sobą pozwalają nam na “bieganie” po kodzie. Czasami jest to bardzo przydatne. Możemy dzięki nim zajrzeć do dowolnego kawałka kodu w kontekście wywołania i, co najważniejsze, zmodyfikować go.

Następny użyteczny moduł to dis. Pozwala on zdemontować kod Pythona do operacji jednostkowych kodu bytowego.

Z przydatnych modułów dodatkowych znajdziemy np. natto, które pozwala nam zamienić na czytelną HTML’ową postać dowolny obiekt i zwizualizować w przejrzysty sposób jego stan. Wśród innych modułów znajdziemy także pytrace automatycznie monitorujący stan stosu wywołań i nagrywający ważne informacje z jego prac. Ostatnim z modułów, o którym chciałbym wspomnieć, jest zaś tiper, który pozwala nam na zrzucenie stanu stosu wywołań do wygodnej postaci, którą będziemy mogli zdebugować narzędziami zewnętrznymi, jak choćby pdb.

### O alternatywnych rozwiązaniach słów kilka

Spośród alternatywych narzędzi, z którymi miałem okazję się zapoznać, chciałbym krótko przedstawić dwa. Pierwszym z nich jest dobrze znany mi Django-pdb. Pozwala on na uruchomienie konsoli pdb na działającym serwerze django, gdy pojawi się błąd. Jest to również metoda debugowania typu post-mortem, nie jest jednak wygodna, gdy mówimy o środowisku produkcyjnym, choć na pewno nieco bezpieczniejsza niż Werkzeug. Uruchomienie tego narzędzia w serwisie, który działa na kilku serwerach, będzie wręcz niemożliwe, dlatego też w ekstremalnych przypadkach wolę jednak korzystać z debuggera Werkzeug. Drugie narzędzie godne uwagi, na które natrafiłem w trakcie przygotowań do prezentacji, to wdb. Jest to interaktywny debugger Pythona, który podobnie jak Werkzeug debugger, można wpiąć bezpośrednio jako aplikację WSGI obudowującą naszą aplikację. Za pomocą wdb możemy wykonywać różne typy debugowania. Radzi on sobie zarówno z post-mortem jak i remote debuggingiem. W stosunku do prezentowanego narzędzia ma on jednak, jak dla mnie, zbyt rozbudowany interfejs, z którego i tak przeważnie nie korzystam. Wydaje mi się, że warto rozważyć użycie wdb podczas pracy nad kodem, jednak w moim przypadku, do tego celu doskonale sprawdza się debugger dołączony do IDE.

Jest jeszcze jeden moduł o którym chciałbym jedynie wspomnieć: "pyrasite". Pozwala on na wstrzyknięcie dowolnego kodu uruchomionej aplikacji. Stanowi więc wartą rozważenia alternatywę dla Werkzeug'a jeśli ten zawodzi.

### Na co nie było miejsca

Zdecydowanie zbrakło mi miejsca na poruszenie spraw związanych z tym, jak wykorzystać debbuger Werkzeug. Możliwości jest wiele. Przykładowo próbowałem kiedyś pakować błąd do postaci spiklowanego obiektu, po czym odtworzyć go w osobnym środowisku już z wykorzystaniem Werkzeug. Fakt, iż aplikacja, która wygenerowała błąd, nie była webowa, a służyła raczej za zintegrowany system kontroli procesu agregacji danych.


Źródła:

* [http://werkzeug.pocoo.org/docs/debug/](http://werkzeug.pocoo.org/docs/debug/) “Dokumentacja Werkzeugowego Debuggera”
* [http://skillsmatter.com/podcast/scala/intro-to-python-debug](http://skillsmatter.com/podcast/scala/intro-to-python-debug) “Introduction to python debugging [video]”
* [https://pypi.python.org/pypi/natto/0.1.7](https://pypi.python.org/pypi/natto/0.1.7) “Narzędzie do wizualnego prezentowania stanu obiektu”
* [http://code.google.com/p/modwsgi/wiki/DebuggingTechniques](http://code.google.com/p/modwsgi/wiki/DebuggingTechniques) “Trochę ciekawych informacji o debugowaniu aplikacji internetowych”
* [http://pyrasite.readthedocs.org/en/latest/](http://pyrasite.readthedocs.org/en/latest/) “Code injection to running process”
* [https://pypi.python.org/pypi/django-pdb](https://pypi.python.org/pypi/django-pdb) “Django PDB - interaktywne debuggowania aplikacji django w terminalu”

