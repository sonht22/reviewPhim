import cv2
import os
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QMenu, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QAction, QCursor

# --- 1. WIDGET VIDEO (TẦNG GIỮA) ---
class VideoClipWidget(QFrame):
    request_delete = pyqtSignal(QFrame)

    def __init__(self, file_path, duration_sec, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.duration = duration_sec
        
        # Style CapCut: Xanh Teal
        self.setStyleSheet("""
            QFrame {
                background-color: #00796b; 
                border: 1px solid #004d40;
                border-radius: 4px;
            }
        """)
        self.setFixedHeight(60) # Chiều cao cố định
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Tên file
        self.lbl_name = QLabel(os.path.basename(file_path), self)
        self.lbl_name.setStyleSheet("color: white; font-weight: bold; background: rgba(0,0,0,0.5); padding: 2px;")
        self.lbl_name.move(5, 5)

        self.generate_filmstrip()

    def generate_filmstrip(self):
        """Tạo thumbnail cắt từ video"""
        try:
            cap = cv2.VideoCapture(self.file_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            num_thumbs = 8 # Số lượng ảnh thumbnail
            step = max(1, total_frames // num_thumbs)
            
            for i in range(num_thumbs):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
                ret, frame = cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = frame.shape
                    q_img = QImage(frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
                    pix = QPixmap.fromImage(q_img).scaled(80, 60, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                    
                    lbl = QLabel()
                    lbl.setPixmap(pix)
                    lbl.setScaledContents(True)
                    self.layout.addWidget(lbl)
            cap.release()
            self.lbl_name.raise_()
        except: pass

    def update_width(self, pixels_per_second):
        self.setFixedWidth(int(self.duration * pixels_per_second))

    def contextMenuEvent(self, event):
        self.show_menu(event, "Xóa Video")

    def show_menu(self, event, text):
        menu = QMenu(self)
        action = QAction(f"🗑️ {text}", self)
        action.triggered.connect(lambda: self.request_delete.emit(self))
        menu.addAction(action)
        menu.exec(QCursor.pos())

# --- 2. WIDGET AUDIO (TẦNG DƯỚI) ---
class AudioClipWidget(QFrame):
    request_delete = pyqtSignal(QFrame)

    def __init__(self, file_path, duration_sec, parent=None):
        super().__init__(parent)
        self.duration = duration_sec
        # Style CapCut: Xanh dương đậm
        self.setStyleSheet("""
            QFrame {
                background-color: #2d3436; 
                border-bottom: 3px solid #00cec9;
                border-radius: 4px;
            }
        """)
        self.setFixedHeight(40)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        lbl = QLabel(f"🎵 {os.path.basename(file_path)}", self)
        lbl.setStyleSheet("color: #00cec9; border: none; padding-left: 10px; font-weight: bold;")
        
    def update_width(self, pixels_per_second):
        self.setFixedWidth(int(self.duration * pixels_per_second))

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        action = QAction("🗑️ Xóa Audio", self)
        action.triggered.connect(lambda: self.request_delete.emit(self))
        menu.addAction(action)
        menu.exec(QCursor.pos())

# --- 3. WIDGET PHỤ ĐỀ / TEXT (TẦNG TRÊN CÙNG) ---
class SubtitleClipWidget(QFrame):
    request_delete = pyqtSignal(QFrame)

    def __init__(self, text, start_time, duration_sec, parent=None):
        super().__init__(parent)
        self.text = text
        self.start_time = start_time
        self.duration = duration_sec
        
        # Style CapCut: Màu Cam/Nâu cho Text
        self.setStyleSheet("""
            QFrame {
                background-color: #d35400; 
                border: 1px solid #e67e22;
                border-radius: 4px;
            }
            QLabel { color: white; font-weight: bold; border: none; }
        """)
        self.setFixedHeight(30) # Text bé hơn chút
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        
        self.lbl_text = QLabel(f"T: {text}", self)
        self.lbl_text.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.lbl_text)

    def update_width(self, pixels_per_second):
        self.setFixedWidth(int(self.duration * pixels_per_second))

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        action = QAction("🗑️ Xóa Phụ đề", self)
        action.triggered.connect(lambda: self.request_delete.emit(self))
        menu.addAction(action)
        menu.exec(QCursor.pos())