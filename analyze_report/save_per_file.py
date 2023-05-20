import argparse
import json
import cv2

def draw_current_rect(image, bbox, color, type_letter, position):
    image = cv2.rectangle(image, (bbox[0], bbox[1]), \
            (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 3)
    cv2.putText(image, type_letter, position, cv2.FONT_HERSHEY_SIMPLEX, \
            min(bbox[2], bbox[3])/100, color, int(min(bbox[2], bbox[3])/50))

def markup_text_position(bbox):
    return (bbox[0], bbox[1] - 10)

def result_text_position(bbox):
    return (bbox[0] + bbox[2] + 10, bbox[1] + bbox[3] - 10)

def draw_rects(image_item, dataset_path):
    image_name = image_item["image"]
    image = cv2.imread(dataset_path + image_name)
    #markup = image_item["markup"]

    type_names = dict()
    for type_value in data["types_list"]:
        type_names[type_value["id"]] = type_value["name"][0]

    common_markup_color = (0, 165, 255)
    TP_color = (0, 255, 0)
    FP_color = (0, 0, 255)
    FN_color = (255, 0, 0)
    atypical_markup_color = (125, 125, 125)
    atypical_result_color = (255, 255, 255)
    for bbox_info in image_item["bbox_stat"]:
        if bbox_info["error_type"] == "TP":
            result_color = TP_color
            markup_color = common_markup_color
            found_type = bbox_info["markup_type"]
        elif bbox_info["error_type"] == "FP": 
            result_color = FP_color
            markup_color = common_markup_color
            found_type = bbox_info["found_type"]
        elif bbox_info["error_type"] == "FN":
            markup_color = FN_color
            found_type = -1
        else:
            result_color = atypical_result_color
            markup_color = atypical_markup_color
            found_type = -1
            if "found_type" in bbox_info:
                found_type = bbox_info["found_type"]
        
        if "markup_bbox" in bbox_info:
            if "markup_type" in bbox_info:
                letter = type_names[bbox_info["markup_type"]]
            else:
                letter = "A"
            position = markup_text_position(bbox_info["markup_bbox"])
            draw_current_rect(image, bbox_info["markup_bbox"], markup_color, letter, position)

        if found_type != -1:
            letter = type_names[found_type]
            position = result_text_position(bbox_info["result_bbox"])
            draw_current_rect(image, bbox_info["result_bbox"], result_color, letter, position)
            
    
    #for markup_value in image_item["markup"]:
    #    bbox = markup_value["bbox"]
    #    type_letter = type_names[markup_value["type"]]
    #    color = (0, 165, 255)
    #    image = cv2.rectangle(image, (bbox[0], bbox[1]), \
    #        (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 3)
    #    cv2.putText(image, type_letter, (bbox[0], bbox[1] - 10), \
    #        cv2.FONT_HERSHEY_SIMPLEX, min(bbox[2], bbox[3])/100, color, int(min(bbox[2], bbox[3])/50))
    #
    #for result_value in image_item["result"]:
    #    bbox = result_value["bbox"]
    #    type_letter = type_names[result_value["type"]]
    #    color = (0, 0, 255)
    #    image = cv2.rectangle(image, (bbox[0], bbox[1]), \
    #        (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 3)
    #    cv2.putText(image, type_letter, (bbox[0] + bbox[2] + 10, bbox[1] + bbox[3] - 10), \
    #        cv2.FONT_HERSHEY_SIMPLEX, min(bbox[2], bbox[3])/100, color, int(min(bbox[2], bbox[3])/50))
    return image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", required=True, type=str, help="Path to dataset")
    parser.add_argument("-f", required=True, type=str, help="Path to file to process")
    parser.add_argument("-o", required=True, type=str, help="Path to save images")
    parser.add_argument("-s", required=True, type=str, help="Path to stat file")
    args = parser.parse_args()

    save_path = args.o + "/"
    file_path = args.f
    stat_path = args.s
    dataset_path = args.d + "/"

    with open(stat_path, "r") as f:
        data = json.load(f)

    with open(file_path, "r") as file:
        for line in file:
            line = line.replace("\n", "")
            if "." in line:
                for image_item in data["objects"]:
                    if line == image_item["image"]:
                        image = draw_rects(image_item, dataset_path)
                        image_name = image_item["image"].replace("/", "_")
                        cv2.imwrite(save_path + image_name, image)
                        break