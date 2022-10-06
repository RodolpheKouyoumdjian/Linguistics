from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
import pandas as pd
from collections import Counter
import string
from datetime import datetime
import json

start_time = datetime.now()
all_texts = {}
language_ids = {}
characters = (string.punctuation + '“”„').replace('-', '')

# Returns dataframe of sorted words
def get_word_frequency(text):
    freq = Counter(text.split())
    return freq

# Finds in which language the text was written
def find_language(text):
    matched_lines = [line for line in text[:2000].split('\n') if "Language:" in line][0].replace('Language: ', '').replace('\r', '')
    return matched_lines

def remove_punctuation(text):
    return text.lower().translate(str.maketrans(characters, ' '*len(characters))).translate(str.maketrans(string.digits, ' '*len(string.digits)))

# Sort by language and store in dictionary and store data
def create_all_texts_dict(id):
    try:
        text = load_etext(id)
        stripped_text = strip_headers(text).strip()

        try:
            language = find_language(text)
        except:
            language = 'Unknown'

        try:
            all_texts[language] += (' ' + stripped_text)
            language_ids[language].append(id)
        except:
            all_texts[language] = stripped_text
            language_ids[language] = [id]
    except:
        pass

# Store Gutenberg and ids per language in json files
json.dump(all_texts, open('GutenbergCorpus.json', 'w'))
json.dump(language_ids, open('LanguageIDS.json', 'w'))

# Find each languages frequency and store data in csv
for lang in all_texts.keys():
    all_texts[lang] = remove_punctuation(all_texts[lang])
    words_freq = get_word_frequency(all_texts[lang])
    words = list(words_freq.keys())
    frequency = list(words_freq.values())
    df = pd.DataFrame({'Words': words, 'Frequency': frequency}).sort_values(by='Frequency', ascending=False).reset_index().drop(columns=['index'])
    df.to_csv(lang + 'Frequency.csv')

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))