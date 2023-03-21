import os
import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", required=True, type=str, help="Path to report")
    parser.add_argument("-f", required=True, type=str, help="File to save stat")
    parser.add_argument("-l", required=True, type=str, help="Titel to start record with")
    parser.add_argument("--read", required=False, type=str, help="File to save read images")
    parser.add_argument("--unread", required=False, type=str, help="File to save unread images")
    args = parser.parse_args()
    report_path = args.r
    file_path = args.f
    titel = args.l
    read_path = args.read
    unread_path = args.unread

    with open(report_path, "r") as f:
        data = json.load(f)
    
    images_read = []
    images_unread = []
    
    for value in data["objects"]:
        if "markup" not in value.keys():
            print(f"{value} has no markup field")
            assert()
        for box in value["markup"]:
            if "decoded" not in box.keys():
                print(f"{value}[\"markup\"] has no decoded field")
                assert()
            if box["decoded"]:
                images_read.append(value["image"])
            else:
                images_unread.append(value["image"])
    
    with open(file_path, "a") as f:
        f.write(titel + "\n")
        total_count = len(images_read) + len(images_unread)
        label_name = "Total count"
        count = str(total_count).rjust(7)
        f.write(label_name + count + "\n")

        label_name = "Read count"
        count = str(len(images_read)).rjust(8)
        percent = "{:.1f}".format(len(images_read) / total_count * 100).rjust(8)
        f.write(label_name + count + percent + "%" + "\n")

        label_name = "Unead count"
        count = str(len(images_unread)).rjust(7)
        percent = "{:.1f}".format(len(images_unread) / total_count * 100).rjust(8)
        f.write(label_name + count + percent + "%" + "\n")

        f.write("\n")

    if read_path != None:
        with(open(read_path, "a")) as f:
            for value in images_read:
                f.write(value + "\n")

    if unread_path != None:
        with(open(unread_path, "a")) as f:
            for value in images_unread:
                f.write(value + "\n")