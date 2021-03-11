from app import *
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
        selected_index = selected_index.intersection(country_index[selected[1]])

    # filter by lang
    if selected[2] != 'all':
        selected_index = selected_index.intersection(lang_index[selected[2]])

    # classify by category
    selected_category = {x[0]: x[1] for x in ((i, selected_index.intersection(category_index[i])) for i in category_index) if len(x[1]) > 0}
    selected_category_count = {i: sum(full_data[x][11] for x in selected_category[i]) for i in selected_category}
    category_order = sorted(selected_category_count.keys())
    selected_category_top = {i: sorted(selected_category[i], key=lambda x: full_data[x][8], reverse=True)[:3] for i in selected_category}
    
    for c in selected_category_top:
        for i, v in enumerate(selected_category_top[c]):
            selected_category_top[c][i] = attr_for_homepage(full_data, v)
        ref_view_count = min(i['count'] for i in selected_category_top[c]) / 5
        for v in selected_category_top[c]:
            v['color_value'] = math.log(v['count'] / ref_view_count) / sum(math.log(i['count'] / ref_view_count) for i in selected_category_top[c])
            v['size_value'] = v['color_value'] * math.log(selected_category_count[c] / 10000)

    feed_data = [(category_names[str(i)], selected_category_top[i]) for i in category_order]
    
    if len(feed_data) == 0:
        return render_template('empty.html', selected=selected, message='No result')

    return render_template('index.html', selected=selected, feed_data=feed_data)

@app.route('/category', methods=['POST'])
def category_page():
    selected = [request.form['time'], request.form['country'], request.form['lang']]
    id = category_id[request.form['category']]

    video_selected = category_index[id]
    tag_selected = category_tag[id]

    # filter by time
    if selected[0] != 'all':
        video_selected = video_selected.intersection(time_index[selected[0]])
        tag_selected = tag_selected.intersection(time_tag[selected[0]])

    # filter by country
    if selected[1] != 'all':
        video_selected = video_selected.intersection(country_index[selected[1]])
        tag_selected = tag_selected.intersection(country_tag[selected[1]])

    # filter by lang
    if selected[2] != 'all':
        video_selected = video_selected.intersection(lang_index[selected[2]])
        tag_selected = tag_selected.intersection(lang_tag[selected[2]])

    # sort tags
    tag_view = {x: sum(full_data[i][8] for i in tag_index[x]) for x in tag_selected}
    tag_frequency = {x: len(tag_index[x]) for x in tag_selected}
    tag_sorted_view = sorted(tag_selected, key=lambda x: tag_view[x], reverse=True)
    tag_sorted_frequency = sorted(tag_selected, key=lambda x: tag_frequency[x], reverse=True)
    
    tag_num = len(tag_selected)
    
    # delete before submission
    ###
    if tag_num > 50000:
        tag_sorted_view = tag_sorted_view[:50000]
        tag_sorted_frequency = tag_sorted_frequency[:50000]

        tag_selected = set(tag_sorted_view).intersection(set(tag_sorted_frequency))

        tag_num = len(tag_selected)
        tag_rank = {t: [0, 0] for t in tag_selected}
    
        for i, t in enumerate(tag_sorted_view):
            if t in tag_rank:
                rank = math.ceil((i + 1) / 50000 * 10000) / 100
                tag_rank[t][0] = rank
        
        for i, t in enumerate(tag_sorted_frequency):
            if t in tag_rank:
                rank = math.ceil((i + 1) / 50000 * 10000) / 100
                tag_rank[t][1] = rank
    ####
    else:
        tag_rank = {t: [0, 0] for t in tag_selected}
        
        for i, t in enumerate(tag_sorted_view):
            if t in tag_rank:
                rank = math.ceil((i + 1) / tag_num * 10000) / 100
                tag_rank[t][0] = rank
        
        for i, t in enumerate(tag_sorted_frequency):
            if t in tag_rank:
                rank = math.ceil((i + 1) / tag_num * 10000) / 100
                tag_rank[t][1] = rank

    feed_data = [{(' '.join(t.split()), *tag_rank[t]) for t in tag_selected}]
    print(len(feed_data[0]))

    return render_template('category.html', selected=selected, category_name=request.form['category'], feed_data=feed_data)