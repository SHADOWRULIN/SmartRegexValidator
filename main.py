import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from gui.home import HomePage

# We will uncomment these in the next steps as we build them!
# from gui.validator import ValidatorPage 
# from gui.simulator import SimulatorPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Regex-Based Validator - TOA Project")
        self.setFixedSize(800, 600) # Desktop application size
        
        # QStackedWidget allows us to switch between pages smoothly
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize the Home Page
        # We pass self.show_validator so the Home page's button can trigger it
        self.home_page = HomePage(self.show_validator)
        
        # Add page to the stack
        self.stacked_widget.addWidget(self.home_page)
        
        # Set Home Page as the first visible screen
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_validator(self):
        # We will connect this to the real validator page in the next step.
        print("Start button clicked! Ready to switch to the Validator Page...")

if __name__ == "__main__":
    # Standard PyQt6 initialization
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())