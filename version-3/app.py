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
    return response.json() if response.status_code == 200 else {}

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

    if sighting_id in sightings:
        current_details = sightings[sighting_id]
        st.write(f"Current details: {current_details}")

        # Now accessing structured details
        species = current_details.split(' at ')[0]  # This assumes the format is "Species at Location ..."
        location = current_details.split(' at ')[1].split(' on ')[0]
        date = current_details.split(' on ')[1].split(' at ')[0]
        time = current_details.split(' at ')[1].split(' ')[-1]

        new_species = st.text_input("New Species", value=species)
        new_location = st.text_input("New Location", value=location)
        new_date = st.date_input("New Date", value=datetime.strptime(date, '%Y-%m-%d'))
        new_time = st.time_input("New Time", value=datetime.strptime(time, '%H:%M'))

        if st.button("Update"):
            result = update_sighting(sighting_id, new_species, new_location, new_date.isoformat(), new_time.strftime("%H:%M"))
            
            if result.status_code == 200:
                st.success("✅ Sighting updated successfully!")
            else:
                st.error("❌ Error updating sighting: " + result.json().get('detail', 'Unknown error'))
    else:
        st.write("🚫 Invalid sighting ID.")

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
