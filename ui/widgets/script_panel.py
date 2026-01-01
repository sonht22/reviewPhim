from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget, QPushButton

class ScriptPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "panel") # Để ăn CSS
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        lbl = QLabel("📜 KỊCH BẢN (SEGMENTS)")
        lbl.setStyleSheet("font-weight: bold; color: #aaaaaa;")
        layout.addWidget(lbl)

        self.script_list = QListWidget()
        # Mock data (sau này sẽ load từ Logic)
        self.script_list.addItems(["1. Intro...", "2. Main Event...", "3. Conclusion..."])
        layout.addWidget(self.script_list)
        
        btn_add = QPushButton("+ Thêm Segment")
        btn_add.setProperty("class", "secondary")
        layout.addWidget(btn_add)