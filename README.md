## Yacut

Yacut is a service for cutting long links.

### Overview

In essence, the service has one function, it allows users to shorten links.

For this reason, the Flask framework was used to implement the project.

### Technologies

- Python 3.9.5
- Flask 2.0.2

### Installation and launch

Clone the repository and go to it using the command line:

```
git clone 
```

```
cd yacut
```

Create and activate a virtual environment:

```
python3 -m venv venv
```

Linux/MacOS

```
source venv/bin/activate
```

Windows

```
source venv/scripts/activate
```

Install dependencies from a file requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Please note that the following environment variables must be created for the application to work correctly:

FLASK_APP=yacut
FLASK_ENV=development (or production depending on your needs)
DATABASE_URI=sqlite:///db.sqlite3 (or any other DB that your are going to use)
SECRET_KEY=DEFAULT 

### License

MIT

### Author

Alexander Kiselov, beginner Python developer