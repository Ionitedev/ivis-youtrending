# import logging
import time

import pandas as pd
import pickle

from dateutil.parser import isoparse
from datetime import datetime, timedelta

from langdet import *

def merge_countries():
    # br
    br_data = pd.read_csv("./csv/BR_youtube_trending_data.csv", encoding="utf-8")
    br_data.insert(0, "country", "br")
    # ca
    ca_data = pd.read_csv("./csv/CA_youtube_trending_data.csv")
    ca_data.insert(0, "country", "ca")
    # de
    de_data = pd.read_csv("./csv/DE_youtube_trending_data.csv")
    de_data.insert(0, "country", "de")
    # fr
    fr_data = pd.read_csv("./csv/FR_youtube_trending_data.csv")
    fr_data.insert(0, "country", "fr")
    # gb
    gb_data = pd.read_csv("./csv/GB_youtube_trending_data.csv")
    gb_data.insert(0, "country", "gb")
    # in
    in_data = pd.read_csv("./csv/IN_youtube_trending_data.csv")
    in_data.insert(0, "country", "in")
    # jp
    jp_data = pd.read_csv("./csv/JP_youtube_trending_data.csv")
    jp_data.insert(0, "country","jp")
    # kr
    kr_data = pd.read_csv("./csv/KR_youtube_trending_data.csv")
    kr_data.insert(0, "country", "kr")
    # mx
    mx_data = pd.read_csv("./csv/MX_youtube_trending_data.csv")
    mx_data.insert(0, "country", "mx")
    # ru
    ru_data = pd.read_csv("./csv/RU_youtube_trending_data.csv")
    ru_data.insert(0, "country", "ru")
    # us
    us_data = pd.read_csv("./csv/US_youtube_trending_data.csv")
    us_data.insert(0, "country", "us")

    all_frames = [br_data, ca_data, de_data, fr_data, gb_data, in_data, jp_data, kr_data, mx_data, ru_data, us_data]
    all_data = pd.concat(all_frames).reset_index(drop=True) # concat and reset index

    # drop some attributes, add "lang"
    all_data = all_data.drop(columns = ["description", "channelId", "ratings_disabled", "comments_disabled"])
    all_data.insert(0, "lang", "unknown")    

    # Parse dates
    # publishing date
    for idx in range(all_data.shape[0]):
        pub_date = all_data['publishedAt'][idx]
        all_data.at[idx, 'publishedAt'] = isoparse(pub_date)
    # trending date
    for idx in range(all_data.shape[0]):
        trend_date = all_data['trending_date'][idx]
        all_data.at[idx, 'trending_date'] = isoparse(trend_date)

    return all_data

######################################################################################
# main
def main():
    all_data = merge_countries()

    trending_dates = all_data.trending_date.unique()    # numpy.ndarray
    latest_date = max(trending_dates)
    starting_date = latest_date - timedelta(days=90)    # three months ago
    all_data = all_data.drop(all_data[all_data.trending_date < starting_date].index).reset_index(drop=True)
    all_data.to_csv("./csv/youtrend_merged_3m.csv",quoting=1,index=0,encoding="utf-8")
    print("==========Data within three months saved.===========")

    # Update language detection results in the csv file
    langs = run_detect(tool='googletrans')
    # with open("./variables/langs.pickle", "rb") as f:
    #     langs = pickle.load(f)
    for i in range(all_data.shape[0]):
        vid = all_data['video_id'][i]
        all_data.at[i, 'lang'] = langs[vid][1]
    all_data.to_csv("./csv/youtrend_merged_3m.csv",quoting=1,index=0,encoding="utf-8")
    print("==========Language detected.===========")

    # build index
    # tags: string to set

    tags_col = all_data['tags'].str.split('|')
    tags = []
    for tag_list in tags_col:
        tags.append(set(tag_list))
    data_new = all_data.drop(['tags'], axis=1)
    data_new.insert(7, 'tags', tags)

    # merge trending dates
    video_trends = {}
    for idx in range(data_new.shape[0]):
        vid = data_new['video_id'][idx]
        country = data_new['country'][idx]
        date = data_new['trending_date'][idx]
        # key = (country, vid)
        key = vid
        if not key in video_trends:
            video_trends[key] = []
        video_trends[key].append(date)

    data_new.insert(9, 'tuple_trending_dates', '')
    for idx in range(data_new.shape[0]):
        vid = data_new['video_id'][idx]
        country = data_new['country'][idx]
        # key = (country, vid)
        key = vid
        data_new.at[idx, 'tuple_trending_dates'] = video_trends[key]

    columns = data_new.columns
    attr = columns.tolist()
    del attr[2]
    del attr[-6]
    alist = list(range(len(attr)))
    attr = dict(zip(alist, attr))
    with open('./index/attributes.pickle','wb') as f:
        pickle.dump(attr, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(attr)

    # country index
    # keys: 'gb', 'mx', 'fr', 'ru', 'kr', 'us', 'in', 'jp', 'br', 'ca', 'de'
    country_idx = {}
    for _, row in data_new.iterrows():
        #print(c)
        c = row['country']
        vid = row['video_id']
        if not c in country_idx:
            country_idx[c] = set()
        country_idx[c].add(vid)
    with open('./index/country_index.pkl', 'wb') as file:
        pickle.dump(country_idx, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    yt_dict = data_new.set_index('video_id').T.to_dict('list')
    # print(yt_dict['dA2gaw0-Ar4'])

    # Category index
    # keys: 23, 10, 24, 2, 26, 22, 17, 20, 27, 25, 28, 19, 15, 1, 29
    category_idx = {}
    for vid in yt_dict:
        ctid = yt_dict[vid][5] # category ID
        if not ctid in category_idx:
            category_idx[ctid] = set()
        category_idx[ctid].add(vid)
    with open('./index/category_index.pkl', 'wb') as file:
        pickle.dump(category_idx, file, protocol=pickle.HIGHEST_PROTOCOL)

    # Language index
    lang_idx = {}
    for vid in yt_dict:
        lg = yt_dict[vid][0] # language
        if not lg in lang_idx:
            lang_idx[lg] = set()
        lang_idx[lg].add(vid)
    with open('./index/lang_index.pkl', 'wb') as file:
        pickle.dump(lang_idx, file, protocol=pickle.HIGHEST_PROTOCOL)

    # Trending index
    trending_1w = set()
    trending_2w = set()
    trending_1m = set()
    for vid in yt_dict:
        if latest_date < yt_dict[vid][7]:
            raise ValueError('Please update the latest trending date!')
        time = latest_date - yt_dict[vid][7]
        if time <= timedelta(days=6):
            trending_1w.add(vid)
        if time <= timedelta(days=13):
            trending_2w.add(vid)
        if time <= timedelta(days=30):
            trending_1m.add(vid)
        
    trending_idx = {'1w': trending_1w, '2w': trending_2w, '1m': trending_1m}
    with open('./index/time_index.pkl', 'wb') as file:
        pickle.dump(trending_idx, file, protocol=pickle.HIGHEST_PROTOCOL)

    # save data in pickle
    data = data_new.drop(['trending_date'],axis=1)
    data.to_csv("./csv/youtrend_merged_3m.csv",quoting=1,index=0,encoding="utf-8")
    yout = data.set_index('video_id').T.to_dict('list')
    # yout = {key=video_id: value=(a tuple of attributes)}

    for key in yout:
        yout[key] = tuple(yout[key])

    with open("./index/full_data.pkl","wb") as f:
        pickle.dump(yout, f)

main()