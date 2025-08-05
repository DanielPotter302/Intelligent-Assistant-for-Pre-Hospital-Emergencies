from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_active_user, get_admin_user
from app.models.user import User
from app.models.knowledge import KnowledgeCategory, KnowledgeItem, VideoLink, BookLink, UserFavorite
from app.schemas.knowledge import (
    KnowledgeCategoryResponse, KnowledgeItemResponse, VideoLinkResponse, 
    BookLinkResponse, UserFavoriteResponse, KnowledgeItemCreate, KnowledgeItemUpdate,
    VideoLinkCreate, VideoLinkUpdate, BookLinkCreate, BookLinkUpdate
)
from app.schemas.common import ApiResponse, PaginatedResponse

router = APIRouter()

@router.get("/categories", response_model=ApiResponse)
async def get_knowledge_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取知识库分类"""
    # 获取顶级分类
    categories = db.query(KnowledgeCategory).filter(
        KnowledgeCategory.parent_id.is_(None),
        KnowledgeCategory.status == "active"
    ).order_by(KnowledgeCategory.sort_order).all()
    
    # 构建分类树
    def build_category_tree(category):
        children = db.query(KnowledgeCategory).filter(
            KnowledgeCategory.parent_id == category.id,
            KnowledgeCategory.status == "active"
        ).order_by(KnowledgeCategory.sort_order).all()
        
        category_data = KnowledgeCategoryResponse.from_orm(category)
        if children:
            category_data.children = [build_category_tree(child) for child in children]
        
        return category_data
    
    category_tree = [build_category_tree(cat) for cat in categories]
    
    return ApiResponse(
        message="Knowledge categories retrieved successfully",
        data=category_tree
    )

@router.get("/items", response_model=ApiResponse)
async def get_knowledge_items(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    category_id: int = Query(None),
    content_type: str = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """获取知识库项目"""
    offset = (page - 1) * page_size
    
    # 构建查询
    query = db.query(KnowledgeItem).filter(KnowledgeItem.status == "active")
    
    if category_id:
        query = query.filter(KnowledgeItem.category_id == category_id)
    
    if content_type:
        query = query.filter(KnowledgeItem.content_type == content_type)
    
    if search:
        query = query.filter(
            KnowledgeItem.title.contains(search) |
            KnowledgeItem.content.contains(search) |
            KnowledgeItem.author.contains(search)
        )
    
    # 获取总数
    total = query.count()
    
    # 获取分页数据
    items = query.order_by(KnowledgeItem.created_at.desc()).offset(offset).limit(page_size).all()
    
    item_data = [KnowledgeItemResponse.from_orm(item) for item in items]
    
    return ApiResponse(
        message="Knowledge items retrieved successfully",
        data=PaginatedResponse(
            total=total,
            page=page,
            page_size=page_size,
            records=item_data
        )
    )

@router.get("/items/{item_id}", response_model=ApiResponse)
async def get_knowledge_item(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取知识库项目详情"""
    item = db.query(KnowledgeItem).filter(
        KnowledgeItem.id == item_id,
        KnowledgeItem.status == "active"
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found"
        )
    
    # 增加查看次数
    item.view_count += 1
    db.commit()
    
    return ApiResponse(
        message="Knowledge item retrieved successfully",
        data=KnowledgeItemResponse.from_orm(item)
    )

