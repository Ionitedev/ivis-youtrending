import pickle

with open('full_data.pkl', 'rb') as f:
    full_data = pickle.load(f)

tags = dict()

for i in full_data:
    for t in full_data[i][6]:
        t = t.replace('\\', '')
        if t not in tags:
            tags[t] = set()
        tags[t].add(i)

with open('tag_index.pkl', 'wb') as f:
    pickle.dump(tags, f)

print('tags: {}, count: {}'.format(len(tags), sum(len(tags[i]) for i in tags)))
print('tag_index.pkl saved.')
print()

with open('category_index.pkl', 'rb') as f:
    category_index = pickle.load(f)

category_tag = dict()

for c in category_index:
    if c not in category_tag:
        category_tag[c] = set()
    for i in category_index[c]:
        for t in full_data[i][6]:
            t = t.replace('\\', '')
            category_tag[c].add(t)

with open('category_tag.pkl', 'wb') as f:
    pickle.dump(category_tag, f)

print('most tags in a category: {} in {}'.format(max(len(category_tag[i]) for i in category_tag), sorted(category_tag.keys(), key=lambda x: len(category_tag[x]), reverse=True)[0]))
print('category_tag.pkl saved.')
print()

with open('lang_index.pkl', 'rb') as f:
    lang_index = pickle.load(f)

lang_tag = dict()

for c in lang_index:
    if c not in lang_tag:
        lang_tag[c] = set()
    for i in lang_index[c]:
        for t in full_data[i][6]:
            t = t.replace('\\', '')
            lang_tag[c].add(t)

with open('lang_tag.pkl', 'wb') as f:
    pickle.dump(lang_tag, f)

print('most tags in a lang: {}'.format(max(len(lang_tag[i]) for i in lang_tag)))
print('lang_tag.pkl saved.')
print()

with open('time_index.pkl', 'rb') as f:
    time_index = pickle.load(f)

time_tag = dict()

for c in time_index:
    if c not in time_tag:
        time_tag[c] = set()
    for i in time_index[c]:
        for t in full_data[i][6]:
            t = t.replace('\\', '')
            time_tag[c].add(t)

with open('time_tag.pkl', 'wb') as f:
    pickle.dump(time_tag, f)

print('most tags in a period: {}'.format(max(len(time_tag[i]) for i in time_tag)))
print('time_tag.pkl saved.')
print()

with open('country_index.pkl', 'rb') as f:
    country_index = pickle.load(f)

country_tag = dict()

for c in country_index:
    if c not in country_tag:
        country_tag[c] = set()
    for i in country_index[c]:
        for t in full_data[i][6]:
            t = t.replace('\\', '')
            country_tag[c].add(t)

with open('country_tag.pkl', 'wb') as f:
    pickle.dump(country_tag, f)

print('most tags in a country: {}'.format(max(len(country_tag[i]) for i in country_tag)))
print('country_tag.pkl saved.')
