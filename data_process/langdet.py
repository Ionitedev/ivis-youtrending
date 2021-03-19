import time
import logging

import pandas as pd
import pickle
from textblob import TextBlob 
from langdetect import detect, DetectorFactory, detect_langs
from google_trans_new import google_translator

DetectorFactory.seed = 0

def detect_text(text, tool='googletrans'):
    translator = google_translator()
    if tool=='textblob':
        lang = TextBlob(text).detect_language().lower()
    else:
        lang = translator.detect(text)[0]
    return lang

def load_state():
    # dict: {vid: [title, lang]}
    with open('./variables/langs.pickle', 'rb') as f:
        langs = pickle.load(f)
    return langs

def save_state(langs):
    with open('./variables/langs.pickle', 'wb') as f:
        # Save current results
        pickle.dump(langs, f, protocol=pickle.HIGHEST_PROTOCOL)

def get_count(lang_dict):
    # Counting request times to googletrans API
    count = 0
    for i in lang_dict:
        if not lang_dict[i][1] == 'unknown':
            count += 1
    return count

def get_lang_index(lang_dict):
    # Save language indices
    lang_idx = {}
    for vid in lang_dict:
        lang = lang_dict[vid][1] # language
        if not lang in lang_idx:
            lang_idx[lang] = []
        lang_idx[lang].append(vid)
    return lang_idx

def try_langdetect(lang_dict):
    # lang_ld = {}
    with open("./variables/langdetect.pickle", "rb") as f:
        # Save langdetect results in lang_ld
        lang_ld = pickle.load(f)

    regularLangs = ['ko','ru','fr','ja','es']    # langdetect seem to get accurate results for these languages
    langdetect_inaccurate = []
    langdetect_unable = []

    for vid in lang_dict:
        title = lang_dict[vid][0]
        lang = lang_dict[vid][1]
        if lang=='unknown' and (not vid in lang_ld):
            try:
                lang = detect(title)
                if not lang in regularLangs:
                    langdetect_inaccurate.append(vid)
                else:
                    # somehow more accurate, further check needed
                    lang_ld[vid] = [title, lang]
                    # lang_dict[vid] = [title, lang]  # write in lang_dict
            except:
                langdetect_unable.append(vid)
    
    with open('./variables/langdetect.pickle', 'wb') as f:
        # Save current results
        pickle.dump(lang_ld, f, protocol=pickle.HIGHEST_PROTOCOL)

    return lang_ld, langdetect_unable, langdetect_inaccurate

