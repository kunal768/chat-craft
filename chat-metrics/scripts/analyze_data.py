import pandas as pd

# Load the CSV data
data = pd.read_csv('../data/chat_data.csv')

# Calculate average response time
average_response_time = data['response_time'].mean()
print(f"Average Response Time: {average_response_time:.2f} seconds")

# Sentiment distribution
sentiment_counts = data['sentiment'].value_counts()
print("\nSentiment Distribution:")
print(sentiment_counts)