from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.db.config.url import PostgresURL

class EngineDB:
    _engine = None  
    _sessionmaker = None  
    
    @classmethod
    def _init_engine(cls):
        if cls._engine is None:
            url = PostgresURL().get_url()
            cls._engine = create_async_engine(
                url=url,
                echo=False
            )
            cls._sessionmaker = async_sessionmaker(
                cls._engine, 
                expire_on_commit=False
            )
    
    @classmethod
    async def get_session(cls) -> AsyncSession:
        cls._init_engine()
        return cls._sessionmaker()