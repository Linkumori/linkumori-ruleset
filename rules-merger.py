import json

def consolidate_rules(file1_path, file2_path):
    # Initialize storage structures same as original script
    rule_id = 1
    universal_params = set()
    domain_specific_rules = {}

    def process_rule(rule):
        domains = rule["condition"].get("requestDomains", [])
        params = rule["action"]["redirect"]["transform"]["queryTransform"]["removeParams"]
        
        # Follow same logic as original script
        if not domains:
            universal_params.update(params)
        else:
            domain_key = tuple(sorted(domains))
            if domain_key not in domain_specific_rules:
                domain_specific_rules[domain_key] = set()
            domain_specific_rules[domain_key].update(params)

    # Read and process first file
    with open(file1_path, 'r', encoding='utf-8') as f:
        rules1 = json.load(f)
        for rule in rules1:
            process_rule(rule)

    # Read and process second file
    with open(file2_path, 'r', encoding='utf-8') as f:
        rules2 = json.load(f)
        for rule in rules2:
            process_rule(rule)

    # Create consolidated rules using same format as original
    consolidated_rules = []
    
    # Create domain-specific rules
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
        consolidated_rules.append(rule)
        rule_id += 1

    # Add universal rule if applicable (same as original)
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
        consolidated_rules.append(universal_rule)

    return consolidated_rules

# File paths
file1_path = "rules1.json"
file2_path = "rules2.json"
output_path = "consolidated_mv3_rules.json"

# Consolidate rules
consolidated_rules = consolidate_rules(file1_path, file2_path)

# Save consolidated rules
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(consolidated_rules, f, indent=4)

print(f"Consolidated rules have been saved to {output_path}")
