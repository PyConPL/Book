# **Wzorce projektowe w Python**

Co, gdyby okazało się, że zupełnie inna osoba w zupełnie innym czasie i przestrzeni logiki biznesowej stanęła przed dokładnie takim samym problemem projektowym jak ty w tej chwili? Co, jeśli takich osób było więcej niż jedna, a ich wiedza i doświadczenia są zebrane w jednym miejscu i gotowe do użycia? Znajomość koncepcji rozwiązań powszechnych problemów w połączeniu z zasadą 80/20 (20% Twojej pracy wystarczy na wygenerowanie 80% rezultatów) może okazać się bardzo wydajną bronią, która powinna być w rękach każdego programisty.

  

## Czym są wzorce projektowe?

W inżynierii oprogramowania wzorzec projektowy jest ogólnie powtarzalnym rozwiązaniem często występującego problemu w projektowaniu oprogramowania. Jest to opis lub szablon rozwiązania problemu, który można wykorzystać w wielu różnych sytuacjach. Wzorce nie udostępniają gotowego kodu, a jedynie ogólne sposoby rozwiązywania problemów w fazie projektowania. Należy je samodzielnie zaimplementować w konkretnej aplikacji.

  

## Wspólny słownik

O ile łatwiej jest dogadać się z kimś, używając wspólnego słownika, nie zaczynając wszystkiego od Adama i Ewy. Pozwoli to nie tylko na przekazanie większej ilości informacji mniejszą ilością słów, ale również pomoże myśleć o architekturze aplikacji bardziej abstrakcyjnie na poziomie wzorca, a nie konkretnie na poziomie obiektu.

  

## Wynalazek czy odkrycie?

Skąd wzięły się wzorce projektowe? Czy za każdym ze wzorców stoi genialny autorytet, który wytyczył drogę rozwiązywania danego problemu? Czy jest to praktyczna odpowiedź inżynierii, na zadany problem, która została sprawdzona w boju? Krokiem milowym w dziedzinie wzorców projektowych jest książka *Design Patterns: Elements of Reusable Object-Oriented Software* autorstwa Bandy Czterech (GoF), w której został wykonany ogrom pracy polegającej na przyjrzeniu się różnym udanym systemom i wyciągnięciu z nim koncepcji rozwiązań tych samych problemów, a następnie nazwaniu ich i pogrupowaniu. Pokazuje to, że wzorce projektowe rodzą się w praktycznym środowisku, a następnie są odkrywane.

  

## Wzorce Bandy Czterech

W artykule i na prezentacji zostaną przedstawione wzorce w wyżej wspomnianej *Design Patterns: Elements of Reusable Object-Oriented Software,* książki co nie oznacza, że są to jedynie istniejące wzorce (tylko w książce jest ich 23, zostanie omówionych 6).

### Strategia
Definiuje rodzinę algorytmów, pakuje je jako oddzielne klasy i powoduje, że są w pełni wymienne. Zastosowanie tego wzorca pozwala na to, aby zmiany w implementacji algorytmów przetwarzania były całkowicie niezależne od strony klienta.

  

	      
	import abc


	class Context:
	    def __init__(self, strategy):
	        self._strategy = strategy

	    def context_interface(self):
	        self._strategy.algorithm_interface()


	class Strategy(metaclass=abc.ABCMeta):
	    @abc.abstractmethod
	    def algorithm_interface(self):
	        pass


	class ConcreteStrategyA(Strategy):
	    def algorithm_interface(self):
	        pass


	class ConcreteStrategyB(Strategy):
	    def algorithm_interface(self):
	        pass


	def main():
	    concrete_strategy_a = ConcreteStrategyA()
	    context = Context(concrete_strategy_a)
	    context.context_interface()

Dzięki kompozycji możemy zmieniać zachowanie obiektu w czasie działania programu tak długo, jak długo obiekty, których używamy do kompozycji, będą implementować dany interfejs.


### Stan
Umożliwia obiektowi zmianą zachowania wraz ze zmianą jego wewnętrznego stanu. Po zmianie funkcjonuje on jako inna klasa. Wzorzec ten hermetyzuje stan obiektu w odrębnych klasach, delegując do nich odpowiedzialność obsługi konkretnych zdarzeń. Funkcjonowanie jako inna klasa jest realizowane poprzez kompozycję i odwoływanie się do różnych obiektów stanu.

  

    import abc

	class Context:
	    def __init__(self, state):
	        self._state = state

	    def request(self):
	        self._state.handle()


	class State(metaclass=abc.ABCMeta):
	    @abc.abstractmethod
	    def handle(self):
	        pass


	class ConcreteStateA(State):
	    def handle(self):
	        pass


	class ConcreteStateB(State):
	    def handle(self):
	        pass


	def main():
	    concrete_state_a = ConcreteStateA()
	    context = Context(concrete_state_a)
	    context.request()

  

Warto zwrócić uwagę, że zastosowanie wzorca Stanu prowadzi do zwiększenia liczby klas w projekcie, jest to cena za elastyczność i jeśli przewidujemy zwiększającą się liczbę klas, będzie to rozwiązanie zawsze korzystne. Pocieszeniem jest, że klienci nie wchodzą nigdy w bezpośrednią reakcję ze stanami a jedynie przez Kontekst.

  




