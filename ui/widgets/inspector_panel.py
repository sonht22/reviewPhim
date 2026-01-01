# FILE: ui/widgets/inspector_panel.py
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QLineEdit, QPushButton

class InspectorPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "panel")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("⚙️ CHỈNH SỬA CHI TIẾT"))
        
        layout.addWidget(QLabel("Script:"))
        self.txt_script = QTextEdit()
        self.txt_script.setMaximumHeight(100)
        layout.addWidget(self.txt_script)
        
        # Time inputs
        time_layout = QHBoxLayout()
        self.inp_start = QLineEdit("00:00:00")
        self.inp_end = QLineEdit("00:00:05")
        
        time_layout.addWidget(QLabel("Start:"))
        time_layout.addWidget(self.inp_start)
        time_layout.addWidget(QLabel("End:"))
        time_layout.addWidget(self.inp_end)
        layout.addLayout(time_layout)
        
        layout.addStretch()
        self.btn_save = QPushButton("Lưu thay đổi")
        layout.addWidget(self.btn_save)