from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class KnowledgeCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = 0
    status: str = "active"

class KnowledgeCategoryCreate(KnowledgeCategoryBase):
    pass

class KnowledgeCategoryUpdate(KnowledgeCategoryBase):
    name: Optional[str] = None
    sort_order: Optional[int] = None
    status: Optional[str] = None

class KnowledgeCategoryResponse(KnowledgeCategoryBase):
    id: int
    created_at: datetime
    children: Optional[List['KnowledgeCategoryResponse']] = []

    class Config:
        from_attributes = True

class KnowledgeItemBase(BaseModel):
    category_id: int
    title: str
    content: str
    content_type: str
    author: Optional[str] = None
    publisher: Optional[str] = None
    publish_date: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    status: str = "active"

class KnowledgeItemCreate(KnowledgeItemBase):
    pass

class KnowledgeItemUpdate(KnowledgeItemBase):
    category_id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None
    status: Optional[str] = None

class KnowledgeItemResponse(KnowledgeItemBase):
    id: int
    view_count: int
    download_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VideoLinkBase(BaseModel):
    title: str
    description: Optional[str] = None
    video_url: str
    category_id: int
    sort_order: int = 0
    status: str = "active"

class VideoLinkCreate(VideoLinkBase):
    pass

class VideoLinkUpdate(VideoLinkBase):
    title: Optional[str] = None
    video_url: Optional[str] = None
    category_id: Optional[int] = None
    sort_order: Optional[int] = None
    status: Optional[str] = None

class VideoLinkResponse(VideoLinkBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class BookLinkBase(BaseModel):
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    book_url: str
    sort_order: int = 0
    status: str = "active"

class BookLinkCreate(BookLinkBase):
    pass

class BookLinkUpdate(BookLinkBase):
    title: Optional[str] = None
    book_url: Optional[str] = None
    sort_order: Optional[int] = None
    status: Optional[str] = None

class BookLinkResponse(BookLinkBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserFavoriteBase(BaseModel):
    user_id: int
    favorite_type: str
    favorite_id: int

class UserFavoriteCreate(UserFavoriteBase):
    pass

class UserFavoriteResponse(UserFavoriteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 