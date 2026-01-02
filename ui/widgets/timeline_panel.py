from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, 
    QLabel, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QWheelEvent
from ui.widgets.timeline_track import VideoClipWidget, AudioClipWidget, SubtitleClipWidget

# --- THƯỚC ĐO (GIỮ NGUYÊN) ---
class TimeRuler(QWidget):
    def __init__(self, pixels_per_second=30):
        super().__init__()
        self.setFixedHeight(25)
        self.pixels_per_second = pixels_per_second
        self.total_width = 2000

    def set_scale(self, pps, width):
        self.pixels_per_second = pps
        self.total_width = width
        self.setFixedWidth(width)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#202124"))
        painter.setPen(QPen(QColor("#7f8c8d"), 1))
        painter.setFont(QFont("Segoe UI", 8))
        
        step_sec = 1
        if self.pixels_per_second < 20: step_sec = 5
        elif self.pixels_per_second > 80: step_sec = 0.5

        end_time = int(self.total_width / self.pixels_per_second) + 1
        current_sec = 0
        while current_sec < end_time:
            x = int(current_sec * self.pixels_per_second)
            painter.drawLine(x, 15, x, 25)
            if current_sec % 5 == 0 or (step_sec < 1 and current_sec % 1 == 0):
                painter.drawText(x + 2, 12, f"{int(current_sec//60):02}:{int(current_sec%60):02}")
            current_sec += step_sec

