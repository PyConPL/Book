#Porozmawiaj ze swoją aplikację - Kamil Kujawiński i Marcin Najtkowski

## Systemy IVR

IVR (ang. Interactive Voice Response) to nazwa systemu w telekomunikacji, umożliwiającego interaktywną obsługę osoby dzwoniącej. IVR ma więc funkcjonalność automatycznego Call center (lub jego części). [^ivr_wiki]  System IVR może być zainstalowany bezpośrednio u klienta, w sieci PSTN, a także jako aplikacja korzystająca z uług IaaS. Ostatniemu rozwiązaniu poświęcimy ten artykuł oraz naszą prezentację.

[^ivr_wiki]: https://pl.wikipedia.org/wiki/Interactive_Voice_Response

Najpopularniejszą funkcją systemów IVR jest wybór języka, autoryzacja klienta (np. przy pomocy numeru PIN), częściowa lub w pełni automatyczna obsługa przez telefon. Wydawać by się mogło, że używanie telefonów do komunikacji z systemami to przeszłość. Jednak różni ludzie mają różne potrzeby, a szeroki wachlarz kanałów dostępu pozwala zwiększyć zasięg naszych usług. Osoby często i długo podróżujące samochodem mogą zaoszczędzić sporo czasu telefonicznie robiąc zakupy, płacić rachunki, zamawiać ubezpieczenia, rezerować bilety do kina czy teatru. Starsze osoby mające problemy z obsługą komputerów, mogą preferować korzystanie z telefonów, które już dobrze znają.


## Produkty dostępne na rynku

Rynek dostawców usług telekomunikacyjnych działających w chmurze jest bardzo duży. Jest wiele firm, które różnią się możliwościami, infrastrukturą i przede wszystkim cenami. Najważniejszym dla nich rynkiem są Stany Zjednoczone i to tamtejsi klienci mogą wykorzystać 100% dostępnych możliwości. Nawet Brytyjczycy nie mogą się cieszyć pełnym wsparciem dla ich języka, ponieważ wiele opcji jest ograniczona do amerykańskiej wersji języka angielskiego.

W tabeli poniżej przedstawiliśmy elementy, które mogą wpłynąć na wybór dostawcy, ale przede wszystkim pokazać w jakich segmentach operują dostawcy.


|  | Plivo | Tropo | Twilio |
|----------------------------------------------------------------------------------------------|:------------------------:|:---------------------------------:|:------------------------:|
| Ceny (polski numer miesięcznie / minuta rozmowy wychodzącej / minuta rozmowa przychodzącej) | 0,8$ / 2,35¢-7,3¢ / 0,5¢ | 10$ / 5-7¢ / 3¢ | 1$ / 2¢-7,5¢ / 0,75¢  |
| Serwery | dedykowane | Voxeo [^cisco_confidentiality] | AWS |
| Paczka w PyPi | plivo | tropo-webapi-python | twilio |
| Synteza mowy / język polski | 16 języków / tak | 25 języków / tak | 26 języków / tak |
| Transkrypcja nagrań | tylko angielski | tylko angielski | tylko angielski |
| Rozpoznowanie mowy / język polski | tak / nie | tak / tak | nie / nie |
| Standardy | PlivoXML | VoiceXML, SSML, SRGS | TwiML |
| SMS / MMS | tak / nie | tak / nie | tak / tylko USA i Kanada |
| Numery telefonów / polskie numery | 55 krajów / tak | 28 krajów / tak | 44 krajów / tak |
| Instalacja on-premises | tak (open source) | tak (licencja) | nie |
| Najwięksi użytkownicy | Mozilla, Netflix | Deutsche Telekom, IBM [^cisco_confidentiality] | Uber, Paypal, Coca-Cola |


Zdecydowanie najpopularniejszym rozwiązaniem na rynku jest Twilio. Jednak z różnych względów jest to rozwiązanie, które nie odpowiada wszystkim użytkownikom. Twilio nie posiada własnej serwerowni - korzysta z Amazon Web Services. Krytycy uważają, że wirtualne maszyny są zdecydowanie mniej efektywne w przetwarzaniu dźwięku. Dla wielu firm niedopuszczalne także jest udostępnianie swoich danych poza serwery firmowe. Na takie zapotrzebowanie odpowiadają Tropo oferując możliwość instalacji On-Premises w pakiecie Enterprise oraz Plivo, które otworzyło kod źródłowy na licencji Mozilla Public License Version 1.1.

