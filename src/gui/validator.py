from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtCore import Qt
from regex.patterns import validate_email, validate_password

class ValidatorPage(QWidget):
    def __init__(self, switch_to_simulator_callback):
        super().__init__()
        self.switch_to_simulator_callback = switch_to_simulator_callback
        
        # Main Layout wrapper to keep the form centered even when maximized
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Regex Validation")
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #235789; margin-bottom: 30px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Form Container (Modern Card Style)
        form_frame = QFrame()
        form_frame.setMinimumWidth(500)
        form_frame.setMaximumWidth(700)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
            QLabel { font-size: 15px; font-weight: bold; color: #235789; margin-top: 10px;}
            QLineEdit {
                padding: 12px;
                font-size: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: #FDFFFC;
                color: #020100;
            }
            QLineEdit:focus {
                border: 2px solid #235789;
            }
        """)
        
        # Add Drop Shadow to the Card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 5)
        form_frame.setGraphicsEffect(shadow)
        
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(10)
        
        # Email Input
        self.email_label = QLabel("Email Address")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("e.g., user@domain.com")
        self.email_result = QLabel("")
        self.email_result.setStyleSheet("font-size: 13px; font-weight: bold; margin-top: 2px; border: none;")
        self.email_result.hide() # Hidden initially
        
        # Password Input with Clean Toggle
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Minimum 8 chars, 1 Upper, 1 Lower, 1 Digit")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.toggle_pwd_btn = QPushButton("Show")
        self.toggle_pwd_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggle_pwd_btn.setStyleSheet("""
            QPushButton { border: none; font-size: 14px; font-weight: bold; color: #7f8c8d; background: transparent; padding: 0 10px; }
            QPushButton:hover { color: #235789; }
        """)
        self.toggle_pwd_btn.clicked.connect(self.toggle_password)
        
        pwd_layout = QHBoxLayout()
        pwd_layout.setContentsMargins(0,0,0,0)
        pwd_layout.addWidget(self.password_input)
        pwd_layout.addWidget(self.toggle_pwd_btn)
        
        self.password_result = QLabel("")
        self.password_result.setStyleSheet("font-size: 13px; font-weight: bold; margin-top: 2px; border: none;")
        self.password_result.hide()
        
        # Add widgets to form layout
        form_layout.addWidget(self.email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.email_result)
        form_layout.addSpacing(15)
        form_layout.addWidget(self.password_label)
        form_layout.addLayout(pwd_layout)
        form_layout.addWidget(self.password_result)
        form_frame.setLayout(form_layout)
        
        # Buttons Setup
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.validate_btn = QPushButton("Validate Inputs")
        self.validate_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.validate_btn.setFixedSize(300, 45)
        self.validate_btn.setStyleSheet("""
            QPushButton { background-color: #235789; color: #FDFFFC; font-size: 16px; font-weight: bold; border-radius: 8px; border: none; }
            QPushButton:hover { background-color: #1a4166; }
            QPushButton:pressed { background-color: #112a42; }
        """)
        self.validate_btn.clicked.connect(self.run_validation)
        
        self.simulate_btn = QPushButton("Simulate DFA ►")
        self.simulate_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.simulate_btn.setFixedSize(300, 45)
        self.simulate_btn.setStyleSheet("""
            QPushButton { background-color: #F1D302; color: #020100; font-size: 16px; font-weight: bold; border-radius: 8px; border: none; }
            QPushButton:hover { background-color: #d4b902; }
            QPushButton:pressed { background-color: #b39b02; }
        """)
        self.simulate_btn.hide()
        self.simulate_btn.clicked.connect(self.trigger_simulation)
        
        button_layout.addWidget(self.validate_btn)
        button_layout.addWidget(self.simulate_btn)
        
        # Assemble Page
        main_layout.addWidget(title)
        main_layout.addWidget(form_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(30)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def toggle_password(self):
        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pwd_btn.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pwd_btn.setText("Show")

    def run_validation(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        # Track if both fields have at least some text
        has_input = True
        
        self.email_result.show()
        if not email:
            self.email_result.setText("⚠ Email field cannot be empty.")
            self.email_result.setStyleSheet("color: #C1292E; font-size: 13px; font-weight: bold; margin-top: 2px;")
            has_input = False
        elif validate_email(email):
            self.email_result.setText("✓ Valid Email Address")
            self.email_result.setStyleSheet("color: #27ae60; font-size: 13px; font-weight: bold; margin-top: 2px;")
        else:
            self.email_result.setText("✗ Invalid: Check for missing '@' or domain")
            self.email_result.setStyleSheet("color: #C1292E; font-size: 13px; font-weight: bold; margin-top: 2px;")
            
        self.password_result.show()
        if not password:
            self.password_result.setText("⚠ Password field cannot be empty.")
            self.password_result.setStyleSheet("color: #C1292E; font-size: 13px; font-weight: bold; margin-top: 2px;")
            has_input = False
        elif validate_password(password):
            self.password_result.setText("✓ Strong Password")
            self.password_result.setStyleSheet("color: #27ae60; font-size: 13px; font-weight: bold; margin-top: 2px;")
        else:
            self.password_result.setText("✗ Invalid: Needs 8 chars, 1 Upper, 1 Lower, 1 Digit")
            self.password_result.setStyleSheet("color: #C1292E; font-size: 13px; font-weight: bold; margin-top: 2px;")
            
        # Only show the simulation button if they actually typed something to simulate
        if has_input:
            self.simulate_btn.show()
        else:
            self.simulate_btn.hide()

    def trigger_simulation(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        self.switch_to_simulator_callback(email, password)