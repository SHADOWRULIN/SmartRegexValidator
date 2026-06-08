import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon
from gui.home import HomePage
from gui.validator import ValidatorPage 
from gui.simulator import SimulatorPage

# Get the absolute path of the directory containing main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive DFA-Based Email & Password Validation System")
        
        self.setMinimumSize(900, 650)
        self.resize(1024, 768) 
        
        # OPTIMIZED: Bulletproof absolute path for the logo
        logo_path = os.path.join(BASE_DIR, "assets", "logo.png")
        self.setWindowIcon(QIcon(logo_path))
        
        self.setStyleSheet("background-color: #FDFFFC; color: #020100;")
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.home_page = HomePage(self.show_validator)
        self.validator_page = ValidatorPage(self.show_simulator)
        self.simulator_page = SimulatorPage(self.show_validator)
        
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.validator_page)
        self.stacked_widget.addWidget(self.simulator_page)
        
        self.stacked_widget.setCurrentWidget(self.home_page)
        self.center_window()

    def center_window(self):
        """Calculates screen dimensions and centers the application window."""
        # Get the exact geometry of the application window
        qr = self.frameGeometry()
        # Get the exact center point of the monitor/screen
        cp = self.screen().availableGeometry().center()
        # Move the application's geometry center to the screen's center
        qr.moveCenter(cp)
        # Apply the newly calculated top-left coordinate to move the actual window
        self.move(qr.topLeft())

    def show_validator(self):
        self.stacked_widget.setCurrentWidget(self.validator_page)
        
    def show_simulator(self, email, password):
        self.simulator_page.load_data(email, password)
        self.stacked_widget.setCurrentWidget(self.simulator_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())