# Google Translate tu nie pomoże!
## Łukasz Taczuk

Załóżmy, że mamy przed sobą skompilowany program w postaci pliku exe. Po jego uruchomieniu okazuje się, że wszystkie widoczne teksty są w języku greckim, albo chińskim. Teoretycznie, w celu nauczenia się obsługi programu, jesteśmy skazani zapamiętanie wszystkich "szlaczków" albo (jak to często ludzie robią) na nieporęczne zerkanie na zrzuty ekranu z dodanymi napisami, które wyjaśniają do czego służy dany przycisk. Na szczęście to nieprawda! Nie dość, że jesteśmy w stanie przetłumaczyć występujące w programie ciągi znaków, to proces ten możemy całkowicie zautomatyzować na wypadek wydania nowszej wersji programu. Wystarczy odrobina wiedzy na temat plików wykonywalnych i szczypta niekonwencjonalnego myślenia.

### Ale po kolei

Tekst wyświetlany na ekranie, czy to w programie czy grze może pochodzić z wielu źródeł. Niektóre gry posiadają pliki zapisane w wewnętrznym formacie, w których znajdują się kwestie wypowiadane przez bohaterów. Tak samo programy mogą pobierać tytuły okien, teksty na przyciskach i wartości pól tekstowych z plików przygotowanych przez twórców, dopiero po uruchomieniu aplikacji.
W tym przypadku, aby uzyskać inną wersję językową, wystarczy jedynie otworzyć taki plik, dokonać zmian i zapisać przetłumaczone ciągi znaków. Trudność takich zmian zależy jednak od konkretnego programu – niektóre pliki zawierają treść zapisaną otwartym tekstem, inne będą wymagać zaawansowanej inżynierii wstecznej programu, celem ustalenia formatu zapisu. Ten sposób tłumaczenia wykracza jednak poza zakres tego artykułu.

Drugim źródłem treści są zasoby pliku wykonywalnego (Resources). Są to binarne dane, które mogą zostać dołączone do pliku wykonywalnego w Windows. W szczególności zasobami mogą być okna dialogowe (wraz z całą ich zawartością, czyli napisami) lub po prostu ciągi znaków.

Trzecim źródłem i zarazem tym, na którym najbardziej będzie się skupiać artykuł, są ciągi znaków umieszczone bezpośrednio w kodzie źródłowym programu i skompilowane wraz z kodem do postaci wykonywalnej.


### Zasoby

Charakterystyczną cechą zasobów jest fakt, że każdy zasób, który jest identyfikowany po swoim numerze identyfikacyjnym może posiadać wiele wersji, po jednej na każdy język naturalny. W momencie uzyskiwania dostępu do konkretnego zasobu, udostępniany jest ten, który pasuje do języka Systemu Operacyjnego. Dzięki temu, jeden program może wyświetlać informacje w wielu językach, odpowiednio dobranych dla użytkownika.


Do modyfikowania zasobów umieszczonych wraz z plikiem .exe, można użyć specjalnie stworzonych w tym celu gotowych edytorów. Efekt jaki chcemy uzyskać to możliwość automatycznego tłumaczenia aplikacji z minimalnym udziałem ludzkim. Poszukiwany edytor powinien zatem móc być używany w trybie batch oraz nie powinien powodować efektów ubocznych, takich jak lekka zmiana wyglądu okien dialogowych (niektórym edytorom zdarza się zmieniać, na przykład czcionkę, co jest kuriozalne). Dodatkowo, najlepiej będzie jeśli edytor będzie dostępny za darmo.
Programem, który spełnia wszystkie powyższe punkty jest Resource Hacker i za jego pomocą będą przeprowadzane operacje tłumaczenia zasobów.

Operacja zautomatyzowanego tłumaczenia przebiega w wielu etapach.
Na początku, na podstawie oryginalnego pliku .exe, generowany jest plik .rc. Jest to plik, który opisuje wygląd oraz zawartość, między innymi, okien dialogowych. Jego zawartość jest zapisana otwartym tekstem, co daje nam możliwość łatwego jej modyfikowania.

	ResHacker.exe -extract original.exe , resource_orig.rc ,,,

