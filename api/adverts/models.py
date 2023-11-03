import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from api.database import Base
from sqlalchemy import text
from typing import Literal


advert_type = Literal["Покупка", "Продажа", "Оказание услуг"]


class Advert(Base):
    __tablename__ = "adverts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(index=True)
    ad_type: Mapped[advert_type] = mapped_column(nullable=False)
    price: Mapped[int]
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc',now())")
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
            
        )
    )
    owner = relationship("User", back_populates="adverts", single_parent=True)
    complaints = relationship("Complaint", back_populates="advert")
