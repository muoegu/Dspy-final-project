import streamlit as st
import pandas as pd
from modules import Count_sum
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import io
import ast

st.set_page_config(layout="wide")




st.title('COREFL ++')


# values = st.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0))
# st.write('Values:', values)


data = "chaplin_learners_analysis4.csv"
df = pd.read_csv(data, sep='\t', encoding='utf-8')
df_len = len(df)

def categorize_levels(df, column_name):
    df['Proficiency_Category'] = df[column_name].apply(lambda x: 'intermediate' if x in ['A1 (lower beginner)', 'A2 (upper beginner)', 'B1 (lower intermediate)'] else 'advanced')
    return df

def add_total_counts(df, column_name):
    df['total_counts'] = df[column_name].apply(lambda x: sum(eval(x).values()) if isinstance(x, str) and x.startswith('{') else 0)
    return df


def df_head_select_boxes(df_len):
    head_option = st.selectbox(
        'Display Data Size:',
        (10, 20, 50, 100, 'all'), key='selectbox20')
    return df_len if head_option == 'all' else head_option

st.write('Corpus data')

st.info('Here, you can select the number of data entries to display. By scrolling to the right or down, you can view all the data.')
st.write(f'Data size: {df_len}')

if __name__ == "__main__":
    df_len = len(df) 
    head_option = df_head_select_boxes(df_len)


df = categorize_levels(df, 'Proficiency')
df = add_total_counts(df, 'pos_counts')

st.dataframe(df.head(head_option), height=200)
st.write('Data description')
st.write(df.describe())


column_names = df.columns.tolist()


def filter_df(df, column, options, default_option, key):
    option = st.selectbox(column, options, key=key)
    if option != default_option:
        df = df[df[column] == option]
    return df, option

def display_selected_options(selected_options, title):
    with st.sidebar:
        st.markdown(f"### {title}")
        for column, option in selected_options.items():
            st.write(f"- **{column}:** {option}")


def apply_filters(df, column_prefix, l1_options=('All','German', 'Spanish'), 
                proficiency_options=('All','intermediate', 'advanced')):
    selected_options = {}
    df_filtered, option = filter_df(df, 'Medium', ('All','Written', 'Spoken'), 'All', f'{column_prefix}selectbox1')
    selected_options['Medium'] = option
    df_filtered, option = filter_df(df_filtered, 'Sex', ('All','Male', 'Female'), 'All', f'{column_prefix}selectbox2')
    selected_options['Sex'] = option
    df_filtered, option = filter_df(df_filtered, 'L1', l1_options, 'All', f'{column_prefix}selectbox3')
    selected_options['L1'] = option
    df_filtered, option = filter_df(df_filtered, 'Proficiency_Category', proficiency_options, 'All', f'{column_prefix}selectbox4')
    selected_options['Proficiency_Category'] = option
    selected_columns = st.multiselect('Choose columns:', df_filtered.columns, key=f'{column_prefix}multiselect')
    additional_columns = ['token_details', 'word_pos_pairs', 'word_counts', 'pos_counts', 'lemma_counts']
    filtered_df = df_filtered[selected_columns + additional_columns]
    return filtered_df, selected_options


def display_filtered_data(df_filtered, title):
    st.write(title)
    st.write(len(df_filtered))
    st.write('filtered data')
    st.dataframe(df_filtered, height=200)


st.write('Data Comparison Filter')
st.info('Here, you can select parameters for comparing two sets of data. By choosing the items you want to display in the "Choose columns:" section, you can verify that the filter function is working properly. The results can be checked in the sidebar on the left.')
col1, col2 = st.columns(2)


with col1:
    st.write("Filter Options")
    filtered_df1, selected_options1 = apply_filters(df, 'col1_')
    display_filtered_data(filtered_df1, 'Column 1 Data')

with col2:
    st.write("Filter Options")
    filtered_df2, selected_options2 = apply_filters(df, 'col2_')
    display_filtered_data(filtered_df2, 'Column 2 Data')
    

display_selected_options(selected_options1, 'Selected filter for Dataset1')
display_selected_options(selected_options2, 'Selected filter for Dataset2')



# def filter_df(df, column, options, default_option, key):
#     option = st.selectbox(column, options, key=key)
#     if option != default_option:
#         df = df[df[column] == option]
#     return df


# col1, col2 = st.columns(2)


