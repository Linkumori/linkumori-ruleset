import json

def divide_json_by_param_count(input_file):
    with open(input_file, "r") as file:
        data = json.load(file)
    
    grouped_data = {
        "1-10": [],
        "11-20": [],
        "21-30": [],
        "31-40": [],
        "41-50": [],
        "over50": []
    }

    for entry in data:
        param_count = len(entry.get("action", {}).get("redirect", {}).get("transform", {}).get("queryTransform", {}).get("removeParams", []))
        
        if param_count <= 10:
            group_key = "1-10"
        elif param_count <= 20:
            group_key = "11-20"
        elif param_count <= 30:
            group_key = "21-30"
        elif param_count <= 40:
            group_key = "31-40"
        elif param_count <= 50:
            group_key = "41-50"
        else:
            group_key = "over50"
        
        grouped_data[group_key].append(entry)

    # Write each group to a separate JSON file
    for group_key, items in grouped_data.items():
        output_file = f"group_{group_key}.json"
        with open(output_file, "w") as output:
            json.dump(items, output, indent=4)
        print(f"File '{output_file}' created with {len(items)} entries.")

# Usage
input_file = "rules1.json"  # Path to your JSON file
divide_json_by_param_count(input_file)
