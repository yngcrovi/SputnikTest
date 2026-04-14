from sqlalchemy import select, delete, func
from src.db.model import AlertModel
from src.db.config.engine import EngineDB

class AlertService:
    
    def __init__(self, session = None):
        self._session = None
        self.alert_table = AlertModel

    async def _get_session(self):
        if self._session is None:
            self._session = await EngineDB.get_session() 
        return self._session

    async def create_alert(self, file_id: str, level: str, message: str) -> AlertModel:
        alert = self.alert_table(file_id=file_id, level=level, message=message)
        session = await self._get_session()
        async with session:
            session.add(alert)
            await session.commit()
            await session.refresh(alert)
            return alert

    async def list_alerts(self, page: int = 1, size: int = 3) -> tuple[list[AlertModel], int]:
        session = await self._get_session()
        async with session:
            total = await session.scalar(select(func.count()).select_from(self.alert_table))
            offset = (page - 1) * size
            query = select(self.alert_table).order_by(self.alert_table.created_at.desc()).offset(offset).limit(size)
            result = await session.execute(query)
            items = list(result.scalars().all())
            return items, total or 0
        
    async def delete_alerts(self, file_id: str) -> None:
        session = await self._get_session()
        async with session:
            await session.execute(
                delete(self.alert_table).where(self.alert_table.file_id == file_id)
            )
            await session.commit()
        