# with col1:
#     st.write("Filter Options")
#     df1 = filter_df(df, 'Medium', ('All','Written', 'Spoken'), 'All', 'selectbox1')
#     df1 = filter_df(df1, 'Sex', ('All','Male', 'Female'), 'All', 'selectbox2')
#     df1 = filter_df(df1, 'L1', ('All','German', 'Spanish'), 'All', 'selectbox3')
#     df1 = filter_df(df1, 'Proficiency_Category', ('All','intermediate', 'advanced'), 'All', 'selectbox4')
#     # df1 = filter_df(df1, 'Year data collection', ('All','2017', '2018', '2019', '2020', '2021'), 'All', 'selectbox5')
#     selected_columns = st.multiselect('Choose columns:', df1.columns, key='multiselect1')
#     filtered_df1 = df1[selected_columns + ['token_details'] + ['word_pos_pairs'] + ['word_counts'] + ['pos_counts'] + ['lemma_counts']]
#     st.write(len(filtered_df1))
#     st.write('filtered data')
#     st.write(filtered_df1)
    

# with col2:
#     st.write("Filter Options")
#     df2 = filter_df(df, 'Medium', ('All','Written', 'Spoken'), 'All', 'selectbox11')
#     df2 = filter_df(df2, 'Sex', ('All','Male', 'Female'), 'All', 'selectbox12')
#     df2 = filter_df(df2, 'L1', ('All','German', 'Spanish'), 'All', 'selectbox13')
#     df2 = filter_df(df2, 'Proficiency_Category', ('All','intermediate', 'advanced'), 'All', 'selectbox14')
#     # df2 = filter_df(df2, 'Year data collection', ('All','2017', '2018', '2019', '2020', '2021'), 'all', 'selectbox15')
#     selected_columns = st.multiselect('Choose columns:', df2.columns, key='multiselect2')
#     filtered_df2 = df2[selected_columns + ['token_details'] + ['word_pos_pairs'] + ['word_counts'] + ['pos_counts'] + ['lemma_counts']]
#     st.write(len(filtered_df2))
#     st.write('filtered data')
#     st.write(filtered_df2)






# def total_word_count(df, column, word):
#     if not isinstance(df[column].iloc[0], dict):
#         df[column] = df[column].apply(ast.literal_eval)

#     total_count = df[column].apply(lambda d: d.get(word, 0)).sum()
#     return total_count

# search_key = st.text_input('Search word', '')

# a = total_word_count(filtered_df1, 'word_counts', search_key)
# st.write(a)



st.title("Comparison of Results")


# def display_select_boxes():
#     count_option = st.selectbox(
#             'Select count option:',
#             ('pos_counts', 'word_counts'), key='selectbox7')

#     return count_option


def display_select_boxes():
    options_mapping = {
        'Part-of-Speech Counts': 'pos_counts',
        'Word Frequency Counts': 'word_counts',
        'Not strict': 'lemma_counts'
        
    }

    count_option_label = st.selectbox(
        'Select count option:',
        options_mapping.keys(), 
        key='selectbox7'
    )

    count_option = options_mapping[count_option_label]

    return count_option

if __name__ == "__main__":
    count_option = display_select_boxes()

mode_option = st.selectbox(
            'Select Case Sensitivity:',
            ('case sensitive', 'not sensitive'), key='selectbox40')

result1 = Count_sum(filtered_df1, count_option)
result2 = Count_sum(filtered_df2, count_option)


def create_df(result):
    pos = list(result.keys())
    counts = list(result.values())

    count_df = pd.DataFrame({'POS or Word': pos, 'count': counts})

    count_df['percentage'] = (count_df['count'] / count_df['count'].sum()) * 100
    count_df['percentage'] = count_df['percentage'].round(2)

    return count_df



if __name__ == "__main__":

    result1_df = create_df(result1)
    result2_df = create_df(result2)
    
    result1_len = len(result1)
    result2_len = len(result2)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Result 1", result1_df)
        st.write("Total", result1_len)
    with col2:
        st.write("Result 2", result2_df)
        st.write("Total", result2_len)
        


def merge_and_sort_dataframes(df1, df2, merge_on, b, sort_by, suffixes=('_a', '_b')):
    df1 = df1.reset_index()
    df2 = df2.reset_index()
    merged_df = pd.merge(df1[[merge_on, b]], df2[[merge_on, b]], on=merge_on, suffixes=suffixes)

    merged_df = merged_df.sort_values(by=sort_by, ascending=False)

    merged_df.set_index(merge_on, inplace=True)

    return merged_df

