import pickle
import datetime

with open('full_data.pkl', 'rb') as f:
    full_data = pickle.load(f)

time_index = {'1w': set(), '2w': set(), '1m': set()}
latest = datetime.date(2021, 3, 7)
for i in full_data:
    t = latest - full_data[i][7][-1].date()
    if t <= datetime.timedelta(days=7):
        time_index['1w'].add(i)
    elif t <= datetime.timedelta(days=14):
        time_index['2w'].add(i)
    elif t <= datetime.timedelta(days=30):
        time_index['1m'].add(i)
    
with open('time_index.pkl', 'wb') as f:
    pickle.dump(time_index, f)

print('time_index.pkl saved.')


with open('category_index.pkl', 'rb') as f:
    category_index = pickle.load(f)

category_index = {i: category_index[i].intersection(full_data.keys()) for i in category_index}

with open('category_index.pkl', 'wb') as f:
    pickle.dump(category_index, f)


print('country_index.pkl saved.')
with open('country_index.pkl', 'rb') as f:
    country_index = pickle.load(f)

country_index = {i: country_index[i].intersection(full_data.keys()) for i in country_index}

with open('country_index.pkl', 'wb') as f:
    pickle.dump(country_index, f)

print('country_index.pkl saved.')


with open('lang_index.pkl', 'rb') as f:
    lang_index = pickle.load(f)

lang_index = {i: lang_index[i].intersection(full_data.keys()) for i in lang_index}

with open('lang_index.pkl', 'wb') as f:
    pickle.dump(lang_index, f)

print('lang_index.pkl saved.')