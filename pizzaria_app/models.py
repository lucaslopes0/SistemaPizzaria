from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from typing import List, Optional

from config import ConfigService
from discounts import DiscountStrategy, NoDiscountStrategy


@dataclass
class Pizza:
    nome: str
    preco: float


@dataclass
class OrderItem:
    pizza: Pizza
    quantidade: int

    @property
    def total(self) -> float:
        return self.pizza.preco * self.quantidade

    def to_dict(self) -> dict:
        return {
            "pizza": {
                "nome": self.pizza.nome,
                "preco": self.pizza.preco,
            },
            "quantidade": self.quantidade,
            "total": self.total,
        }


class OrderStatus(Enum):
    NOVO = auto()
    EM_PREPARO = auto()
    SAIU_ENTREGA = auto()
    ENTREGUE = auto()


@dataclass
class Order:
    """
    Order atua como:
    - Subject do padrão Observer (mantém lista de observers e notifica).
    - Context do padrão Strategy (usa DiscountStrategy para calcular desconto).
    """
    id: Optional[int] = None
    itens: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.NOVO
    desconto_strategy: DiscountStrategy = field(
        default_factory=NoDiscountStrategy
    )
    _observers: List["OrderObserver"] = field(
        default_factory=list, init=False, repr=False
    )

    def add_item(self, pizza: Pizza, quantidade: int) -> None:
        self.itens.append(OrderItem(pizza, quantidade))

    @property
    def subtotal(self) -> float:
        return sum(item.total for item in self.itens)

    @property
    def desconto(self) -> float:
        return self.desconto_strategy.calcular_desconto(self)

    @property
    def total_final(self) -> float:
        config = ConfigService()
        taxa_servico = self.subtotal * config.percentual_servico
        return self.subtotal + taxa_servico + config.taxa_entrega - self.desconto

    # --- Métodos de Observer ---

    def attach(self, observer: "OrderObserver") -> None:
        self._observers.append(observer)

    def detach(self, observer: "OrderObserver") -> None:
        self._observers.remove(observer)

    def _notify_observers(self) -> None:
        for obs in self._observers:
            obs.update(self)

    def set_status(self, novo_status: OrderStatus) -> None:
        self.status = novo_status
        self._notify_observers()

    # --- Serialização para JSON (API) ---

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "status": self.status.name,
            "itens": [item.to_dict() for item in self.itens],
            "subtotal": self.subtotal,
            "desconto": self.desconto,
            "total_final": self.total_final,
        }
