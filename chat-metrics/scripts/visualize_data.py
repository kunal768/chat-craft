import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load the CSV data
data = pd.read_csv('../data/chat_data.csv')

# Convert timestamp to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Plot sentiment distribution
plt.figure(figsize=(10, 6))
sns.countplot(x='sentiment', data=data, hue='sentiment', palette='viridis', dodge=False, legend=False)
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.savefig('../visualizations/sentiment_distribution.png')
plt.show(block=False)

# Plot volume of questions over time
time_series = data['timestamp'].dt.date.value_counts().sort_index()

plt.figure(figsize=(10, 6))
plt.plot(time_series.index, time_series.values, marker='o')
plt.title('Volume of Questions Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Questions')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../visualizations/volume_of_questions.png')
plt.show(block=False)

# Identify key topics (example keywords)
keywords = ['order', 'return', 'shipping', 'payment', 'support']
keyword_counts = Counter()

for message in data['message']:
    for keyword in keywords:
        if keyword in message.lower():
            keyword_counts[keyword] += 1

# Plot key topics frequency
plt.figure(figsize=(10, 6))
sns.barplot(x=list(keyword_counts.keys()), y=list(keyword_counts.values()), hue=list(keyword_counts.keys()), dodge=False, palette='magma', legend=False)
plt.title('Key Topics Frequency')
plt.xlabel('Topics')
plt.ylabel('Frequency')
plt.savefig('../visualizations/key_topics_frequency.png')
plt.show(block=False)

# Keep plots open
plt.show()