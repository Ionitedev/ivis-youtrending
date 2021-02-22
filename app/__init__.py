from flask import Flask
import csv
import pickle

with open('app/static/Self-Introduction-to-IVIS21-_Responses_.csv') as f:
    csv_data = tuple(csv.reader(f))

s = b''
for i in range(11):
    with open('app/static/{}.pkl'.format(i), 'rb') as f:
        s += f.read()

test_data = pickle.loads(s)

for i, line in enumerate(csv_data):
    line.append(i)
    if i == 0:
        continue
    for j in range(12, 24):
        line[j] = int(line[j])

app = Flask(__name__)
from app import views
