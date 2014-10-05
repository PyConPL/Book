# NoCaptcha - jak zabezpieczyć formularz przed zautomatyzowanym uzupełnianiem bez udziału użytkownika.
## Jakub Wasielak

### Wstęp

W poniższym artykule przedstawiam alternatywne podejście do bardzo popularnej metody ochrony przed botami – CAPTCHA, kompletny, zautomatyzowany i publiczny test Turinga do odróżniania ludzi od robotów, który już od 2000 roku „broni” formularzy internetowych przed zautomatyzowanym dostępem. Obecnie, w dobie powszechnego upraszczania interfejsu użytkownika, CAPTCHA staje się coraz większym obciążeniem dla projektantów stron internetowych. Jednak okazuje się, że CAPTCHA może zostać bardzo łatwo zastąpiona poprzez kombinację takich mechanizmów, jak: Honeypot, sprawdzanie czasu wypełniania formularza oraz metod opartych o szyfrowanie md5. Celem tego artykułu jest zaprezentowanie i rozpowszechnienie innych metod zabezpieczania formularzy niż CAPCHA.

### O CAPTCHA

#### Powstanie
Pierwsze wzmianki na temat zastosowania CAPTCHA pochodzą już z 1997 roku, kiedy została ona wykorzystana w wyszukiwarce AltaVista w celu ochrony przed automatycznym dodawaniem adresów do bazy. W 1998 roku mechanizm przypominający dzisiejsze działanie CAPTCHA zostało opatentowane przez zespół programistów. Przez lata generatory CAPTCHA były udoskonalane, aby możliwie jak najbardziej ułatwić użytkownikom odczytywanie graficznie przedstawionych tekstów, a jednocześnie maksymalnie je utrudnić mechanizmom OCR ("Optical Character Recognition").

