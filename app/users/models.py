from typing import Literal
from sqlalchemy.orm import relationship
from app.adverts.models import Advert
from sqlalchemy.sql import expression

from app.database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


user_type = Literal["user", "admin"]
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[user_type] = mapped_column(server_default="user", nullable=False)
    adverts: Mapped["Advert"] = relationship(back_populates="owner")
    is_active: Mapped[bool] = mapped_column(server_default=expression.true(), nullable=False)