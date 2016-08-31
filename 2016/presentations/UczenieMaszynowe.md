#Uczenie maszynowe - czyli jak rozwi¹zywaæ nietrywialne problemy #

##Streszczenie##

Techniki uczenia maszynowego s¹ szeroko wykorzystywane w ró¿nych obszarach codziennego ¿ycia. Problemy takie jak klasyfikacja czy predykcja, których rozwi¹zanie przy pomocy tradycyjnych algorytmów siê nie sprawdza, mog¹ byæ z powodzeniem implementowane metodami pozwalaj¹cymi nauczyæ program podejmowaæ trafne decyzje. Python idealnie nadaje siê do wykorzystania tych technik, w czym pomaga bez ma³a kilkadziesi¹t mniej lub bardziej wyspecjalizowanych bibliotek.

##Rozwój znaczenia i metod uczenia mazynowego##

Gdy w roku 1965 na Uniwerstytecie Stanforda powstawa³ system Dendral, nikt pewnie nie przypuszcza³, ¿e ledwie 50 lat póŸniej uczenie maszynowe (machine learning, ML) bêdzie technik¹ wszechobecn¹, z której korzystamy codziennie, niemal na ka¿dym kroku.

Dendral by³ specjalistycznym oprogramowaniem naukowym, s³u¿¹cym do analizy, grupowania oraz rozpoznawania, nieznanych do tej pory cz³owiekowi, moleku³ zwi¹zków chemicznych. Uzyskane przez program rezultaty zosta³y opublikowane w literaturze naukowej. By³o to pierwsze w historii odkrycie dokonane bezpoœrednio przez komputer, a Dendral uwa¿any jest za prekursora systemów wykorzystuj¹cych uczenie maszynowe.

Motorem napêdowym dynamicznego rozwoju technik sztucznej inteligencji oraz uczenia maszynowego by³ wzrost iloœci gromadzonych danych. Widaæ to dobrze na przyk³ad w dziedzinie biologii, gdzie pod koniec XX wieku intensywnie badano sposoby pozyskiwania informacji o sekwencjach nukleotydowych genów. W roku 2003 g³oœno by³o o zakoñczeniu wielkiego projektu sekwencjonowania ludzkiego genomu (HGP, human genom project). Uzyskanie pierwszej sekwencji ca³ego genomu cz³owieka zajê³o naukowcom 13 lat i kosztowa³o a¿ 3 mld dolarów. Dziœ jesteœmy w stanie zsekwencjonowaæ ca³y genom w ci¹gu zaledwie kilku godzin, za kwotê rzêdu jedynie tysi¹ca dolarów. Czyste, surowe dane niewiele jednak nam daj¹. Nie jest dla nas przecie¿ wa¿na sekwencja sama w sobie, ale wynikaj¹ce z niej wnioski, takie jak okreœlenie sk³onnoœci i ryzyka zachorowania na poszczególne choroby, zidentyfikowanie opornoœci na niektóre leki (wa¿ne przy planowaniu skutecznego leczenia) itp. 

Nawiasem mówi¹c, koszt d³ugotrwa³ego przechowywania danych sekwencyjnych bywa na tyle du¿y, ¿e czêsto bardziej op³aca siê zachowaæ próbkê DNA i w razie potrzeby ponownie przeprowadziæ sekwencjonowanie  To kolejny wa¿ny aspekt zwi¹zany z „er¹ danych”, który, jako wykraczaj¹cy poza tematykê artyku³u, pominê w dalszych rozwa¿aniach.
Du¿a iloœæ gromadzonych danych nie jest domen¹ jedynie biologii. Mamy obrazy medyczne, dane meteorologiczne, dane gospodarcze, dane o ruchu w sieci i szereg innych. I podobnie – bazuj¹c na tych pozornie bezu¿ytecznych surowych danych, chcemy wyci¹gn¹æ konkretne, praktyczne wnioski.

