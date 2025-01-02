import json
from collections import defaultdict
from typing import Dict, List, Set

class RuleConsolidator:
    def __init__(self):
        self.domain_params = defaultdict(set)
        self.next_rule_id = 1

    def load_rules(self, file_path: str) -> None:
        """Load rules from a JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            rules = json.load(f)
            self._process_rules(rules)

    def _process_rules(self, rules: List[dict]) -> None:
        """Process rules and organize by domain."""
        for rule in rules:
            domains = rule['condition']['requestDomains']
            params = rule['action']['redirect']['transform']['queryTransform']['removeParams']
            
            # Add parameters to each domain
            for domain in domains:
                self.domain_params[domain].update(params)

    def create_consolidated_rule(self, domain: str, params: Set[str]) -> dict:
        """Create a single consolidated rule for a domain."""
        rule = {
            "id": self.next_rule_id,
            "priority": 1,
            "action": {
                "type": "redirect",
                "redirect": {
                    "transform": {
                        "queryTransform": {
                            "removeParams": sorted(list(params))
                        }
                    }
                }
            },
            "condition": {
                "resourceTypes": ["main_frame", "sub_frame", "xmlhttprequest"],
                "requestDomains": [domain]
            }
        }
        self.next_rule_id += 1
        return rule

    def consolidate(self) -> List[dict]:
        """Create consolidated ruleset."""
        consolidated_rules = []
        
        # Sort domains by number of parameters (descending)
        sorted_domains = sorted(
            self.domain_params.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        # Create rules for each domain
        for domain, params in sorted_domains:
            consolidated_rules.append(
                self.create_consolidated_rule(domain, params)
            )
        
        return consolidated_rules

    def save_rules(self, rules: List[dict], output_path: str) -> None:
        """Save consolidated rules to file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(rules, f, indent=2)

def main():
    consolidator = RuleConsolidator()
    
    # Load both rule sets
    consolidator.load_rules('consolidated_mv3_rules.json')
    
    # Consolidate rules
    consolidated_rules = consolidator.consolidate()
    
    # Save consolidated rules
    consolidator.save_rules(
        consolidated_rules,
        'consolidated_rules.json'
    )

if __name__ == "__main__":
    main()
