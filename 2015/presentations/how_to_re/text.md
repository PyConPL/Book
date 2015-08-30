# How to re, czyli jak wyrażenia regularne stały się tym, czym są obecnie. #

## 1. Historia ##
Wyrażenia regularne (powszechnie znane jako regular expressions, bądź w skrócie regex/regexp) są to wzorce, które opisują łańcuchy symboli. Jak podaje wikipedia: "Wyrażenia regularne mogą określać zbiór pasujących łańcuchów, mogą również wyszczególniać istotne części łańcucha." [1] Obecnie wyrażenia regularne znajdują często zastosowanie w programowaniu. Jednakże ich początki datowane są na lata 40, XX wieku, z informatyką miały niewiele wspólnego.

### a) Biologia na ratunek informatyce ###
Za podstawę współczesnej informatyki uznawane są automaty skończone, które wywodzą się z pracy Alana Turinga. [2] Maszyna Turinga, to abstrakcyjny model komputera służącego do wykonywania algorytmów, składającego się z nieskończenie długiej taśmy podzielonej na pola, w których zapisuje się dane [3].
Zainspirowani pracą Turinga, dwaj neurolodzy Warren McCulloch i Walter Pitts zbudowali sztuczny neuron, który jest uproszczonym matematycznym modelem biologicznego neuronu. Służy jako podstawowy blok budulcowy sztucznych sieci neuronowych. [4] W 1943 wyniki swojej pracy opublikowali w artykule naukowym w Bulletin of Mathematical Biophysics 2:115-133 zatytułowanym: "A logical calculus of the ideas immanent in nervous activity". Okazało się, że ten artykuł stał się podwaliną pod rozwój współczesnej informatyki, chociaż nie taki był jego cel. [5]

### b) Co tam panie, w matematyce słychać ###
Kilkanaście lat później, w 1956 roku, matematyk Stephen Kleene poszedł o krok dalej i bazując na neuronie McCullocha-Pittsa [4], zaproponował prostą algebrę, swoje przemyślenia publikując w artykule "Representation of events in nerve nets and finite automata". [6] Jego celem było opisanie mózgu jako rachunku logicznego.
Kleene'a nie interesowało to, czy model McCullocha-Pittsa był dokładny; skupił się na tym czym ten model jest. W przeciwieństwie do podejścia McCullocha-Pittsa, Kleene udowodnił, że model neuronu nie ogranicza się jedynie do ludzkiego mózgu, ale w rzeczywistości opisuje szerszy zakres jakim jest każdy automat skończony, bez ograniczeń na to, czy jest to zwierzę, człowiek czy maszyna. Tym samym, nawiązał do wykładu o automatach, jaki von Neumann dał w trakcie Sympozjum Hixona. [9] To właśnie John von Neumann był jednym z pierwszych, którzy próbowali przedstawić ogólną teorię automatów wykorzystując narzędzia logiki.
Artykuł Kleene'a był pierwszym krokiem na drodze ku temu, by można było wyrażenia regularne zaszczepić w programach komputerowych.

### c) Jak by tu tego użyć w informatyce ###
Prawdopodobnie, efekt pracy, którą dokonali wymienieni wcześniej naukowcy, nigdy by nie trafił do komputerów, gdyby nie Janusz Brzozowski. [10] Brzozowski, który uzyskał tytuł doktora nauk elektrycznych na Princeton University, przez pewien czas wykładał w Berkeley. Wtedy też zaprezentował sposób na wykorzystanie wyrażeń regularnych by stworzyć diagram stanów, które były szeroko wykorzystywane w latach 50-tych do projektowania i implementowania programów w ówczesnych komputerach.
Właśnie w Berkeley, Ken Thompson [12] miał z Brzozowskim do czynienia. Bazując na tym co usłyszał, postanowił zaadoptować to podejście, i zaimplemenować je w oprogramowaniu. Pracując przy tworzeniu UNIX-a, napisał coś, co ostatecznie miało stać się narzędziem "grep" a zaimplementowane było w edytorze "QED". "grep" to w rzeczywistości skrót od "Globally search for regular expression re and Print it", czyli w wolnym tłumaczeniu "globalne wyszukiwanie wyrażeń regularnych oraz wyświetlanie ich". Swój algorytm opisał w artykule "Regular Expression Search Algorithm" [14], a całość zaimplementował w asemblerze dla IBM 7090.

### d) Gdzie tego szukać? ###
Od momentu, gdy Thompson zaimplementował pierwszą wersję wyrażeń regularnych w QED minęło sporo czasu. Wraz z rozwojem oprogrwamowania, regexpy można znleźć w "vi", "lex" "sed", "AWK" czy w "Emacsie". Opróćz tego, mnóstwo IDE korzysta z odkryć, których korzenie sięgają lat 40-tych.
Jednym z pierwszych zastosowań w językach programowania, może się poszczycić Perl. Bazując na tym, większość współczesnych języków posiada zbliżoną składnię: do tego grona można zaliczyć Javę, JavaScript, Ruby czy, oczywiście Pythona.

### e) Podsumowanie ###
Zakres transformacji, które wyrażenia regularne przeszły, jest zadziwiający. Zaczynając od pracy Rudolfa Carnapa [11] w zakresie logicznej składni języka, poprzez wspomniane neurony McCullocha-Pittsa. Następnie podchwycone przez von Neumannowy opis komputera EDVAC czy jego późniejszą teorię automatów. By ostatecznie, otrzymać nazwę dzięki matematykowi Stephenowi Kleene.
Dzięki Januszowi Brzozowskiemu, który wykorzystał je by zaprojektować diagramy stanów, a następnie zaimplementowane po raz pierwszy, przez Kena Thompsona, ostatecznie trafiły do wszelkiej maści programów, by służyć ku uciesze programistów.

## 2. Bibliografia ##
Powyższy opis jest mocno skrótowy i nie wyczerpuje tematu. Jest bardziej zarysem tego, jak interesujące są początki informatyki, którą znamy w obecnej formie. W celu zgłębienia tematu polecam pozycje [2] oraz [14]. Jak widać na powyższym przykładzie, z wielu, wydawałoby się, niezależnych przemyśleń powstało coś uniwersalnego. Dlatego warto znać historię, dokonania poprzednich pokoleń, by na tym bazując, tworzyć lepszą jakość.

[1] https://pl.wikipedia.org/wiki/Wyra%C5%BCenie_regularne
[2] Speech and Language Processing: An introduction to natural language processing, computational linguistics, and speech recognition. Daniel Jurafsky & James H. Martin
[3] https://pl.wikipedia.org/wiki/Maszyna_Turinga
[4] https://pl.wikipedia.org/wiki/Neuron_McCullocha-Pittsa
[5] http://blog.staffannoteberg.com/2013/01/30/regular-expressions-a-brief-history/
[6] http://books.google.com/books?id=oL57iECEeEwC
[7] https://pl.wikipedia.org/wiki/J%C4%99zyk_regularny
[8] http://kelty.org/or/papers/Kelty_Franchi_LogicalInstruments_2009.pdf
[9] https://www.cs.ucf.edu/~dcm/Teaching/COP5611Spring2010/vonNeumannSelfReproducingAutomata.pdf
[10] https://en.wikipedia.org/wiki/Janusz_Brzozowski_(computer_scientist)
[11] https://en.wikipedia.org/wiki/Rudolf_Carnap#Logical_syntax
[12] https://pl.wikipedia.org/wiki/Ken_Thompson
[13] https://pl.wikipedia.org/wiki/Unix
[14] http://www.fing.edu.uy/inco/cursos/intropln/material/p419-thompson.pdf
