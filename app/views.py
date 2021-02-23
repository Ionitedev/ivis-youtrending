from app import app, full_data, country_index, lang_index, time_index, category_index, view_rank, category_view_rank, category_names
from flask import render_template, request, session, redirect
from functools import reduce

@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'GET':
        selected = ['all', 'all', 'all']
    else:
        selected = [request.form['time'], request.form['country'], request.form['lang']]
        
    selected_index = set(full_data.keys())
    try:
        # filter by time
        if selected[0] != 'all':
            selected_index = selected_index.intersection(time_index[selected[0]])

        # filter by country
        if selected[1] != 'all':
            selected_index = selected_index.intersection(country_index[selected[1]])

        # filter by lang
        if selected[2] != 'all':
            selected_index = selected_index.intersection(lang_index[selected[2]])

        # classify by category
        selected_category = [x for x in ((i, selected_index.intersection(category_index[i])) for i in sorted(category_index.keys())) if len(x[1]) > 0]
        selected_category_top = {i[0]: sorted(i[1], key=category_view_rank[i[0]].index, reverse=True)[:3] for i in selected_category}
    except Exception:
        pass
        
    return render_template('index.html', selected=selected)

@app.route('/category', methods=['POST'])
def category_page():
    selected = [request.form['time'], request.form['country'], request.form['lang']]
    return render_template('index.html', selected=selected)