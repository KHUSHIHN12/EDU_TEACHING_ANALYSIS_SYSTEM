import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

def clusters(score_data, k=5):
    print(" Step 1: Extracting data from Score_Table")
    df = pd.read_csv("data/score_data.csv")

    pivot_df = df.pivot(index='student_id', columns='course_id', values='course_score').fillna(0)

    num_students = pivot_df.shape[0]
    if k >= num_students:
        k = min(3, num_students)
        print(f" Too few students. Setting k = {k}")

    print(" Step 2: Preprocessing scores")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(pivot_df)

    print(" Step 3: Running KMeans clustering")
    kmeans = KMeans(
        n_clusters=k,
        init='random',
        n_init=10,
        max_iter=300,
        tol=1e-4,
        random_state=42
    )
    kmeans.fit(X_scaled)
    pivot_df['cluster'] = kmeans.labels_
    print("\n Cluster Summary:")
    avg_scores = {}
    for i in range(k):
        group = pivot_df[pivot_df['cluster'] == i]
        avg_score = np.mean(group.drop(columns='cluster').values)
        avg_scores[i] = avg_score
        print(f"Cluster {i+1}: Avg Score = {avg_score:.1f}, Students = {len(group)}")


    def get_label(avg_score):
        if avg_score >= 80:
            return "Excellent"
        elif avg_score >= 70:
            return "Good"
        elif avg_score >= 60:
            return "Average"
        elif avg_score >= 50:
            return "Below Average"
        else:
            return "Poor"

    cluster_labels = {cid: get_label(score) for cid, score in avg_scores.items()}
    pivot_df['cluster_label'] = pivot_df['cluster'].map(cluster_labels)
    pivot_df.reset_index(inplace=True)
    pivot_df.to_csv("data/Clustered_Students.csv", index=False)
    print(" Clustered student data saved to 'data/Clustered_Students.csv'")

    # t-SNE Visualization 
    if num_students >= 5:
        print(" Step 8: Visualizing clusters with t-SNE")
        tsne = TSNE(n_components=2, perplexity=min(5, num_students - 1), random_state=42)
        tsne_result = tsne.fit_transform(X_scaled)

        plt.figure(figsize=(8, 6))
        plt.scatter(tsne_result[:, 0], tsne_result[:, 1], c=kmeans.labels_, cmap='tab10', s=60)
        plt.title('Student Clustering Results')
        plt.xlabel('t-SNE Dim 1')
        plt.ylabel('t-SNE Dim 2')
        plt.colorbar(label='Cluster')
        plt.grid(True)
        plt.show()
    else:
        print("Not enough students for t-SNE plot (min 5 required). Skipping.")


if __name__ == "__main__":
    clusters("data/score_data.csv", k=5)

