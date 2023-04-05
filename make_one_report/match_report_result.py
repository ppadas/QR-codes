import argparse
import json
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", required=True, type=str, help="Path to report file")
    parser.add_argument("-m", required=True, type=str, help="Path to markup file")
    parser.add_argument("-d", required=True, type=str, help="Path to dst match file")
    args = parser.parse_args()

    markup_path = args.m
    report_path = args.r
    dst_path = args.d

    match_results = dict()

    with open(markup_path, "r") as markup_file:
        markup = json.load(markup_file)
    
    with open(report_path, "r") as report_file:
        report = json.load(report_file)

    match_results["types_list"] = markup["types_list"]
    match_results["objects"] = []
    for result_value in report["objects"]:
        image_info = dict()
        image_info["image"] = result_value["image"]
        image_info["result"] = result_value["markup"]
        current_markup = None
        for markup_value in markup["objects"]:
            if image_info["image"] == markup_value["image"]:
                current_markup = markup_value
                break
        if current_markup == None:
            raise Exception("No markup for " + image_info["image"])
        else:
            image_info["markup"] = current_markup["markup"]
            match_results["objects"] .append(image_info)

    
    with open(dst_path, "w") as f:
        json.dump(match_results, f, indent=2)