merged_df = merge_and_sort_dataframes(result1_df, result2_df, 'POS or Word', 'percentage', ['percentage_a', 'percentage_b'])



# merged_df = pd.merge(result1_df[['POS or Word', 'percentage']], result2_df[['POS or Word', 'percentage']], on='POS or Word', suffixes=('_a', '_b'))
# merged_df = merged_df.sort_values(by=['percentage_a', 'percentage_b'], ascending=False)
# merged_df.set_index('POS or Word', inplace=True)


top_10_indices = merged_df.index[:15].tolist()

col1, col2 = st.columns(2)

with col1:
    head_num = st.selectbox(
            'Select count option:',
            (5, 10, 15, 20), key='selectbox30')

with col2:
    option = st.multiselect('ignore:', top_10_indices)


def seach_type():
    seach_type = st.selectbox(
            'Select seach type:',
            ('by dataframe', 'by word'), key='selectbox50')
    return seach_type




if __name__ == "__main__":
    seach_type = seach_type()
    st.write(seach_type)


#Concordance Search

st.title("Concordance Search")

col1, col2, col3 = st.columns(3)

with col1:
    concordance_key = st.text_input('Search key', '')

with col2:
    display_option = st.selectbox(
        "Select data to display",
        ("Both", "Words Before", "Words After")
    )

with col3:
    search_button = st.button('Search')

def search_surrounding_words_pos(df, search_word):
    prev_results = []  
    next_results = []  

    for word_pos_pairs in df['word_pos_pairs']: 
        word_pos_pairs = eval(word_pos_pairs)
        for i, (word, pos) in enumerate(word_pos_pairs):
            if word == search_word:
                if i > 0:
                    prev_word, prev_pos = word_pos_pairs[i-1]
                    prev_results.append((prev_word, prev_pos))
                if i < len(word_pos_pairs) - 1:
                    next_word, next_pos = word_pos_pairs[i+1]
                    next_results.append((next_word, next_pos))

    prev_df = pd.DataFrame(prev_results, columns=['word', 'POS'])
    next_df = pd.DataFrame(next_results, columns=['word', 'POS'])

    return prev_df, next_df




def analyze_pos_and_word_frequencies(data):
    pos_frequencies = data['POS'].value_counts(normalize=True) * 100
    word_frequencies = data['word'].value_counts()

    return pos_frequencies, word_frequencies

def display_frequencies(df, label):
    pos_freq, word_freq = analyze_pos_and_word_frequencies(df)
    return pos_freq.head(10), word_freq.head(10)

