import streamlit as st
import pandas as pd

st.title('前処理用')

uploaded_test = st.file_uploader("Upload data (csv)")

if uploaded_test is not None:
    df = pd.read_csv(uploaded_test, sep='\t', encoding='utf-8')
    
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Paris', 'London']
}
test_df = pd.DataFrame(data)

st.write(test_df)

