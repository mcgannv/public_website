# Set up
## Install Python 3.11
You can follow the installation guide here [link](https://www.python.org/downloads/)

## Install Poetry
You can install poetry for your machine by following Poetry's official documentation here [link](https://python-poetry.org/docs/)

Check if you have poetry correctly installed by running
```shell
poetry --version
```

## Create New Virtual Environment
Change to project directory

### Linux Users
```shell
poetry env use python3.11
```

### Windows Users
Follow Poetry's official documentation on how to create new environment in PowerShell here [link](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment)

### Activate Virtual Environment
After command finishes, there will be an output of the virtual environment path. Copy that and paste it in the command below.
For Linux users you can activate your virtual environment
```shell
source <paste path here>/bin/activate
```

## Install Package Dependencies
```shell
poetry install
```

## Start Flask App
```shell
flask --app webapp run
```

## View Pizza Page
In your browser, go to http://127.0.0.1:5000/pizza

# Different Virtual Environment
If you have Pip installed, create a new virtual environment that you know how, and you can pip install all the packages inside pyproject.toml.