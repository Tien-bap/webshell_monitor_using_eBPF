LIMIT = 1000


class ProcessCache:
    def __init__(self):
        self.limit = LIMIT
        self.event_map = {}
        self.child_map = {}


    def update_cache(self, event):
        self.update_event_map(event)


    def update_event_map(self, event):
        event_id = event["event_id"]
        parent_event_id = event["parent_event_id"]
        self.event_map[event_id] = event
        self.update_child_map(event_id, parent_event_id)

        if len(self.event_map) > self.limit:
            oldest_event_id = min(self.event_map.keys())
            del self.event_map[oldest_event_id]


    def update_child_map(self, event_id, parent_event_id):
        if parent_event_id not in self.child_map:
            self.child_map[parent_event_id] = set()
        self.child_map[parent_event_id].add(event_id)
    

    def get_parent_chain(self, event_id):

        chain = []

        current_id = event_id

        while current_id in self.event_map:

            event = self.event_map[current_id]
            chain.append(event)

            parent_id = event["parent_event_id"]

            if parent_id == -1:
                break

            current_id = parent_id

        return chain
    
    def get_children(self, event_id):
        child_event_ids = self.child_map.get(event_id, set())
        chain = []
        for child_id in child_event_ids:
            if child_id in self.event_map:
                chain.append(self.event_map[child_id])
        return chain
    
    def get_event(self, event_id):
        return self.event_map.get(event_id)
    
    def search_events(self, search_text):
        for event in self.event_map.values():
            # if (search_text in str(event["pid"]) or
            #     search_text in event["process_name"] or
            #     search_text in str(event["event_id"])):
            if search_text in str(event["pid"]):
                return event
            
        return None