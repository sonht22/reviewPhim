# ui/styles.py

DARK_THEME_QSS = """
QMainWindow {
    background-color: #1e1e1e;
}
QWidget {
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
    /* XÓA DÒNG font-size: 14px; ĐI */
}

/* Nếu muốn set font riêng cho nút hoặc nhãn thì set cụ thể như này sẽ không lỗi */
QPushButton, QLabel, QTextEdit {
    font-size: 14px; 
}
QFrame.panel {
    background-color: #252526;
    border: 1px solid #3e3e42;
    border-radius: 6px;
}
QPushButton {
    background-color: #00b5b5;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #00dcd8;
}
QPushButton.secondary {
    background-color: #3e3e42;
}
QListWidget {
    background-color: #2d2d30;
    border: none;
}
QLineEdit, QTextEdit {
    background-color: #1e1e1e;
    border: 1px solid #3e3e42;
    color: white;
    padding: 5px;
}
"""