Zastosowania algorytmów uczenia maszynowego widzimy na co dzieñ. Kto z nas wpisuj¹c has³o do popularnej wyszukiwarki nie zwróci³ uwagi na pojawiaj¹ce siê sugestie? Mamy podpowiedzi w pasku przegl¹darki, po witrynach oprowadzaj¹ nas wirtualni asystenci, w pisaniu tekstów pomaga autokorekta, porz¹dek w poczcie zapewniaj¹ wykrywacze spamu, dostajemy propozycje artyku³ów podobnych do aktualnie czytanego, sugestie podobnych tematycznie filmów, wyselekcjonowane reklamy. Uczenie maszynowe pozwala na stworzenie szybkich i wiarygodnych prognoz pogody, wspomaga ocenê zdolnoœci kredytowej, prognozy ekonomiczne, obecne jest w nawigacji samochodowej, grach komputerowych. Do bardziej zaawansowanych problemów nale¿¹ rozpoznawanie mowy, pisma odrêcznego, interpretacja obrazów medycznych i wiele, wiele innych.

Uczenie maszynowe rozumiemy jako zdolnoœæ programu do uczenia siê, do generalizacji. Algorytm konstruuje siê zwykle w ten sposób, ¿e uruchamia siê program na niewielkim wycinku dostêpnych danych, na podstawie których dokonuje on parametryzacji, czyli inaczej mówi¹c – uczy siê. Je¿eli uczenie przebieg³o pomyœlnie, wówczas program bêdzie w stanie podj¹æ w³aœciw¹ decyzjê nawet, je¿eli oka¿emy mu dane, z którymi nigdy wczeœniej nie mia³ do czynienia.
Istot¹ problemów które rozwi¹zujemy metodami uczenia maszynowego s¹ klasyfikacja oraz predykcja. Nie jest moim celem omówienie tutaj konkretnych technik, do których zaliczyæ mo¿emy m.in. sztuczne sieci neuronowe (ANN, *artificial neural networks*) bêd¹ce (mocno uproszczon¹) imitacj¹ procesu uczenia zachodz¹cego w mózgu, maszyny wektorów noœnych (SVM, *support vector machines*), których idea polega na optymalizacji granicy decyzyjnej, ukryte modele markowa (HMM, *hidden markov models*) maj¹ce zastosowanie w analizie procesów stochastycznych czy drzewa decyzyjne (DT, decision trees), które dokonuj¹ klasyfikacji na podstawie odpowiednio wygenerowaniej struktury drzewiastej. W ostatnich latach furorê robi uczenie g³êbokie (*deep learning*), które jest swego rodzaju rozszerzeniem i udoskonaleniem trochê ju¿ odchodz¹cej na boczny tor idei sieci neuronowych. Wœród popularnych technik jest oczywiscie stary, ale jary algorytm k-œrednich i wiele, wiele innych. Czytelników zainteresowanych g³êbszym wyjaœnieniem poszczególnych algorytmów odsy³am do jak¿e bogatej literatury, np. [3].

##Najpopularniejsze biblioteki ML##

