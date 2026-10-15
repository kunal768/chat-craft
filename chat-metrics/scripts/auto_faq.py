import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter

# Load the CSV data
data = pd.read_csv('../data/chat_data.csv')

# Vectorize the messages
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['message'])

# Apply K-Means clustering
kmeans = KMeans(n_clusters=5, random_state=0)
kmeans.fit(X)

# Assign each message to a cluster
data['cluster'] = kmeans.labels_

# Function to find representative question
def find_representative_question(cluster_data):
    question_counts = Counter(cluster_data)
    return question_counts.most_common(1)[0][0]

# Select representative questions
representative_questions = {}
for i in range(5):
    cluster_data = data[data['cluster'] == i]['message']
    representative_questions[i] = find_representative_question(cluster_data)

# Display representative questions
for cluster, question in representative_questions.items():
    print(f"Cluster {cluster}: {question}")