# 管理员API - 知识内容管理
@router.post("/admin/items", response_model=ApiResponse)
async def create_knowledge_item(
    item_data: KnowledgeItemCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """创建知识内容（管理员）"""
    # 验证分类是否存在
    category = db.query(KnowledgeCategory).filter(
        KnowledgeCategory.id == item_data.category_id,
        KnowledgeCategory.status == "active"
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found"
        )
    
    item = KnowledgeItem(**item_data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return ApiResponse(
        message="Knowledge item created successfully",
        data=KnowledgeItemResponse.from_orm(item)
    )

@router.put("/admin/items/{item_id}", response_model=ApiResponse)
async def update_knowledge_item(
    item_id: int,
    item_data: KnowledgeItemUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """更新知识内容（管理员）"""
    item = db.query(KnowledgeItem).filter(KnowledgeItem.id == item_id).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found"
        )
    
    # 更新字段
    update_data = item_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    
    return ApiResponse(
        message="Knowledge item updated successfully",
        data=KnowledgeItemResponse.from_orm(item)
    )

@router.delete("/admin/items/{item_id}", response_model=ApiResponse)
async def delete_knowledge_item(
    item_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """删除知识内容（管理员）"""
    item = db.query(KnowledgeItem).filter(KnowledgeItem.id == item_id).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge item not found"
        )
    
    # 软删除
    item.status = "inactive"
    db.commit()
    
    return ApiResponse(
        message="Knowledge item deleted successfully",
        data=None
    )

# 视频链接相关API
@router.get("/videos", response_model=ApiResponse)
async def get_video_links(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    category_id: int = Query(None)
):
    """获取视频链接列表"""
    query = db.query(VideoLink).filter(VideoLink.status == "active")
    
    if category_id:
        query = query.filter(VideoLink.category_id == category_id)
    
    videos = query.order_by(VideoLink.sort_order).all()
    video_data = [VideoLinkResponse.from_orm(video) for video in videos]
    
    return ApiResponse(
        message="Video links retrieved successfully",
        data=video_data
    )

@router.get("/videos/{video_id}", response_model=ApiResponse)
async def get_video_link(
    video_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取视频链接详情"""
    video = db.query(VideoLink).filter(
        VideoLink.id == video_id,
        VideoLink.status == "active"
    ).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video link not found"
        )
    
    return ApiResponse(
        message="Video link retrieved successfully",
        data=VideoLinkResponse.from_orm(video)
    )

# 管理员API - 视频链接管理
@router.post("/admin/videos", response_model=ApiResponse)
async def create_video_link(
    video_data: VideoLinkCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """创建视频链接（管理员）"""
    # 验证分类是否存在
    category = db.query(KnowledgeCategory).filter(
        KnowledgeCategory.id == video_data.category_id,
        KnowledgeCategory.status == "active"
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found"
        )
    
    video = VideoLink(**video_data.dict())
    db.add(video)
    db.commit()
    db.refresh(video)
    
    return ApiResponse(
        message="Video link created successfully",
        data=VideoLinkResponse.from_orm(video)
    )

@router.put("/admin/videos/{video_id}", response_model=ApiResponse)
async def update_video_link(
    video_id: int,
    video_data: VideoLinkUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """更新视频链接（管理员）"""
    video = db.query(VideoLink).filter(VideoLink.id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video link not found"
        )
    
    # 更新字段
    update_data = video_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(video, field, value)
    
    db.commit()
    db.refresh(video)
    
    return ApiResponse(
        message="Video link updated successfully",
        data=VideoLinkResponse.from_orm(video)
    )

@router.delete("/admin/videos/{video_id}", response_model=ApiResponse)
async def delete_video_link(
    video_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """删除视频链接（管理员）"""
    video = db.query(VideoLink).filter(VideoLink.id == video_id).first()
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video link not found"
        )
    
    # 软删除
    video.status = "inactive"
    db.commit()
    
    return ApiResponse(
        message="Video link deleted successfully",
        data=None
    )

# 书籍链接相关API
@router.get("/books", response_model=ApiResponse)
async def get_book_links(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取书籍链接列表"""
    books = db.query(BookLink).filter(
        BookLink.status == "active"
    ).order_by(BookLink.sort_order).all()
    
    book_data = [BookLinkResponse.from_orm(book) for book in books]
    
    return ApiResponse(
        message="Book links retrieved successfully",
        data=book_data
    )

@router.get("/books/{book_id}", response_model=ApiResponse)
async def get_book_link(
    book_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取书籍链接详情"""
    book = db.query(BookLink).filter(
        BookLink.id == book_id,
        BookLink.status == "active"
    ).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book link not found"
        )
    
    return ApiResponse(
        message="Book link retrieved successfully",
        data=BookLinkResponse.from_orm(book)
    )

# 管理员API - 书籍链接管理
@router.post("/admin/books", response_model=ApiResponse)
async def create_book_link(
    book_data: BookLinkCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """创建书籍链接（管理员）"""
    book = BookLink(**book_data.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return ApiResponse(
        message="Book link created successfully",
        data=BookLinkResponse.from_orm(book)
    )

@router.put("/admin/books/{book_id}", response_model=ApiResponse)
async def update_book_link(
    book_id: int,
    book_data: BookLinkUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """更新书籍链接（管理员）"""
    book = db.query(BookLink).filter(BookLink.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book link not found"
        )
    
    # 更新字段
    update_data = book_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)
    
    db.commit()
    db.refresh(book)
    
    return ApiResponse(
        message="Book link updated successfully",
        data=BookLinkResponse.from_orm(book)
    )

@router.delete("/admin/books/{book_id}", response_model=ApiResponse)
async def delete_book_link(
    book_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """删除书籍链接（管理员）"""
    book = db.query(BookLink).filter(BookLink.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book link not found"
        )
    
    # 软删除
    book.status = "inactive"
    db.commit()
    
    return ApiResponse(
        message="Book link deleted successfully",
        data=None
    )

# 收藏相关API
@router.post("/favorites", response_model=ApiResponse)
async def add_favorite(
    favorite_type: str,
    favorite_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """添加收藏"""
    # 检查是否已经收藏
    existing_favorite = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id,
        UserFavorite.favorite_type == favorite_type,
        UserFavorite.favorite_id == favorite_id
    ).first()
    
    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already favorited"
        )
    
    # 创建新收藏
    favorite = UserFavorite(
        user_id=current_user.id,
        favorite_type=favorite_type,
        favorite_id=favorite_id
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    
    return ApiResponse(
        message="Favorite added successfully",
        data=UserFavoriteResponse.from_orm(favorite)
    )

@router.delete("/favorites/{favorite_id}", response_model=ApiResponse)
async def remove_favorite(
    favorite_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取消收藏"""
    favorite = db.query(UserFavorite).filter(
        UserFavorite.id == favorite_id,
        UserFavorite.user_id == current_user.id
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    db.delete(favorite)
    db.commit()
    
    return ApiResponse(
        message="Favorite removed successfully",
        data=None
    )

@router.get("/favorites", response_model=ApiResponse)
async def get_user_favorites(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """获取用户收藏列表"""
    offset = (page - 1) * page_size
    
    favorites = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id
    ).order_by(UserFavorite.created_at.desc()).offset(offset).limit(page_size).all()
    
    total = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id
    ).count()
    
    favorite_data = [UserFavoriteResponse.from_orm(fav) for fav in favorites]
    
    return ApiResponse(
        message="User favorites retrieved successfully",
        data=PaginatedResponse(
            total=total,
            page=page,
            page_size=page_size,
            records=favorite_data
        )
    )

# 搜索API
@router.get("/search", response_model=ApiResponse)
async def search_knowledge(
    keyword: str = Query(..., min_length=1),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """搜索知识库内容"""
    offset = (page - 1) * page_size
    
    # 搜索知识项目
    items_query = db.query(KnowledgeItem).filter(
        KnowledgeItem.status == "active",
        (KnowledgeItem.title.contains(keyword) |
         KnowledgeItem.content.contains(keyword) |
         KnowledgeItem.author.contains(keyword))
    )
    
    total = items_query.count()
    items = items_query.order_by(KnowledgeItem.created_at.desc()).offset(offset).limit(page_size).all()
    
    item_data = [KnowledgeItemResponse.from_orm(item) for item in items]
    
    return ApiResponse(
        message="Search completed successfully",
        data=PaginatedResponse(
            total=total,
            page=page,
            page_size=page_size,
            records=item_data
        )
    ) 