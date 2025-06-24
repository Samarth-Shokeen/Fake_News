#data_processing.py
import os
import pandas as pd
import nltk
import seaborn as sb
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

nltk.download('stopwords')
nltk.download('wordnet')
stopwords = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# File paths
current_dir = os.path.dirname(os.path.abspath(__file__))
data_files = ['train.csv', 'test.csv', 'valid.csv', 'true.csv', 'fake.csv', 'train1.csv']

def load_data(filename):
    return pd.read_csv(os.path.join(current_dir, filename))

def preprocess_text(text):
    tokens = [word.lower() for word in text.split() if word.isalpha()]
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stopwords]
    return " ".join(lemmatized_tokens)

def create_distribution(data, label_column='Label'):
    plt.figure(figsize=(6, 4))
    sb.countplot(x=label_column, hue=label_column, data=data, palette='hls')
    plt.title(f"{label_column} Distribution")
    plt.show()

def main():
    datasets = {file: load_data(file) for file in data_files}
    for name, data in datasets.items():
        print(f"{name} dataset size: {data.shape}")
        print(data.head(5))
        if 'Label' in data.columns:
            create_distribution(data)

if __name__ == '__main__':
    main()

def get_clean_data():
    train_df = load_data('train.csv')
    test_df = load_data('test.csv')

    # Clean statements
    train_df['Statement'] = train_df['Statement'].astype(str).apply(preprocess_text)
    test_df['Statement'] = test_df['Statement'].astype(str).apply(preprocess_text)

    return train_df, test_df

def load_cleaned_data():
    train_df = load_data('train.csv')
    test_df = load_data('test.csv')
    
    train_df['Statement'] = train_df['Statement'].astype(str).apply(preprocess_text)
    test_df['Statement'] = test_df['Statement'].astype(str).apply(preprocess_text)

    return train_df, test_df
