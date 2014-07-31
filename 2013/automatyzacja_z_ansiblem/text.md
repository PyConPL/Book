# Automatyzacja z Ansible
## Jak zrobić, żeby zrobić i się nie narobić

Wiktor Kołodziej, Deployed.pl
Grzegorz Nosek, MegiTeam

### Hello, world

Ansible to narzędzie do automatyzacji. Można nim zrobić praktycznie wszystko to, co normalnie robi się na piechotę w shellu. Nad ręcznym logowaniem się na serwery ma jedną niezaprzeczalną zaletę: jest powtarzalny. Nie męczy się, nie nudzi i nie zapomina o drobiazgach.

Jako, że Ansible napisany jest w pythonie, to instalacja sprowadza się do:

    # pip install ansible

Żeby jednak Ansible do czegoś się przydał, trzeba mu przygotować listę serwerów, którymi będzie zarządzał („inventory”). Standardowo ma postać pliku `.ini`, gdzie nagłówki sekcji w [] to nazwy grup. Jeżeli nie utworzymy żadnej grupy wszystkie serwery będą w domyślnej grupie `all`. Na początek nam ona wystarczy - nasze inventory będzie miało jedną linijkę. Domyślnie leży ono w `/etc/ansible/hosts`, ale może się znajdować gdziekolwiek, na przykład w `inventory.txt` w bieżącym katalogu. Żeby przy każdym wywołaniu Ansible nie podawać parametru `-i inventory.txt`, możemy ustawić tę ścieżkę w środowisku:

    # echo localhost > inventory.txt
    # export ANSIBLE_HOSTS=$PWD/inventory.txt

W odróżnieniu od niektórych alternatyw, typu Puppet czy SaltStack, Ansible nie wymaga żadnej konfiguracji na zarządzanych maszynach -- nie musimy instalować agentów czy generować specjalnych kluczy. Domyślnie cała komunikacja (również z localhostem) odbywa się po SSH. Żeby nie wpisywać bez przerwy hasła, stwórzmy klucz SSH i sprawdźmy, że działa:

    # ssh-keygen
    # cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    # ssh localhost echo "TADA"

Teraz pora na przetestowanie samego narzędzia. Możemy użyć wbudowanego polecenia `ping`:

    # ansible localhost -m ping
    localhost | success >> {
        "changed": false, 
        "ping": "pong"
    }

### Co dalej?

Kolejnym podstawowym modułem jest `command`. Pozwala on wykonać dowolną komendę. Sprawdźmy np. uptime naszego localhosta:

    # ansible localhost -m command -a "uptime"
    localhost | success | rc=0 >>
     15:54:30 up 2 days,  5:50,  3 users,  load average: 0.12, 0.18, 0.22

