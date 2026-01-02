from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel

class ScriptPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. Tạo Layout
        layout = QVBoxLayout()
        
        # 2. Tạo Tiêu đề
        lbl_title = QLabel("📝 KỊCH BẢN AI (GENERATED SCRIPT)")
        layout.addWidget(lbl_title)

        # 3. Tạo ô chứa văn bản (Đây là cái self.text_area bị thiếu)
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Kịch bản sau khi AI phân tích sẽ hiện ở đây...")
        self.text_area.setReadOnly(True) # Chỉ cho đọc, không cho sửa tay (tùy bạn)
        layout.addWidget(self.text_area)
        
        # 4. Set layout cho Panel
        self.setLayout(layout)

    def update_data(self, segments):
        """
        Hàm này được MainWindow gọi khi AI chạy xong.
        Nhiệm vụ: Hiển thị danh sách segments lên màn hình.
        """
        if not hasattr(self, 'text_area'):
            print("❌ Lỗi: Chưa khởi tạo text_area trong ScriptPanel")
            return

        self.text_area.clear()
        
        # Header
        self.text_area.append(f"✅ ĐÃ TẠO THÀNH CÔNG: {len(segments)} PHÂN ĐOẠN")
        self.text_area.append("="*40 + "\n")

        # Loop qua từng segment để hiển thị
        for seg in segments:
            # Lấy thông tin từ object
            start = seg.visual_time.start
            end = seg.visual_time.end
            script = seg.script
            visual = seg.visual_description
            
            # Format text hiển thị đẹp mắt
            display_text = (
                f"🎬 SEGMENT #{seg.id}  [{start} --> {end}]\n"
                f"🗣️ Lời thoại: {script}\n"
                f"👀 Hình ảnh: {visual}\n"
                f"{'-'*30}"
            )
            
            self.text_area.append(display_text)