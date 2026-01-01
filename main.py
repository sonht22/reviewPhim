import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow 

def main():
    # 1. Khởi tạo ứng dụng
    app = QApplication(sys.argv)
    
    # 2. Khởi tạo cửa sổ chính
    window = MainWindow()
    window.show()
    
    # 3. Chạy vòng lặp sự kiện (giữ app luôn chạy)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()