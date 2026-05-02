from os import name
from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state:str
    pin: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'mumbai', 'state': 'MH', 'pin': '123123'}

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'gender': 'male', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)
temp = patient1.model_dump(include=name)
temp = patient1.model_dump(exclude_unset=True)

#model_dump() is used to convert a model into a dictionary

print(type(temp))
print(patient1)

#Quick Summary Table
#Option	Meaning
#model_dump()	convert model → dict
#include	only these fields
#exclude	remove these fields
#exclude_unset	only user-provided values
#exclude_defaults	remove default values
#exclude_none	remove None values
#by_alias	use alias names
#mode="json"	JSON-safe output