from pydentic import BaseModel, Field #type:ignore
from typing import  Optional
from datetime import datetime
from pydantic import field_validator, model_validator, computed_field #type:ignore
from enum import Enum


class LessonType(Enum):
    VIDEO = "video"
    ARTICLE = "article"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    EXAM = "exam"
    ATTACHMENT = "attachment"
    OTHER = "other"



class CoursePromotions(BaseModel):

    promotion_id: int
    admin_id: int
    discount_percentage: float
    promo_code: str
    start_date: datetime
    end_date: datetime
    created_at: datetime = Field(default_factory=datetime.now)  
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    is_deleted: bool = False
    @model_validator(mode='after')  
    def check_dates(cls, values: dict) -> dict:
        if values.get("start_date") >= values.get("end_date"):
            raise ValueError("Start date must be before end date")
        return values

class CourseCategory(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    parent_category: Optional['CourseCategory'] = None  # for parent categories
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)  
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    is_deleted: bool = False
    @model_validator(mode='after')
    def check_parent_category(cls, values: dict) -> dict:
        if values.get("parent_category_id") == values.get("category_id"):
            raise ValueError("Parent category cannot be the same as the category itself")
        return values
    
CourseCategory.model_rebuild()
 


class Lesson(BaseModel):
    lesson_id: int
    topic: str
    description: str
    duration: int  # in seconds
    lesson_type: LessonType  # e.g., video, article, quiz
    content: str # URL or path to the content
    created_at: datetime = Field(default_factory=datetime.now)  
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    is_deleted: bool = False

class Module(BaseModel):
    module_id: int
    name: str
    description: str
    lessons: Optional[list[Lesson]] = []
    created_at: datetime = Field(default_factory=datetime.now)  
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    is_deleted: bool = False

class Course(BaseModel):
    course_id: int
    title: str
    description: str
    instructor_id: int
    thumbnail: Optional[str] = None  # URL or path to the thumbnail 
    price: float
    discount: Optional[float] = None  # percentage discount
    category: CourseCategory
    prerequisites: Optional[str] = None  # e.g., "Basic Python
    modules: Optional[list[Module]]  = []
    created_at: datetime = Field(default_factory=datetime.now)  
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True
    is_deleted: bool = False

    @computed_field
    def total_duration(self) -> int:
        return sum(lesson.duration for module in self.modules for lesson in module.lessons) 
    


