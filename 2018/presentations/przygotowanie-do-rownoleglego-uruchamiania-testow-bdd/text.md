# Przygotowanie do równoległego uruchamiania testów BDD

## Behave Driven Development
W mojej ocenie projektowanie i napisanie frameworka do testów jest znacznie ciekawszym zadaniem niż implementacja kolejnej aplikacji webowej opartej na Django. Chcąc dostarczać oprogramowanie o najwyższej jakości, trzeba mieć dobrze napisane testy, które powinny trwać krótko i dać miarodajny wynik. Behave Driven Development mówi, aby zdefiniować pakiet testów przed implementacją funkcjonalności oraz zapewnić kanał komunikacji między osobami technicznymi i developerami w postaci języka Gherkin.

Przykład scenariusza testowego napisanego w Gherkinie:

```
Feature: Some terse yet descriptive text of what is desired
  In order to realize a named business value
  As an explicit system actor
  I want to gain some beneficial outcome which furthers the goal

  Scenario: Some determinable business situation
    Given some precondition
      And some other precondition
     When some action by the actor
      And some other action
      And yet another action
     Then some testable outcome is achieved
      And something else we can check happens too
```

Jest to zamknięta struktura, która pozwala nam zadeklarować kontekst testów (Given), przedstawić akcje (When, And, But) oraz wykonać asercję (sprawdzenie) oczekiwanego wyniku (Then). Bezpośrednim benefitem zamkniętej struktury scenariuszy testów jest możliwość kontroli statusu wykonanego scenariusza (na podstawie kroku w którym jesteśmy) oraz możliwości swobodnego dzielenia ich na grupy w zależności od tego, co chcemy z nimi zrobić.

## Architektura
Inicjacja testów jest krytycznie ważna. Architektura powinna być przemyślana w taki sam sposób jak testowana aplikacja. Chociaż było to bardzo dawno, to pamiętam jakby to było wczoraj - moje pierwsze kroki we frameworku Django. Wcześniej nie miałem styczności z frameworkami webowymi i pisałem kod wedle własnego uznania. Logika przemieszana z HTML-em i JavaScriptem w porównaniu z wzorcami narzuconymi przez Django - to było coś! Kiedy zobaczyłem testy Selenium napisane w Pythonie, które linia po linii wykonywały jakieś akcje w przeglądarce, wróciły koszmary z przeszłości. Scenariuszy testowych było bardzo dużo, a koszt utrzymania w porównaniu z zerową wartością biznesową był ogromny. Nieważne, ile masz napisanych testów - jeżeli ich nie uruchamiasz i nie analizujesz wyników, każda sekunda poświęcona na ich development jest czasem zmarnowanym. Dlatego uważam, że każdy moment jest dobry, aby zacząć od nowa. Taka też zapadła decyzja - wybór padł na framework do BDD python-behave.

## Dlaczego BDD
Podejście Behave Driven Development pozwala na wyeliminowanie luki komunikacyjnej między zespołem deweloperskim (dev, tester), a osobami nietechnicznymi (product owner, analityk biznesowy). Sama składnia Gherkin w teorii jest prosta i pozwala na pisanie scenariuszy nawet osobom nietechnicznym. W praktyce zauważyłem, że nie zawsze dla wszystkich jest ona oczywista i na pewno warto poczytać o niej trochę więcej niż jeden artykuł w internecie (w źródłach załączam ciekawe książki). Z pewnością scenariuszom napisanym w Gherkinie nie brakuje czytelności, która zapewni, że każdy członek zespołu będzie wiedział, o co w nich chodzi. To dotyczy nowych funkcjonalności. A co w przypadku gotowego systemu, do którego chcemy napisać (przepisać) nowe testy? Z pewnością trzeba zdefiniować kluczowe funkcjonalności oraz zadbać o najlepszy sposób raportowania pokrycia testami. Siłą rzeczy nie będziemy pisać testów przed funkcjonalnością, ale o ile mamy dokumentację i testy akceptacyjne, możemy posłużyć się nimi do napisania Gherkina, a później dać product ownerowi gotowe scenariusze do akceptacji. Framework behave wymaga trzymania się określonej konwencji, ale dopiero po wdrożeniu Page Object Pattern, nasze testy stały się bardzo łatwo utrzymywalne i przystępne dla każdego developera testów.

