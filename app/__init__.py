from flask import Flask
import csv

with open('app/static/Self-Introduction-to-IVIS21-_Responses_.csv') as f:
    csv_data = tuple(csv.reader(f))

with open('app/static/1.csv', encoding='utf-8') as f:
    test_data = tuple(csv.reader(f))

for i, line in enumerate(csv_data):
    line.append(i)
    if i == 0:
        continue
    for j in range(12, 24):
        line[j] = int(line[j])

app = Flask(__name__)
from app import views
