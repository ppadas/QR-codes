#to do статистика по конкретному типу

from estimate_encoding import encoding_stat
from estimate_bbox import bbox_stat
from match_boxes import match_bboxes

import argparse
import json
import os

def make_match_result(indexed_markup, indexed_result, match_values, 
    no_match_markup, no_match_result):

    current_match = dict()
    current_match["image"] = object_info["image"]
    current_match["matched"] = []
    current_match["no_match_result"] = []
    current_match["no_match_markup"] = []

    for matched_pair in match_values:
        pair = dict()
        pair["markup"] = indexed_markup[matched_pair[0]]
        pair["result"] = indexed_result[matched_pair[1]]
        current_match["matched"].append(pair)

    for markup_id in no_match_markup:
        current_match["no_match_markup"].append(indexed_markup[markup_id])
    for result_id in no_match_result:
        current_match["no_match_result"].append(indexed_result[result_id])

    return current_match



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", required=True, type=str, help="Src file with matched report and markup")
    parser.add_argument("-s", required=True, type=str, help="Path to stat file")
    parser.add_argument("-m", required=True, type=str, help="Path to match file")
    args = parser.parse_args()

    result_path = args.r
    stat_path = args.s
    match_path = args.m
    
    common_stat = dict()
    common_stat["objects"] = []

    common_match = dict()
    common_match["objects"] = []

    with open(result_path, "r") as f:
        data = json.load(f)

    for object_info in data["objects"]:
        current_object_stat = dict()
        current_object_stat["image"] = object_info["image"]

        indexed_markup, indexed_result, match_values, no_match_markup, no_match_result = \
            match_bboxes(object_info)
        
        current_match = make_match_result(indexed_markup, indexed_result, 
            match_values, no_match_markup, no_match_result)
        common_match["objects"].append(current_match)

        #current_object_stat["decoded"] = encoding_stat(object_info)
        current_object_stat["bbox_stat"] = bbox_stat(object_info)
        common_stat["objects"].append(current_object_stat)

    with open(stat_path, "w") as f:
        json.dump(common_stat, f, indent=2)
    
    with open(match_path, "w") as f:
        json.dump(common_match, f, indent=2)

