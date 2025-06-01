import pandas as pd

# Load the full dataset
df = pd.read_csv("data/student_course_dataset.csv")

# 1. Student Data
student_data = df[['student_id', 'student_name', 'section', 'classroom']].drop_duplicates()
student_data.to_csv("data/student_data.csv", index=False)

# 2. Course Data
course_data = df[['course_id', 'course_name']].drop_duplicates()
course_data.to_csv("data/course_data.csv", index=False)

# 3. Score Data
score_data = df[['student_id', 'course_id', 'student_attendance', 'course_score']]
score_data.to_csv("data/score_data.csv", index=False)
