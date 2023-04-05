#to do статистика по конкретному типу

from estimate_encoding import encoding_stat

import argparse
import json
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", required=True, type=str, help="Src file with matched report and markup")
    parser.add_argument("-s", required=True, type=str, help="Path to stat file")
    args = parser.parse_args()

    result_path = args.r
    stat_path = args.s
    
    common_stat = dict()
    common_stat["objects"] = []

    with open(result_path, "r") as f:
        data = json.load(f)

    for object_info in data["objects"]:
        current_object_stat = dict()
        current_object_stat["image"] = object_info["image"]
        current_object_stat["decoded"] = encoding_stat(object_info)

        common_stat["objects"].append(current_object_stat)

    with open(stat_path, "w") as f:
        json.dump(common_stat, f, indent=2)
