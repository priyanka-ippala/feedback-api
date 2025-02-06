import re
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# List of common filler words
FILLER_WORDS = {"um","umm", "Ah", "uhh", "like", "you know", "basically", "actually", "so", "well"}

def count_filler_words(response):
    words = response.lower().split()
    filler_count = sum(1 for word in words if word in FILLER_WORDS)
    return (filler_count / len(words)) * 100 if words else 0

def detect_repeated_words(response):
    words = response.lower().split()
    repeated_count = sum(1 for i in range(len(words) - 1) if words[i] == words[i + 1])
    return repeated_count
def analyze_sentiment(response):
    analysis = TextBlob(response)
    polarity = analysis.sentiment.polarity  # -1 (negative) to 1 (positive)
    
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"

def check_relevance(question, response):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([question, response])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    
    if similarity > 0.7:
        return "Highly relevant"
    elif similarity > 0.4:
        return "Somewhat relevant"
    else:
        return "Not relevant"

def analyze_response(question, response):
    filler_percentage = count_filler_words(response)
    repeated_words = detect_repeated_words(response)
    sentiment = analyze_sentiment(response)
    relevance = check_relevance(question, response)

    return {
        "filler_percentage": filler_percentage,
        "repeated_words_count": repeated_words,
        "sentiment": sentiment,
        "relevance": relevance,
        "feedback": generate_feedback(filler_percentage, repeated_words, sentiment, relevance)
    }

def generate_feedback(filler_percentage, repeated_words, sentiment, relevance):
    feedback = []

    if filler_percentage > 15:
        feedback.append("Too many filler words! Try speaking more clearly.")
    elif filler_percentage > 5:
        feedback.append("Try reducing filler words for better clarity.")
    
    if repeated_words > 0:
        feedback.append(f"You repeated words {repeated_words} times. Try to be more concise.")
    
    feedback.append(f"Your response has a {sentiment} tone.")

    return " ".join(feedback)
