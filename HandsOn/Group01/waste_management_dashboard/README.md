
# District Data Viewer Web App

This guide provides instructions on how to set up the environment, install dependencies, and run the server and frontend for the District Data Viewer Web App, which now has a separate structure for the server and the query execution logic.

## Environment Setup

### Creating a Conda Environment

To create a new conda environment with Python 3.9, run:

```
conda create -n myenv python=3.9
```

### Activating the Conda Environment

Activate the newly created environment with:

```
conda activate myenv
```

## Dependency Installation

### Installing Packages from `requirements.txt`

First, try to install the required packages using Conda:

```
conda install --file requirements.txt
```

If some packages are not available in the Conda repositories, you can use pip (make sure your environment is activated):

```
pip install -r requirements.txt
```

## Running the Server

With your environment set up and dependencies installed, you can start the server by running the `flask_server.py` in the backend folder:

```
python flask_server.py
```

Ensure the server is running on `http://127.0.0.1:5000/`.

The `flask_server.py` file is responsible for setting up the Flask server and defining the routes. It imports the query execution function from `query_handler.py` which contains the logic to perform the SPARQL queries.

## Running the Frontend

Open the `district_data_viewer.html` file in a web browser to interact with the application.

1. Click on the 'Get District Data' button to make a request to the server.
2. View the response displayed on the page, which shows the district data retrieved from the Flask server.

## Troubleshooting

- If you encounter CORS issues, ensure that `flask-cors` is installed and properly configured in your Flask application.
- Use your browser's developer tools (F12 or right-click > Inspect) to check for any errors in the console, especially if the AJAX request fails.

For any additional help, refer to the Flask and Conda documentation or check online communities for support.
