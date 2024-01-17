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

# Code inspired from a simple Bluetooth LowEnergy Scanner by StefanD986 at https://gist.github.com/StefanD986/1b00e6c078516a60e5e3e691903b9051
# Code for the official Bluetooth LowEnergy Scanner by Qt at https://doc.qt.io/qtforpython-6/overviews/qtbluetooth-lowenergyscanner-example.html#bluetooth-low-energy-scanner
# Code for Bluetooth LowEnergy Scanner ported to pyqt5 by SietseAchterop at https://github.com/SietseAchterop/BLE_pyqt5 
# Code for the official Bluetooth chat app by Qt at https://doc.qt.io/qtforpython-6/overviews/qtbluetooth-btchat-example.html#bluetooth-chat

# QtBluetooth classes for pyqt5 by RiverBank Computing at https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtbluetooth/qtbluetooth-module.html
# QtBluetooth classes for pyside6 (similar to pyqt5 and looking more complete) by Qt at https://doc.qt.io/qtforpython-6/PySide6/QtBluetooth/index.html#module-PySide6.QtBluetooth
# QtBluetooth classes for qt5 (old snapshot) by Developpez.com at https://qt.developpez.com/doc/5.0-snapshot/modules/

# Asking for user permissions in pyqt5 might need to be through the specific platform.
# For instance for Android permissions, you can use [QtAndroid module](https://doc.qt.io/qt-5/qtandroid.html#requestPermissions).

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QLabel, QGridLayout, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtBluetooth import QBluetoothDeviceDiscoveryAgent, QBluetoothDeviceInfo, QBluetoothLocalDevice

## Main variables and objects

## Class definition

