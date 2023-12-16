import spacy
from collections import Counter
import pandas as pd

def analyze_pos(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    word_counts = Counter()
    pos_counts = Counter()

    for token in doc:
        word_counts[token.text] += 1
        pos_counts[token.pos_] += 1

    return word_counts, pos_counts

# df = pd.DataFrame({'text': ['This is a sample text.', 'Another text example.']})

# df[['word_counts', 'pos_counts']] = df['text'].apply(lambda x: pd.Series(analyze_pos(x)))

# df


import pandas as pd
import ast 

def count(df, column_name):
    totals = {}
    for row in df[column_name]:
        if isinstance(row, str):
            row = ast.literal_eval(row)

        for key, value in row.items():
            totals[key] = totals.get(key, 0) + value

    return totals

# result = count(chaplin_learners_all, 'pos_counts')
# result

