from __future__ import annotations
from abc import ABC, abstractmethod


class OrderObserver(ABC):
    """
    Observer: quem deseja ser notificado quando o status do pedido mudar.
    """

    @abstractmethod
    def update(self, order: "Order") -> None:
        pass


class CozinhaDisplayObserver(OrderObserver):
    """
    Observer que representa o painel da cozinha.
    """

    def update(self, order: "Order") -> None:
        print(f"[COZINHA] Pedido #{order.id} mudou para: {order.status.name}")


class NotificacaoClienteObserver(OrderObserver):
    """
    Observer que representa uma notificação ao cliente.
    """

    def update(self, order: "Order") -> None:
        print(f"[CLIENTE] Seu pedido #{order.id} agora está: {order.status.name}")


class LoggerObserver(OrderObserver):
    """
    Observer que representa um logger simples.
    """

    def update(self, order: "Order") -> None:
        print(f"[LOGGER] Status do pedido #{order.id} atualizado: {order.status.name}")
