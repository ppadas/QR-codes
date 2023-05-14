import argparse
import json
import os

threshold_in_ration = 0.01
threshold_out_ration = 0.1

def getPerType(data, type_to_save):
    names = set()
    for image_item in data["objects"]:
        for bbox in image_item["bbox_stat"]:
            if bbox["error_type"] == type_to_save:
                names.add(image_item["image"])
    return list(names)

def getPureFP(data):
    names = set()
    for image_item in data["objects"]:
        for bbox in image_item["bbox_stat"]:
            if bbox["error_type"] == "FP" and "markup_type" not in bbox:
                names.add(image_item["image"])
    return list(names)

def getPureFN(data):
    names = set()
    for image_item in data["objects"]:
        for bbox in image_item["bbox_stat"]:
            if bbox["error_type"] == "FN" and "found_type" not in bbox:
                names.add(image_item["image"])
    return list(names)

def getWrongType(data):
    names = set()
    for image_item in data["objects"]:
        for bbox in image_item["bbox_stat"]:
            if "found_type" in bbox and "markup_type" in bbox and \
                bbox["markup_type"] != bbox["found_type"] :
                names.add(image_item["image"])
    return list(names)

def getCropped(data):
    names = set()
    for image_item in data["objects"]:
        for bbox in image_item["bbox_stat"]:
            if "max_in" in bbox and \
                (bbox["max_in"] > threshold_in_ration or bbox["max_out"] > threshold_out_ration):
                names.add(image_item["image"])
    return list(names)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", required=True, type=str, help="Path to stat file")
    parser.add_argument("-f", required=True, type=str, help="Path to file to save images names")
    parser.add_argument("-o", required=True, type=str, help="What kind of errors \
        (available: TP, FP, FN, FP_offset, wrong_type, pure_FP, pure_FN)")
    args = parser.parse_args()

    available_options = set(["TP", "FP", "FN", "FP_offset", "wrong_type", "pure_FP", "pure_FN"])
    stat_path = args.s
    file_path = args.f
    option = args.o

    if option not in available_options:
        print("Error: Option is not available")
        exit()

    with open(stat_path, "r") as f:
        data = json.load(f)

    names = []
    if option in ["TP", "FP", "FN"]:
        names = getPerType(data, option)
    elif option == "pure_FP":
        names = getPureFP(data)
    elif option == "pure_FN":
        names = getPureFN(data)
    elif option == "wrong_type":
        names = getWrongType(data)
    elif option == "FP_offset":
        names = getCropped(data)
    
    with open(file_path, "w") as f:
        f.write(option + "\n\n")
        for name in names:
            f.write(name + "\n")