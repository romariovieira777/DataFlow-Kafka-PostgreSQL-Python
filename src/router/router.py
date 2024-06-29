from fastapi import APIRouter
from src.controller import auth_controller, product_controller, kafka_consumer_product_controller

router = APIRouter()

router.include_router(auth_controller.router, prefix='/api/vert/auth', tags=['Authentication'])
router.include_router(product_controller.router, prefix='/api/vert', tags=['Product'])
router.include_router(kafka_consumer_product_controller.router, prefix='/api/vert', tags=['Kafka'])
