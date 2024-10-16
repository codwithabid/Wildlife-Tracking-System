from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import Dict, Optional
from datetime import datetime, date

app = FastAPI()

class Sighting(BaseModel):
    species: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')  # YYYY-MM-DD
    time: str = Field(..., pattern=r'^\d{2}:\d{2}$')       # HH:MM

    @validator('date')
    def validate_date(cls, v):
        sighting_date = datetime.strptime(v, '%Y-%m-%d').date()
        if sighting_date > date.today():
            raise ValueError('Date cannot be in the future.')
        return v

    @validator('time')
    def validate_time(cls, v):
        datetime.strptime(v, '%H:%M')  # This will raise if invalid
        return v

    @validator('species', 'location')
    def capitalize(cls, v):
        return v.strip().title()  # Capitalizes each word and removes extra spaces

class SightingResponse(BaseModel):
    id: int
    species: str
    location: str
    date: str
    time: str

class SightingUpdate(BaseModel):
    location: Optional[str]
    date: Optional[str]
    time: Optional[str]

sightings_dict: Dict[int, Sighting] = {}
sighting_id_counter = 1

@app.post("/sightings/", response_model=SightingResponse)
async def add_sighting(sighting: Sighting):
    # Check for existing sightings
    for existing_id, existing_sighting in sightings_dict.items():
        if (existing_sighting.species.lower() == sighting.species.lower() and
            existing_sighting.location.lower() == sighting.location.lower() and
            existing_sighting.date == sighting.date and
            existing_sighting.time == sighting.time):
            raise HTTPException(status_code=400, detail="Sighting already exists with the same details.")

    global sighting_id_counter
    sightings_dict[sighting_id_counter] = sighting
    response = SightingResponse(id=sighting_id_counter, **sighting.dict())
    sighting_id_counter += 1
    return response

@app.get("/sightings/", response_model=Dict[int, str])
async def view_sightings():
    if not sightings_dict:
        raise HTTPException(status_code=404, detail="No sightings recorded")
    return {sighting_id: f"{sighting.species} at {sighting.location} on {sighting.date} at {sighting.time}"
            for sighting_id, sighting in sightings_dict.items()}

@app.get("/sightings/search/")
async def search_sightings(species: Optional[str] = None, location: Optional[str] = None):
    found_sightings = {
        sighting_id: sighting for sighting_id, sighting in sightings_dict.items()
        if (species is None or species.lower() in sighting.species.lower()) and
           (location is None or location.lower() in sighting.location.lower())
    }

    if not found_sightings:
        raise HTTPException(status_code=404, detail="No sightings found for the given filters.")
    
    return {sighting_id: f"{sighting.species} at {sighting.location} on {sighting.date} at {sighting.time}"
            for sighting_id, sighting in found_sightings.items()}

@app.put("/sightings/{sighting_id}", response_model=SightingResponse)
async def update_sighting(sighting_id: int, updated_sighting: SightingUpdate):
    if sighting_id not in sightings_dict:
        raise HTTPException(status_code=404, detail="Sighting not found")

    existing_sighting = sightings_dict[sighting_id]

    # Update fields if provided in the request
    if updated_sighting.location is not None:
        existing_sighting.location = updated_sighting.location.title()  # Capitalize location
    if updated_sighting.date is not None:
        # Validate new date
        sighting_date = datetime.strptime(updated_sighting.date, '%Y-%m-%d').date()
        if sighting_date > date.today():
            raise HTTPException(status_code=400, detail='Date cannot be in the future.')
        existing_sighting.date = updated_sighting.date
    if updated_sighting.time is not None:
        # Validate new time
        datetime.strptime(updated_sighting.time, '%H:%M')  # This will raise if invalid
        existing_sighting.time = updated_sighting.time

    return SightingResponse(id=sighting_id, **existing_sighting.dict())

@app.delete("/sightings/{sighting_id}")
async def delete_sighting(sighting_id: int):
    if sighting_id not in sightings_dict:
        raise HTTPException(status_code=404, detail="Sighting not found")

    # Delete the sighting
    del sightings_dict[sighting_id]
    return {"detail": "Sighting deleted successfully"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Sighting Tracker API! Use /docs for more information."}
