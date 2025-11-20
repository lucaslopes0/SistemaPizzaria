from __future__ import annotations

from flask import Flask, request, jsonify

from config import ConfigService
from models import Pizza, Order, OrderStatus
from discounts import (
    NoDiscountStrategy,
    CupomPercentualStrategy,
    DescontoPorValorMinimoStrategy,
)
from observers import (
    CozinhaDisplayObserver,
    NotificacaoClienteObserver,
    LoggerObserver,
)
from payments import (
    PixPaymentHandler,
    CartaoPaymentHandler,
    DinheiroPaymentHandler,
    PaymentHandler,
)


app = Flask(__name__)

# "Banco de dados" em memória
ORDERS: dict[int, Order] = {}
NEXT_ORDER_ID: int = 1

# Cardápio fixo em memória (poderia vir de BD no futuro)
MENU: dict[str, Pizza] = {
    "margherita": Pizza("Margherita", 30.0),
    "calabresa": Pizza("Calabresa", 35.0),
    "portuguesa": Pizza("Portuguesa", 38.0),
}


def get_new_order_id() -> int:
    global NEXT_ORDER_ID
    oid = NEXT_ORDER_ID
    NEXT_ORDER_ID += 1
    return oid


def aplicar_desconto(order: Order, data_desconto: dict | None) -> None:
    """
    Define a DiscountStrategy do pedido com base em um payload simples.
    Exemplo de payload:
    {
      "tipo": "percentual",
      "percentual": 0.1
    }
    ou
    {
      "tipo": "valor_minimo",
      "minimo": 100,
      "desconto_fixo": 10
    }
    """
    if not data_desconto:
        order.desconto_strategy = NoDiscountStrategy()
        return

    tipo = data_desconto.get("tipo")

    if tipo == "percentual":
        percentual = float(data_desconto.get("percentual", 0.0))
        order.desconto_strategy = CupomPercentualStrategy(percentual)
    elif tipo == "valor_minimo":
        minimo = float(data_desconto.get("minimo", 0.0))
        desconto_fixo = float(data_desconto.get("desconto_fixo", 0.0))
        order.desconto_strategy = DescontoPorValorMinimoStrategy(
            minimo=minimo,
            desconto_fixo=desconto_fixo,
        )
    else:
        order.desconto_strategy = NoDiscountStrategy()


def escolher_handler_pagamento(metodo: str) -> PaymentHandler:
    metodo = metodo.upper()
    if metodo == "PIX":
        return PixPaymentHandler()
    elif metodo == "CARTAO":
        return CartaoPaymentHandler()
    else:
        return DinheiroPaymentHandler()


# =========================
#   Endpoints da API
# =========================

@app.route("/config", methods=["GET"])
def get_config():
    config = ConfigService()
    return jsonify(
        {
            "taxa_entrega": config.taxa_entrega,
            "percentual_servico": config.percentual_servico,
        }
    )


@app.route("/menu", methods=["GET"])
def get_menu():
    return jsonify(
        [
            {"id": key, "nome": pizza.nome, "preco": pizza.preco}
            for key, pizza in MENU.items()
        ]
    )


@app.route("/orders", methods=["POST"])
def create_order():
    """
    Cria um novo pedido.
    Exemplo de body JSON:
    {
      "itens": [
        { "pizza_id": "margherita", "quantidade": 1 },
        { "pizza_id": "calabresa", "quantidade": 2 }
      ],
      "desconto": {
        "tipo": "percentual",
        "percentual": 0.1
      }
    }
    """
    body = request.get_json(force=True)

    itens = body.get("itens", [])
    dados_desconto = body.get("desconto")

    order = Order()
    order.id = get_new_order_id()

    # Observers: registramos na criação
    order.attach(CozinhaDisplayObserver())
    order.attach(NotificacaoClienteObserver())
    order.attach(LoggerObserver())

    # Adiciona itens do cardápio
    for item in itens:
        pizza_id = item.get("pizza_id")
        quantidade = int(item.get("quantidade", 1))

        pizza = MENU.get(pizza_id)
        if not pizza:
            return jsonify({"error": f"pizza_id inválido: {pizza_id}"}), 400

        order.add_item(pizza, quantidade)

    # Aplica estratégia de desconto (Strategy)
    aplicar_desconto(order, dados_desconto)

    # Salva no "banco"
    ORDERS[order.id] = order

    return jsonify(order.to_dict()), 201


@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify([o.to_dict() for o in ORDERS.values()])


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id: int):
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"error": "Pedido não encontrado"}), 404
    return jsonify(order.to_dict())


@app.route("/orders/<int:order_id>/status", methods=["PATCH"])
def update_order_status(order_id: int):
    """
    Atualiza o status do pedido.
    Body:
    { "status": "EM_PREPARO" }
    """
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"error": "Pedido não encontrado"}), 404

    body = request.get_json(force=True)
    status_str = body.get("status")

    try:
        novo_status = OrderStatus[status_str]
    except KeyError:
        return jsonify({"error": f"Status inválido: {status_str}"}), 400

    order.set_status(novo_status)

    return jsonify(order.to_dict())


@app.route("/orders/<int:order_id>/pay", methods=["POST"])
def pay_order(order_id: int):
    """
    Processa o pagamento de um pedido.
    Body:
    { "metodo": "PIX" }  # ou "CARTAO", "DINHEIRO"
    """
    order = ORDERS.get(order_id)
    if not order:
        return jsonify({"error": "Pedido não encontrado"}), 404

    body = request.get_json(force=True)
    metodo = body.get("metodo", "DINHEIRO")

    handler = escolher_handler_pagamento(metodo)
    handler.processar_pagamento(order)  # Factory Method por baixo dos panos

    return jsonify(
        {
            "message": f"Pagamento processado com sucesso via {metodo.upper()}",
            "order": order.to_dict(),
        }
    )


if __name__ == "__main__":
    # Ajusta config global se quiser
    config = ConfigService()
    config.taxa_entrega = 7.0
    config.percentual_servico = 0.08

    app.run(debug=True)
