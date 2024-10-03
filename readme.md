
# 🌍 Location Timeline Mapper
This project generates an interactive map from Google's **Timeline Edits.json** file. It marks your location points on the map with different colors based on the day of the week and allows filtering by year, month, and day. You can also click on each point to view the timestamp and a link to open the location in Google Maps!

## 🚀 Features
-  **Color-coded map markers**: Each day of the week has its own color for easy differentiation.

-  **Popups with timestamps**: View the exact time of each location point.

-  **Google Maps integration**: Click on the map markers to open that location directly in Google Maps.

-  **Speed display**: If available, the speed (in meters per second) will also be shown for each point.

-  **Date filtering**: Use dropdowns to filter locations by year, month, and day.

## 🛠️ Installation

### Requirements
- Python 3.7 or higher

### Install Dependencies
1. Clone this repository:
```bash
git clone https://github.com/rafaelboschini/location-timeline-mapper
``` 

2. Navigate to the project directory:
```bash
cd location-timeline-mapper
``` 

3. Install the required dependencies:
```bash
pip install flask folium
``` 

4. Place your `Timeline Edits.json` file in the root folder of this project.

### Dependencies
-  **Flask**: Used to run a local web server and create a simple web interface.

-  **Folium**: Generates the interactive map using Leaflet.js.

Install them with: `pip install flask folium`

Alternatively,  you  can  install  them  all  using  the  requirements.txt:
pip  install  -r  requirements.txt 

### 📊 Usage
Run  the  Flask  application: `python generate-map.py`

Open  your  browser  and  go  to  http://127.0.0.1:5000/.
Use  the  dropdown  filters  to  select  specific  dates  or  view  all  location  points.
Click  on  any  marker  to  view  the  timestamp  and  open  the  location  in  Google  Maps.  

### 📂 Directory Structure

    location-timeline-mapper/
    │
    ├──  generate-map.py  # Main application script
    ├──  Timeline  Edits.json  # Your JSON file with timeline data
    ├──  templates/  # Directory where the map HTML will be saved
    │  └──  map.html
    ├──  README.md  # Project readme
    └──  requirements.txt  # Python dependencies

### 👤 Author
Rafael  Boschini <rafaelboschini@gmail.com>

### 📝 Notes
This  project  uses  a  development  server  via  Flask.  For  production  environments,  consider  using  a  WSGI  server  like  Gunicorn. 

### 🧑‍💻 Contributions
Feel  free  to  fork  the  project,  submit  issues,  or  open  pull  requests  to  improve  this  project!

### 📜 License
This  project  is  licensed  under  the  MIT  License. 
