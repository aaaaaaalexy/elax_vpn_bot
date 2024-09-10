from sqlalchemy import Integer, BigInteger, String, Boolean, Date, DateTime, ARRAY
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from bot.utils import conf
from .base import Base


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    tg_firstname: Mapped[str] = mapped_column(String(32), nullable=False)
    contact: Mapped[str] = mapped_column(String(11), nullable=True)
    balance: Mapped[int] = mapped_column(Integer, nullable=False, default=conf.DEFAULT_BALANCE)
    time_sub: Mapped[Date] = mapped_column(Date, nullable=False)
    count_clients: Mapped[int] = mapped_column(Integer, nullable=False, default=conf.DEFAULT_COUNT_CLIENTS)
    reminder_sent: Mapped[ARRAY[bool]] = mapped_column(ARRAY(Boolean), default=[False, False])
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=conf.DEFAULT_USER_ENABLED)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())