#### ReCAPTCHA
![ReCAPTCHA](http://www.cmu.edu/startups/images/logo-recaptcha.jpg)

W roku 2007 Luis Von Ahn po raz pierwszy zaprezentował ideę reCAPTCHA. Każda akcja użytkownika polegająca na przepisaniu tekstu z obrazka do odpowiedniego pola była w rzeczywistości pracą nie przynoszącą realnych korzyści. Biorąc pod uwagę jednego użytkownika, rozpoznanie tekstu nie ma żadnej korzyści, lecz przesuwając skalę do milionów użytkowników wypełniających zabezpieczone formularze na całym świecie, wykorzystanie tej aktywności okazało się istotne. Pomysł Luisa Von Ahn polegał na zastosowaniu w obrazkach CAPTCHA fragmentów rzeczywistych skanów książek, których nie potrafiły rozpoznać skanery OCR. Standardowe pole reCAPTCHA składa się z dwóch słów – jednego sprawdzającego użytkownika, oraz drugiego mającego na celu rozpoznanie niemożliwego do automatycznego odczytania tekstu. W 2009 roku mechanizm reCAPTCHA został wykupiony przez Google i od tamtej pory jest najbardziej popularnym mechanizmem stosowanym do zabezpieczania formularzy.

#### Nowoczesne alternatywy
![Nowoczesne_alternatywy](http://nakedgang.net/cms/images/site_images/areyouahuman.png)

Wraz z rozwojem języka JavaScript oraz powstawaniem coraz liczniejszych bibliotek ułatwiających dynamiczną obsługę treści stron internetowych powstawało dużo rozwiązań opartych wyłącznie o grafiki oraz akcje inne, niż przepisywanie tekstu – np. przeciągnięcie elementu za pomocą myszy. Największym serwisem prezentującym gotowe wtyczki jest strona www.areyouahuman.com. Te metody, choć bezpieczne i proste, bardzo często nie pasują do treści prezentowanej na stronie, uniemożliwiają obsługę strony wyłącznie za pomocą klawiatury oraz najprawdopodobniej nawet nie zostaną wyświetlone bez włączonej obsługi języka JavaScript.


#### Wady
Największą wadą CAPTCHA jest konieczność poświęcenia czasu przez użytkowników na czynność, która nie przynosi im samym żadnej korzyści. W czasach, gdy ogromny nacisk jest kładziony na zatrzymanie użytkownika na swojej stronie, zastosowanie CAPTCHA może mieć duży wpływ na realne straty finansowe. W artykule "F**k CAPTCHA" opublikowanym na stronie www.90percentofeverything.com opisano wpływ likwidacji standardowego mechanizmu CAPTCHA na konwersję użytkowników. Okazało się, że współczynnik konwersji wzrósł o 33,3%. Realnie, przez rejestrację przechodziło o ponad 15% więcej użytkowników, niż poprzednio.
Same obrazki bardzo często są zupełnie nieczytelne. W tym miejscu można by zamieścić dziesiątki zrzutów zupełnie nieczytelnych obrazków CAPTCHA, które są dostępne w internecie. Ze statystyk prowadzonych w systemie Sympatia.pl można odczytać, że kiedy jeszcze CAPTCHA była stosowana, co czwarta osoba była zmuszona wybrać opcję „wygeneruj ponownie”. 
Nie można również zapomnieć o utrudnieniu dla osób niepełnosprawnych – niedowidzących i niewidomych. Choć niektóre systemy posiadają opcję automatycznego czytania tekstu, wciąż jest to niewielki odsetek, a także wciąż duże obciążenie dla osób, które i bez tego posiadają utrudniony dostęp do treści.


### NoCAPTCHA

Poniższe rozwiązanie jest wzorowane na propozycji przedstawionej przez Neda Batcheldera na stronie nedbatchelder.com w artykule pt. "stopbots". Aby poradzić sobie z likwidacją mechanizmu CAPTCHA postanowił on wprowadzić szereg metod, które automatycznie miały rozróżniać ludzi od robotów. Ogólna zasada dotycząca obrony przed robotami polega nie na zastosowaniu pojedynczego, uniwersalnego rozwiązania, lecz na kombinacji wielu metod, z których każda zablokuje jeden konkretny rodzaj robotów. Wszystkie poniższe zabezpieczenia wiążą się z ukrytymi polami, niewidocznymi dla użytkownika. Obecnie boty są w stanie łatwo rozpoznać pola ukryte poprzez znacznik:

	<input type="hidden">

Są one nauczone, aby nie uzupełniać takich pól – skoro są one niewidoczne dla użytkownika, zapewne ich uzupełnienie nie jest konieczne, aby przejść do kolejnego kroku formularza. Dlatego o wiele lepiej sprawdza się ukrywanie elementu przez klasy CSS. W dużym uproszczeniu takie pole będzie wyglądać następująco:

	<input style="display: none;">

Oczywiście powyższy napis można modyfikować jeszcze bardziej. Zamiast stylu w kodzie HTML, można zastosować  klasę zadeklarowaną w plikach CSS. Ponadto znacznik input można zawrzeć w innych znacznikach, które to dopiero będą ukryte.

#### Timestamp

Najprostsza metoda obrony przed robotami polega na dodaniu jednego ukrytego pola do formularza. Pole to, zwane tutaj "timestampem" zawiera aktualną datę wygenerowania formularza zapisaną w UNIX-owym formacie timestamp (liczonym w sekundach od 1 stycznia 1970). Podczas wysyłki formularza należy porównywać obecny czas z czasem podanym w polu timestamp. Jeżeli formularz składający się z kilkunastu pól został uzupełniony i wysłany w np. mniej niż 5 sekund, wprost oznacza to, że nie mógł go uzupełnić człowiek.
Oczywiście ta zapora może zostać bardzo łatwo ominięta – wystarczy tak zaprogramować robota, aby po wygenerowaniu formularza odczekał oczekiwaną wartość czasu i dopiero po tym wysłał dane. Niemniej jest to najprostsza, a zarazem najbardziej skuteczna z metod ochronnych. Większość botów nie jest wymierzona w jeden konkretny cel – przemierzają one Internet od linku do linku starając się wypełnić każdy napotkany formularz.  Jeżeli posiadamy mały lub średni serwis, zapewne zastosowanie wyłącznie tej metody ochroni nas przed robotami, lecz jeżeli prowadzimy duży serwis, musimy być gotowi aby odeprzeć te skierowane wyłącznie w nas ataki.

#### Honeypot

Honeypot, czyli "lep na muchy" jest tak samo prostą metody obrony jak timestamp. Robot uzupełniający formularz szuka pól input o specyficznych, znanych mu nazwach, takich jak "login", "email", czy "password". Aby oszukać automat, należy pomiędzy normalnymi polami formularza zamieścić pułapki, których uzupełnienie powodowałoby błąd podczas walidacji formularza. Formularz, w którym trzeba podać imię i hasło mógłby wyglądać następująco:

	<input type="text" name="name">
	<input type="text" name="email" class="hidden">
	<input type="password" name="password">

Jeżeli w powyższym formularzu zwrócone zostałyby dane dla pola "email", które jest schowane przed użytkownikiem w pliku CSS, oznaczałoby to wprost, że został on wygenerowany automatycznie, a nie przez prawdziwego użytkownika.
Oczywiście przy złożonym formularzu zawierającym wiele różnych pół ciężko będzie znaleźć honeypoty o takich nazwach, które jeszcze nie występują, lecz rozwiązanie tego problemu pojawi się w dalszej części.
Aby jeszcze bardziej usprawnić działanie "lepów", można wprowadzić losowość w generowanym formularzu – pola mogą mieć różne nazwy, dodatkowo mogą pojawiać się losowo między różnymi realnymi polami w formularzu. Wprowadzenie dynamiki do formularza pozwoli ochronić się przed atakami skierowanymi bezpośrednio w naszą stronę. Jednak samo to rozwiązanie jest również proste do obejścia. Jeżeli osoba programująca robota zapozna się ze stroną, może zadeklarować, jakie pola powinien uzupełniać robot oraz nakazać mu, żeby resztę pól omijał.

#### MD5
Ostatnia linia zabezpieczeń polega na zakodowaniu nazw rzeczywistych pól w formularzu. Kodowanie może odbywać się na różne sposoby, ale proponowana jest następująca metoda:

	nazwa = md5 ( hasło + nazwa pola + timestamp )

Kodowanie nazw odbywa się po stronie aplikacji w trakcie generowania formularza, dlatego użytkownik widzi tylko rezultat końcowy, czyli gotową nazwę. Hasło jest zabezpieczeniem wewnętrznym przed złamaniem metody – tak długo, jak nie zostanie one poznane, nie będzie istniała metoda na odwzorowanie algorytmu przetwarzania nazwy. Kodowanie MD5 jest nieodwracalne, natomiast zmiana już jednego znaku zmienia zupełnie całą sumę. Nazwa pola służy do rozpoznawania, które konkretnie pole chcemy przekodować. Ostatnie pole, timestamp wprowadza dynamikę w nazwach pól. Każde odświeżenie formularza będzie powodować wyglądające na losowe zmiany nazw pól. Poniżej przykład dwóch nazw jednego pola:

Pole "email" przy haśle "bardzotrudnehasło" wygenerowane w odstępie 1 sekundy:

	md5( „bardzotrudnehasłoemail1378206571” ) = „3d4d9a18d1584fb54a049cc79416d7b7”
	md5( „bardzotrudnehasłoemail1378206572” ) = „99adcde65db4b8a6d4b98916a708867b”

Tak więc pole użyte w formularzu zamiast wyglądać w następujący sposób:

	<input type="text" name="name">

będzie wyglądać na przykład tak:

	<input type="text" name="3d4d9a18d1584fb54a049cc79416d7b7">

Po wysłaniu formularza z powrotem do aplikacji na podstawie powyższej formuły oraz biorąc jako timestamp ten przekazany w polu timestamp będzie możliwe ponowne wygenerowanie tych samych sum md5, które zostały przekazane jako nowe nazwy pól. Dzięki temu można będzie uzyskać oryginalne nazwy pól bez prezentowania ich nawet przez chwilę użytkownikowi.

Dzięki temu rozwiązaniu każdy formularz prezentowany użytkownikowi będzie inny. Niemożliwe więc będzie zastosowanie żadnych sztywnych metod wpisywania danych.

#### Formularz przed i po
Dla użytego wcześniej formularza zawierającego imię i hasło:

	<input type="text" name="name">
	<input type="password" name="password">

wygenerowany bezpieczny formularz może wyglądać następująco:

	<input type="hidden" name="timestamp" value="1378201731">
	<input type="text" name="1d8d80c45b7b66368d4dfe28df74d1d2">
	<input type="text" name="email" class="hidden">
	<input type="password" name="3b1c1e6e4c0275fc468aa94fc4e973f5">
	<input type="text" name="login" class="hidden">

Natomiast po kolejnym odświeżeniu strony ten sam formularz będzie bardzo odmienny od poprzedniego:

	<input type="hidden" name="timestamp" value="1378201771">
	<input type="text" name="password" class="hidden">
	<input type="text" name="city" class="hidden">
	<input type="text" name="bf4123f857426f9f60c395520f0c5ee1">
	<input type="password" name="5a4f20be80fc229c16154269260e9bee">

Nie jest więc możliwe przygotowanie się do tego, jak będzie wyglądać wygenerowany przez stronę formularz. Pomimo braku standardowego machizmu CAPTCHA bez udziału ludzkiego czynnika prawidłowe wypełnienie formularzu przez robota nie będzie możliwe. A wszystko to dzieje się za plecami użytkownika, który nie zauważy nawet jednej linijki odróżniającej taki formularz od standardowego.

### NoCAPTCHA w Django

Instalacja i korzystanie z biblioteki NoCAPTCHA w Django jest wyjątkowo proste i wymaga jedynie kilku akcji.
Po zainstalowaniu pakietu przez pip:
`pip install nocaptcha`
wystarczy go dodać do listy `INSTALLED_APPS` w ustawieniach:

	INSTALLED_APPS = (
		... 
		'nocaptcha',
		... )

Po tym kroku NoCAPTCHA jest już zainstalowana i można z niej korzystać. Aby stworzyć przykładowy formularz stosujący wszystkie opisane powyżej zabezpieczania dodajemy wyłącznie kilka linijek do standardowego formularza Django:

    from nocaptcha.forms import NoCaptchaForm

	class ContactForm(NoCaptchaForm, forms.Form):
		secret_password = "NoCAPTCHA rządzi!"
		name = forms.CharField(label="Imię”)
		password = forms.PasswordField(label="Hasło")


Tylko tyle aby nasze formularze pozostawały bezpieczne przed robotami.

### Podsumowanie

Powyższy artykuł ma na celu wskazanie jednej z wielu możliwych ścieżek realizacji zagadnienia ochrony formularzy przed automatycznym uzupełnianiem. Nie jest to jedyne możliwe wyjście, z pewnością nie jest też stuprocentowo skuteczne. Jednak to, na czym należy się skupić projektując stronę, to znalezienie środka pomiędzy bezpieczeństwem, a wygodą użytkownika. Rozwiązania NoCAPTCHA nadaje się do łatwego dodawania kolejnych poziomów usprawnień bez wymaganej interakcji ze strony użytkownika. Koniec końców istotne jest to, aby twórcy botów zamiast zająć się pracochłonnym zadaniem pokonania naszych poziomów zabezpieczeń spróbowali szczęścia na innych serwisach – być może nawet konkurencyjnych.
