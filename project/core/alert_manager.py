from flask import json


class AlertManager:
    def __init__(self, alert_queue, rule_mgr):
        self.alert_queue = alert_queue
        self.rule_mgr = rule_mgr

    def add_event(self, event):
        rule = self.rule_mgr.check_rules(event)
        
        if rule:
            alert_event = {
                "rule_id": rule["id"],
                "rule_name": rule["name"],
                "rule_description": rule["description"],
                **event
            }
            self.log_alert(alert_event)
            self.alert_queue.put(alert_event)


    def log_alert(self, event):
        with open("data/alerts.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")