Zawartość tego pliku musi następnie zostać przeanalizowana pod kątem występujących w nim ciągów znaków. Znalezione ciągi są potem zrzucane do pliku, który będzie robił za słownik.

Po uzyskaniu pliku-słownika następuje jedyny etap, w którym wymagany jest element ludzki – tłumaczenie. Zawartość pliku musi zostać przetłumaczona do języka docelowego. Wprawdzie można tutaj, teoretycznie, obejść się bez interwencji ludzkiej poprzez użycie programu do automatycznego tłumaczenia, lecz – jak wiadomo – efekt jest często opłakany. Warto zatem poświęcić odrobinę swojego czasu na dokładne przetłumaczenie wszystkich ciągów. W idealnej sytuacji będzie to jednorazowy wysiłek, a uzyskany w ten sposób słownik będzie można wykorzystywać wielokrotnie. Przeważnie, przy nowszych wersjach, praca sprowadza się do dodania jedynie paru linii składających się na tłumaczenie wyłącznie nowych ciągów znaków, które zostały umieszczone w nowszej wersji programu (względem tej już wcześniej przetłumaczonej).

Kiedy słownik jest już gotowy, tworzony jest przetłumaczony plik .rc, który zawiera wszystkie ciągi znaków, znajdujące się w słowniku, zamienione na ich odpowiedniki w języku docelowym.
Opcjonalnie, można również zmienić wszystkie linie zawierające informacje o języku, zaczynające się od LANGUAGE. Wykonanie tej czynności umożliwi późniejsze wygenerowanie programu wielojęzykowego, którego język będzie zależał od środowiska, w którym zostanie uruchomiony. Taką funkcjonalność zapewnia sam mechanizm Resources w Windowsie.

Oczywiście, istnieje możliwość utworzenia wielu słowników dla różnych języków przez osobę lub osoby tłumaczące.

Kolejnym etapem jest skompilowanie przetłumaczonego lub przetłumaczonych plików .rc do postaci nadającej się do ponownego umieszczenia w pliku .exe. Do tego celu służy program RC.exe, który można otrzymać wraz z darmową instalacją Visual Studio Express. Co ciekawe, jedyną zależnością tego programu jest plik RcDll.dll znajdujący się w tym samym katalogu. Można zatem skopiować oba pliki i używać ich bez konieczności posiadania Visual Studio. Autor nie jest jednak prawnikiem – nie ma więc zamiaru wypowiadać się na temat prawnych zagadnień takiego rozwiązania.

	RC.exe /i include /fo translated.res translated.rc

Po uzyskaniu skompilowanych plików .res, można ponownie skorzystać z programu Resource Hacker do dołączenia jego zawartości do tłumaczonego programu.

	ResHacker.exe -addoverwrite original.exe , translated.exe , translated.res ,,,

Aby zautomatyzować załkowicie ten proces, został napisany Pythonowy wrapper, którego zadaniem było uruchamianie programu Resource Hacker z odpowiednimi parametrami, generowanie i obsługa słowników dla poszczególnych języków oraz zajmowanie się różnymi osobliwościami Resource Hackera i RC.exe, które nie zostały tu opisane z powodu braku miejsca.

Uzyskany w ten sposób program wykonywalny zawiera przetłumaczone zasoby, które zostaną użyte po jego uruchomieniu. Efektem będzie wyświetlanie tekstu oraz okien dialogowych w języku innym niż oryginalnie. Niemniej jednak, opisana tutaj metoda posiada jedną wadę: działa tylko jeśli twórca zastosował mechanizm zasobów w swojej aplikacji. W przypadku użycia ciągów znaków umieszczonych bezpośrednio w kodzie potrzebne będzie inne podejście.

