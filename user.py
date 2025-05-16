from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from datetime import datetime
from pydantic import field_validator, model_validator, computed_field #type:ignore
import bcrypt
from course import Course, CourseCategory


class User(BaseModel):
    user_id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, pattern=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    confirm_password: str = Field(..., min_length=8)
    @field_validator("password")
    def hash_password(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    @model_validator(mode="after")
    def check_passwords(cls, values: dict) -> dict:
        if values.get("password") != values.get("confirm_password"):
            raise ValueError("Passwords do not match")
        return values
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = False
    is_deleted: bool = False
    is_verified: bool = False

class Address(BaseModel):
    address_id: int
    street: str
    city: str
    state: str
    country: str
    postal_code: str
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    

class UserProfile(BaseModel):  
    user_id: int
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    adress: Optional[Address] = None
    phone_number: Optional[str] = None
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    

class Instructor(BaseModel):
    instructor_id: int
    user_id: int
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    expertise: Optional[str] = None 
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    payment_info: Optional[str] = None  # URL or path to payment info
    is_active: bool = True
    is_deleted: bool = False


class Admin(BaseModel):
    admin_id: int
    user_id: int
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    is_active: bool = True
    is_deleted: bool = False


class UserSettings(BaseModel):
    user_id: int
    email_notifications: bool = True
    sms_notifications: bool = False
    push_notifications: bool = False
    dark_mode: bool = False


class UserActivity(BaseModel):
    user_id: int
    last_login: Optional[str] = Field(default=None)
    last_activity: Optional[str] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    is_active: bool = True
    is_deleted: bool = False


class UserEnrolment(BaseModel):
    enrolment_id: int
    user_id: int
    course_id: int
    enrollment_date: Optional[str] = Field(default=None)
    progress: float = 0.0  # Progress percentage
    is_active: bool = True
    is_deleted: bool = False
    is_completed: bool = False

class UserFeedback(BaseModel):
    feedback_id: int
    user_id: int
    course_id: int
    rating: int  =Field(..., ge=1, le=5  )# 1 to 5 scale
    comment: Optional[str] = None
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    is_user_enrolled: bool = False
    is_anonymous: bool = False
    is_active: bool = True
    is_deleted: bool = False

class InstructorRevenue(BaseModel):
    revenue_id: int
    instructor_id: int
    revenue: float
    enrolment_id: int
    payment_date: Optional[str] = Field(default=None)
    revenue_split: float =  revenue # 70% to instructor, 30% to platform
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None) 


class InstructorPayment(BaseModel):
    payment_id: int
    instructor_id: int
    payment_info: Optional[str] = None  # URL or path to payment info
    amount: float
    payment_date: Optional[str] = Field(default=None)
    payment_method: str  # e.g., PayPal, bank transfer
    payment_status: str
    payment_reference: Optional[str] = None
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)