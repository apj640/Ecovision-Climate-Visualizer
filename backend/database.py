from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Define Base model for SQLAlchemy
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
