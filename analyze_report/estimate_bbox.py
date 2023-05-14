import copy

threshold_in_ration = 0.01
threshold_out_ration = 0.1

def bbox_stat(object_info):
    '''
    Документацию нужно смотреть в документе
    https://docs.google.com/document/d/1u4_jnB_Wm2VkAfSPwoEg0FPKNoaCh15_/edit#
    '''

    if "image" not in object_info or \
       "result" not in object_info or \
       "markup" not in object_info:
        raise Exception("Report object error")

    stat_info = []
    indexed_markup = dict()
    indexed_result = dict()
    i = 0
    for markup_value in object_info["markup"]:
        indexed_markup[i] = markup_value
        i += 1
    
    i = 0
    for result_value in object_info["result"]:
        indexed_result[i] = result_value
        i += 1

    match_values = []
    no_match_markup = []
    no_match_result = []

    # match
    # что если один result смэтчился с неколькими
    for markup_key, markup_value in indexed_markup.items():
        current_match_result = -1
        max_intersection = 0
        bbox_markup = markup_value["bbox"]

        for result_key, result_value in indexed_result.items():
            bbox_result = result_value["bbox"]
            current_intersection = compute_intersection(bbox_result, bbox_markup)
            if current_intersection > max_intersection:
                max_intersection = current_intersection
                current_match_result = result_key
        
        if current_match_result != -1:
            match_values.append([markup_key, current_match_result])
        else:
            no_match_markup.append(markup_key)
    
    for result_key, result_value in indexed_result.items():
        matched = False
        for matched_pair in match_values:
            if result_key == matched_pair[1]:
                matched = True
                break
        if not matched:
            no_match_result.append(result_key)
    
    process_matched_values(match_values, indexed_markup, indexed_result, stat_info)
    process_true_FN_values(no_match_markup, indexed_markup, stat_info)
    process_true_FP_values(no_match_result, indexed_result, stat_info)
    return stat_info



def compute_max_in_out_offset(box_result, box_markup):
    left_offset = box_result[0] - box_markup[0]
    right_offset = box_result[0] + box_result[2] - (box_markup[0] + box_markup[2])
    top_offset = box_result[1] - box_markup[1]
    bottom_offset = box_result[1] + box_result[3] - (box_markup[1] + box_markup[3])
    max_in = max(0, left_offset, -right_offset, top_offset, -bottom_offset) / \
        min(box_markup[2], box_markup[3])
    max_out = max(0, -left_offset, right_offset, -top_offset, bottom_offset) / \
        min(box_markup[2], box_markup[3])
    return max_in, max_out


def compute_intersection(box_1, box_2):
    x_left = max(box_1[0], box_2[0])
    x_right = min(box_1[0] + box_1[2], box_2[0] + box_2[2])
    y_top = max(box_1[1], box_2[1])
    y_bottom = min(box_1[1] + box_1[3], box_2[1] + box_2[3])

    if x_left > x_right or y_top > y_bottom:
        return 0
    else:
        return (x_right - x_left) * (y_bottom - y_top)

def compute_union(box_1, box_2):
    intersection = compute_intersection(box_1, box_2)
    return box_1[2] * box_1[3] + box_2[2] * box_2[3] - intersection

def process_matched_values(match_values, indexed_markup, indexed_result, stat_info):
    for match_value in match_values:
        if indexed_markup[match_value[0]]["type"] == 2: #atypical
            current_stat = dict()
            current_stat["error_type"] = "Not consider"
            stat_info.append(current_stat)
            return
        current_stat = dict()
        current_stat["error_type"] = "TP"
        markup = indexed_markup[match_value[0]]
        result = indexed_result[match_value[1]]
        max_in, max_out = compute_max_in_out_offset(result["bbox"], markup["bbox"])
        intersection = compute_intersection(result["bbox"], markup["bbox"])
        union = compute_union(result["bbox"], markup["bbox"])
        current_stat["markup_type"] = markup["type"]
        current_stat["max_in"] = max_in
        current_stat["max_out"] = max_out
        current_stat["intersection_area"] = intersection
        current_stat["union_area"] = union
        if markup["type"] != result["type"] or \
          current_stat["max_in"] > threshold_in_ration or \
          current_stat["max_out"] > threshold_out_ration:
            current_stat["error_type"] = "FP"
            current_stat["found_type"] = result["type"]
            current_stat["bbox_markup_area"] = markup["bbox"][2] * markup["bbox"][3]
            current_stat["bbox_markup_area"] = result["bbox"][2] * result["bbox"][3]
        stat_info.append(current_stat)

def process_true_FN_values(no_match_markup, indexed_markup, stat_info):
    for value in no_match_markup:
        markup = indexed_markup[value]
        if markup["type"] == 2:
            current_stat = dict()
            current_stat["error_type"] = "Not consider"
            stat_info.append(current_stat)
            return
        current_stat["error_type"] = "FN"
        current_stat = dict()
        current_stat["error_type"] = "FN"
        current_stat["markup_type"] = markup["type"]
        current_stat["bbox_markup_area"] = markup["bbox"][2] * markup["bbox"][3]
        stat_info.append(current_stat)
    
def process_true_FP_values(no_match_result, indexed_result, stat_info):
    for value in no_match_result:
        result = indexed_result[value]
        current_stat = dict()
        current_stat["error_type"] = "FP"
        current_stat["found_type"] = result["type"]
        current_stat["bbox_found_area"] = result["bbox"][2] * result["bbox"][3]
        stat_info.append(current_stat)
