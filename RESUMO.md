## Singleton

### 1. Descrição e propósito

* **Problema que resolve**
  Evitar múltiplas instâncias de uma mesma classe quando só faz sentido haver **uma única instância global** (ex.: gerenciador de configuração, logger, conexão principal com recurso compartilhado). ([refactoring.guru][1])
* **Intenção principal**
  Garantir que uma classe tenha **apenas uma instância** e fornecer um **ponto de acesso global** a essa instância. ([refactoring.guru][1])
* **Contexto adequado**

  * Quando você precisa de um **estado global compartilhado**, mas quer encapsular esse estado em um objeto, não em variáveis globais soltas.
  * Quando a criação de múltiplas instâncias seria **cara**, inconsistente ou logicamente incorreta (ex.: vários “gerenciadores centrais” competindo entre si).

### 2. Estrutura

Papéis principais:

* `Singleton`

  * Classe que mantém uma **referência estática** para sua única instância.
  * Torna o construtor inacessível diretamente (privado/protegido).
  * Expõe um método estático (`getInstance()`) que cria a instância uma vez e depois a retorna sempre que chamado.

Pseudo-UML textual:

* `Client` → chama `Singleton.getInstance()`
* `Singleton`

  * `- instance : Singleton` (estático)
  * `- Singleton()` (construtor privado)
  * `+ getInstance() : Singleton`

Relações:

* **Clientes** não instanciam a classe diretamente com `new`, apenas chamam o **método de acesso estático**.
* Todos os clientes compartilham a mesma instância retornada pelo Singleton.

### 3. Quando utilizar

Cenários típicos:

* Classe que **coordena recursos globais**: gerenciador de configuração, logger central, pool de conexões, registrador de plugins.
* Quando faz sentido conceitual ter **“uma única entidade”** no domínio (ex.: kernel, gerenciador de janelas, etc.).

“Cheiros” que indicam uso:

* Uso intenso de **variáveis globais** ou singletons “caseiros” espalhados.
* Criação repetida de objetos que deveriam ser **únicos e compartilhados**.
* Dificuldade em garantir consistência de estado global.

### 4. Iterações e variações

Variações comuns:

* **Singleton preguiçoso (lazy)**: instancia o objeto somente na primeira chamada de `getInstance()`.
* **Singleton ansioso (eager)**: instancia o objeto na carga da classe (inicialização estática).
* **Thread-safe singleton**: adiciona mecanismos de sincronização ao lazy para ambientes concorrentes (locks, double-checked locking, inicialização estática segura). ([refactoring.guru][2])

Adaptações por linguagem:

