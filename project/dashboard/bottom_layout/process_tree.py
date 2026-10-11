from PySide6.QtWidgets import (
    QGroupBox,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)
from PySide6.QtCore import Qt, Signal, QObject


class ProcessTree(QObject):

    event_selected = Signal(dict)  # Signal to emit the selected event
    

    def __init__(self, process_cache):
        super().__init__()

        self.process_cache = process_cache
        self.widget = QGroupBox("Process Tree")

        layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Process")

        layout.addWidget(self.tree)

        self.widget.setLayout(layout)
        self.tree.itemClicked.connect(self.on_item_clicked)

    def clear(self):
        self.tree.clear()

    
    def show_parent_chain(self, event):
        self.tree.clear()

        event_id = event["event_id"]
        parent_chain = self.process_cache.get_parent_chain(event_id)

        if not parent_chain:
            return

        root_event = parent_chain[-1]
        root_item = QTreeWidgetItem([f"(PID {root_event['pid']}) {root_event['process']} {root_event['details']}"])
        root_item.setData(0, Qt.UserRole, root_event)
        self.tree.addTopLevelItem(root_item)

        current_item = root_item

        for event in reversed(parent_chain[:-1]):
            child_item = QTreeWidgetItem([f"(PID {event['pid']}) {event['process']} {event['details']}"])
            child_item.setData(0, Qt.UserRole, event)
            current_item.addChild(child_item)
            current_item = child_item

        child_events = self.process_cache.get_children(event_id)
        for child_event in child_events:
            child_item = QTreeWidgetItem([f"(PID {child_event['pid']}) {child_event['process']} {child_event['details']}"])
            child_item.setData(0, Qt.UserRole, child_event)
            current_item.addChild(child_item) 

        self.tree.expandAll()


    def on_item_clicked(self, item, column):
        event = item.data(0, Qt.UserRole)
        self.event_selected.emit(event)

    def search(self, search_text):
        matching_events = self.process_cache.search_events(search_text)
        if not matching_events:
            return
        self.tree.clear()
        event = matching_events
        self.show_parent_chain(event)

