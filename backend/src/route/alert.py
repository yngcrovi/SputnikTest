from fastapi import APIRouter, Depends
from src.schema import AlertItem, ListAlertItem
from src.db.service import AlertService

route = APIRouter(
    prefix="/alerts",
    tags=['File'],
)


@route.get("", response_model=ListAlertItem)
async def list_alerts_view(page: int = 1, size: int = 3, alert_service: AlertService = Depends(AlertService)):
    items, total = await alert_service.list_alerts(page=page, size=size)
    return {
        "items": items,           # файлы на текущей странице
        "total": total,           # всего файлов в БД
        "page": page,             # текущая страница
        "size": size,             # сколько на странице
        "pages": (total + size - 1) // size  # всего страниц
    }
