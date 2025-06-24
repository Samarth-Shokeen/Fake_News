# train_model.py
import joblib
import data_processing
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def preprocess_data():
    train_news, test_news = data_processing.get_clean_data()
    train_data = train_news['Statement'].values
    train_labels = train_news['Label'].values
    test_data = test_news['Statement'].values
    test_labels = test_news['Label'].values
    return train_data, train_labels, test_data, test_labels

def create_pipeline():
    classifier = LogisticRegression(max_iter=1000)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1, 3), max_features=10000)),
        ('classifier', classifier)
    ])
    return pipeline

def train_and_save_model():
    train_data, train_labels, test_data, test_labels = preprocess_data()
    pipeline = create_pipeline()

    param_grid = {
        'classifier__C': [0.1, 1, 10],
        'classifier__solver': ['liblinear', 'saga']
    }

    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(train_data, train_labels)

    joblib.dump(grid_search.best_estimator_, 'trained_model.pkl')

    predictions = grid_search.predict(test_data)
    accuracy = accuracy_score(test_labels, predictions)
    print(f"Best Hyperparameters: {grid_search.best_params_}")
    print(f"Accuracy: {accuracy}")
    print(classification_report(test_labels, predictions))
    print(confusion_matrix(test_labels, predictions))

if __name__ == '__main__':
    train_and_save_model()