if search_button:
    prev_df1, next_df1 = search_surrounding_words_pos(filtered_df1, concordance_key)
    prev_df2, next_df2 = search_surrounding_words_pos(filtered_df2, concordance_key)
    prev_df1_len = len(prev_df1)
    next_df1_len = len(next_df1)
    prev_df2_len = len(prev_df2)
    next_df2_len = len(next_df2)
    
    filtered_df1_sum = sum(result1_df['count'])
    filtered_df2_sum = sum(result2_df['count'])
    percentage_prev1 =  prev_df1_len / filtered_df1_sum
    percentage_prev2 =  prev_df2_len / filtered_df2_sum
    percentage_next1 =  next_df1_len / filtered_df1_sum
    percentage_next2 =  next_df2_len / filtered_df2_sum
    
    

    pos_freq_before1, word_freq_before1 = display_frequencies(prev_df1, "Words Before")
    pos_freq_after1, word_freq_after1 = display_frequencies(next_df1, "Words After")
    pos_freq_before2, word_freq_before2 = display_frequencies(prev_df2, "Words Before")
    pos_freq_after2, word_freq_after2 = display_frequencies(next_df2, "Words After")

    if display_option in ["Both", "Words Before"]:

        col1, col4 = st.columns([3, 3])
        with col1:
            st.write(f"Words Before \"{concordance_key}\": {prev_df1_len}/{filtered_df1_sum} {percentage_prev1}%") 
            st.dataframe(prev_df1, width=400, height=200)
        with col4:
            st.write(f"Words Before \"{concordance_key}\": {prev_df2_len}/{filtered_df2_sum} {percentage_prev2}%") 
            st.dataframe(prev_df2, width=400, height=200)
            

        col2, col3, col5, col6 = st.columns([1, 1, 1, 1])
        with col2:
            st.write("Top 10 POS Frequencies")
            st.dataframe(pos_freq_before1, width=200, height=300)
        with col3:
            st.write("Top 10 Word Frequencies")
            # st.write(word_freq_before1)
            st.dataframe(word_freq_before1, width=200, height=300)
            
        with col5:
            st.write("Top 10 POS Frequencies")
            # st.write(pos_freq_before2)
            st.dataframe(pos_freq_before2, width=200, height=300)
            
        with col6:
            st.write("Top 10 Word Frequencies")
            # st.write(word_freq_before2)
            st.dataframe(word_freq_before2, width=200, height=300)
            

    if display_option in ["Both", "Words After"]:

        col1, col4 = st.columns([3, 3])
        with col1:
            st.write(f"Words Before \"{concordance_key}\": {next_df1_len}/{filtered_df1_sum} {percentage_next1}%") 
            st.dataframe(next_df1, width=400, height=200)
        with col4:
            st.write(f"Words Before \"{concordance_key}\": {next_df2_len}/{filtered_df2_sum} {percentage_next2}%") 
            st.dataframe(next_df2, width=400, height=200)
            
        col2, col3, col5, col6 = st.columns([1, 1, 1, 1])
        with col2:
            st.write("Top 10 POS Frequencies")
            st.dataframe(pos_freq_after1, width=200, height=300)
        with col3:
            st.write("Top 10 Word Frequencies")
            # st.write(word_freq_before1)
            st.dataframe(word_freq_after1, width=200, height=300)
            
        with col5:
            st.write("Top 10 POS Frequencies")
            # st.write(pos_freq_before2)
            st.dataframe(pos_freq_after2, width=200, height=300)
            
        with col6:
            st.write("Top 10 Word Frequencies")
            # st.write(word_freq_before2)
            st.dataframe(word_freq_after2, width=200, height=300)



def remove_rows_by_index(df, index_list):
    return df[~df.index.isin(index_list)]

merged_df = merge_and_sort_dataframes(result1_df, result2_df, 'POS or Word', 'percentage', ['percentage_a', 'percentage_b'])



st.title("Charts")

def process_dataframe(merged_df):
    df_copy = merged_df.copy()

    df_copy['diff'] = abs(df_copy['percentage_a'] - df_copy['percentage_b'])

    df_copy = df_copy.sort_values(by='diff', ascending=False)

    return df_copy

if __name__ == "__main__":
    processed_df = process_dataframe(merged_df)



# df_copy = merged_df.copy()

# # コピーに対して差の絶対値を計算し、新しいカラムに追加
# df_copy['diff'] = abs(df_copy['percentage_a'] - df_copy['percentage_b'])

# # コピーを並べ替え
# df_copy = df_copy.sort_values(by='diff', ascending=False)
# df_copy


merged_df = merged_df.head(head_num)


def plot_bar_graph(df, col_a, col_b):
    df[[col_a, col_b]].plot(kind='bar', figsize=(12, 6))
    plt.title('Percentage Comparison by POS or Word')
    plt.ylabel('Percentage(%)')
    plt.xlabel('POS or Word')
    plt.legend(['Dataset A', 'Dataset B'])
    plt.xticks(rotation=45)
    st.pyplot(plt)

def plot_pie_graph(df, col_a, col_b):
    total_a = df[col_a].sum()
    total_b = df[col_b].sum()
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    axs[0].pie(df[col_a], labels=df.index, autopct=lambda p: '{:.1f}%'.format(p * total_a / 100), startangle=140)
    axs[0].set_title('Dataset A Percentage')
    axs[1].pie(df[col_b], labels=df.index, autopct=lambda p: '{:.1f}%'.format(p * total_b / 100), startangle=140)
    axs[1].set_title('Dataset B Percentage')
    st.pyplot(plt)

def plot_stacked_bar_graph(df, col_a, col_b):
    df[[col_a, col_b]].plot(kind='bar', stacked=True, figsize=(12, 6))
    plt.title('Stacked Percentage Comparison by POS or Word')
    plt.ylabel('Percentage(%)')
    plt.xlabel('POS or Word')
    plt.legend(['Dataset A', 'Dataset B'])
    plt.xticks(rotation=45)
    st.pyplot(plt)
    
