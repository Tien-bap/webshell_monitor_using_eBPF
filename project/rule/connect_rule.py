from flask import json


path = "data/rules/rules.json"

class ConnectRule:
    def __init__(self):
        self.path = path
        self.load_rules()

    def load_rules(self):
        with open(self.path, "r") as f:
            self.rules = json.load(f)

        self.connect_rules = self.rules.get("connect_rules", [])
        self.file_rules = self.rules.get("file_rules", [])
        self.execve_rules = self.rules.get("execve_rules", [])

    def check_rule(self, event):
        rule = self.check_rule_connect(event)
        if rule:
            return rule

        rule = self.check_rule_file(event)
        if rule:
            return rule
        
        rule = self.check_rule_execve(event)
        if rule:
            return rule

        return None
        
    def check_rule_connect(self, event):
        for rule in self.connect_rules:
            if event["event_type"] == rule["condition"]["event_type"]:
                return rule

        return None
    
    def check_rule_file(self, event):
        for rule in self.file_rules:
            if event["event_type"] == rule["condition"]["event_type"]:
                if event["details"] in rule["condition"]["file_path"]["sensitive_files"]:

                    return rule

        return None
    
    def check_rule_execve(self, event):
        for rule in self.execve_rules:
            if event["event_type"] == rule["condition"]["event_type"]:
                if event["details"]["command"] in rule["condition"]["commands"]:
                    return rule

        return None