from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from wordcloud import WordCloud
from Model import Categories
import pandas as pd
import matplotlib.pyplot as plt


def add_to_plot(wordcloud, title):
    fig = plt.figure()
    fig.suptitle(title, fontsize=20)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

def make_word_cloud():

    # stopwords to remove
    total_stopwords = [ENGLISH_STOP_WORDS, "said"]

    train_data = pd.read_csv('DataSets/train_set.csv', sep="\t")

    # business wordcloud
    business_list = train_data[(train_data['Category'] == Categories.Business)]
    business_list = business_list['Content']
    final_string = ""
    for content in business_list:
        final_string = ' '.join([word for word in content.split() if word not in total_stopwords])
    wordcloud = WordCloud(width = 1000, height = 600, background_color = "white", max_words = 1000).generate(final_string)
    add_to_plot(wordcloud, "Business")

    # politics wordcloud
    final_string = ""
    politics_list = train_data[(train_data['Category'] == Categories.Politics)]
    politics_list = politics_list['Content']
    for content in politics_list:
        final_string = ' '.join([word for word in content.split() if word not in total_stopwords])
    wordcloud = WordCloud(width = 1000, height = 600, background_color = "white", max_words = 1000).generate(final_string)
    add_to_plot(wordcloud, "Politics")
    
    # film wordcloud
    final_string = ""
    film_list_list = train_data[(train_data['Category'] == Categories.Film)]
    film_list_list = film_list_list['Content']
    for content in film_list_list:
        final_string = ' '.join([word for word in content.split() if word not in total_stopwords])
    wordcloud = WordCloud(width = 1000, height = 600, background_color = "white", max_words = 1000).generate(final_string)
    add_to_plot(wordcloud, "Film")
    
    # football wordcloud
    final_string = ""
    football_list = train_data[(train_data['Category'] == Categories.Football)]
    football_list = football_list['Content']
    for content in football_list:
        final_string = ' '.join([word for word in content.split() if word not in total_stopwords])
    wordcloud = WordCloud(width = 1000, height = 600, background_color = "white", max_words = 1000).generate(final_string)
    add_to_plot(wordcloud, "Football")

    # technology wordcloud
    final_string = ""
    technology_list = train_data[(train_data['Category'] == Categories.Technology)]
    technology_list = technology_list['Content']
    for content in technology_list:
        final_string = ' '.join([word for word in content.split() if word not in total_stopwords])
    wordcloud = WordCloud(width = 1000, height = 600, background_color = "white", max_words = 1000).generate(final_string)
    add_to_plot(wordcloud, "Technology")

    plt.show()


make_word_cloud()
