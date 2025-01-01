import spacy

nlp = spacy.load('en_core_web_sm')

text = "I am looking for a full-stack development job for HUF 5,000,000 per year, I am mainly interested in web development."

doc = nlp(text)

keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN', 'NUM', 'ADJ']]

print(f"Kulcsszavak: {keywords}")
