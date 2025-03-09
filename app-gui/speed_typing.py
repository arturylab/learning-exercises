import sys
import time
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QFont

# Sample texts for the typing test
TEXT_SAMPLES = [
    "The quick brown fox jumps over the lazy dog.",
    "PyQt5 is a powerful tool for creating GUI applications.",
    "Speed typing tests can improve your writing skills.",
    "Machine learning and AI are transforming the world.",
    "Quantum computing is the future of complex problem-solving.",
    "Data science is an interdisciplinary field focused on extracting knowledge from data.",
    "Python is a versatile programming language used for various applications.",
    "Cybersecurity is essential in protecting digital information.",
    "Blockchain technology underpins cryptocurrencies like Bitcoin.",
    "Virtual reality provides immersive experiences in digital environments.",
]

class SpeedTypingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title and size
        self.setWindowTitle('Speed Typing Test')
        self.setGeometry(100, 100, 500, 300)

        # Set font size for labels and text input
        font = QFont()
        font.setPointSize(24)

        # Display a random text sample
        self.text_label = QLabel(random.choice(TEXT_SAMPLES), self)
        self.text_label.setFont(font)

        # Text input area for typing the displayed text
        self.text_input = QTextEdit(self)
        self.text_input.setFont(font)
        self.text_input.textChanged.connect(self.start_test)

        # Button to restart the test
        self.restart_button = QPushButton('Restart', self)
        self.restart_button.clicked.connect(self.restart_test)
        self.restart_button.setDisabled(True)

        # Label to display the result (WPM and accuracy)
        self.result_label = QLabel('', self)

        # Layout to arrange widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.text_label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.restart_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def start_test(self):
        # Start the timer when the user starts typing
        if not hasattr(self, 'start_time'):
            self.start_time = time.time()
        self.text_input.textChanged.connect(self.check_typing)
        self.restart_button.setDisabled(False)
    
    def check_typing(self):
        # Check the typed text against the target text
        typed_text = self.text_input.toPlainText()
        target_text = self.text_label.text()

        # If the typed text matches the target text
        if typed_text.strip() == target_text.strip():
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            words = len(typed_text.split())
            wpm = (words / elapsed_time) * 60

            # Calculate accuracy
            correct_chars = sum(1 for a, b in zip(typed_text, target_text) if a == b)
            accuracy = (correct_chars / len(target_text)) * 100

            # Display the result
            self.result_label.setText(f'WPM: {wpm:.2f}\nAccuracy: {accuracy:.2f}%')
            self.text_input.setDisabled(True)

    def restart_test(self):
        # Restart the test with a new random text sample
        self.text_label.setText(random.choice(TEXT_SAMPLES))
        self.text_input.clear()
        self.text_input.setDisabled(False)
        self.text_input.setFocus()
        self.result_label.setText('')
        self.restart_button.setDisabled(True)
        if hasattr(self, 'start_time'):
            del self.start_time

if __name__ == '__main__':
    # Create the application and main window
    app = QApplication(sys.argv)
    window = SpeedTypingApp()
    window.show()
    # Run the application event loop
    sys.exit(app.exec_())