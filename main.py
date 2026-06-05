import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from gui.home import HomePage
from gui.validator import ValidatorPage 

# We will uncomment this in the final step
# from gui.simulator import SimulatorPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Regex-Based Validator - TOA Project")
        self.setFixedSize(800, 600)
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize Pages
        self.home_page = HomePage(self.show_validator)
        self.validator_page = ValidatorPage(self.show_simulator)
        
        # Add to stack
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.validator_page)
        
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_validator(self):
        """Switches to the Validator Page."""
        self.stacked_widget.setCurrentWidget(self.validator_page)
        
    def show_simulator(self, email, password):
        """Will switch to the Simulator Page and pass the inputs."""
        print(f"Ready to simulate DFA for Email: {email} | Password: {password}")
        # We will build this connection in Step 9!

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())