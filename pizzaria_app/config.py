from __future__ import annotations
from typing import Optional


class ConfigService:
    """
    Singleton responsável por centralizar configurações globais da aplicação.
    Apenas uma instância existe em todo o sistema.
    """
    _instance: Optional["ConfigService"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Configurações padrão
            cls._instance.taxa_entrega = 5.0          # em reais
            cls._instance.percentual_servico = 0.10   # 10%
        return cls._instance

    def __repr__(self) -> str:
        return (f"<ConfigService taxa_entrega={self.taxa_entrega}, "
                f"percentual_servico={self.percentual_servico}>")