## Środowisko
W przypadku testów automatycznych kluczową rzeczą jest instancja, na której będą one uruchamiane. Aby uniknąć błędnych wniosków po uruchomieniu (false negative bądź false positive), powinno się zagwarantować aplikacji stabilne środowisko. Doskonałym pomysłem będzie więc jego pełna automatyzacja za pomocą narzędzi typu Docker czy Puppet. Jest to istotne zwłaszcza przy developmencie oraz podejściu continous deployment. Gdy wszyscy pracują na jednakowych instancjach, nie ma możliwości, że developer testów napisze kod, który będzie się zachowywał inaczej w zależności od środowiska. Instancja testowa (nie developerska) powinna być w maksymalny sposób zbliżona do produkcyjnej. Każda najmniejsza różnica może wpłynąć na wynik testów. Oczywiście, ze względu na koszty, to prawdopodobnie będzie niemożliwe. Jako alternatywę można stosować finalne uruchomienie testów na środowisku OAT, które powinno być najbliżej konfiguracji instancji produkcyjnej.

## Dane testowe
Testy nie mogą bazować na żadnych danych, które nie są przez nie sprawdzone. Dobrym przykładem są użytkownicy i ich dane logowania. O ile zdecydujemy się uruchamiać testy aplikacji, która ma dane i będzie ich miała coraz więcej, powinniśmy zawsze sprawdzić 100% fikstur, których zamierzamy użyć. To takie pisanie testów do testów. W przypadku użytkowników można użyć biblioteki requests, wysłać odpowiednie zapytania do systemu i zwalidować odpowiedź. To pozwoli na uniknięcie sytuacji, gdy testy zwrócą błąd przy samym końcu, bo jeden z użytkowników ma zmienione hasło.

## Stabilność testów
Testy muszą być niezależne. Wynik jednego testu nie może bazować na danych innego. Jest to kluczowe wymaganie, aby dojść do sedna prezentacji, czyli uruchamiania wielowątkowego. Nie należy także ignorować testów, które raz na kilka uruchomień zwracają błąd. Test, który losowo nie przechodzi, jest bugiem - powinno się go traktować w taki sam sposób jak bug na produkcji. Ignorowanie tego problemu może spowodować w dłuższym okresie brak poważnego traktowania wyników przez zespół, co w późniejszym etapie prognozuje ryzyko porzucenia ich dalszego rozwoju (brak wartości biznesowej). Testy powinny być tak samo wersjonowane jak aplikacja, aby można było w łatwy sposób użyć ich w przypadku hotfixów.

## Uruchamianie i raportowanie wyników
Test powinien bezpośrednio mówić, dlaczego nie przeszedł. W przypadku Selenium najczęściej spotykanym wyjątkiem jest “TimeoutException”. W wielu sytuacjach oznacza to coś innego, a wygląda podobnie. Każdy tego typu błąd powinien być przechwycony i zakomunikowany. Spotkałem się z podejściem, w którym poprzez automatyzację traktowano uruchamianie pojedynczych test case’ów napisanych przy wykorzystaniu Selenium. Uruchamianie testów i czekanie na ich wynik to marnowanie czasu. Uruchamianie testów lokalnie i praca nad czymś innym - to marnowanie zasobów. Testy powinny być uruchamiane zgodnie z określonym harmonogramem (przede wszystkim przed mergem), najlepiej codziennie na zewnętrznej instancji (CI), a nie na lokalnych komputerach! Nikt nie będzie ich traktował poważnie, skoro nie zawsze przechodzą. Nikt też nie będzie poważnie traktował wyników testów, które zostały uruchomione lokalnie.

## Podsumowanie
Aby osiągnąć zadowalający efekt przy pracy z testami, potrzebnych jest sporo różnych kompetencji. Zakres pracy wymaga od zespołu automatyzacji środowisk (devops), zaprojektowania architektury testów, konfiguracji Jenkinsa oraz narzędzi pomocniczych (dev) oraz stworzeniu scenariuszy testów (tester). Stabilny kod testów, gotowy do skalowalności, powinien posiadać:
* pozytywny, “zielony” build na Jenkinsie (testy zawsze przechodzą, gdy aplikacja działa poprawnie),
* zautomatyzowane środowiska uruchamiania testów,
* zautomatyzowane środowiska z aplikacją i danymi testowymi,
* brak wyników typu false negative/positive,
* opracowany, jasny i klarowny system raportowania i prezentowania wyników,
* niezależne scenariusze.

## Źródła:
* http://behave.readthedocs.io/en/latest/
* https://en.wikipedia.org/wiki/Behavior-driven_development
* https://en.wikipedia.org/wiki/Continuous_integration
* https://en.wikipedia.org/wiki/Operational_acceptance_testing
* http://selenium-python.readthedocs.io/
* http://docs.behat.org/en/v2.5/guides/1.gherkin.html
* BDD in Action - John Ferguson Smart
* Specification by Example: How Successful Teams Deliver the Right Software - Gojko Adzic
* Testuj oprogramowanie jak Google. Metody automatyzacji - James A. Whittaker, Jason Arbon, Jeff Carollo
