import pandas as pd
from modules import Count_sum
import matplotlib.pyplot as plt
from modules import apply_filters
from modules import display_selected_options
from modules import result2df
from modules import display_wordcloud
import numpy as np
import streamlit as st

st.set_page_config(layout="wide")


st.title('COREFL ++')
st.info("This app is an enhanced corpus analysis application designed to utilize the COEFL corpus(http://corefl.learnercorpora.com/) for English learners, making comparative analysis and visualization simpler. Please refer to the supplied hints for easier navigation and use of the app.")
# Create a table of contents in the sidebar
st.sidebar.title("Contents")
st.sidebar.markdown("""
- [Corpus data](#section-1)
- [Data Comparison Filter](#section-2)
- [Comparison of Results](#section-3)
- [Word Search](#section-4)
- [Charts](#section-5)
""")
st.markdown("<a name='section-1'></a>", unsafe_allow_html=True)
st.subheader('Corpus data')
df = pd.read_csv('learners_combined_data.csv', sep='\t', encoding='utf-8')
df_len = len(df)
st.write('Data size:',df_len)
#add proficiency category calomn
def categorize_levels(df, column_name):
    df['Proficiency_Category(2)'] = df[column_name].apply(lambda x: 'intermediate' if x in ['A1 (lower beginner)', 'A2 (upper beginner)', 'B1 (lower intermediate)'] else 'advanced')
    return df
def categorize_levels2(df, column_name):
    def categorize(x):
        if x in ['A1 (lower beginner)', 'A2 (upper beginner)']:
            return 'beginner'
        elif x in ['B1 (lower intermediate)', 'B2 (upper intermediate)']:
            return 'intermediate'
        else:
            return 'advanced'
    df['Proficiency_Category(3)'] = df[column_name].apply(categorize)
    return df
#add total counts column
def add_total_counts(df, column_name):
    df['total_counts'] = df[column_name].apply(lambda x: sum(eval(x).values()) if isinstance(x, str) and x.startswith('{') else 0)
    return df
df = categorize_levels(df, 'Proficiency')
df = categorize_levels2(df, 'Proficiency')
df = add_total_counts(df, 'pos_counts')
def select_display_size(df_len):
    head_option = st.selectbox(
        'Display Data Size:',
        (10, 20, 50, 100, 'all'), key='selectbox20')
    return df_len if head_option == 'all' else head_option
if __name__ == "__main__":
    df_len = len(df) 
    head_option = select_display_size(df_len)
st.dataframe(df.head(head_option), height=200)
#st.write('Data description')
#st.write(df.describe())
st.subheader('Data Comparison Filter')
st.markdown("<a href='section-2'></a>", unsafe_allow_html=True)
with st.expander("Hint"):
    st.info('💡Here, you can select parameters for comparing two sets of data. By choosing the items you want to display in the "Choose columns:" section, you can verify that the filter function is working properly. The results can be checked in the sidebar on the left.')
col1, col2 = st.columns(2)
with col1:
    st.write("Filter Options")
    filtered_df1, selected_options1 = apply_filters(df, 'col1_')    
    filtered_df1_len = len(filtered_df1)
    st.write('Filtered DatasetA :', filtered_df1_len)
    # filtered_df1 = df
    st.dataframe(filtered_df1.head(10), height=200)
with col2:
    st.write("Filter Options")
    filtered_df2, selected_options2 = apply_filters(df, 'col2_')
    filtered_df2_len = len(filtered_df2)
    st.write('Filtered DatasetB :', filtered_df2_len)
    # filtered_df2 = df
    st.dataframe(filtered_df2.head(10), height=200)
#display selected options on sidebar
display_selected_options(selected_options1, 'Filter Dataset A' ,filtered_df1_len)
display_selected_options(selected_options2, 'Filter Dataset B',filtered_df2_len)
st.subheader("Comparison of Results")
st.markdown("<a name='section-3'></a>", unsafe_allow_html=True)
with st.expander("Hint"):
    st.info('💡In this section, you can compare datasets after applying filters and view the results. You can select and display the comparison results for the frequency of words and POS.')
def display_select_boxes():
    options_mapping = {
        'POS Counts': 'pos_counts',
        'Word Frequency with Morphological Sensitivity': 'word_counts',
        'Word Frequency without Morphological Sensitivity': 'lemma_counts'
    }
    count_option_label = st.radio(
        'Select count option:',
        options_mapping.keys(), 
        key='selectbox7'
    )
    count_column_name = options_mapping[count_option_label]
    return count_column_name
if __name__ == "__main__":
    count_column_name = display_select_boxes()
