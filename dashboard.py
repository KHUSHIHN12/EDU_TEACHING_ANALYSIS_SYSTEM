import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import os
import sys



df = pd.read_csv("data/student_course_dataset.csv")



# 1. Count of students by Class (class_name)
class_counts = df[['student_id', 'classroom', 'section']].drop_duplicates()
class_counts['class'] = class_counts['classroom'] + " - " + class_counts['section']
counts = class_counts['class'].value_counts().reset_index()
counts.columns = ['Class Name', 'Number of Students']

counts = counts.sort_values(by='Number of Students', ascending=False)

# Plot
plt.figure(figsize=(10, 6))
barplot = sns.barplot(data=counts, x='Class Name', y='Number of Students', palette='Set1')

# Add count labels on top of bars
for i in range(len(counts)):
    barplot.text(i, counts['Number of Students'].iloc[i] + 0.5,
                 str(counts['Number of Students'].iloc[i]),
                 ha='center', va='bottom', fontsize=10, color='black')

plt.title("Count of Students by Class")
plt.xlabel("Class Name")
plt.ylabel("Number of Students")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visual/student_by_class.png")
#plt.show()
plt.close()

#--------------************-----------------
sns.set(style="whitegrid")
 #4. Attendance by Year of Study (Boxplot)
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='classroom', y='student_attendance', palette="muted")
plt.title("Attendance Distribution by Classroom")
plt.xlabel("Classroom")
plt.ylabel("Attendance (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visual/attendance_by_classroom_boxplot.png")
plt.close()

#-------------------****************-------------------
df = pd.read_csv("data/Clustered_Students.csv", index_col=0)


course_df = pd.read_csv("data/student_course_dataset.csv")
course_map = dict(zip(course_df['course_id'].astype(str), course_df['course_name']))


course_columns = [col for col in df.columns if col in course_map]
df.rename(columns={col: course_map[col] for col in course_columns}, inplace=True)


subject_names = list(course_map.values())


existing_subjects = [subj for subj in subject_names if subj in df.columns]


cluster_performance = df.groupby('cluster')[existing_subjects].mean()


plt.figure(figsize=(12, 6))
sns.heatmap(cluster_performance, annot=True, cmap='YlGnBu', fmt=".1f", cbar_kws={'label': 'Average Score'})
plt.title("Average Student Performance per Subject in Each Cluster")
plt.xlabel("Subjects")
plt.ylabel("Cluster")
plt.tight_layout()
plt.savefig("visual/boxplocluster_heatmap.png")
#plt.show()
plt.close()

#--------------------********************-------------------------
df_rules = pd.read_csv('data/FP_Image_Association_Confidence.csv')


unique_conf = df_rules['Confidence'].unique()


sampled_conf = unique_conf
if len(unique_conf) > 15:
    sampled_conf = random.sample(list(unique_conf), 15)


sampled_rules = pd.DataFrame()
for conf in sampled_conf:
    
    subset = df_rules[df_rules['Confidence'] == conf]
    
    rule = subset.sample(n=1, random_state=42)  
    sampled_rules = pd.concat([sampled_rules, rule])


def abbreviate(items, max_len=20):
    if len(items) > max_len:
        return items[:max_len] + '...'
    return items

labels = sampled_rules.apply(lambda row: f"{{{abbreviate(row['Antecedent'])}}} => {{{abbreviate(row['Consequent'])}}}", axis=1)
confidences = sampled_rules['Confidence']


plt.figure(figsize=(12, 8))
bars = plt.barh(labels, confidences, color='skyblue')
plt.xlabel('Confidence')
plt.title('Sample of 15 Association Rules with Distinct Confidence Values')
plt.xlim(0, 1)
plt.gca().invert_yaxis()

for bar, conf in zip(bars, confidences):
    plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
             f"{conf:.2f}", va='center')

plt.tight_layout()
plt.savefig("visual/association_rules.png")
#plt.show()
plt.close()

