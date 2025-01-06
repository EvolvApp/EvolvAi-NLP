import spacy
import re
import enchant
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)

programming_languages = ["Python", "Java", "JavaScript", "C#", "C++", "React", "Ruby", "PHP", "Swift", "Go", "Rust", "backend", "frontend"]
developer_roles = ["developer", "engineer", "architect"]

for lang in programming_languages:
    matcher.add(lang, [[{"LOWER": lang.lower()}]])

d = enchant.Dict("en_US")

def extract_keywords_and_entities(text):

    doc = nlp(text)

    keywords = [token.lemma_.lower() for token in doc if token.pos_ in ['NOUN', 'ADJ', 'PROPN', 'VERB'] and not token.is_stop]
    keywords = list(dict.fromkeys(keywords)) # Duplikációk eltávolítása

    entities = [(ent.text, ent.label_) for ent in doc.ents]

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        entities.append((span.text, "PROGRAMMING_LANGUAGE"))

    entities = list(dict.fromkeys(entities))

    languages = []
    for i, token in enumerate(doc):
        if token.text in programming_languages:
            phrase = token.text
            for j in range(i + 1, min(i + 2, len(doc))):
                if doc[j].text in developer_roles:
                    phrase += " " + doc[j].text
                    break
            languages.append(phrase)
        elif token.text in developer_roles:
            phrase = token.text
            for j in range(i - 1, max(-1, i - 2), -1):
                if doc[j].text in programming_languages:
                    phrase = doc[j].text + " " + phrase
                    break
            languages.append(phrase)

    languages = list(dict.fromkeys(languages))

    spelling_errors = [word for word in text.split() if not d.check(word) and not re.match(r'\b\d+\b', word) and not re.match(r'[^\w\s]', word)]
    spelling_errors = list(dict.fromkeys(spelling_errors))

    money_pattern = re.compile(r'\b\d+\s*(?:USD|HUF|EUR|GBP|JPY)\b', re.IGNORECASE)
    money_entities = money_pattern.findall(text)
    money_entities = list(dict.fromkeys(money_entities))

    return keywords, entities, languages, spelling_errors, money_entities

def generate_summary(keywords, entities, languages, spelling_errors, money_entities):


    summary = "A szöveg:\n"

    if keywords:
        summary += f"Főbb kulcsszavak: {', '.join(keywords)}\n"
    if entities:
        summary += "Entitások:\n"
        for entity, label in entities:
            summary += f"- {entity} ({label})\n"
    if languages:
        summary += f"Programozási nyelvek/Technológiák: {', '.join(languages)}\n"
    if spelling_errors:
        summary += f"Helyesírási hibák: {', '.join(spelling_errors)}\n"
    if money_entities:
        summary += f"Pénzösszegek: {', '.join(money_entities)}\n"
    else:
        summary += "Nem található pénzösszeg.\n"

    return summary

text = "I think the best job in my prefere C# developer and java frontendd i dont like react i think te bes pay 1000Usd/ month I am a java developer and backend developer also i am a developer"

keywords, entities, languages, spelling_errors, money_entities = extract_keywords_and_entities(text)

summary = generate_summary(keywords, entities, languages, spelling_errors, money_entities)
print(summary)