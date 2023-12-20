from sqlalchemy import Column, Integer, String, Boolean, LargeBinary

from src.core.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    password = Column(LargeBinary)
    active = Column(Boolean, default=True)
