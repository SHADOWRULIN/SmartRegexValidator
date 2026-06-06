from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, switch_to_validator_callback):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Interactive DFA Simulator")
        # Baltic Blue text
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #235789; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Validate Email and Password using DFA Simulation\nTheory of Automata Project")
        subtitle.setStyleSheet("font-size: 18px; color: #020100; margin-bottom: 40px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        start_btn = QPushButton("Start Validation")
        start_btn.setFixedSize(220, 55)
        # Adding hover and click animation effects
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #235789;
                color: #FDFFFC;
                font-size: 18px;
                font-weight: bold;
                border-radius: 8px;
                border: 2px solid #235789;
            }
            QPushButton:hover {
                background-color: #FDFFFC;
                color: #235789;
            }
            QPushButton:pressed {
                background-color: #F1D302;
                color: #020100;
                border: 2px solid #F1D302;
            }
        """)
        start_btn.clicked.connect(switch_to_validator_callback)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)