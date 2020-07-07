import pandas as pd

import nltk
#nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()

# stemming train set
train_data = pd.read_csv('DataSets/train_set.csv', sep="\t", encoding = 'utf8')
for idx, row in train_data.iterrows():
    print "Currently on line : " + str(idx) + " of train set"
    final_content = "";
    current_content = row.Content
    content_words = word_tokenize(current_content)
    for w in content_words:
        final_content = final_content + " " + ps.stem(w)
    train_data.set_value(idx, 'Content', final_content)

    final_title = "";
    current_title = row.Title
    title_words = word_tokenize(current_title)
    for w in title_words:
        final_title = final_title + " " + ps.stem(w)
    train_data.set_value(idx, 'Title', final_title)

train_data.to_csv('DataSets/stemmed_train_set.csv', sep='\t', encoding = 'utf8' ,index = False, index_label = False)

# stemming test set
test_data = pd.read_csv('DataSets/test_set.csv', sep="\t", encoding = 'utf8')
for idx, row in test_data.iterrows():
    print "Currently on line : " + str(idx) + " of test set"
    final_content = "";
    current_content = row.Content
    content_words = word_tokenize(current_content)
    for w in content_words:
        final_content = final_content + " " + ps.stem(w)
    test_data.set_value(idx, 'Content', final_content)

    final_title = "";
    current_title = row.Title
    title_words = word_tokenize(current_title)
    for w in title_words:
        final_title = final_title + " " + ps.stem(w)
    test_data.set_value(idx, 'Title', final_title)
test_data.to_csv('DataSets/stemmed_test_set.csv', sep='\t', encoding = 'utf8' ,index = False, index_label = False)