import streamlit as st

st.title('Final Project')
st.write('程式設計與資料科學導論(Dspy)')

st.write('R11142011: Yusuke Taira (語言所)')
st.write('R10142010: Mikhail Stepanenko (語言所)')
st.write('R11142010: Micah Kitsunai (語言所)')


st.link_button("COREFL", 'http://corefl.learnercorpora.com/')

st.write('Chaplin youtube: ','https://youtu.be/eO1HvF2G2Sw?si=YYsvgScwzDREkz-P')
video_url = 'https://youtu.be/eO1HvF2G2Sw?si=YYsvgScwzDREkz-P'

st.video(video_url)

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