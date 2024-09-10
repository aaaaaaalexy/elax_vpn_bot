from sqlalchemy import Integer, DateTime, String
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Payment(Base):
    __tablename__ = 'paymenets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), nullable=False)
    balance_before: Mapped[int] = mapped_column(Integer, nullable=False)
    deposited: Mapped[int] = mapped_column(Integer, nullable=False)
    uuid: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())