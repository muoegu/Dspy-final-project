import streamlit as st
import pandas as pd
import spacy
from collections import Counter

st.title('前処理用')

uploaded_data = st.file_uploader("Upload data (csv)")

if uploaded_data is not None:
    df = pd.read_csv(uploaded_data, sep='\t', encoding='utf-8')
    
def analyze_pos(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    word_counts = Counter()
    pos_counts = Counter()

    for token in doc:
        word_counts[token.text] += 1
        pos_counts[token.pos_] += 1

    return dict(word_counts), dict(pos_counts)

def add_analysis_columns(df, text_column):
    df[['word_counts', 'pos_counts']] = df[text_column].apply(lambda x: pd.Series(analyze_pos(x)))

    return df


nlp = spacy.load('en_core_web_sm')

def add_word_pos_pairs(df, text_column):

    def get_word_pos_pairs(text):
        doc = nlp(text)
        return [(token.text, token.pos_) for token in doc]

    df['word_pos_pairs'] = df[text_column].apply(get_word_pos_pairs)

    return df



df = add_analysis_columns(df, 'Text')
df

result_df = add_word_pos_pairs(df, 'Text')


st.write(result_df)

