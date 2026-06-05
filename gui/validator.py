from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from regex.patterns import validate_email, validate_password

class ValidatorPage(QWidget):
    def __init__(self, switch_to_simulator_callback):
        super().__init__()
        self.switch_to_simulator_callback = switch_to_simulator_callback
        
        # Main Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel("Regex Validation")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Input Form Container (Card Style)
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel { 
                font-size: 14px; 
                font-weight: bold;
                color: #2c3e50;  /* Forces the label text to be dark */
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                color: black;    /* Ensures the text you type is also visible */
            }
        """)
        form_layout = QVBoxLayout()
        
        # Email Input
        self.email_label = QLabel("Email Address:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("e.g., john123@gmail.com")
        self.email_result = QLabel("") # Hidden initially
        
        # Password Input
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("e.g., Abc12345")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_result = QLabel("") # Hidden initially
        
        # Add to form layout
        form_layout.addWidget(self.email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.email_result)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.password_result)
        form_frame.setLayout(form_layout)
        
        # Buttons
        self.validate_btn = QPushButton("Validate with Regex")
        self.validate_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.validate_btn.clicked.connect(self.run_validation)
        
        self.simulate_btn = QPushButton("View DFA Simulation ➔")
        self.simulate_btn.setStyleSheet("background-color: #8e44ad; color: white; padding: 10px; font-weight: bold; border-radius: 5px;")
        self.simulate_btn.hide() # Hide until validation is run
        self.simulate_btn.clicked.connect(self.trigger_simulation)
        
        # Add everything to main layout
        layout.addWidget(title)
        layout.addWidget(form_frame)
        layout.addSpacing(20)
        layout.addWidget(self.validate_btn)
        layout.addWidget(self.simulate_btn)
        
        self.setLayout(layout)

    def run_validation(self):
        """Runs the regex engine and updates the UI."""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        # Email Check
        if validate_email(email):
            self.email_result.setText("✓ Valid Email")
            self.email_result.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.email_result.setText("✗ Invalid Email (Missing @ or domain)")
            self.email_result.setStyleSheet("color: red; font-weight: bold;")
            
        # Password Check
        if validate_password(password):
            self.password_result.setText("✓ Valid Password")
            self.password_result.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.password_result.setText("✗ Invalid Password (Needs 8 chars, 1 Upper, 1 Lower, 1 Digit)")
            self.password_result.setStyleSheet("color: red; font-weight: bold;")
            
        # Show the simulate button now that we have inputs
        self.simulate_btn.show()

    def trigger_simulation(self):
        """Passes the inputs to the main window to start the simulation."""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        self.switch_to_simulator_callback(email, password)