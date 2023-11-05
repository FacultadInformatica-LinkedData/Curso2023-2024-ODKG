# Madrid Waste Management App Documentation


## Overview
This project, named Madrid Waste App, is aimed at visualizing waste management and many more data about each district in Madrid . 
The application is built using the Flask framework, and utilizes libraries such as Leaflet.js for mapping, Chart.js for charting, and Bootstrap for styling.

## Directory Structure
The directory structure is organized as follows:

[Name of the App]/
- MadridWaste/
    - static/
        - css/: Contains CSS files for styling the application.
        - data/: Contains GeoJSON files for each district. 
        - js/: Contains JavaScript files for client-side logic.
  - templates/: Contains HTML templates.
  - venv/: Contains your virtual environment.
  - app.py: The main Flask application file.
  requirements.txt: Lists the Python dependencies.

### Libraries
  
The following libraries are linked in the base.html file and need to be downloaded:

- link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
- link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet/v1.7.1/leaflet.css" /
- script src="http://cdn.leafletjs.com/leaflet/v1.7.1/leaflet.js"></script
- script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script
- script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script

### Core Components

- Base Template (base.html):

The base.html file is the base template from which other templates inherit. It includes links to external stylesheets and scripts for Bootstrap, Leaflet.js, and Chart.js. It also provides basic structure for the application, such as a sidebar and main content area, and defines blocks (title, body, scripts) that can be overridden in child templates.

- html files in templates folder (district.html):

Each html file except the index extends base.html and provides the structure for displaying district details.
This is done in order to avoid repeating CSS (DRY design pattern principle) for pages with the same structure .
For instance district.html overrides the title, body, and scripts blocks to provide a title, a table for displaying waste data, and a chart for visualizing waste data, respectively. It utilizes Bootstrap for layout and styling, and Chart.js for rendering the chart.

- Main Flask Application (app.py):

The app.py file is the main Flask application file. It defines routes for handling requests to different URLs, and functions for processing these requests and rendering templates.
If there are too many routes functions because of too many pages, these functions will be placed in a rooter or contorler folder
in an urls.py file.

#### Routes:


- /: Renders the index.html template.
- /district: Renders the district.html template, passing waste data for the specified district to the template.

### Functions:

Functions in app.py retrieve data (e.g., from a SPARQL endpoint), process data, and pass data to templates for rendering.

### Map Script (map1.js)

The map1.js file contains the script for rendering a map using Leaflet.js, loading GeoJSON files representing districts, and handling user interactions with the map. It defines functions for adding districts to the map, styling districts, and handling mouse events.


### Execution Flow
When a user accesses the app, they are served the index.html template, which provides a map of Madrid.
The user can interact with the map to select a district, which triggers a redirect to the /district route.
The app.py file processes the request, retrieves and processes waste data for the specified district, and renders the district.html template, passing the waste data to the template.
The district.html template displays the waste data in a table and a chart, utilizing Bootstrap for layout and styling, and Chart.js for rendering the chart.

### Extending the App

You can extend the app by defining new routes and functions in app.py. For each route, there is always one associated template from the templates directory that you will have to create. Style and script must preferably be separated from the HTML and put in the js or css folder inside static. There is some CSS and js directly in the HTML, which is bad practice, but will be corrected later. When creating a new route to a template, you must specify if you do a POST or a GET request. Usually, POST request is only to pass data after asuccessfull  filled  form.


## Setting Up the Development Environment

It's essential to have a virtual environment to manage dependencies and ensure that the application runs consistently across different setups. Below are the steps to set up a virtual environment and install the necessary dependencies from the `requirements.txt` file on Mac, Windows, and Linux.

### Creating a Virtual Environment

#### On Mac and Linux:
1. Open a terminal.
2. Navigate to the project directory `MerilApp/MadridWaste`.
3. Run the following command to create a virtual environment named `venv`:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
   or Windows
    
   ```
    venv\Scripts\activate
   ```
4. pip install -r requirements.txt

    