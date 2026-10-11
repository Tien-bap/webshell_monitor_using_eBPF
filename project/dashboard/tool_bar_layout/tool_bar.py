from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QToolBar,
    QLineEdit,
    QPushButton,
)

from dashboard.tool_bar_layout.white_list_filter import WhiteListFilter


class ToolBar(QObject):

    search_clicked = Signal(str)

    def __init__(self, window, filter_mgr):
        super().__init__()

        self.window = window
        self.filter_mgr = filter_mgr
        self.white_list_filter = WhiteListFilter(self.window,self.filter_mgr)

        self.tool_bar()

    def tool_bar(self):

        # -------------------------
        # Menu
        # -------------------------

        menu = self.window.menuBar()

        filter_menu = menu.addMenu("Menu")

        white_list_action = QAction(
            "Edit White List Filter",
            self.window
        )

        filter_menu.addAction(white_list_action)

        white_list_action.triggered.connect(
            self.white_list_filter.start
        )

        # -------------------------
        # Search Toolbar
        # -------------------------

        toolbar = QToolBar("Search")
        toolbar.setMovable(False)

        self.window.addToolBar(toolbar)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search PID / Process / Event ID..."
        )

        self.search_button = QPushButton("Search")

        toolbar.addWidget(self.search_box)
        toolbar.addWidget(self.search_button)

        self.search_button.clicked.connect(
            self.on_search
        )

        self.search_box.returnPressed.connect(
            self.on_search
        )

    def on_search(self):
        keyword = self.search_box.text().strip()
        if keyword:
            self.search_clicked.emit(keyword)