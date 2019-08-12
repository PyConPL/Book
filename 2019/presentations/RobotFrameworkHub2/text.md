## Wprowadzenie
W pracy nad kodem, który wykonuje się z tzw. ręki, to jest niesterowanym odgórnym systemem,
zespoły często napotykają problem powtarzania się. W dużej bazie funkcjonalności często dłużej trwa odnalezienie
istniejącej implementacji, niż stworzenie jej na nowo, stąd potrzeba użycia narzędzi indeksujących
i samotworzącej się dokumentacji, która "na żywo" będzie dostępnej dla każdego użytkownika wspólnego systemu.

## Napotkane problemy
### Robot Framework
Na początku całej drogi w zespole testowym, zdecydowaliśmy się wykorzystać Robot Framework, jako bazę do automatyzacji zadań testowych i ogólnie zadań pracowniczych.
Robot Framework cechuje się prostym składniowo podejściem do "programowania", w wyniku którego powstają - najlepiej rozczłonkowane - procedury, które są w prosty sposób zrozumiałe przez
użytkowników na ogół niezwiązanych z informatyką czy w ogóle językiem technicznym.

### Niespotykane przypadki użycia
Okazało się jednak, że użycie tego konkretnego frameworka generuje pewną potrzebę. Tą potrzebą jest tworzenie przybudówek do Robot Frameworka, związanych z tym,
że nikt wcześniej nie używał go konkretnie do implementacji zadań automatyzujących związanych z Apache Hadoopem,
Oozie, czy Hadoop File Systemem (HDFS).

