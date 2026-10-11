from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtGui import QColor, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QGroupBox,
    QHeaderView,
    QTableView,
    QVBoxLayout,
)

MAX_ROWS = 500


class LiveEvent(QObject):

    event_selected = Signal(dict)  # Signal to emit the selected event

    def __init__(self, dashboard_queue):

        super().__init__()

        self.dashboard_queue = dashboard_queue

        # Lưu event tương ứng với từng dòng
        self.events = []

        self.widget = QGroupBox("Live Events")

        self.model = QStandardItemModel()

        self.timer = QTimer()
        self.timer.timeout.connect(self.read_queue)
        self.timer.start(50)

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        layout = QVBoxLayout()

        self.model.setHorizontalHeaderLabels([
            "Event ID",
            "Timestamp",
            "Event",
            "Container",
            "PID",
            "PPID",
            "TGID",
            "Process",
            "Detail"
        ])

        self.table = QTableView()

        self.table.setModel(self.model)

        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)

        self.table.clicked.connect(self.row_clicked)

        self.set_column_size()

        layout.addWidget(self.table)

        self.widget.setLayout(layout)

    # ======================================================
    # Column
    # ======================================================

    def set_column_size(self):

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(QHeaderView.Interactive)

        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 220)
        self.table.setColumnWidth(2, 90)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 60)
        self.table.setColumnWidth(5, 60)
        self.table.setColumnWidth(6, 60)
        self.table.setColumnWidth(7, 120)

        header.setSectionResizeMode(
            8,
            QHeaderView.Stretch
        )

    # ======================================================
    # Queue
    # ======================================================

    def read_queue(self):
        while not self.dashboard_queue.empty():

            event = self.dashboard_queue.get_nowait()

            self.add_event(event)

    # ======================================================
    # Highlight
    # ======================================================

    def highlight_items(self, event_type, items):

        colors = {
            "ALERT": "#ffb3b3",
            "execve": "#d5f5d5",
            "openat": "#fff3b0",
            "connect": "#ffd5d5",
            "listen": "#ffd5d5",
            "bind": "#ffd5d5",
        }

        color = colors.get(event_type)

        if color is None:
            return

        color = QColor(color)

        for item in items:
            item.setBackground(color)

    # ======================================================
    # Insert Event
    # ======================================================

    def add_event(self, event):

        detail = event["details"]

        if isinstance(detail, dict):
            detail = ", ".join(
                f"{k}={v}"
                for k, v in detail.items()
            )

        items = [
            QStandardItem(str(event["event_id"])),
            QStandardItem(event["timestamp"]),
            QStandardItem(event["event_type"]),
            QStandardItem(event["container"]),
            QStandardItem(str(event["pid"])),
            QStandardItem(str(event["ppid"])),
            QStandardItem(str(event["tgid"])),
            QStandardItem(event["process"]),
            QStandardItem(detail),
        ]

        self.highlight_items(
            event["event_type"],
            items
        )

        self.model.insertRow(0, items)

        # Đồng bộ model <-> event
        self.events.insert(0, event)

        if len(self.events) > MAX_ROWS:
            self.events.pop()

        if self.model.rowCount() > MAX_ROWS:
            self.model.removeRow(MAX_ROWS)

        self.table.scrollToTop()

    # ======================================================
    # Click Event
    # ======================================================

    def row_clicked(self, index):
        row = index.row()
        event = self.events[row]
        self.event_selected.emit(event)