### Ciągi znaków bezpośrednio w kodzie


Z punktu widzenia programisty, najprostszym sposobem umieszczania tekstu w aplikacjach, jest bezpośrednie wpisanie ciągu znaków w kod, tak jak na przykład:

	printf(„Hello world\n”);

Podejście to jest o tyle wygodne, że nie wymaga składowania ciągów w zewnętrznych plikach oraz gimnastykowania się celem użycia ich. Jeżeli jednak spoglądamy na taki program pod kątem ewentualnego tłumaczenia jest to istny horror. Nawet dysponując oryginalnym kodem źródłowym, nie jest to rzecz prosta w wykonaniu, skoro ciągi mogą być porozrzucane wszędzie w kodzie. Poziom trudności zwielokrotnia się jeśli jedyne czym dysponujemy, to już skompilowany plik wykonywalny.

Celem tłumacza będzie zatem przede wszystkim ustalenie wszystkich miejsc, w których znajdują się ciągi znaków w aplikacji.

### Odwołania do ciągów znaków

Aby móc tego dokonać, należy najpierw ustalić w jaki sposób komputer używa ciągów znaków oraz jak się do nich odwołuje z poziomu asemblera.

Przykładowy kod, który wypisuje godzinę w języku C wygląda następująco:

	printf(„Jest godzina %d:%02d\n”, hours, minutes);

Po skompilowaniu jego odpowiednik w asemblerze będzie wyglądał mniej więcej tak:

	push offset minutes
	push offset hours
	push offset format_string ; „Jest godzina %d:%02d\n”
	call printf

Najpierw następuje wrzucenie adresów wszystkich parametrów funkcji na stos, a potem wywołanie funkcji printf, która po uruchomieniu zdejmuje te argumenty ze stosu i buduje z nich ostateczny ciąg do wyświetlenia na ekran.

Ponieważ format_string jest wskaźnikiem na ciąg znaków, adres na który wskazuje będzie zawierał treść, która może zostać przetłumaczona. Dezasemblując zatem program i szukając w nim odwołań do pamięci, można zatem znaleźć interesujące nas ciągi znaków. Należy jednak zauważyć, że nie każde takie odwołanie będzie tym, na którym nam zależy. Przykładem mogą być choćby znajdujące się obok dwie pozostałe instrukcje push, które choć wyglądają tak samo (wrzucają na stos adres pewnej komórki pamięci), nie są odwołaniem do żadnego ciągu znaków.
Co więcej, zamiast:

	push offset minutes

kompilator mógł równie dobrze wygenerować następujący kod:

	mov eax, offset minutes  ; zapisz adres komórki do rejestru eax
	push eax  ; wrzuć zawartość rejestru eax na stos
	...

Należy zatem mieć na uwadze, że interesujące może być każde odwołanie do pamięci, nie tylko to najbardziej oczywiste.

Po uzyskaniu wszystkich potencjalnych adresów ciągów znaków, można przystąpić do budowania słownika, analogicznie jak miało to miejsce w przypadku mechanizmu Resources. Trzeba jednak zauważyć, że w odróżnieniu od słownika wygenerowanego na podstawie zasobów, nie wszystkie, a nawet większość znalezionych odwołań nie będzie wskazywała na ciągi znaków, lecz będzie tzw. false-positive. Konieczne jest zatem odsianie wszystkich odwołań, które wskazują na coś, co na pewno ciągiem znaków nie jest.

