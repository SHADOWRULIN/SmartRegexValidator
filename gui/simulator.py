import os
import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QComboBox, 
                             QGraphicsView, QGraphicsScene, QFileDialog,
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtGui import QPixmap, QPainter, QCursor
from PyQt6.QtCore import Qt, QTimer, QRectF
from automata.email_dfa import simulate_email_dfa
from automata.password_dfa import simulate_password_dfa

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SimulatorPage(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.current_log = []
        self.current_step = 0
        self.email_data = ""
        self.password_data = ""
        self.is_paused = False
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_next_step)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Top Bar
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        self.back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.back_btn.setFixedSize(100, 35)
        self.back_btn.setStyleSheet("QPushButton { background-color: #020100; color: #FDFFFC; font-weight: bold; border-radius: 5px; font-size: 14px;} QPushButton:hover { background-color: #235789; }")
        self.back_btn.clicked.connect(self.go_back)
        
        title = QLabel("Theory of Automata: DFA Live Simulator")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #235789;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        top_bar.addWidget(self.back_btn)
        top_bar.addWidget(title)
        top_bar.addStretch()
        
        # --- ROW 1: Configuration & Main Actions ---
        controls_row1 = QHBoxLayout()
        
        self.target_selector = QComboBox()
        self.target_selector.addItems(["Email DFA", "Password DFA"])
        self.target_selector.currentIndexChanged.connect(self.setup_simulation)
        self.target_selector.setStyleSheet("padding: 5px; font-size: 14px; border: 1px solid #235789; border-radius: 4px; background: white;")
        
        self.speed_selector = QComboBox()
        self.speed_selector.addItems(["Speed: Normal", "Speed: Slow", "Speed: Fast"])
        self.speed_selector.setStyleSheet("padding: 5px; font-size: 14px; border: 1px solid #235789; border-radius: 4px; background: white;")
        
        self.start_sim_btn = QPushButton("Start Automata")
        self.start_sim_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.start_sim_btn.setStyleSheet("QPushButton { background-color: #235789; color: #FDFFFC; padding: 6px 20px; font-weight: bold; border-radius: 4px; font-size: 14px;} QPushButton:hover { background-color: #1a4166; }")
        self.start_sim_btn.clicked.connect(self.start_animation)

        self.export_btn = QPushButton("Export Report")
        self.export_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.export_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: #FDFFFC; padding: 6px 20px; font-weight: bold; border-radius: 4px; font-size: 14px;} QPushButton:hover { background-color: #219653; } QPushButton:disabled { background-color: #95a5a6; color: #ecf0f1; }")
        self.export_btn.clicked.connect(self.export_report)
        self.export_btn.setEnabled(False) 

        controls_row1.addWidget(QLabel("Target Language:"))
        controls_row1.addWidget(self.target_selector)
        controls_row1.addWidget(self.speed_selector)
        controls_row1.addWidget(self.start_sim_btn)
        controls_row1.addWidget(self.export_btn)
        controls_row1.addStretch()

        # --- ROW 2: Playback & Zoom Controls ---
        controls_row2 = QHBoxLayout()

        self.step_back_btn = QPushButton("Back Step")
        self.pause_btn = QPushButton("Pause")
        self.step_fwd_btn = QPushButton("Next Step")
        
        for btn in [self.step_back_btn, self.pause_btn, self.step_fwd_btn]:
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("QPushButton { background-color: #34495e; color: white; padding: 6px 15px; font-weight: bold; border-radius: 4px; font-size: 14px;} QPushButton:hover { background-color: #2c3e50; } QPushButton:disabled { background-color: #bdc3c7; color: #ecf0f1; }")
            btn.setEnabled(False)
            
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.step_back_btn.clicked.connect(self.step_backward)
        self.step_fwd_btn.clicked.connect(self.step_forward)

        self.zoom_in_btn = QPushButton("Zoom In")
        self.zoom_out_btn = QPushButton("Zoom Out")
        self.zoom_fit_btn = QPushButton("Fit Viewer")
        
        for btn in [self.zoom_in_btn, self.zoom_out_btn, self.zoom_fit_btn]:
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet("QPushButton { background-color: #F1D302; color: #020100; padding: 6px 15px; font-weight: bold; border-radius: 4px; font-size: 13px;} QPushButton:hover { background-color: #d4b902; }")
            
        self.zoom_in_btn.clicked.connect(lambda: self.image_view.scale(1.2, 1.2))
        self.zoom_out_btn.clicked.connect(lambda: self.image_view.scale(0.8, 0.8))
        self.zoom_fit_btn.clicked.connect(self.fit_image_in_view)
        
        controls_row2.addWidget(QLabel("Playback Controls:"))
        controls_row2.addWidget(self.step_back_btn)
        controls_row2.addWidget(self.pause_btn)
        controls_row2.addWidget(self.step_fwd_btn)
        controls_row2.addStretch()
        controls_row2.addWidget(self.zoom_in_btn)
        controls_row2.addWidget(self.zoom_out_btn)
        controls_row2.addWidget(self.zoom_fit_btn)

        # TOA Specifics: Formal Language & Input Tape
        toa_layout = QVBoxLayout()
        self.language_label = QLabel("Formal Language: L = { username@domain.extension }")
        self.language_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #235789; font-family: monospace;")
        self.language_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.tape_label = QLabel("Input Tape: [ ]")
        self.tape_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #C1292E; background-color: #f0f0f0; padding: 10px; border-radius: 5px; font-family: Consolas, monospace;")
        self.tape_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        toa_layout.addWidget(self.language_label)
        toa_layout.addWidget(self.tape_label)

        # Display Layer (Canvas + Tabs)
        display_layout = QHBoxLayout()
        self.image_scene = QGraphicsScene()
        self.image_view = QGraphicsView(self.image_scene)
        self.image_view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.image_view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.image_view.setStyleSheet("background-color: white; border: 2px solid #235789; border-radius: 8px;")
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 2px solid #235789; border-radius: 8px; }
            QTabBar::tab { background: #e0e0e0; color: #020100; padding: 8px 15px; font-weight: bold; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 2px;}
            QTabBar::tab:selected { background: #235789; color: white; }
        """)
        
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("QTextEdit { background-color: #020100; color: #F1D302; font-family: Consolas, monospace; font-size: 14px; padding: 15px; border: none;}")
        
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_widget.setStyleSheet("QTableWidget { background-color: white; color: black; font-family: Consolas, monospace; font-size: 14px; border: none;}")
        
        self.tabs.addTab(self.log_box, "Live Log")
        self.tabs.addTab(self.table_widget, "Transition Table")
        
        display_layout.addWidget(self.image_view, stretch=6)
        display_layout.addWidget(self.tabs, stretch=4)
        
        self.status_label = QLabel("Machine Halted. Ready for Input.")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #235789; margin-top: 10px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(top_bar)
        layout.addLayout(controls_row1)
        layout.addLayout(controls_row2)
        layout.addSpacing(10)
        layout.addLayout(toa_layout)
        layout.addSpacing(10)
        layout.addLayout(display_layout, stretch=1)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)

    def load_data(self, email, password):
        self.email_data = email
        self.password_data = password
        self.target_selector.setCurrentIndex(0)
        self.setup_simulation()

    def fit_image_in_view(self):
        self.image_view.fitInView(self.image_scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def populate_table(self, headers, rows):
        self.table_widget.clear()
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setHorizontalHeaderLabels(headers)
        for r_idx, row in enumerate(rows):
            for c_idx, item in enumerate(row):
                table_item = QTableWidgetItem(str(item))
                table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table_widget.setItem(r_idx, c_idx, table_item)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def setup_simulation(self):
        self.timer.stop()
        self.is_paused = False
        self.pause_btn.setText("Pause")
        for btn in [self.export_btn, self.pause_btn, self.step_back_btn, self.step_fwd_btn]:
            btn.setEnabled(False)
        
        selection = self.target_selector.currentText()
        if selection == "Email DFA":
            self.language_label.setText("Formal Language: L = { username@domain.extension }")
            self.current_string = self.email_data
            self.current_prefix = "email_dfa"
            self.is_accepted, self.current_log = simulate_email_dfa(self.email_data)
            headers = ["Current State", "letter/num", "@", "."]
            rows = [
                ["→ q0", "q1", "Dead", "Dead"], ["q1", "q1", "q2", "Dead"],
                ["q2", "q3", "Dead", "Dead"], ["q3", "q3", "Dead", "q4"],
                ["q4", "*q5", "Dead", "Dead"], ["*q5 (Accept)", "*q5", "Dead", "Dead"],
                ["Dead", "Dead", "Dead", "Dead"]
            ]
            self.populate_table(headers, rows)
        else:
            self.language_label.setText("Formal Language: L = { Password | len(w) >= 8, contains [A-Z], [a-z], [0-9] }")
            self.current_string = self.password_data
            self.current_prefix = "password_dfa"
            self.is_accepted, self.current_log = simulate_password_dfa(self.password_data)
            headers = ["State", "Upper(U)", "Lower(L)", "Digit(D)"]
            rows = [
                ["→ q0", "q_U", "q_L", "q_D"], ["q_U", "q_U", "q_UL", "q_UD"],
                ["q_L", "q_UL", "q_L", "q_LD"], ["q_D", "q_UD", "q_LD", "q_D"],
                ["q_UL", "q_UL", "q_UL", "q_ULD"], ["q_UD", "q_UD", "q_ULD", "q_UD"],
                ["q_LD", "q_ULD", "q_LD", "q_LD"], ["*q_ULD (Accept)", "*q_ULD", "*q_ULD", "*q_ULD"],
                ["Rejected", "Rejected", "Rejected", "Rejected"]
            ]
            self.populate_table(headers, rows)
            
        self.current_step = 0
        self.update_ui_for_step(0)

    def update_tape(self, index):
        if index < 0:
            self.tape_label.setText(f"Input Tape: [ START ] {' '.join(list(self.current_string))}")
            return
        chars = list(self.current_string)
        if index < len(chars):
            chars[index] = f"[{chars[index]}]" 
        formatted_string = " ".join(chars)
        
        if index >= len(self.current_string):
             self.tape_label.setText(f"Input Tape: {formatted_string} [ END ]")
        else:
             self.tape_label.setText(f"Input Tape: {formatted_string}")

    def update_ui_for_step(self, step_idx):
        # 1. Rebuild Log
        self.log_box.clear()
        selection = self.target_selector.currentText()
        if selection == "Email DFA":
            self.log_box.append(f"--- DFA INITIALIZED ---\nInput: {self.email_data}\n")
        else:
            self.log_box.append(f"--- DFA INITIALIZED ---\nInput: {self.password_data}\n")
            
        for i in range(step_idx):
            step_data = self.current_log[i]
            char = step_data['char']
            if char == 'END':
                self.log_box.append(f">> Final Status: {step_data['status']}")
            else:
                self.log_box.append(f"Read '{char}' | {step_data['from_state']} ➔ {step_data['to_state']}")

        # 2. Update Tape & Image
        if step_idx == 0:
            self.update_tape(-1)
            img_path = os.path.join(BASE_DIR, "assets", f"{self.current_prefix}_base.png")
            self.status_label.setText("Machine Halted. Ready for Input.")
            self.status_label.setStyleSheet("color: #020100; font-size: 18px; font-weight: bold;")
        else:
            self.update_tape(step_idx - 1)
            t_state = self.current_log[step_idx - 1]['to_state']
            safe_name = t_state.replace(" / ", "_").replace(" ", "_")
            img_path = os.path.join(BASE_DIR, "assets", f"{self.current_prefix}_{safe_name}.png")
            
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            self.image_scene.clear()
            self.image_scene.addPixmap(pixmap)
            if step_idx == 0: self.fit_image_in_view()

        # 3. Handle Completion State
        if step_idx == len(self.current_log):
            self.timer.stop()
            result = "ACCEPTED" if self.is_accepted else "REJECTED"
            color = "#27ae60" if self.is_accepted else "#C1292E"
            
            self.status_label.setText(f"LANGUAGE ACCEPTED: {'YES' if self.is_accepted else 'NO'}")
            self.status_label.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: bold;")
            self.log_box.append(f"\n--- SIMULATION STATISTICS ---\nStates Visited: {step_idx}\nTransitions: {step_idx - 1}\nFinal State: {self.current_log[-1]['to_state']}\nResult: {result}\n-----------------------------")
            
            self.start_sim_btn.setEnabled(True)
            self.target_selector.setEnabled(True)
            self.speed_selector.setEnabled(True)
            self.export_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.is_paused = False
            self.pause_btn.setText("Pause")
            self.step_fwd_btn.setEnabled(False)
            self.step_back_btn.setEnabled(True)
        elif step_idx > 0:
            self.status_label.setText("Processing String... (PAUSED)" if self.is_paused else "Processing String...")
            self.status_label.setStyleSheet("color: #F1D302; font-size: 18px; font-weight: bold;")
            self.export_btn.setEnabled(False)
            self.start_sim_btn.setEnabled(False)

    # --- Playback Controls Logic ---
    def toggle_pause(self):
        if self.is_paused:
            self.is_paused = False
            self.pause_btn.setText("Pause")
            self.step_back_btn.setEnabled(False)
            self.step_fwd_btn.setEnabled(False)
            self.status_label.setText("Processing String...")
            
            speed = self.speed_selector.currentText()
            interval = 600
            if "Slow" in speed: interval = 1200
            elif "Fast" in speed: interval = 200
            self.timer.start(interval)
        else:
            self.is_paused = True
            self.timer.stop()
            self.pause_btn.setText("Resume")
            self.status_label.setText("Processing String... (PAUSED)")
            self.step_back_btn.setEnabled(self.current_step > 0)
            self.step_fwd_btn.setEnabled(self.current_step < len(self.current_log))

    def step_backward(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_ui_for_step(self.current_step)
            self.step_back_btn.setEnabled(self.current_step > 0)
            self.step_fwd_btn.setEnabled(True)

    def step_forward(self):
        if self.current_step < len(self.current_log):
            self.current_step += 1
            self.update_ui_for_step(self.current_step)
            self.step_back_btn.setEnabled(True)
            self.step_fwd_btn.setEnabled(self.current_step < len(self.current_log))

    def start_animation(self):
        self.setup_simulation()
        self.current_step = 0
        self.is_paused = False
        self.pause_btn.setEnabled(True)
        self.target_selector.setEnabled(False)
        self.speed_selector.setEnabled(False)
        self.tabs.setCurrentIndex(0) 
        self.status_label.setText("Processing String...")
        self.status_label.setStyleSheet("color: #F1D302; font-size: 18px; font-weight: bold;") 
        
        speed = self.speed_selector.currentText()
        interval = 600
        if "Slow" in speed: interval = 1200
        elif "Fast" in speed: interval = 200
        self.timer.start(interval)

    def animate_next_step(self):
        if self.current_step < len(self.current_log):
            self.current_step += 1
            self.update_ui_for_step(self.current_step)

    def export_report(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Simulation Report", "DFA_Simulation_Report.txt", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("========================================\n  THEORY OF AUTOMATA - DFA SIMULATION   \n========================================\n\n" + self.log_box.toPlainText())
                self.status_label.setText("Report Exported Successfully!")
                self.status_label.setStyleSheet("color: #27ae60; font-size: 18px; font-weight: bold;")
            except Exception:
                self.status_label.setText("Error exporting report.")
                self.status_label.setStyleSheet("color: #C1292E; font-size: 18px; font-weight: bold;")

    def go_back(self):
        self.timer.stop()
        self.go_back_callback()