# mode_option = st.selectbox(
#             'Select Case Sensitivity:',
#             ('case sensitive', 'not sensitive'), key='selectbox40')
result1 = Count_sum(filtered_df1, count_column_name)
result2 = Count_sum(filtered_df2, count_column_name)
if __name__ == "__main__":
    result1_df = result2df(result1)
    result2_df = result2df(result2)
    result1_len = len(result1)
    result2_len = len(result2)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dataset A**")
        st.dataframe(result1_df, height=300)
        st.write("Total:", result1_len)
    with col2:
        st.markdown("**Dataset B**")
        st.dataframe(result2_df, height=300)
        st.write("Total:", result2_len)
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
top_10_indices = merged_df.index[:20].tolist()
col1, col2 = st.columns(2)
with col1:
    head_num = st.selectbox(
            'Select count option:',
            (5, 10, 15, 20), key='selectbox30')
with col2:
    ignore_option = st.multiselect('Ignore:', top_10_indices)
# def seach_type():
#     seach_type = st.radio(
#             'Select seach type:',
#             ('show dataset analysis', 'show word analysis'), key='selectbox50')
#     return seach_type
# if __name__ == "__main__":
#     seach_type = seach_type()
#Concordance Search
st.write('')
st.subheader("Word Search")
st.markdown("<a name='section-4'></a>", unsafe_allow_html=True)
with st.expander("Hint"):
    st.info('💡In this section, you can perform a detailed analysis of words. You can investigate the frequency and occurrence of a particular word, as well as the words that appear before and after it, along with their POS.')
col1, col2, col3 = st.columns(3)
with col1:
    concordance_key = st.text_input('Search key', placeholder='ex: the')
with col2:
    display_option = st.selectbox(
        "Select data to display",
        ("Both", "Words Before", "Words After", "None")
    )
with col3:
    st.write('')
    search_button = st.button('Search')
def word_search_num():
    head_option2 = st.selectbox(
        'Display Data Size:',
        (5, 10, 20, 50), key='selectbox60')
    return head_option2
if __name__ == "__main__":
    head_option2 = word_search_num
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
def analyze_and_display_top_frequencies(data, top_n):
    pos_frequencies = data['POS'].value_counts(normalize=True) * 100
    word_frequencies = data['word'].value_counts()
    return pos_frequencies.head(top_n), word_frequencies.head(top_n)
def format_percentage(num):
    if num == 0:
        return "0%"
    else:
        return f"{num:.2g}%"
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
formatted_percentage = format_percentage(percentage_prev1)
formatted_percentage2 = format_percentage(percentage_prev2)
formatted_percentage3 = format_percentage(percentage_next1)
formatted_percentage4 = format_percentage(percentage_next2)
pos_freq_before1, word_freq_before1 = analyze_and_display_top_frequencies(prev_df1,10)
pos_freq_after1, word_freq_after1 = analyze_and_display_top_frequencies(next_df1,10)
pos_freq_before2, word_freq_before2 = analyze_and_display_top_frequencies(prev_df2,10)
pos_freq_after2, word_freq_after2 = analyze_and_display_top_frequencies(next_df2,10)
st.session_state['pos_freq_before1'], st.session_state['word_freq_before1'] = analyze_and_display_top_frequencies(prev_df1, 10)
st.session_state['pos_freq_after1'], st.session_state['word_freq_after1'] = analyze_and_display_top_frequencies(next_df1, 10)
st.session_state['pos_freq_before2'], st.session_state['word_freq_before2'] = analyze_and_display_top_frequencies(prev_df2, 10)
st.session_state['pos_freq_after2'], st.session_state['word_freq_after2'] = analyze_and_display_top_frequencies(next_df2, 10)
if search_button:
    if display_option == "None":
        st.write("")
    if display_option in ["Both", "Words Before"]:
        col1, col4 = st.columns([3, 3])
        with col1:
            st.write(f"Words Before \"{concordance_key}\" in dataset A : ", prev_df1_len) 
            st.write(f"{prev_df1_len}/{filtered_df1_sum} {formatted_percentage}")            
            st.dataframe(prev_df1, width=400, height=200)
        with col4:
            st.write(f"Words Before \"{concordance_key}\" in dataset B : ", prev_df2_len) 
            st.write(f"{prev_df2_len}/{filtered_df2_sum} {formatted_percentage2}%") 
            st.dataframe(prev_df2, width=400, height=200)
        col2, col3, col5, col6 = st.columns([1, 1, 1, 1])
        with col2:
            st.write("Top 10 POS Frequencies")
            st.dataframe(pos_freq_before1, width=200, height=300)
        with col3:
            st.write("Top 10 Word Frequencies")
            st.dataframe(word_freq_before1, width=200, height=300)
        with col5:
            st.write("Top 10 POS Frequencies")
            st.dataframe(pos_freq_before2, width=200, height=300)
        with col6:
            st.write("Top 10 Word Frequencies")
            st.dataframe(word_freq_before2, width=200, height=300)
    if display_option in ["Both", "Words After"]:
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col4 = st.columns([3, 3])
        with col1:
            st.write(f"Words After \"{concordance_key}\" in dataset A : ", next_df1_len) 
            st.write(f"{next_df1_len}/{filtered_df1_sum} {formatted_percentage}")            
            st.dataframe(next_df1, width=400, height=200)
        with col4:
            st.write(f"Words After \"{concordance_key}\" in dataset B : ", next_df2_len) 
            st.write(f"{next_df2_len}/{filtered_df2_sum} {formatted_percentage2}%") 
            st.dataframe(next_df2, width=400, height=200)
        col2, col3, col5, col6 = st.columns([1, 1, 1, 1])
        with col2:
            st.write("Top 10 POS Frequencies")
            st.dataframe(pos_freq_after1, width=200, height=300)
        with col3:
            st.write("Top 10 Word Frequencies")
            st.dataframe(word_freq_after1, width=200, height=300)
        with col5:
            st.write("Top 10 POS Frequencies")
            st.dataframe(pos_freq_after2, width=200, height=300)
        with col6:
            st.write("Top 10 Word Frequencies")
            st.dataframe(word_freq_after2, width=200, height=300)
