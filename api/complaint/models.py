import datetime
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship
from api.adverts.models import Advert

from api.database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from api.users.models import User


class Complaint(Base):
    __tablename__ = "Complaints"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    advert: Mapped["Advert"] = relationship(
        back_populates="complaints",
        single_parent=True,
    )
    advert_id: Mapped[int] = mapped_column(ForeignKey("adverts.id", ondelete="CASCADE",))
    user: Mapped["User"] = relationship(
        back_populates="complaints",
        single_parent=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc',now())"))