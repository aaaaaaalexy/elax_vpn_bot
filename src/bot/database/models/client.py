from sqlalchemy import String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from bot.utils import conf
from .base import Base


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), nullable=False)
    name:  Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    private_key: Mapped[str] = mapped_column(String(44), nullable=False)
    public_key: Mapped[str] = mapped_column(String(44), nullable=False)
    preshare_key: Mapped[str] = mapped_column(String(44), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=conf.DEFAULT_CLIENT_ENABLED)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())