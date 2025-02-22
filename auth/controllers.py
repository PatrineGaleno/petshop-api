from ninja_extra import api_controller, route
from ninja_jwt.controller import ControllerBase
from ninja.types import DictStrAny

from .schemas import (
    CustomTokenObtainOutSchema,
    CustomTokenObtainSchema,
)

@api_controller('auth/', tags=['AUTH'])
class AuthController(ControllerBase):
    @route.post(
        'token/',
        response=DictStrAny,
        url_name='token_obtain',
    )
    def obtain_token(self, request, user_token: CustomTokenObtainSchema):
        user_token.check_user_authentication_rule()
        return user_token.output_schema().dict()
