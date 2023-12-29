import spacy
from collections import Counter
import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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

def Count_sum(df, column_name):
    totals = {}
    for row in df[column_name]:
        if isinstance(row, str):
            row = ast.literal_eval(row)

        for key, value in row.items():
            totals[key] = totals.get(key, 0) + value

    return totals

# result = count(chaplin_learners_all, 'pos_counts')
# result

def result2df(result):
    pos = list(result.keys())
    counts = list(result.values())
    count_df = pd.DataFrame({'POS or Word': pos, 'count': counts})
    count_df['percentage'] = (count_df['count'] / count_df['count'].sum()) * 100
    count_df['percentage'] = count_df['percentage'].round(2)
    return count_df



def filter_df(df, column, options, default_option, key):
    option = st.selectbox(column, options, key=key)
    if option != default_option:
        df = df[df[column] == option]
    return df, option

def display_selected_options(selected_options, title, len):
    with st.sidebar:
        st.markdown(f"#### {title}   (`{len}`)")
        for column, option in selected_options.items():
            st.write(f"- **{column}:** `{option}`")



def apply_filters(df, column_prefix, l1_options=('All','German', 'Spanish'), 
                proficiency_options=('All','intermediate', 'advanced')):
    selected_options = {}

    df_filtered, option = filter_df(df, 'Task title', ('All','2. Famous person','3. Film','13. Frog', '14. Chaplin'), 'All', f'{column_prefix}selectbox11')
    selected_options['Task title'] = option

    df_filtered, option = filter_df(df_filtered, 'Medium', ('All','Written', 'Spoken'), 'All', f'{column_prefix}selectbox1')
    selected_options['Medium'] = option

    df_filtered, option = filter_df(df_filtered, 'Sex', ('All','Male', 'Female'), 'All', f'{column_prefix}selectbox2')
    selected_options['Sex'] = option

    df_filtered, option = filter_df(df_filtered, 'L1', l1_options, 'All', f'{column_prefix}selectbox3')
    selected_options['L1'] = option

    df_filtered, option = filter_df(df_filtered, 'Proficiency_Category(2)', proficiency_options, 'All', f'{column_prefix}selectbox4')
    selected_options['Proficiency_Category(2)'] = option

    df_filtered, option = filter_df(df_filtered, 'Proficiency_Category(3)', ('All','beginner','intermediate', 'advanced'), 'All', f'{column_prefix}selectbox5')
    selected_options['Proficiency_Category(3)'] = option


    age_range = st.slider('Age', 0, 100, (0, 100), key=f'{column_prefix}age_range_slider')
    df_filtered = df_filtered[(df_filtered['Age'] >= age_range[0]) & (df_filtered['Age'] <= age_range[1])]
    selected_options['Age'] = f"{age_range[0]} - {age_range[1]}"
    
    age_range = st.slider('Years studying English', 0, 100, (0, 100), key=f'{column_prefix}age_range_slider2')
    df_filtered = df_filtered[(df_filtered['Years studying English'] >= age_range[0]) & (df_filtered['Years studying English'] <= age_range[1])]
    selected_options['Years studying English'] = f"{age_range[0]} - {age_range[1]}"
    
    age_range = st.slider('Age of exposure to English', 0, 100, (0, 100), key=f'{column_prefix}age_range_slider3')
    df_filtered = df_filtered[(df_filtered['Age of exposure to English'] >= age_range[0]) & (df_filtered['Age of exposure to English'] <= age_range[1])]
    selected_options['Age of exposure to English'] = f"{age_range[0]} - {age_range[1]}"

    selected_columns = st.multiselect('Choose columns:', df_filtered.columns, key=f'{column_prefix}multiselect', placeholder="ex: Medium, L1")

    additional_columns = ['token_details', 'word_pos_pairs', 'word_counts', 'pos_counts', 'lemma_counts']
    filtered_df = df_filtered[selected_columns + additional_columns]

    return filtered_df, selected_options



#wordcloud
def display_wordcloud(result1, result2):
    wordcloud1 = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate_from_frequencies(result1)
    wordcloud2 = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate_from_frequencies(result2)
    
    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud1)
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(plt)
        
    with col2:
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud2)
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(plt)