class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        # Set main window title
        self.setWindowTitle("Basic bluetooth information exchanger")
        
        # Create components of the main window
        self.create_bluetooth_discovery_screen()
        self.create_statusbar()
        
        # Display the main window
        self.showMaximized()

    def create_bluetooth_discovery_screen(self):
            
        # Define a central widget with a specific layout
        # Tip: QLayout cannot be set on the MainWindow directly
        self.bluetooth_discovery_window = QWidget()
        self.setCentralWidget(self.bluetooth_discovery_window)
        self.bluetooth_discovery_window_layout = QGridLayout()
        self.bluetooth_discovery_window.setLayout(self.bluetooth_discovery_window_layout)
        
        # Define control buttons
        self.bluetooth_discovery_button = QPushButton("Search for Bluetooth devices")
        self.bluetooth_discovery_button.clicked.connect(self.on_bluetooth_discovery_button_clicked)
        self.exit_button = QPushButton("Exit app")
        self.exit_button.clicked.connect(self.close)
        
        # Define text display box
        self.bluetooth_search_status_label = QLabel()
        info_text_init = "Bluetooth search status: NOT ACTIVE"
        self.bluetooth_search_status_label.setText(info_text_init)

        # Update the widgets in the selected layout
        self.bluetooth_discovery_window_layout.addWidget(self.bluetooth_discovery_button, 1, 1, 1, 1)
        self.bluetooth_discovery_window_layout.addWidget(self.bluetooth_search_status_label, 3, 1, 1, 1)
        self.bluetooth_discovery_window_layout.addWidget(self.exit_button, 5, 1, 1, 1)
        self.bluetooth_discovery_window_layout.setRowStretch(0, 1)
        self.bluetooth_discovery_window_layout.setRowStretch(1, 0)
        self.bluetooth_discovery_window_layout.setRowStretch(2, 1)
        self.bluetooth_discovery_window_layout.setRowStretch(3, 0)
        self.bluetooth_discovery_window_layout.setRowStretch(4, 1)
        self.bluetooth_discovery_window_layout.setRowStretch(5, 0)
        self.bluetooth_discovery_window_layout.setRowStretch(6, 1)
        self.bluetooth_discovery_window_layout.setColumnStretch(0, 1)
        self.bluetooth_discovery_window_layout.setColumnStretch(2, 1)

    def create_statusbar(self):
        
        # Instantiate a status bar
        self.status_bar = QStatusBar()
        
        # Define the status bar as part of the main window
        self.setStatusBar(self.status_bar)

        # object_centre_track_label.setVisible(True)
        
        # Set text for the status bar
        self.bluetooth_status_label = QLabel()
        status_bar_text_init = "Bluetooth status: UNKNOWN"
        self.bluetooth_status_label.setText(status_bar_text_init)
        self.status_bar.addWidget(self.bluetooth_status_label)

    def on_bluetooth_discovery_button_clicked(self):
        
        print("Start Bluetooth discovery steps")

        # Disable clicked button to prevent spamming
        self.bluetooth_discovery_button.setEnabled(False)
        
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
            alert.close()

        else:
            # Create a Bluetooth Scanner object
            print("Create Bluetooth Scanner object")
            self.bluetooth_scanner = BluetoothScanner()
            self.bluetooth_scanner.update_scan_completed.connect(self.on_bluetooth_scan_completed)
            self.bluetooth_scanner.update_scan_failed.connect(self.on_bluetooth_scan_failed)

            # Confirm bluetooth is supported on device
            self.local_bluetooth_info = self.bluetooth_scanner.share_host_bluetooth_info()
            is_local_bluetooth_supported = self.local_bluetooth_info.get('validity')
            is_local_bluetooth_active = self.local_bluetooth_info.get('mode')
            status_bar_text = ""
            if is_local_bluetooth_supported:
                if is_local_bluetooth_active:
                    status_bar_text = "Bluetooth status: SUPPORTED - ACTIVE"
                else:
                    status_bar_text = "Bluetooth status: SUPPORTED - NOT ACTIVE"
            else:
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
                    alert.close()
            
            else:
                # Instantiate the alert message for bluetooth discovery
                alert = QMessageBox()
                alert.setText('Start searching for bluetooth devices nearby?')

                # Set standard buttons for the alert window
                alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                alert.setDefaultButton(QMessageBox.Ok)
                
                # Handle alert window button press
                alert_value = alert.exec()
                if alert_value == QMessageBox.Ok:
                    alert.close()
                   
                    local_bluetooth_discovery_timeout = self.local_bluetooth_info.get('discovery_timeout')
                    info_text = "Bluetooth search status: IN PROGRESS"
                    info_text += "\nSearch duration = " + str(local_bluetooth_discovery_timeout) + " second(s)"
                    self.bluetooth_search_status_label.setText(info_text)

                    print("Start discovery")
                    self.bluetooth_scanner.start_scan()
                
                else:
                    self.bluetooth_discovery_button.setEnabled(True)
                    alert.close()

    def on_bluetooth_scan_completed(self):
        self.local_bluetooth_info = self.bluetooth_scanner.share_host_bluetooth_info()
        info_text = "Bluetooth search status: DONE\n"
        for device_found_info in self.local_bluetooth_info.get('scan_result'):
            info_text += "\n" + device_found_info
        self.bluetooth_search_status_label.setText(info_text)
        status_bar_text = "Bluetooth status: SUPPORTED - ACTIVE"
        self.bluetooth_status_label.setText(status_bar_text)
        self.bluetooth_discovery_button.setEnabled(True)

    def on_bluetooth_scan_failed(self):
        info_text = "Bluetooth search status: ERROR"
        self.bluetooth_search_status_label.setText(info_text)
        status_bar_text = "Bluetooth status: SUPPORTED - ACTIVE"
        self.bluetooth_status_label.setText(status_bar_text)
        self.bluetooth_discovery_button.setEnabled(True)

