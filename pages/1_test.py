import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import spacy
import io
from collections import Counter
import re

nlp = spacy.load("en_core_web_sm")


st.title('Final Project')

# uploaded_test = st.file_uploader("Upload data (csv)")
# if uploaded_test is not None:

data = "Chaplin_Learners_all.csv"
df = pd.read_csv(data, sep='\t', encoding='utf-8')
st.write(df.head(5))
st.write(len(df))
st.write(df.describe())

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

def create_value_counts(df, selected_columns):
    result = {}
    for column_name in selected_columns:
        column_name_modified = column_name.replace(" ", "-")
        counts = df[column_name].value_counts()
        percentage = (df[column_name].value_counts(normalize=True) * 100).round(1)
        result[column_name_modified] = pd.DataFrame({
            'Counts': counts, 
            'Percentage (%)': percentage
        })
    
    return result

value_counts_result = create_value_counts(df, selected_column)
for key, value in value_counts_result.items():
    st.write(f"{key}:")
    st.write(value)
    st.write()
    
st.write("Text Data:")
text_df = df["Text"]
st.write(text_df)
    

text = st.text_area("Input text here:")

if text:  
    word_count = len(text.split())
    st.write(f"Word count: {word_count}")
    
    doc = nlp(text)
    word_count = len([token.text for token in doc if token.is_alpha])
    st.write(f"Word coun by Spacy: {word_count}")

    
    wordcloud = WordCloud(width = 800, height = 800, background_color ='white').generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    st.image(buf, caption='Generated WordCloud', use_column_width=True)
    
#all text's word cloud
combined_text = ' '.join(df['Text'])
word_count = len(text.split())
st.write(f"Word count: {word_count}")

doc = nlp(text)
word_count = len([token.text for token in doc if token.is_alpha])
st.write(f"Word coun by Spacy: {word_count}")

wordcloud = WordCloud(width = 800, height = 800, background_color ='white').generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
st.image(buf, caption='Generated WordCloud', use_column_width=True)



text_t = st.text_area("Input text here:あsんkl")

if text_t: 
    def word_frequency_ranking(text_t):
        # 小文字に変換し、単語以外の文字を除去
        words = re.findall(r'\b\w+\b', text_t.lower())
        # 単語の出現回数をカウント
        frequency = Counter(words)
        # 頻度が高い順にソート
        return frequency.most_common()

    # 関数のテスト
    # text = "This is a test. This test is simple. Very, very simple."
    st.write(word_frequency_ranking(text_t))