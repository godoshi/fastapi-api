# Requirements

python 3.9.10

## Pre-Reading
[pyenv](https://github.com/pyenv/pyenv)
[python virtual environments](https://docs.python.org/3/library/venv.html)
[python modules](https://docs.python.org/3/tutorial/modules.html)
[python csv](https://docs.python.org/3/library/csv.html)
[geojson]()
[fastapi](https://fastapi.tiangolo.com/)
[uvicorn](https://www.uvicorn.org/)
[python-multipart](https://andrew-d.github.io/python-multipart/])

## Project setup
```
# create virtual environment
python -m venv venv

# activate virtual environment
source venv/bin/activate

# install requirements
pip install -r api/requirements.txt
```

### Run FastAPI server with hot-reloads
```
cd api
uvicorn main:app --reload
```

## TODO
- Organize code
- Authentication
- Unit Testing
- Contanierization
- CI/CD
- Postman Collection