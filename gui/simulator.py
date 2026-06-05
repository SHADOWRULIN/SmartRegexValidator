import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QComboBox, QFrame)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer
from automata.email_dfa import simulate_email_dfa
from automata.password_dfa import simulate_password_dfa

class SimulatorPage(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.current_log = []
        self.current_step = 0
        self.email_data = ""
        self.password_data = ""
        
        # Timer for the animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_next_step)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Top Bar: Back Button and Title
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton("Back to Validator")
        self.back_btn.setFixedSize(150, 30)
        self.back_btn.setStyleSheet("background-color: #7f8c8d; color: white; border-radius: 5px;")
        self.back_btn.clicked.connect(self.go_back)
        
        title = QLabel("Theory of Automata: DFA Simulator")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        top_bar.addWidget(self.back_btn)
        top_bar.addWidget(title)
        top_bar.addStretch()
        
        # Controls Layer
        controls = QHBoxLayout()
        self.target_selector = QComboBox()
        self.target_selector.addItems(["Email DFA", "Password DFA"])
        self.target_selector.currentIndexChanged.connect(self.setup_simulation)
        self.target_selector.setStyleSheet("padding: 5px; font-size: 14px;")
        
        self.start_sim_btn = QPushButton("▶ Start Animation")
        self.start_sim_btn.setStyleSheet("background-color: #2980b9; color: white; padding: 5px 15px; font-weight: bold; border-radius: 5px;")
        self.start_sim_btn.clicked.connect(self.start_animation)
        
        controls.addWidget(QLabel("Select Target:"))
        controls.addWidget(self.target_selector)
        controls.addWidget(self.start_sim_btn)
        controls.addStretch()

        # Display Layer: Diagram (Left) and Log (Right)
        display_layout = QHBoxLayout()
        
        # Diagram Image
        self.image_label = QLabel("Diagram will load here...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: white; border: 1px solid #bdc3c7; border-radius: 5px;")
        self.image_label.setMinimumSize(400, 300)
        
        # Transition Log
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("background-color: #2c3e50; color: #ecf0f1; font-family: Consolas, monospace; font-size: 14px; padding: 10px;")
        
        display_layout.addWidget(self.image_label, stretch=6)
        display_layout.addWidget(self.log_box, stretch=4)
        
        # Status Label
        self.status_label = QLabel("Ready to simulate.")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Assemble Main Layout
        layout.addLayout(top_bar)
        layout.addSpacing(10)
        layout.addLayout(controls)
        layout.addLayout(display_layout)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def load_data(self, email, password):
        """Called by main.py to inject the strings typed by the user."""
        self.email_data = email
        self.password_data = password
        self.target_selector.setCurrentIndex(0)
        self.setup_simulation()

    def setup_simulation(self):
        """Prepares the UI based on whether Email or Password is selected."""
        self.timer.stop()
        self.log_box.clear()
        self.status_label.setText("Ready to simulate.")
        self.status_label.setStyleSheet("color: black; font-size: 18px; font-weight: bold;")
        
        selection = self.target_selector.currentText()
        
        if selection == "Email DFA":
            img_path = "assets/email_dfa.png"
            self.is_accepted, self.current_log = simulate_email_dfa(self.email_data)
            self.log_box.append(f"--- INITIALIZING EMAIL DFA ---\nInput String: {self.email_data}\n")
        else:
            img_path = "assets/password_dfa.png"
            self.is_accepted, self.current_log = simulate_password_dfa(self.password_data)
            self.log_box.append(f"--- INITIALIZING PASSWORD DFA ---\nInput String: {self.password_data}\n")
            
        # Load Image if it exists
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            # Scale image to fit the label while keeping aspect ratio
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.image_label.setText("Diagram image not found.\nPlease run graph_generator.py first.")

    def start_animation(self):
        """Begins reading the transition log."""
        self.setup_simulation() # Reset first
        self.current_step = 0
        self.start_sim_btn.setEnabled(False)
        self.target_selector.setEnabled(False)
        self.status_label.setText("Processing String...")
        self.status_label.setStyleSheet("color: #f39c12; font-size: 18px; font-weight: bold;") # Orange
        
        # Fire the timer every 600 milliseconds (0.6 seconds)
        self.timer.start(600)

    def animate_next_step(self):
        """Processes one character transition and updates the log."""
        if self.current_step < len(self.current_log):
            step_data = self.current_log[self.current_step]
            char = step_data['char']
            f_state = step_data['from_state']
            t_state = step_data['to_state']
            
            if char == 'END':
                log_entry = f">> Final Status: {step_data['status']}"
            else:
                log_entry = f"Read '{char}' | {f_state} ➔ {t_state}"
                
            self.log_box.append(log_entry)
            self.current_step += 1
        else:
            # Animation finished
            self.timer.stop()
            self.start_sim_btn.setEnabled(True)
            self.target_selector.setEnabled(True)
            
            if self.is_accepted:
                self.status_label.setText("FINAL RESULT: STRING ACCEPTED")
                self.status_label.setStyleSheet("color: #27ae60; font-size: 22px; font-weight: bold;") # Green
                self.log_box.append("\n==> AUTOMATA HALTED: ACCEPTED")
            else:
                self.status_label.setText("FINAL RESULT: STRING REJECTED")
                self.status_label.setStyleSheet("color: #c0392b; font-size: 22px; font-weight: bold;") # Red
                self.log_box.append("\n==> AUTOMATA HALTED: REJECTED")

    def go_back(self):
        """Stops the animation and returns to the validator page."""
        self.timer.stop()
        self.go_back_callback()