# Python w służbie jej królewskiej mości - czyli o parsowaniu stron i szpiegowaniu użytkowników słów kilka
## Marcin Karkocha

W jaki sposób śledzi się użytkowników w internecie? Co tak na prawdę wiedzą dostawcy internetu o naszej aktywności? Czy jesteśmy w internecie anonimowi a co najważniejsze bezpieczni?
Brzmi kontrowersyjnie, zapraszam na przegląd narzędzi służących analizie treści w tym wypadku znajdujących się w internecie w klimacie Jamesa Bonda.

### Dlaczego śledzimy użytkowników?

Zastanawiacie się pewnie o co chodzi mi z tym śledzeniem użytkowników w sieci, już śpieszę wyjaśnić. Pracowałem mianowcie w firmie która zajmowała się bezpieczeństwem sieci informatycznych w tym także analizą ruchu i treści w nim używanych.

Wciąż brzmi to przynajmniej kontrowersyjnie a wręcz hackersko? Po co jednak robi się takie rzeczy? W naszym wypadku w celu poprawienia bezpieczeństwa użytkownika w sieci.

Możecie więc zastanowić się jak dużo wiedzą o waszej aktywności inni i czy aby na pewno jesteście w internecie anonimowi. Możecie zastanowić się też czy skutecznym rozwiązaniem jest sieć Thor, podpowiem iż nie.  Na szczęście według prawa które póki co obowiązuje także te firmy dane są anonimizowane a połączenie ich z jakimkolwiek użytkownikiem pozbawionym osobowości służy jedynie obieraniu pewnych przypuszczeń ułatwiających pracę systemu w przyszłości.

Pewności jednak nigdy nie można mieć o czym świadczy choćby niedawno bardzo głośna afera z P.R.I.S.M-em w USA.

Wciąż nie jesteście wystraszeni? No to przyjrzyjmy się temu jak to się robi.

### Jak parsować strony internetowe?

W Pythonie dostajemy bardzo bogaty zestaw narzędzi do obróbki tekstu, xml'a czy html'a. Zacznijmy od biblioteki "re" i wyrażeń regularnych, które czasami są zwyczajnie niezastąpione. Przejdźmy dalej do bardziej zaawansowanych narzędzi, jak HtmlParser. Pozwala on na wychwycenie momentu przetwarzania konkretnego tag'a dokumentu html. Na tej podstawie możemy selektywnie zbierać wybrane informacje, np. tylko linki do obrazków pochodzących z znaczników <img/>. Następnie przyjrzyjmy się bibliotece BeautifulSoup, która jest bardzo potężnym narzędziem analizy dokumentów, oraz lxml (na bazie którego wspomniany BeautifulSoup może pracować). Inne narzędzia, które warto wymienić to: parslypy, htmltidy, xml2data oraz pyQuery (które działa zupełnie jak selektory w jQuery do wybierania informacji).

### Żeby było szybciej!

Mamy jak widać spory zbiór darmowych narzędzi, gotowych do użycia. Zastanówmy się zatem, którego narzędzia powinniśmy użyć, jeśli zależy nam na jak najlepszej wydajności. Podam tu przykład gdzie zastąpienie beautifulSoupa przez HtmlParser spowodowało spadek czasu trwania analizy z 6 sekund do zaledwie 7-8 milisekund. Prawda że takie liczby robią wrażenie?

Tu zawsze powinny pojawić się pytania, jakich danych potrzebujemy i jakiej potrzebujemy wydajności. Niektóre narzędzia świetnie poradzą sobie w tym, co chcemy robić, ale ich wydajność pozostawi sporo do życzenia. Inne zaś, okażą się toporne w użyciu i będą wymagały mnóstwa pracy z naszej strony, jednak wydajność będzie odpowiednia.

W przypadku wspomnianej już wcześniej selektywnej analizy pliku (czy też budowaniu statystyk na podstawie dokumentu), szczerze polecam narzędzie proste i wydajne - HtmlParser. Jeśli natomiast chcemy wybierać dane bardziej kompleksowo i zależy nam na ich strukturze - to świetnie sprawdzi się lxml lub inne narzędzia, działające na ideii xPatha. Z kolei do wybierania danych z określonych wierzchołków dokumentu, kiedy wydajność nie ma wielkiego znaczenia, z czystym sumieniem mogę polecić bibliotekę pyQuery. Ma ona bardzo przyjazny i prosty w użyciu interfejs.

### Ciekawostki

W ramach ciekawostek chciałbym przytoczyć dwa z przykładów które przygotowałem, aby zachęcić do zobaczenia całej prezentacji.

Pierwszy przykład dotyczy parsowania stron Sejmu oraz pewnego osobliwego znacznika, na który natknąłem się poddając je parsowaniu.

Przykład drugi natomiast, to popularna strona internetowa z przyrostkiem "tube" w nazwie, która przed analizą treści zabezpiecza się dodając uszkodzone bajty do zawartości strony.

### Podsumowanie

We właściwej prezentacji, poza wymienionymi narzędziami przybliżę też metody analizy danych. Przyjrzymy się również narzędziom, które pozowolą nam zrównoleglić proces analizy, czy też podzielić go na mniejsze zadania. Po za tym przytoczę sporo informacji o tym, co wiemy o użytkownikach internetu i co z tą wiedzą możemy zrobić. Mam nadzieje, że wciąż jesteście zaintrygowani.


* [http://www.crummy.com/software/BeautifulSoup](http://www.crummy.com/software/BeautifulSoup) - "Dokumentacja BeautifulSoupa [brzydka ale z przykładami]"
* [http://lxml.de/](http://lxml.de/) - "Strona lxmla a na niej dużo informacji o parsowaniu danych"
* [http://www.w3schools.com/xpath/](http://www.w3schools.com/xpath/) - "Mały tutorial do xPatha"
* [http://pythonhosted.org/pyquery/api.html](http://pythonhosted.org/pyquery/api.html) - "PyQuery czyli jak robić biblioteki przyjazne programiście"
