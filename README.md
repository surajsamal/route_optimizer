# Route Optimizer App

Optimized route for delivery from my favorite restaurant to my home — fast, smooth, and smart.

# Tools Used

- Streamlit – for building an interactive web app
- TomTom Maps API – for geocoding and route optimization
- Folium – to visualize the route on an interactive map
- Python Requests – to call the TomTom API

# What It Does

- Takes start and end locations
- Fetches the shortest/fastest route** using TomTom's routing engine
- Displays an interactive map with the optimized path
- Built for delivery apps, courier planning, and personal logistics

# Try It Out

You can run this locally:

```bash
git clone https://github.com/surajsamal/route_optimizer.git
cd route_optimizer
pip install -r requirements.txt
streamlit run route_optimizer.py
