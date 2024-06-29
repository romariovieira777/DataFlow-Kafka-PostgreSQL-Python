from fastapi import APIRouter
from src.schema.schema import LoginSchema, ResponseSchema, TokenResponse
from src.service.service import AuthService

router = APIRouter()


@router.post('/login')
async def login(request: LoginSchema):
    try:
        token = AuthService.get_token(request=request)

        if token is not None:
            return ResponseSchema(code="200",
                                  status="Ok",
                                  message="Success Login",
                                  result=TokenResponse(access_token=token, token_type="Bearer")).dict(exclude_none=True)

        else:
            return ResponseSchema(code="500",
                                  status="Internal Server Error",
                                  message="Incorrect username or password").dict(exclude_none=True)

    except Exception as e:
        return ResponseSchema(code="500",
                              status="Internal Server Error",
                              message=e.__str__()).dict(exclude_none=True)
