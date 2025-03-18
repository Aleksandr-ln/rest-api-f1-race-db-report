# REST API Report of Monaco 2018 Racing


## Description
This project provides a REST API to generate and serve a report on the qualification results of the Monaco 2018 Grand Prix in Formula 1.
The API supports JSON and XML response formats and stores the data in an SQLite database using Peewee ORM.

The project uses Flask, Flask-RESTful, Peewee, Flasgger (Swagger) for interactive API documentation, and pytest for unit testing.

## Getting started

Clone the Repository

```
cd existing_repo
git remote add origin https://git.foxminded.ua/foxstudent107874/task-9-convert-and-store-data-to-the-database.git
git branch -M main
git push -uf origin main
```

## Create & Activate Virtual Environment

```
python -m venv venv
source venv/bin/activate  # For macOS/Linux
source venv/Scripts/activate	# For Git Bash
venv\Scripts\activate   # For Windows
```

## Install Dependencies

```
pip install -r requirements.txt
```

## Database Initialization
```
export PYTHONPATH=$(pwd)/..
python -m database.setup_db
```

## Run the API

```
export PYTHONPATH=$(pwd)/..
python race_report_api.py
```

The API will be available at:
http://localhost:5000/api/v1/report/?event=Monaco%202018%20Grand%20Prix&session=Qualification

***

# API Usage

## Notes:
- `event` and `session` parameters must correspond to existing records in the database.
- Available `format`: `json` (default), `xml`.

# JSON Request:

```
curl -X GET "http://localhost:5000/api/v1/report/?event=Monaco%202018%20Grand%20Prix&session=Qualification&format=json"

```

# XML Request:

```
curl -X GET "http://localhost:5000/api/v1/report/?event=Monaco%202018%20Grand%20Prix&session=Qualification&format=xml"

```

## Database Structure

### Tables

#### Driver
| Field        | Type       | Description                              |
|--------------|------------|------------------------------------------|
| id           | AutoField  | Primary key                              |
| abbreviation | CharField  | Driver abbreviation (unique, 3 letters)  |
| full_name    | CharField  | Full name of driver                      |
| team         | CharField  | Team name                                |

#### RaceInfo
| Field       | Type            | Description                               |
|-------------|-----------------|-------------------------------------------|
| id          | AutoField       | Primary key                               |
| driver      | ForeignKeyField | Reference to Driver                       |
| event       | CharField       | Name of race event (e.g., Monaco 2018 GP) |
| session     | CharField       | Name of session (e.g., Qualification)     |
| date        | DateField       | Date of the event                         |
| start_time  | DateTimeField   | Start time of race/session (nullable)     |
| end_time    | DateTimeField   | End time of race/session (nullable)       |

- Composite Unique Index on `(driver, event, session)` to prevent duplicates.

## Expected Response (JSON):

```
{
    "race": "Monaco 2018 Grand Prix - Qualification",
    "date": "2018-05-24",
    "results": [
        {
            "position": 1,
            "driver": "Sebastian Vettel",
            "team": "FERRARI",
            "lap_time": "1:04.415"
        }
    ],
    "disqualified": [
        {
            "position": 16,
            "driver": "Lewis Hamilton",
            "team": "MERCEDES",
            "lap_time": "-7:12.460"
        }
    ]
}


```

## Swagger UI
This project includes an interactive API documentation using Swagger UI.

To access the documentation, run the API server and navigate to:

```
http://localhost:5000/apidocs/#/default/get_api_v1_report_

```

### How to Use Swagger UI
1. Open **Swagger UI** in your browser.
2. Select the `GET /api/v1/report/` endpoint.
3. Choose a response format (`json` or `xml`).
4. Click **Execute** to send the request.
5. View the response directly in the UI.

***

## Testing
This project includes unit tests to validate the API's functionality and report generation.

```
coverage run -m pytest tests/
coverage report -m
```

## Technologies Used
- **Flask** – Web framework for building the API
- **Flask-RESTful** – Extension for building RESTful APIs
- **Flasgger** – Automatic Swagger documentation generation
- **pytest** – Unit testing framework
- **dataclasses** – Structured data representation
- **xml.etree.ElementTree** – XML conversion
- **bs4 (BeautifulSoup)** – XML parsing in tests

## Authors
Oleksandr Onupko