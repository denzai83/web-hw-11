from datetime import datetime, date
from pydantic import BaseModel, EmailStr


class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: date
    
    
class ContactResponse(ContactModel):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True