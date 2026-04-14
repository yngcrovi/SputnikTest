import pytest
from src.schema import FileItem, ListFileItem

@pytest.mark.asyncio
async def test_create_file_view(client):
    files = [
        {
            "title": (None, "Текстовый документ"),
            "file": ("document.txt", b"This is test content .txt", "text/plain")
        }, 
        {
            "title": (None, "pdf документ"),
            "file": ("document.pdf", b"This is test content .pdf", "application/pdf")
        }
    ]
    
    for file in files:
        response = await client.post("/files", files=file)
        assert response.status_code == 201
        data = response.json()
        assert isinstance(data, dict)
        try:
            file_item = FileItem(**data)
            print(f"Валидация пройдена: {file_item.id}")
        except Exception as e:
            pytest.fail(f"Ответ не соответствует модели FileItem: {e}")
    

@pytest.mark.asyncio
async def test_list_files_view(client):
    response = await client.get("/files")
    data = response.json()
    assert isinstance(data, dict)
    assert data.get("total") == 2
    assert data.get("page") == 1
    assert data.get("size") == 3
    assert data.get("pages") == 1
    for item in data.get("items"):
        assert isinstance(item, dict)
        assert "id" in item and isinstance(item.get("id"), str) and len(item.get("id")) == 36
        assert "title" in item and isinstance(item.get("title"), str)
        assert "original_name" in item and isinstance(item.get("original_name"), str)
        assert "mime_type" in item and isinstance(item.get("original_name"), str)
        assert "size" in item and isinstance(item.get("size"), int)
        assert "processing_status" in item and isinstance(item.get("processing_status"), str)
    assert len(data.get("items")) == 2
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_file_view(client):
    response = await client.get("/files")
    data = response.json()
    for item in data.get("items"):
        delete_response = await client.delete(f"/files/{item['id']}")
        assert delete_response.status_code == 204