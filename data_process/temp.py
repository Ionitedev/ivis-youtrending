import pickle

with open('country_index.pkl', 'rb') as f:
    country_index = pickle.load(f)
country_index = {i: set(country_index[i]) for i in country_index}
with open('country_index.pkl', 'wb') as f:
    pickle.dump(country_index, f)

with open('time_index.pkl', 'rb') as f:
    time_index = pickle.load(f)
time_index = {i: set(time_index[i]) for i in time_index}
with open('time_index.pkl', 'wb') as f:
    pickle.dump(time_index, f)

with open('lang_index.pkl', 'rb') as f:
    lang_index = pickle.load(f)
lang_index = {i: set(lang_index[i]) for i in lang_index}
with open('lang_index.pkl', 'wb') as f:
    pickle.dump(lang_index, f)

with open('category_index.pkl', 'rb') as f:
    category_index = pickle.load(f)
category_index = {i: set(category_index[i]) for i in category_index}
with open('category_index.pkl', 'wb') as f:
    pickle.dump(category_index, f)