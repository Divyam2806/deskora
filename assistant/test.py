import spacy

nlp = spacy.load("en_core_web_sm")

def show_entities(text):
    doc = nlp(text)
    if doc.ents:
        print("\nNamed Entities found:")
        for ent in doc.ents:
            print(f" - {ent.text} → {ent.label_}")
    else:
        print("No named entities detected.")

while True:
    user_input = input("\nType something (or 'exit'): ")
    if user_input.lower() == "exit":
        break
    show_entities(user_input)
