"""Validação e cálculo de cotações."""

from pydantic import BaseModel, StrictInt

from app.catalog import CATALOGO
from app.errors import ErroApi


class ItemCotacao(BaseModel):
    sku: str
    quantity: StrictInt


class PedidoCotacao(BaseModel):
    items: list[ItemCotacao]


def validar_itens(itens):
    if not 1 <= len(itens) <= 5:
        raise ErroApi(422, "INVALID_QUANTITY_OR_ITEMS", "Items must have between 1 and 5 entries")

    skus = [item.sku for item in itens]
    if len(skus) != len(set(skus)):
        raise ErroApi(422, "INVALID_QUANTITY_OR_ITEMS", "Duplicated SKU in items")

    for item in itens:
        if item.sku not in CATALOGO:
            raise ErroApi(422, "INVALID_PRODUCT", f"Product {item.sku} not found")

        if not 1 <= item.quantity <= 10:
            raise ErroApi(422, "INVALID_QUANTITY_OR_ITEMS", "Quantity must be between 1 and 10")


def percentual_desconto(subtotal):
    if subtotal >= 100000:
        return 10
    if subtotal >= 50000:
        return 5
    return 0


def calcular_cotacao(itens):
    subtotal = sum(CATALOGO[item.sku]["unitPriceCents"] * item.quantity for item in itens)
    percentual = percentual_desconto(subtotal)
    desconto = subtotal * percentual // 100

    return {
        "subtotalCents": subtotal,
        "discountPercent": percentual,
        "discountCents": desconto,
        "totalCents": subtotal - desconto,
    }
