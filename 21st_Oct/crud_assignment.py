from flask import Flask, jsonify, request

app = Flask(__name__)

students = [
{
"id": 1,
"name": "Rhea Kapoor",
"course": "Python",
"score": 82
},
{
"id": 2,
"name": "Zain Malik",
"course": "SQL",
"score": 76
},
{
"id": 3,
"name": "Devika Rao",
"course": "Cloud",
"score": 91
}
]

@app.get("/students")
def get_students():
    return jsonify(students)

@app.get("/students/<int:id>")
def get_student(id):
    for student in students:
        if student["id"] == id:
            return jsonify(students[id])
    return jsonify({"message": "Student not found"}),404

@app.post("/students")
def create_student():
    new_student = request.get_json()
    students.append(new_student)
    return jsonify({
        "message": "Student created",
    })

@app.put("/students/<int:id>")
def update_student(id):
    data = request.get_json()
    for student in students:
        if student["id"] == id:
            student["name"] = data["name"]
            student["course"] = data["course"]
            student["score"] = data["score"]

            return jsonify({
                "message": "Student updated",
            }), 200

    return jsonify({
        "message": "Student not found",
    }),404


@app.delete("/students/<int:id>")
def delete_student(id):
    for student in students:
        if student["id"] == id:
            students.remove(student)
            return jsonify({
                "message": "Student deleted",
            })
    return jsonify({
        "message": "Student not found",
    }),404

if __name__ == "__main__":
    app.run(debug=True)
