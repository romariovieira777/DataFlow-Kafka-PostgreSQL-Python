import datetime
from datetime import timedelta
from sqlalchemy.orm import Session
from src.config.config import ACCESS_TOKEN_EXPIRE_MINUTES, get_db_vert, TIMEZONE, TOPIC_KAFKA_PRODUCT
from src.model.model import UserModel, ProductModel, PricingModel, AvailabilityModel
from src.repository.repository import JWTRepo, UserRepository, VertRepository
from src.schema.schema import LoginSchema, ProductSchema
from src.kafka.service import KafkaService

"""
    Authentication
"""


class AuthService:

    @classmethod
    def get_token(cls, request: LoginSchema):

        session = next(get_db_vert())

        user = UserRepository.retrieve_by_first_username(session, UserModel, request.username)

        if user is not None:

            if UserRepository.verify_password(request.password, user.hashed_password):

                token = JWTRepo.generate_token({
                    "username": request.username
                }, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

                return token
            else:
                raise Exception("Incorrect username or password")


"""
    Product
"""


class ProductService:

    @staticmethod
    def register_product(db: Session, product: ProductSchema):
        product_model = ProductModel(
            name=product.name,
            description=product.description,
            category=product.category
        )
        product_inserted = VertRepository.insert(db=db, model=product_model)

        pricing_model = PricingModel(
            product_id=product_inserted.id,
            ammount=product.pricing.ammount,
            currency=product.pricing.currency
        )
        VertRepository.insert(db=db, model=pricing_model)

        availability_model = AvailabilityModel(
            product_id=product_inserted.id,
            quantity=product.availability.quantity,
            timestamp=datetime.datetime.now(TIMEZONE)
        )
        VertRepository.insert(db=db, model=availability_model)

        kafka_service = KafkaService()
        kafka_service.send_to_kafka(topic=TOPIC_KAFKA_PRODUCT, data={
            "id": product_inserted.id,
            "name": product.name,
            "description": product.description,
            "pricing": {
                "amount": product.pricing.ammount,
                "currency": product.pricing.currency,
            },
            "availability": {
                "quantity": product.availability.quantity,
                "timestamp": availability_model.timestamp.astimezone(TIMEZONE).strftime('%Y-%m-%dT%H:%M:%SZ')
            },
            "category": product.category
        })

    @staticmethod
    def get_product_all(db: Session):
        products = VertRepository.retrieve_products_all(db=db)
        return products



