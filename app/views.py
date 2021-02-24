from app import app, full_data, country_index, lang_index, time_index, category_index, view_rank, category_view_rank, category_names
from app.util import attr_for_homepage
from flask import render_template, request, session, redirect
from functools import reduce
import math

@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'GET':
        selected = ['all', 'all', 'all']
    else:
        selected = [request.form['time'], request.form['country'], request.form['lang']]
        
    selected_index = set(full_data.keys())

    # filter by time
    if selected[0] != 'all':
        selected_index = selected_index.intersection(time_index[selected[0]])

    # filter by country
    if selected[1] != 'all':
        selected_index = selected_index.intersection(country_index[selected[1].upper()])

    # filter by lang
    if selected[2] != 'all':
        selected_index = selected_index.intersection(lang_index[selected[2]])

    # classify by category
    selected_category = {x[0]: x[1] for x in ((i, selected_index.intersection(category_index[i])) for i in category_index) if len(x[1]) > 0}
    selected_category_count = {i: sum(full_data[x][11] for x in selected_category[i]) for i in selected_category}
    category_order = sorted(selected_category_count.keys())
    selected_category_top = {i: sorted(selected_category[i], key=lambda x: full_data[x][11], reverse=True)[:3] for i in selected_category}
    
    for c in selected_category_top:
        for i, v in enumerate(selected_category_top[c]):
            selected_category_top[c][i] = attr_for_homepage(full_data, v)
        for v in selected_category_top[c]:
            v['color_value'] = math.log(v['count']) / sum(math.log(i['count']) for i in selected_category_top[c])
            v['size_value'] = v['color_value'] *  math.log(selected_category_count[c])

    feed_data = [(category_names[str(i)], selected_category_top[i]) for i in category_order]
    
    if len(feed_data) == 0:
        return render_template('empty.html', selected=selected, message='No result')

    return render_template('index.html', selected=selected, feed_data=feed_data)

@app.route('/category', methods=['POST'])
def category_page():
    selected = [request.form['time'], request.form['country'], request.form['lang']]
    message = 'To be completed. Category: ' + request.form['category']
    return render_template('empty.html', selected=selected, message=message)