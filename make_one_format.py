import json

# Scr разметка в coco json и dst разметка
file_name = "/home/krolchonok/Documents/Study/4_term/QR-codes/make_markup/Barcode_Image_Dataset/valid/_annotations.coco.json"
dst_name = "/home/krolchonok/Documents/Study/4_term/QR-codes/make_markup/Barcode_Image_Dataset/valid/markup.json"


src_data = dict()
new_data = dict()

new_data["types_list"] = []

value = dict()
value["id"] = 0
value["name"] = "QR-code"
new_data["types_list"].append(value)

value = dict()
value["id"] = 1
value["name"] = "Data matrix"
new_data["types_list"].append(value)


new_data["objects"] = []

with open(file_name, "r") as f:
    src_data = json.load(f)

with open(file_name, "w") as f:
    json.dump(src_data, f, indent=2)

i = 0
for image_value in src_data["images"]:
    image_id = image_value["id"]
    height = image_value["height"]
    width = image_value["width"]
    image_name = src_data["images"][i]["file_name"]
    i += 1
    boxes = []
    types = []
    for markup_value in src_data["annotations"]:
        if image_id == markup_value["image_id"]:
            category = markup_value["category_id"]
            #Сопоставление категорий зависит от датасета и его изначальной разметки
            if category == 0 or category == 1:
                continue
            elif category == 2:
                types.append(1)
            elif category == 3:
                continue
            elif category == 4:
                types.append(0)
            else:
                types.append(-1)
                continue
            #types.append(0)
            markup_value["bbox"][0] /= width
            markup_value["bbox"][1] /= height
            markup_value["bbox"][2] /= width
            markup_value["bbox"][3] /= height
            boxes.append(markup_value["bbox"])
    
    assert(len(boxes) == len(types))

    if len(types) != 0:
        value_to_insert = dict()
        value_to_insert["image"] = image_name
        value_to_insert["markup"] = []

        j = 0
        for bbox in boxes:
            inner_value = dict()
            inner_value["type"] = types[j]
            inner_value["bbox"] = bbox
            value_to_insert["markup"].append(inner_value)
            j += 1

        new_data["objects"].append(value_to_insert)


with open(dst_name, "w") as f:
    json.dump(new_data, f, indent=2)