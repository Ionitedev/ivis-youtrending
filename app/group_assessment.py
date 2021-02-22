from app import csv_data
import re

def assessment(p_id, a_id=[i for i in range(12, 24)]):
    # p_id: a list of indexes of student names
    # a_id: a list of indexes of attributes 
    
    # quantitative data
    radar = {}

    if 12 in a_id:
        radar["Information Visualization"] = max([csv_data[student_id][12] for student_id in p_id])
        # radar["Information Visualization"] = stats.mode([csv_data[student_id][12] for student_id in p_id])[0][0]
    if 13 in a_id:
        radar["Statistical"] = max([csv_data[student_id][13] for student_id in p_id])
    if 14 in a_id:
        radar["Mathematics"] = max([csv_data[student_id][14] for student_id in p_id])
    if 15 in a_id:
        radar["Drawing and Artistic"] = max([csv_data[student_id][15] for student_id in p_id])
    if 16 in a_id:
        radar["Computer Usage"] = max([csv_data[student_id][16] for student_id in p_id])
    if 17 in a_id:
        radar["Programming"] = max([csv_data[student_id][17] for student_id in p_id])
        # radar["Programming"] = stats.mode([csv_data[student_id][17] for student_id in p_id])[0][0]
    if 18 in a_id:
        radar["Computer Graphics"] = max([csv_data[student_id][18] for student_id in p_id])
    if 19 in a_id:
        radar["Human-Computer Interaction"] = max([csv_data[student_id][19] for student_id in p_id])
    if 20 in a_id:
        radar["User Experience Evaluation"] = max([csv_data[student_id][20] for student_id in p_id])
    if 21 in a_id:
        radar["Communication"] = round(sum([int(csv_data[student_id][21]) for student_id in p_id]) / len(p_id), 0) # or mode, min
    if 22 in a_id:
        radar["Collaboration"] = round(sum([int(csv_data[student_id][22]) for student_id in p_id]) / len(p_id), 0) # or mode, min
    if 23 in a_id:
        radar["Code Repository"] = max([csv_data[student_id][23] for student_id in p_id])
        # radar["Code Repository"] = stats.mode([csv_data[student_id][23] for student_id in p_id])[0][0]

    # qualitative data
    # Social media platform: KTH social or KTH Canvas or Facebook?
    # a naive version...

    # yes_count = [0] * 3
    # no_count = [0] * 3
    # for i in range(3):
    #     for student_id in p_id:
    #         if(csv_data[student_id][8+i][0] == 'Y'):
    #             yes_count[i] += 1
    #         elif(csv_data[student_id][8+i][0] == 'N'):
    #             no_count[i] += 1
    # scp_id = yes_count.index(max(yes_count))
    # if(scp_id == 0): scp_choice = "Recommended social media platform is: KTH Canvas"
    # elif(scp_id == 1): scp_choice = "Recommended social media platform is: KTH Social"
    # else: scp_choice = "Recommended social media platform is: Facebook"
    def word_split(ans):

        import re
        return re.split(r'[,. -]+', ans)

    def naive_scp(p_id):

        yn_count = {"KTH Canvas": [0,0], "KTH Social": [0,0], "Facebook": [0,0]}
        for student_id in p_id:
            if(csv_data[student_id][8][0] == 'Y'):
                yn_count["KTH Canvas"][0] += 1
            elif(csv_data[student_id][8][0] == 'N'):
                yn_count["KTH Canvas"][1] += 1
            if(csv_data[student_id][9][0] == 'Y'):
                yn_count["KTH Social"][0] += 1
            elif(csv_data[student_id][9][0] == 'N'):
                yn_count["KTH Social"][1] += 1
            if(csv_data[student_id][10][0] == 'Y'):
                yn_count["Facebook"][0] += 1
            elif(csv_data[student_id][10][0] == 'N'):
                yn_count["Facebook"][1] += 1
        # tend to choose the platform with most users within the selected group
        sorted_scp = sorted(yn_count.keys(), key=yn_count.get, reverse=True)
        # an ordered list of recommended communication platforms
        return sorted_scp

    def scp_recommend(p_id):

        availability = {"KTH Canvas": 0, "KTH Social": 0, "Facebook": 0}
        # use weighted score for each answer
        # Canvas
        for student_id in p_id:
            if 'never' in word_split(csv_data[student_id][8]):
                del availability["KTH Canvas"]
                break
            if "KTH Canvas" in availability:
                if 'day' in word_split(csv_data[student_id][8]):
                    availability["KTH Canvas"] += 3
                elif 'week' in word_split(csv_data[student_id][8]) or 'weeks' in word_split(csv_data[student_id][8]):
                    availability["KTH Canvas"] += 2
                elif 'mind' in word_split(csv_data[student_id][8]):
                    availability["KTH Canvas"] += 1
        # KTH Social
        for student_id in p_id:
            if 'never' in word_split(csv_data[student_id][9]):
                del availability["KTH Social"]
                break
            if "KTH Social" in availability:
                if 'day' in word_split(csv_data[student_id][9]):
                    availability["KTH Social"] += 3
                elif 'week' in word_split(csv_data[student_id][9]) or 'weeks' in word_split(csv_data[student_id][9]):
                    availability["KTH Social"] += 2
                elif 'mind' in word_split(csv_data[student_id][9]):
                    availability["KTH Social"] += 1
        # FB
        for student_id in p_id:
            if 'never' in word_split(csv_data[student_id][10]):
                del availability["Facebook"]
                break
            if "Facebook" in availability:
                if 'day' in word_split(csv_data[student_id][10]):
                    availability["Facebook"] += 3
                elif 'week' in word_split(csv_data[student_id][10]) or 'weeks' in word_split(csv_data[student_id][10]):
                    availability["Facebook"] += 2
                elif 'mind' in word_split(csv_data[student_id][10]):
                    availability["Facebook"] += 1
        # an ordered list of available social media platforms
        return availability        
    
    scp = scp_recommend(p_id)

    return radar, scp