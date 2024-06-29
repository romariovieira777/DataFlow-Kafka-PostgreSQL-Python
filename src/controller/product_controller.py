from fastapi import APIRouter, Depends
from starlette.requests import Request
from src.config.config import get_db_vert
from src.repository.repository import JWTBearer
from src.schema.schema import ResponseSchema, ProductSchema
from src.service.service import ProductService
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register/product", dependencies=[Depends(JWTBearer())])
async def register_product_controller(request: Request, product: ProductSchema,
                                      db_vert: Session = Depends(get_db_vert)):
    try:
        product_service = ProductService()

        product_service.register_product(db=db_vert, product=product)

        return ResponseSchema(
            code="200",
            status="Ok",
            message="Product register successfully",
            result=None
        ).dict(exclude_none=True)

    except Exception as e:
        return ResponseSchema(
            code="500",
            status="Error",
            message=e.__str__()
        ).dict(exclude_none=True)


@router.get("/product/all", dependencies=[Depends(JWTBearer())])
async def product_all_controller(request: Request, db_vert: Session = Depends(get_db_vert)):
    try:
        product_service = ProductService()

        products = product_service.get_product_all(db=db_vert)

        return ResponseSchema(
            code="200",
            status="Ok",
            message="Retrieve products successfully",
            result=products
        ).dict(exclude_none=True)

    except Exception as e:
        return ResponseSchema(
            code="500",
            status="Error",
            message=e.__str__()
        ).dict(exclude_none=True)
