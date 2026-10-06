"""Catálogo fixo de produtos em memória."""

PRODUTOS = [
    {"sku": "KB-100", "name": "Teclado Mecânico", "unitPriceCents": 25990, "available": True},
    {"sku": "MS-200", "name": "Mouse Sem Fio", "unitPriceCents": 12990, "available": True},
    {"sku": "HD-300", "name": "Headset USB", "unitPriceCents": 19990, "available": True},
    {"sku": "MN-400", "name": "Monitor 27", "unitPriceCents": 119990, "available": True},
]

CATALOGO = {produto["sku"]: produto for produto in PRODUTOS}


def buscar_produto(sku):
    return CATALOGO.get(sku)
