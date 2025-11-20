# 🍕 Sistema de Pizzaria – Flask + Angular com Design Patterns

Projeto acadêmico que implementa um **sistema simples de pizzaria**, com foco em demonstrar na prática o uso de **Design Patterns** em uma aplicação web com:

* **Backend** em Python usando **Flask**
* **Frontend** em **Angular** (standalone, com SSR configurado)
* Utilização explícita de 4 padrões de projeto:

  * **Singleton**
  * **Strategy**
  * **Observer**
  * **Factory Method**

O objetivo é ter um sistema didático, com front e back integrados, pronto para ser apresentado em contexto acadêmico ou como portfólio.

---

## 🧱 Arquitetura Geral do Projeto

Estrutura de pastas sugerida:

```text
.
├── pizzaria_app/          # Backend Flask
│   ├── app.py
│   ├── config.py
│   ├── discounts.py
│   ├── models.py
│   ├── observers.py
│   ├── payments.py
│   └── requirements.txt
└── pizzaria-frontend/     # Frontend Angular
    ├── src/
    │   ├── main.ts
    │   ├── main.server.ts
    │   └── app/
    │       ├── app.component.ts
    │       ├── app.routes.ts
    │       ├── app.routes.server.ts
    │       ├── app.config.server.ts
    │       ├── core/services/pizzaria-api.service.ts
    │       └── pages/
    │           ├── menu/
    │           ├── cart/
    │           ├── payment/
    │           └── order-tracking/
    └── package.json
```

---

## ⚙️ Backend – Flask

O backend expõe uma API REST simples para gerenciar cardápio, pedidos e pagamentos.

### Endpoints principais

* `GET /config` – Retorna configurações globais (ex.: taxa de entrega, percentual de serviço).
* `GET /menu` – Retorna o cardápio de pizzas.
* `POST /orders` – Cria um novo pedido.
* `GET /orders` – Lista todos os pedidos.
* `GET /orders/<id>` – Retorna os detalhes de um pedido específico.
* `PATCH /orders/<id>/status` – Atualiza o status do pedido.
* `POST /orders/<id>/pay` – Processa o pagamento do pedido.

### Arquivos importantes

* `app.py`
  Criação da aplicação Flask, configuração de CORS, rotas e “banco de dados” em memória.

* `config.py`
  Implementa o **Singleton** `ConfigService`, responsável pelas configurações globais (taxa de entrega, percentual de serviço).

* `discounts.py`
  Contém as **Strategies** de desconto (sem desconto, cupom percentual, desconto por valor mínimo).

* `models.py`
  Modelos de domínio (`Pizza`, `Order`, `OrderItem`) e implementação do **Subject** do padrão **Observer**.

* `observers.py`
  Observers concretos (ex.: `CozinhaDisplayObserver`, `NotificacaoClienteObserver`, `LoggerObserver`).

* `payments.py`
  Implementa o **Factory Method** através de `PaymentHandler` e `PaymentProcessor` para diferentes meios de pagamento.

---

## 🌐 Frontend – Angular

O frontend é uma aplicação Angular standalone, que consome a API Flask.

### Service principal

* `core/services/pizzaria-api.service.ts`
  Centraliza as chamadas HTTP para o backend:

  * `getMenu()`
  * `createOrder()`
  * `getOrder()`
  * `updateOrderStatus()`
  * `payOrder()`
  * etc.

### Principais páginas

* `menu` – Lista o cardápio e permite adicionar pizzas ao carrinho.
* `cart` – Exibe os itens selecionados e envia a criação do pedido para a API.
* `payment` – Seleciona o método de pagamento e chama `/orders/:id/pay`.
* `order-tracking` – Acompanha o status do pedido via `/orders/:id`.

### Rotas (exemplo simplificado)

```ts
export const routes: Routes = [
  { path: '', redirectTo: 'menu', pathMatch: 'full' },
  { path: 'menu', component: MenuComponent },
  { path: 'cart', component: CartComponent },
  { path: 'payment', component: PaymentComponent },
  { path: 'tracking', component: OrderTrackingComponent },
];
```

---

## 🧩 Design Patterns Utilizados

### 1. Singleton – `ConfigService` (`config.py`)

**Problema:** Várias partes do sistema precisam das mesmas configurações (ex.: taxa de entrega) de forma consistente.

**Solução:** `ConfigService` é implementado como **Singleton**, garantindo uma única instância das configurações em todo o backend.

Uso típico:

* `Order.total_final` utiliza `ConfigService` para aplicar taxa de entrega e percentual de serviço sobre o subtotal.

