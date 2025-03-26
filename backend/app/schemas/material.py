from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class MaterialBase(BaseModel):
    """教材基础模型"""
    display_name: str = Field(..., description="教材名称")
    category_ids: str = Field(..., description="分类ID列表，逗号分隔")
    description: Optional[str] = Field(None, description="教材描述")
    cover: Optional[str] = Field(None, description="封面图片(base64)")
    type: str = Field(..., description="教材类型(upload/create)")

class MaterialCreate(MaterialBase):
    """创建教材请求模型"""
    blob_id: Optional[int] = Field(None, description="文件ID，上传类型教材必填")

class MaterialUpdate(MaterialBase):
    """更新教材请求模型"""
    display_name: Optional[str] = None
    category_ids: Optional[str] = None
    type: Optional[str] = None

class MaterialResponse(MaterialBase):
    """教材响应模型"""
    id: int
    blob_id: Optional[int] = None
    content: Optional[str] = None
    publish_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MaterialListResponse(BaseModel):
    """教材列表响应模型"""
    items: List[MaterialResponse]
    total: int
    page: int
    page_size: int 