from pydantic import BaseModel

class PaginationItem(BaseModel):
    total: int
    page: int
    size: int
    pages: int