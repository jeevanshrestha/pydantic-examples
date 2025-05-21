from pydantic import BaseModel, EmailStr, Field, AnyUrl, field_validator, model_validator, computed_field
from typing import Annotated, Optional, List, Dict

class Address(BaseModel):
    """
    A class representing an address with various attributes.
    """
    street: str = Field(..., description="Street address")
    city: str = Field(..., description="City name")
    state: str = Field(..., description="State name")
    zip: str = Field(..., description="ZIP code")

    def __str__(self):
        return f"Address(street={self.street}, city={self.city}, state={self.state}, zip={self.zip})"
    

class EmergencyContact(BaseModel):
    """
    A class representing an emergency contact with various attributes.
    """
    name: str = Field(..., description="Name of the emergency contact")
    relationship: str = Field(..., description="Relationship to the patient")
    phone: str = Field(..., description="Phone number of the emergency contact")

    def __str__(self):
        return f"EmergencyContact(name={self.name}, relationship={self.relationship}, phone={self.phone})"

class Patient(BaseModel):
    """
    A class representing a patient with various attributes.
    """
    id: Optional[int] = Field(None, description="Unique identifier for the patient")
    name: str = Field(..., description="Name of the patient", min_length=1, max_length=100)

    #transformation example
    @field_validator("name")
    @classmethod
    def transform_name(cls, value: str) -> str: 
        return value.upper()
    
    email: EmailStr = Field(..., description="Email address of the patient")  

    #Email field validation example
    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        valid_domain = ["icici.com", "hdfc.com", "axis.com"]
        if not any(value.endswith(domain) for domain in valid_domain):
            raise ValueError("Email must end with one of the following domains: " + ", ".join(valid_domain))
        return value    
    age: int 

    #custom validator example
    @field_validator("age" , mode='after')
    @classmethod
    def validate_age(cls, value:int) -> int:
        if value < 0 or value > 120:
            raise ValueError("Age must be a between 0 to 120")
        return value
    phone: Optional[str] = Field(None, description="Phone number of the patient")
    linkedin: Optional[AnyUrl] = Field(None, description="LinkedIn profile URL of the patient")
    address: Optional[Address] = Field(None, description="Address of the patient")
    phone: Optional[str] = Field(None, description="Phone number of the patient")
    weight: float = Field(None, description="Weight of the patient in kg", ge=0)
    height: float = Field(None, description="Height of the patient in cm", ge=0)
    married: Annotated[bool, Field(default=False, description="Marital status of the patient")]
    allergies: Optional[List[str]] = Field(None, description="List of allergies the patient has", min_items=0, max_items=10)
    medications: Optional[List[str]] = Field(None, description="List of medications the patient is taking")
    emergency:  Optional[EmergencyContact] = Field(None, description="Emergency contact information")

    #computed field example
    @computed_field
    def bmi(self) -> float:
        if self.weight and self.height:
            height_in_meters = self.height / 100
            # BMI = weight (kg) / (height (m)^2)
            return round(self.weight / (height_in_meters ** 2), 2)
        return None


    @model_validator(mode='wrap')
    def check_emergency_contact(cls, values, handler):
        model = handler(values)
        if model.age > 60 and not model.emergency:
            raise ValueError("Emergency contact is required for patients over 60 years old")
        return model
    
    def __str__(self):
        return f"Patient(id={self.id}, name={self.name}, age={self.age}, weight={self.weight}, height={self.height}, allergies={self.allergies}, medications={self.medications})"

        class Config:
            strict = True  # Enforce strict validation
            anystr_strip_whitespace = True
            min_anystr_length = 1
            # Enable word wrapping for JSON schema descriptions in OpenAPI docs
            json_schema_extra = {
                "examples": [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "email": "johndoe@hdfc.com",
                        "age": 30,
                        "phone": "+1-555-1234",
                        "linkedin": "https://www.linkedin.com/in/johndoe",
                        "address": {
                            "street": "123 Main St",
                            "city": "Anytown",
                            "state": "CA",
                            "zip": "12345"
                        },
                        
                        "weight": 70.5,
                        "height": 175.0,
                        "married": False,
                        "allergies": ["Peanuts", "Penicillin"],
                        "medications": ["Aspirin"],
                        "emergency": {
                            "name": "Jane Doe",
                            "relationship": "Sister",
                            "phone": "+1-555-5678"
                        }
                        
                    }
                ]
            }


address   = Address(street="123 Main St", city="Anytown", state="CA", zip="12345")
emergency = EmergencyContact(name="Jane Doe", relationship="Sister", phone="+1-555-5678")
patient_info = {        
                        "name": "John Doe",
                        "email": "johndoe@icici.com",
                        "age": 65,
                        "phone": "+1-555-1234",
                        "linkedin": "https://www.linkedin.com/in/johndoe",
                        "address":address,
                        "weight": 70.5,
                        "height": 175.0,
                        "married": False,
                        "allergies": ["Peanuts", "Penicillin"],
                        "medications": ["Aspirin"],
                        "emergency": emergency
}

patient = Patient(**patient_info)
print(patient.model_dump())
print(patient.model_dump_json())