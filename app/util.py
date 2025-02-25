import datetime

# 0: 'lang', 1: 'country', 2: 'title', 3: 'publishedAt', 4: 'channelTitle',
# 5: 'categoryId', 6: 'tags', 7: 'tuple_trending_dates', 8: 'view_count',
# 9: 'likes', 10: 'dislikes', 11: 'comment_count', 12: 'thumbnail_link'

def long_num(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'G'][magnitude]) if magnitude > 0 else str(num)

def rank_map(counters, reverse=False):
    values = sorted(set(counters.values()), reverse=reverse)
    value_counter = {v: 0 for v in values}
    for i in counters:
        value_counter[counters[i]] += 1

    for i in range(1, len(values)):
        value_counter[values[i]] += value_counter[values[i - 1]]

    return value_counter

def attr_for_homepage(full_data, id):
    res = dict()
    res['title'] = full_data[id][2]
    res['url'] = 'https://www.youtube.com/watch?v=' + id
    res['channel'] = full_data[id][4]
    res['count'] = int(full_data[id][8])
    res['count_long_num'] = long_num(int(full_data[id][8]))
    res['pubdate'] = str(full_data[id][3].date())
    res['trenddate1'] = str(full_data[id][7][0].date())
    res['trenddate2'] = str(full_data[id][7][-1].date())
    res['cover_url'] = full_data[id][12]
    res['days'] = (datetime.date(2021, 3, 9) - full_data[id][7][-1].date()).days
    return res

def attr_for_taglist(full_data, id, tagset):
    res = dict()
    res['title'] = full_data[id][2]
    res['url'] = 'https://www.youtube.com/watch?v=' + id
    res['tags'] = set(full_data[id][6]).intersection(tagset)
    if len(res['tags']) == 0:
        res['tags'] = list(full_data[id][6])[:2]
    res['tags'] = '|'.join(list(res['tags']))
    res['cover_url'] = full_data[id][12]
    return res