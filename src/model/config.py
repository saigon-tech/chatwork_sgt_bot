from src.extensions import db
from .base import BaseModel


class Config(BaseModel):
    __tablename__ = "configs"
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)
