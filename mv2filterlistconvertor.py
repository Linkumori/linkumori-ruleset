import re
import json

# Define the function to parse MV3 rules and format them into the desired JSON structure
def parse_mv3_rules(file_path):
    rules = []
    rule_id = 1
    universal_params = set()
    domain_specific_rules = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("$removeparam"):
                    match = re.search(r'\$removeparam=([^,]+)(?:,doc)?(?:,domain=(.*))?', line)
                    if match:
                        param_name = match.group(1)
                        domains = match.group(2).split('|') if match.group(2) else []

                        if not domains:
                            universal_params.add(param_name)
                        else:
                            domain_key = tuple(sorted(domains))
                            if domain_key not in domain_specific_rules:
                                domain_specific_rules[domain_key] = set()
                            domain_specific_rules[domain_key].add(param_name)

        # Create consolidated domain-specific rules
        for domain_key, params in domain_specific_rules.items():
            rule = {
                "id": rule_id,
                "priority": 1,
                "action": {
                    "type": "redirect",
                    "redirect": {
                        "transform": {
                            "queryTransform": {
                                "removeParams": list(params)
                            }
                        }
                    }
                },
                "condition": {
                    "resourceTypes": ["main_frame", "sub_frame", "xmlhttprequest"],
                    "requestDomains": list(domain_key)
                }
            }
            rules.append(rule)
            rule_id += 1

        # Add universal rule if applicable
        if universal_params:
            universal_rule = {
                "id": rule_id,
                "priority": 1,
                "action": {
                    "type": "redirect",
                    "redirect": {
                        "transform": {
                            "queryTransform": {
                                "removeParams": list(universal_params)
                            }
                        }
                    }
                },
                "condition": {
                    "resourceTypes": ["main_frame", "sub_frame", "xmlhttprequest"]
                }
            }
            rules.append(universal_rule)

        return rules
    except FileNotFoundError:
        print("File not found.")
        return []

# Path to the file containing MV3 rules
input_file_path = "filters.txt"
output_file_path = "converted_mv3_rules.json"

# Parse the rules and save to JSON
parsed_rules = parse_mv3_rules(input_file_path)

# Save the consolidated rules to a JSON file
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(parsed_rules, json_file, indent=4)

print(f"Converted rules have been saved to {output_file_path}")
