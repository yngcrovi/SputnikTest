# tests/conftest.py
import pytest_asyncio
from unittest.mock import patch
import tempfile
from pathlib import Path
import shutil
from src.db.model import BaseModel
from src.db.config.engine import EngineDB 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from src.app import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="session")
async def setup_db():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    
    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(setup_db):
    async_session = sessionmaker(setup_db, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture
async def client(db_session):
    temp_storage = tempfile.mkdtemp()
    temp_storage_path = Path(temp_storage) / "files"
    temp_storage_path.mkdir(parents=True, exist_ok=True)
    
    original_get_session = EngineDB.get_session
    
    from src.path import StoragePath
    original_init = StoragePath.__init__
    
    def mock_init(self):
        self.storage_dir = temp_storage_path
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    async def mock_get_session():
        return db_session
    
    # Мокаем Celery
    with patch('src.route.file.process_file.delay') as mock_celery:
        mock_celery.return_value = None  # Ничего не делаем
        
        try:
            EngineDB.get_session = mock_get_session
            StoragePath.__init__ = mock_init
            
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                yield client
        finally:
            EngineDB.get_session = original_get_session
            StoragePath.__init__ = original_init
            shutil.rmtree(temp_storage, ignore_errors=True)