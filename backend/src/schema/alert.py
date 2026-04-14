from datetime import datetime

from pydantic import BaseModel, ConfigDict
from .base import PaginationItem

class AlertItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_id: str
    level: str
    message: str
    created_at: datetime

class ListAlertItem(PaginationItem):
    items: list[AlertItem]