Autor z powodzeniem stosował następujące kroki:
* Czy instrukcja zawiera odwołanie do pamięci
* Czy miejsce w pamięci, do którego następuje odwołanie jest poprawne – adres wskazuje na którąś z sekcji programu, zadeklarowanych w nagłówkach pliku wykonywalnego
* Czy to, co znajduje się tamtym miejscu wygląda jak ciąg znaków

	if instr.Instruction.Category & 0xFFFF == bea.DATA_TRANSFER and
	   instr.Instruction.Mnemonic in ('mov ', 'push ') and
	   instr.Argument2.AccessMode == bea.READ and
	   instr.Argument2.ArgType & bea.CONSTANT_TYPE and
	   instr.Argument2.ArgType & bea.ABSOLUTE_):

		section = self.pe.get_section_by_rva(self.pe.va2rva(instr.Instruction.Immediat))
		if section and (section.IMAGE_SCN_CNT_INITIALIZED_DATA or section.IMAGE_SCN_CNT_UNINITIALIZED_DATA):
			check_if_points_to_a_string(instr)


Ostatni podpunkt z poprzedniej listy można rozszerzyć o takie heurystyki jak:
Minimalna i maksymalna długość ciągu znaków
Czy wszystkie znaki są znakami, które dają się wyświetlić na ekranie
W przypadku gdy znane jest użyte kodowanie znaków, czy ciąg nie zawiera znaków, które w tym konkretnym kodowaniu nie istnieją.

	try:
		unicode_s = s.decode(input_encoding)
	except UnicodeDecodeError:
		return False

Dla kodowania utf-16, które jest w stanie zapisać prawie każdą używaną na świecie literę, w tym japońskie, chińskie czy koreańskie „szlaczki” również można znaleźć sposób. Znając oryginalny język tłumaczonego programu, można ograniczyć zakres znaków unicode, które mogą wystąpić. Należy skorzystać w tym celu z tablic ogólnodostępnych w internecie.

Jeśli zaś interesują nas właśnie japońskie Kanji (które znajdują się w tym samym zakresie co znaki chińskie i koreańskie, przez co nie da się ich łatwo oddzielić od znaków stosowanych w tych dwóch pozostałych językach) można skorzystać z sylabusa do języka japońskiego. Opisane są w nim wszystkie znaki, które powinien znać pierwszoklasista, drugoklasista i tak dalej, przez wszystkie lata szkoły. Po połączeniu zbiorów znaków z wszystkich klas, otrzymuje się listę wszystkich najpopularniejszych znaków Kanji, stosowanych na co dzień. Każdorazowe sprawdzenie czy każdy znak znajdujący się w zakresie zarezerwowanym dla CJK (Chinese Japanese Korean) jest również w wygenerowanym zbiorze najpopularniejszych Kanji daje bardzo dobre efekty.

Po zastosowaniu powyższych heurystyk i wygenerowaniu słownika, należy przetłumaczyć go, tak jak miało to miejsce z Zasobami. W przypadku dalszego występowania false-positives należy je pominąć, z przyczyn oczywistych: „przetłumaczenie” czegoś, co nie jest naprawdę ciągiem znaków będzie skutkowało zepsuciem programu.

### Problemy z tłumaczeniem w miejscu

Gdy znane są pozycje oryginalnych ciągów znaków, gotowy jest słownik, pora na tłumaczenie. Najprostszym rozwiązaniem byłoby nadpisywanie znaków bezpośrednio we wskazywanym obszarze pamięci. Niestety, nie jest to zawsze możliwe. Przykładowo, przy próbie tłumaczenia słowa well (studnia) wystąpi taka sytuacja:

	char *place = ”Well”;

W pamięci będziemy mieli następujące bajty:

	'W', 'e', 'l', 'l', '\0', ??,  ??,  ??

Ponieważ plik .exe jest zbudowany tak, aby zajmować jak najmniej miejsca, bezpośrednio po znaku null, oznaczającym koniec ciągu znaków, z dużym prawdopodobieństwem znajdują się kolejne dane – jakieś wartości liczbowe lub kolejny string. Jeśli pamięć zostałaby nadpisana w miejscu, wyglądałaby tak:

	'S', 't', 'u', 'd', 'n', 'i', 'a', '\0'

