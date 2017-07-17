# Co mają wspólnego trzęsienia ziemi, cyklon tropikalny, lawiny błotne i nasze repozytoria? - Paweł Kopka

Co łączy repozytoria, trzęsienia ziemi, lawiny błotne oraz cyklony tropikalne? Pewnie większości z
was przychodzi do głowy słowo "katastrofa", ale dzisiaj nie o tym. Odpowiedź na otwierające pytanie to:
rozkłady odwrotnie potęgowe. Nie są tak "popularne" jak rozkład normalny, ale też wypełnianiają znaczącą
przestrzeń w naszym świecie.

## Rozkład odwrotnie potęgowy

Rozkłady odwrotnie potęgowe, czasem znane jako rozkłady Pareto lub Riemann Zeta, można opisać
dość prostym wzorem $f(x) = c/x^a$. Oczywiście charakteryzują się one pewnymi założeniami
(takimi jak x nie może równać się zero), ale nie warto się w nie zagłębiać. W wielkim skrócie ten
rozkład mówi, że małe zdarzenia zdarzają się znacznie częściej niż wielkie. Świetnym przykładem
jest badanie Pareto, który interesował się zamożnością ludzi. Opisywał rozkład dóbr wśród społeczeństwa,
a, jak można się domyślać, dużo więcej ludzi posiada mały dobytek, natomiast maleńka część
społeczeństwa posiada dużo dłuższe ciągi zer na kontach. Jako ciekawostkę można dodać, że z tych
badań powstała zasada Pareto, która mówi, że 20% populacji posiada 80% bogactwa. To nam mówi jaka
jest skala różnicy między ilością dóbr na początku rozkładu, a w jego ogonie.

## Przykłady

Nasza ulubiona Wikipedia prezentuje wiele przykładów występowania rozkładów odwrotnie potęgowych
z wielu dziedzin. Można zacząć od słowa, a dokładnie od częstotliwości jego występowania w długich
tekstach. Jeśli policzymy ile razy pojawiają się poszczególne słowa i wyznaczymy histogram, to
zobaczymy, że jego kształt będzie przypominał nasze rozkłady odwrotnie potęgowe. Przykładami z
astronomii oraz geologii są meteoryty oraz ziarenka piasku. W świecie finansów jest to wielkość
odszkodowań ubezpieczyciela za wypadki komunikacyjne. Kto wie, może z użyciem tych rozkładów liczone
są nasze składki OC i AC. Jako przykład bliższy tematyce PyCona możemy podać wielkość plików przesyłanych
protokołem TCP. W tytułowym pytaniu wyliczone zostały przykłady z dziedziny geofizyki, która obfituje
w rozkłady odwrotnie potęgowe.
Przykłady rozkładów odwrotnie potęgowych stosowanych w geofizyce przedstawiono w [1].
Cyklony tropikalne, a raczej ich energia, jak wszystkie wcześniej wymienione
zjawiska, charakteryzuje się tym, że duże zdarzają się bardzo rzadko. Myślę, że mieszkańcy Hawajów
bardzo cieszą się z tego powodu. Pewnie to również wpływa na niewielką migrację ludzi z miejsc zagrożonych.
Podobnie jest z lawinami błotnymi. Jednak najlepszym przykładem rozkładów odwrotnie potęgowych są trzęsienia ziemi.
Przesuwające się płyty tektoniczne podczas zmian w naprężeniach dość często uwalniają  energię.
Niemniej jednak są to zjawiska nieodczuwalne dla człowieka ze względu na ich wielkość. Jednak czasem głęboko
pod ziemią występują zdarzenia o ogromnej energii powodujące fale sejsmiczne, które wywołują trzęsienia ziemi
oraz inne katastrofy, takie jak tsunami. Pewnie każdy słyszał, jak wielkie zniszczenia niosą ze sobą takie zjawiska.
Może dlatego też wielu naukowców próbuje zrozumieć ich działanie lub też wyliczyć prawdopodobieństwo ich wystąpienia.
Rozkładem odwrotnie potęgowym możemy opisać stosunek energii wydarzenia sejsmicznego do częstości jego występowania, który wiąże
się z bardzo dobrze znanym prawem Gutenberga-Richtera, co widać na wzorze oraz wykresach. W 2002 roku udało się
dość dobrze wyznaczyć wykładnik dla trzęsień ziemi, którego wartość wynosi blisko a=1,63. Co ciekawe, dla tego
zjawiska jest też drugi przykład rozkładu odwrotnie potęgowego, czyli czasy między trzęsieniami ziemi. Jest to
związane z prawem Omoriego, które mówi, że trzęsienia ziemi potrafią wywoływać kolejne trzęsienia ziemi, tak zwane "aftershock".

