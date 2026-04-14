import mimetypes
from sqlalchemy import select, func
from src.db.model import FileModel
from src.db.config.engine import EngineDB
from uuid import uuid4
from pathlib import Path
from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from src.path import StoragePath
from src.db.service import AlertService

class FileService(StoragePath):
    
    def __init__(self):
        super().__init__()
        self._session = None
        self.file_table = FileModel

    async def _get_session(self):
        if self._session is None:
            self._session = await EngineDB.get_session() 
        return self._session

    async def _scan_file_for_threats(self, file_id: str) -> None:
        session = await self._get_session()
        async with session:
            file_item = await session.get(self.file_table, file_id)
            if not file_item:
                return

            file_item.processing_status = "processing"
            reasons: list[str] = []
            extension = Path(file_item.original_name).suffix.lower()

            if extension in {".exe", ".bat", ".cmd", ".sh", ".js"}:
                reasons.append(f"suspicious extension {extension}")

            if file_item.size > 10 * 1024 * 1024:
                reasons.append("file is larger than 10 MB")

            if extension == ".pdf" and file_item.mime_type not in {"application/pdf", "application/octet-stream"}:
                reasons.append("pdf extension does not match mime type")

            file_item.scan_status = "suspicious" if reasons else "clean"
            file_item.scan_details = ", ".join(reasons) if reasons else "no threats found"
            file_item.requires_attention = bool(reasons)
            await session.commit()

    async def _extract_file_metadata(self, file_id: str) -> None:
        session = await self._get_session()
        async with session:
            file_item = await session.get(self.file_table, file_id)
            if not file_item:
                return

            stored_path = self.storage_dir / file_item.stored_name
            if not stored_path.exists():
                file_item.processing_status = "failed"
                file_item.scan_status = file_item.scan_status or "failed"
                file_item.scan_details = "stored file not found during metadata extraction"
                await session.commit()
                return

            metadata = {
                "extension": Path(file_item.original_name).suffix.lower(),
                "size_bytes": file_item.size,
                "mime_type": file_item.mime_type,
            }

            if file_item.mime_type.startswith("text/"):
                content = stored_path.read_text(encoding="utf-8", errors="ignore")
                metadata["line_count"] = len(content.splitlines())
                metadata["char_count"] = len(content)
            elif file_item.mime_type == "application/pdf":
                content = stored_path.read_bytes()
                metadata["approx_page_count"] = max(content.count(b"/Type /Page"), 1)

            file_item.metadata_json = metadata
            file_item.processing_status = "processed"
            await session.commit()

    async def list_files(self, page: int = 1, size: int = 3) -> tuple[list[FileModel], int]:
        session = await self._get_session()
        async with session:
            total = await session.scalar(select(func.count()).select_from(self.file_table))
            offset = (page - 1) * size
            query = select(self.file_table).order_by(self.file_table.created_at.desc()).offset(offset).limit(size)
            result = await session.execute(query)
            items = list(result.scalars().all())
            return items, total or 0


    async def get_file(self, file_id: str, need_raise: bool = True) -> FileModel:
        session = await self._get_session()
        async with session:
            file_item = await session.get(self.file_table, file_id)
            if not file_item and need_raise:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
            elif not file_item and not need_raise:
                return
            return file_item


    async def create_file(self, title: str, upload_file: UploadFile) -> FileModel:
        content = await upload_file.read()
        if not content:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

        file_id = str(uuid4())
        suffix = Path(upload_file.filename or "").suffix
        stored_name = f"{file_id}{suffix}"
        stored_path = self.storage_dir / stored_name
        stored_path.write_bytes(content)

        file_item = self.file_table(
            id=file_id,
            title=title,
            original_name=upload_file.filename or stored_name,
            stored_name=stored_name,
            mime_type=upload_file.content_type or mimetypes.guess_type(stored_name)[0] or "application/octet-stream",
            size=len(content),
            processing_status="uploaded",
        )
        session = await self._get_session()
        async with session:
            session.add(file_item)
            await session.commit()
            await session.refresh(file_item)
        return file_item


    async def update_file(self, file_id: str, title: str) -> FileModel:
        session = await self._get_session()
        async with session:
            file_item = await session.get(self.file_table, file_id)
            if not file_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
            file_item.title = title
            await session.commit()
            await session.refresh(file_item)
            return file_item


    async def delete_file(self, file_id: str) -> None:
        session = await self._get_session()
        async with session:
            file_item = await session.get(self.file_table, file_id)
            if not file_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
            stored_path = self.storage_dir / file_item.stored_name
            if stored_path.exists():
                stored_path.unlink()
            await AlertService(session).delete_alerts(file_id)
            await session.delete(file_item)
            await session.commit()


    async def get_file_path(self, file_id: str) -> tuple[FileModel, Path]:
        file_item = await self.get_file(file_id)
        stored_path = self.storage_dir / file_item.stored_name
        if not stored_path.exists():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stored file not found")
        return file_item, stored_path