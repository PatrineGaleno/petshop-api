from ninja import Schema
from ninja_jwt.schema import TokenObtainPairInputSchema
from users.schemas import UserOut


class CustomTokenObtainOutSchema(Schema):
    token: str
    user: UserOut


class CustomTokenObtainSchema(TokenObtainPairInputSchema):
    def output_schema(self) -> CustomTokenObtainOutSchema:
        token = self.to_response_schema().access
        return CustomTokenObtainOutSchema(token=token, user=self._user)
