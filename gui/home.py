from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, switch_to_validator_callback):
        super().__init__()
        
        # Set up a vertical layout, centered
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title Label
        title = QLabel("Smart Regex Validator")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtitle Label
        subtitle = QLabel("Validate Email and Password using DFA Simulation\nTheory of Automata Project")
        subtitle.setStyleSheet("font-size: 18px; color: #7f8c8d; margin-bottom: 40px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Start Button
        start_btn = QPushButton("Start Validation")
        start_btn.setFixedSize(200, 50)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        # When clicked, trigger the function passed from main.py
        start_btn.clicked.connect(switch_to_validator_callback)
        
        # Add everything to the layout
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)