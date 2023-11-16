Setup and running the app:

1. `pip install poetry` (or safer, follow the instructions: https://python-poetry.org/docs/#installation)
2. Install dependencies `cd` into the directory where the `pyproject.toml` is located then `poetry install`
3. [UNIX]: Run the FastAPI server via poetry with the bash script: `poetry run ./run.sh`
4. [WINDOWS]: Run the FastAPI server via poetry with the Python command: `poetry run python app/main.py`
5. Open http://localhost:8001/

To stop the server, press CTRL+C

Additionally:
Download rdflib-endpoint: https://pypi.org/project/rdflib-endpoint/

Development In free time:
Implement auto reload, not to be forced to rerun server after every change
https://stackoverflow.com/questions/63809553/how-to-run-fastapi-application-from-poetry


Tymo update testing

update luca

