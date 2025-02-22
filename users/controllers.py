from typing import List

from django.http import Http404
from ninja import Query
from ninja.types import DictStrAny
from ninja_extra import api_controller, route, status
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction

from .schemas import (
    UserFilter,
    UserIn,
    UserOut,
)
from .models import User


@api_controller(
    'users/',
    auth=JWTAuth(),
    tags=['USERS'],
)
class UserController:
    @route.get(
        '/',
        response=List[UserOut],
        permissions=[],
    )
    def list(self, filters: UserFilter = Query(...)):
        users = User.objects.all()
        users = filters.filter(users)
        return users

    @route.get(
        '/{int:id}/',
        response={
            status.HTTP_200_OK: UserOut,
            status.HTTP_404_NOT_FOUND: DictStrAny,
        },
        permissions=[],
    )
    def get(self, id: int):
        try:
            return status.HTTP_200_OK, get_object_or_404(User, id=id)
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                'message': f'{User._meta.verbose_name.capitalize()} não existe.'
            }

    @route.post(
        '/',
        auth=None,
        response={
            status.HTTP_201_CREATED: UserOut,
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
    def register(self, request, payload: UserIn):
        try:
            with transaction.atomic():
                payload = payload.dict()
                
                username = payload.get('username')
                user_with_same_username = User.objects.filter(username=username).first()
                
                if user_with_same_username is not None:
                    return status.HTTP_400_BAD_REQUEST, {"message": "Já existe um registro com esse nome de usuário."}
                
                user = User.objects.create_user(**payload, role='P')
                
                return status.HTTP_201_CREATED, user
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {'message': str(error)}

    @route.put(
        '/',
        response={
            status.HTTP_200_OK: UserOut,
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
    def edit(self, request, payload: UserIn):
        try:
            with transaction.atomic():
                payload = payload.dict()
                
                username = payload.get('username')
                user_with_same_username = User.objects.filter(username=username).exclude(id=request.user.id).first()
                
                if user_with_same_username is not None:
                    return status.HTTP_400_BAD_REQUEST, {"message": "Já existe um registro com esse nome de usuário."}
                
                user = get_object_or_404(User, id=request.user.id)
                
                for k, v in payload.items():
                    if k == 'password':
                        user.set_password(v)
                        continue
                    setattr(user, k, v)    
                
                user.save()
                
                return status.HTTP_200_OK, user
        except Http404:
            return status.HTTP_404_NOT_FOUND, {
                'message': f'{User._meta.verbose_name.capitalize()} não existe.'
            }
        except IntegrityError as error:
            return status.HTTP_500_INTERNAL_SERVER_ERROR, {'message': str(error)}
