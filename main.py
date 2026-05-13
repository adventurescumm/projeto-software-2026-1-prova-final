from flask import Flask, request, jsonify
from db import db
from models import Course
from validate import token_required
import os

def create_app():
    app = Flask(__name__)
    
    postgres_user = os.environ.get('POSTGRES_USER', 'appuser')
    postgres_password = os.environ.get('POSTGRES_PASSWORD', 'apppass')
    postgres_url = os.environ.get('POSTGRES_URL', 'localhost')
    
    # Define o padrão, mas permite que o Pytest sobrescreva depois
    db_uri = f"postgresql://{postgres_user}:{postgres_password}@{postgres_url}:5432/courses"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", db_uri)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)


    @app.route("/courses", methods=["POST"])
    @token_required("ADMIN")
    def create_course():
        data = request.json

        course = Course(
            name=data["name"],
            email=data["email"],
            name_instructor=data["name_instructor"],
        )

        db.session.add(course)
        db.session.commit()

        return jsonify({
            "id": str(course.id),
            "name": course.name,
            "email": course.email,
            "name_instructor": course.name_instructor,
            "code_course": course.code_course,
            "created_at": course.created_at,
            "status": course.status.value
        }), 201

    @app.route("/courses/<uuid:course_id>", methods=["DELETE"])
    @token_required("ADMIN")
    def delete_course(course_id):
        course = Course.query.get_or_404(course_id)

        db.session.delete(course)
        db.session.commit()

        return "", 204

    @app.route("/courses", methods=["GET"])
    @token_required(None)
    def list_courses():
        courses = Course.query.all()

        return [
            {
            "id": str(course.id),
            "name": course.name,
            "email": course.email,
            "name_instructor": course.name_instructor,
            "code_course": course.code_course,
            "created_at": course.created_at,
            "status": course.status
            }
            for course in courses
        ], 200

    return app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
