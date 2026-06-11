from pydantic import BaseModel, field_validator, Field
from typing import Literal
import re

FORBIDDEN = ['..', '/', '\\', '\x00', '\n', '\r']
RESERVED = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'LPT1', 'LPT2'}

class DocumentCreate(BaseModel):
    locale: Literal["en", "es", "pt"]
    content: str = Field(..., min_length=1)
    filename: str | None = None
    
    @field_validator('filename')
    @classmethod
    def validate_filename(cls, v):
        if v is None:
            return v
        v = v.strip()
        if any(p in v for p in FORBIDDEN):
            raise ValueError('Forbidden characters in filename')
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Only alphanumeric, dash, underscore allowed')
        if v.upper() in RESERVED:
            raise ValueError('Reserved filename')
        if len(v) > 100:
            raise ValueError('Filename too long (max 100 chars)')
        return v

class DocumentUpdate(BaseModel):
    content: str

class DocumentResponse(BaseModel):
    filename: str
    locale: str
    content: str

class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    count: int

class DocumentDeleteResponse(BaseModel):
    deleted: bool
    filename: str
    message: str

class ReindexResponse(BaseModel):
    indexed: bool
    count: int
    locale: str
    message: str