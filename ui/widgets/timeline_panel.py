from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSlider
from PyQt6.QtCore import Qt

class TimelinePanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "panel")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        
        layout.addWidget(QLabel("TIMELINE"))
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        layout.addWidget(self.slider)