def plot_all_graphs(df, col1, col2):
    plot_bar_graph(df, col1, col2)
    plot_pie_graph(df, col1, col2)
    plot_stacked_bar_graph(df, col1, col2)


# merged_df2 = merge_and_sort_dataframes(pos_freq_before1, pos_freq_before2, 'POS', 'proportion', ['percentage_a', 'percentage_b'])
# merged_df2

def main():
    count_option = st.selectbox("Select option:", ("by dataframe", "by word"))
    chart_options = st.multiselect('Select chart type:', ['all','bar chart', 'pie chart', 'word cloud'])

    if count_option == 'by dataframe':
        if 'all' in chart_options:
            plot_all_graphs(merged_df, 'percentage_a', 'percentage_b')
        else:
            if 'pie chart' in chart_options:
                plot_pie_graph(merged_df, 'percentage_a', 'percentage_b')
            if 'bar chart' in chart_options:
                plot_bar_graph(merged_df, 'percentage_a', 'percentage_b')
            if 'word cloud' in chart_options:
                plot_stacked_bar_graph(merged_df, 'percentage_a', 'percentage_b')
    elif count_option == 'by word':
        if 'all' in chart_options:
            plot_all_graphs(merged_df, 'percentage_a', 'percentage_b')
        else:
            if 'pie chart' in chart_options:
                plot_pie_graph(merged_df2, 'percentage_a', 'percentage_b')
            if 'bar chart' in chart_options:
                plot_bar_graph(merged_df2, 'percentage_a', 'percentage_b')
            if 'word cloud' in chart_options:
                plot_stacked_bar_graph(merged_df2, 'percentage_a', 'percentage_b')

if __name__ == "__main__":
    main()





# merged_df[['percentage_a', 'percentage_b']].plot(kind='bar', figsize=(12, 6))
# plt.title('Percentage Comparison by POS or Word')
# plt.ylabel('Percentage(%)')
# plt.xlabel('POS or Word')
# plt.legend(['Dataset A', 'Dataset B'])
# plt.xticks(rotation=45)
# st.pyplot(plt)



# total_a = merged_df['percentage_a'].sum()
# total_b = merged_df['percentage_b'].sum()
# fig, axs = plt.subplots(1, 2, figsize=(12, 6))
# axs[0].pie(merged_df['percentage_a'], labels=merged_df.index, autopct=lambda p: '{:.1f}%'.format(p * total_a / 100), startangle=140)
# axs[0].set_title('Dataset A Percentage')
# axs[1].pie(merged_df['percentage_b'], labels=merged_df.index, autopct=lambda p: '{:.1f}%'.format(p * total_b / 100), startangle=140)
# axs[1].set_title('Dataset B Percentage')
# st.pyplot(plt)


# merged_df[['percentage_a', 'percentage_b']].plot(kind='bar', stacked=True, figsize=(12, 6))
# plt.title('Stacked Percentage Comparison by POS or Word')
# plt.ylabel('Percentage(%)')
# plt.xlabel('POS or Word')
# plt.legend(['Dataset A', 'Dataset B'])
# plt.xticks(rotation=45)
# st.pyplot(plt)


# def display_bar_chart():
#     top_15_1 = result1_df.sort_values('percentage', ascending=False).head(head_num)
#     top_15_2 = result2_df.sort_values('percentage', ascending=False).head(head_num) #.head(15)???
    
#     col1, col2 = st.columns(2)

#     with col1:
#         plt.figure(figsize=(12, 8))
#         plt.bar(top_15_1['POS or Word'], top_15_1['percentage'])
#         plt.xlabel('POS or Word')
#         plt.ylabel('percentage')
#         plt.title(' mksladgdnkjla by Percentage')
#         plt.xticks(rotation=45)

#         st.pyplot(plt)
        
#     with col2:      
#         plt.figure(figsize=(12, 8))
#         plt.bar(top_15_2['POS or Word'], top_15_2['percentage'])
#         plt.xlabel('POS or Word')
#         plt.ylabel('percentage')
#         plt.title('jwil by Percentage')
#         plt.xticks(rotation=45)

#         st.pyplot(plt)

# if __name__ == "__main__":
#     display_bar_chart()




#wordcloud
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


