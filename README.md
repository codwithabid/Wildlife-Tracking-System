# Wildlife Tracking System

## Overview
This FastAPI application enables users to track and manage wildlife sightings. Users can create, read, update, and delete records, ensuring data integrity with built-in validations. 

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

## Versions
### [v1](https://github.com/codwithabid/Wildlife-Tracking-System/tree/main/version-1)
- **Description**: Initial version of the wildlife tracking API using FastAPI with an in-memory dictionary for data storage.
- **Features**: Basic CRUD operations for wildlife sightings, including input validation.

### [v2](https://github.com/codwithabid/Wildlife-Tracking-System/tree/main/version-2)
- **Description**: Enhanced version using FastAPI with PostgreSQL for data storage.
- **Features**: All features from v1, plus improved data persistence and reliability.

### [v3](https://github.com/codwithabid/Wildlife-Tracking-System/tree/main/version-3)
- **Description**: Final version integrating FastAPI for the backend, PostgreSQL for the database, and Streamlit for a user-friendly frontend.
- **Features**: Comprehensive wildlife tracking solution with a seamless user experience.

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
  This project is licensed under the [RIVON.AI](https://github.com/rivon-ai) License. See the LICENSE file for details.
