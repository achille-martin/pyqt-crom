#!/usr/bin/env python3

# MIT License

# Copyright (c) 2023-2024 Achille MARTIN

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Code inspired from :
# * Simple Bluetooth LowEnergy Scanner by StefanD987 at https://gist.github.com/StefanD986/1b00e6c078516a60e5e3e691903b9051
# * Official Bluetooth LowEnergy Scanner by Qt at https://doc.qt.io/qtforpython-6/overviews/qtbluetooth-lowenergyscanner-example.html#bluetooth-low-energy-scanner

# Tip for PyQt Signals: use pyqtSignal(<type>) to pass a <type>
# For instance: pyqtSignal(str) to pass a string

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QLabel, QGridLayout, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QBluetoothLocalDevice

import sys
import os.path # To manage file paths for cross-platform apps
import logging as log_tool # The logging library for debugging

## Main variables and objects

# Define path reference: app folder is the reference for the device
app_folder = os.path.expanduser('~')
if not os.path.exists(app_folder):
    # Ensure that a path can be defined to generate the necessary files on device
    app_folder = os.getcwd()

# Set logger config and instantiate object
logger_logging_level = "DEBUG"
logger_output_file_name = "pyqt5-app.log"
logger_output_prefix_format = "[%(asctime)s] [%(levelname)s] - %(message)s"

logger = log_tool.getLogger(__name__)
logger.setLevel(logger_logging_level)
logger_output_file_path = os.path.join(app_folder, str(logger_output_file_name))
file_handler = log_tool.FileHandler(logger_output_file_path)
formatter = log_tool.Formatter(logger_output_prefix_format)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

## Class definition

