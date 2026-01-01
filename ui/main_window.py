from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt
from ui.styles import DARK_THEME_QSS

# Import các mảnh ghép
from ui.widgets.script_panel import ScriptPanel
from ui.widgets.player_panel import PlayerPanel
from ui.widgets.inspector_panel import InspectorPanel
from ui.widgets.timeline_panel import TimelinePanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Recap Pro - Modular UI")
        self.resize(1280, 800)
        
        # 1. Apply Style
        self.setStyleSheet(DARK_THEME_QSS)

        # 2. Setup Layout chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # === LẮP GHÉP CÁC PHẦN ===
        
        # Phần trên: Splitter chia 3 cột (Script | Player | Inspector)
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.script_panel = ScriptPanel()
        self.player_panel = PlayerPanel()
        self.inspector_panel = InspectorPanel()
        
        top_splitter.addWidget(self.script_panel)
        top_splitter.addWidget(self.player_panel)
        top_splitter.addWidget(self.inspector_panel)
        
        top_splitter.setSizes([250, 600, 300]) # Tỷ lệ kích thước
        
        # Phần dưới: Timeline
        self.timeline_panel = TimelinePanel()

        # Thêm vào layout tổng
        main_layout.addWidget(top_splitter, stretch=7)
        main_layout.addWidget(self.timeline_panel, stretch=3)