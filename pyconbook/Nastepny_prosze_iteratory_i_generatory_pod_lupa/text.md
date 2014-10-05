# Następny proszę: iteratory i generatory pod lupą
## Jan Kaliszewski


*Artykuł ten stanowi uzupełnienie konferencyjnego wystąpienia o analizę (obszerniejszą niż to możliwe w ramach samej prezentacji) konkretnego przypadku zastosowania pythonowych generatorów. Na prostym, ale możliwie realistycznym, "z życia wziętym" przykładzie pokazuję, jak wykorzystanie generatorów może pomóc w stopniowym powstawaniu coraz lepszego kodu: eleganckiego, czytelnego i nadającego się do wielokrotnego użycia.*


By móc zaprząc generatory do konkretnego zadania, stwórzmy narzędzie przetwarzającą logi (dzienniki systemowe jakiegoś hipotetycznego serwera). Załóżmy przy tym, że:

* dane odczytywać będziemy z pliku (bądź podobnego źródła, np. uniksowego potoku);
* plik jest potencjalnie bardzo duży (nie powinniśmy naraz wczytywać całości do pamięci, lecz raczej przetwarzać dane strumieniowo);
* każdy rekord logów (danych wejściowych) to 1 wiersz składający się z następujących pól (rozdzielonych znakami tabulacji):
  * *data i czas* (np. ``2013-10-17 22:43:01.102378``),
  * *nazwa poziomu logowania* (np. ``WARNING``),
  * *komunikat* (dowolny tekst);
* dane wejściowe są zawsze prawidłowe (to drobne uproszczenie pozwoli nam pominąć obsługę błędów);
* przetwarzanie logów polegać ma na:
  * parsowaniu poszczególnych rekordów,
  * filtrowaniu ich -- czyli przepuszczaniu w oparciu o określone kryteria, np. *tylko rekordy o poziomie logowania ``ERROR`` i ``CRITICAL``*,
  * formatowaniu danych w nowy sposób, np. z zastosowaniem innego separatora pól, innego formatowania *daty i czasu*, z pominięciem pola *nazwa poziomu logowania* itp.;
* rezultat zapisywać będziemy do nowego pliku (bądź podobnego zasobu, np. gniazda sieciowego).

Ponadto przyjmijmy, że na potrzeby naszego przykładu:

* używać będziemy Pythona w wersji *3.3* (obecnie najnowszej),
* format rekordu danych wejściowych określimy za pomocą stałych zdefiniowanych na samym początku programu

\null

      import re
      from datetime import datetime
       
      STANDARD_RECORD_REGEX = re.compile(r'''
        (?P<datetime>[^\t]+)\t
        (?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\t
        (?P<message>.*)\n''', re.VERBOSE)

      # <datetime> field -- in terms of datetime.strptime():
      STANDARD_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

### Skrypt pisany na kolanie

Gdyby zrealizować nasze zadanie w formie skryptu do jednorazowego użytku, dalsza część programu mogłaby wyglądać tak:

    def process_log(log_path, output_path):
        with open(log_path) as log, \
             open(output_path, 'w') as output:
            for record in log:
                # parse record
                record = STANDARD_RECORD_REGEX.match(record).groupdict()
                # filter by log level
                if record['level'] not in ('ERROR', 'CRITICAL'):
                    continue
                # parse date/time
                record['datetime'] = datetime.strptime(
                    record['datetime'], STANDARD_DATETIME_FORMAT)
                # format and write
                output.write('{datetime:%x %X} {message}\n'
                             .format_map(record))

    process_log('input.log', 'output-0.log')

Wszystkie czynności: otwieranie plików, odczyt, parsowanie, filtrowanie, formatowanie, zapis -- umieściliśmy w jednej funkcji, ustalając "na sztywno" ich parametry. Ten kod aż prosi się o refaktoryzację.


### Biblioteka do wielokrotnego użytku


By móc elastycznie i wygodnie określać sposób parsowania i kryteria filtrowania danych oraz styl formatowania ich na wyjściu -- wyprowadźmy poszczególne czynności do osobnych funkcji, np.:

    def level_filter(record):
        if record['level'] in ('ERROR', 'CRITICAL'):
            return record
        return None  # explicit is better than implicit :)

Skoro zaś zależy nam na elastyczności -- przydatna będzie też parametryzacja poszczególnych działań:

    def level_filter(record, *levels_to_keep):
        if record['level'] in levels_to_keep:
            return record
        return None

    def record_parser(record, record_regex):
        return record_regex.match(record).groupdict()

    def datetime_parser(record, format_string):
        return dict(record,
                    datetime=datetime.strptime(record['datetime'],
                                               format_string))

    def output_formatter(record, format_string):
        return format_string.format_map(record)

