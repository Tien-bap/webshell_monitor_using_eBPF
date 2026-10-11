from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDialog,
    QListWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
)

class WhiteListFilter:
    def __init__(self, window, filter_mgr):
        self.dialog = QDialog(window)
        self.filter_mgr = filter_mgr
        self.dialog.setWindowTitle("Filter")
        self.dialog.resize(500, 300)
        self.set_filter_window_layout()

    def start(self):
        self.load_list_ignored_pids()
        self.dialog.exec()

    def set_filter_window_layout(self):
        layout = QVBoxLayout(self.dialog)

        pid_label = QLabel("Ignored PIDs")

        self.pid_list = QListWidget()

        input_label = QLabel("New PID")

        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("Enter PID")

        self.add_button = QPushButton("Add PID")
        self.remove_button = QPushButton("Remove PID")
        self.reset_button = QPushButton("reset")
        self.add_button.clicked.connect(self.add_pid)
        self.remove_button.clicked.connect(self.remove_pid)
        self.reset_button.clicked.connect(self.reset)

        layout.addWidget(pid_label)
        layout.addWidget(self.pid_list)
        layout.addWidget(input_label)
        layout.addWidget(self.pid_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.reset_button)

        # self.load_list_ignored_pids()
        
        

        
    def load_list_ignored_pids(self):
        self.filter_mgr.load()
        self.pid_list.clear()
        for pid in sorted(self.filter_mgr.ignored_pids):
            self.pid_list.addItem(str(pid))

    def add_pid(self):
        text = self.pid_input.text().strip()
        if not text.isdigit():
            return
        pid = int(text)
        self.filter_mgr.add_pid(pid)
        self.pid_list.addItem(str(pid))
        self.pid_input.clear()

    def remove_pid(self):
        item = self.pid_list.currentItem()
        
        if item is None:
            return

        if item:
            row = self.pid_list.row(item)
            self.pid_list.takeItem(row)

        self.filter_mgr.remove_pid(int(item.text()))
        self.pid_input.clear()

    def reset(self):
        self.pid_list.clear()
        self.filter_mgr.reset()