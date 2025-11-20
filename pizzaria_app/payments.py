from __future__ import annotations
from abc import ABC, abstractmethod

from models import Order


class PaymentProcessor(ABC):
    """
    Interface comum para processadores de pagamento.
    """

    @abstractmethod
    def pagar(self, order: Order) -> None:
        pass


class PixPaymentProcessor(PaymentProcessor):
    def pagar(self, order: Order) -> None:
        print(f"[PAGAMENTO PIX] Pagando R$ {order.total_final:.2f} via PIX.")


class CartaoPaymentProcessor(PaymentProcessor):
    def pagar(self, order: Order) -> None:
        print(f"[PAGAMENTO CARTÃO] Pagando R$ {order.total_final:.2f} no cartão.")


class DinheiroPaymentProcessor(PaymentProcessor):
    def pagar(self, order: Order) -> None:
        print(f"[PAGAMENTO DINHEIRO] Pagando R$ {order.total_final:.2f} em dinheiro.")


class PaymentHandler(ABC):
    """
    Creator no padrão Factory Method.
    Define o metodo de alto nível `processar_pagamento`,
    que delega ao factory method `create_processor()` a escolha
    do processador concreto.
    """

    def processar_pagamento(self, order: Order) -> None:
        processor = self.create_processor()
        processor.pagar(order)

    @abstractmethod
    def create_processor(self) -> PaymentProcessor:
        """
        Factory Method: subclasse decide qual processor concreto será criado.
        """
        pass


class PixPaymentHandler(PaymentHandler):
    def create_processor(self) -> PaymentProcessor:
        return PixPaymentProcessor()


class CartaoPaymentHandler(PaymentHandler):
    def create_processor(self) -> PaymentProcessor:
        return CartaoPaymentProcessor()


class DinheiroPaymentHandler(PaymentHandler):
    def create_processor(self) -> PaymentProcessor:
        return DinheiroPaymentProcessor()
