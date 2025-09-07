from pydantic import BaseModel, Field
from typing import Any, Dict, Union

class Message(BaseModel):
    is_error: bool = False
    msg: Any
    status_code: int

class Error(BaseModel):
    detail: str = Field(description="Описание ошибки")

class Error_400(Error):
    message: str = Field(description="Сообщение об ошибке")
    body: Dict[str, Union[str, Union[int, float]]] = Field(description="Полученные входные данные")