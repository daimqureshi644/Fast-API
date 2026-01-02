from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field, field_validator, computed_field
from typing import List, Dict, Optional, Annotated, Literal
import json
import os

app = FastAPI(title="Daim Qurehi Patient Managments System (Backend)")

def load_data():
    if not os.path.exists('patients.json'):
        return{
            "P001": {"id": "P001", "name": "Daim", "city": "Abbottabad", "age": 22, "gender": "male", 
                     "height": 1.75, "weight": 72.0, "email": "daim@hdfc.com"},
            "P002": {"id": "P002", "name": "Qureshi", "city": "Karachi", "age": 25, "gender": "male",
                      "height": 1.82, "weight": 88.5, "email": "qureshi@icici.com"}
        }
    with open ('patients.json','r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return{}
        
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=4)

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Unique ID", examples=["P001"])]
    name: Annotated[str, Field(..., max_length=50, examples=["Daim"])]
    email: EmailStr
    city: str
    age: Annotated[int, Field(..., gt=0, lt=120)]
    gender: Literal['male', 'female', 'other']
    height: Annotated[float, Field(..., gt=0, description="Height in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kg")]


    @field_validator('email')
    @classmethod
    def validate_domain(cls, value):
        valid_domains = ['hdfc.com', 'icici.com', 'gmail.com']
        if value.split('@')[-1] not in valid_domains:
            raise ValueError("Only hdfc.com, icici.com or gmail.com allowed")
        return value

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5: return "Underweight"
        elif self.bmi < 25: return "Normal"
        return "Overweight"

@app.get("/")
def home():
    return {"Project": "FastAPI Practice", "User": "Daim Qureshi", "Status": "Active"}

@app.get("/view-all")
def get_all():
    return load_data()

@app.post("/add-patient")
def add_patient_api(patient: Patient): # Renamed to avoid conflict with Streamlit function
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="ID already exists!")
    data[patient.id] = patient.model_dump()
    save_data(data)
    return {"message": "Success", "patient": data[patient.id]}

@app.get("/search/{p_id}")
def search_patient(p_id: str): # Renamed to avoid conflict with Streamlit function
    data = load_data()
    if p_id in data:
        return data[p_id]
    raise HTTPException(status_code=404, detail="Patient Not Found")

@app.put("/update-patient/{p_id}")
def update_patient(p_id: str, patient: Patient):
    data = load_data()
    if p_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")
    
    data[p_id] = patient.model_dump()
    save_data(data)
    return {"message": "Patient updated successfully", "patient": data[p_id]}

@app.delete("/delete-patient/{p_id}")
def delete_patient(p_id: str):
    data = load_data()
    if p_id not in data:
        raise HTTPException(status_code=404, detail="Patient Not Found")
    
    del data[p_id]
    save_data(data)
    return {"message": "Patient deleted successfully"}