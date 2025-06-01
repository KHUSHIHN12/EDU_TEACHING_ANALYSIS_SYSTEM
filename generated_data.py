import random
import pandas as pd
from faker import Faker

fake = Faker()

# Define updated courses
courses_updated = [
    {"course_id": "CS101", "course_name": "Linear Algebra"},
    {"course_id": "CS102", "course_name": "Advanced Mathematics"},
    {"course_id": "CS103", "course_name": "Data Structures"},
    {"course_id": "CS104", "course_name": "Discrete Mathematics"},
    {"course_id": "CS105", "course_name": "C Language"},
    {"course_id": "CS106", "course_name": "Python Programming"},
]

# Sections and classrooms
sections = ['A', 'B', 'C']
classrooms = {'A': "Room 101", 'B': "Room 102", 'C': "Room 103"}
students_per_section = 100 // 3
extra = 100 % 3
section_distribution = {'A': students_per_section + (1 if extra > 0 else 0),
                        'B': students_per_section + (1 if extra > 1 else 0),
                        'C': students_per_section}

# Generate students
section_students = []
student_id_counter = 1000
for section, count in section_distribution.items():
    for _ in range(count):
        student = {
            "student_id": f"S{student_id_counter}",
            "student_name": fake.name(),
            "section": section,
            "classroom": classrooms[section]
        }
        section_students.append(student)
        student_id_counter += 1

# Generate dataset
data_complete = []
for student in section_students:
    for course in courses_updated:
        attendance = round(random.normalvariate(85, 10), 2)
        attendance = min(max(attendance, 50), 100)
        score = round(random.normalvariate(70, 15), 2)
        score = min(max(score, 30), 100)
        data_complete.append({
            "student_id": student["student_id"],
            "student_name": student["student_name"],
            "course_id": course["course_id"],
            "course_name": course["course_name"],
            "student_attendance": attendance,
            "course_score": score,
            "section": student["section"],
            "classroom": student["classroom"]
        })

df_final = pd.DataFrame(data_complete)
df_final.to_csv("data/student_course_dataset.csv", index=False)
