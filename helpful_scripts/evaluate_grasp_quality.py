import os
import json
import numpy as np
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
        num_success = np.count_nonzero(success)
        success_rate = round(num_success * 100 / total_num, 2)
        result[i] = success_rate

    # Failure Category
    failure = fall_time < 0
    num_failure = np.count_nonzero(failure)
    failure_rate = round(num_failure * 100 / total_num, 2)
    result[-1] = failure_rate
    return result.tolist()

def eval(input_dir, output_dir):
    # Directories
    result_path = os.path.join(output_dir, f"hithand_filtered.csv")

    # Column names
    columns_names = ["Objects", "> 3s", "> 2s", "> 1s", "> 0s", "Failure Rate (%)", "#Grasps"]
    results = []

    for json_file in os.listdir(input_dir):
        if not json_file.endswith('.json'):
            continue

        json_file_path = os.path.join(input_dir, json_file)
        with open(json_file_path) as jf:
            json_data = json.load(jf)

        result = rank_categories(json_data["fall_time"])
        object_name = json_data["prompt"]
        result.insert(0, object_name)
        result.append(len(json_data["fall_time"]))
        results.append(result)

    # Convert results to NumPy array
    results_array = np.array(results, dtype=object)  # Using dtype=object since first column is string

    # Compute statistics
    numeric_results = results_array[:, 1:].astype(float)  # Convert numeric columns to float
    mean_values = np.mean(numeric_results, axis=0)
    sum_values = np.sum(numeric_results[:, -1])  # Sum for last column (#Grasps)

    # Append statistics row
    summary_row = np.concatenate(([f"Mean"], mean_values[:-1], [sum_values])).tolist()
    results.append(summary_row)

    # Save to CSV
    with open(result_path, "w") as f:
        f.write(",".join(columns_names) + "\n")
        for row in results:
            f.write(",".join(map(str, row)) + "\n")

if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    eval(input_dir, output_dir)