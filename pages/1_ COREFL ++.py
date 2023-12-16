import streamlit as st
import pandas as pd
from modules import Count_sum
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import io

st.title('COREFL ++')



data = "chaplin_learners_analysis.csv"
df = pd.read_csv(data, sep='\t', encoding='utf-8')

def categorize_levels(df, column_name):
    df['Proficiency_Category'] = df[column_name].apply(lambda x: 'intermediate' if x in ['A1 (lower beginner)', 'A2 (upper beginner)', 'B1 (lower intermediate)'] else 'advanced')
    return df

def add_total_counts(df, column_name):
    df['total_counts'] = df[column_name].apply(lambda x: sum(eval(x).values()) if isinstance(x, str) and x.startswith('{') else 0)
    return df

def df_head_select_boxes():
    head_option = st.selectbox(
        'Select count option:',
        (5, 10, 20, 50 ,100), key='selectbox20')
    return head_option

if __name__ == "__main__":
    head_option = df_head_select_boxes()

df = categorize_levels(df, 'Proficiency')
df = add_total_counts(df, 'pos_counts')


st.write(df.head(head_option))
st.write(len(df))
st.write(df.describe())

column_names = df.columns.tolist()
# st.write(column_names)

def filter_df(df, column, options, default_option, key):
    option = st.selectbox(column, options, key=key)
    if option != default_option:
        df = df[df[column] == option]
    return df



col1, col2 = st.columns(2)

with col1:
    st.write("Filter Options")
    df1 = filter_df(df, 'Medium', ('All','Written', 'Spoken'), 'All', 'selectbox1')
    df1 = filter_df(df1, 'Sex', ('All','Male', 'Female'), 'All', 'selectbox2')
    df1 = filter_df(df1, 'L1', ('All','German', 'Spanish'), 'All', 'selectbox3')
    df1 = filter_df(df1, 'Proficiency', ('All','intermediate', 'advanced'), 'All', 'selectbox4')
    # df1 = filter_df(df1, 'Year data collection', ('All','2017', '2018', '2019', '2020', '2021'), 'All', 'selectbox5')
    selected_columns = st.multiselect('Choose columns:', df1.columns, key='multiselect1')
    filtered_df1 = df1[selected_columns + ['word_counts']+ ['pos_counts']]
    st.write(len(filtered_df1))
    st.write('filtered data')
    st.write(filtered_df1)
    

with col2:
    st.write("Filter Options")
    df2 = filter_df(df, 'Medium', ('All','Written', 'Spoken'), 'All', 'selectbox11')
    df2 = filter_df(df2, 'Sex', ('All','Male', 'Female'), 'All', 'selectbox12')
    df2 = filter_df(df2, 'L1', ('All','German', 'Spanish'), 'All', 'selectbox13')
    df2 = filter_df(df2, 'Proficiency', ('All','intermediate', 'advanced'), 'All', 'selectbox14')
    # df2 = filter_df(df2, 'Year data collection', ('All','2017', '2018', '2019', '2020', '2021'), 'all', 'selectbox15')
    selected_columns = st.multiselect('Choose columns:', df2.columns, key='multiselect2')
    filtered_df2 = df2[selected_columns + ['word_counts']+ ['pos_counts']]
    st.write(len(filtered_df2))
    st.write('filtered data')
    st.write(filtered_df2)


def display_select_boxes():
    col1, col2 = st.columns(2)

    with col1:
        selected_option1 = st.selectbox(
            'Select count option:',
            ('pos_counts', 'word_counts'), key='selectbox7')

    with col2:
        selected_option2 = st.selectbox(
            'Select count option:',
            ('pos_counts', 'word_counts'), key='selectbox8')

    return selected_option1, selected_option2

if __name__ == "__main__":
    count_option1, count_option2 = display_select_boxes()

result1 = Count_sum(filtered_df1, count_option1)
result2 = Count_sum(filtered_df2, count_option2)




def create_df(result):
    count_df = pd.DataFrame.from_dict(result, orient='index', columns=['count'])
    count_df['percentage'] = (count_df['count'] / count_df['count'].sum()) * 100
    count_df['percentage'] = count_df['percentage'].round(2)
    return count_df



if __name__ == "__main__":
    st.title("Comparison of Results")

    result1_df = create_df(result1)
    result2_df = create_df(result2)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Result 1", result1_df)
    with col2:
        st.write("Result 2", result2_df)
        


def display_bar_chart():
    top_15_1 = result1_df.sort_values('percentage', ascending=False).head(15)
    top_15_2 = result2_df.sort_values('percentage', ascending=False).head(15)
    
    
    col1, col2 = st.columns(2)

    with col1:
        plt.figure(figsize=(12, 8))
        plt.bar(top_15_1.index, top_15_1['percentage'])
        plt.xlabel('aaa')
        plt.ylabel('percentage')
        plt.title(' mksladgdnkjla by Percentage')
        plt.xticks(rotation=45)

        st.pyplot(plt)
        
    with col2:      
        plt.figure(figsize=(12, 8))
        plt.bar(top_15_2.index, top_15_2['percentage'])
        plt.xlabel('mnskl')
        plt.ylabel('percentage')
        plt.title('jwil by Percentage')
        plt.xticks(rotation=45)

        st.pyplot(plt)

if __name__ == "__main__":
    st.title("Bar chart")
    display_bar_chart()


def display_wordcloud():

    wordcloud1 = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate_from_frequencies(result1)
    wordcloud2 = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate_from_frequencies(result2)
    

    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud1)
        plt.axis("off")
        plt.tight_layout(pad=0)

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        image = Image.open(img_buf)

        st.image(image, caption='Word Cloud')
        
    with col2:
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud2)
        plt.axis("off")
        plt.tight_layout(pad=0)

        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        image = Image.open(img_buf)

        st.image(image, caption='Word Cloud')

if __name__ == "__main__":
    st.title("Word Cloud")
    display_wordcloud()