Tak jak w przeglądarkach internetowych uznanym standardem jest HTML, tak w komunikacji głosowej człowiek - komputer standardem jest VoiceXML (VXML)[^voicexml_wiki]. Przy pomocy tego formatu definiujemy syntezę i rozpoznawanie mowy, zarządzenie rozmową oraz odtwarzanie dźwięku. Istnieją specyfikacje rozszerzające, które pozwalają na definicję gramatyki rozpoznawanej mowy (SRGS), opis sposobu syntezy mowy (SSML) oraz kilka innych. Specyfikacja VoiceXML pozwala na stworzenie całej aplikacji i zainstalowanie jej po stronie klienta, jednak większość dostawców nie wspiera w pełni tych standardów stawiając na własne formaty oraz większą rolę API.

Większość graczy na rynku zrezygnowała z korzystania ze standardu VoiceXML i utworzyła własne języki komunikacji z API - tak powstały PlivoXML i TwiML. Możliwości tych języków są zbieżne z VoiceXML.

Nie zawsze stworzenie własnego Call Center wymaga pracy programistów, w prostych przypadkach menadżer może sobie wyklikać cały scenariusz rozmowy z klientem. W tym celu Twilio stworzyło otwarty projekt OpenVBX, który oczywiście korzyta z usług Twilio. Użytkownik ma możliwość przy pomocy techniki drag &amp; drop stworzyć system IVR z menu tonowymi, nagrywaniem rozmów i przekierowywaniem połączeń do wybranych numerów. Jak wspomnieliśmy OpenVBX jet ograniczony wyłącznie do korzystania z Twilio, dlatego też powstała zjailbreakowana wersja, która współpracuje z Tropo. Zawsze to jakiś wybór.

[^cisco_confidentiality]: Od momentu przejęcia Tropo przez Cisco wiele informacji nie jest ujawnianych.
[^voicexml_comparision]: http://stackoverflow.com/questions/28801353/what-are-the-differences-between-voicexml-and-twiml-plivoxml
[^voicexml_wiki]: https://en.wikipedia.org/wiki/VoiceXML

## Twilio 

Jedną z bardziej popularnych, jeśli nie najpopularniejszą platformą umożliwiającą implementację "interfejsu telefonicznego" we własnych projektach jest - jak już wspomnieliśmy - Twilio. Rzut okiem na listę firm i organizacji korzystających z ich rozwiązań rozwiewa ewentualne wątpliwości - figurują tam m.in. ebay, Uber, airbnb, a nawet filadelfijska policja.
Z pewnością istotną rolę w zdobywaniu popularności odgrywa dostępność i przystępność produktów spod szyldu Twilio. Oferowane w modelu IaaS, pozwalają wzbogacić system o funkcjonalność wykonywania i odbierania połączeń (do wykorzystania out-of-the-box syntezator mowy w wielu językach) oraz wysyłania i odbierania wiadomości tekstowych w sposób dziecinnie prosty. A to daje szerokie pole do popisu - powiadomienia SMS, telekonferencje, alarmy, automatyczna infolinia, autoryzacja i wiele, wiele innych, gotowe do użycia w przeciągu kilku godzin. Najważniejsze jest to, że nie trzeba się martwić o skomplikowaną infrastrukturę. Oczywiście usługi nie są darmowe, jednak ich ceny wydają się rozsądne nawet dla prywatnych projektów czy małych firm, nie wspominając o porównaniu do kosztów zbudowania podobnych rozwiązań od podstaw. Warto przy okazji zauważyć, że Twilio dość aktywnie wspiera developerów i uczestniczy m.in. w organizacji hackathonów - na takiej formie promocji korzystają obie strony.