Inspiracj¹ do napisania tego artyku³u by³o dla mnie znalezione w sieci zestawienie 20 bibliotek ML dla Pythona [6] uporz¹dkowanych wed³ug doœæ oryginalnego kryterium popularnoœci – wyra¿a³o siê ono liczb¹ commitów na githubie oraz osób bior¹cych udzia³ w tworzeniu biblioteki (contributors). Liczba dostêpnych bibliotek jest jednak znacznie wiêksza. Joseph Misiti w swoim repozytorium zgromadzi³ zestawienie listuj¹ce grubo ponad 150 ró¿nych bibliotek dla Pythona, które w jakimœ stopniu s¹ wykorzystywane w uczeniu maszynowym [5].*
Niew¹tpliwie najpopularniejsz¹ bibliotek¹ oraz de facto standardem jest **scikit-learn* (https://github.com/scikit-learn/scikit-learn) . Biblioteka ta, oparta na popularnych pakietach numerycznych i naukowych, NumPy oraz SciPy cieszy siê te¿ du¿ym wsparciem spo³ecznoœci. Jest bibliotek¹ ogólnego zastosowania – zawiera wiele modu³ów implementuj¹cych ró¿ne algorytmy oraz techniki ML. Biblioteka jest bardzo ³atwa w u¿yciu i wydajna. Jednak za t¹ ³atwoœæ i mnogoœæ zastosowañ p³aci siê elastycznoœci¹. Trudno w scikit-learn zmodyfikowaæ szczegó³owe parametry algorytmu, dopasowuj¹c go do konkretnego problemu. Dlatego, gdy chcemy wykonywaaæ operacje bardziej niskopoziomowe, warto siêgn¹æ po dedykowan¹, bardziej elastyczn¹ bibliotekê, jak np. **PyBrain** (https://github.com/pybrain/pybrain), pozwalaj¹c¹ skonstruowaæ praktycznie dowoln¹ sieæ neuronow¹, modyfikuj¹c np. funkcje aktywacji itp. PyBrain równie¿ wykorzystuje SciPy.

Istniej¹ te¿ biblioteki, które rozszerzaj¹ funkcjonalnoœæ pakietu scikit-learn, np. **Nilearn** (https://github.com/nilearn/nilearn), zawieraj¹ca funkcje szczególnie przydatne w analizie obrazów aktywnoœci mózgu.

Poniewa¿ metody uczenia maszynowego wymagaj¹ zwykle obliczeñ na macierzach i innych z³o¿onych strukturach matematycznych, wiele bibliotek bazuje na specjalistycznych bibliotekach numerycznych. Wspomniany wy¿ej scikit-learn wymaga SciPy i NumPy. Inn¹ bibliotek¹ implementuj¹c¹ zaawansowane obliczenia numeryczne jest **Theano** (https://github.com/Theano/Theano). Theano mo¿e równie¿ byæ samodzielnie wykorzystywana do ML, szczególnie w implementacji sieci neuronowych oraz uczenia g³êbokiego. Theano implementuje równie¿ rozwi¹zania pozwalaj¹ce efektywnie wykonywaæ obliczenia na procesorach graficznych (GPU). 

Wœród bibliotek bazuj¹cych na Theano warto wskazaæ **Pylearn2** (https://github.com/lisa-lab/pylearn2) oraz **Block** (https://github.com/mila-udem/blocks), **Keras** (https://github.com/fchollet/keras) i **Lasagne** *(https://github.com/Lasagne/Lasagne).

Ciekawym pakietem jest równie¿ **Tensorflow** (https://github.com/tensorflow/tensorflow), stworzony w ramach projektu Google Brain. Implementuje wysokopoziomowy dostêp do sieci neuronowych. Do niew¹tpliwych zalet zaliczyæ tu nale¿y obs³ugê obliczeñ równoleg³ych oraz na procesorach graficznych. Biblioteka napisana jest w wiêkszoœci w C++, ale posiada niezbêdne wi¹zania do Pythona.

Wœród bibliotek naj³atwiej znajdziemy te wspieraj¹ce sieci neuronowe czy uczenie g³êbokie. Nie brakuje jednak te¿ modu³ów pozwalaj¹cych na u¿ycie mniej popularnych metod, np. **Pyevolve** (https://github.com/perone/Pyevolve) jest przyk³adem biblioteki implementuj¹cej algorytmy genetyczne. Z kolei **NuPIC** (https://github.com/numenta/nupic) implementuje metodê hierarchical temporal memory (HTM). Technika HTM architektur¹ przypomina sieci neuronowe, ma jednak inne pod³o¿e biologiczne i zasadê dzia³ania.

**Nltk** (http://www.nltk.org/) jest bibliotek¹ dedykowan¹ dla problemów przetwarzania jêzyka naturalnego.

Bibliotek¹ ogólnego przeznaczenia, bez zale¿noœci od SciPy i Theano jest **Pattern** (https://github.com/clips/pattern), dedykowana w szczególnoœci do eksploracji witryn internetowych. Wspomnieæ nale¿y równie¿ biblioteki **H2O** (https://github.com/h2oai/h2o-3)  i **caffe** (https://github.com/BVLC/caffe).

Zwieñczeniem tej niezwykle skrótowej prezentacji niech bêdzie **fuel** (https://github.com/mila-udem/fuel), biblioteka zapewniaj¹ca ³atwy dostêp do popularnych zbiorów danych takich jak MNIST (baza danych pisma odrêcznego). CIFAR-10 (baza obrazów) czy Google's One Billion Words (beza tekstowa). Z kolei **Python Machine Learning Samples** (https://github.com/awslabs/machine-learning-samples) zawiera zbiór przyk³adowych aplikacji wykorzystuj¹cych ML.
 
Tabela 1. Wybrane biblioteki ML dla pythona uporz¹dkowane wg liczby wspó³autorów (contributors) [dane liczbowe wg stanu z 31.08.2016].
|    Biblioteka                  |    commits    |    contributors    |    github                                                 |
|--------------------------------|---------------|--------------------|-----------------------------------------------------------|
|    scikit-learn                |    21148      |    661             |    https://github.com/scikit-learn/scikit-learn           |
|    tensorflow                  |    7339       |    372             |    https://github.com/tensorflow/tensorflow               |
|    Theano                      |    23286      |    250             |    https://github.com/Theano/Theano                       |
|    keras                       |    2592       |    250             |    https://github.com/fchollet/keras                      |
|    caffe                       |    3766       |    208             |    https://github.com/BVLC/caffe                          |
|    pylearn2                    |    7100       |    116             | https://github.com/lisa-lab/pylearn2                      |
|    NuPIC                       |    5986       |    73              | https://github.com/numenta/nupic                          |
|    H2O                         |    19092      |    62              | https://github.com/h2oai/h2o-3                            |
|    lasagne                     |    1050       |    51              |    https://github.com/Lasagne/Lasagne                     |
|    blocks                      |    3175       |    48              |    https://github.com/mila-udem/blocks                    |
|    nilearn                     |    5145       |    45              |    https://github.com/nilearn/nilearn                     |
|    pybrain                     |    984        |    31              | https://github.com/pybrain/pybrain                        |
|    fuel                        |    1035       |    28              |    https://github.com/mila-udem/fuel                      |
|    pattern                     |    943        |    20              | https://github.com/clips/pattern                          |
|    fann                        |    156        |    19              |    https://github.com/libfann/fann                        |
|    machine-learning-samples    |    29         |    13              |    https://github.com/awslabs/machine-learning-samples    |
|    Pyevolve                    |    168        |    12              |    https://github.com/perone/Pyevolve                     |


##Bibliografia##

1.	Britz D., Implementing a Neural Network from Scratch in Python – An Introduction, http://www.wildml.com/2015/09/implementing-a-neural-network-from-scratch/
2.	Górecki P., Uczenie maszynowe, sztuczna inteligencja i (samo)œwiadomoœæ, 2014,  http://www.tabletowo.pl/2014/11/23/uczenie-maszynowe-sztuczna-inteligencja-i-samoswiadomosc/
3.	Holehouse AS., Stanford Machine Learning , http://www.holehouse.org/mlclass/
4.	Mayo M., 7 Steps to Mastering Machine Learning With Python, 2015, http://www.kdnuggets.com/2015/11/seven-steps-machine-learning-python.html
5.	Misiti J., Awesome Machine Learning, https://github.com/josephmisiti/awesome-machine-learning#python-cv
6.	Peddibhotla G.B., Top 20 Python Machine Learning Open Source Projects, 2015, http://www.kdnuggets.com/2015/06/top-20-python-machine-learning-open-source-projects.html
7.	Python Tools for Machine Learning, 2014, https://www.cbinsights.com/blog/python-tools-machine-learning/ 
8.	Robinson S., The Best Machine Learning Libraries in Python, 2015, http://stackabuse.com/the-best-machine-learning-libraries-in-python/ 
9.	Rosebrock A., My Top 9 Favorite Python Deep Learning Libraries, 2016, https://www.pyimagesearch.com/2016/06/27/my-top-9-favorite-python-deep-learning-libraries/ 
10.	Scikit-learn. Machine Learning in Python, http://scikit-learn.org/