# Subclass QMainWindow to customize the application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        logger.debug("MainWindow::__init__ - Entered method")
        
        # Set main window title
        self.setWindowTitle("Basic Bluetooth scanner")
        
        # Create components of the main window
        self.create_bluetooth_discovery_screen()
        self.create_statusbar()
        
        # Display the main window (maximised)
        self.showMaximized()

        # Set word wrap and max width for the display box to prevent text escape out of screen
        # The operation comes after the main window is resized
        self.bluetooth_search_status_label.setWordWrap(True)
        self.bluetooth_search_status_label.setMaximumWidth(self.bluetooth_discovery_button.width())

        logger.debug("MainWindow::__init__ - Exited method")

    def create_bluetooth_discovery_screen(self):
            
        logger.debug("MainWindow::create_bluetooth_discovery_screen - Entered method")
        
        # Define a central widget with a specific layout
        # Tip: QLayout cannot be set on the MainWindow directly
        self.bluetooth_discovery_screen = QWidget()
        self.setCentralWidget(self.bluetooth_discovery_screen)
        self.bluetooth_discovery_screen_layout = QGridLayout()
        self.bluetooth_discovery_screen.setLayout(self.bluetooth_discovery_screen_layout)
        
        # Define control buttons
        self.bluetooth_discovery_button = QPushButton(">>> Search for Bluetooth devices <<<")
        self.bluetooth_discovery_button.clicked.connect(self.on_bluetooth_discovery_button_clicked)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        
        # Define search status display box
        self.bluetooth_search_status_label = QLabel()
        text_init = "Bluetooth search status: NOT ACTIVE"
        self.bluetooth_search_status_label.setText(text_init)

        # Update the widgets in the selected layout
        self.bluetooth_discovery_screen_layout.addWidget(self.bluetooth_discovery_button, 1, 1, 1, 1)
        self.bluetooth_discovery_screen_layout.addWidget(self.bluetooth_search_status_label, 3, 1, 1, 1)
        self.bluetooth_discovery_screen_layout.addWidget(self.exit_button, 5, 1, 1, 1)
        self.bluetooth_discovery_screen_layout.setRowStretch(0, 1)
        self.bluetooth_discovery_screen_layout.setRowStretch(1, 0)
        self.bluetooth_discovery_screen_layout.setRowStretch(2, 1)
        self.bluetooth_discovery_screen_layout.setRowStretch(3, 0)
        self.bluetooth_discovery_screen_layout.setRowStretch(4, 1)
        self.bluetooth_discovery_screen_layout.setRowStretch(5, 0)
        self.bluetooth_discovery_screen_layout.setRowStretch(6, 1)
        self.bluetooth_discovery_screen_layout.setColumnStretch(0, 1)
        self.bluetooth_discovery_screen_layout.setColumnStretch(2, 1)

        logger.debug("MainWindow::create_bluetooth_discovery_screen - Exited method")

    def create_statusbar(self):

        logger.debug("MainWindow::create_statusbar - Entered method")
        
        # Instantiate a status bar
        self.status_bar = QStatusBar()
        
        # Define the status bar as part of the main window
        self.setStatusBar(self.status_bar)

        # Set text for the status bar
        self.bluetooth_status_label = QLabel()
        text_init = "Bluetooth status: UNKNOWN"
        self.bluetooth_status_label.setText(text_init)
        self.status_bar.addWidget(self.bluetooth_status_label)

        logger.debug("MainWindow::create_statusbar - Exited method")

    def on_bluetooth_discovery_button_clicked(self):
        
        logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Entered method")
        logger.info("MainWindow::on_bluetooth_discovery_button_clicked - Button has been clicked")

        # Disable clicked button to prevent spamming
        self.bluetooth_discovery_button.setEnabled(False)
        logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Disabled button")
        
        # Instantiate the alert message for bluetooth capability
        alert = QMessageBox()
        alert.setText("""
        Does your device support Bluetooth?
        
        Note: If your device does not support Bluetooth,
        The app will be unusable.
        """
        )

        # Set standard buttons for the alert window
        alert.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        alert.setDefaultButton(QMessageBox.No)
        
        # Handle alert window button press
        alert_value = alert.exec()
        if alert_value == QMessageBox.No:
            status_bar_text = "Bluetooth status: NOT SUPPORTED - APP UNUSABLE"
            self.bluetooth_status_label.setText(status_bar_text)
            self.bluetooth_discovery_button.setEnabled(True)
            logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Bluetooth not supported feedback - Enabled button")
            alert.close()
            logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Exited method")

        else:
            # Create a Bluetooth Scanner object
            # TODO: fix inefficiency of creating a new object at every button click
            self.bluetooth_scanner = BluetoothScanner()
            # Setup signals / callbacks to the Bluetooth Scanner object
            self.bluetooth_scanner.update_scan_completed.connect(self.on_bluetooth_scan_completed)
            self.bluetooth_scanner.update_scan_failed.connect(self.on_bluetooth_scan_failed)
            logger.info("MainWindow::on_bluetooth_discovery_button_clicked - Created Bluetooth Scanner object")

            # Confirm Bluetooth is supported on (local) device
            self.local_bluetooth_info = self.bluetooth_scanner.share_host_bluetooth_info()
            is_local_bluetooth_supported = self.local_bluetooth_info.get('validity')
            is_local_bluetooth_active = self.local_bluetooth_info.get('mode')
            status_bar_text = ""
            if is_local_bluetooth_supported:
                logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Bluetooth supported on device")
                if is_local_bluetooth_active:
                    logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Bluetooth active on device")
                    status_bar_text = "Bluetooth status: SUPPORTED - ACTIVE"
                else:
                    logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Bluetooth not active on device")
                    status_bar_text = "Bluetooth status: SUPPORTED - NOT ACTIVE"
            else:
                logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Bluetooth not supported on device")
                status_bar_text = "Bluetooth status: NOT SUPPORTED"
                self.close()

            # Update bluetooth status label
            self.bluetooth_status_label.setText(status_bar_text)

            # Request the user to turn ON Bluetooth to bypass restrictions if needed
            if not is_local_bluetooth_active:
                alert = QMessageBox()
                alert.setText("""
                Please turn Bluetooth ON on your device
                Otherwise the app may not work as expected.
                """
                )

                # Set standard buttons for the alert window
                alert.setStandardButtons(QMessageBox.Ok)
                alert.setDefaultButton(QMessageBox.Ok)

                # Handle alert window button press
                alert_value = alert.exec()
                if alert_value == QMessageBox.Ok:
                    self.bluetooth_discovery_button.setEnabled(True)
                    logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Requested user to activate Bluetooth on device - Enabled button")
                    alert.close()
                    logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Exited method")
            
            else:
                # Instantiate the alert message for bluetooth discovery
                alert = QMessageBox()
                alert.setText('Start searching for Bluetooth devices nearby?')

                # Set standard buttons for the alert window
                alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                alert.setDefaultButton(QMessageBox.Ok)
                
                # Handle alert window button press
                alert_value = alert.exec()
                if alert_value == QMessageBox.Ok:
                    alert.close()
                    
                    # Update search status (in progress)
                    local_bluetooth_discovery_timeout = self.local_bluetooth_info.get('discovery_timeout')
                    search_status_text = "Bluetooth search status: IN PROGRESS"
                    search_status_text += "\nSearch duration = " + str(local_bluetooth_discovery_timeout) + " second(s)"
                    self.bluetooth_search_status_label.setText(search_status_text)

                    # Start Bluetooth discovery scan
                    logger.info("MainWindow::on_bluetooth_discovery_button_clicked - Starting Bluetooth discovery scan")
                    self.bluetooth_scanner.start_scan()
                    logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Exited method")
                
                else:
                    self.bluetooth_discovery_button.setEnabled(True)
                    logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Received cancellation of Bluetooth discovery - Enabled button")
                    alert.close()
                    logger.debug("MainWindow::on_bluetooth_discovery_button_clicked - Exited method")

    def on_bluetooth_scan_completed(self):
        
        logger.debug("MainWindow::on_bluetooth_scan_completed - Entered method")
        logger.info("MainWindow::on_bluetooth_scan_completed - Scan has completed")
        
        # Collect host Bluetooth info
        self.local_bluetooth_info = self.bluetooth_scanner.share_host_bluetooth_info()

        # Update Bluetooth search status
        search_status_text = "Bluetooth search status: DONE\n"
        for device_found_info in self.local_bluetooth_info.get('scanned_devices'):
            search_status_text += "\n\n" + device_found_info
        self.bluetooth_search_status_label.setText(search_status_text)

        # Update Bluetooth status
        status_bar_text = "Bluetooth status: SUPPORTED - ACTIVE"
        self.bluetooth_status_label.setText(status_bar_text)

        self.bluetooth_discovery_button.setEnabled(True)
        logger.debug("MainWindow::on_bluetooth_scan_completed - Scan finished - Enabled button")

        logger.debug("MainWindow::on_bluetooth_scan_completed - Exited method")

    def on_bluetooth_scan_failed(self):
        
        logger.debug("MainWindow::on_bluetooth_scan_failed - Entered method")
        logger.info("MainWindow::on_bluetooth_scan_failed - Scan has failed")
        
        # Update Bluetooth search status
        search_status_text = "Bluetooth search status: ERROR"
        self.bluetooth_search_status_label.setText(search_status_text)

        # Update Bluetooth search status
        status_bar_text = "Bluetooth status: SUPPORTED - ACTIVE"
        self.bluetooth_status_label.setText(status_bar_text)

        self.bluetooth_discovery_button.setEnabled(True)
        logger.debug("MainWindow::on_bluetooth_scan_failed - Scan failed - Enabled button")

        logger.debug("MainWindow::on_bluetooth_scan_failed - Exited method")

