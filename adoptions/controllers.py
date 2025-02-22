from typing import List

from django.http import Http404
from ninja import Query
from ninja.types import DictStrAny
from ninja_extra import api_controller, route, status
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction

from .schemas import (
    PetFilter,
    PetOut,
    AdoptionFilter,
    AdoptionIn,
    AdoptionOut,
)
from .models import Pet, Adoption


@api_controller(
    'pets/',
    auth=JWTAuth(),
    tags=['PETS'],
)
class PetController:
    @route.get(
        '/',
        response=List[PetOut],
        permissions=[],
    )
    def list(self, filters: PetFilter = Query(...)):
        pets = Pet.objects.all()
        pets = filters.filter(pets)
        return pets

    @route.get(
        '/{int:id}/',
        response={
            status.HTTP_200_OK: PetOut,
            status.HTTP_404_NOT_FOUND: DictStrAny,
        },
        permissions=[],
    )
    def get(self, id: int):
        try:
            return status.HTTP_200_OK, get_object_or_404(Pet, id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                'message': f'{Pet._meta.verbose_name.capitalize()} não existe.'
            }


@api_controller(
    'adoptions/',
    auth=JWTAuth(),
    tags=['ADOPTIONS'],
)
class AdoptionController:
    @route.get(
        '/',
        response=List[AdoptionOut],
        permissions=[],
    )
    def list(self, filters: AdoptionFilter = Query(...)):
        adoptions = Adoption.objects.all()
        adoptions = filters.filter(adoptions)
        return adoptions

    @route.get(
        '/{int:id}/',
        response={
            status.HTTP_200_OK: AdoptionOut,
            status.HTTP_404_NOT_FOUND: DictStrAny,
        },
        permissions=[],
    )
    def get(self, id: int):
        try:
            return status.HTTP_200_OK, get_object_or_404(Adoption, id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                'message': f'{Adoption._meta.verbose_name.capitalize()} não existe.'
            }

    @route.post(
        '/',
        response={
            status.HTTP_201_CREATED: AdoptionOut,
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
    def register(self, request, payload: AdoptionIn):
        try:
            with transaction.atomic():
                payload = payload.dict()
                
                pet_id = payload.get('pet_id', 0)
                pet = Pet.objects.filter(id=pet_id).first()
                
                if pet is None:
                    return status.HTTP_404_NOT_FOUND, {'message': 'Pet não encontrado.'}
                                
                if pet.status != 'A':
                    return status.HTTP_400_BAD_REQUEST, {'message': 'Pet não está disponível para adoção.'}
                
                if pet.adoption_set.all().filter(status='P').exists():
                    return status.HTTP_400_BAD_REQUEST, {'message': 'Já existe uma tratativa de adoção pendente para esse Pet.'}
                
                payload.update({'customer_id': request.user.id})
                
                adoption = Adoption.objects.create(**payload)
                
                return status.HTTP_201_CREATED, adoption
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {'message': str(error)}
