from flask import Flask, jsonify, request
from pathlib import Path
import json

app = Flask(__name__)

DATA_FILE = Path("data/courses.json")

VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed"
}


def ensure_data_file():
    """Create the data directory and JSON file if needed."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_courses():
    """Read courses from the JSON file."""
    ensure_data_file()

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_courses(courses):
    """Write courses to the JSON file."""
    ensure_data_file()

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(courses, file, indent=2)


def validate_course_data(data, require_all_fields=True):
    """Validate course input and return an error message if invalid."""
    required_fields = [
        "name",
        "description",
        "target_completion_date",
        "status"
    ]

    if require_all_fields:
        missing_fields = [
            field for field in required_fields
            if field not in data
        ]

        if missing_fields:
            return f"Missing fields: {', '.join(missing_fields)}"

    if "name" in data and not isinstance(data["name"], str):
        return "name must be a string"

    if "description" in data and not isinstance(data["description"], str):
        return "description must be a string"

    if "target_completion_date" in data:
        if not isinstance(data["target_completion_date"], str):
            return "target_completion_date must be a string"

    if "status" in data and data["status"] not in VALID_STATUSES:
        return (
            "status must be one of: "
            + ", ".join(sorted(VALID_STATUSES))
        )

    return None


@app.get("/api/courses")
def get_courses():
    courses = load_courses()
    return jsonify(courses), 200


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    courses = load_courses()

    course = next(
        (course for course in courses if course["id"] == course_id),
        None
    )

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    return jsonify(course), 200


@app.post("/api/courses")
def create_course():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    error = validate_course_data(data)

    if error:
        return jsonify({"error": error}), 400

    courses = load_courses()

    if courses:
        new_id = max(course["id"] for course in courses) + 1
    else:
        new_id = 1

    new_course = {
        "id": new_id,
        "name": data["name"],
        "description": data["description"],
        "target_completion_date": data["target_completion_date"],
        "status": data["status"]
    }

    courses.append(new_course)
    save_courses(courses)

    return jsonify(new_course), 201


@app.put("/api/courses/<int:course_id>")
def replace_course(course_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    error = validate_course_data(data)

    if error:
        return jsonify({"error": error}), 400

    courses = load_courses()

    for index, course in enumerate(courses):
        if course["id"] == course_id:
            replacement = {
                "id": course_id,
                "name": data["name"],
                "description": data["description"],
                "target_completion_date": data["target_completion_date"],
                "status": data["status"]
            }

            courses[index] = replacement
            save_courses(courses)

            return jsonify(replacement), 200

    return jsonify({"error": "Course not found"}), 404


@app.patch("/api/courses/<int:course_id>")
def update_course(course_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON"}), 400

    error = validate_course_data(data, require_all_fields=False)

    if error:
        return jsonify({"error": error}), 400

    courses = load_courses()

    for course in courses:
        if course["id"] == course_id:
            allowed_fields = {
                "name",
                "description",
                "target_completion_date",
                "status"
            }

            for field in allowed_fields:
                if field in data:
                    course[field] = data[field]

            save_courses(courses)
            return jsonify(course), 200

    return jsonify({"error": "Course not found"}), 404


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    courses = load_courses()

    filtered_courses = [
        course for course in courses
        if course["id"] != course_id
    ]

    if len(filtered_courses) == len(courses):
        return jsonify({"error": "Course not found"}), 404

    save_courses(filtered_courses)

    return jsonify({
        "message": "Course deleted successfully"
    }), 200

@app.get("/api/courses/stats")
def get_course_stats():
    courses = load_courses()

    stats = {
        "total_courses": len(courses),
        "Not Started": 0,
        "In Progress": 0,
        "Completed": 0
    }

    for course in courses:
        status = course.get("status")
        if status in VALID_STATUSES:
            stats[status] += 1

    return jsonify(stats), 200

if __name__ == "__main__":
    app.run(debug=True)