Jeżeli dane znajdujące się za ciągiem „well” były gdzieś używane (a najprawdopodobniej właśnie były), to wskaźnik, który na nie wskazywał, w najlepszym przypadku zacznie wskazywać na ciąg znaków „ia” (jeśli był wskaźnikiem na ciąg znaków). W najgorszym zaś – jego użycie spowoduje wysypanie się programu (jeśli był, na przykład, wskaźnikiem na funkcję).

W tej sytuacji, konieczne jest znalezienie dodatkowego miejsca, gdzie można będzie zapisać przetłumaczone wersje ciągów. Wprawdzie w każdym pliku wykonywalnym, z uwagi na konieczność wyrównywania rozmiarów sekcji tak, aby były wielokrotnością pewnych ustalonych wartości (patrz specyfikacja plików PE/COFF), znajdują się „dziury”, które nie są używane. Nie są one przeważnie wystarczająco duże, aby pomieścić tłumaczenie nawet względnie małego programu lub gry. Do wyboru jest zatem albo zmiana rozmiaru ostatniej sekcji, tak aby umożliwić zmieszczenie się pod jej koniec tłumaczenia, albo utworzenie nowej sekcji, wyłącznie na tę potrzebę.
Do obu rozwiązań można zastosować bibliotekę pefile, która umożliwia ograniczone manipulowanie zawartością plików PE/COFF (exe).
Należy mieć świadomość, że istnieją gotowe programy, które potrafią zarówno zmieniać rozmiary istniejących sekcji, jak i dodawać kolejne. Dodatkowo, funkcjonalność ta nie jest dostępna w tej bibliotece jako „gotowiec” i należy ją ręcznie zaimplementować, jednak z uwagi na chęć zautomatyzowania tej czynności wykorzystana została właśnie ta biblioteka.


Do automatycznego zdezasemblowania oraz analizy programu, została z kolei użyta biblioteka BeaEngine, za pomocą pythonowego wrappera BeaEnginePython.

### Double null-terminated buffer

Następnym problemem na jaki można się natknąć podczas procesu znajdywania potencjalnych ciągów znaków, to fakt, że niektóre funkcje przyjmują jako argument coś, co jest nazywane double null-terminated buffer.
Jest to lista ciągów, stworzona tak, że bezpośrednio po znaku terminującym pierwszy ciąg (nullem), umieszczony jest kolejny ciąg. Po nim kolejny i tak dalej. Ostatni ciąg w liście zakończony jest podwójnym znakiem terminującym.
Inny sposób wyobrażenia sobie tej struktury to dodanie na końcu listy ciągów znaków pustego ciągu, a następnie sklejenie ich ze sobą, zostawiając znaki terminujące.


Na czym konkretnie polega problem? Otóż z punktu widzenia kodu maszynowego (i zarazem źródłowego), wywołanie funkcji przyjmującej taki bufor nie różni się niczym od wywołania funkcji przyjmującej normalny ciąg znaków. Zarówno w jednym, jak i drugim przypadku występuje przekazanie wskaźnika na coś, co wygląda jak pojedynczy ciąg znaków. Jedynie w pierwszym przypadku, za pierwszym ciągiem, w pamięci, mieści się kolejny.
Jeżeli to odwołanie zostanie potraktowane jak normalny wskaźnik na string, efekt tłumaczenia będzie taki, że do funkcji zostanie przekazany przetłumaczony pierwszy ciąg... oraz wszystkie kolejne, przypadkowe ciągi znaków, które będą się znajdywać bezpośrednio po nim w obszarze pamięci, gdzie mieszczą się tłumaczenia.
Skąd program automatycznie analizujący aplikację powinien zatem się domyślić, że nie należy tym razem zaprzestać odczytu zawartości pamięci po dojściu do terminatora, a potraktować ten obszar specjalnie?

Sposób wykorzystany przez autora nie jest być może najwyższych lotów, ale działa: ponieważ takich ciągów jest w programie stosunkowo mało, osoba tłumacząca musi je oznaczyć ręcznie jako taki bufor. Po natrafieniu w pamięci na ciąg o treści takiej, jak oznaczona, program wie, że należy czytać zawartość dalej, aż do napotkania podwójnego terminatora.

