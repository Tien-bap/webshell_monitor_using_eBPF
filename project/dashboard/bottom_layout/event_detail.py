from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import (
    QGroupBox,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)


class EventDetail(QObject):

    ignore_clicked = Signal(dict)
    kill_clicked = Signal(dict)
    web_log_clicked = Signal(dict)

    def __init__(self, cache):
        super().__init__()

        self.cache = cache
        self.current_event = None

        self.widget = QGroupBox("Event Detail")

        layout = QVBoxLayout()

        # -------------------------
        # Event Detail
        # -------------------------

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)

        layout.addWidget(self.detail_text)

        # -------------------------
        # Action Buttons
        # -------------------------

        button_layout = QHBoxLayout()

        self.ignore_button = QPushButton("Ignore")
        self.kill_button = QPushButton("Kill")
        self.web_log_button = QPushButton("web log")

        button_layout.addStretch()

        button_layout.addWidget(self.ignore_button)
        button_layout.addWidget(self.kill_button)
        button_layout.addWidget(self.web_log_button)

        layout.addLayout(button_layout)

        self.widget.setLayout(layout)

        # -------------------------
        # Signals
        # -------------------------

        self.ignore_button.clicked.connect(self.on_ignore_clicked)
        self.kill_button.clicked.connect(self.on_kill_clicked)
        self.web_log_button.clicked.connect(self.on_web_log_clicked)

    def show_event(self, event):
        self.current_event = event

        text = ""

        for key, value in event.items():
            text += f"{key}: {value}\n"

        self.detail_text.setPlainText(text)

    def on_ignore_clicked(self):
        if self.current_event is not None:
            self.ignore_clicked.emit(self.current_event)

    def on_kill_clicked(self):
        if self.current_event is not None:
            self.kill_clicked.emit(self.current_event)

    def on_web_log_clicked(self):
        if self.current_event is not None:
            self.web_log_clicked.emit(self.current_event)

    def search(self, keyword):
        if not keyword:
            return

        # Search in the cache for events matching the keyword
        results = self.cache.search_events(keyword)

        if results:
            # Show the first matching event in the detail view
            self.show_event(results)