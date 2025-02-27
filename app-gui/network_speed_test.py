"""
Python-based network speed test tool using PyQt5 for a modern, interactive interface.
Measures download and upload speeds using the speedtest module.
Tests network latency (ping) to the nearest server.
Provides a clean UI with results displayed clearly.
Offers a 'Start Test' button for user control.
"""

import sys
import speedtest
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal


class SpeedTestThread(QThread):
    """Thread for running speed tests without blocking the UI"""
    update_status = pyqtSignal(str)
    update_result = pyqtSignal(str)
    test_finished = pyqtSignal(bool, str)  # Success flag and error message if any

    def run(self):
        try:
            # Initialize the Speedtest object and get the best server
            self.update_status.emit("Finding best server...")
            st = speedtest.Speedtest()
            best_server = st.get_best_server()
            self.update_result.emit(f"Selected server: {best_server['host']} located in {best_server['name']}, {best_server['country']}.\n")

            # TEST DOWNLOAD SPEED
            self.update_status.emit("Testing download speed...")
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            self.update_result.emit(f"Selected server: {best_server['host']} located in {best_server['name']}, {best_server['country']}.\n"
                                   f"Download speed: {download_speed:.2f} Mbps\n")

            # TEST UPLOAD SPEED
            self.update_status.emit("Testing upload speed...")
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            self.update_result.emit(f"Selected server: {best_server['host']} located in {best_server['name']}, {best_server['country']}.\n"
                                   f"Download speed: {download_speed:.2f} Mbps\n"
                                   f"Upload speed: {upload_speed:.2f} Mbps\n")

            # TEST LATENCY (PING)
            self.update_status.emit("Testing latency...")
            ping = st.results.ping
            self.update_result.emit(f"Selected server: {best_server['host']} located in {best_server['name']}, {best_server['country']}.\n"
                                   f"Download speed: {download_speed:.2f} Mbps\n"
                                   f"Upload speed: {upload_speed:.2f} Mbps\n"
                                   f"Latency: {ping:.2f} ms\n")

            self.test_finished.emit(True, "")
        except Exception as e:
            self.test_finished.emit(False, str(e))


class SpeedTestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.test_thread = None
    
    def init_ui(self):
        """Initializes the UI layout and widgets."""
        self.setWindowTitle("Network Speed Test")
        self.setGeometry(100, 100, 400, 300)

        # Apply custom font and palette
        app_font = QFont("Helvetica Neue", 12)
        self.setFont(app_font)

        layout = QVBoxLayout()

        # Label to instruct the user
        self.label = QLabel("Click 'Start Test' to measure your network speed.")
        self.label.setStyleSheet("color: #333333; font-size: 14px; font-weight: bold;")
        layout.addWidget(self.label)

        # Start button to initiate the speed test
        self.start_button = QPushButton("Start Test", self)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.start_button.clicked.connect(self.run_speed_test)
        layout.addWidget(self.start_button)

        # Label to display the results
        self.results_label = QLabel("")
        self.results_label.setStyleSheet("color: #333333; font-size: 14px;")
        layout.addWidget(self.results_label)

        # Apply layout to the main window
        self.setLayout(layout)

        # Apply overall window styling
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                text-align: center;
            }
        """)

    def run_speed_test(self):
        """Initiates the network speed test in a separate thread."""
        # Disable the button during test
        self.start_button.setEnabled(False)
        self.start_button.setText("Testing...")
        self.results_label.setText("")
        
        # Create and start the test thread
        self.test_thread = SpeedTestThread()
        self.test_thread.update_status.connect(self.update_status)
        self.test_thread.update_result.connect(self.update_result)
        self.test_thread.test_finished.connect(self.on_test_finished)
        self.test_thread.start()

    def update_status(self, message):
        """Updates the status label with the current operation."""
        self.label.setText(message)

    def update_result(self, result):
        """Updates the results label with test results."""
        self.results_label.setText(result)

    def on_test_finished(self, success, error_message):
        """Handles the completion of the speed test."""
        self.start_button.setEnabled(True)
        self.start_button.setText("Start Test")
        
        if success:
            self.label.setText("Test completed successfully.")
        else:
            self.label.setText("Test failed.")
            self.results_label.setText(f"An error occurred during the test: {error_message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeedTestApp()
    window.show()
    sys.exit(app.exec_())
