from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from src.db.model import BaseModel

class AlertModel(BaseModel):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String(36), ForeignKey("files.id"), nullable=False)
    level: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(String(500), nullable=False)