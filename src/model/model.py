import datetime
import pytz
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from src.config.config import Base, TIMEZONE


def get_current_time():
    return datetime.datetime.now(pytz.timezone(TIMEZONE))

class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class ProductModel(Base):
    __tablename__ = "tb_product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String)

    pricing = relationship("PricingModel", uselist=False, back_populates="product")
    availability = relationship("AvailabilityModel", uselist=False, back_populates="product")


class PricingModel(Base):
    __tablename__ = "tb_pricing"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("tb_product.id"), unique=True, index=True)
    ammount = Column(Float)
    currency = Column(String)

    product = relationship("ProductModel", back_populates="pricing")


class AvailabilityModel(Base):
    __tablename__ = "tb_availability"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("tb_product.id"), unique=True, index=True)
    quantity = Column(Integer)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(TIMEZONE))

    product = relationship("ProductModel", back_populates="availability")