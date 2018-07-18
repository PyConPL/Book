# Python + Microsoft Azure
Microsoft Azure to infrastruktura i usługi, które tworzą ekosystem chmury publicznej, prywatnej i hybrydowej, dostępnej w 140 krajach świata. Publiczna część chmury Microsoft Azure, to 54 regiony na całym świecie - więcej niż w przypadku innych dostawców infrastruktury chmury publicznej. Pod względem ilości serwerów, chmura Microsoft Azure jest większa niż Amazon AWS i Google Cloud Platform razem wzięte. Można firmę Microsoft kochać, można nienawidzieć i można być obojętnym, ale udział platformy Microsoft Azure w rynku chmurowym, dynamika jej wzrostu i skupienie jej twórców na społeczności deweloperów są trudne do zignorowania - nawet dla największych jej przeciwników.

90% firm z listy Fortune Top 500 korzysta z chmury Microsoft Azure i jest to aktualnie pierwszy wybór dużych przedsiębiorstw w drodze do chmury. Stan ten nie był by możliwy bez olbrzymiego udziału technologii otwartych - takich jak Linux i Python - oraz gigantycznej społeczności, zgromadzonej nie tylko wokół tych technologii, ale także wokół zagadnienia interoperacyjności.

> **Interoperacyjność** – cecha produktu lub systemu, którego interfejsy funkcjonują w pełnej zgodności, tak by współpracować z innymi produktami lub systemami, które istnieją, bądź mogą istnieć w przyszłości, bez jakiegokolwiek ograniczenia dostępu lub ograniczonych możliwości implementacji.
> — Źródło: [Interoperacyjność – Wikipedia, wolna encyklopedia](https://pl.wikipedia.org/wiki/Interoperacyjno%C5%9B%C4%87)

Język Python, w kontekście chmury Microsoft Azure, to nie tylko kwestia środowiska uruchomieniowego dla aplikacji napisanych w tym języku. To także kwestia wykorzystania języka Python w usługach i narzędziach wykorzystujących tę platformę, usługach ją tworzących oraz narzędziach służących do jej obsługi. Python jest wszechobecny w świecie Microsoft Azure. Nie mniej ciekawie jest i w drugą stronę - usługi dostępne na platformie Microsoft Azure mogą być, i są, szeroko wykorzystywane w aplikacjach i rozwiązaniach napisanych w języku Python.

## Python na Microsoft Azure
Możliwości uruchomienia kodu Python na platformie Microsoft Azure jest wiele - od aplikacji web (Azure App Service Web Apps), przez serverless pod postacią Azure Functions czy Azure container Instances, po usługi infrastruktury, takie jak klastry Kubernetes, maszyny wirtualne z systemami Linux, Windows i BSD. Nieco oddzielną kategorię dla środowisk uruchomieniowych Python na Azure tworzą platformy przetwarzania danych, takie jak Azure Data Lake Analytics, Azure Data Factory czy Azure HDInsights (Hadoop as a Service) oraz platforma przetwarzania HPC - Azure Batch.

Kwestia interoperacyjności w kontekście uruchamiania kodu Python na platformie Azure jest jasna - Azure App Service Web Apps (a także API Apps, bazujące na tych samych usługach), Azure Functions jak i Azure Container Instances, Batch oraz HDInsights bazują - wedle uznania - na systemach z rodziny Linux lub Windows. Wybór leży po stronie użytkownika. Ciężko jest powiedzieć, że jedna ze stron jest faworyzowana - obie mają plusy i minusy. Środowiska uruchomieniowe oparte o stos Microsoft wymagają znajomości narzędzi i produktów Microsoft, zaś środowiska oparte o stosy otwarte, bazują na ogół na konteneryzacji.
W przypadku rozwiązań takich jak maszyny wirtualne, Azure Batch czy HDInsights, mamy do czynienia ze środowiskami zwirtualizowanymi, gdzie bazą jest system operacyjny - Linux, Windows bądź BSD.

W artykule tym nie mamy dość miejsca, aby opisać wszystkie środowiska uruchomieniowe dla aplikacji Python w Azure - naświetlę tylko te (moim zdaniem) najciekawsze. Maszyny wirtualne to najpopularniejsza odmiana rozwiązań infrastrukturalnych, dostępnych jako usługa (IaaS). W ich przypadku, podobnie jak w przypadku klastrów bazujących na orkiestracji - np. Kubernetes - kultura pracy i nawyki (dev, ops i devops) nie różnią się znacząco od tych, które mamy wypracowane na środowiskach lokalnych - nie ważne czy deweloperskich, czy produkcyjnych. Kwestię maszyn wirtualnych i klastrów zostawiam zatem bez zagłębiania się w szczegóły na temat uruchamiania na nich kodu Python - nie ma w nich nic odkrywczego, ani wartego cennego miejsca na amach tego wydawnictwa.

W połowie drogi pomiędzy maszynami wirtualnymi (IaaS), a usługami platformy jako usługi (PaaS), znajdziemy Azure Batch, która to usługa jest z pewnością warta przedstawienia. Jest to mechanizm niezwykle potężny, należący do najstarszych usług w Azure, ale jednocześnie mało znany i niezwykle popularny - w kręgach naukowych i wyspecjalizowanych, ale jednak. Czym jest Azure Batch?

### Azure Batch
„Compute job scheduling service” - tak przedstawiana jest ta usługa na stronach azure.com. Usługa Azure Batch umożliwia wydajne uruchamianie aplikacji równoległych oraz aplikacji do obliczeń o wysokiej wydajności - wszystko to w dowolnej skali. W Azure Batch definiujemy zasoby obliczeniowe których użyjemy, aby wykonywać zadania przy użyciu aplikacji czy skryptów - bez ręcznego konfigurowania infrastruktury i zarządzania nią. 

Załóżmy, że mamy stworzoną w języku Python aplikację do obliczeń równoległych, wykorzystującą protokół MPI (np. za pomocą mpi4py). Aplikacja wymaga przynajmniej 10 maszyn, każda z nich musi mieć przynajmniej 16 rdzeni CPU i co najmniej 96GB RAM. Maszyny muszą mieć możliwość komunikacji z użyciem RDMA (np. InfiniBand). Na każdej z maszyn mamy mieć system operacyjny Linux, np. Ubuntu Server 16.04 LTS, oraz zestaw zależności aplikacji (sudo apt install build-essential && sudo pip3 install -r requirements.txt).

Naszym zadaniem jest uruchomić 10 maszyn o zadanej konfiguracji, skopiować kod aplikacji, zainstalować zależności, uruchomić aplikację, śledzić stan całego systemu (etap procesu na jakim są poszczególne maszyny). Na własnej infrastrukturze potrzebowalibyśmy 160 rdzeni i 960GB RAM oraz systemu orkiestracji (np. Ansible czy Puppet) - inwestycja byłaby uzasadniona, gdyby system był wykorzystywany 24/7/365. Co jednak w przypadku, gdy system będzie wykorzystywany raz w tygodniu? Raz w miesiącu? Raz w roku? Raz w życiu? Azure Batch.

W Azure Batch definiujemy/tworzymy dwie rzeczy. Pierwszą z nich jest skrypt Python w którym określamy infrastrukturę, która napędzi nasz system (np. 10 maszyn Standard_H16r, każda z 16 vCPU i 112GB RAM oraz wsparciem dla RDMA). W skrypcie tym określamy też proces przygotowania maszyn - np. instalację zależności - oraz wskazujemy aplikację / skrypt, który ma zostać uruchomiony na każdej z maszyn po jej uruchomieniu i przygotowaniu.
Drugą rzeczą, której potrzebujemy, jest aplikacja / skrypt, na który wskazujemy - nie ma znaczenia jaki jest jej charakter. Może to być aplikacja matematyczna, finansowa, statystyczna. Może wykorzystywać MPI z użyciem RDMA pomiędzy maszynami.

Jedną komendą wysyłamy oba elementy do Azure i dostajemy możliwość monitorowania stanu systemu w czasie - uruchamianie maszyn, przygotowanie, start aplikacji, wykonywanie, zakończenie, a co najważniejsze, możemy całą tę infrastrukturę usunąć automatycznie wraz z zakończeniem działania systemu. Zapłacimy tylko za czas działania maszyn (włączonych systemów operacyjnych).

Koszt jednej godziny działania takiego systemu (10 maszyn Standard_H16r), to około 18 EUR.

Za mało mocy?

10 maszyn po 128 rdzeni, 4TB RAM i 4TB lokalnego SSD (PCI-E) każda, to koszt nieco ponad 300 EUR za godzinę. Ile można zrobić w godzinę, pozostawiam do oceny Tobie.

Głównym przedstawicielem Platform as a Service w Azure, tworzonym także  z myślą o aplikacjach Python, jest platforma aplikacji web. Microsoft Azure App Service to platforma dla aplikacji web - w naszym kontekście dla aplikacji web pisanych w języku Python. Azure App Service pozwala na uruchomienie kodu Python natywnie (dla platformy), czyli na Windows Server (2016), przy użyciu dowolnego serwera aplikacji, choć wbudowany i domyślny to uWSGI. Platforma ta pozwala na instalację zależności i wykonywanie skryptów/komend według zadanego przez Was schematu. Azure App Services pozwala także na uruchomienie kodu Python na systemie Linux - przy użyciu konteneryzacji (Docker) - także w konfiguracjach wielokontenerowych (compose lub k8s). Tutaj nie ma, podobnie ja w przypadku maszyn wirtualnych, nic, na co warto byłoby poświęcać pozostałe wiersze publikacji.

Dalej na horyzoncie usług platformy jako usługi, leżą kontenery w czystej formie - Azure Container Instances i Azure Container Registry.

### Azure Container Instances + Azure Container Registry
Azure ACI to platforma konteneryzacji w czystej formie - bez orkiestracji i bez konieczności zarządzania klastrami czy pojedynczymi serwerami. Wyobraźmy sobie hipotetyczną sytuację, gdzie stworzyłaś/stworzyłeś swój obraz Docker - nie jest ważne jaką spełnia rolę - czy to mikroserwis web, czy usługa analizy danych. Chcesz po prostu uruchomić ten obraz (lub zestaw obrazów). Nie interesuje Cię na jakim klastrze, na jakim serwerze - po prostu ma zostać uruchomiony. To właśnie ACI - jedna komenda i kontener jest uruchomiony „w chmurze”.

Azure Container Registry (ACR), to prywatne repozytorium obrazów Docker - do użytku nie tylko z usługami Azure (jak ACI), ale także z każdą inną usługą - także Dockerem na Twoim komputerze prywatnym. Poza funkcją przechowywania obrazów Dockerowych, ACR posiada jeszcze dwie inne, cenne cechy - potrafi budować obrazy na żądanie oraz budować obrazy automatycznie (na podstawie określonych przez Ciebie zależności).

Łącząc ACI i ACR otrzymujemy potężną platformę do zadań specjalnych, opartych o kontenery Docker. Jednym z przykładów jest rozszerzenie do Jenkinsa, które pozwala na dołączanie agentów „on demand”, gdzie agenty (np. do buildów aplikacji) uruchamiane są jako kontenery w ACI.

Płacimy wyłącznie za czas życia kontenera i zasoby jakie zużył - brak stałych opłat.

Z zupełnie innej strony platformy Microsoft Azure znajdują się usługi związane z przetwarzaniem danych - w kontekście języka Python, głównie Big Data. Jednym z flagowych przedstawicieli tej rodziny usług, a jednocześnie usługą ściśle związaną z językiem Python, jest Azure Data Lake Analytics.

### Azure Data Lake Analytics 
ADLA to implementacja Apache YARN pod postacią usługi, która wykorzystuje Azure Data Lake Store, będącym implementacją Apache HDFS. Usługa Azure Data Lake Analytics jest usługą analizy danych na żądanie, pozwalającą uprościć analizowanie danych big data. Zamiast wdrażać, konfigurować i dostosowywać maszyny, możesz pisać zapytania umożliwiające przekształcanie danych i wyodrębniać wartościowe informacje właściwie od ręki, płacąc jedynie za wykonane zadania.

Azure Data Lake Analytics wykorzystuje domyślnie język U-SQL. Możliwe jest jednak rozszerzenie funkcjonalności o Python poza standardowymi bibliotekami Pythona 3.5, ADLA posiada moduły pandas, numpy i numexpr.

Azure Data Lake Store pozwala na przechowywanie nielimitowanej ilości danych, a dane te nie muszą być w żaden sposób ustrukturyzowane - mogą być to zrzuty baz SQL, pliki JSON, TSV, CSV, TXT, a nawet materiały video.

## Azure w Python
Niezależnie od tego czy będziemy uruchamiać kod Python na Azure czy nie, a jeśli tak, to w jakiej formie - od maszyn wirtualnych, przez App Service po ACI i Data Lake Analytics - Azure posiada ważną cechę, która zmienia wiele w kwestii architektury aplikacji i całych rozwiązań - także tam, gdzie spoiwem jest Python. Cechą tą jest Azure Resource Manager - warstwa zarządzania platformą. Tworzy ją nie tylko olbrzymia mechanika, której nie widzimy, ale przede wszystkim dziesiątki interfejsów API:

[Azure REST API Reference | Microsoft Docs](https://docs.microsoft.com/en-us/rest/api/azure/)

oznacza to, że jesteśmy w stanie pisać aplikacje, które są „świadome” tego, że działają na platformie Microsoft Azure i są w stanie podejmować z nią interakcję. Od najprostszych przykładów, gdzie aplikacja działa na np. 5 maszynach wirtualnych i na podstawie ilości wiadomości na kolejce, włącza lub wyłącza kolejne instancje samej siebie; przez aplikację, która raz na dobę potrafi utworzyć zadanie kopiowania danych z bazy SQL (za pomocą Azure Data Factory) do Azure Data Lake Store, a następnie uruchomić zadanie przekształcenia i analizy tych danych za pomocą Azure Data Lake Analyics; po scenariusz w którym ta sama aplikacja dwa razy w miesiącu uruchamia systemy billingowania milionów klientów, uruchamiając zadanie Azure Batch na setkach serwerów. Frontend takiej aplikacji może być uruchomiony na Azure App Services Web Apps i automatycznie skalowany, a mikroserwisy wspomagające procesy biznesowe, uruchamiane w Azure Container Instances. Nic nie stoi na przeszkodzie, aby maszyny wirtualne dla backendu i aplikacji web na froncie, zastąpić zarządzanymi klastrami Kubernetes, gdzie aplikacja sama będzie podejmowała decyzję o dołączeniu kolejnych nodów i sama wykona tę operację.

Wykorzystanie chmury publicznej - Microsoft Azure - nie wiąże się najczęściej z pokonaniem barier technologicznych. Najczęstsze bariery występują w umysłach architektów, programistów i menadżerów. 

 Przypisy:

[Dokumentacja techniczna, interfejs API i przykłady kodu | Microsoft Docs](https://docs.microsoft.com/)
[Wikipedia](https://www.wikipedia.org/)