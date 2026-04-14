from pathlib import Path

class StoragePath:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        self.storage_dir = BASE_DIR / "storage" / "files"
        self.storage_dir.mkdir(parents=True, exist_ok=True)