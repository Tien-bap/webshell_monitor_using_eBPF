
import json
from unittest import case
from rule.connect_rule import ConnectRule

class RuleManager:
    def __init__(self):
        self.connect_rule = ConnectRule()

    def check_rules(self, event):
        return self.connect_rule.check_rule(event)
        