# Testowanie mikroserwisów z Argo i Zalenium

### Maciej Brzozowski

## Wprowadzenie

W artykule zostaną przedstawione problemy i ich rozwiązania, które napotkaliśmy w projekcie zbudowanym w architekturze
mikroserwisów oraz bardzo wysokiej gęstości zmian i zastosowanych narzędzi, przyjrzymy się jak doszlśmy do zaawansowanej
automatyzacji. Tekst stanowi zarys tego, co zostanie pokazane na prezentacji. Po przeczytaniu tych kilku akapitów,
widzowi będzie dużo łatwiej zrozumieć, co właściwie dzieje się (wysokopoziomowo) na ekranie.

## Testowany produkt

Finalny produkt w założeniu ma pozwalać na przeszukiwanie przepastnych baz wiedzy w banku Nordea i umożliwienie
znalezienia źródeł potrzebnych informacji oraz uzyskanie dostępu do danych. Wszystko opakowane w piękny interfejs
i obsługiwane w prosty sposób.

### Technologia

Produkt łączy w sobie rozproszone aplikacje napisane w języku Scala oraz część graficzną napisaną z wykorzystaniem
frameworku AngularJS. Aplikacje komunikują się za pomocą protokołu HTTP oraz wykorzystują Kafkę jako kolejkę
komunikacyjną. Elementy budowane są za pomocą środowiska Bazel by w łatwy i szybki sposób skompilować różne technologie
do postaci obrazów Dockera oraz utworzyć potrzebne definicje zasobów dla środowiska zarządzania kontenerami
Openshift/Kubernetes. Do tego dochodzą systemy zewnętrze, do których system ma się zintegrować.

## Napotkany problem

Projekt składa się z dość sporej liczby rozproszonych serwisów, gdzie każdy z nich jest w postaci kontenera. Postawienie
całego systemu wraz z jego konfiguracją nie jest trywialnym zadaniem. W celu przetestowania systemu postanowiliśmy
skupić się na testowaniu tylko tych serwisów, które się ze sobą bezpośrednio komunikują jaki i już wystawionej
całej aplikacji. Opcja druga pozwala na sprawdzenie scenariuszy od końca do końca jak i potwierdzenia czy aktualny stan
konfiguracji jest należyty. Jako, że system docelowo znaduje się na platformie Openshift, testy od końca do końca
są rownież wykonywane na tej platformie. Przy takich testach wykorzystany jest gotowy sposób wystawiania systemu
przygotowany przez zespół DevOps. Po stronie testera leży tylko przygotowanie scenariuszy testowych. Natomiast 
w sytuacji kiedy testowane są powiązane serwisy występuje potrzeba przygotowania fragmentów systemu, gdzie występuje 
grupa powiązanych serwisów wraz z ich konfiguracjami. Tym razem tester musi przygotować środowisko testowe, w którym
możne zasymulować rożne przypadki testowe i oczywiście napisać scenariusze testowe, które sprawdzą interakcje pomiędzy
tymi serwisami. Nastała potrzeba wykorzystania narzędzia, które pomoże w zestawieniu grupy kontenerów. Nasuwającym się
remedium na taki problem jest zastosowanie Docker Compose, który szybko i prosto umożliwi zastawienie grupy kontenerów.
W praktyce zastosowanie Docker Compose wprowadza redundantny sposób utrzymania konfiguracji dla każdego serwisu,
gdyż występuje potrzeba przygotowania konfiguracji dla środowiska Openshift i Docker Compose. Docker Compose nie posiada
również możliwości budowania przepływów pracy. Postawione raz kontenery są skonfigurowane "na sztywno" i nie można 
symulować przypadków testowych w prosty sposób. Wystapiła potrzeba narzędzia, które pozwoli budować przepływy pracy 
oraz pozwoli na użycie gotowych już konfiguracji ze środowiska Openshift/Kubernetes. Odpowiedzią na zaistniały problem 
okazało się narzędzie o nazwie Argo, które pozwala na budowanie przepływów pracy w środowisku Kubernetes.

## Testowanie

Aplikacja testowana jest na różnych poziomach, począwszy od testów jednostkowych, systemowych i testach od końca do końca.
Testy jednostkowe są pisane przez programistów danej funkcji systemu. Testy systemowe i testy od końca do końca są pisane
przez testerów dedykowanych do projektu.

## Użyte narzędzia

Do testów jednostkowych wykorzystana jest biblioteka Scalatest, która jest naturalnym wyborem dla testów jednostkowych 
dla języka Scala. Dla wyższych poziomów testowania należało wybrać narzędzie, które umożliwi czytanie testów dla osób 
nietechnicznych i będzie w prosty sposób rozszerzalne - te założenia świetnie spełnia Robot Framework. Ze względów 
wymienionych w jednym z wcześniejszych akapitów do budowania przepływów pracy użyty został Argo. Dla przeglądarkowych 
testów graficznych oczywistym wyborym jest Selenium, lecz w tym przypadku postawiliśmy na projekt Zalenium, 
który rozszerza funkcje tego pierwszego.

### Robot Framework

Robot Framework jest oprogramowaniem napisanym w Pythonie, które umożliwia łatwą automatyzację zadań przy użyciu
tzw. keywordów, które pozwalają ułożyć kod w bloki proste do zrozumienia dla niewtajemniczonych w arkana
programistycznych czarów.

### Argo

Argo zaś jest narzędziem do budowania przepływów zadań i procesów w środowisku Kubernetes. Argo aranżuje przepływ pracy
w postaci kaskadowych kroków lub też acyklicznego grafu. Kazdy krok schematu jest osobnym kontenerem. Przy jego pomocy
udało się zbudować scenariusze testowe w docelowym środowisku (Openshift/Kubernetes), w którym dostarczana jest aplikacja.

### Zalenium

Jest to wyprodukowane przez Zalando rozszerzenie Selenium Grid, który pozwala zestawić wiele procesów automatycznych
testów Selenium w postaci kontenerów, na różnych przeglądarkach i z podglądem na żywo. Zalenium jest wykorzystywane
do testowania aplikacji od strony graficznej.

## Jak to zadziałało?

Wszystkie procesy wystawieniowe zostały zaprojektowane przy pomocy Argo. Wystarczyło do tego podjąć kilka dodatkowych 
kroków, w postaci uruchomienia obrazu Zalenium dla testów graficznych, puszczenia testów czy klonowania repozytorium
testowego. Po podaniu odpowiednich argumentów, wszystko wykonuje się samo. Testerowi pozostaje rozszerzanie pakietów
testowych i raportowanie defektów.

## Źródła

[Robot Framework](https://robotframework.org)

[Argo](https://argoproj.github.io)

[Selenium](https://www.seleniumhq.org)

[Zalenium](https://opensource.zalando.com/zalenium)

[Docker](https://www.docker.com)

[Docker Compose](https://docs.docker.com/compose)

[Openshift](https://www.openshift.com)

[Kubernetes](https://kubernetes.io)

[Scala](https://www.scala-lang.org)

[Scalatest](http://www.scalatest.org)

[AngularJS](https://angularjs.org)

[Kafka](https://kafka.apache.org)

[Bazel](https://bazel.build)