def detect_langs(lang_dict, tool):
    langs = load_state()    # restore all reliable results
    for vid in lang_dict:
        if vid in langs:
            lang_dict[vid] = langs[vid]
    
    allclear = True
    for vid in lang_dict:
        if lang_dict[vid][1]=='unknown':
            allclear = False
    if allclear: 
        print("0 undetected entry. detect_langs return.")
        return

    # load langdetect results
    lang_ld, langdetect_unable, langdetect_inaccurate = try_langdetect(lang_dict)
    # print(lang_ld)
    # print(langdetect_inaccurate)

    flag = True

    try:
        text = "C𝚊𝚕𝚕 𝚘𝚏 𝙳𝚞𝚝𝚢®: 𝙱𝚕𝚊𝚌𝚔 𝙾𝚙𝚜 𝙲𝚘𝚕𝚍 𝚆𝚊𝚛 - 𝚁𝚎𝚟𝚎𝚊𝚕 𝚃𝚛𝚊𝚒𝚕𝚎𝚛"
        lang = detect_text(text, tool)
    except:
        flag = False

    for vid in langdetect_unable:
        title = lang_dict[vid][0]
        lang = lang_dict[vid][1]
        if flag:
            try:
                lang = detect_text(title, tool)
        
                time.sleep(0.5)
                
                langs[vid] = [title, lang]
                lang_dict[vid][1] = lang
                save_state(langs)

                print("======== {} detected, {} entries left ==========".format(get_count(lang_dict), len(lang_dict)-get_count(lang_dict)))     
                print("Title: {}".format(title))
                print("{}: {}".format(tool, lang))
            except:
                if len(title) < 3:
                    print('TextBlob requires at least 3 character! Input language manually.')
                    print('Video ID :{}, Title: "{}"'.format(vid, title))
                    lang = input()
                    print('Language {}, {} entries left'.format(lang, len(langs)-get_count(langs)))
                    langs[vid] = [title, lang]
                    lang_dict[vid][1] = lang
            
                    save_state(langs)
                    
                    # lang_manual[vid] = [title, 'unknown']
                    # with open('./variables/textblobfail.pickle','wb') as file:
                    #     pickle.dump(lang_manual, file, protocol=pickle.HIGHEST_PROTOCOL)
                else:
                    # lang_manual[vid] = [title, 'unknown']
                    print("First section. Translator failed. Too many request.")
                    # raise
                    flag = False
                    raise

    for vid in langdetect_inaccurate:    
        title = lang_dict[vid][0]
        lang = lang_dict[vid][1]
        if flag:
            try:
                lang = detect_text(title, tool)
        
                time.sleep(0.5)
                
                langs[vid] = [title, lang]
                lang_dict[vid][1] = lang
                save_state(langs)

                print("======== {} detected, {} entries left ==========".format(get_count(lang_dict), len(lang_dict)-get_count(lang_dict)))     
                print("Title: {}".format(title))
                print("{}: {}".format(tool, lang))
            except:
                if len(title) < 3:
                    print('TextBlob requires at least 3 character! Input language manually.')
                    print('Video ID :{}, Title: "{}"'.format(vid, title))
                    lang = input()
                    print('Language {}, {} entries left'.format(lang, len(langs)-get_count(langs)))
                    langs[vid] = [title, lang]
                    lang_dict[vid][1] = lang
            
                    save_state(langs)
                    
                    # lang_manual[vid] = [title, 'unknown']
                    # with open('./variables/textblobfail.pickle','wb') as file:
                    #     pickle.dump(lang_manual, file, protocol=pickle.HIGHEST_PROTOCOL)
                else:
                    # lang_manual[vid] = [title, 'unknown']
                    print("Second section. TextBlob failed. Too many requests.")
                    flag = False
                    raise
    
    # modify langdetect results
    for vid in lang_dict:
        title = lang_dict[vid][0]
        lang = lang_dict[vid][1]
        if flag and lang=='unknown':
            try:
                lang = detect_text(title, tool)
        
                time.sleep(0.5)
                
                lang_dict[vid][1] = lang
                langs[vid] = [title, lang]
                save_state(langs)

                print("======== {} detected, {} entries left ==========".format(get_count(lang_dict), len(lang_dict)-get_count(lang_dict)))     
                print("Title: {}".format(title))
                print("{}: {}".format(tool, lang))
            except:
                if len(title) < 3:
                    print('TextBlob requires at least 3 character! Input language manually.')
                    print('Video ID :{}, Title: "{}"'.format(vid, title))
                    lang = input()
                    print('Language {}, {} entries left'.format(lang, len(langs)-get_count(langs)))
                    lang_dict[vid][1] = lang

                    langs[vid][1] = lang            
                    save_state(langs)
                    
                    # lang_manual[vid] = [title, 'unknown']
                    # with open('./variables/textblobfail.pickle','wb') as file:
                    #     pickle.dump(lang_manual, file, protocol=pickle.HIGHEST_PROTOCOL)
                else:
                    # lang_manual[vid] = [title, 'unknown']
                    print("Third section. TextBlob failed. Too many requests.-------Turning into langdetect.")
                    flag = False
        elif (not flag) and lang=='unknown':
            # use langdetect results if textblob is limited
            lang_dict[vid] = lang_ld[vid]
    
    # return lang_dict

def run_detect(tool='googletrans'):
    all_data = pd.read_csv("./csv/youtrend_merged_3m.csv")
    # concatenated data among all countries, language set to unknown
    # latest data
    data_lang = all_data[['video_id', 'title', 'lang']]
    data_lang = data_lang.set_index('video_id').T.to_dict('list')   

    detect_langs(data_lang, tool)
    return data_lang

# run_detect()
    
        
    



            
