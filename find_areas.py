import json
#import matplotlib.pyplot as plt

prefix = "/home/krolchonok/Documents/Study/4_term/QR-codes/make_markup/QR Codes Detection.v1i.coco/"
postfix = ["train/markup.json", "test/markup.json", "valid/markup.json"]

areas = []
for post in postfix:
    file_name = prefix + post
    with open(file_name, "r") as f:
        data = json.load(f)
        for value in data["objects"]:
            for code_info in value["markup"]:
                box = code_info["bbox"]
                areas.append(box[2] * box[3])

thresholds = [100, 1000, 10000, 100000, 1000000000, 10000000000]
value_to_hist = [0] * len(thresholds)
for area in areas:
    index = 0
    for t in thresholds:
        if area > t:
            index += 1
    if index >= len(thresholds):
        index = len(thresholds) -1
    value_to_hist[index] += 1

print(value_to_hist)
