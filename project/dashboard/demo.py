#pip install PySide6
import sys
from PySide6.QtWidgets import QHeaderView # tu dong gian deu
from PySide6.QtCore import Qt # bang
from PySide6.QtCore import QTimer
from queue import Queue 

from PySide6.QtWidgets import (
    QApplication,       # Khởi động ứng dụng Qt
    QWidget,            # Cửa sổ chính
    QHBoxLayout,        # Chia ngang
    QVBoxLayout,        # Chia dọc
    QGroupBox,          # Khung có tiêu đề
    QTreeWidget,        # Hiển thị cây Process
    QTreeWidgetItem,    # Một node trong cây
    QTableWidget,       # Hiển thị bảng Event
    QTableWidgetItem,   # Một ô trong bảng
    QTextEdit,          # Hiển thị văn bản
)

app = QApplication(sys.argv)   # khoi tao ung dung

window = QWidget()      # Tao cua so chinh
window.setWindowTitle("eBPF Security Monitor")      # title
window.resize(1200, 700)

main_layout = QVBoxLayout(window)

# ======================
# Top Layout
# ======================

# ---------- Live Events ----------
group_events = QGroupBox("Live Events")
layout_events = QVBoxLayout()

table = QTableWidget()
table.setColumnCount(3)
table.setHorizontalHeaderLabels(["Time", "PID", "Event"])
table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # tu dong gian deu
table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded) #thanh cuon
table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded) #thanh cuon



# for r, row in enumerate(events):
#     for c, value in enumerate(row):
#         table.setItem(r, c, QTableWidgetItem(value))

layout_events.addWidget(table)
group_events.setLayout(layout_events)



# add layout
main_layout.addWidget(group_events)

window.show()

sys.exit(app.exec())