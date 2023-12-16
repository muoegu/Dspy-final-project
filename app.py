import streamlit as st
import spacy

nlp = spacy.load("en_core_web_sm")

st.title('Final Project')
st.write('程式設計與資料科學導論(Dspy)')

st.write('R11142010: Micah Kitsunai')
st.write('R11142010: Micah Kitsunai')
st.write('R11142010: Micah Kitsunai')


st.link_button("Go to gallery", 'http://corefl.learnercorpora.com/')
# st.slider("Pick a number", 0, 100)
# st.select_slider("Pick a size", ["S", "M", "L"])
# st.balloons()
# st.snow()
# st.toast('Warming up...')
# st.error('Error message')
# st.warning('Warning message')
# st.info('Info message')
# st.success('Success message')
# # st.exception(e)