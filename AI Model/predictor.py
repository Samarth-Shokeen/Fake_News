import joblib

def classify_headline(headline):
    model = joblib.load('trained_model.pkl')
    prediction = model.predict([headline])[0]
    return "Fake" if prediction == 1 else "Real"

if __name__ == "__main__":
    user_input = input("Enter a news headline to classify as Real or Fake: ")
    result = classify_headline(user_input)
    print(f"The headline is classified as: {result}")
