import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

def add_sighting(species, location, date, time):
    response = requests.post(f"{API_URL}/sightings/", json={
        "species": species,
        "location": location,
        "date": date,
        "time": time
    })
    return response

def view_sightings():
    response = requests.get(f"{API_URL}/sightings/")
    if response.status_code == 200:
        sightings_dict = response.json()
        sightings = []

        for sighting_id, sighting_str in sightings_dict.items():
            st.write(f"Processing sighting: {sighting_id}: {sighting_str}")

            # Split the string correctly based on expected format
            parts = sighting_str.split(' on ')
            if len(parts) < 2:
                st.warning("Unexpected format for sighting. Skipping...")
                continue
            
            # Extract species and location
            species_location = parts[0].rsplit(' at ', 1)  # Split only once from the right
            if len(species_location) != 2:
                st.warning("Unexpected format for species and location. Skipping...")
                continue
            
            species = species_location[0].strip()
            location = species_location[1].strip()
            
            # Extract date and time
            date_time = parts[1].strip()  # This is now "Date at Time"
            date_part, time_part = date_time.split(' at ')  # This should correctly split
            date_part = date_part.strip()
            time_part = time_part.strip()

            sightings.append({
                'species': species,
                'location': location,
                'date': date_part,
                'time': time_part,
                'id': int(sighting_id)  # Use the actual sighting ID
            })
        
        return sightings
    return []

def search_sightings(species):
    response = requests.get(f"{API_URL}/sightings/search/", params={"species": species})
    return response.json() if response.status_code == 200 else {}

def update_sighting(sighting_id, species, location, date, time):
    response = requests.put(f"{API_URL}/sightings/{sighting_id}", json={
        "species": species,
        "location": location,
        "date": date,
        "time": time
    })
    return response

def delete_sighting(sighting_id):
    response = requests.delete(f"{API_URL}/sightings/{sighting_id}")
    return response

# Set page config
st.set_page_config(page_title="Wildlife Tracking System", layout="wide")

# Title styling
st.markdown("""
    <style>
        body {
            color: white;
            background-color: #4CAF50; /* Optional: Change background color */
        }
        .header {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            color: #FFFFFF; /* Header text color */
        }
        .subheader {
            font-size: 20px;
            text-align: center;
            color: #FFFFFF; /* Subheader text color */
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h2 class='subheader'>Welcome to the</h2>", unsafe_allow_html=True)
st.markdown("<h1 class='header'>🌿 Wildlife Tracking System 🌿</h1>", unsafe_allow_html=True)

menu = ["Add a new sighting", "View all sightings", "Search sightings by species", "Update a sighting", "Delete a sighting", "Exit"]
choice = st.selectbox("Select an option", menu)

if choice == "Add a new sighting":
    st.subheader("Add Sighting")
    species = st.text_input("Species", placeholder="Enter the species name")
    location = st.text_input("Location", placeholder="Enter the location")
    date = st.date_input("Date", value=datetime.today())
    time = st.time_input("Time")

    if st.button("Submit"):
        result = add_sighting(species, location, date.isoformat(), time.strftime("%H:%M"))
        if result.status_code == 200:
            st.success("✅ Sighting added successfully!")
        else:
            st.error("❌ Error adding sighting: " + result.json().get('detail', 'Unknown error'))

elif choice == "View all sightings":
    st.subheader("All Sightings")
    sightings = view_sightings()
    if sightings:
        for sighting_id, details in sightings.items():
            st.write(f"**{sighting_id}**: {details}")
    else:
        st.write("🚫 No sightings recorded.")

elif choice == "Search sightings by species":
    st.subheader("Search Sightings")
    search_species = st.text_input("Enter species name to search")
    if st.button("Search"):
        results = search_sightings(search_species)
        if results:
            for sighting_id, details in results.items():
                st.write(f"**{sighting_id}**: {details}")
        else:
            st.write("🚫 No sightings found for the given species.")

elif choice == "Update a sighting":
    st.subheader("Update Sighting")
    sighting_id = st.number_input("Enter the sighting ID to update", min_value=0, step=1)
    sightings = view_sightings()

    # Assuming sightings is a list of dictionaries
    sighting_map = {sighting['id']: sighting for sighting in sightings}

    if sighting_id in sighting_map:
        current_details = sighting_map[sighting_id]
        st.write(f"Current details: {current_details}")

        # Accessing structured details directly
        species = current_details['species']
        location = current_details['location']
        date = current_details['date']
        time = current_details['time']

        new_species = st.text_input("New Species", value=species)
        new_location = st.text_input("New Location", value=location)
        new_date = st.date_input("New Date", value=datetime.strptime(date, '%Y-%m-%d'))
        new_time = st.time_input("New Time", value=datetime.strptime(time, '%H:%M:%S'))

        if st.button("Update"):
            result = update_sighting(sighting_id, new_species, new_location, new_date.isoformat(), new_time.strftime("%H:%M"))

            # Check if the request was successful
            if result.status_code == 200:
                st.success("✅ Sighting updated successfully!")
            else:
                # Try to get the error detail, but don't let it interfere with the success message
                try:
                    error_detail = result.json().get('detail', 'Unknown error')
                    st.warning(f"Update completed, but with issues: {error_detail}")
                except ValueError:
                    # Log the raw response for debugging
                    print(f"Update Response: {result.status_code} - {result.text}")
                    st.warning("Update completed, but an error occurred. Please check the logs for details.")
    else:
        st.write("🚫 Invalid sighting ID. Please check the ID and try again.")

elif choice == "Delete a sighting":
    st.subheader("Delete Sighting")
    sighting_id = st.number_input("Enter the sighting ID to delete", min_value=1, step=1)
    if st.button("Delete"):
        result = delete_sighting(sighting_id)
        if result.status_code == 200:
            st.success("✅ Sighting deleted successfully!")
        else:
            st.error("❌ Error deleting sighting: " + result.json().get('detail', 'Unknown error'))

elif choice == "Exit":
    st.write("👋 Thank you for using the Wildlife Tracking System!")
