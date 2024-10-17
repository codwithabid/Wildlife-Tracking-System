from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Dict, Optional
from database import database, SessionLocal
from models import SightingModel, Base

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        try:
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('Time must be in HH:MM format.')
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

@app.post("/sightings/", response_model=SightingResponse)
async def add_sighting(sighting: Sighting, db: Session = Depends(get_db)):
    db_sighting = SightingModel(**sighting.dict())
    
    # Check for existing sightings
    existing = db.query(SightingModel).filter(
        SightingModel.species.ilike(sighting.species),
        SightingModel.location.ilike(sighting.location),
        SightingModel.date == sighting.date,
        SightingModel.time == sighting.time,
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Sighting already exists with the same details.")

    db.add(db_sighting)
    db.commit()
    db.refresh(db_sighting)
    return SightingResponse(id=db_sighting.id, **sighting.dict())

@app.get("/sightings/", response_model=Dict[int, str])
async def view_sightings(db: Session = Depends(get_db)):
    sightings = db.query(SightingModel).all()
    if not sightings:
        raise HTTPException(status_code=404, detail="No sightings recorded")
    
    return {sighting.id: f"{sighting.species} at {sighting.location} on {sighting.date} at {sighting.time}" for sighting in sightings}

@app.get("/sightings/search/")
async def search_sightings(species: Optional[str] = None, location: Optional[str] = None, db: Session = Depends(get_db)):
    found_sightings = db.query(SightingModel).filter(
        (SightingModel.species.ilike(f"%{species}%") if species else True),
        (SightingModel.location.ilike(f"%{location}%") if location else True)
    ).all()

    if not found_sightings:
        raise HTTPException(status_code=404, detail="No sightings found for the given filters.")
    
    return {sighting.id: f"{sighting.species} at {sighting.location} on {sighting.date} at {sighting.time}" for sighting in found_sightings}

@app.put("/sightings/{sighting_id}", response_model=SightingResponse)
async def update_sighting(sighting_id: int, updated_sighting: Sighting, db: Session = Depends(get_db)):
    # Retrieve the sighting to update
    sighting_to_update = db.query(SightingModel).filter(SightingModel.id == sighting_id).first()

    # Check if the sighting exists
    if not sighting_to_update:
        raise HTTPException(status_code=404, detail="Sighting not found")

    # Update fields
    sighting_to_update.species = updated_sighting.species.title()
    sighting_to_update.location = updated_sighting.location.title()
    
    # Validate and update date
    try:
        sighting_date = datetime.strptime(updated_sighting.date, '%Y-%m-%d').date()
        if sighting_date > date.today():
            raise HTTPException(status_code=400, detail='Date cannot be in the future.')
        sighting_to_update.date = sighting_date  # Set the validated date
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid date format. Expected YYYY-MM-DD.')

    # Validate and update time
    try:
        # Ensure time is formatted correctly
        datetime.strptime(updated_sighting.time, '%H:%M')
        sighting_to_update.time = updated_sighting.time  # Only set if valid
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid time format. Expected HH:MM.')

    # Commit changes to the database
    db.commit()
    db.refresh(sighting_to_update)  # Refresh to get updated values
    
    # Return the updated sighting response
    return SightingResponse(
        id=sighting_to_update.id,
        species=sighting_to_update.species,
        location=sighting_to_update.location,
        date=sighting_to_update.date,
        time=sighting_to_update.time
    )

@app.delete("/sightings/{sighting_id}")
async def delete_sighting(sighting_id: int, db: Session = Depends(get_db)):
    sighting_to_delete = db.query(SightingModel).filter(SightingModel.id == sighting_id).first()
    if not sighting_to_delete:
        raise HTTPException(status_code=404, detail="Sighting not found")

    db.delete(sighting_to_delete)
    db.commit()
    return {"detail": "Sighting deleted successfully"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Sighting Tracker API! Use /docs for more information."}

# Start database connection
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
