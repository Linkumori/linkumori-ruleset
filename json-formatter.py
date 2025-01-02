import json

def format_rules(input_file, output_file):
    """
  for unified formatting of rules in JSON file
    """
    try:
        # Read input JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Format the rules
        formatted_rules = []
        for rule in data:
            formatted_rule = {
                "id": rule["id"],
                "priority": rule["priority"],
                "action": rule["action"],
                "condition": rule["condition"]
            }
            formatted_rules.append(formatted_rule)
        
        # Write formatted rules to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write opening bracket
            f.write('[\n')
            
            # Write rules
            for i, rule in enumerate(formatted_rules):
                # Convert rule to JSON string with proper indentation
                rule_str = json.dumps(rule, indent=4)
                
                # Write rule
                f.write(rule_str)
                
                # Add comma if not last rule
                if i < len(formatted_rules) - 1:
                    f.write(',')
                
                # Add newline
                f.write('\n')
            
            # Write closing bracket
            f.write(']\n')
            
        print(f"Successfully formatted {len(formatted_rules)} rules")
        
    except Exception as e:
        print(f"Error processing JSON: {str(e)}")

def main():
    input_file = "rules1.json"  # Input file path
    output_file = "formatted_rules4.json"  # Output file path
    
    format_rules(input_file, output_file)

if __name__ == "__main__":
    main()
