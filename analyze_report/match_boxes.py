

def match_bboxes(object_info):

    if "image" not in object_info or \
       "result" not in object_info or \
       "markup" not in object_info:
        raise Exception("Report object error")

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
    
    return indexed_markup, indexed_result, match_values, no_match_markup, no_match_result

def compute_intersection(box_1, box_2):
    x_left = max(box_1[0], box_2[0])
    x_right = min(box_1[0] + box_1[2], box_2[0] + box_2[2])
    y_top = max(box_1[1], box_2[1])
    y_bottom = min(box_1[1] + box_1[3], box_2[1] + box_2[3])

    if x_left > x_right or y_top > y_bottom:
        return 0
    else:
        return (x_right - x_left) * (y_bottom - y_top)