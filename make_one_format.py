import json

file_name = "/home/krolchonok/Documents/Study/4_term/QR-codes/make_markup/Barcode Image Dataset/train/_annotations.coco.json"
dst_name = "/home/krolchonok/Documents/Study/4_term/QR-codes/make_markup/tmp4.json"
src_data = dict()
new_data = dict()

new_data["objects"] = []

with open(file_name, "r") as f:
    src_data = json.load(f)

with open(file_name, "w") as f:
    json.dump(src_data, f, indent=2)

i = 0
for image_value in src_data["images"]:
    image_id = image_value["id"]
    image_name = src_data["images"][i]["file_name"]
    boxes = []
    types = []
    for markup_value in src_data["annotations"]:
        if image_id == markup_value["image_id"]:
            boxes.append(markup_value["bbox"])
            category = markup_value["category_id"]
            if category == 0 or category == 1:
                types.append("Barcode")
            elif category == 2:
                types.append("DataMatrix")
            elif category == 3:
                types.append("Other")
            elif category == 4:
                types.append("QR")
            else:
                types.append("Error")
    
    value_to_insert = dict()
    value_to_insert["image"] = image_name
    value_to_insert["markup"] = []

    assert(len(boxes) == len(types))

    j = 0
    for bbox in boxes:
        inner_value = dict()
        inner_value["type"] = types[j]
        inner_value["bbox"] = bbox
        value_to_insert["markup"].append(inner_value)
        j += 1
    
    new_data["objects"].append(value_to_insert)
    i += 1


with open(dst_name, "w") as f:
    json.dump(new_data, f, indent=2)