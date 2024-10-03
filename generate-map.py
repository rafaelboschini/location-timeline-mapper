import json
import folium
from datetime import datetime
from flask import Flask, render_template_string, request

# Function to read the "Timeline Edits.json" file and return coordinates, timestamps, and speed
def read_timeline_edits(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    points = []
    for edit in data.get("timelineEdits", []):
        if "rawSignal" in edit and "signal" in edit["rawSignal"] and "position" in edit["rawSignal"]["signal"]:
            position = edit["rawSignal"]["signal"]["position"]
            lat = position["point"]["latE7"] / 1e7  # Latitude
            lng = position["point"]["lngE7"] / 1e7  # Longitude
            timestamp = position["timestamp"]  # Timestamp
            speed = position.get("speedMetersPerSecond", 0)  # Speed (if available)
            points.append((lat, lng, timestamp, speed))
    
    return points

# Function to assign marker colors based on the day of the week
def assign_color_by_day(iso_date):
    date = datetime.fromisoformat(iso_date)
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'pink', 'yellow']
    return colors[date.weekday()]

# Function to create the map with filters
def create_map(points, year=None, month=None, day=None):
    # Apply filters (if any)
    if year or month or day:
        filtered_points = []
        for point in points:
            date = datetime.fromisoformat(point[2])
            if (year and date.year != int(year)) or (month and date.month != int(month)) or (day and date.day != int(day)):
                continue
            filtered_points.append(point)
        points = filtered_points

    # Check if there are any points to display
    if not points:
        print("No points to display on the map.")
        return None

    # Center the map on the first point
    map_object = folium.Map(location=[points[0][0], points[0][1]], zoom_start=12)
    
    # Add markers to the map
    for point in points:
        lat, lng, timestamp, speed = point
        color = assign_color_by_day(timestamp)
        formatted_timestamp = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # Create popup text with timestamp and link to Google Maps
        popup_text = f"""
        <b>Timestamp:</b> {formatted_timestamp}<br>
        <a href="https://www.google.com/maps?q={lat},{lng}" target="_blank">Open in Google Maps</a>
        """
        if speed > 0:
            popup_text += f"<br><b>Speed:</b> {speed} m/s"

        folium.CircleMarker(
            location=[lat, lng],
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(map_object)
    
    # Save the map to an HTML file
    map_object.save('templates/map.html')

# Function to extract available years, months, and days from the data
def extract_date_options(points):
    years = set()
    months = set()
    days = set()
    
    for point in points:
        date = datetime.fromisoformat(point[2])
        years.add(date.year)
        months.add((date.year, date.month))
        days.add((date.year, date.month, date.day))
    
    return sorted(years), sorted(months), sorted(days)

# Flask app to create the web interface
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Read the JSON file
    points = read_timeline_edits('Timeline Edits.json')
    
    # Extract date options (years, months, days)
    years, months, days = extract_date_options(points)

    # Get selected filters
    year = request.form.get('year')
    month = request.form.get('month')
    day = request.form.get('day')

    # Create the map based on the selected filters
    create_map(points, year, month, day)
    
    # Render the HTML page with map and filters
    return render_template_string('''
    <html>
    <head>
        <title>Location Map</title>
    </head>
    <body>
        <h1>Location Map</h1>
        <form method="POST">
            <label for="year">Year:</label>
            <select name="year" id="year">
                <option value="">All</option>
                {% for y in years %}
                    <option value="{{ y }}" {% if y == year %}selected{% endif %}>{{ y }}</option>
                {% endfor %}
            </select>

            <label for="month">Month:</label>
            <select name="month" id="month">
                <option value="">All</option>
                {% for (y, m) in months %}
                    <option value="{{ m }}" {% if month and m == month|int %}selected{% endif %}>
                        {{ y }}-{{ m }}
                    </option>
                {% endfor %}
            </select>

            <label for="day">Day:</label>
            <select name="day" id="day">
                <option value="">All</option>
                {% for (y, m, d) in days %}
                    <option value="{{ d }}" {% if day and d == day|int %}selected{% endif %}>
                        {{ y }}-{{ m }}-{{ d }}
                    </option>
                {% endfor %}
            </select>

            <button type="submit">Filter</button>
        </form>

        <iframe src="/map.html" width="100%" height="600px"></iframe>
    </body>
    </html>
    ''', years=years, months=months, days=days, year=year, month=month, day=day)

@app.route('/map.html')
def display_map():
    return render_template_string(open('templates/map.html').read())

if __name__ == '__main__':
    app.run(debug=True)
