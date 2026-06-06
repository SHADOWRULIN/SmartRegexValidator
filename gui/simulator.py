import os
import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QComboBox, 
                             QGraphicsView, QGraphicsScene)
from PyQt6.QtGui import QPixmap, QPainter, QCursor
from PyQt6.QtCore import Qt, QTimer, QRectF
from automata.email_dfa import simulate_email_dfa
from automata.password_dfa import simulate_password_dfa

# Dynamically calculate the root directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SimulatorPage(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.current_log = []
        self.current_step = 0
        self.email_data = ""
        self.password_data = ""
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_next_step)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Top Bar
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back_btn.setFixedSize(100, 35)
        self.back_btn.setStyleSheet("""
            QPushButton { background-color: #020100; color: #FDFFFC; font-weight: bold; border-radius: 5px; font-size: 14px;}
            QPushButton:hover { background-color: #235789; }
        """)
        self.back_btn.clicked.connect(self.go_back)
        
        title = QLabel("DFA Live Simulator")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #235789;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        top_bar.addWidget(self.back_btn)
        top_bar.addWidget(title)
        top_bar.addStretch()
        
        # Controls Layer
        controls = QHBoxLayout()
        self.target_selector = QComboBox()
        self.target_selector.addItems(["Email DFA", "Password DFA"])
        self.target_selector.currentIndexChanged.connect(self.setup_simulation)
        self.target_selector.setStyleSheet("padding: 5px; font-size: 14px; border: 1px solid #235789; border-radius: 4px; background: white;")
        
        self.start_sim_btn = QPushButton("► Start")
        self.start_sim_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.start_sim_btn.setStyleSheet("""
            QPushButton { background-color: #235789; color: #FDFFFC; padding: 6px 20px; font-weight: bold; border-radius: 4px; font-size: 14px;}
            QPushButton:hover { background-color: #1a4166; }
        """)
        self.start_sim_btn.clicked.connect(self.start_animation)

        # Zoom Controls with clean typography
        self.zoom_in_btn = QPushButton("+ Zoom In")
        self.zoom_out_btn = QPushButton("- Zoom Out")
        self.zoom_fit_btn = QPushButton("⛶ Fit")
        for btn in [self.zoom_in_btn, self.zoom_out_btn, self.zoom_fit_btn]:
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton { background-color: #F1D302; color: #020100; padding: 6px 12px; font-weight: bold; border-radius: 4px; font-size: 13px;}
                QPushButton:hover { background-color: #d4b902; }
            """)
        self.zoom_in_btn.clicked.connect(lambda: self.image_view.scale(1.2, 1.2))
        self.zoom_out_btn.clicked.connect(lambda: self.image_view.scale(0.8, 0.8))
        self.zoom_fit_btn.clicked.connect(self.fit_image_in_view)
        
        controls.addWidget(QLabel("Select Target:"))
        controls.addWidget(self.target_selector)
        controls.addWidget(self.start_sim_btn)
        controls.addStretch()
        controls.addWidget(self.zoom_in_btn)
        controls.addWidget(self.zoom_out_btn)
        controls.addWidget(self.zoom_fit_btn)

        # Display Layer
        display_layout = QHBoxLayout()
        
        # Diagram Viewer
        self.image_scene = QGraphicsScene()
        self.image_view = QGraphicsView(self.image_scene)
        self.image_view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.image_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.image_view.setStyleSheet("background-color: white; border: 2px solid #235789; border-radius: 8px;")
        
        # Log Box
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("""
            QTextEdit {
                background-color: #020100; 
                color: #F1D302; 
                font-family: Consolas, monospace; 
                font-size: 14px; 
                padding: 15px; 
                border-radius: 8px;
                border: 2px solid #235789;
            }
        """)
        
        display_layout.addWidget(self.image_view, stretch=6)
        display_layout.addWidget(self.log_box, stretch=4)
        
        self.status_label = QLabel("Ready to simulate.")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #235789; margin-top: 10px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(top_bar)
        layout.addSpacing(10)
        layout.addLayout(controls)
        layout.addSpacing(10)
        layout.addLayout(display_layout, stretch=1) # Forces this layout to expand
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def load_data(self, email, password):
        self.email_data = email
        self.password_data = password
        self.target_selector.setCurrentIndex(0)
        self.setup_simulation()

    def fit_image_in_view(self):
        self.image_view.fitInView(self.image_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def setup_simulation(self):
        self.timer.stop()
        self.log_box.clear()
        self.status_label.setText("Ready to simulate.")
        self.status_label.setStyleSheet("color: #020100; font-size: 18px; font-weight: bold;")
        
        selection = self.target_selector.currentText()
        
        if selection == "Email DFA":
            img_name = "email_dfa_base.png"
            self.current_prefix = "email_dfa"
            self.is_accepted, self.current_log = simulate_email_dfa(self.email_data)
            self.log_box.append(f"--- INITIALIZING EMAIL DFA ---\nInput String: {self.email_data}\n")
        else:
            img_name = "password_dfa_base.png"
            self.current_prefix = "password_dfa"
            self.is_accepted, self.current_log = simulate_password_dfa(self.password_data)
            self.log_box.append(f"--- INITIALIZING PASSWORD DFA ---\nInput String: {self.password_data}\n")
            
        # OPTIMIZED: Absolute path combination
        img_path = os.path.join(BASE_DIR, "assets", img_name)
            
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            self.image_scene.clear()
            self.image_scene.addPixmap(pixmap)
            self.image_scene.setSceneRect(QRectF(pixmap.rect()))
            self.fit_image_in_view()
        else:
            self.log_box.append("\n[!] Diagram image not found.")

    def start_animation(self):
        self.setup_simulation()
        self.current_step = 0
        self.start_sim_btn.setEnabled(False)
        self.target_selector.setEnabled(False)
        self.status_label.setText("Processing String...")
        self.status_label.setStyleSheet("color: #F1D302; font-size: 18px; font-weight: bold;") 
        
        self.timer.start(600)

    def animate_next_step(self):
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
            
            safe_state_name = t_state.replace(" / ", "_").replace(" ", "_")
            highlight_img_name = f"{self.current_prefix}_{safe_state_name}.png"
            
            # OPTIMIZED: Absolute path combination
            highlight_img_path = os.path.join(BASE_DIR, "assets", highlight_img_name)
            
            if os.path.exists(highlight_img_path):
                pixmap = QPixmap(highlight_img_path)
                self.image_scene.clear()
                self.image_scene.addPixmap(pixmap)
                
            self.current_step += 1
        else:
            self.timer.stop()
            self.start_sim_btn.setEnabled(True)
            self.target_selector.setEnabled(True)
            
            if self.is_accepted:
                self.status_label.setText("FINAL RESULT: STRING ACCEPTED")
                self.status_label.setStyleSheet("color: #27ae60; font-size: 22px; font-weight: bold;")
                self.log_box.append("\n==> AUTOMATA HALTED: ACCEPTED")
            else:
                self.status_label.setText("FINAL RESULT: STRING REJECTED")
                self.status_label.setStyleSheet("color: #C1292E; font-size: 22px; font-weight: bold;") 
                self.log_box.append("\n==> AUTOMATA HALTED: REJECTED")

    def go_back(self):
        self.timer.stop()
        self.go_back_callback()