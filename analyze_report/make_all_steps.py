import argparse
import json
import os

import subprocess

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", required=True, type=str, help="Src file with matched report and markup")
    parser.add_argument("-d", required=True, type=str, help="Path to dataset")
    parser.add_argument("-o", required=True, type=str, help="Dir to save all steps")
    args = parser.parse_args()

    dir_path = args.o

    dataset_path = args.d
    report_path = args.r
    stat_path = dir_path + "/stat.json"
    match_path = dir_path + "/match_bbox.json"
    images_common_prefix = dir_path + "/Images_per_typer/"

    subprocess.run(['mkdir', dir_path])
    subprocess.run(['mkdir', images_common_prefix])
    subprocess.run(['python3', 'common_stat.py', '-r', report_path, '-s', stat_path,
        '-m', match_path])
    
    options = ["TP", "FP", "FN", "FP_offset", "wrong_type", "pure_FP", "pure_FN"]
    for option in options:
        file_name = images_common_prefix + option + ".txt"
        folder_name = images_common_prefix + "/" + option + "/"
        
        subprocess.run(['python3', 'save_error_types.py', '-s', report_path,
            '-s', stat_path, '-f', file_name, '-o', option])

        subprocess.run(['mkdir', folder_name])

        subprocess.run(['python3', 'save_per_file.py', '-d', dataset_path,
            '-f', file_name, '-s', folder_name, '-r', report_path])
        


