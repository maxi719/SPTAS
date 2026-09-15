from app import create_app
from app.extensions import db
from app.models import Lecturer

DEFAULT_LECTURERS = [
    ("lec001", "Dr. John Smith", "Computer Science", "john.smith@university.edu"),
    ("lec002", "Prof. Sarah Johnson", "Computer Science", "sarah.johnson@university.edu"),
    ("lec003", "Dr. Michael Brown", "Information Technology", "michael.brown@university.edu"),
    ("lec004", "Prof. Emily Davis", "Software Engineering", "emily.davis@university.edu"),
    ("lec005", "Dr. Robert Wilson", "Data Science", "robert.wilson@university.edu"),
]

app = create_app()
with app.app_context():
    db.create_all()
    password = app.config["DEMO_LECTURER_PASSWORD"]
    for lecturer_id, name, department, email in DEFAULT_LECTURERS:
        lecturer = db.session.get(Lecturer, lecturer_id)
        if lecturer is None:
            lecturer = Lecturer(id=lecturer_id, name=name, department=department, email=email)
            lecturer.set_password(password)
            db.session.add(lecturer)
        elif not lecturer.password_hash:
            lecturer.set_password(password)
    db.session.commit()
    print(f"Seed complete. Demo lecturer password comes from DEMO_LECTURER_PASSWORD={password!r}")
