from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class PlayerPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "panel")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Màn hình đen giả lập Player
        self.screen = QLabel("VIDEO PREVIEW PLAYER")
        self.screen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screen.setStyleSheet("background-color: black; border-radius: 4px; font-size: 20px; color: #555;")
        self.screen.setMinimumHeight(300)
        layout.addWidget(self.screen)

        # Control Bar
        controls = QHBoxLayout()
        controls.addWidget(QLabel("00:00:00"))
        
        self.btn_play = QPushButton("▶ PLAY")
        controls.addStretch()
        controls.addWidget(self.btn_play)
        controls.addStretch()
        
        layout.addLayout(controls)