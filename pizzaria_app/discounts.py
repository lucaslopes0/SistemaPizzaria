from __future__ import annotations
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """
    Strategy: interface comum para estratégias de desconto.
    """

    @abstractmethod
    def calcular_desconto(self, order: "Order") -> float:
        """
        Retorna o valor do desconto (em reais) para o pedido informado.
        """
        pass


class NoDiscountStrategy(DiscountStrategy):
    """
    Nenhum desconto aplicado.
    """

    def calcular_desconto(self, order: "Order") -> float:
        return 0.0


class CupomPercentualStrategy(DiscountStrategy):
    """
    Desconto percentual aplicado sobre o subtotal do pedido.
    Ex.: cupom de 10% -> percentual = 0.10
    """

    def __init__(self, percentual: float) -> None:
        self.percentual = percentual

    def calcular_desconto(self, order: "Order") -> float:
        return order.subtotal * self.percentual


class DescontoPorValorMinimoStrategy(DiscountStrategy):
    """
    Desconto fixo apenas se o subtotal passar de um valor mínimo.
    Ex.: R$ 10,00 de desconto para pedidos acima de R$ 100,00.
    """

    def __init__(self, minimo: float, desconto_fixo: float) -> None:
        self.minimo = minimo
        self.desconto_fixo = desconto_fixo

    def calcular_desconto(self, order: "Order") -> float:
        if order.subtotal >= self.minimo:
            return self.desconto_fixo
        return 0.0
