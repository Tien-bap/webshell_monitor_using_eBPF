from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QPlainTextEdit,
    QWidget,
    QVBoxLayout,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
    QGroupBox,
    QFormLayout,
)


class WebLogAnalyzerWindow:

    def __init__(self):
        pass

    def start(self, logs):
        self.window = QMainWindow()
        self.window.setWindowTitle("Web Log Analyzer")
        self.window.resize(1400, 700)

        central = QWidget()
        self.window.setCentralWidget(central)

        self.main_layout = QVBoxLayout(central)
        # -------------------------
        # Widgets
        # -------------------------
        self.log_table = self.log_table_view()
        self.log_detail = self.log_detail_view()
        self.load_logs(logs)
        self.log_table.clicked.connect(self.row_clicked)
        # -------------------------
        # Splitter
        # -------------------------
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.log_table)
        self.splitter.addWidget(self.log_detail)
        self.splitter.setStretchFactor(0, 7)
        self.splitter.setStretchFactor(1, 3)

        self.main_layout.addWidget(self.splitter)
        self.window.show()


    def log_table_view(self):
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Time",
            "Source IP",
            "Method",
            "URL",
            "Status",
            "Size"
        ])

        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)

        return table
    

    def log_detail_view(self):

        group = QGroupBox("HTTP Request Detail")
        layout = QFormLayout(group)
        # -------------------------
        # Basic Request Information
        # -------------------------
        self.lb_time = QLabel("-")
        self.lb_ip = QLabel("-")
        self.lb_method = QLabel("-")
        self.lb_url = QLabel("-")
        self.lb_uri = QLabel("-")
        self.lb_query = QLabel("-")
        # -------------------------
        # Response Information
        # -------------------------
        self.lb_status = QLabel("-")
        self.lb_size = QLabel("-")
        self.lb_request_time = QLabel("-")
        # -------------------------
        # Client Information
        # ------------------------
        self.lb_host = QLabel("-")
        self.lb_referer = QLabel("-")
        self.lb_remote_user = QLabel("-")

        self.txt_user_agent = QPlainTextEdit()
        self.txt_user_agent.setReadOnly(True)
        self.txt_user_agent.setMaximumHeight(80)


        # -------------------------
        # Add Layout
        # -------------------------
        layout.addRow("Time:", self.lb_time)
        layout.addRow("Source IP:", self.lb_ip)
        layout.addRow("Method:", self.lb_method)
        layout.addRow("URL:", self.lb_url)
        layout.addRow("Request URI:", self.lb_uri)
        layout.addRow("Query String:", self.lb_query)

        layout.addRow("Status Code:", self.lb_status)
        layout.addRow("Response Size:", self.lb_size)
        layout.addRow("Request Time:", self.lb_request_time)

        layout.addRow("Host:", self.lb_host)
        layout.addRow("Referer:", self.lb_referer)
        layout.addRow("Remote User:", self.lb_remote_user)
        layout.addRow("User-Agent:", self.txt_user_agent)

        return group
    


    def load_logs(self, logs):
        self.logs = logs
        self.log_table.setRowCount(len(logs))
        for row, log in enumerate(logs):
            self.log_table.setItem(row, 0,QTableWidgetItem(log["time"].astimezone().strftime("%Y-%m-%d %H:%M:%S")))
            self.log_table.setItem(row, 1,QTableWidgetItem(log["ip"]))
            self.log_table.setItem(row, 2,QTableWidgetItem(log["method"]))
            self.log_table.setItem(row, 3,QTableWidgetItem(log["url"]))
            self.log_table.setItem(row, 4,QTableWidgetItem(str(log["status"])))
            self.log_table.setItem(row, 5,QTableWidgetItem(str(log["size"])))


    def row_clicked(self, index):
        row = index.row()
        if row < 0:
            return
        log = self.logs[row]

        # -------------------------
        # Request Information
        # -------------------------
        self.lb_time.setText(log["time"].astimezone().strftime("%Y-%m-%d %H:%M:%S"))
        self.lb_ip.setText(log.get("ip", "-"))
        self.lb_method.setText(log.get("method", "-"))
        self.lb_url.setText(log.get("url", "-"))
        self.lb_uri.setText(log.get("request_uri", "-"))
        self.lb_query.setText(log.get("query_string", "-"))


        # -------------------------
        # Response Information
        # -------------------------
        self.lb_status.setText(str(log.get("status", "-")))
        self.lb_size.setText(str(log.get("size", "-")))
        self.lb_request_time.setText(log.get("request_time", "-"))


        # -------------------------
        # Client Information
        # -------------------------
        self.lb_host.setText(log.get("host", "-"))
        self.lb_referer.setText(log.get("referer", "-"))
        self.lb_remote_user.setText(log.get("remote_user", "-"))


        self.txt_user_agent.setPlainText(
            log.get("user_agent", "-")
        )