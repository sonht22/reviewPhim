import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QStyle, QSlider
)
from PyQt6.QtCore import Qt, QUrl, QTime
from PyQt6.QtGui import QIcon, QAction

# --- IMPORT MODULE MULTIMEDIA CỦA QT ---
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

class PlayerPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #000000;") # Nền đen
        
        # 1. Khởi tạo Trình phát media (Engine)
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        
        # Thiết lập âm lượng mặc định (70%)
        self.audio_output.setVolume(0.7)

        self.setup_ui()
        
        # Kết nối các tín hiệu xử lý
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 2. Màn hình Video (Video Widget thực thụ thay vì QLabel)
        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("background-color: black;")
        
        # Gắn màn hình vào trình phát
        self.media_player.setVideoOutput(self.video_widget)
        
        layout.addWidget(self.video_widget, stretch=1)

        # 3. Thanh điều khiển (Control Bar)
        controls = QFrame()
        controls.setFixedHeight(50)
        controls.setStyleSheet("background-color: #202124; border-top: 1px solid #3c4043;")
        
        c_layout = QHBoxLayout(controls)
        c_layout.setContentsMargins(10, 0, 10, 0)
        
        # Timecode
        self.lbl_time = QLabel("00:00 / 00:00")
        self.lbl_time.setStyleSheet("color: #ecf0f1; font-family: monospace; font-weight: bold;")
        
        # Slider tua video (Progress Bar)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 4px; background: #5f6368; border-radius: 2px; }
            QSlider::sub-page:horizontal { background: #00b894; border-radius: 2px; }
            QSlider::handle:horizontal { background: white; width: 12px; height: 12px; margin: -4px 0; border-radius: 6px; }
        """)
        self.slider.sliderMoved.connect(self.set_position)

        # Nút Play/Pause
        self.btn_play = QPushButton()
        self.update_play_button_icon(False) # Mặc định icon Play
        self.btn_play.setFixedSize(40, 40)
        self.btn_play.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_play.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 20px;
                border: 1px solid #5f6368;
                color: white; font-size: 18px;
            }
            QPushButton:hover { background-color: rgba(255,255,255,0.1); border-color: white; }
        """)
        self.btn_play.clicked.connect(self.play_video)

        # Sắp xếp controls
        c_layout.addWidget(self.btn_play)
        c_layout.addWidget(self.lbl_time)
        c_layout.addWidget(self.slider)

        layout.addWidget(controls)
        self.setLayout(layout)

    # --- LOGIC XỬ LÝ VIDEO ---

    def load_video(self, file_path):
        """Hàm này được gọi khi Double Click vào video ở danh sách"""
        print(f"▶ Player đang load: {file_path}")
        
        # Chuyển đường dẫn file thành QUrl (Bắt buộc với Qt6)
        url = QUrl.fromLocalFile(file_path)
        self.media_player.setSource(url)
        
        # Tự động play luôn cho mượt
        self.play_video()

    def play_video(self):
        """Bật/Tắt Play/Pause"""
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            self.update_play_button_icon(False)
        else:
            self.media_player.play()
            self.update_play_button_icon(True)

    def update_play_button_icon(self, is_playing):
        """Đổi icon nút bấm"""
        if is_playing:
            self.btn_play.setText("⏸") # Icon Pause
        else:
            self.btn_play.setText("▶")  # Icon Play

    def media_status_changed(self, status):
        """Xử lý khi video kết thúc"""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.btn_play.setText("↺") # Icon Replay

    def position_changed(self, position):
        """Cập nhật slider khi video chạy"""
        self.slider.setValue(position)
        self.update_duration_info(position)

    def duration_changed(self, duration):
        """Cập nhật độ dài tổng của video"""
        self.slider.setRange(0, duration)

    def set_position(self, position):
        """Khi người dùng kéo slider -> tua video"""
        self.media_player.setPosition(position)

    def update_duration_info(self, current_ms):
        """Đổi mili-giây sang định dạng 00:00"""
        duration_ms = self.media_player.duration()
        
        def format_time(ms):
            seconds = (ms // 1000) % 60
            minutes = (ms // 60000) % 60
            return f"{minutes:02}:{seconds:02}"

        t_current = format_time(current_ms)
        t_total = format_time(duration_ms)
        self.lbl_time.setText(f"{t_current} / {t_total}")