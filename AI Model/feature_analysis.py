# feature_analysis.py
import data_processing
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np

# Load and clean data
train_news, _ = data_processing.get_clean_data()  # Fix here
statements = train_news['Statement'].values

# Initialize vectorizers
countV = CountVectorizer(max_features=10000)
tfidfV = TfidfTransformer()

# Transform the data
train_count = countV.fit_transform(statements)
train_tfidf = tfidfV.fit_transform(train_count)

# Function to print vocabulary and TF-IDF stats
def analyze_features():
    print("Top 25 CountVectorizer Features:")
    print(countV.get_feature_names_out()[:25])
    print("\nTF-IDF Matrix Shape:", train_tfidf.shape)
    print("\nSample TF-IDF Rows:")
    print(train_tfidf.toarray()[:3])

if __name__ == '__main__':
    analyze_features()