class BluetoothScanner(QObject):
   
    update_scan_failed = pyqtSignal()
    update_scan_completed = pyqtSignal()

    def __init__(self):
        super().__init__()

        logger.debug("BluetoothScanner::__init__ - Entered method")

        # Instantiate local bluetooth device object and useful variables
        self.local_bluetooth_device = QBluetoothLocalDevice()
        self.local_bluetooth_validity = None
        self.local_bluetooth_mode = None
        self.local_bluetooth_devices = None
        self.local_bluetooth_address = None
        self.local_bluetooth_name = None
        # self.local_bluetooth_device.powerOn()  # Too many restrictions on some OS
        logger.info("BluetoothScanner::__init__ - Created Bluetooth Local Device object")
       
        # Retrieve local Bluetooth device info
        self.retrieve_local_device_info()

        # Create useful variables for Bluetooth discovery
        self.device_search_list = []
        self.device_found_list = []
        self.bluetooth_discovery_timeout = 5  # seconds

        # Create device discovery agent
        self.device_discovery_agent = QBluetoothDeviceDiscoveryAgent(self)
        self.device_discovery_agent.setLowEnergyDiscoveryTimeout(self.bluetooth_discovery_timeout * 1000)  # timer in ms
        # Setup callbacks for the discovery agent
        self.device_discovery_agent.deviceDiscovered.connect(self.add_device)
        self.device_discovery_agent.error.connect(self.scan_error)
        self.device_discovery_agent.finished.connect(self.scan_finished)
        self.device_discovery_agent.canceled.connect(self.scan_finished)
        logger.info("BluetoothScanner::__init__ - Created Bluetooth Device Discovery object")
        
        logger.debug("BluetoothScanner::__init__ - Exited method")

    def start_scan(self):
        
        logger.debug("BluetoothScanner::start_scan - Entered method")
        logger.info("BluetoothScanner::start_scan - Starting Bluetooth scan")
        
        try:
            self.device_discovery_agent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod(2))
        except Exception as e:
            logger.debug("BluetoothScanner::start_scan - Caught exception:\n" 
                    + str(e.message)
            )
            pass
        
        logger.debug("BluetoothScanner::start_scan - Exited method")

    def add_device(self, device):
        
        logger.debug("BluetoothScanner::add_device - Entered method")
        logger.debug("BluetoothScanner::add_device - Received request to add new device:\n"
                + str(device)
        )

        if device.coreConfigurations() and QBluetoothDeviceInfo.LowEnergyCoreConfiguration:
            self.device_search_list.append(QBluetoothDeviceInfo(device))
            logger.debug("BluetoothScanner::add_device - Added device to search results since Low Energy")
        
        logger.debug("BluetoothScanner::add_device - Exited method")

    def scan_finished(self):
        
        logger.debug("BluetoothScanner::scan_finished - Entered method")
        logger.info("BluetoothScanner::scan_finished - Finishing Bluetooth scan")
        
        self.device_found_list = []
        for device_info in self.device_search_list:
            device_descr = 'Name: {name}, UUID: {UUID}, rssi: {rssi}'.format(UUID=device_info.deviceUuid().toString(),
                                                                             name=device_info.name(),
                                                                             rssi=device_info.rssi(),
            )
            self.device_found_list.append(device_descr)
        logger.debug("BluetoothScanner::scan_finished - Devices found:\n"
                + str(self.device_found_list)
        )

        logger.debug("BluetoothScanner::scan_finished - Sending signal scan completed")
        self.update_scan_completed.emit()
        
        logger.debug("BluetoothScanner::scan_finished - Exited method")

    def scan_error(self):
        
        logger.debug("BluetoothScanner::scan_error - Entered method")
        logger.info("BluetoothScanner::scan_error - Analysing scan error")
        
        logger.debug("BluetoothScanner::scan_error - Sendinf signal scan completed")
        self.update_scan_failed.emit()
        
        logger.debug("BluetoothScanner::scan_error - Exited method")

    def retrieve_local_device_info(self):
        
        logger.debug("BluetoothScanner::retrieve_local_device_info - Entered method")
        logger.info("BluetoothScanner::retrieve_local_device_info - Retrieving local Bluetooth device info")
        
        self.local_bluetooth_validity = self.local_bluetooth_device.isValid()
        self.local_bluetooth_mode = self.local_bluetooth_device.hostMode()
        self.local_bluetooth_devices = self.local_bluetooth_device.allDevices()
        self.local_bluetooth_address = self.local_bluetooth_device.address()
        self.local_bluetooth_name = self.local_bluetooth_device.name()

        logger.debug("BluetoothScanner::retrieve_local_device_info - Collected local Bluetooth device info:"
                + "\nValidity = " + str(self.local_bluetooth_validity)
                + "\nMode = " + str(self.local_bluetooth_mode)
                + "\nDevices (Local extra) = " + str(self.local_bluetooth_devices)
                + "\nName = " + str(self.local_bluetooth_name)
                + "\nAddress = " + str(self.local_bluetooth_address)
        )
        
        logger.debug("BluetoothScanner::retrieve_local_device_info - Exited method")

    def share_host_bluetooth_info(self):
        
        logger.debug("BluetoothScanner::share_host_bluetooth_info - Entered method")
        
        # Update local device info
        self.retrieve_local_device_info()

        # Create Bluetooth host info dictionary for clear communication
        host_bluetooth_info_dict = {}
        host_bluetooth_info_dict['validity'] = self.local_bluetooth_validity
        host_bluetooth_info_dict['mode'] = self.local_bluetooth_mode
        host_bluetooth_info_dict['devices'] = self.local_bluetooth_devices
        host_bluetooth_info_dict['address'] = self.local_bluetooth_address
        host_bluetooth_info_dict['name'] = self.local_bluetooth_name
        host_bluetooth_info_dict['discovery_timeout'] = self.bluetooth_discovery_timeout
        host_bluetooth_info_dict['scanned_devices'] = self.device_found_list
        logger.debug("BluetoothScanner::share_host_bluetooth_info - Created Bluetooth host info dictionary")
        
        logger.debug("BluetoothScanner::share_host_bluetooth_info - Exited method")
        return host_bluetooth_info_dict

## Application definition

def main():
    logger.info("========================\n")
    logger.info("========================")
    logger.debug("main - Entered function and logger instantiated")
    logger.debug("main - Log output file can be found at:\n" + str(logger_output_file_path))

    # Define the app object/instance
    app = QApplication(sys.argv)
    
    # Create a Qt widget, which is going to be the main window.
    main_window = MainWindow()
    
    # Start the event loop and handle the exit code
    logger.info("main - App started")
    sys.exit(app.exec())
    logger.info("main - App terminated")
    
    # The application will reach here only after an exit or the event loop has stopped.
    logger.debug("main - Exited function")

if __name__ == '__main__':
    main()