---

### 2. Strategy – Descontos (`discounts.py` + `models.py`)

**Problema:** A regra de desconto do pedido pode variar (sem desconto, cupom, valor mínimo, etc.).

**Solução:** Padrão **Strategy**:

* Interface `DiscountStrategy`.
* Implementações concretas:

  * `NoDiscountStrategy`
  * `CupomPercentualStrategy`
  * `DescontoPorValorMinimoStrategy`

Na classe `Order`, existe um atributo `desconto_strategy`, e o cálculo do desconto é delegado para a estratégia configurada.

---

### 3. Observer – Notificações de Pedido (`models.py` + `observers.py`)

**Problema:** Quando o status de um pedido muda, múltiplos “interessados” (cozinha, cliente, logs) precisam ser notificados sem acoplamento forte.

**Solução:** Padrão **Observer**:

* `Order` funciona como **Subject**, mantendo uma lista de observers.
* Observers possíveis:

  * `CozinhaDisplayObserver`
  * `NotificacaoClienteObserver`
  * `LoggerObserver`

Ao chamar `order.set_status(novo_status)`, o `Order` notifica todos os observers via `update(order)`.

---

### 4. Factory Method – Pagamentos (`payments.py`)

**Problema:** Diferentes formas de pagamento (PIX, cartão, dinheiro) não devem ser tratadas com um monte de `if/else` espalhados.

**Solução:** Padrão **Factory Method**:

* Interface `PaymentProcessor` com implementação para cada método:

  * `PixPaymentProcessor`
  * `CartaoPaymentProcessor`
  * `DinheiroPaymentProcessor`
* Classe `PaymentHandler` define o fluxo principal `processar_pagamento(order)`, chamando o factory method `create_processor()`.

Para cada meio de pagamento, existe um `*PaymentHandler` que decide qual processor criar.
No endpoint `/orders/<id>/pay`, o backend escolhe o handler com base no JSON recebido.

---

## 🔄 Fluxo Geral da Aplicação

1. **Menu (frontend)**
   Usuário seleciona pizzas e monta o carrinho (armazenado localmente no navegador).

2. **Carrinho → Criação de Pedido**
   O frontend envia o carrinho para `POST /orders`.
   O backend:

   * Cria a `Order`
   * Aplica a `DiscountStrategy`
   * Usa `ConfigService` para calcular o valor final
   * Registra observers (cozinha, cliente, logger)

3. **Pagamento**
   A tela de pagamento chama `POST /orders/:id/pay`, informando o método (PIX, cartão, dinheiro).
   O backend:

   * Usa o **Factory Method** para criar o processor adequado
   * Processa o pagamento do pedido

4. **Acompanhamento**
   Tela de tracking consulta `GET /orders/:id` para ver o status.
   Quando o status é atualizado (`PATCH /orders/:id/status`), o **Observer** notifica os interessados.

---

## ▶️ Como Executar o Projeto

### 1. Organizar as pastas

Certifique-se de que a estrutura está assim:

```text
.
├── pizzaria_app/
└── pizzaria-frontend/
```

---

### 2. Subir o Backend (Flask)

Entre na pasta `pizzaria_app/`:

#### 2.1 Criar e ativar o ambiente virtual

**Windows:**

```bash
cd pizzaria_app
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**

```bash
cd pizzaria_app
python3 -m venv venv
source venv/bin/activate
```

#### 2.2 Instalar as dependências

```bash
pip install -r requirements.txt
```

#### 2.3 Subir a API Flask

```bash
python app.py
```

A API ficará disponível em:

* `http://127.0.0.1:5000`

---

### 3. Subir o Frontend (Angular)

Em outro terminal, entre na pasta `pizzaria-frontend/`:

#### 3.1 Instalar dependências

```bash
cd pizzaria-frontend
npm install
```

#### 3.2 Rodar em modo desenvolvimento (SPA)

Para simplificar, pode usar apenas o modo client (sem SSR) durante o desenvolvimento:

```bash
npm run dev
# ou
ng serve
```

O frontend ficará acessível em:

* `http://localhost:4200`

---

### 4. Observações

* Garanta que o backend Flask esteja rodando em `http://127.0.0.1:5000`.
* Certifique-se de que o CORS está habilitado em `app.py` usando algo como:

```python
from flask_cors import CORS

CORS(app)
```

Assim, o Angular consegue consumir a API sem problemas de CORS.

---

Pronto! Basta salvar este conteúdo como **`README.md`** na raiz do projeto (ou dentro do backend/frontend, como preferir).
