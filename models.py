import uuid
import enum
from datetime import datetime
from db import db
from sqlalchemy import Identity

class CourseStatus(enum.Enum):
    DISPONIVEL = "DISPONIVEL"
    CANCELADO = "CANCELADO"

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    name_instructor = db.Column(db.String(100), nullable=False)
    code_course = db.Column(db.Integer, Identity(start=1), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.Enum(CourseStatus, name="course_status"), nullable=False, default=CourseStatus.DISPONIVEL)