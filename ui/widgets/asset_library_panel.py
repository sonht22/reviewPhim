import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QListWidget, QListWidgetItem, QAbstractItemView, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor, QIcon, QKeySequence, QShortcut # <--- Thêm QKeySequence, QShortcut

class AssetLibraryPanel(QWidget):
    def __init__(self):
        super().__init__()
        # Màu nền tổng thể
        self.setStyleSheet("background-color: #202124; border-right: 1px solid #3c4043;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)
        
        # 1. Header
        header_layout = QHBoxLayout()
        lbl_title = QLabel("MEDIA")
        lbl_title.setStyleSheet("font-weight: 900; color: #dadce0; font-size: 14px; border: none;")
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # 2. Nút chức năng
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        btn_style = """
            QPushButton { 
                background-color: #303134; 
                color: #e8eaed; 
                border: 1px solid #5f6368; 
                padding: 8px; 
                border-radius: 6px; 
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { 
                background-color: #8ab4f8; 
                color: #202124;
                border: 1px solid #8ab4f8;
            }
            QPushButton:pressed {
                background-color: #669df6;
            }
        """
        
        self.btn_import_video = QPushButton("+ Video")
        self.btn_import_video.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_import_video.setStyleSheet(btn_style)
        
        self.btn_import_audio = QPushButton("+ Audio")
        self.btn_import_audio.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_import_audio.setStyleSheet(btn_style)
        
        btn_layout.addWidget(self.btn_import_video)
        btn_layout.addWidget(self.btn_import_audio)
        layout.addLayout(btn_layout)

        # 3. Kẻ ngang
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #3c4043;")
        layout.addWidget(line)

        # 4. Danh sách
        self.asset_list = QListWidget()
        
        # --- [QUAN TRỌNG] Thay đổi Focus Policy ---
        # Để nhận được phím Delete, ListWidget PHẢI có Focus (StrongFocus)
        self.asset_list.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self.asset_list.setStyleSheet("""
            QListWidget { 
                background-color: transparent; 
                border: none;
                outline: none; /* Ẩn viền nét đứt khi focus */
            }
            QListWidget::item { 
                background: transparent;
                border-radius: 6px;
                padding: 4px;
                margin-bottom: 4px;
            }
            QListWidget::item:hover { 
                background-color: #303134; 
            }
            QListWidget::item:selected { 
                background-color: #3c4043; 
                border: 1px solid #5f6368;
            }
        """)
        self.asset_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.asset_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.asset_list)
        
        # --- [MỚI] TÍCH HỢP PHÍM DELETE ---
        # Tạo phím tắt Delete gắn vào danh sách
        self.delete_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Delete), self.asset_list)
        # Khi bấm Delete -> Gọi hàm xóa item đang chọn
        self.delete_shortcut.activated.connect(self.remove_selected_item)

        self.setLayout(layout)

    def add_asset(self, file_path, asset_type="video"):
        """Thêm file vào danh sách"""
        file_name = os.path.basename(file_path)
        
        if asset_type == "video":
            icon_text = "🎬"
            text_color = "#8ab4f8" 
        else:
            icon_text = "🎵"
            text_color = "#f28b82" 
            
        item = QListWidgetItem(self.asset_list)
        item.setData(Qt.ItemDataRole.UserRole, file_path)
        
        container_widget = QWidget()
        container_widget.setStyleSheet("background: transparent;")
        
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(5, 5, 5, 5) 
        container_layout.setSpacing(10)
        
        lbl_icon = QLabel(icon_text)
        lbl_icon.setStyleSheet("font-size: 16px; border: none;")
        
        lbl_name = QLabel(file_name)
        lbl_name.setStyleSheet(f"color: {text_color}; font-weight: 500; font-size: 12px; border: none;")
        lbl_name.setWordWrap(False)
        
        # --- Nút Xóa (Icon OIP) ---
        btn_delete = QPushButton()
        btn_delete.setFixedSize(24, 24)
        btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_delete.setToolTip("Xóa (Delete)")
        
        img_folder = r"D:\CU SƠN\tool\reviewPhim\ui\img"
        icon_path_png = os.path.join(img_folder, "OIP.png")
        icon_path_jpg = os.path.join(img_folder, "OIP.jpg")
        icon_path_jpeg = os.path.join(img_folder, "OIP.jpeg")
        
        final_icon_path = None
        if os.path.exists(icon_path_png): final_icon_path = icon_path_png
        elif os.path.exists(icon_path_jpg): final_icon_path = icon_path_jpg
        elif os.path.exists(icon_path_jpeg): final_icon_path = icon_path_jpeg

        if final_icon_path:
            btn_delete.setIcon(QIcon(final_icon_path))
            btn_delete.setIconSize(QSize(18, 18))
            btn_delete.setStyleSheet("""
                QPushButton { background-color: transparent; border: none; border-radius: 4px; }
                QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); }
            """)
        else:
            btn_delete.setText("✕")
            btn_delete.setStyleSheet("""
                QPushButton { color: #5f6368; border: none; font-weight: bold; }
                QPushButton:hover { color: #d93025; }
            """)

        # Nối nút bấm với hàm xóa item cụ thể
        btn_delete.clicked.connect(lambda: self.remove_asset_item(item))

        container_layout.addWidget(lbl_icon)
        container_layout.addWidget(lbl_name, stretch=1)
        container_layout.addWidget(btn_delete)
        
        container_widget.setLayout(container_layout)
        item.setSizeHint(container_widget.sizeHint()) 
        self.asset_list.setItemWidget(item, container_widget)

    def remove_asset_item(self, item):
        """Xóa một item cụ thể (được gọi từ nút X)"""
        row = self.asset_list.row(item)
        self.asset_list.takeItem(row)

    def remove_selected_item(self):
        """Xóa item đang được chọn (được gọi từ phím Delete)"""
        # Lấy item đang được highlight
        current_item = self.asset_list.currentItem()
        if current_item:
            self.remove_asset_item(current_item)