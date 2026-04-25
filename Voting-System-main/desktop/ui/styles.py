# ui/styles.py
from config import COLORS

# Main window styles
MAIN_WINDOW_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}
QMenuBar {
    background-color: #ffffff;
    border-bottom: 1px solid #ddd;
}
QMenuBar::item {
    padding: 8px 12px;
}
QMenuBar::item:selected {
    background-color: #4CAF50;
    color: white;
}
QMenu {
    background-color: white;
    border: 1px solid #ddd;
}
QMenu::item {
    padding: 8px 20px;
}
QMenu::item:selected {
    background-color: #4CAF50;
    color: white;
}
"""

# Button styles
PRIMARY_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: #45a049;
}}
QPushButton:pressed {{
    background-color: #3d8b40;
}}
"""

SECONDARY_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {COLORS['secondary']};
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}}
QPushButton:hover {{
    background-color: #1976D2;
}}
"""

DANGER_BUTTON_STYLE = f"""
QPushButton {{
    background-color: {COLORS['danger']};
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}}
QPushButton:hover {{
    background-color: #d32f2f;
}}
"""

# Card style
CARD_STYLE = """
QGroupBox {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-top: 10px;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}
"""

# Table style
TABLE_STYLE = """
QTableView {
    background-color: white;
    alternate-background-color: #f9f9f9;
    selection-background-color: #4CAF50;
    selection-color: white;
    gridline-color: #ddd;
    border: 1px solid #ddd;
}
QHeaderView::section {
    background-color: #f0f0f0;
    padding: 8px;
    border: 1px solid #ddd;
    font-weight: bold;
}
"""

# Input style
INPUT_STYLE = """
QLineEdit, QTextEdit, QComboBox, QDateTimeEdit {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #4CAF50;
}
"""