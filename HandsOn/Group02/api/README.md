# Open Data and Knowledge graphs API

This is the final submission of the project from group 2. We have developed an API that implements all the logic to show the Madrid map and to interact with it. The main purpose of the project is to see al the restaurants of the different districts of Madrid.

## Structure of the API

The API has the following structure:

```
📦Interfaz_ODKG
 ┣ 📂api
 ┃ ┣ 📂files
 ┃ ┃ ┣ 📜mapaScript.js
 ┃ ┃ ┗ 📜style.css
 ┃ ┣ 📂images
 ┃ ┃ ┣ 📜logo.jpg
 ┃ ┃ ┗ 📜wallpaper.jpg
 ┃ ┣ 📂route
 ┃ ┃ ┣ 📜core.py
 ┃ ┃ ┗ 📜home.py
 ┃ ┣ 📂schema
 ┃ ┃ ┣ 📜distrito_schema.py
 ┃ ┃ ┣ 📜local_schema.py
 ┃ ┃ ┗ 📜locales_schema.py
 ┃ ┗ 📂templates
 ┃   ┗ 📜mapa.html
 ┣ 📜main.py
 ┣ 📜README.md
 ┗ 📜requirements.txt
```

The `api` folder contains all the information about the API in different subfolders:
* `files` subfolder contains the logic of the web page.
* `images` subfolder contains image files of the background and the logo of the web.
* `route` subfolder contains different blueprints that define the methods and path for the API. It also implements all the logic for the queries.
* `schema` subfolder contains the schemas defined of the endpoint returns .It's based on `flask-marshmallow` which allows to define the schema of the output of the API methods.
* `templates` subfolder contains the html file (the web itself).

## How to install the necessary packages

To install the project, first create a new fresh environment using your preferred way (pyenv, Anaconda, ...).

After that, install the `requirements.txt` file which contains all the basic packages to run the API.

```sh
pip install -r requirements.txt
```

## How to start the API

To start the service you only need to start the `main.py` file in the following way.

```sh
python main.py
```

## Usage of the API
This API is connected to the port 5000. To see the documentation of the API you must access this URL: http://127.0.0.1:5000/apidocs.
To see the map you must access this URL: http://127.0.0.1:5000.

## Warnings
To use the API correctly, first of all you must configure the rdf link in the endpoint of helios and then just deploy the helios' API.
For Helios, you must use Java 21.0.1 due to codification problems.