def remove_rows_by_index(df, index_list):
    return df[~df.index.isin(index_list)]
# merged_df = merge_and_sort_dataframes(result1_df, result2_df, 'POS or Word', 'percentage', ['percentage_a', 'percentage_b'])
#wordcloud
def remove_keys_from_dict(target_dict, keys_to_remove):
    keys_to_delete = [key for key in target_dict if key in keys_to_remove]
    for key in keys_to_delete:
        del target_dict[key]
    return target_dict
result1_for_wordcloud = remove_keys_from_dict(result1, ignore_option)
result2_for_wordcloud = remove_keys_from_dict(result2, ignore_option)
# if __name__ == "__main__":
#     if count_column_name == 'word_counts':
#         st.subheader("Word Cloud")
#         display_wordcloud(result1_for_wordcloud, result2_for_wordcloud)
#     else:
#         st.write("")
#charts
st.subheader("Visualaization")
st.markdown("<a name='section-5'></a>", unsafe_allow_html=True)
merged_pos_freq_before = merge_and_sort_dataframes((st.session_state['pos_freq_before1']), (st.session_state['pos_freq_before2']), 'POS', 'proportion', ['proportion_a', 'proportion_b'])
merged_pos_freq_after = merge_and_sort_dataframes((st.session_state['pos_freq_after1']), (st.session_state['pos_freq_after2']), 'POS', 'proportion', ['proportion_a', 'proportion_b'])
merged_word_freq_before = merge_and_sort_dataframes((st.session_state['word_freq_before1']), (st.session_state['word_freq_before2']), 'word', 'count', ['count_a', 'count_b'])
merged_word_freq_after = merge_and_sort_dataframes((st.session_state['word_freq_after1']), (st.session_state['word_freq_after2']), 'word', 'count', ['count_a', 'count_b'])
# def process_dataframe(merged_df):
#     df_copy = merged_df.copy()
#     df_copy['diff'] = abs(df_copy['percentage_a'] - df_copy['percentage_b'])
#     df_copy = df_copy.sort_values(by='diff', ascending=False)
#     return df_copy
# if __name__ == "__main__":
#     processed_df = process_dataframe(merged_df)
def plot_bar_graph(df, col_a, col_b):
    df = remove_rows_by_index(df, ignore_option).head(head_num)
    color_a = '#bdecb6' 
    color_b = '#c3b1e1'
    ax = df[[col_a, col_b]].plot(kind='bar', figsize=(12, 6), color=[color_a, color_b])
    for p in ax.patches:
        ax.annotate('{:.1f}%'.format(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom')
    plt.ylabel('Percentage(%)')
    plt.xlabel('POS or Word')
    plt.legend(['Dataset A', 'Dataset B'])
    plt.xticks(rotation=45)
    st.pyplot(plt)
def plot_bar_graph2(df, col_a, col_b):
    df = remove_rows_by_index(df, ignore_option).head(head_num)
    color_a = '#bdecb6' 
    color_b = '#c3b1e1'
    ax = df.plot(kind='bar', stacked=True, figsize=(12, 6), color=[color_a, color_b])
    for bar in ax.patches:
        ax.annotate('{:.1f}%'.format(bar.get_height()), 
                    (bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2),
                    ha='center', va='center')
    plt.ylabel('Percentage(%)')
    plt.xlabel('POS or Word')
    plt.legend(['Dataset A', 'Dataset B'])
    plt.xticks(rotation=45)
    st.pyplot(plt)
def plot_pie_graph(df, col_a, col_b):
    df = remove_rows_by_index(df, ignore_option).head(head_num)
    total_a = df[col_a].sum()
    total_b = df[col_b].sum()
    cmap = plt.get_cmap('viridis')
    colors = cmap(np.linspace(0, 1, len(df)))
    colors = colors[:, :-1]  
    colors = colors + (1 - colors) * 0.6  
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    axs[0].pie(df[col_a], labels=df.index, autopct=lambda p: '{:.1f}%'.format(p * total_a / 100), startangle=140, colors=colors)
    axs[0].set_title('Dataset A')
    axs[1].pie(df[col_b], labels=df.index, autopct=lambda p: '{:.1f}%'.format(p * total_b / 100), startangle=140, colors=colors)
    axs[1].set_title('Dataset B')
    st.pyplot(plt)
# def plot_stacked_bar_graph(df, col_a, col_b):
#     df = remove_rows_by_index(df, ignore_option).head(head_num)
#     df[[col_a, col_b]].plot(kind='bar', stacked=True, figsize=(12, 6))
#     plt.title('Stacked Percentage Comparison by POS or Word')
#     plt.ylabel('Percentage(%)')
#     plt.xlabel('POS or Word')
#     plt.legend(['Dataset A', 'Dataset B'])
#     plt.xticks(rotation=45)
#     st.pyplot(plt)
def plot_all_graphs(df, col1, col2):
    display_wordcloud(result1_for_wordcloud, result2_for_wordcloud)
    plot_pie_graph(df, col1, col2)
    plot_bar_graph(df, col1, col2)
    # plot_bar_graph2(df, col1, col2)
    # plot_stacked_bar_graph(df, col1, col2)
# merged_df2 = merge_and_sort_dataframes(pos_freq_before1, pos_freq_before2, 'POS', 'proportion', ['percentage_a', 'percentage_b'])
# merged_df2
# merged_df = merge_and_sort_dataframes(result1_df, result2_df, 'POS or Word', 'percentage', ['percentage_a', 'percentage_b'])
def main():
    col1, col2, col3 = st.columns(3)
    with col1:
        count_option = st.radio("Analysis option:", ('show dataset analysis', 'show word analysis'),key='selectbox70')
    with col2:
        chart_options = st.multiselect('Select display chart type:', ['all','bar chart', 'pie chart', 'word cloud'])
    if count_option == 'show dataset analysis':
        if 'all' in chart_options:
            plot_all_graphs(merged_df, 'percentage_a', 'percentage_b')
        else:
            if 'pie chart' in chart_options:
                plot_pie_graph(merged_df, 'percentage_a', 'percentage_b')
            if 'bar chart' in chart_options:
                plot_bar_graph(merged_df, 'percentage_a', 'percentage_b')
            if 'word cloud' in chart_options:
                display_wordcloud(result1_for_wordcloud, result2_for_wordcloud)
    elif count_option == 'show word analysis':
        with col3:
            display_option3 = st.radio(
            "Select data to display",
            ("Both", "Words Before", "Words After")
        )
        if 'Both' in display_option3:
            st.subheader('POS before')
            plot_pie_graph(merged_pos_freq_before, 'proportion_a', 'proportion_b')
            plot_bar_graph(merged_pos_freq_before, 'proportion_a', 'proportion_b')
            st.subheader('POS after')
            plot_pie_graph(merged_pos_freq_after, 'proportion_a', 'proportion_b')
            plot_bar_graph(merged_pos_freq_after, 'proportion_a', 'proportion_b')
            st.markdown("<hr>", unsafe_allow_html=True)
            st.subheader('word before')
            plot_pie_graph(merged_word_freq_before, 'count_a', 'count_b')
            plot_bar_graph(merged_word_freq_before, 'count_a', 'count_b')
            st.subheader('word after')
            plot_pie_graph(merged_word_freq_after, 'count_a', 'count_b')
            plot_bar_graph(merged_word_freq_after, 'count_a', 'count_b')
        if "Words Before" in display_option3:
            st.subheader('POS before')
            plot_pie_graph(merged_pos_freq_before, 'proportion_a', 'proportion_b')
            plot_bar_graph(merged_pos_freq_before, 'proportion_a', 'proportion_b')
            st.subheader('POS after')
            plot_pie_graph(merged_pos_freq_after, 'proportion_a', 'proportion_b')
            plot_bar_graph(merged_pos_freq_after, 'proportion_a', 'proportion_b')
        if "Words After" in display_option3:
            st.subheader('word before')
            plot_pie_graph(merged_word_freq_before, 'count_a', 'count_b')
            plot_bar_graph(merged_word_freq_before, 'count_a', 'count_b')
            st.subheader('word after')
            plot_pie_graph(merged_word_freq_after, 'count_a', 'count_b')
            plot_bar_graph(merged_word_freq_after, 'count_a', 'count_b')
if __name__ == "__main__":
    main()