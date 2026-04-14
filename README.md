## Тестовое задание на позицию Fullstack разработчика (Python + React)

**Комментарий:**
1. Поставленные задачи выполнил
2. В pyproject.toml добавил зависимсоти для тестов
3. В папке backend установить зависимости внутри виртуального окружения и запустить тесты:
    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install -e ".[test]"
    pytest tests/ -v -s
    ```

**Запуск:**
1. ```docker compose -f docker-compose.dev.yml up```
2. ```docker exec -it backend alembic upgrade head```

**Открыть фронт:** ```http://localhost:3000/test``` 

**Открыть бэк:** ```http://localhost:8000/docs```