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


class SpeedTestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    

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
        """Runs the network speed test and displays results."""
        self.label.setText("Testing... Please wait.")
        QApplication.processEvents()

        try:
            # Initialize the Speedtest object and get the best server
            st = speedtest.Speedtest()
            best_server = st.get_best_server()
            self.results_label.setText(f"Selected server: {best_server['host']} located in {best_server['name']}, {best_server['country']}.\n")
            QApplication.processEvents()

            # TEST DOWNLOAD SPEED
            self.label.setText("Testing download speed...")
            QApplication.processEvents()
            download_speed = st.download() / 1_000_000 # Convert to Mbps
            self.results_label.setText(f"Download speed: {download_speed:.2f} Mbps\n")
            QApplication.processEvents()

            # TEST UPLOAD SPEED
            self.label.setText("Testing upload speed...")
            QApplication.processEvents()
            upload_speed = st.upload() / 1_000_000 # Convert to Mbps
            self.results_label.setText(f"Download speed: {download_speed:.2f} Mbps\n"
                                       f"Upload speed: {upload_speed:.2f} Mbps\n")
            QApplication.processEvents()

            # TEST LATENCY (PING)
            self.label.setText("Testing latency...")
            QApplication.processEvents()
            ping = st.results.ping
            self.results_label.setText(f"Download speed: {download_speed:.2f} Mbps\n"
                                       f"Upload speed: {upload_speed:.2f} Mbps\n"
                                       f"Latency: {ping:.2f} ms\n")
            QApplication.processEvents()

            self.label.setText("Test completed successfully.")

        except Exception as e:
            self.results_label.setText(f"An error occurred during the test. {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeedTestApp()
    window.show()
    sys.exit(app.exec_())