### Singleton
Wzorzec zapewniający, że klasa będzie miała tylko i wyłącznie jedną instancję obiektu i zapewnia globalny punkt dostępu do tej instancji.

  

    class Singleton(type):
	    def __init__(cls, name, bases, attrs, **kwargs):
	        super().__init__(name, bases, attrs)
	        cls._instance = None

	    def __call__(cls, *args, **kwargs):
	        if cls._instance is None:
	            cls._instance = super().__call__(*args, **kwargs)
	        return cls._instance


	class MyClass(metaclass=Singleton):
	    pass


	def main():
	    m1 = MyClass()
	    m2 = MyClass()
	    assert m1 is m2

Można byłoby zadać pytanie, czy nie wystarczyłoby użyć do tego zmiennych globalnych? Zwróćmy uwagę, że wzorzec ma 2 założenia: 1 - zapewnienie istnienia tylko jednej instancji obiektu 2- zapewnienie globalnego punktu dostępu zmienne globalne mogą zapewnić realizację drugiego z tych postulatów, ale nie pierwszego.

  

### Metoda Fabrykująca
Definiuje interfejs pozwalający na tworzenie obiektów, ale pozwala klasą podrzędnym decydować jakiej klasy obiekty zostanie stworzony. Wzorzec ten przekazuje więc za tworzenie obiektów do klas podrzędnych.

    import abc

	class Creator(metaclass=abc.ABCMeta):
	    def __init__(self):
	        self.product = self._factory_method()

	    @abc.abstractmethod
	    def _factory_method(self):
	        pass

	    def some_operation(self):
	        self.product.interface()


	class ConcreteCreator1(Creator):
	    def _factory_method(self):
	        return ConcreteProduct1()


	class ConcreteCreator2(Creator):
	    def _factory_method(self):
	        return ConcreteProduct2()


	class Product(metaclass=abc.ABCMeta):
	    @abc.abstractmethod
	    def interface(self):
	        pass


	class ConcreteProduct1(Product):
	    def interface(self):
	        pass


	class ConcreteProduct2(Product):
	    def interface(self):
	        pass


	def main():
	    concrete_creator = ConcreteCreator1()
	    concrete_creator.product.interface()
	    concrete_creator.some_operation()

  

Wygląda na to, że jedyne co robimy, to przenosimy odpowiedzialność tworzenia obiektów do innych podklas. I tak jest to prawda, hermetyzujemy miejsce, które podlega zmianom, które może mieć wielu klientów dzięki temu mamy tylko jeden element, który będzie podlegał modyfikacjom podczas zmian w systemie.

  

### Dekorator
Po pierwsze wzorzec Dekorator nie ma nic wspólnego z dekoratorami, czyli natywną właściwością języka Python.

Pozwala na dynamiczne przydzielanie danemu obiektowi nowych zachowań, dekoratory dają elastyczność do tej, jaką dają dziedziczenie, oferują w zamian znacznie rozszerzoną funkcjonalność dodawania funkcjonalność w sposób dynamiczny.

	import abc

	class Component(metaclass=abc.ABCMeta):
	    @abc.abstractmethod
	    def operation(self):
	        pass


	class Decorator(Component, metaclass=abc.ABCMeta):
	    def __init__(self, component):
	        self._component = component

	    @abc.abstractmethod
	    def operation(self):
	        pass


	class ConcreteDecoratorA(Decorator):
	    def operation(self):
	        self._component.operation()


	class ConcreteDecoratorB(Decorator):
	    def operation(self):
	        self._component.operation()


	class ConcreteComponent(Component):
	    def operation(self):
	        pass

	def main():
	    concrete_component = ConcreteComponent()
	    concrete_decorator_a = ConcreteDecoratorA(concrete_component)
	    concrete_decorator_b = ConcreteDecoratorB(concrete_decorator_a)
	    concrete_decorator_b.operation()

Obiekty dekorujące są tego samego typu co obiekty dekorowane, obiekt podstawowy może zostać zawinięty w jeden lub w większą ilość dekoratorów. Dekorator dodaje swoje zachowanie przed lub po delegowaniu do obiektu dekorowanego właściwego zadania.

  

### Fasada
Zapewnia jeden, zunifikowany interfejs dla całego zestawu interfejsów określonego podsystemu. Fasada tworzy nowy interfejs wysokiego poziomu, który powoduje, że korzystanie z całego podsystemu staje się łatwiejsze.

      
	class Facade:
	    def __init__(self):
	        self._subsystem_1 = Subsystem1()
	        self._subsystem_2 = Subsystem2()

	    def operation(self):
	        self._subsystem_1.operation1()
	        self._subsystem_1.operation2()
	        self._subsystem_2.operation1()
	        self._subsystem_2.operation2()


	class Subsystem1:
	    def operation1(self):
	        pass

	    def operation2(self):
	        pass


	class Subsystem2:
	    def operation1(self):
	        pass

	    def operation2(self):
	        pass


	def main():
	    facade = Facade()
	    facade.operation()

  

Podczas projektowania i tworzenia systemu powinniśmy zwracać szczególną uwagę na liczbę klas współpracujących z sobą i ograniczać interakcję tylko do potrzebnego minimum. Pozwala to uniknąć sytuacji, w których wiele różnych klas jest z sobą ściśle powiązanych, a zmiana w jednej klasie powoduje wiele zmian w innych klasach.

## Źródła

 - [https://sourcemaking.com/](https://sourcemaking.com/)
 - *Rusz głową Wzorce projektowe* Autorzy: Eric Freeman, Bert Bates, Kathy Sierra, Elisabeth Robson
 - *Design Patterns: Elements of Reusable Object-Oriented Software* Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides
