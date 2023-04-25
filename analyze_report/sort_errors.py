import json

path = "./stat.json"

with open(path, 'r') as f:
    data = json.load(f)

images_per_errors = dict()
images_per_errors["TP"] = []
images_per_errors["true_FP"] = []
images_per_errors["true_FN"] = []
images_per_errors["wrong_box"] = []
images_per_errors["wrong_type"] = []

all_good = []

for value in data["objects"]:
    image = value["image"]
    for result in value["bbox_stat"]:
        if result["error_type"] = "TP":
            images_per_errors["TP"].append(image)
            continue
        if result["error_type"] = "FN":
            images_per_errors["true_FN"].append(image)
            continue
        if result["error_type"] = "FP":
            if "markup_type" not in result:
                images_per_errors["true_FP"].append(image)
                continue
            if result["markup_type"] != result["found_type"]:
                images_per_errors["true_FP"].append(image)
                continue