Połączenia i wiadomości wysłane za pośrednictwem Twilio dotrą do niemal 200 krajów na całym świecie, natomiast odbiór poprzez lokalne numery możliwy jest w ponad 40 krajach. Możemy więc założyć kilka numerów i udostępnić własną aplikację na lokalnych rynkach w Polsce, Niemczech, Meksyku, Portoryko i Hong Kongu.

Komunikacja z Twilio odbywa się dwukierunkowo. Akcje wykonywane przez aplikację wywołują metody RESTowego API (`api.twilio.com`). Za reakcję na zdarzenia odpowiedzialne jest już nasze własne API, do którego zapytania kieruje Twilio, oczekując odpowiednich komunikatów XML.
Korzystanie z obu wymienionych ułatwia udostępniona przez Twilio biblioteka (`pip install twilio`). Moduł `twilio.rest` wykorzystujemy np. w celu zainicjowania połączenia czy wysłania wiadomości. Zaś do generowania XML-owych… tzn. TwiML-owych odpowiedzi obsługujących odbiór połączeń i wiadomości, używamy `twilio.twiml`.

Aby rozpocząć, należy w pierwszej kolejności - tu bez niespodzianek - założyć konto. Następnie wybieramy kraj i numer telefonu (w zależności od lokalizacji, niektóre numery umożliwiają tylko obsługę wiadomości tekstowych lub połączeń). Pozostaje jeszcze uzupełnić adres naszego API, zapisać SID oraz token.

Krótki przykład najlepiej zobrazuje tę prostotę, którą tak się zachwycamy.
```python
>>> from twilio.rest import TwilioRestClient
>>> client = TwilioRestClient(MY_SID, MY_TOKEN)
>>> client.messages.create(to='+48123456789', from_=MY_NUMBER, body='Hello world!')
```

Tym sposobem zostało wykonane zapytanie do RESTowego API, co z kolei poskutkowało wysłaniem SMSa.

IVR wymaga już nieco więcej wkładu, niemniej nadal jest stosunkowo łatwy do zaimplementowania. Poniżej fragment kodu - widok Django - stanowiący bazę pod IVR. Dzwoniący wybiera dział, z którym chce się połączyć. Po dokonaniu wyboru rozmowa zostaje przekierowana na odpowiedni numer.

```python
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View
from twilio import twiml

class IVR(View):
    """Główny widok IVR"""
    
    # Adresy kolejnych widoków, w zależności od wybranej opcji
    choices = {
        '1': reverse('incoming_complaints'),
        '2': reverse('incoming_sales'),
        '3': reverse('incoming_consultant'),
        '0': reverse('incoming_tech'),
    }

    def post(self, request):
        response = twiml.Response()
        choice = request.POST.get('Digits')
        if choice:
            if self.choices.get(choice):
                response.redirect(self.choices[choice])
                return HttpResponse(response)
            else:
                response.say(
                    'Wybrano niewłaściwą opcję.',
                    voice='alice',
                    language='pl-PL',
                )

        with response.gather(
            numDigits=4,
            action=reverse('ivr'),
            method='POST',
            timeout=10,
        ) as response:
            response.say(
                'Aby połączyć się z działem reklamacji, wybierz jeden. '
                'Aby połączyć się z działem handlowym, wybierz dwa. '
                'Aby połączyć się z działem technicznym, wybierz trzy. '
                'W celu połączenia z konsultantem, wybierz zero.',
                voice='alice',
                language='pl-PL',
                loop=3,
            )
        return HttpResponse(response)
```

Dzięki prostej obsłudze przekierowań aplikację można dowolnie rozbudowywać, dokładając kolejne widoki zwracające komunikaty TwiML. A kiedy głos Alice stanie się męczący, nic nie stoi na przeszkodzie, by nagrać własne komunikaty. 

Co dalej? Twilio przygotowało dość obszerną dokumentację. I choć nawigacja wydaje się umiarkowanie intuicyjna, dokumentacja pokrywa zdecydowaną większość dostępnych funkcjonalności oraz ich kombinacji i stanowi dobry materiał do dalszej eksploracji tematu. Do czego gorąco zachęcamy.



## Bibliografia

https://www.twilio.com/
https://www.plivo.com/
https://www.tropo.com/

