import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont  # <--- THÊM DÒNG NÀY

# Import giao diện chính
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # === [FIX LỖI FONT SIZE -1] ===
    # Thiết lập font mặc định cho toàn bộ ứng dụng ngay từ đầu
    # Bạn có thể đổi "Segoe UI" thành "Arial" hoặc "Roboto" tùy thích
    default_font = QFont("Segoe UI", 10) 
    app.setFont(default_font)
    # ==============================

    # Khởi tạo cửa sổ chính
    window = MainWindow()
    window.show()

    # Chạy vòng lặp sự kiện
    sys.exit(app.exec())

if __name__ == "__main__":
    main()