# --- PANEL CHÍNH ---
class TimelinePanel(QWidget):
    seek_request = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.pixels_per_second = 30 # Zoom mặc định
        self.duration_total = 300   
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. TOOLBAR (Chỉ để hiển thị thông tin, Zoom dùng chuột)
        info_bar = QFrame()
        info_bar.setFixedHeight(30)
        info_bar.setStyleSheet("background-color: #2d3436; border-bottom: 1px solid #636e72;")
        il = QHBoxLayout(info_bar)
        il.addWidget(QLabel("💡 Gợi ý: Giữ 'Ctrl' + Lăn chuột để Zoom Timeline"))
        main_layout.addWidget(info_bar)

        # 2. VÙNG CUỘN (SCROLL AREA)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #1e272e; border: none;")
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # --- CONTAINER CHÍNH ---
        self.content_container = QWidget()
        self.content_container.mousePressEvent = self.on_timeline_click
        
        # Layout tổng: Xếp chồng Ruler -> Track Text -> Track Video -> Track Audio
        self.container_layout = QVBoxLayout(self.content_container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(2) # Khoảng cách giữa các tầng
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # A. Ruler
        self.ruler = TimeRuler(self.pixels_per_second)
        self.container_layout.addWidget(self.ruler)

        # --- B. CÁC TRACK RIÊNG BIỆT (Horizontal Layout) ---
        
        # Track 1: Phụ đề (Subtitle)
        self.track_sub_container = QWidget()
        self.track_sub_container.setFixedHeight(40) # Chiều cao cố định
        self.track_sub_container.setStyleSheet("background-color: #2f3640; border-bottom: 1px dashed #57606f;")
        self.track_sub_layout = QHBoxLayout(self.track_sub_container)
        self.track_sub_layout.setContentsMargins(0, 5, 0, 5)
        self.track_sub_layout.setSpacing(5)
        self.track_sub_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.container_layout.addWidget(self.track_sub_container)

        # Track 2: Video (Chính)
        self.track_video_container = QWidget()
        self.track_video_container.setFixedHeight(70) 
        self.track_video_container.setStyleSheet("background-color: #353b48; border-bottom: 1px dashed #57606f;")
        self.track_video_layout = QHBoxLayout(self.track_video_container)
        self.track_video_layout.setContentsMargins(0, 5, 0, 5)
        self.track_video_layout.setSpacing(0) # Video nối liền nhau
        self.track_video_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.container_layout.addWidget(self.track_video_container)

        # Track 3: Audio
        self.track_audio_container = QWidget()
        self.track_audio_container.setFixedHeight(50)
        self.track_audio_container.setStyleSheet("background-color: #2f3640;")
        self.track_audio_layout = QHBoxLayout(self.track_audio_container)
        self.track_audio_layout.setContentsMargins(0, 5, 0, 5)
        self.track_audio_layout.setSpacing(5)
        self.track_audio_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.container_layout.addWidget(self.track_audio_container)
        
        # Đẩy khoảng trống xuống dưới
        self.container_layout.addStretch()

        # --- KIM ĐỎ (PLAYHEAD) ---
        self.playhead = QFrame(self.content_container)
        self.playhead.setFixedWidth(2)
        self.playhead.setStyleSheet("background-color: #e74c3c; border: none;")
        self.playhead.move(0, 0)
        self.playhead.resize(2, 500)
        self.playhead.raise_()

        self.scroll_area.setWidget(self.content_container)
        main_layout.addWidget(self.scroll_area)
        
        self.update_timeline_width()

    # --- XỬ LÝ ZOOM BẰNG CHUỘT (CTRL + WHEEL) ---
    def wheelEvent(self, event: QWheelEvent):
        # Kiểm tra nếu đang giữ phím Ctrl
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept() # Đã xử lý xong, không cuộn trang
        else:
            super().wheelEvent(event) # Nếu không giữ Ctrl thì cuộn bình thường

    def zoom_in(self):
        self.pixels_per_second += 5
        if self.pixels_per_second > 200: self.pixels_per_second = 200
        self.on_zoom_changed()

    def zoom_out(self):
        self.pixels_per_second -= 5
        if self.pixels_per_second < 5: self.pixels_per_second = 5
        self.on_zoom_changed()

    def on_zoom_changed(self):
        self.update_timeline_width()
        # Cập nhật độ rộng cho tất cả các clip trong 3 track
        self.update_track_items(self.track_sub_layout)
        self.update_track_items(self.track_video_layout)
        self.update_track_items(self.track_audio_layout)

    def update_track_items(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() and hasattr(item.widget(), 'update_width'):
                item.widget().update_width(self.pixels_per_second)

    def update_timeline_width(self):
        width = int(self.duration_total * self.pixels_per_second)
        if width < self.scroll_area.width(): width = self.scroll_area.width()
        self.content_container.setFixedWidth(width)
        self.ruler.set_scale(self.pixels_per_second, width)
        # Nới các container track ra theo timeline
        self.track_sub_container.setFixedWidth(width)
        self.track_video_container.setFixedWidth(width)
        self.track_audio_container.setFixedWidth(width)

    # --- THÊM ITEM VÀO ĐÚNG TẦNG ---
    def add_video_track(self, file_path, duration=10):
        clip = VideoClipWidget(file_path, duration)
        clip.update_width(self.pixels_per_second)
        clip.request_delete.connect(self.remove_item)
        self.track_video_layout.addWidget(clip)
        self.check_duration(duration)

    def add_audio_track(self, file_path, duration=10):
        clip = AudioClipWidget(file_path, duration)
        clip.update_width(self.pixels_per_second)
        clip.request_delete.connect(self.remove_item)
        self.track_audio_layout.addWidget(clip)
        self.check_duration(duration)

    def add_subtitle_track(self, text, start_time, duration=5):
        # Lưu ý: Hiện tại đang xếp chồng ngang, logic set vị trí (start_time) 
        # sẽ cần spacer item nếu muốn chính xác tuyệt đối. 
        # Ở đây ta add vào đuôi để demo hiển thị.
        clip = SubtitleClipWidget(text, start_time, duration)
        clip.update_width(self.pixels_per_second)
        clip.request_delete.connect(self.remove_item)
        self.track_sub_layout.addWidget(clip)

    def remove_item(self, widget):
        widget.deleteLater()

    def check_duration(self, duration):
        if duration > self.duration_total:
            self.duration_total = duration + 20
            self.update_timeline_width()

    # --- SYNC PLAYER ---
    def update_cursor_position(self, ms):
        seconds = ms / 1000
        x_pos = int(seconds * self.pixels_per_second)
        self.playhead.move(x_pos, 0)
        self.playhead.setFixedHeight(self.content_container.height()) # Kim dài hết chiều cao
        
        # Auto scroll
        v_width = self.scroll_area.viewport().width()
        scroll = self.scroll_area.horizontalScrollBar().value()
        if x_pos > scroll + v_width - 50:
            self.scroll_area.horizontalScrollBar().setValue(x_pos - 100)

    def on_timeline_click(self, event):
        x = event.pos().x()
        ms = int((x / self.pixels_per_second) * 1000)
        self.playhead.move(x, 0)
        self.seek_request.emit(ms)

    def clear_timeline(self):
        # Helper xóa layout
        def clear_layout(layout):
            while layout.count():
                item = layout.takeAt(0)
                if item.widget(): item.widget().deleteLater()
        
        clear_layout(self.track_sub_layout)
        clear_layout(self.track_video_layout)
        clear_layout(self.track_audio_layout)