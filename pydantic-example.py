from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field #type:ignore
from pydantic import ConfigDict
from typing import List ,  Dict, Optional
import json

class Cart(BaseModel):
    id: int
    sku: str = Field(..., description="SKU of the product", example="ABC123")
    name: str
    price: float
    quantity: int
    
class BlogItem(BaseModel):
    id: int
    title: str
    content: str
    imageUrl: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

# Example of a model with required and optional fields
class Employe(BaseModel):
    id:int
    name:str = Field(..., 
                     min_length=3, 
                     max_length=50, 
                     pattern="^[a-zA-Z ]*$", 
                     description  = "Employee Name",
                     example= "Jeevan Shrestha")
    age:int
    imageUrl: Optional[str] = None
    department: Optional[str] = "General"
    salary: float   = Field(..., gt=1000, description="Salary must be greater than 1000")     

# Example of field validator
# This validator checks if the username is at least 4 characters long
class User(BaseModel):
    username: str
    @field_validator('username')
    def username_validation(cls, v):
        if len(v) <4:
            raise ValueError('Username must be 4 characters')
        
        return v
# Example of model validator
class SignupData(BaseModel):
    username: str
    @field_validator('username')
    def username_validation(cls, v):
        if len(v) <4:
            raise ValueError('Username must be 4 characters')
        
        return v
    password: str
    confirm_password: str
    @model_validator(mode='after')
    def password_match(cls, values):
        if values.password != values.confirm_password:
            raise ValueError('Password and Confirm Password do not match')
        return values
    
    created_at: datetime  
    updated_at: datetime 

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.strftime('%d/%m/%Y %H:%M'),
        }
    )

# Example of a model with a computed field
class ComputedCartItem(BaseModel):
    price: float
    quantity: int
    @computed_field
    @property
    def total_price(self) -> float:
        return self.price * self.quantity
    
class CartItem(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    @computed_field
    @property
    def total_price(self) -> float:
        return self.price * self.quantity

class Booking(BaseModel):
    user_id: int
    room_id: int
    check_in: datetime
    nights: int = Field(..., gt=1, description="Nights must be greater than 1")
    rate_per_night: float = Field(..., gt=0, description="Rate per night must be greater than 0")
    @computed_field
    @property
    def total_amount(self) -> float:
        return self.nights * self.rate_per_night
        
# Example of Nested Models

class Address(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str
class UserProfile(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z ]*$")
    email: str = Field(..., pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    age: int
    address: Address
    phone_numbers: str
    cart: List[Cart] = Field(default_factory=list)   
    cart: List[Cart] = []   
class Comment(BaseModel):
    id: int
    post_id: int
    comment: str
    parent_id: Optional[int] = None
    replies: Optional[List['Comment']] = Field(default_factory=list)  # Forward reference to allow nested comments 

Comment.model_rebuild()  # Rebuild the model to resolve forward references
Comment.model_rebuild()  # Rebuild the model to resolve forward references
class UserSettings(BaseModel):
    user_id: int
    settings: Dict[str, str] = Field(default_factory=dict)   
    settings: Dict[str, str] = {}   

class UserPreferences(BaseModel):
    user_id: int
    preferences: List[str] = Field(default_factory=list)  # List of user preferences     
    preferences: List[str] = []  # List of user preferences     

class UserActivities(BaseModel):
    user_id: int
    activities: List[Dict[str, str]] = Field(default_factory=list)  # List of user activities with key-value pairs
    activities: List[Dict[str, str]] = []  # List of user activities with key-value pairs

userActivities = UserActivities(
    user_id=1,
    activities=[
        {"activity": "login", "timestamp": "2023-10-01T12:00:00Z"},
        {"activity": "logout", "timestamp": "2023-10-01T14:00:00Z"},
    ]
)   

userPreferences = UserPreferences(
    user_id=1,
    preferences=["dark_mode", "email_notifications"]
)   

UserSettings    = UserSettings(
    user_id=1,
    settings={
        "theme": "dark",
        "language": "en",
        "notifications": "enabled"
    }
)   

userProfile = UserProfile(
    id=1,
    name="John Doe",
    email="jeevanshrestha09@gmail.com",
    age=30,
    address=Address(
        street="123 Main St",
        city="Kathmandu",
        state="Bagmati",
        postal_code="44600",
        country="Nepal"
    ),
    phone_numbers="1234567890",
    cart=[
        Cart(id=1, sku="ABC123", name="Product 1", price=10.0, quantity=2),
        Cart(id=2, sku="XYZ456", name="Product 2", price=20.0, quantity=1)
    ]
)
# Example of creating a BlogItem instance
blog_item = BlogItem(
    id=1,
    title="My First Blog Post",
    content="This is the content of my first blog post.",
    imageUrl="https://example.com/image.jpg",
    tags=["python", "pydantic"]
)      


# Example of creating an Employe instance
employe = Employe(
    id=1,
    name="John Doe",
    age=30,
    imageUrl="https://example.com/image.jpg",
    department="Engineering",
    salary=5000.0
)
# Example of creating a comment instance
comment = Comment(
    id=1,
    post_id=1,
    comment="This is a comment.",
    parent_id=None,
    replies=[
        Comment(
            id=2,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=1
        )
    ]
)

# example of comment instance with 15 nexted comments
comments = Comment(
    id=1,
    post_id=1,
    comment="This is a comment.",
    parent_id=None,
    replies=[
        Comment(
            id=2,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=1
        ),
        Comment(
            id=3,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=2
        ),
        Comment(
            id=4,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=3
        ),
        Comment(
            id=5,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=2
        ),
        Comment(
            id=6,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=5
        ),
        Comment(
            id=7,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=6
        ),  
        Comment(
            id=8,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=5
        ),
        Comment(
            id=9,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=8
        ),
        Comment(
            id=10,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=9
        ),  
        Comment(
            id=11,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=8
        ),  
        Comment(
            id=12,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=11
        ),
        Comment(
            id=13,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=2
        ),  
        Comment(
            id=14,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=13
        ),
        Comment(
            id=15,
            post_id=1,
            comment="This is a reply to the comment.",
            parent_id=14
        )
    ]
)

json_data = comments.model_dump_json(indent=2)
def build_comment_tree(comments_list):
    comment_dict = {c['id']: {**c, 'replies': []} for c in comments_list}
    root = []
    for c in comments_list:
        if c['parent_id']:
            parent = comment_dict.get(c['parent_id'])
            if parent:
                parent['replies'].append(comment_dict[c['id']])
        else:
            root.append(comment_dict[c['id']])
    return root

comments_flat = json.loads(json_data)
if isinstance(comments_flat, dict):
    # flatten nested replies into a flat list
    def flatten(comment, acc):
        acc.append({k: v for k, v in comment.items() if k != 'replies'})
        for r in comment.get('replies', []):
            flatten(r, acc)
    flat_list = []
    flatten(comments_flat, flat_list)
    tree = build_comment_tree(flat_list)
    print(json.dumps(tree, indent=2))
else:
    print("Invalid JSON data for comment tree.")


#Serializing and Deserializing

# Serialize to JSON
signupdata = SignupData( 
    username="jeevanshrestha09",
    password="password123",
    confirm_password="password123",
    created_at=datetime(2025, 5, 16, 20, 47),
    updated_at=datetime(2025, 5, 16, 20, 47)
)
dict_data_signup = signupdata.model_dump()
print("Serialized dictionary data:")    
print(dict_data_signup)
json_data_signup = signupdata.model_dump_json(indent=2)
print("Serialized JSON data:")
print(json_data_signup)