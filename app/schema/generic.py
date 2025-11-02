from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel

class MetaSchema(BaseModel):
    page: int
    total_page: int
    limit: int

# 3. Generic response wrapper using TypeVars
T = TypeVar('T') # Type variable for dynamic data type

class GenericResponse(BaseModel, Generic[T]):
    message: str = "success"
    data: Optional[T] = None
    meta: Optional[MetaSchema] = None