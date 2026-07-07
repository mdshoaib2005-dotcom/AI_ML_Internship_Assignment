import random
import pickle
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

# Download NLTK data
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

# ------------------------------
# Knowledge Base
# ------------------------------

KNOWLEDGE_BASE = [
    {
        "tag": "greeting",
        "patterns": ["hello", "hi", "hey", "good morning"],
        "responses": [
            "Hello! Welcome to CollegeBot.",
            "Hi there! How can I help you?",
            "Hey! Ask me anything about the college."
        ]
    },
    {
        "tag": "farewell",
        "patterns": ["bye", "goodbye", "exit"],
        "responses": [
            "Goodbye!",
            "Take care!",
            "See you again!"
        ]
    },
    {
        "tag": "admission",
        "patterns": ["admission", "apply", "enroll"],
        "responses": [
            "Admissions are open every June."
        ]
    },
    {
        "tag": "fees",
        "patterns": ["fees", "fee", "tuition", "cost"],
        "responses": [
            "Engineering fee is Rs. 80,000 per year."
        ]
    },
    {
        "tag": "hostel",
        "patterns": ["hostel", "accommodation"],
        "responses": [
            "Separate hostels are available for boys and girls."
        ]
    },
    {
        "tag": "courses",
        "patterns": ["courses", "programs", "degrees"],
        "responses": [
            "We offer B.Tech, BCA, MCA, MBA and more."
        ]
    }
]

# ------------------------------
# Prepare Training Data
# ------------------------------

training_sentences = []
training_labels = []

for intent in KNOWLEDGE_BASE:
    for pattern in intent["patterns"]:
        training_sentences.append(pattern)
        training_labels.append(intent["tag"])

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_sentences)

# Label Encoder
encoder = LabelEncoder()
y = encoder.fit_transform(training_labels)

# Train Model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

print("✅ Model trained successfully!")

# ------------------------------
# Save Model
# ------------------------------

with open("chatbot_model.pkl", "wb") as file:
    pickle.dump(model, file)

with open("tfidf_vectorizer.pkl", "wb") as file:
    pickle.dump(vectorizer, file)

with open("label_encoder.pkl", "wb") as file:
    pickle.dump(encoder, file)

print("✅ Model saved successfully!")

# ------------------------------
# Prediction Function
# ------------------------------

def predict_intent(user_input):
    user_vector = vectorizer.transform([user_input])
    prediction = model.predict(user_vector)
    tag = encoder.inverse_transform(prediction)[0]
    return tag

# ------------------------------
# Response Function
# ------------------------------

def get_response(tag):
    for intent in KNOWLEDGE_BASE:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "Sorry, I don't understand."

# ------------------------------
# Chat Function
# ------------------------------

def chat():
    print("=" * 50)
    print("          NLP CollegeBot")
    print("=" * 50)
    print("Type 'bye' to exit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "bye":
            print("Bot: Goodbye!")
            break

        tag = predict_intent(user_input)
        response = get_response(tag)

        print("Bot:", response)
        print()

# ------------------------------
# Main
# ------------------------------

if __name__ == "__main__":
    chat()

from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Display the confusion matrix
ConfusionMatrixDisplay.from_estimator(model, X, y)

plt.title("Chatbot Intent Classification")
plt.savefig("chatbot_confusion_matrix.png")
plt.show()
