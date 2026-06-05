import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from gui.home import HomePage
from gui.validator import ValidatorPage 
from gui.simulator import SimulatorPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Regex-Based Validator - TOA Project")
        # Made the window slightly wider to accommodate the simulator log and image
        self.setFixedSize(900, 650) 
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize Pages and pass the navigation callbacks
        self.home_page = HomePage(self.show_validator)
        self.validator_page = ValidatorPage(self.show_simulator)
        self.simulator_page = SimulatorPage(self.show_validator)
        
        # Add to stack
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.validator_page)
        self.stacked_widget.addWidget(self.simulator_page)
        
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_validator(self):
        """Switches to the Validator Page."""
        self.stacked_widget.setCurrentWidget(self.validator_page)
        
    def show_simulator(self, email, password):
        """Injects data and switches to the Simulator Page."""
        self.simulator_page.load_data(email, password)
        self.stacked_widget.setCurrentWidget(self.simulator_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())