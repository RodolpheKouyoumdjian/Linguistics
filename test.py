import time
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
import string
import json
all_texts = {}
language_ids = {}
characters = (string.punctuation + '“”„').replace('-', '')

'''def find_language(text):
    matched_lines = [line for line in text[:2000].split('\n') if "Language:" in line][0].replace('Language: ', '').replace('\r', '')
    return matched_lines

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

ids = [i for i in range(50)]

t = time.time()
map(create_all_texts_dict, ids)
print(time.time()-t)
print(language_ids)
t = time.time()
for id in ids:
    create_all_texts_dict(id)
print(time.time()-t)
print(language_ids)
'''

ids = [i for i in range(68500)]

def load_valid_texts(id):
    try:
        text =  load_etext(id)
        return text
    except:
        return None

data = {'Data': list(map(load_valid_texts, ids))}
json.dump(data, open('gutenbergtexts.json', 'w'))
