import jwt
import pytz
from datetime import timedelta, datetime
from typing import TypeVar, Generic, List, Optional
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session, joinedload
from starlette.requests import Request
from src.config.config import SECRET_KEY, ALGORITHM, TIMEZONE
from src.model.model import ProductModel

T = TypeVar('T')


class BaseRepo:

    @staticmethod
    def retrieve_all(db: Session, model: Generic[T]):
        return db.query(model).all()

    @staticmethod
    def retrieve_by_id(db: Session, model: Generic[T], id_model: int):
        return db.query(model).filter(model.id == id_model).all()

    @staticmethod
    def retrieve_by_first_id(db: Session, model: Generic[T], id_model: int):
        return db.query(model).filter(model.id == id_model).first()

    @staticmethod
    def insert(db: Session, model: Generic[T]):
        db.add(model)
        db.commit()
        db.refresh(model)

        return model

    @staticmethod
    def update(db: Session, model: Generic[T]):
        db.commit()
        db.refresh(model)

    @staticmethod
    def delete(db: Session, model: Generic[T]):
        db.delete(model)
        db.commit()

    @staticmethod
    def bulk(db: Session, models: List):
        db.bulk_save_objects(models)
        db.commit()

    @staticmethod
    def convert_to_timezone(timestamp, timezone_str):
        local_tz = pytz.timezone(timezone_str)
        if timestamp.tzinfo is None:
            timestamp = pytz.utc.localize(timestamp)

        local_time = timestamp.astimezone(local_tz)
        return local_time


class JWTRepo:

    @staticmethod
    def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(TIMEZONE) + expires_delta
        else:
            expire = datetime.now(TIMEZONE) + timedelta(minutes=15)

        to_encode.update({"exp": expire})

        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            return credentials.credentials

    @staticmethod
    def verify_jwt(jwt_token: str):
        isTokenValid: bool = False

        jwt_token = jwt_token.replace('"', '')

        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=ALGORITHM)
        except Exception as e:
            print(f'Error: {e.__str__()}')
            payload = None

        if payload:
            isTokenValid = True

        return isTokenValid


class UserRepository(BaseRepo):

    @classmethod
    def verify_password(cls, password, hashed_password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        return pwd_context.verify(password, hashed_password)

    @classmethod
    def retrieve_by_first_username(cls, db: Session, model: Generic[T], username: str):
        return db.query(model).filter(model.username == username).first()


class VertRepository(BaseRepo):

    @classmethod
    def retrieve_products_all(cls, db: Session):
        products = db.query(ProductModel).options(joinedload(ProductModel.pricing), joinedload(ProductModel.availability)).all()
        for product in products:
            if product.availability:
                product.availability.timestamp = cls.convert_to_timezone(product.availability.timestamp, 'America/Sao_Paulo')

        return products
