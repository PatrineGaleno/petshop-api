from ninja import Swagger
from ninja_extra import NinjaExtraAPI

from auth.controllers import AuthController
from users.controllers import UserController
from sales.controllers import (SaleController, ProductController)


api = NinjaExtraAPI(
    title='Petshop API',
    docs=Swagger(
        settings={'persistAuthorization': True}
    ),
)

api.register_controllers(
    AuthController,
    UserController,
    SaleController,
    ProductController,
)
