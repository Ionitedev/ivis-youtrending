import csv
import pickle
import math

with open('1.csv', encoding='utf-8') as f:
    data = tuple(csv.reader(f))

print(len(data))
s = pickle.dumps(data)
print(len(s))

blocksize = 20 * 1024 ** 2
for i in range(math.ceil(len(s) / blocksize)):
    with open('{}.pkl'.format(i), 'wb') as f:
        f.write(s[i * blocksize: (i + 1) * blocksize])

s = b''
for i in range(11):
    with open('{}.pkl'.format(i), 'rb') as f:
        s += f.read()

print(len(s))
data = pickle.loads(s)
print(len(data))