class BluetoothScanner(QObject):
   
    # Tip for Signals: use pyqtSignal(str) to pass a string
    update_scan_failed = pyqtSignal()
    update_scan_completed = pyqtSignal()

    def __init__(self):
    
        super().__init__()

        # Instantiate local bluetooth device object and relevant variables
        self.local_bluetooth_device = QBluetoothLocalDevice()
        self.local_bluetooth_validity = None
        self.local_bluetooth_mode = None
        self.local_bluetooth_devices = None
        self.local_bluetooth_address = None
        self.local_bluetooth_name = None
        # self.local_bluetooth_device.powerOn()
        self.retrieve_local_device_info()

        # Create elements for bluetooth communications
        self.device_search_list = []
        self.device_found_list = []
        self.bluetooth_discovery_timeout = 5  # seconds
        print("Create Device Discovery Agent")
        self.device_discovery_agent = QBluetoothDeviceDiscoveryAgent(self)
        self.device_discovery_agent.setLowEnergyDiscoveryTimeout(self.bluetooth_discovery_timeout * 1000)  # timer in ms
        self.device_discovery_agent.deviceDiscovered.connect(self.add_device)
        self.device_discovery_agent.error.connect(self.scan_error)
        self.device_discovery_agent.finished.connect(self.scan_finished)
        self.device_discovery_agent.canceled.connect(self.scan_finished)

    def start_scan(self):
        print("Start scan")
        try:
            self.device_discovery_agent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod(2))
        except Exception as e:
            print("Exception raised: " + e.message)
            pass

    def add_device(self, device):
        print("Add device")
        print("New device to add: " + str(device))
        if device.coreConfigurations() and QBluetoothDeviceInfo.LowEnergyCoreConfiguration:
            self.device_search_list.append(QBluetoothDeviceInfo(device))

    def scan_finished(self):
        print("scan finished")
        self.device_found_list = []
        for device_info in self.device_search_list:
            device_descr = 'Name: {name}, UUID: {UUID}, rssi: {rssi}'.format(UUID=device_info.deviceUuid().toString(),
                                                                             name=device_info.name(),
                                                                             rssi=device_info.rssi(),
            )
            self.device_found_list.append(device_descr)

        self.update_scan_completed.emit()

    def scan_error(self):
        print("scan error")
        self.update_scan_failed.emit()

    def retrieve_local_device_info(self):
        print("Retrieve local device info")
        self.local_bluetooth_validity = self.local_bluetooth_device.isValid()
        self.local_bluetooth_mode = self.local_bluetooth_device.hostMode()
        self.local_bluetooth_devices = self.local_bluetooth_device.allDevices()
        self.local_bluetooth_address = self.local_bluetooth_device.address()
        self.local_bluetooth_name = self.local_bluetooth_device.name()

        print("List of debug variables for the local device:")
        print("Validity = " + str(self.local_bluetooth_validity))
        print("Mode = " + str(self.local_bluetooth_mode))
        print("Devices = " + str(self.local_bluetooth_devices))
        print("Address = " + str(self.local_bluetooth_address))
        print("Name = " + str(self.local_bluetooth_name))

    def share_host_bluetooth_info(self):
        self.retrieve_local_device_info()
        host_bluetooth_info_dict = {}
        host_bluetooth_info_dict['validity'] = self.local_bluetooth_validity
        host_bluetooth_info_dict['mode'] = self.local_bluetooth_mode
        host_bluetooth_info_dict['devices'] = self.local_bluetooth_devices
        host_bluetooth_info_dict['address'] = self.local_bluetooth_address
        host_bluetooth_info_dict['name'] = self.local_bluetooth_name
        host_bluetooth_info_dict['discovery_timeout'] = self.bluetooth_discovery_timeout
        host_bluetooth_info_dict['scan_result'] = self.device_found_list
        return host_bluetooth_info_dict

## Application definition

if __name__ == '__main__':

    # Define the app object/instance
    app = QApplication(sys.argv)
    
    # Create a Qt widget, which is going to be the main window.
    main_window = MainWindow()
    
    # Start the event loop and handle the exit code
    sys.exit(app.exec())
