# Korzystanie z GPIO mikrokontrolerów

Dla osoby mającej doświadczenie w Pythonie rozpoczęcie pracy ze środowiskiem
MicroPython zwykle nie nastręcza problemów od strony programistycznej. Z
drugiej strony wymaga ona wiedzy elektronicznej w celu właściwego bezpiecznego
i skutecznego korzystania z GPIO. W tym artykule omówimy podstawowe techniki
związane z GPIO starając się jednocześnie odświeżyć podstawowe prawa fizyki
dotyczące elektroniki.

## GPIO jako wyjście

### Bezpośrednie zasilanie z GPIO

W przypadku elementów działających z małą mocą i wymagających niewielkich
napięć, takich jak pojedyncze diody LED możliwe jest zasilanie bezpośrednio z
pinu z ewentualnym zastosowaniem rezystora. Przykładowa sytuacja - próbujemy
zasilić niskoprądową diodę LED przy użyciu chipa ESP8266.

Podłączenie przedstawia ryc 1

![ryc. 1 Dioda z rezystorem ograniczającym](ryc1.svg)

Z dokumentacji
technicznej odczytujemy następujące parametry:

* Spadek napięcia diody 2,5 V
* Prąd diody: 2 mA
* Napięcie GPIO: 3,3 V
* Maksymalny prąd dla GPIO chipa: 12 mA

Ponieważ napięcie i maksymalny prąd jakiego jest w stanie dostarczyć GPIO są
większe od wymaganych przez diodę, możemy zasilić ją bezpośrednio. Aby dobrać
wielkość rezystora przypomnijmy sobie II prawo Kirchhoffa i prawo Ohma. Pierwsze
z nich mówi nam, że spadek napięcia na rezystorze musi wynieść tyle ile wynosi
różnica między napięciem na GPIO a spadkiem napięcia na diodzie. Prawo Ohma
określa zaś, że wartość opornika jest stosunkiem spadku
napięcia i natężenia prądu. Otrzymujemy wzór:

```
R = \frac{V_S - V_{LED}}{I}
```

Podstawiając wartości: 3,3V, 2,5V i 2mA otrzymujemy żądaną oporność 400Ω.
Możemy zatem użyć bliskiego tej wartości opornika 470Ω dostępnego w większości
zestawów.

Ostatnią wartością, którą warto policzyć jest jeszcze moc rezystora, którą
uzyskujemy ze znanego wzoru:

```
P = U \cdot I
```

Moc naszego rezystora w tym obwodzie wyniesie więc 1,6 mW. Jest to dużo mniej
niż maksymalna moc standardowych rezystorów wynosząca 250 mW, zatem moc
rezystora nie będzie stanowiła problemu.

#### Uwaga:

Prawo Ohma znajduje zastosowanie wyłącznie dla elementów takich jak
rezystory. Elementy półprzewodnikowe cechują się nieliniową zależnością między
napięciem a natężeniem prądu. Błędem byłoby stwierdzenie, że dioda z powyższego
przykładu ma 1,2 kΩ i oczekiwanie, że dla innych napięć dioda zachowa ten
stosunek U / I. Dioda pracować może tylko w wąskim zakresie napięcia. Poniżej
niego w ogóle nie włączy się, natomiast powyżej jej oporność gwałtownie
spadnie, co szybko doprowadzi do przepalenia.

### Tranzystor jako przełącznik

Wachlarz zastosowań tranzystorów w elektronice analogowej i cyfrowej jest
bardzo szeroki. My jednak skupimy się na jednym - wykorzystaniu tranzystora do
kontroli obwodu o wysokim natężeniu prądu przy pomocy znacznie niższego. W tym
celu zastosujemy konfigurację "wspólnego emitera":

![ryc. 2 Tranzystor NPN jako przełącznik diody](ryc2.svg)

W układzie tym w momencie, gdy pin znajduje się w stanie niskim, tranzystor
znajduje się w stanie zatkania - brak przewodnictwa między kolektorem a
emiterem. Gdy pin przejdzie w stan wysoki - tranzystor osiąga stan nasycenia -
prąd między kolektorem i emiterem przewodzony jest z minimalnym oporem.
Spróbujmy przy jego pomocy zasilić "żarówkę" LED na 12V o mocy 1,5 W.

Parametry:

* Wzmocnienie tranzystora: β = 200
* Maksymalny prąd kolektor-emiter: 1A
* Napięcie stanu nasyconego baza-emiter: 0.7 V

Mając daną moc i napięcie źródła światła możemy wyliczyć płynący przez nie prąd
jako 125 mA. Jest to również prąd kolektor-emiter.
Wymagany prąd baza-emiter wyniesie zatem 125 mA / 200 = 0,63 mA.
Stąd też przy zastosowaniu wzoru powyżej otrzymujemy oporność 4,73 kΩ.
Użyjemy zatem na bazie opornik o wartości 4,7 kΩ, który powinien nam
zagwarantować wymagany prąd baza-emiter jeśli pin GPIO przejdzie w stan wysoki
3,3V.


### Tranzystor a przekaźnik

