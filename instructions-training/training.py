
import re
import string
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from board.regex import get_word_count
import warnings
from board.list_analysis import get_lower_bound

warnings.filterwarnings('ignore')

df = pd.read_csv('instructions_training.csv', encoding='latin1')

instruction_msg = df[df.isInstruction == 1]
not_instruction_msg = df[df.isInstruction == 0]
not_instruction_msg = not_instruction_msg.sample(n=len(instruction_msg),
                         random_state=42)
 
balanced_data = df

punctuations_list = string.punctuation
def remove_punctuations(text):
    temp = str.maketrans('', '', punctuations_list)
    return text.translate(temp)

# Stopwords are commonly used words like 'the' and 'it' which add no relevant information
def remove_stopwords(text):
    stop_words = stopwords.words('english')
 
    imp_words = []
 
    # Storing the important words
    for word in str(text).split():
        word = word.lower()
 
        if word not in stop_words:
            imp_words.append(word)
 
    output = " ".join(imp_words)
 
    return output

# def get_word_average(data):
#     word_count = []
#     for x in data['listElement']:
#         word_count.append(get_word_count(x))
#     test_list = word_count
#     mean = sum(test_list) / len(test_list) 
#     variance = sum([((x - mean) ** 2) for x in test_list]) / len(test_list) 
#     res = variance ** 0.5
#     return mean - res

balanced_data['listElement'] = balanced_data['listElement'].astype(str).apply(lambda x: x.lower())
balanced_data['listElement'] = balanced_data['listElement'].apply(lambda x: remove_punctuations(x))
# get_word_average(balanced_data[balanced_data['isInstruction'] == 0])
# get_word_average(balanced_data[balanced_data['isInstruction'] == 1])

balanced_data['listElement'] = balanced_data['listElement'].apply(lambda text: remove_stopwords(text))


def count_words(data,type):
    word_count = []
    count = 0
    for x in data['listElement']:
        if get_word_count(x) > get_lower_bound():
            word_count.append(x)
            count += 1
    email_corpus = " ".join(data['listElement'])
    words = re.findall(r'\w+', email_corpus)
    return Counter(words).most_common(300)

instruction_words = count_words(balanced_data[balanced_data['isInstruction'] == 1], type='instruction')
non_instruction_words = count_words(balanced_data[balanced_data['isInstruction'] == 0], type='Non-instruction')

new_count = []
for x in instruction_words:
    data = balanced_data[balanced_data['isInstruction'] == 0]
    email_corpus = " ".join(data['listElement'])
    words = email_corpus.split()
    count = 0
    for word in words:
        if word == x[0]:
            count += 1
    new_count.append((x[0],x[1]/(count+1)))

sorted_by_second = sorted(new_count, key=lambda tup: tup[1])
print(sorted_by_second)
