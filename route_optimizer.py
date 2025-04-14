import requests
import folium
import streamlit as st

# === YOUR TOMTOM API KEY ===
TOMTOM_API_KEY = st.secrets["TOMTOM_API_KEY"]

# === INPUT LOCATIONS ===
origin = (12.9716, 77.5946)   # Restaurant: Bangalore
destination = (12.9352, 77.6145)  # Customer: Bangalore

def get_route(origin, destination, api_key):
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{origin[0]},{origin[1]}:{destination[0]},{destination[1]}/json"
    params = {
        "key": api_key,
        "traffic": "true"
    }

    response = requests.get(url, params=params)
    data = response.json()

    summary = data['routes'][0]['summary']
    route = data['routes'][0]['legs'][0]['points']

    return {
        "distance_km": summary['lengthInMeters'] / 1000,
        "travel_time_min": summary['travelTimeInSeconds'] / 60,
        "traffic_delay_min": summary['trafficDelayInSeconds'] / 60,
        "route_points": [(p['latitude'], p['longitude']) for p in route]
    }

def create_map(route_points, origin, destination):
    m = folium.Map(location=origin, zoom_start=13)
    folium.Marker(origin, tooltip="Origin", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(destination, tooltip="Destination", icon=folium.Icon(color='red')).add_to(m)
    folium.PolyLine(route_points, color="blue", weight=5).add_to(m)
    return m

# === Streamlit UI ===
st.title("Suraj's Delivery Route Optimizer")

route_info = get_route(origin, destination, TOMTOM_API_KEY)

st.write(f"**Distance:** {route_info['distance_km']:.2f} km")
st.write(f"**Estimated Time:** {route_info['travel_time_min']:.1f} mins")
st.write(f"**Traffic Delay:** {route_info['traffic_delay_min']:.1f} mins")

m = create_map(route_info['route_points'], origin, destination)
st.components.v1.html(m._repr_html_(), height=500)
