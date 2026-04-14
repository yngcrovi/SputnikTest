from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from src.schema import FileUpdate, FileItem, ListFileItem
from src.db.service import FileService
from src.task.task import process_file

route = APIRouter(
    prefix='/files',
    tags=['File'],
)

@route.get("", response_model=ListFileItem)
async def list_files_view(page: int = 1, size: int = 3, file_service: FileService = Depends(FileService)):
    items, total = await file_service.list_files(page=page, size=size)
    return {
        "items": items,           # файлы на текущей странице
        "total": total,           # всего файлов в БД
        "page": page,             # текущая страница
        "size": size,             # сколько на странице
        "pages": (total + size - 1) // size  # всего страниц
    }

@route.post("", response_model=FileItem, status_code=201)
async def create_file_view(
    title: str = Form(...),
    file: UploadFile = File(...),
    file_service: FileService = Depends(FileService)
):
    file_item = await file_service.create_file(title=title, upload_file=file)
    process_file.delay(file_item.id)
    return file_item

@route.get("/{file_id}", response_model=FileItem)
async def get_file_view(file_id: str, file_service: FileService = Depends(FileService)):
    return await file_service.get_file(file_id)

@route.patch("/{file_id}", response_model=FileItem)
async def update_file_view(
    file_id: str,
    payload: FileUpdate,
    file_service: FileService = Depends(FileService)
):
    return await file_service.update_file(file_id=file_id, title=payload.title)


@route.get("/{file_id}/download")
async def download_file(file_id: str, file_service: FileService = Depends(FileService)):
    file_item = await file_service.get_file(file_id)
    stored_path = file_service.storage_dir / file_item.stored_name
    if not stored_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stored file not found")
    return FileResponse(
        path=stored_path,
        media_type=file_item.mime_type,
        filename=file_item.original_name,
    )


@route.delete("/{file_id}", status_code=204)
async def delete_file_view(file_id: str, file_service: FileService = Depends(FileService)):
    await file_service.delete_file(file_id)