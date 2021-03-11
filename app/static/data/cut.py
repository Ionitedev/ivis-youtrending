import pickle

with open('full_data.pkl', 'rb') as f:
    full_data = pickle.load(f)

with open('time_index.pkl', 'rb') as f:
    time_index = pickle.load(f)

cut_data = {i: full_data[i] for i in time_index['3m']}
with open('full_data.pkl', 'wb') as f:
    pickle.dump(cut_data, f)