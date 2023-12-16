import streamlit as st
import pandas as pd
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# from PIL import Image
import spacy
# import io
from collections import Counter
# import re
# from ..modules import analyze_pos

nlp = spacy.load("en_core_web_sm")


st.title('Final Project Test Page2')

# uploaded_test = st.file_uploader("Upload data (csv)")
# if uploaded_test is not None:

data = "chaplin_learners_analysis.csv"
df = pd.read_csv(data, sep='\t', encoding='utf-8')
st.write(df.head(5))
st.write(len(df))
st.write(df.describe())

column_names = df.columns.tolist()

st.write(column_names)

option = st.selectbox(
    'Medium:',
    ('Written', 'Spoken', 'Both'))

if option == "Written":
    written_df = df[df["Medium"] == "Written"]
    st.write('You selected:', option)
    st.write(written_df)
    
if option == "Spoken":
    spoken_df = df[df["Medium"] == "Spoken"]
    st.write('You selected:', option)
    st.write(spoken_df)
    
if option == "Both":
    st.write('You selected:', option)
    st.write(df)

column_names = df.columns
# st.write(column_names)

selected_column = st.multiselect('Please choose the category you want to search for:', column_names)
# st.write('Selected category:', selected_column)

def analyze_pos(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    word_counts = Counter()
    pos_counts = Counter()

    for token in doc:
        word_counts[token.text] += 1
        pos_counts[token.pos_] += 1

    return word_counts, pos_counts

analized_df = spoken_df[['word_counts', 'pos_counts']] = spoken_df['Text'].apply(lambda x: pd.Series(analyze_pos(x)))

st.write(analized_df)
