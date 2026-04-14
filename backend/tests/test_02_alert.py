import pytest
from src.db.model import FileModel, AlertModel
from uuid import uuid4

@pytest.mark.asyncio
async def test_list_alerts_view(client):
    response = await client.get("/alerts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)



@pytest.mark.asyncio
async def test_alert_different_levels(client, db_session):
    files_id = [str(uuid4()), str(uuid4())]
    test_files = [
        FileModel(
            id=files_id[0],
            title="Файл для теста уровней info",
            original_name="test.txt",
            stored_name=f"{files_id[0]}.txt",
            mime_type="text/plain",
            size=100,
            processing_status="pending",
            requires_attention=False
        ),
       FileModel(
            id=files_id[1],
            title="Файл для теста уровней warning",
            original_name="test2.txt",
            stored_name=f"{files_id[1]}.txt",
            mime_type="text/plain",
            size=150,
            processing_status="pending",
            requires_attention=False
        ) 
    ]
    db_session.add_all(test_files)
    await db_session.commit()
    
    test_alerts = [AlertModel(id=1, file_id=files_id[0], level="info", message="Тестовое сообщение уровня info"), 
                   AlertModel(id=2, file_id=files_id[1], level="warning", message="Тестовое сообщение уровня warning")]
    db_session.add_all(test_alerts)
    await db_session.commit()
    response = await client.get("/alerts")
    data: dict = response.json() 
    assert response.status_code == 200
    assert data.get("total") == 2
    assert data.get("page") == 1
    assert data.get("size") == 3
    assert data.get("pages") == 1
    assert len(data.get("items")) == 2
    try:
        for item in data.get("items"):
            alert_item = AlertModel(**item)
            print(f"Валидация пройдена: {alert_item.file_id}")
    except Exception as e:
        pytest.fail(f"Ответ не соответствует модели FileItem: {e}")