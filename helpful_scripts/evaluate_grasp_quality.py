import os
import json
import numpy as np
import pandas as pd
import argparse

user_home = os.path.expanduser("~")
def make_parser():
    """ Input Parser """
    parser = argparse.ArgumentParser(description='Standalone script for Grasp Quality Evaluation.')
    parser.add_argument('--input_dir', type=str, help='Directory of Grasp Information',
                        default=os.path.join(user_home, 'Documents/Dataset/hithand_filtered'))
    parser.add_argument('--output_dir', type=str, help='Directory of Gripper urdf/usd',
                        default=os.path.join(user_home, 'Documents/Dataset/hithand_filtered'))
    
    return parser

parser = make_parser()
args = parser.parse_args()

def rank_categories(fall_time, test_time=3.0, num_categories=5):
    fall_time = np.array(fall_time)
    defined_threshold = np.linspace(test_time, 0, num_categories-1)
    total_num = len(fall_time)
    result = np.zeros(num_categories)

    # Success Categories
    for i in range(num_categories - 1):
        if defined_threshold[i] == 0.0:
            success = fall_time >= defined_threshold[i]
        else:
            success = fall_time > defined_threshold[i]
        num_success = len(fall_time[success])
        success_rate = round(num_success * 100 / total_num, 2)
        result[i] = success_rate

    # Failure Category
    failure = fall_time < 0
    num_failure = len(fall_time[failure])
    failure_rate = round(num_failure * 100 / total_num, 2)
    result[-1] = failure_rate
    return result.tolist()

def eval():
    # Directories
    input_dir = args.input_dir
    output_dir = args.output_dir

    result_name = input_dir.split("/")[-1]
    result_path = os.path.join(output_dir, f"{result_name}.xlsx")

    # Pandas DataFrame init
    columns_names = ["Objects", "> 3s", "> 2s", "> 1s", "> 0s", "Failure Rate (%)", "#Grasps"]
    df = pd.DataFrame(columns=columns_names)

    for k, json_file in enumerate(os.listdir(input_dir)):
        if not ('.json' in json_file):
            continue
        json_file_path = os.path.join(input_dir, json_file)
        with open(json_file_path) as jf:
            json_data = json.load(jf)
        result = rank_categories(json_data["fall_time"])

        # Add object names and total number of grasps
        object_name = json_data["object_id"]
        result.insert(0, object_name)
        result.insert(len(result), len(json_data["fall_time"]))

        # Add result to row of dataframe
        df.loc[k]= result

    # Add result statistic (mean, sum) to the last row
    last_row = len(df)
    df.loc[last_row, columns_names[1:6]] = df.mean(numeric_only=True)[columns_names[1:6]]
    df.loc[last_row, columns_names[-1]] = df.sum(numeric_only=True)[columns_names[-1]]

    # Pandas DataFrame to excel
    df.to_excel(result_path)

if __name__ == "__main__":
    eval()