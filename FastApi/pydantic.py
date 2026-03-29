from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    married: bool = False
    allergies: Optional[List[str]] = None
    contact: Dict[str, str] = None
    phone: str = Field(..., min_length=10, max_length=10)

def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print(patient.phone)

p = Patient(name="John", age=30, weight=70.5, married=True, allergies=["penicillin"], contact={"email": "john@example.com", "phone": "1234567890"}, phone="1234567890")
update_patient(p)
print(p)    