Poprawnym sposobem powinno być każdorazowe sprawdzanie czy na końcu znalezionego ciągu nie znajdują się kolejne ciągi, które są ostatecznie zakończone podwójnym terminatorem. Z uwagi jednak na fakt, że kompilatory i linkery starają się maksymalnie upakować dane tak, aby zminimalizować rozmiar plików wykonywalnych, takie podejście mogłoby generować bardzo dużo false-positive'ów, ponieważ niezwiązane ze sobą ciągi znaków będą z dużym prawdopodobieństwem leżały obok siebie.
Ciekawym spostrzeżeniem może być fakt, że w przypadku double null-terminated buffer, wszystkie odwołania do niego wskazują wyłącznie na pierwszy ciąg. Oznacza to, że jeżeli znaleziona została grupa czegoś, co może zostać zakwalifikowane jako ciągi znaków i żaden z nich, poza tym pierwszym, nie posiada odwołań z kodu, to z dużym prawdopodobieństwem mamy do czynienia z double null-terminated buffer.
Niestety, powyższa metoda nie została jeszcze sprawdzona w praktyce, więc nie wiadomo jak dobre wyniki można uzyskać za jej pomocą.


### Wskaźnik na wskaźnik

Niektóre funkcje mogą z kolei przyjmować jako argument wskaźnik na tablicę stringów. Tutaj sytuacja jest jeszcze trudniejsza, albowiem bez dokładnej analizy kodu nie ma możliwości ustalenia, że uzyskany wskaźnik jest faktycznie wskaźnikiem na listę wskaźników. Na pierwszy rzut oka będzie to po prostu wskaźnik na jakieś dane binarne, Dopiero dokładniejsze przyjrzenie się ujawni, że co cztery bajty (przy założeniu kodu 32-bitowego) mamy do czynienia z wskaźnikiem na ciąg znaków.

	char *strings[] = {”Ala”, ”ma”, kota”, NULL};

	'0x00', '0xDA', '0x40', '0x00', // → ”Ala”
	'0x04', '0xDA', '0x40', '0x00', // → ”ma”
	'0x07', '0xDA', '0x40', '0x00', // → ”kota”
	'0x00', '0x00', '0x00', '0x00', // NULL

Tym razem, z pomocą przychodzi nam tablica relokacji.
Czasami, w trakcie uruchamiania programu, zachodzi potrzeba przeniesienia jego kodu w inne miejsce w pamięci niż by kompilator sobie życzył. Jeśli w kodzie znajdują się odwołania do konkretnych miejsc w pamięci (za pomocą adresacji bezwzględnej), przesunięcie programu gdzie indziej spowoduje, że pod wskazanymi adresami nie będzie już znajdywało się to, co wcześniej miało się znajdywać. Aby temu zapobiec, kompilator tworzy tablice relokacji, w których umieszcza pozycje wszystkich bezwzględnych odwołań do pamięci. Gdy System Operacyjny musi dany program zrelokować, korzysta z tablicy relokacji, aby poprawić odpowiednie miejsca w kodzie, tak aby po przeniesieniu programu odwołania do pamięci dalej wskazywały w poprawne miejsce.

Ponieważ odwołania do ciągów znaków są odwołaniami bezwzględnymi, wszystkie powinny się znaleźć w tablicy relokacji danego programu. Pozostaje więc tylko przejrzeć ich zawartość i zastosować wspomniane wcześniej heurystyki celem sprawdzenia, czy faktycznie mamy do czynienia z ciągami znaków.
Umożliwienie relokacji programu jest nieobowiązkowe i nie każdy kompilator (lub programista, który nim steruje) udostępni tablicę relokacji wraz z programem. Nie można przez to polegać wyłącznie na jej istnieniu do tłumaczenia aplikacji, a omówione wcześniej metody muszą zostać zaimplementowane na wypadek potrzeby tłumaczenia aplikacji, które tablic relokacji nie mają.