Mimo że tranzystor i przekaźnik mogą spełniać podobną rolę w obwodzie, istnieje
między nimi duża różnica.
Przekaźnik przełącza styki mechanicznie przy pomocy elektromagnesu.
Tranzystor nie posiada elementów mechanicznych.
Jego działanie opiera się na technologii półprzewodnikowej.
Aby wybrać, która z tych opcji jest dla nas właściwa, należy rozważyć wady i
zalety obu rozwiązań.

### Zalety przekaźnika

* Może przewodzić zwykle prąd o znacznie wyższym natężeniu niż
  tranzystor.
* Może przewodzić zarówno prąd zmienny, jak i stały.
* Sposób zasilania cewki jest niezależny od tego, jaki prąd przez
  niego płynie, zatem obwód jest bardziej uniwersalny.

### Zalety tranzystora
* Ma o kilka rzędów wielkości mniejsze niż przekaźnik opóźnienie pomiędzy
  kontrolującym go sygnałem, a odpowiedzią.
* Ze względu na brak elementów mechanicznych, nie ulega zmęczeniu przy
  przełączaniu.
* Wymaga znacznie mniejszego prądu na bazie, niż przekaźnik do uruchomienia
  cewki.
* Jego praca jest bezgłośna.
* Nie posiadając elementów indukcyjnych nie wywołuje problemu samoindukcji w
  momencie wyłączenia (przekaźnik może wymagać zastosowania diody ochronnej,
  która pochłonie przepięcie).

Tak więc w sytuacji, gdy mamy do czynienia z prądem zmiennym, lub o dużym
natężeniu, wybierzemy przekaźnik. Podobnie, gdy nie znamy parametrów odbiornika
energii, który będzie kontrolowany. W przypadku sygnału wypełniającego (PWM)
musimy zastosować tranzystor ze względu na małe opóźnienie i zdolność do
wytrzymania licznych przełączeń. W wielu innych sytuacjach wybór pozostaje
kwestią priorytetów.

## GPIO jako wejście

### Rezystory podciągające

Piny niepodłączone mogą negatywnie wpływać na pracę mikrokontrolera.
Pełnią one role swego rodzaju anteny – zbierają zakłócenia cyfrowe(na przykład
silne szpilki sygnałowe). Taki stan pinu określamy w języku angielskim jako
*floating*.
Rezystory podciągające służą do uniknięcia zakłóceń cyfrowych, które mogą
prowadzić do nieprawidłowej pracy układu.
![ryc. 3 Zastosowanie rezystora podciągającego](ryc3.svg)
Na rycinie widzimy przykład pinu podciągniętego do stanu wysokiego przez
rezystor. Jeśli zewrzemy przełącznik, wysoka wartość rezystora sprawia,
że linia 3,3 V nie jest już w stanie ustalić stanu pinu na wysoki, gdyż jego
potencjał ustalany jest przez bazę. Stąd pin osiągnie stan niski.
Wartości rezystorów zależą od częstotliwości zmian stanów na linii.
Na przykład dla linii I2C należy stosować 4,7kOm, dla przycisków 10kOm

### Bouncing sygnału

Zbudowaliśmy już układ według powyższego schematu i postanowiliśmy
go przetestować. Napiszmy zatem prosty kod:

```
import machine

cur_value = 0
toggle_count = 0
pin = machine.Pin(5, machine.Pin.IN)

while True:
    value = pin.value()
    if value != cur_value:
        print(toggle_count)
        cur_value = value
        toggle count += 1
```

Ten prosty program ma nam zliczać kolejne zmiany stanu pina 16.
Teoretycznie licznik powinien wzrosnąć o 1 przy każdym wciśnięciu i zwolnieniu
przycisku. Czasem jednak obserwujemy, że wciśnięcie powoduje kilka zmian stanu
przycisku. Zjawisko to zwane po angielsku *bouncing* jest czymś normalnym na
mechanicznych stykach. Możemy wobec niego zastosować dwa podejścia.

#### Podejście hardware'owe

W tym podejściu stosujemy odpowiednią modyfikację obwodu. Najprostszym
rozwiązaniem jest zastosowanie tzw. układu RC składającego się z rezystora i
kondensatora.

![ryc. 4 Przycisk z układem RC](ryc4.svg)

Obwód ten różni się od poprzedniego obecnością dodatkowego rezystora i
kondensatora. Po zamknięciu przełącznika przejście pinu w stan wysoki zostanie
opóźnione do czasu naładowania się kondensatora. Wartości rezystora i
kondensatora należy dobrać doświadczalnie tak, aby wyeliminować *bouncing*
jednak by wprowadzone opóźnienie nie było zbyt wysokie.

#### Podejście software'owe

Zjawisko *bouncingu* możemy obsłużyć również software'owo. W tym celu
wprowadzamy stosowne opóźnienie w kodzie:

```
    import time
    # ...
        value = pin.value()
        if value != cur_value:
            time.sleep_ms(300)
    # ...
```

## Materiały internetowe

* http://www.electronics-tutorials.ws/ - wyczerpujące samouczki różnych
  zagadnień elektronicznych.
* https://learn.sparkfun.com/tutorials/ - samouczki nastawione na pracę
  z mikrokontrolerami
* http://micropython-on-wemos-d1-mini.readthedocs.io/en/latest/ - materiały
  ze szkolenia micropythonowego Radomira Dopieralskiego
* https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html
  - oficjalna dokumentacja micropythona na ESP 8266
