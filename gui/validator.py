from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from regex.patterns import validate_email, validate_password

class ValidatorPage(QWidget):
    def __init__(self, switch_to_simulator_callback):
        super().__init__()
        self.switch_to_simulator_callback = switch_to_simulator_callback
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Regex Validation")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #235789; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #FDFFFC;
                border: 2px solid #235789;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel { font-size: 15px; font-weight: bold; color: #020100; }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #235789;
                border-radius: 4px;
                background-color: #FDFFFC;
                color: #020100;
            }
        """)
        form_layout = QVBoxLayout()
        
        # Email Input
        self.email_label = QLabel("Email Address:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("e.g., john123@gmail.com")
        self.email_result = QLabel("")
        
        # Password Input with Toggle
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("e.g., Abc12345")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.toggle_pwd_btn = QPushButton("👁")
        self.toggle_pwd_btn.setFixedSize(40, 40)
        self.toggle_pwd_btn.setStyleSheet("border: none; font-size: 20px; background: transparent; color: #235789;")
        self.toggle_pwd_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_pwd_btn.clicked.connect(self.toggle_password)
        
        pwd_layout = QHBoxLayout()
        pwd_layout.addWidget(self.password_input)
        pwd_layout.addWidget(self.toggle_pwd_btn)
        self.password_result = QLabel("")
        
        form_layout.addWidget(self.email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.email_result)
        form_layout.addSpacing(15)
        form_layout.addWidget(self.password_label)
        form_layout.addLayout(pwd_layout)
        form_layout.addWidget(self.password_result)
        form_frame.setLayout(form_layout)
        
        # Buttons with Hover Effects
        button_style = """
            QPushButton {
                background-color: %s;
                color: %s; padding: 12px; font-size: 16px; font-weight: bold; border-radius: 6px;
            }
            QPushButton:hover { background-color: #FDFFFC; color: %s; border: 2px solid %s; }
        """
        self.validate_btn = QPushButton("Validate with Regex")
        self.validate_btn.setStyleSheet(button_style % ("#235789", "#FDFFFC", "#235789", "#235789"))
        self.validate_btn.clicked.connect(self.run_validation)
        
        self.simulate_btn = QPushButton("View DFA Simulation ➔")
        self.simulate_btn.setStyleSheet(button_style % ("#F1D302", "#020100", "#020100", "#F1D302"))
        self.simulate_btn.hide()
        self.simulate_btn.clicked.connect(self.trigger_simulation)
        
        layout.addWidget(title)
        layout.addWidget(form_frame)
        layout.addSpacing(20)
        layout.addWidget(self.validate_btn)
        layout.addWidget(self.simulate_btn)
        
        self.setLayout(layout)

    def toggle_password(self):
        """Switches between Password and Normal text display."""
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pwd_btn.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pwd_btn.setText("👁")

    def run_validation(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if validate_email(email):
            self.email_result.setText("✓ Valid Email")
            self.email_result.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.email_result.setText("✗ Invalid Email (Missing @ or domain)")
            self.email_result.setStyleSheet("color: #C1292E; font-weight: bold;") # Flag Red
            
        if validate_password(password):
            self.password_result.setText("✓ Valid Password")
            self.password_result.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.password_result.setText("✗ Invalid Password (Needs 8 chars, 1 Upper, 1 Lower, 1 Digit)")
            self.password_result.setStyleSheet("color: #C1292E; font-weight: bold;") # Flag Red
            
        self.simulate_btn.show()

    def trigger_simulation(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        self.switch_to_simulator_callback(email, password)