### Nadaktywny zespół
Nasz zespół napotkał problem "pokusy" tworzenia kodu. Wynikało to z prostej zależności -- zatrudniliśmy masę fascynatów
programowania, po czym powiedzieliśmy im: nie programujcie. Skończyło się zniechęceniem, bo często i gęsto napotkane
problemy nie znajdowały ani gotowego rozwiązania (trudne do odnalezienia w dużej bazie kodu) ani implementacji 
(DRY - Don't Repeat Yourself).

### "Sprzedaż" rozwiązań reszcie firmy
Ten problem nasilił się wraz z pojawieniem się kolejnej potrzeby. Okazało się, że nasze narzędzia potrzebne są nie tylko w naszym zespole, 
ale również poza nim. Jak "sprzedać" to co mamy, skoro sami nie wiemy do końca co napisaliśmy? 
Taki stan rzeczy jest absolutnie nieakceptowalny w wysoce sformalizowanym otoczeniu, jakim jest bank.
Bezsilnie obserwowaliśmy, jak siostrzane zespoły tworzyły podobne rozwiązania, tracąc zasoby na rzecz powtarzania wykonanej już pracy.

## Robot Framework Hub
### Poprzednie próby rozwiązań
Próbowaliśmy wielu usprawnień, zaczynając od oczywistej - tworzenia dokumentacji. Nie zawsze był jednak czas, by ją uaktualniać; nie zawsze był czas by ją czytać.
Podjęliśmy się organizacji spotkań międzyprojektowych i międzyzespołowych, ale nie każdy miał ochotę w nich uczestniczyć i nie zawsze poruszany był akurat ten temat, 
który zapobiegłby tworzeniu istniejących rozwiązań. Wtem, jeden z kolegów zaprezentował nam Robot Framework Hub.

### Hub
To oprogramowanie open source autorstwa Bryana Oakleya z Oklahomy. Brayan Oakley stworzył dość proste
w założeniu narzędzie, które analizowało bazę kodu, otrzymaną na wejściu i wyciągało z tej bazy 
wszystkie funkcje z bibliotek w pythonie i Robot Frameworku.
Wyciągnięte funkcje są analizowane pod kątem dokumentacji i treści, a z zebranych danych tworzona jest prosta witryna internetowa,
wzorowana na oryginalnej dokumentacji Robot Framework.

Wydawałoby się, że rozwiązało to wszystkie problemy, aż do momentu, kiedy w użytkownicy zaczęli zgłaszać błędy w witrynie.
Wiele bibliotek nie zostało odczytanych i brakowało dokumentacji. Wróciliśmy w dużej mierze do punktu wyjścia.

Niestety, okazało się, że Bryan Oakley zarzucił projekt 3 lata temu i to w stanie niezgodności z najnowszą wersją Pythona
-- Pythonem 3. Z tego powodu biblioteki korzystające z wielu udogodnień nowej wersji naszego ulubionego języka programowania, 
nie były odczytywalne przez RF Hub.


## Robot Framework Hub... 2?
### Po co to zrobiliśmy?
Sprawa stała się poważna, mieliśmy gotowe rozwiązanie, które nic nam nie daje. Zdecydowaliśmy sie na naprawę, ale nasze
podejścia nie były satysfakcjonujące, a to kłopoty z wystawieniem aplikacji, a to jakaś biblioteka się buntowała. Wtedy
naszedł nas inny pomysł: trzeba ukierunkować niezaspokajalną potrzebę rozwijania aplikacji u naszych kolegów. Dwóch zdecydowało się na
implementację rozwiązania i udostępnienie go open source dla wszystkich użytkowników Robot Frameworka.

### Dlaczego Python 3?
Wybór platformy był dość oczywisty, padło na Python 3, gdyż jest to główny język używany w naszym środowisku. Tworzenie rozwiązania w poprzednim Pythonie
nie miałoby sensu, bo to już istnieje. Tworzenie go w innym języku niż Python byłoby niecelowe, bo Robot Framework jest głównie narzędziem Pythonowym.

### Ukierunkowana nadaktywność
Ukierunkowaliśmy nadaktywność recenzentów i twórców oprogramowania w kierunku stworzenia konkretnego narzędzia. Uznaliśmy to
za dobry kierunek jeśli chodzi o celowość (potrzebne w naszej firmie), "marketing" (konkretne rozwiązanie, którym możemy się chwalić na GitHubie)
i zabawę (po prostu fajnie jest coś takiego stworzyć).

### Zastosowane rozwiązania
Chcieliśmy, żeby aplikacja była zaprojektowana zgodnie z wszelkimi dobrymi zasadami, więc zaimplementowaliśmy ORM, przy użyciu
SQL Alchemy, co pozwala na szybką i bezpieczną komunikację aplikacji z bazą danych, co usprawnia proces zapisywania i usuwania danych z bazy.
Ponadto możliwe jest skorzystanie z innej, niż domyślna baza danych w postaci SQLite. 
PostgreSQL, MySql, Sql Server czy Oracle wymagają jedynie doinstalowania odpowiednich sterowników i podania likalizacji bazy dnaych. 
Sercem aplikacji jest framework FastAPI, będący obecnie jednym z najszybszych pythonowych frameworków tego typu, 
dodatkowo serwującym interaktywną dokumentację w standardzie OpenAPI, znaną wcześniej jako Swagger.
Aplikację docelowo stawiamy jako kontener dockerowy, co pomaga w restarcie i łatwym rozpowszechnianiu tego narzędzia.
Cały projekt używa też TravisCI, żeby umożliwić szybkie i celne testowanie modułów i integracji między nimi.
Nowa wersja programu również wykorzystuje izolację zadań: część odpowiedzialna za API, komunikację z bazą danych i frontend,
działa niezależnie od modułu obsługujecego analizę bazy kodu i wysyłki danych do aplikacji. 
Z drobnych usprawnień, można również nie uwazględniać podstawowych bibliotek Robot Frameworka, żeby nie zaśmiecać dużej bazy
dodatkowymi, znanymi wszystkim bibliotekami, dodawać nowe biblioteki bez potrzeby usuwania starych, a takze aktualizację danych poprzez API.


## Źródła
[Robot Framework](https://robotframework.org/)

[Fast Api](https://fastapi.tiangolo.com/)

[SQL Alchemy](https://docs.sqlalchemy.org/en/13/)

[Repozytorium Github RFHUB](https://github.com/boakley/robotframework-hub)

[Repozytorium GitHub RFHUB2](https://github.com/pbylicki/rfhub2)

[DRY Principle - wiki](https://pl.wikipedia.org/wiki/DRY)

