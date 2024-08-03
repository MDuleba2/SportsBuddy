import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QCheckBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Dark Mode Example")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.button = QPushButton("Click Me", self)
        self.button.clicked.connect(self.on_button_click)
        layout.addWidget(self.button)

        self.dark_mode_switch = QCheckBox("Dark Mode")
        self.dark_mode_switch.stateChanged.connect(self.toggle_dark_mode)
        layout.addWidget(self.dark_mode_switch)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_button_click(self):
        self.button.setText("Clicked!")

    def toggle_dark_mode(self):
        if self.dark_mode_switch.isChecked():
            with open("client\styles\dark_mode.css", "r") as file:
                stylesheet = file.read()
            app.setStyleSheet(stylesheet)
        else:
            app.setStyleSheet("")

def main():
    
    global app 
    app = QApplication(sys.argv)


    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()