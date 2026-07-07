import random
import re
import string

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
            "Goodbye! Best of luck.",
            "See you again!",
            "Take care!"
        ]
    },

    {
        "tag": "admission",
        "patterns": ["admission", "apply", "enroll"],
        "responses": [
            "Admissions open every June. Apply through our official website."
        ]
    },

    {
        "tag": "fees",
        "patterns": ["fees", "fee", "cost", "tuition"],
        "responses": [
            "Engineering Fee: Rs 80,000 per year."
        ]
    },

    {
        "tag": "courses",
        "patterns": ["courses", "programs", "degrees"],
        "responses": [
            "We offer B.Tech, BCA, BBA, MBA, MCA and many more."
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
        "tag": "placements",
        "patterns": ["placement", "jobs", "salary"],
        "responses": [
            "Top recruiters include Infosys, TCS, Wipro and Amazon."
        ]
    },

    {
        "tag": "unknown",
        "patterns": [],
        "responses": [
            "Sorry, I didn't understand. Please ask about admissions, fees, hostel or courses."
        ]
    }
]

def preprocess(text):                              #prepocessor()
    """
    Clean the user input.
    - Convert to lowercase
    - Remove punctuation
    - Remove extra spaces
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    text = " ".join(text.split())
    return text


def find_best_match(user_input):                           #find_best_match()
    """
    Compare user input with all patterns in the knowledge base.
    Returns the best matching tag and a response.
    """
    cleaned = preprocess(user_input)
    user_words = set(cleaned.split())

    best_tag = "unknown"
    best_score = 0

    for entry in KNOWLEDGE_BASE:
        if entry["tag"] == "unknown":
            continue

        for pattern in entry["patterns"]:
            pattern_words = set(preprocess(pattern).split())

            overlap = len(user_words & pattern_words)

            if overlap > best_score:
                best_score = overlap
                best_tag = entry["tag"]

    # Return a response for the matched tag
    for entry in KNOWLEDGE_BASE:
        if entry["tag"] == best_tag:
            return best_tag, random.choice(entry["responses"])

    # Fallback
    for entry in KNOWLEDGE_BASE:
        if entry["tag"] == "unknown":
            return "unknown", random.choice(entry["responses"])

REGEX_PATTERNS = [                               #regex patterns
    (r'\b(hi|hello|hey|good morning)\b', 'greeting'),
    (r'\b(bye|goodbye|exit)\b', 'farewell'),
    (r'\b(fee|fees|cost|tuition)\b', 'fees'),
    (r'\b(admission|apply|enroll)\b', 'admission'),
    (r'\b(course|courses|degree)\b', 'courses'),
    (r'\b(hostel|accommodation)\b', 'hostel'),
    (r'\b(placement|job|salary)\b', 'placements')
]

def regex_match(user_input):
    cleaned = preprocess(user_input)

    for pattern, tag in REGEX_PATTERNS:
        if re.search(pattern, cleaned):
            for entry in KNOWLEDGE_BASE:
                if entry["tag"] == tag:
                    return tag, random.choice(entry["responses"])

    return find_best_match(user_input)


def chat():                 #chat()
    print("=" * 50)
    print("      CollegeBot - AI College Assistant")
    print("=" * 50)
    print("Type 'bye' to exit.\n")

    while True:
        user_input = input("You: ")

        if not user_input.strip():
            print("Bot: Please type something.\n")
            continue

        tag, response = regex_match(user_input)

        print("Bot:", response)
        print()

        if tag == "farewell":
            print("Session Ended.")
            break


if __name__ == "__main__":
    chat()
