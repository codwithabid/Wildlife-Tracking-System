# Wildlife Tracking API

## Overview
This FastAPI application enables users to track and manage wildlife sightings. Users can create, read, update, and delete records, ensuring data integrity with built-in validations. The current version utilizes an in-memory dictionary for storage, with plans for future enhancements to integrate PostgreSQL and a Streamlit frontend.

## Features
- **Create Sightings**: Add new wildlife sightings with species, location, date, and time.
- **Read Sightings**: View all recorded sightings or search by species and location.
- **Update Sightings**: Modify existing sightings while preserving the species name and ID.
- **Delete Sightings**: Remove sightings by ID.
- **Input Validation**: Ensure data integrity with validation for date and time formats, and capitalized entries for species and location.

## API Endpoints
### 1. Add a Sighting
- **POST** `/sightings/`
- **Request Body**: 
    ```json
    {
      "species": "Example Species",
      "location": "Example Location",
      "date": "YYYY-MM-DD",
      "time": "HH:MM"
    }
    ```

### 2. View All Sightings
- **GET** `/sightings/`

### 3. Search Sightings
- **GET** `/sightings/search/?species=example&location=example`

### 4. Update a Sighting
- **PUT** `/sightings/{sighting_id}`
- **Request Body**:
    ```json
    {
      "location": "Updated Location",
      "date": "YYYY-MM-DD",
      "time": "HH:MM"
    }
    ```

### 5. Delete a Sighting
- **DELETE** `/sightings/{sighting_id}`

## Future Enhancements
- **v1**: Wildlife tracking using FastAPI and a dictionary for data storage.
- **v2**: Wildlife tracking using FastAPI and PostgreSQL for data storage.
- **v3**: Wildlife tracking using FastAPI for the backend, PostgreSQL for the database, and Streamlit for the frontend.

## Installation
To run the application locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wildlife-tracking-api.git
   cd wildlife-tracking-api

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

4. Install the required packages:
   ```bash
   pip install fastapi uvicorn

6. Run the application:
   ```bash
   uvicorn main:app --reload

## Usage
  Once the application is running, visit http://localhost:8000/docs for interactive API documentation using Swagger UI.

## License
  This project is licensed under the RIVON License. See the LICENSE file for details.
