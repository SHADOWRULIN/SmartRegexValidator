import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QComboBox, 
                             QGraphicsView, QGraphicsScene)
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QTimer, QRectF
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
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_next_step)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Top Bar
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton("⬅ Back")
        self.back_btn.setFixedSize(100, 35)
        self.back_btn.setStyleSheet("""
            QPushButton { background-color: #020100; color: #FDFFFC; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #235789; }
        """)
        self.back_btn.clicked.connect(self.go_back)
        
        title = QLabel("DFA Simulator")
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
        self.target_selector.setStyleSheet("padding: 5px; font-size: 14px; border: 1px solid #235789;")
        
        self.start_sim_btn = QPushButton("▶ Start Animation")
        self.start_sim_btn.setStyleSheet("""
            QPushButton { background-color: #235789; color: #FDFFFC; padding: 8px 15px; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #163859; }
        """)
        self.start_sim_btn.clicked.connect(self.start_animation)

        # Zoom Controls
        self.zoom_in_btn = QPushButton("🔍 +")
        self.zoom_out_btn = QPushButton("🔍 -")
        self.zoom_fit_btn = QPushButton("🔄 Fit")
        for btn in [self.zoom_in_btn, self.zoom_out_btn, self.zoom_fit_btn]:
            btn.setStyleSheet("""
                QPushButton { background-color: #F1D302; color: #020100; padding: 8px; font-weight: bold; border-radius: 5px; }
                QPushButton:hover { background-color: #d4b902; }
            """)
        self.zoom_in_btn.clicked.connect(lambda: self.image_view.scale(1.2, 1.2))
        self.zoom_out_btn.clicked.connect(lambda: self.image_view.scale(0.8, 0.8))
        self.zoom_fit_btn.clicked.connect(self.fit_image_in_view)
        
        controls.addWidget(QLabel("Target:"))
        controls.addWidget(self.target_selector)
        controls.addWidget(self.start_sim_btn)
        controls.addStretch()
        controls.addWidget(self.zoom_in_btn)
        controls.addWidget(self.zoom_out_btn)
        controls.addWidget(self.zoom_fit_btn)

        # Display Layer: Graphics View (Zoom/Pan) and Log
        display_layout = QHBoxLayout()
        
        # QGraphicsView replaces QLabel for native zooming and panning
        self.image_scene = QGraphicsScene()
        self.image_view = QGraphicsView(self.image_scene)
        self.image_view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.image_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag) # Click and drag to pan
        self.image_view.setStyleSheet("background-color: #FDFFFC; border: 2px solid #235789; border-radius: 5px;")
        
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("background-color: #020100; color: #F1D302; font-family: Consolas, monospace; font-size: 14px; padding: 10px; border-radius: 5px;")
        
        display_layout.addWidget(self.image_view, stretch=6)
        display_layout.addWidget(self.log_box, stretch=4)
        
        self.status_label = QLabel("Ready to simulate.")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #235789; margin-top: 5px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(top_bar)
        layout.addLayout(controls)
        layout.addLayout(display_layout)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def load_data(self, email, password):
        self.email_data = email
        self.password_data = password
        self.target_selector.setCurrentIndex(0)
        self.setup_simulation()

    def fit_image_in_view(self):
        """Scales the view so the entire diagram fits perfectly."""
        self.image_view.fitInView(self.image_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def setup_simulation(self):
            self.timer.stop()
            self.log_box.clear()
            self.status_label.setText("Ready to simulate.")
            self.status_label.setStyleSheet("color: #020100; font-size: 18px; font-weight: bold;")
            
            selection = self.target_selector.currentText()
            
            if selection == "Email DFA":
                img_path = "assets/email_dfa_base.png"     # <--- ADDED _base
                self.current_prefix = "email_dfa"          # <--- ADDED PREFIX
                self.is_accepted, self.current_log = simulate_email_dfa(self.email_data)
                self.log_box.append(f"--- INITIALIZING EMAIL DFA ---\nInput String: {self.email_data}\n")
            else:
                img_path = "assets/password_dfa_base.png"  # <--- ADDED _base
                self.current_prefix = "password_dfa"       # <--- ADDED PREFIX
                self.is_accepted, self.current_log = simulate_password_dfa(self.password_data)
                self.log_box.append(f"--- INITIALIZING PASSWORD DFA ---\nInput String: {self.password_data}\n")
                
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
                
                # 1. Update the Text Log
                if char == 'END':
                    log_entry = f">> Final Status: {step_data['status']}"
                else:
                    log_entry = f"Read '{char}' | {f_state} ➔ {t_state}"
                self.log_box.append(log_entry)
                
                # 2. Update the Diagram Image (Live Highlight)
                safe_state_name = t_state.replace(" / ", "_").replace(" ", "_")
                highlight_img_path = f"assets/{self.current_prefix}_{safe_state_name}.png"
                
                if os.path.exists(highlight_img_path):
                    pixmap = QPixmap(highlight_img_path)
                    self.image_scene.clear()
                    self.image_scene.addPixmap(pixmap)
                    # We don't call fit_image_in_view() here so it doesn't glitch while zoomed in!
                    
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