* Linguagens com suporte a inicialização estática segura (Java, C#) facilitam o singleton ansioso.
* Em linguagens dinâmicas (Python, JavaScript), pode-se simular Singleton via **módulos** ou **metaclasses**.

Trade-offs:

* **Prós**: acesso conveniente, controle centralizado, inicialização tardia possível.
* **Contras**: acoplamento global, dificuldade de **testes unitários** (mocking), risco de virar “global disfarçado”, pode concentrar responsabilidade demais. ([refactoring.guru][3])

---

## Strategy

### 1. Descrição e propósito

* **Problema que resolve**
  Evitar código cheio de `if/else` ou `switch` para escolher entre **variações de algoritmos** que fazem a mesma coisa de formas diferentes (ex.: diferentes formas de cálculo, ordenação, compressão, etc.). ([refactoring.guru][4])
* **Intenção principal**
  Definir uma **família de algoritmos**, encapsular cada um em uma classe separada e torná-los **intercambiáveis** em tempo de execução. ([refactoring.guru][5])
* **Contexto adequado**
  Quando você quer poder **mudar o comportamento** de um objeto em tempo de execução, sem alterar o código desse objeto.

### 2. Estrutura

Papéis principais:

* `Strategy` (interface/abstração)

  * Declara a **assinatura do algoritmo** (ex.: `executar()`, `calcular(...)`).
* `ConcreteStrategyA`, `ConcreteStrategyB`, etc.

  * Implementações específicas do algoritmo.
* `Context`

  * Mantém uma referência para um objeto `Strategy`.
  * Delegará o trabalho para a estratégia configurada.

Pseudo-UML textual:

* `Context`

  * `- strategy : Strategy`
  * `+ setStrategy(s : Strategy)`
  * `+ execute()` → delega para `strategy`
* `Strategy`

  * `+ execute()`
* `ConcreteStrategyA` / `ConcreteStrategyB`

  * implementam `execute()`

Relações:

* `Context` **conhece** apenas a interface `Strategy`, não as implementações concretas.
* O cliente configura o `Context` com uma determinada `ConcreteStrategy` (via injeção, setter, construtor ou fábrica).

### 3. Quando utilizar

Cenários típicos:

* Várias variantes de um mesmo processo (ex.: diferentes políticas de desconto, diferentes algoritmos de ordenação, diferentes formas de roteamento).
* Necessidade de **alternar comportamento em runtime**, por configuração, preferências do usuário ou contexto.

Sinais de uso:

* Cadeias grandes de `if/else` baseadas em “tipo”, “modo” ou enum.
* Necessidade de adicionar **novos comportamentos** com frequência, sem mexer em código existente (princípio Open/Closed). ([refactoring.guru][4])

### 4. Iterações e variações

Variações:

* **Estratégia configurável em runtime**: o `Context` expõe um método `setStrategy()` para trocar durante a execução.
* **Estratégia imutável**: escolhida no construtor e nunca mais alterada.
* **Estratégias compartilhadas**: instâncias podem ser compartilhadas (stateless), reduzindo criação de objetos.

Adaptação por linguagem:

* Em linguagens com funções de primeira classe (Python, JavaScript), uma Strategy pode ser **uma função ou closure**, mas a forma OO ajuda a manter o modelo alinhado aos padrões clássicos.
* Em arquiteturas modernas, Strategy combina bem com **injeção de dependência** e contêineres IoC.

Trade-offs:

* **Prós**: elimina condicionais extensas, reduz acoplamento, facilita extensão, facilita testes (você testa cada Strategy isoladamente).
* **Contras**: aumenta o número de classes, pode ser overkill para poucos casos simples. ([refactoring.guru][5])

---

## Observer

### 1. Descrição e propósito

* **Problema que resolve**
  Manter vários objetos sincronizados com o estado de outro objeto sem criar acoplamento forte entre eles (ex.: atualizações de UI, eventos de domínio, notificações). ([refactoring.guru][6])
* **Intenção principal**
  Definir um **mecanismo de assinatura** para notificar múltiplos objetos sobre eventos que acontecem em um objeto observado, de forma desacoplada. ([refactoring.guru][7])
* **Contexto adequado**
  Quando uma mudança em um objeto requer que outros sejam notificados ou atualizados, mas você quer evitar dependências rígidas entre eles.

### 2. Estrutura

Papéis principais:

* `Subject` (Publisher)

  * Mantém uma lista de observadores.
  * Proporciona métodos para **inscrever/desinscrever** (`attach/detach`).
  * Notifica observadores quando um evento acontece (`notify()`).
* `Observer` (Subscriber/Listener)

  * Interface com método `update(...)`.
* `ConcreteSubject`

  * Implementa lógica de negócio e dispara notificações.
* `ConcreteObserver`

  * Implementa reação específica ao evento.

Pseudo-UML textual:

* `Subject`

  * `+ attach(o : Observer)`
  * `+ detach(o : Observer)`
  * `+ notify()`
* `Observer`

  * `+ update(subject : Subject)`
* `ConcreteSubject` : `Subject`

  * `- state`
  * em `setState(...)` → chama `notify()`
* `ConcreteObserver` : `Observer`

  * mantém referência opcional para o `Subject`.

Relações:

* `ConcreteSubject` **não conhece** detalhes dos observadores; apenas mantém uma lista de `Observer`.
* Observadores se **inscrevem voluntariamente** no subject; o subject notifica todos quando algo relevante ocorre.

### 3. Quando utilizar

Cenários típicos:

* Modelos de **evento**: UI, sistemas de plugin, integração entre módulos.
* Vários componentes dependem do **estado de um objeto central** (ex.: múltiplas views observando um modelo).
* Implementação de mecanismos de **pub/sub** simples.

Sinais de uso:

* Chamadas manuais repetidas “lugar por lugar” para atualizar módulos diferentes sempre que algo muda.
* Lógica “espalhada” de atualização de estado, causando bugs quando se esquece de atualizar algum lugar.

### 4. Iterações e variações

Variações:

* **Push vs Pull**:

  * Push: o `Subject` envia dados diretamente no `update(...)`.
  * Pull: o `Observer` consulta o `Subject` quando notificado.
* **Gerenciador de eventos dedicado**: um objeto `EventManager` separado que encapsula listas de assinatura e notificação. ([refactoring.guru][8])
* Observers **fortemente tipados** vs. genéricos (um único evento vs. múltiplos tipos de evento).

Adaptações:

* Em linguagens modernas, Observer frequentemente aparece como:

  * **Eventos e delegates** (C#),
  * **Signals/slots** (Qt),
  * **EventEmitter/EventTarget** (JS/TS),
  * **Rx/Streams** em arquiteturas reativas.

Trade-offs:

* **Prós**: baixo acoplamento, fácil adicionar novos observadores, favorece extensibilidade.
* **Contras**: ordem de notificação nem sempre é clara, pode haver **efeitos colaterais em cascata**, difícil depurar se muitos observers forem encadeados. ([refactoring.guru][6])

---

## Factory Method

### 1. Descrição e propósito

* **Problema que resolve**
  Evitar acoplamento direto a **classes concretas** na criação de objetos, especialmente quando o código de criação varia entre subclasses ou quando o “tipo exato” do produto só é conhecido em tempo de execução. ([refactoring.guru][9])
* **Intenção principal**
  Fornecer uma **interface para criação de objetos** em uma superclasse, permitindo que subclasses **alterem o tipo de objetos** que serão criados. ([refactoring.guru][10])
* **Contexto adequado**
  Quando uma classe não pode antecipar qual classe concreta deve instanciar, ou quando quer delegar essa decisão para subclasses.

### 2. Estrutura

Papéis principais:

* `Product`

  * Interface ou classe base dos objetos sendo criados.
* `ConcreteProductA`, `ConcreteProductB`, ...

  * Implementações concretas do produto.
* `Creator` (ou `Factory`)

  * Classe base que declara o **Factory Method**: `createProduct()`.
  * Pode implementar um **algoritmo geral** que usa `Product`, delegando a criação a `createProduct()`.
* `ConcreteCreatorA`, `ConcreteCreatorB`

  * Subclasses que sobrescrevem `createProduct()` para retornar diferentes `ConcreteProduct`.

Pseudo-UML textual:

* `Creator`

  * `+ someOperation()` → usa `Product`
  * `+ createProduct() : Product` (factory method)
* `ConcreteCreatorA` / `ConcreteCreatorB`

  * sobrescrevem `createProduct()` retornando produtos diferentes.
* `Client`

  * trabalha com `Creator` e `Product`, não com classes concretas.

Relações:

* O **cliente** trabalha com `Creator` e `Product`.
* O **Creator** chama `createProduct()` no próprio objeto, que é polimórfico; subclasses definem qual produto concreto será criado. ([refactoring.guru][11])

### 3. Quando utilizar

Cenários típicos:

* Frameworks onde o **núcleo chama o código do usuário** (inversão de controle) para criar objetos específicos.
* Quando você tem um **fluxo genérico** em `Creator`, mas quer que subclasses possam customizar apenas a parte de criação.
* Quando o código depende de **múltiplas variações de produto**, mas você quer manter o cliente desacoplado de implementações concretas.

Sinais de uso:

* Muitos `new` espalhados com lógica condicional selecionando subclasses.
* Necessidade de introduzir **novos tipos concretos** frequentemente, sem alterar o cliente.

### 4. Iterações e variações

Variações:

* **Factory Method abstrato**: apenas declarado na superclasse, sempre sobrescrito nas subclasses.
* **Factory Method com implementação padrão**: a superclasse fornece uma implementação default, que pode ou não ser sobrescrita.
* Várias fábricas para **famílias de produtos** podem evoluir naturalmente para um **Abstract Factory**. ([refactoring.guru][12])

Adaptações:

* Em linguagens que suportam métodos estáticos com polimorfismo limitado, às vezes o factory method é **estático**, embora o padrão clássico use métodos de instância.
* Em arquiteturas modernas, Factory Method costuma conviver com **injeção de dependência** e contêineres IoC (a DI “vira” a fábrica em muitos casos).

Trade-offs:

* **Prós**: reduz acoplamento a classes concretas, facilita extensão, favorece testes (permite substituir produtos).
* **Contras**: pode introduzir muitas subclasses para cada variação de produto, aumentando a quantidade de classes. ([refactoring.guru][10])

---

## Comparações entre os padrões

### 5. Semelhanças

* **Encapsulamento de mudanças**

  * Todos ajudam a **isolar pontos de variação**:

    * Singleton: variação na forma de acesso a uma instância global.
    * Strategy: variação em algoritmos.
    * Observer: variação em reações a eventos.
    * Factory Method: variação em tipos de objetos criados.
* **Uso de interfaces/abstrações**

  * Strategy, Observer e Factory Method dependem fortemente de **interfaces/abstrações** para desacoplar clientes de implementações concretas.
* **Promoção de extensibilidade**

  * Todos suportam o princípio **Open/Closed**: você estende adicionando novas classes (novas strategies, novos observers, novos products/factories) em vez de alterar código de cliente existente. ([refactoring.guru][13])

### 6. Diferenças

* **Tipo de problema que resolvem**

  * **Singleton**: problema de **quantidade de instâncias** e acesso global.
  * **Strategy**: problema de **escolha e variação de algoritmos**.
  * **Observer**: problema de **notificação e propagação de eventos**.
  * **Factory Method**: problema de **criação desacoplada de objetos**.
* **Categoria de padrão**

  * Singleton e Factory Method são **criacionais**.
  * Strategy e Observer são **comportamentais**.
* **Impacto em acoplamento**

  * **Singleton** tende a **aumentar acoplamento global** (acesso estático).
  * Strategy, Observer e Factory Method tendem a **reduzir acoplamento**, ao introduzir abstrações (interfaces).
* **Impacto em testes**

  * Singleton pode dificultar mocking e isolamento.
  * Strategy, Observer e Factory Method geralmente **facilitam testes** (é fácil injetar implementações “fake” ou stubs).

### 7. Possíveis combinações

* **Factory Method + Strategy**

  * Factory Method pode ser usado para **instanciar a Strategy adequada** com base em configuração, tipo de usuário, contexto etc.
  * Ex.: um `DiscountStrategyFactory` que cria a estratégia de desconto correta (percentual, valor fixo, sem desconto).
* **Observer + Singleton**

  * Um Singleton pode ser o **“dispatcher” central de eventos**, gerenciando inscrições de observers espalhados pela aplicação.
  * Ex.: `EventBus` singleton com métodos `subscribe(event, handler)` / `publish(event, data)`.
* **Factory Method + Observer**

  * Fábricas podem criar objetos já configurados para observar determinado subject ou já inscritos em eventos.
* **Strategy + Observer**

  * Um contexto pode **trocar de Strategy** em resposta a eventos vindos de um Observer.
  * Ex.: sistema que muda a estratégia de cache ou de balanceamento de carga quando um determinado evento é disparado.

Essas combinações fazem sentido porque:

* **Factory Method** cuida de *como* os objetos são criados (e já configurados).
* **Strategy** cuida de *como* um comportamento específico é executado.
* **Observer** cuida de *quando* várias partes do sistema devem reagir.
* **Singleton** pode servir como ponto único de coordenação (com cuidado para não virar anti-pattern).

Juntos, eles formam um conjunto bem poderoso para construir sistemas flexíveis, extensíveis e com responsabilidades bem separadas, alinhados às recomendações do catálogo de padrões do Refactoring Guru.

[1]: https://refactoring.guru/pt-br/design-patterns/singleton?utm_source=chatgpt.com "Singleton"
[2]: https://refactoring.guru/design-patterns/singleton/python/example?utm_source=chatgpt.com "Singleton in Python / Design Patterns"
[3]: https://refactoring.guru/design-patterns/singleton/swift/example?utm_source=chatgpt.com "Singleton in Swift / Design Patterns"
[4]: https://refactoring.guru/pt-br/design-patterns/strategy?utm_source=chatgpt.com "Strategy"
[5]: https://refactoring.guru/design-patterns/strategy?utm_source=chatgpt.com "Strategy"
[6]: https://refactoring.guru/pt-br/design-patterns/observer?utm_source=chatgpt.com "Observer"
[7]: https://refactoring.guru/design-patterns/observer?utm_source=chatgpt.com "Observer"
[8]: https://refactoring.guru/design-patterns/observer/java/example?utm_source=chatgpt.com "Observer in Java / Design Patterns"
[9]: https://refactoring.guru/pt-br/design-patterns/factory-method?utm_source=chatgpt.com "Factory Method"
[10]: https://refactoring.guru/design-patterns/factory-method?utm_source=chatgpt.com "Factory Method"
[11]: https://refactoring.guru/design-patterns/factory-method/csharp/example?utm_source=chatgpt.com "Factory Method in C# / Design Patterns"
[12]: https://refactoring.guru/design-patterns/abstract-factory?utm_source=chatgpt.com "Abstract Factory"
[13]: https://refactoring.guru/design-patterns?utm_source=chatgpt.com "Design Patterns"
