from flask import Flask
import pickle

# read
with open('app/static/data/full_data.pkl', 'rb') as f:
    full_data = pickle.load(f)

with open('app/static/data/country_index.pkl', 'rb') as f:
    country_index = pickle.load(f)

with open('app/static/data/lang_index.pkl', 'rb') as f:
    lang_index = pickle.load(f)
    
with open('app/static/data/time_index.pkl', 'rb') as f:
    time_index = pickle.load(f)

with open('app/static/data/category_index.pkl', 'rb') as f:
    category_index = pickle.load(f)
    
with open('app/static/data/view_rank.pkl', 'rb') as f:
    view_rank = pickle.load(f)
    
with open('app/static/data/category_view_rank.pkl', 'rb') as f:
    category_view_rank = pickle.load(f)

category_names = {  # 34 -> 23 when reading a record of video
    '1': 'Film & Animation',
    '2': 'Autos & Vehicles',
    '10': 'Music',
    '15': 'Pets & Animals',
    '17': 'Sports',
    '18': 'Short Movies',
    '19': 'Travel & Events',
    '20': 'Gaming',
    '21': 'Videoblogging',
    '22': 'People & Blogs',
    '23': 'Comedy',
    '24': 'Entertainment',
    '25': 'News & Politics',
    '26': 'Howto & Style',
    '27': 'Education',
    '28': 'Science & Technology',
    '29': 'Nonprofits & Activism',
    '30': 'Movies',
    '31': 'Anime/Animation',
    '32': 'Action/Adventure',
    '33': 'Classics',
    '34': 'Comedy',
    '35': 'Documentary',
    '36': 'Drama',
    '37': 'Family',
    '38': 'Foreign',
    '39': 'Horror',
    '40': 'Sci-Fi/Fantasy',
    '41': 'Thriller',
    '42': 'Shorts',
    '43': 'Shows',
    '44': 'Trailers'
}

app = Flask(__name__)
from app import views
