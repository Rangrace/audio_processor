import spacy

# Load English tokenizer, tagger, parser, NER
nlp = spacy.load("en_core_web_sm")

def extract_intent(text):
    doc = nlp(text)
    intent = None
    for token in doc:
        if token.pos_ == "VERB":
            intent = token.text
            break
    return intent

user_intent = extract_intent("I want to book a flight to New York")
print("User intent:", user_intent)
