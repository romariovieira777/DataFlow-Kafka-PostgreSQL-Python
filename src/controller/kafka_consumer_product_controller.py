from fastapi import APIRouter, Depends
from starlette.requests import Request
from src.config.config import TOPIC_KAFKA_PRODUCT
from src.repository.repository import JWTBearer
from src.schema.schema import ResponseSchema
from src.kafka.service import KafkaService

router = APIRouter()


@router.get("/kafka/consumer/product", dependencies=[Depends(JWTBearer())])
async def kafka_consumer_product_controller(request: Request):
    try:
        kafka_service = KafkaService()
        msg = kafka_service.consume_from_kafka(topic=TOPIC_KAFKA_PRODUCT)

        return ResponseSchema(
            code="200",
            status="Ok",
            message="Consumer topic kafka successfully",
            result=msg
        ).dict(exclude_none=True)

    except Exception as e:
        return ResponseSchema(
            code="500",
            status="Error",
            message=e.__str__()
        ).dict(exclude_none=True)
