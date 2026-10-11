import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSplitter,
)

from dashboard.tool_bar_layout.tool_bar import ToolBar
from dashboard.center_layout.live_event import LiveEvent
from dashboard.center_layout.alert_view import AlertView
from dashboard.bottom_layout.event_detail import EventDetail
from dashboard.bottom_layout.process_tree import ProcessTree


class MainDashboard:

    def __init__(self, dashboard_queue, alert_queue, filter_mgr, action_mgr, process_cache, web_log_analyzer):

        self.app = QApplication(sys.argv)

        self.window = QMainWindow()
        self.window.setWindowTitle("eBPF Security Monitor")
        self.window.resize(1400, 800)

        central = QWidget()
        self.window.setCentralWidget(central)
        self.filter_mgr = filter_mgr
        self.action_mgr = action_mgr
        self.web_log_analyzer = web_log_analyzer

        self.main_layout = QVBoxLayout(central)

        # ---------------------------
        # Menu
        # ---------------------------

        self.toolbar = ToolBar(self.window, self.filter_mgr)

        # ---------------------------
        # Center Widgets
        # ---------------------------

        self.live_event = LiveEvent(dashboard_queue)
        self.alert_view = AlertView(alert_queue)

        self.center_splitter = QSplitter(Qt.Horizontal)

        self.center_splitter.addWidget(self.live_event.widget)
        self.center_splitter.addWidget(self.alert_view.widget)

        self.center_splitter.setStretchFactor(0, 8)
        self.center_splitter.setStretchFactor(1, 2)

        # ---------------------------
        # Bottom Widgets
        # ---------------------------

        self.event_detail = EventDetail(process_cache)
        self.process_tree = ProcessTree(process_cache)

        self.bottom_widget = QWidget()

        self.bottom_layout = QHBoxLayout(self.bottom_widget)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.bottom_layout.addWidget(self.event_detail.widget, 3)
        self.bottom_layout.addWidget(self.process_tree.widget, 4)

        # ---------------------------
        # Main Splitter
        # ---------------------------

        self.main_splitter = QSplitter(Qt.Vertical)

        self.main_splitter.addWidget(self.center_splitter)
        self.main_splitter.addWidget(self.bottom_widget)

        self.main_splitter.setStretchFactor(0, 8)
        self.main_splitter.setStretchFactor(1, 2)

        self.main_layout.addWidget(self.main_splitter)

        # ---------------------------
        # Signals
        # ---------------------------

        self.live_event.event_selected.connect(
            lambda event: (
                self.event_detail.show_event(event),
                self.process_tree.show_parent_chain(event)
            )
        )

        self.alert_view.event_selected.connect(
            lambda event: (
                self.event_detail.show_event(event),
                self.process_tree.show_parent_chain(event)
            )
        )

        self.process_tree.event_selected.connect(
            lambda event: (
                self.event_detail.show_event(event)
            )
        )

        self.event_detail.ignore_clicked.connect(lambda event: (self.action_mgr.ignore_pids(event)))
        self.event_detail.kill_clicked.connect(lambda event: (self.action_mgr.kill(event)))
        self.event_detail.web_log_clicked.connect(lambda event: (self.web_log_analyzer.start(event)))
        self.toolbar.search_clicked.connect(
            lambda search_text: (
                self.event_detail.search(search_text),
                self.process_tree.search(search_text)
            )
        )

    def start(self):

        self.window.show()

        sys.exit(self.app.exec())