# CodeCraftHub – Learning Management System

## Project Description
CodeCraftHub is a Flask-based REST API for managing learning courses. It supports creating, viewing, updating, and deleting courses. Course information is stored in a JSON file.

## Technologies Used
- Python 3
- Flask
- REST API
- JSON for data storage

## Installation
Install the required dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Run the Application
Start the Flask development server:

```bash
python3 app.py
```

The API runs locally on port 5000.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/courses` | Retrieve all courses |
| POST | `/api/courses` | Create a course |
| GET | `/api/courses/<course_id>` | Retrieve a course |
| PUT | `/api/courses/<course_id>` | Replace a course |
| PATCH | `/api/courses/<course_id>` | Partially update a course |
| DELETE | `/api/courses/<course_id>` | Delete a course |
| GET | `/api/courses/stats` | Retrieve course statistics |

## Course Fields
- `name`
- `description`
- `target_completion_date`
- `status`: Not Started, In Progress, or Completed

## Data Storage
Course data is stored in `data/courses.json`, which the application creates automatically.

## Testing
The API was tested using `curl` commands for creating, retrieving, updating, deleting courses, and retrieving statistics.