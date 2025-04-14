import streamlit as st
import folium
import requests
from streamlit_folium import st_folium

# Load your TomTom API key from Streamlit secrets
TOMTOM_API_KEY = st.secrets["TOMTOM_API_KEY"]

st.set_page_config(page_title="Route Optimizer", layout="centered")
st.title("🗺️ Route Optimizer from Origin to Destination")

st.markdown("Enter the **coordinates** for your Origin and Destination below:")

# Input fields for coordinates
with st.form("coords_form"):
    st.subheader("Origin")
    origin_lat = st.number_input("Origin Latitude", format="%.6f", value=19.076090)
    origin_lon = st.number_input("Origin Longitude", format="%.6f", value=72.877426)

    st.subheader("Destination")
    dest_lat = st.number_input("Destination Latitude", format="%.6f", value=19.218330)
    dest_lon = st.number_input("Destination Longitude", format="%.6f", value=72.978088)

    submitted = st.form_submit_button("Get Optimized Route")

if submitted:
    # Construct TomTom Routing API URL
    route_url = f"https://api.tomtom.com/routing/1/calculateRoute/{origin_lat},{origin_lon}:{dest_lat},{dest_lon}/json?key={TOMTOM_API_KEY}&traffic=false"

    # Call the API
    response = requests.get(route_url)

    if response.status_code == 200:
        data = response.json()
        route = data["routes"][0]["legs"][0]["points"]

        # Create folium map centered at origin
        m = folium.Map(location=[origin_lat, origin_lon], zoom_start=13)

        # Draw polyline on map
        folium.PolyLine(
            locations=[(pt["latitude"], pt["longitude"]) for pt in route],
            color="blue",
            weight=5
        ).add_to(m)

        # Add markers
        folium.Marker([origin_lat, origin_lon], tooltip="Origin", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker([dest_lat, dest_lon], tooltip="Destination", icon=folium.Icon(color="red")).add_to(m)

        # Display map in Streamlit
        st.subheader("Optimized Route:")
        st_folium(m, width=700, height=500)
    else:
        st.error("Failed to get route. Check coordinates or API key.")

