from typing import List

from django.http import Http404
from ninja import Query
from ninja.types import DictStrAny
from ninja_extra import api_controller, route, status
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction

from .schemas import (
    SaleFilter,
    SaleIn,
    SaleOut,
    ProductOut,
    ProductFilter,
)
from .models import Sale, Product


@api_controller(
    'products/',
    auth=JWTAuth(),
    tags=['PRODUCTS'],
)
class ProductController:
    @route.get(
        '/',
        response=List[ProductOut],
        permissions=[],
    )
    def list(self, filters: ProductFilter = Query(...)):
        products = Product.objects.all()
        products = filters.filter(products)
        return products

    @route.get(
        '/{int:id}/',
        response={
            status.HTTP_200_OK: ProductOut,
            status.HTTP_404_NOT_FOUND: DictStrAny,
        },
        permissions=[],
    )
    def get(self, id: int):
        try:
            return status.HTTP_200_OK, get_object_or_404(Product, id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                'message': f'{Product._meta.verbose_name.capitalize()} não existe.'
            }


@api_controller(
    'sales/',
    auth=JWTAuth(),
    tags=['SALES'],
)
class SaleController:
    @route.get(
        '/',
        response=List[SaleOut],
        permissions=[],
    )
    def list(self, filters: SaleFilter = Query(...)):
        sales = Sale.objects.all()
        sales = filters.filter(sales)
        return sales

    @route.get(
        '/{int:id}/',
        response={
            status.HTTP_200_OK: SaleOut,
            status.HTTP_404_NOT_FOUND: DictStrAny,
        },
        permissions=[],
    )
    def get(self, id: int):
        try:
            return status.HTTP_200_OK, get_object_or_404(Sale, id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                'message': f'{Sale._meta.verbose_name.capitalize()} não existe.'
            }

    @route.post(
        '/',
        response={
            status.HTTP_201_CREATED: SaleOut,
            frozenset(
                [
                    status.HTTP_400_BAD_REQUEST,
                    status.HTTP_404_NOT_FOUND,
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                ]
            ): DictStrAny,
        },
        permissions=[],
    )
    def register(self, request, payload: SaleIn):
        try:
            with transaction.atomic():
                payload = payload.dict()
                
                product_id = payload.get("product_id", 0)
                product = Product.objects.filter(id=product_id).first()
                
                if product is None:
                    return status.HTTP_404_NOT_FOUND, {"message": "Produto não encontrado."}
                
                bought_quantity = payload.get("bought_quantity", 0)
                
                if (bought_quantity <= 0) or (bought_quantity > product.current_quantity):
                    return status.HTTP_400_BAD_REQUEST, {"message": "Quantidade inválida para a compra."}
                
                payment_form = payload.get("payment_form", "")
                if payment_form not in ["M", "C"]:
                    return status.HTTP_400_BAD_REQUEST, {"message": "Forma de pagamento inválida."}                    
                
                payload.update({
                    "customer_id": request.user.id,
                    "price_on_sale": product.price,
                })
                
                sale = Sale.objects.create(**payload)
                
                return status.HTTP_201_CREATED, sale
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {'message': str(error)}