Oprócz `ping` i `command`, Ansible oferuje całą masę innych modułów. Są one opisane na stronie [http://www.ansibleworks.com/docs/modules.html](http://www.ansibleworks.com/docs/modules.html). Można też prosto tworzyć własne rozszerzenia w dowolnym języku, który jest w stanie wygenerować format `json`. Nas zapewne najbardziej zainteresuje Python, dla którego Ansible oferuje dodatkowe ułatwienia.

Na potrzeby warsztatów przygotowaliśmy prostą aplikację. Użyjmy modułu `uri` do połączenia się z nią przez http:

    # ansible localhost -m uri -a "url=http://ansible.localdomain.pl/"
    localhost | success >> {
        "accept_ranges": "bytes",
        "changed": false,
        "content_length": "1270",
        ...
    }

Żeby się zarejestrować w aplikacji warsztatowej, trzeba jej przekazać adres MAC (unikalny ID karty sieciowej) -- tak sobie wymyśliliśmy.

Jako że mamy już Ansible zainstalowe, nie trzeba tego MACa wyciągać ręcznie z wyniku komendy typu `ip link list`. Jednym ze standardowych modułów jest `setup`, który nie zmienia nic na docelowej maszynie, ale zbiera o niej podstawowe informacje, tzw. „fakty”:

    # ansible localhost -m setup
    localhost | success >> {
        "ansible_facts": {
            "ansible_all_ipv4_addresses": [
                "172.16.0.150", 
                "192.168.1.132", 
                "192.168.122.1"
            ], 
            "ansible_all_ipv6_addresses": [
                "fe80::a11:96ff:fe7a:e134"
            ], 
            ...
        }
    }

Wśród wielu informacji zwróconych przez moduł `setup` znajdziemy również adres MAC. Aby łatwo rejestrować się w aplikacji, trzeba jakoś połączyć wspomniany wcześniej moduł `uri` oraz zgromadzone poprzez `setup` fakty. Z pomocą przychodzą tzw. playbooki, czyli listy zadań dla Ansible w formacie YAML. W większości miejsc można korzystać z systemu szablonów Jinja2, którego składnia podobna jest do składni szablonów Django.

    ---
    - hosts: all
      vars:
      - nick: nie_umiem_zmienic_nicka
      - mac: "{{ansible_default_ipv4.macaddress}}"
      tasks:
      - uri: url=http://ansible.localdomain.pl/register/{{nick}}/{{mac}}

Chcieliśmy połączyć `uri` z `setup`, użyliśmy `uri` - gdzie się podział `setup`? O ile nie określimy inaczej, moduł `setup` wykonuje się automatycznie na początku każdej grupy zadań w playbooku.

Playbooki uruchamiamy w następujący sposób:

    # ansible-playbook 01.hello-world.yml

Gratulacje, jesteś na pierwszym poziomie wtajemniczenia!

### App, app, and away

Skoro umiemy już zrobić Ansible „cokolwiek”, możemy spróbować zrobić coś przydatnego. Przygotowaliśmy prostą aplikację we Flasku, którą sobie teraz uruchomimy.

Ręcznie wyglądałoby to tak:

    # apt-get install python-virtualenv
    # adduser app
    # su - app
    $ virtualenv ~/.env
    $ git clone https://bitbucket.org/wiktor/ansible-workshop-demo-app.git demo-app
    $ cd demo-app
    $ ~/.env/bin/pip install -r requirements.txt
    $ ~/.env/bin/gunicorn hello:app -p hello.pid -D -b 0.0.0.0:8000

Najprostszy playbook będzie podobny:

    ---
    - hosts: all
      user: root
      tasks:
      - apt: pkg=python-virtualenv state=present
      - user: name=app state=present
    - hosts: all
      user: root
      sudo: true
      sudo_user: app
      tasks:
      - git: repo=https://bitbucket.org/wiktor/ansible-workshop-demo-app.git dest=/home/app/demo-app
      - pip: requirements=/home/app/demo-app/requirements.txt virtualenv=/home/app/.env
      - command: /home/app/.env/bin/gunicorn hello:app -p hello.pid -D -b 0.0.0.0:8000 chdir=/home/app/demo-app
    
Wykonujemy playbook na wszystkich hostach. Używamy modułu `apt` by zainstalować paczkę python-virtualenv. Zakładamy użytkownika `app`. Do tego momentu potrzebowaliśmy się logować jako root. Następny krok możemy już wykonać z mniejszymi uprawnieniami. 
Używamy więc modułu sudo i przełączamy się na użytkownika `app`. Kolejne kroki, czyli klonowanie repozytorium, instalacja zależności aplikacji oraz uruchomienie serwera aplikacyjnego, są już wykonywane z uprawnieniami nowego użytkownika.

W poprzednim przykładzie założyliśmy, że użytkownik, którego utworzymy, będzie się nazywał `app`. Sparametryzujmy to, nazwy mogą być przecież bardziej kreatywne.

W tym celu w pliku `inventory.txt` ustawmy zmienną `app_user` i przy okazji `app_port`:

    localhost app_user=foo app_port=8000

Rozdzielmy też playbooki - jeden niech zainstaluje to, co musimy zrobić z roota, drugi wykona zadania bezpośrednio z nowego użytkownika ze zmiennej `app_user`. Aby zalogować się bezpośrednio na nowego użytkownika, musimy mu najpierw dodać nasz klucz SSH. Kompletne playbooki mogą wyglądać wówczas tak:

    ---
    - hosts: all
      user: root
      tasks:
      - apt: pkg=python-virtualenv state=present
      - user: name={{app_user}} state=present
      - authorized_key: user={{app_user}} key="{{item}}"
        with_file: ~/.ssh/id_rsa.pub


Oraz druga część, przygotowana pod zgłoszenie portu gunicorna do aplikacji warsztatowej:

    ---
    - hosts: all
      user: "{{app_user}}"
      vars:
      - mac: "{{ansible_default_ipv4.macaddress}}"
      tasks:
      - git: repo=https://bitbucket.org/wiktor/ansible-workshop-demo-app.git dest=/home/{{app_user}}/demo-app
      - pip: requirements=/home/{{app_user}}/demo-app/requirements.txt virtualenv=/home/{{app_user}}/.env
      - command: /home/{{app_user}}/.env/bin/gunicorn hello:app -p hello.pid -D -b 0.0.0.0:{{app_port}}
                 chdir=/home/{{app_user}}/demo-app
      - uri: url=http://ansible.localdomain.pl/appup/{{nick}}/{{mac}}/{{app_port}}
      
Playbook wykonał się? Gratulacje, jesteś na drugim poziomie wtajemniczenia!

### Trudne słowo na dziś: idempotentność

Tak jak wspomnieliśmy we wstępie - playbooki są powtarzalne. Ale co to oznacza w praktyce? Otóż nasz playbook, mimo że jest w zasadzie wierną kopią poleceń z shella, ma nad nim odrobinę przewagi -- nie próbuje np. dodawać istniejącego już użytkownika ani drugi raz tworzyć virtualenva. Mimo to, część operacji wykonuje się niepotrzebnie -- po co od nowa instalować te same zależności z requirements.txt, jeżeli nie zmieniła się zawartość repozytorium? Po co uruchamiać już uruchomionego gunicorna?

Idempotentność to cecha, która oznacza, że wykonanie dwa razy tej samej czynności da taki sam efekt, jak wykonanie pojedyncze. To bardzo pożądana własność, która zapewnia uzyskanie powtarzalnych wyników.

Każdy moduł Ansible zwraca informację o tym, czy coś zmienił w stanie systemu. Dzięki temu możemy np. instalować zależności dopiero po zmianie w repozytorium:

    - git: repo=https://bitbucket.org/wiktor/ansible-workshop-demo-app.git dest=/home/{{app_user}}/demo-app
      register: git_repo
    - pip: requirements=/home/{{app_user}}/demo-app/requirements.txt virtualenv=/home/{{app_user}}/.env
      when: git_repo.changed

Zostaje jeszcze tylko idempotentne uruchamianie gunicorna. Nic prostszego:

    - command: /home/{{app_user}}/.env/bin/gunicorn hello:app -p hello.pid -D -b 0.0.0.0:{{app_port}}
               chdir=/home/{{app_user}}/demo-app 
               creates=/home/{{app_user}}/demo-app/hello.pid

Jak w takim razie tego gunicorna zatrzymać? Tu potrzebujemy modułu `shell` a nie `command`, gdyż korzystamy z funkcji tegoż shella:

    ---
    - hosts: all
      user: "{{app_user}}"
      tasks:
      - shell: kill `cat /home/{{app_user}}/demo-app/hello.pid` removes=/home/{{app_user}}/demo-app/hello.pid

Po zatrzymaniu gunicorn usuwa swój plik z ID procesu, więc kolejne uruchomienie tego playbooka nic nie zrobi, zamiast np. oprotestować brak pliku pid.
Aby przejść na kolejny poziom, ostateczny playbook z tego rozdziału powinien uwzględnić linijkę:

      - uri: url=http://ansible.localdomain.pl/appaway/{{nick}}/{{mac}}/{{app_port}}

### Bazo dużo danych

Aplikacja WWW z reguły będzie potrzebować bazy danych, w tej czy innej formie. Zainstalujmy sobie Postgresa:

    ---
    - hosts: all
      user: root
      tasks:
      - apt: pkg=postgresql state=present
    - hosts: all
      user: root
      sudo: true
      sudo_user: postgres
      tasks:
      - postgresql_user: name=demoapp password=S3CR3T
      - postgresql_db: name=demoapp owner=demoapp

Jest pewien problem -- w naszym playbooku jest zapisane hasło. Playbook stał się w tym momencie tajny/poufny/przed-przeczytaniem-skasować i nie możemy się nim na przykład pochwalić koledze. Co więcej, to samo hasło będziemy musieli podać w konfiguracji aplikacji, więc będzie już w dwóch miejscach, o których musimy pamiętać np. przy zmianie. Na ratunek przychodzi wbudowana w Ansible obsługa haseł:

      - postgresql_user: name=demoapp password={{item}}
        with_password: demoapp-db.pass

Przy pierwszym uruchomieniu takiego zadania Ansible wygeneruje losowe, 20-znakowe hasło i zapisze je w pliku `demoapp-db.pass`.

Ponieważ domyślnie Postgres przyjmuje połączenia tylko w obrębie lokalnej maszyny, musimy go trochę przekonfigurować. W tym przypadku prościej będzie dopisać odpowiednie linijki niż generować z szablonu całą konfigurację Postgresa:

    tasks:
    - lineinfile: regexp="^listen_addresses" 
                  line="listen_addresses '*'" 
                  insertafter="Connection Settings" dest=/etc/postgresql/9.1/main/postgresql.conf
      notify: restart postgres
    - lineinfile: regexp="^host all all all" 
                  line="host all all all md5" 
                  dest=/etc/postgresql/9.1/main/pg_hba.conf
      notify: restart postgres
    handlers:
    - name: restart postgres
      service: name=postgresql state=restarted


Musimy jeszcze powiedzieć naszej aplikacji, gdzie ma się łączyć. Uzupełnijmy jej playbook (tuż przed startem gunicorna):

      - template: src=config.py dest=/home/{{app_user}}/demo-app/config.py
        register: config_py
      - shell: kill `cat /home/{{app_user}}/demo-app/hello.pid` removes=/home/{{app_user}}/demo-app/hello.pid
        when: config_py.changed
  
Teraz po każdej zmianie konfiguracji Ansible automatycznie zrestartuje aplikację.

Jak ma wyglądać szablon? Na przykład tak (zawartość ma się znaleźć w pliku config.py w tym samym katalogu co playbook):

    SQLALCHEMY_DATABASE_URI = "postgresql://demoapp:{{lookup('password', 'demoapp-db.pass')}}@localhost/demoapp"

Aby wejść na kolejny poziom, dodaj do swojego playbooka rejestrację bazy (i portu na którym jest uruchomiona):

      - uri: url=http://ansible.localdomain.pl/bazo/{{nick}}/{{mac}}/{{db_port}}

### Is it webscale?

Serwis się rozwija, kolejni użytkownicy korzystają z Hello, world, czas na dostawienie kolejnego serwera. Ale najpierw potrzebujemy load balancera, który rozłoży ruch między serwerami. Postawmy nginxa z prostą konfiguracją:

    ---
    - hosts: all
      user: root
      tasks:
      - apt: pkg=nginx state=present
      - file: path=/etc/nginx/sites-enabled/default state=absent
        notify: restart nginx
      - template: src=loadbalancer.conf dest=/etc/nginx/sites-enabled/loadbalancer.conf
        notify: restart nginx
      handlers:
      - name: restart nginx
        service: name=nginx state=restarted

`notify` i `handlers` to mechanizm podobny do `when: result.changed`, z zasadniczą różnicą: wszystkie handlery uruchamiają się na końcu, po pozostałych zadaniach.

Szablon z konfiguracją, najprostszy możliwy:

    upstream demo_app {
    {% for server in groups['all'] %}
        server {{hostvars[server].ansible_default_ipv4.address}}:{{hostvars[server].app_port}};
    {% endfor %}
    }

    server {
        location / {
            proxy_pass http://demo_app;
        }
    }
Po uruchomieniu nginxa można osiągnąc kolejny stopień wtajemniczenia, dodając do playbooka:

      - uri: url=http://ansible.localdomain.pl/nginx/{{nick}}/{{mac}}/{{nginx_port}}


Dodajmy drugi serwer do inventory:

    localhost app_user=app app_port=8000
    other_host app_user=other_user app_port=8001 ansible_ssh_host=127.0.0.1

Adres IP jest konieczny, jeżeli nazwa `other_host` nie figuruje w DNS. Jeżeli używasz 127.0.0.1, czyli swojej maszyny, wybierz różne numery portów.

Uruchamiamy playbooki od nowa żeby skonfigurować nowy serwer i... zonk. Właśnie zainstalowaliśmy drugiego Postgresa, a każdy gunicorn łączy się do swojej własnej bazy. Niestety nasze serwery nie są już identyczne i musimy to uwzględnić, dzieląc je na grupy w inventory i odpowiednio podmieniając `hosts:` **we wszystkich playbookach**:

    [app]
    localhost app_user=app app_port=8000
    other_host app_user=other_user app_port=8001 ansible_ssh_host=127.0.0.1

    [loadbalancer]
    localhost
    
    [database]
    localhost


Musimy też zmienić konfigurację aplikacji, żeby łączyła się do odpowiedniej bazy danych:

    SQLALCHEMY_DATABASE_URI = "postgresql://demoapp:{{lookup('password', 'demoapp-db.pass')}}@{{db_server}}/demoapp"

Wartość zmiennej `db_server` ustalimy automatycznie. W tym celu musimy trochę rozbudować playbook konfigurujący aplikację:

    - hosts: database
    - hosts: app
      user: "{{app_user}}"
      vars:
      - db_server_host: "{{groups['database'][0]}}"
      - db_server: "{{hostvars[db_server_host].ansible_default_ipv4.address}}"
      tasks:
      - ...

W powyższym playbooku podaliśmy `hosts: database`, mimo, iż nic nie robimy nic na tej grupie.
Jednak nie do końca. Podając hosty typu `database`, poleciliśmy Ansible, by zebrał fakty, które możemy wykorzystać w dalszej części playbooka.

I to już ostatni poziom wtajemniczenia, który można osiągnąć podczas warsztatów:

      - uri: url=http://ansible.localdomain.pl/webscale/{{nick}}/{{mac}}/{{nginx_port}}


### Literatura i źródła ###

* http://www.ansibleworks.com/docs/modules.html
* https://github.com/ansible/ansible/
* https://github.com/ansible/ansible-examples/