By spiąć to wszystko w całość, głównej funkcji przetwarzającej dane pozwolimy przyjmować jako parametr sekwencję czynności do wykonania -- w formie listy krotek ``(<funkcja składowa>, <dodatkowy argument #1>, <dodatkowy argument #2>, ...)``. Niech funkcja ta wywołuje dla każdego rekordu po kolei zestaw otrzymanych funkcji składowych (wraz z dodatkowymi argumentami), a w razie zwrócenia przez którąś z nich wartości ``None`` -- wstrzymuje się od dalszego przetwarzania i zapisywania danego rekordu (realizując w ten sposób filtrowanie):

    def process_log(log_path, output_path, proc_sequence):
        with open(log_path) as log, \
             open(output_path, 'w') as output:
            for record in log:
                for func, *args in proc_sequence:
                    record = func(record, *args)
                    if record is None:
                        break
                else:
                    output.write(record)

Widać tu jeszcze jeden mankament: ograniczeni jesteśmy do plików tekstowych, choć równie dobrze moglibyśmy zechcieć użyć np. potoków czy gniazd sieciowych... By znieść to ograniczenie, oddzielmy samo przetwarzanie danych od operacji wejścia/wyjścia. **I tu po raz pierwszy przyda nam się generator**: nasza główna funkcja przetwarzająca, zamiast zapisywać kolejne rekordy do pliku, będzie po prostu je generować:

    def process_log(log, proc_sequence):
        for record in log:
            for func, *args in proc_sequence:
                record = func(record, *args)
                if record is None:
                    break
            else:
                yield record

Same zaś operacje wejścia/wyjścia umieścimy w osobnej funkcji (którą w razie potrzeby można będzie zastąpić inną):

    def file_to_file(log_path, output_path, proc_sequence):
        with open(log_path) as log, \
             open(output_path, 'w') as output:
            for output_str in process_log(log, proc_sequence):
                output.write(output_str)

Tak stworzona biblioteka może być wykorzystywana na różne sposoby, np.:

    file_to_file('input.log', 'output-1.log', [
        (record_parser, RECORD_REGEX),
        (level_filter, 'ERROR', 'CRITICAL'),
        (datetime_parser, DATETIME_FORMAT),
        (output_formatter, '{datetime:%y%m%d/%H%M%S.%f}:{message}\n'),
    ])

    file_to_file('input.log', 'output-2.log', [
        (record_parser, SOME_OTHER_RECORD_REGEX),
        (level_filter, 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
        (output_formatter, '@{datetime}: {message} ({level})\n'),
    ])

Może być też łatwo rozszerzana o nowe elementy:

    def old_style_formatter(record, format_string):
        return format_string % record

    def stdin_to_socket(output_socket, proc_sequence):
        for output_bytes in process_log(sys.stdin, proc_sequence):
            output_socket.sendall(output_bytes)

    stdin_to_socket(some_writable_socket, [
        (record_parser, RECORD_REGEX),
        (level_filter, 'ERROR', 'CRITICAL'),
        (old_style_formatter, '@%(datetime)s: %(message)s (%(level)s)\n'),
        (str.encode, 'utf-8', 'replace'),
    ])


### Przetwarzanie z przechowywaniem stanu


Załóżmy, że działanie serwera, którego logi przetwarzamy, opiera się na transakcjach:

1. Na początku każdej transakcji zapisywany jest do logów komunikat ``BEGIN``,
2. Następnie wykonywane są (i logowane) kolejne operacje,
3. Na koniec transakcji zapisywany jest do logów:
   * komunikat ``COMMIT``, jeżeli transakcja została zatwierdzona;
   * komunikat ``ROLLBACK``, jeżeli transakcja została unieważniona (wraz ze wszystkimi wykonanymi w jej ramach operacjami).

Spróbujmy dopisać do naszej biblioteki filtr przepuszczający **tylko rekordy pojawiające się w obrębie zatwierdzonych transakcji**

    def transaction_filter(record):
        ???

Tu mamy problem. Jak dotąd wszystkie oferowane przez naszą bibliotekę filtry (i inne funkcje składowe wywoływane przez główną funkcję przetwarzającą) **bezstanowo** przetwarzały pojedyncze rekordy -- w przypadku transakcji pojawia się jednak konieczność przechowywania stanu: najpierw czekamy, aż pojawi się rekord z komunikatem ``BEGIN``, później akumulujemy (ale jeszcze nie przepuszczamy) wszystkie dalsze rekordy, wreszcie -- albo przepuszczamy wszystkie zakumulowane rekordy (gdy pojawi się rekord z komunikatem ``COMMIT``), albo zapominamy o nich (gdy pojawi się rekord z komunikatem ``ROLLBACK``).

Jak to pogodzić z przetwarzaniem danych po jednym rekordzie? Chcielibyśmy przy tym zachować elegancki, zmodularyzowy model naszej biblioteki. Czy da się to osiągnąć bez istotnego komplikowania kodu? Okazuje się, że tak: wystarczy **przepisać nasze funkcje składowe do postaci generatorów**, które główna funkcja przetwarzająca **połączy w łańcuch** (podobny do łańcuchów uniksowych poleceń łączonych potokami, takich jak: ``df | grep home | awk '{print $5}'``)::

    def record_parser(rec_iterator, record_regex):
        for record in rec_iterator:
            yield record_regex.match(record).groupdict()

    def level_filter(rec_iterator, *levels_to_keep):
        for record in rec_iterator:
            if record['level'] in levels_to_keep:
                yield record

    def datetime_parser(rec_iterator, format_string):
        for record in rec_iterator:
            yield dict(record,
                       datetime=datetime.strptime(record['datetime'],
                                                  format_string))

    def output_formatter(rec_iterator, format_string):
        for record in rec_iterator:
            yield format_string.format_map(record)

Sama główna funkcja przetwarzająca przestanie być generatorem, lecz zwracać będzie generator (a więc sposób jej użycia, np. z poziomu funkcji ``file_to_file()``, nie zmieni się)::

    def process_log(log, proc_sequence):
        rec_iterator = log
        for gen_func, *args in proc_sequence:
            rec_iterator = gen_func(rec_iterator, *args)
        return rec_iterator

Warto zauważyć, że w czasie wykonywania kodu tej funkcji ani jeden rekord nie zostanie przetworzony -- zatem nie powinniśmy już nazywać jej *funkcją przetwarzającą*, lecz raczej *funkcją przygotowującą*: przygotowuje ona bowiem łańcuch generatorów (gotowy do "skonsumowania" np. przez pętlę ``for...`` w ``file_to_file()``).

Przy takiej konstrukcji mechanizmu przetwarzania rekordów z łatwością możemy wprowadzić funkcję składową przechowującą stan i "chomikującą" dane, taką jak nasz filtr zatwierdzonych transakcji:

    def transaction_filter(rec_iterator):
        while True:
            # omitting records beyond a transaction:
            while True:
                record = next(rec_iterator)
                if record['message'] == 'BEGIN':
                    break
            # transaction:
            transaction_buffer = []
            while True:
                transaction_buffer.append(record)
                record = next(rec_iterator)
                if record['message'] == 'ROLLBACK':
                    # forgetting accumulated records
                    break
                if record['message'] == 'COMMIT':
                    # generating accumulated records 
                    yield from transaction_buffer
                    yield record
                    break
 
Warto zwrócić uwagę na dwa szczegóły:

* W momencie wyczerpania się danych wejściowych wywołanie ``next(rec_iterator)`` skutkować będzie zgłoszeniem wyjątku ``StopIteration`` -- i nie boimy się tego: wyjątek ten spowoduje to, o co w takiej sytuacji właśnie nam chodzi, czyli zakończenie działania generatora (i propagację wyjątku ``StopIteration`` "na zewnątrz" -- czyli do kolejnego generatora w łańcuchu, bądź np. do pętli ``for...`` w ``file_to_file()``).
* W trzecim wierszu od końca zastosowano nową konstrukcję (wprowadzoną w Pythonie 3.3): ``yield from...`` -- w tym wypadku wiersz ten jest równoznaczny z ``for rec in transaction_buffer: yield rec`` (innym -- ciekawszym -- cechom i zastosowaniom konstrukcji ``yield from...`` poświęcona jest osobna część konferencyjnego wystąpienia).

Ani kod funkcji wejścia/wyjścia, ani sposób ich wywoływania nie ulega zmianom -- np. wywołanie funkcji ``file_to_file()`` może wyglądać tak:

    file_to_file('input.log', 'output-3.log', [
        (record_parser, RECORD_REGEX),
        (transaction_filter,),
        (level_filter, 'WARNING', 'ERROR', 'CRITICAL'),
        (datetime_parser, DATETIME_FORMAT),
        (output_formatter, '{datetime:%x %X} {message}\n'),
    ])

### Co dalej?

Od łańcuchowania generatorów już tylko krok do generatorowych pseudo-wątków, współprogramów (*coroutines*) i innych cudów, od których nieprzyzwyczajonym może zagotować się zawartość czaszki (przynajmniej na początku). Zarówno dociekliwych i żądnych przygód, jak i całkiem od przygód stroniących (i zainteresowanych wyłącznie prostym i eleganckim kodem) -- zapraszam do zapoznania się z niezbyt może nowymi, ale świetnymi prezentacjami Davida Beazleya. Warto też czasem zajrzeć do samej dokumentacji Pythona i okolic.

### Literatura i źródła ###

* http://www.dabeaz.com/generators-uk
* http://www.dabeaz.com/coroutines/
* http://docs.python.org/3/reference/expressions.html#yield-expressions
* http://docs.python.org/3/whatsnew - (szukaj na stronie słowa ``generator``)
