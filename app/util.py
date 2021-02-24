import datetime

def attr_for_homepage(full_data, id):
    res = dict()
    res['title'] = full_data[id][4]
    res['channel'] = full_data[id][6]
    res['count'] = int(full_data[id][11])
    res['pubdate'] = str(full_data[id][5].date())
    res['trenddate1'] = str(full_data[id][7][0].date())
    res['trenddate2'] = str(full_data[id][7][-1].date())
    res['cover_url'] = full_data[id][15]
    return res