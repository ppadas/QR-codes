import argparse
import json
import cv2

def draw_rects(image_item, dataset_path):
    image_name = image_item["image"]
    image = cv2.imread(dataset_path + image_name)
    markup = image_item["markup"]

    type_names = dict()
    for type_value in data["types_list"]:
        type_names[type_value["id"]] = type_value["name"][0]
    
    for markup_value in image_item["markup"]:
        bbox = markup_value["bbox"]
        type_letter = type_names[markup_value["type"]]
        color = (0, 255, 0)
        image = cv2.rectangle(image, (bbox[0], bbox[1]), \
            (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 3)
        cv2.putText(image, type_letter, (bbox[0], bbox[1] - 10), \
            cv2.FONT_HERSHEY_SIMPLEX, min(bbox[2], bbox[3])/100, color, int(min(bbox[2], bbox[3])/50))
    
    for result_value in image_item["result"]:
        bbox = result_value["bbox"]
        type_letter = type_names[result_value["type"]]
        color = (0, 0, 255)
        image = cv2.rectangle(image, (bbox[0], bbox[1]), \
            (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 3)
        cv2.putText(image, type_letter, (bbox[0] + bbox[2] + 10, bbox[1] + bbox[3] - 10), \
            cv2.FONT_HERSHEY_SIMPLEX, min(bbox[2], bbox[3])/100, color, int(min(bbox[2], bbox[3])/50))
    return image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", required=True, type=str, help="Path to dataset")
    parser.add_argument("-f", required=True, type=str, help="Path to file to process")
    parser.add_argument("-s", required=True, type=str, help="Path to save images")
    parser.add_argument("-r", required=True, type=str, help="Path to report file")
    args = parser.parse_args()

    save_path = args.s + "/"
    file_path = args.f
    report_path = args.r
    dataset_path = args.d + "/"

    with open(report_path, "r") as f:
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