### Tłumaczymy


Po utworzeniu nowej sekcji lub rozszerzeniu starej, należy umieścić w niej przetłumaczone ciągi znaków. Następnie, konieczne jest ponowne przejście po wszystkich odwołaniach do nieprzetłumaczonych ciągów oraz podmienienie ich tak, aby wskazywały na nowe, przetłumaczone.
Tak zmodyfikowany plik wykonywalny, po uruchomieniu, będzie wyświetlał wszystkie ciągi znaków w nowym języku.


### Pomysły na przyszłość

Jak można łatwo zauważyć, w przypadku podmiany wskaźników do ciągów znaków, bezpośrednio w kodzie programu, ciągi te są ustawiane na sztywno. Oznacza to, że po przetłumaczeniu aplikacji na jakiś język, będzie ona dostępna wyłącznie w nowym języku a jej poprzednia wersja nie będzie dostępna.

Można temu zaradzić przez udostępnienie wielu wersji aplikacji, każdej przetłumaczonej na dany język. Dużo lepiej by było, gdyby istniała możliwość uzyskania funkcjonalności takiej, jak w przypadku mechanizmu Resources: automatyczne uzyskiwanie odpowiednich ciągów, w zależności od języka zainstalowanego Systemu Operacyjnego.

Autor pracuje aktualnie nad sposobem uzyskania takiego efektu, poprzez zmodyfikowanie metody tłumaczącej aplikację: zamiast podmieniać odwołania do ciągów znaków, do tłumaczonego programu zostaje doklejona lista offsetów, w których nastąpiłaby podmiana wraz ze wskazaniem na nowy ciąg znaków dla danego języka. Doklejonych powinno zostać tyle list, ile języków ma być obsługiwanych przez program (z pominięciem tego oryginalnego). Na końcu należy jeszcze dokleić zestaw instrukcji asemblerowych, którego zadaniem będzie sprawdzenie języka Systemu Operacyjnego, wybranie na tej podstawie odpowiedniej listy tłumaczeń oraz podmienienie wszystkich odwołań, w trakcie działania programu.
Po podmianie, w nagłówku pliku .exe, wartości pola Entry Point (od miejsca wskazywanego przez to pole rozpoczyna się działanie programu) na miejsce, gdzie znajduje się doklejony przez nas zestaw instrukcji, otrzymuje się prawdziwy program wielojęzyczny, pomimo faktu, iż oryginalny twórca nigdy nie przewidywał takiej możliwości.


* [http://msdn.microsoft.com/en-us/library/windows/hardware/gg463119.aspx](http://msdn.microsoft.com/en-us/library/windows/hardware/gg463119.aspx) – Specyfikacja plików PE/COFF (exe)
* [http://code.google.com/p/pefile/](http://code.google.com/p/pefile/) – Biblioteka pefile
* [http://www.beaengine.org/](http://www.beaengine.org/) – Biblioteka BeaEngine
* [https://pypi.python.org/pypi/BeaEnginePython](https://pypi.python.org/pypi/BeaEnginePython) – Pythonowy wrapper na BeaEngine
* [http://msdn.microsoft.com/en-us/library/ms632583.aspx](http://msdn.microsoft.com/en-us/library/ms632583.aspx) – Opis mechanizmu Resources
* [http://jrgraphix.net/research/unicode_blocks.php](http://jrgraphix.net/research/unicode_blocks.php) – Zakresy znaków Unicode
* [http://www.tonypottier.info/Unicode_And_Japanese_Kanji/](http://www.tonypottier.info/Unicode_And_Japanese_Kanji/) – Lista najpowszechniejszych znaków Kanji, uczonych w szkołach
* [http://www.woodmann.com/fravia/covert1.htm](http://www.woodmann.com/fravia/covert1.htm) – Dodawanie nowej sekcji do plików PE/COFF
