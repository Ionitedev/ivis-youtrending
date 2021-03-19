from app import *
from app.util import *
from flask import render_template, request, session, redirect
from functools import reduce
import math

@app.route('/', methods=['GET', 'POST'])
def index_page():
    if request.method == 'GET':
        selected = ['all', 'all', 'all', '8']
    else:
        selected = [request.form['time'], request.form['country'], request.form['lang'], request.form['numtop']]
        
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
    selected_category_count = {i: sum(full_data[x][8] for x in selected_category[i]) for i in selected_category}
    category_order = sorted(selected_category_count.keys(), key=lambda x:selected_category_count[x], reverse=True)
    selected_category_top = {i: sorted(selected_category[i], key=lambda x: full_data[x][8], reverse=True)[:int(selected[3])] for i in selected_category}

    if len(selected_category_top) == 0:
        return render_template('empty.html', selected=selected, message='No result')

    for c in selected_category_top:
        for i, v in enumerate(selected_category_top[c]):
            selected_category_top[c][i] = attr_for_homepage(full_data, v)
        
        ref_view_count = min(i['count'] for i in selected_category_top[c])
        for v in selected_category_top[c]:
            v['color_value'] = 1.01 - v['days'] / {'1w': 7, '2w': 14, '1m': 30, 'all': 90}[selected[0]]
            v['size_value'] = (v['count'] / ref_view_count) / sum((i['count'] / ref_view_count) for i in selected_category_top[c]) * math.log(selected_category_count[c] / 10000)

        ref_color = max(v['color_value'] for v in selected_category_top[c])
        for v in selected_category_top[c]:
            v['color_value'] /= ref_color

    total_size = sum(v['size_value'] for v in selected_category_top[c] for c in selected_category_top)
    for c in selected_category_top:
        for v in selected_category_top[c]:
            v['show_title'] = 1 if v['size_value'] / total_size > 0.004 else 0

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
    tag_selected.discard('[None]')

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

    tag_selected = {t for t in tag_selected if len(video_selected.intersection(tag_index[t])) > 0}
    
    # sort tags
    tag_view = {x: sum(full_data[i][8] for i in tag_index[x].intersection(video_selected)) for x in tag_selected}
    tag_frequency = {x: len(tag_index[x].intersection(video_selected)) for x in tag_selected}
    tag_sorted_view = sorted(tag_selected, key=lambda x: tag_view[x], reverse=True)
    tag_sorted_frequency = sorted(tag_selected, key=lambda x: tag_frequency[x], reverse=True)
    rank_map_view = rank_map(tag_view, reverse=True)
    rank_map_frequency = rank_map(tag_frequency, reverse=True)
    tag_num = len(tag_selected)
    
    tag_rank = {t: [0, 0] for t in tag_selected}
    
    for t in tag_selected:
        tag_rank[t] = [math.ceil((rank_map_view[tag_view[t]]) / tag_num * 10000) / 100, math.ceil((rank_map_frequency[tag_frequency[t]]) / tag_num * 10000) / 100 ]
    
    feed_data = [0] * 4
    # feed_data: [tag, tag search, tag search top, video search top]

    search = request.form.get('search', '')
    
    if len(search) == 0:
        feed_data[0] = {(' '.join(t.split()), *tag_rank[t], tag_view[t], tag_frequency[t]) for t in tag_selected}
        feed_data[1] = set()
        feed_data[2] = tag_sorted_view[:10]
        top_video = list(sorted(set(reduce(lambda x, y: x.union(tag_index[y]), tag_sorted_view[:100], set())).intersection(video_selected), key=lambda x: full_data[x][8], reverse=True))[:10]
        feed_data[3] = [attr_for_taglist(full_data, i, set(feed_data[2])) for i in top_video]
    else:
        tag_search = {i for i in tag_selected if i.startswith(search)}
        tag_not_search = tag_selected.difference(tag_search)
        feed_data[0] = {(' '.join(t.split()), *tag_rank[t], long_num(tag_view[t]), long_num(tag_frequency[t])) for t in tag_not_search}
        feed_data[1] = {(' '.join(t.split()), *tag_rank[t], long_num(tag_view[t]), long_num(tag_frequency[t])) for t in tag_search}
        feed_data[2] = list(sorted(tag_search, key=tag_rank.get))[:10]
        top_video = list(sorted(set(reduce(lambda x, y: x.union(tag_index[y]), list(tag_search)[:100], set())).intersection(video_selected), key=lambda x: full_data[x][8], reverse=True))[:10]
        feed_data[3] = [attr_for_taglist(full_data, i, set(feed_data[2])) for i in top_video]

    return render_template('category.html', selected=selected, category_name=request.form['category'], search=search, feed_data=feed_data)

@app.route('/info', methods=['GET'])
def info_page():
    return redirect('https://sites.google.com/view/youtrend-info')