## A co z tymi repozytoriami?

Od razu warto odnieść się do świetnego mówcy Gary'ego Bernhardta, który w swoim wystąpieniu [2]
 pokazał rozkład potęgowy w dziedzinie programowania, co jednocześnie przyczyniło się do
powstania tego tekstu i prezentacji na konferencji PyCon PL. Jako że wszystko w Pythonie jest obiektem, to spójrzmy
na klasy oraz ich najczęściej występujące elementy, takie jak metody i atrybuty. Tym sposobem mamy już
dwa rozkłady potęgowe, oczywiście, jeśli weźmiemy dość duże repozytoria, np. Django, Sphinx. Pewnie ciężko
to sobie wyobrazić na pierwszy rzut oka. Teraz zajrzyjcie w&nbsp;głąb swojej duszy... albo po prostu spójrzcie
na swoje projekty; jak często tworzycie obiekty z większą liczbą metod niż 10, 20 albo 30? Prawdopodobnie
niezbyt często, głównie dlatego, że jednak lepszą praktyką jest rozbijanie na mniejsze komponenty dla zachowania czytelności kodu.
Dlatego też liczba klas z kilkoma metodami jest znacznie większa. Jak widać, dobre praktyki pisania kodu
spychają nas w stronę rozkładów odwrotnie potęgowych [3]. Warto zauważyć, że tym razem nie jest to żadna katastrofa.

## Może troszkę kodu

Najlepsze przykłady to te, które mamy przed oczami. I właśnie tutaj mamy taki przypadek, możemy policzyć
liczbę wystąpień poszczególnych słów, a później wyznaczyć histogram dla tych zliczeń. Poniżej znajduje się
kilka linii kodu, które robią to z wykorzystaniem uwielbianej przez naukowców biblioteki matplotlib. Aby było
bardziej realistycznie, statystyki nie są całkiem dokładne.


```python
import matplotlib.pyplot as plt

file_name = 'opis.md'
with open(file_name, 'r') as f:
    data = f.read()
data = filter(lambda c: c.isalpha() or c.isspace(), data)
list_words = data.lower().split(' ')
count_words = {}
for word in list_words:
    if word not in count_words:
        count_words[word] = 0
        count_words[word] += 1
plt.hist(count_words.values(), 100)
plt.show()
```

Sporą dawkę wiedzy oraz specjalistów od rozkładów odwrotnie potęgowych można
znaleźć w Zakładzie Geofizyki Teoretycznej (Instytut Geofizyki Polskiej
Akademii Nauk) [4].
A po konferencji PyCon PL pojawi się projekt liczący rozkłady dla repozytoriów
projektów pisanych w języku Python [5].

## Bibliografia

1. Anna Deluca, Álvaro Corral. Fitting and goodness-of-fit test of non-truncated and truncated power-law distributions. Acta Geophysica. 61(6), (2013)
2. Gary Bernhardt. The Unix Chainsaw. Cascadia Ruby Conference, Seattle, WA, USA, 29-30 czerwca 2011
3. Richard Wheeldon, Steve Counsell. Power Law Distributions in Class Relationships.
4. \hyphenatedurl{http://www.igf.edu.pl/geofizyki-teoretycznej.php}
5. \hyphenatedurl{https://github.com/pawelkopka}
