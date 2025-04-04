import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import re
# Load your dataset
dataset = pd.read_csv('labeled_data.csv')

# Split into features and labels
X = dataset['tweet']  # Replace 'text' with your column name
y = dataset['class']  # Replace 'label' with your column name

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text to numbers
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

# Train the model
model = MultinomialNB()
model.fit(X_train_counts, y_train)

# Test accuracy
accuracy = model.score(X_test_counts, y_test)
print("Model Accuracy:", accuracy)

# Save the model and vectorizer
joblib.dump(model, 'abuse_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
print("Model and vectorizer saved!")

