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

# Aim of the app: Beat the pause game by capturing the quickly switched image in a video automatically

# Refresher: the pause game consists in hiding a picture in one frame of a video and
# let the user try to see it by pausing the video
# Note that the pause takes a few seconds to actually trigger
# making the game pretty hard sometimes

# Concept:
# 1) Record screenshots in the background while playing the video
# 2) Identify image / frame changes and save at each sharp change
# 3) Reveal the images hidden to the user (hopefully including the hidden one)

# Warnings:
# This app only works on Linux as there are limitations on Android:
# - The screenshot functionality has been fixed for Qt version >= Qt5.15.4
# - The screenshot funcionality only works for the running app, not for the whole screen
# - The RAM on a phone is not fast enough to take multiple screenshots per second
# - Screenshots saved can only be seen by the app and not by the user in the media folders 
# if permissions are not granted or if scoped storage is in place (Android API >= 11)

import sys
from threading import Timer
import math
import time
import os
import logging as log_tool # The logging library for debugging
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QMessageBox, QStatusBar, QLabel, QFileDialog, QInputDialog
from PyQt5.QtCore import QStandardPaths, QUrl
from PyQt5.QtGui import QScreen

## Main variables and objects

# Define path reference: app folder is the reference for the device
app_folder = os.path.expanduser('~')
if not os.path.exists(app_folder):
    # Ensure that a path can be defined to generate the necessary files on device
    app_folder = os.getcwd()

# Set logger config and instantiate object
logger_logging_level = "DEBUG"
logger_output_file_name = "pyqt5-app-beat-the-pause-game.log"
logger_output_prefix_format = "[%(asctime)s] [%(levelname)s] - %(message)s"

logger = log_tool.getLogger(__name__)
logger.setLevel(logger_logging_level)
logger_output_file_path = os.path.join(app_folder, str(logger_output_file_name))
file_handler = log_tool.FileHandler(logger_output_file_path)
formatter = log_tool.Formatter(logger_output_prefix_format)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

## Class definition

class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        logger.debug("MainWindow::__init__ <(")
        
        # Set main window title
        self.setWindowTitle("Basic geometry shape visualiser")
        
        # Create components of the main window
        self.create_screen_grabber_visualiser()
        self.create_status_bar()

        # Configure initial settings for the app
        self.grab_screen_timeout = 5  # s
        self.grab_screen_frequency = 0.25  # s
        self.grab_screen_start_delay = 0  # s
        self.image_saved_name = "screenshot_saved_1"
        self.image_similarity_percentage = 80  # % - How similar are the images
        self.img_saved_dir = os.getcwd()
        
        logger.debug(f"""MainWindow::__init__ - Initial settings for the app:
                Grab screen timeout = {self.grab_screen_timeout}
                Grab screen frequency = {self.grab_screen_frequency}
                Grab screen start delay = {self.grab_screen_start_delay}
                First screenshot saved name = {self.image_saved_name}
                Image similarity percentage between screenshots = {self.image_similarity_percentage}
                Screenshot save location = {self.img_saved_dir}
                """
        )
        
        # Create useful variables
        self.image_list = []
        self.rmse_threshold = None

        # Display the main window
        self.showMaximized()
        
        logger.info("MainWindow::__init__ - Main Window created")
        
        logger.debug("MainWindow::__init__ )>")

    def create_screen_grabber_visualiser(self):
        
        logger.debug("MainWindow::create_screen_grabber_visualiser <(")
            
        # Define a central widget with a specific layout
        # Tip: QLayout cannot be set on the MainWindow directly
        self.screen_grabber_window = QWidget()
        self.setCentralWidget(self.screen_grabber_window)
        self.screen_grabber_window_layout = QGridLayout()
        self.screen_grabber_window.setLayout(self.screen_grabber_window_layout)
        
        # Define control buttons
        self.screen_grab_button = QPushButton("Grab screenshots")
        self.screen_grab_button.clicked.connect(self.on_screen_grab_button_clicked)
        self.set_save_location_button = QPushButton("Set\nsave location")
        self.set_save_location_button.clicked.connect(self.on_set_save_location_button_clicked)
        self.set_start_delay_button = QPushButton("Set\nstart delay")
        self.set_start_delay_button.clicked.connect(self.on_set_start_delay_button_clicked)
        self.set_timeout_button = QPushButton("Set\ntimeout")
        self.set_timeout_button.clicked.connect(self.on_set_timeout_button_clicked)
        self.set_update_frequency_button = QPushButton("Set\nupdate frequency")
        self.set_update_frequency_button.clicked.connect(self.on_set_update_frequency_button_clicked)
        self.set_image_similarity_button = QPushButton("Set\nimage similarity")
        self.set_image_similarity_button.clicked.connect(self.on_set_image_similarity_button_clicked)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)

        # Update the widgets in the selected layout
        self.screen_grabber_window_layout.addWidget(self.set_save_location_button, 1, 1, 1, 2)
        self.screen_grabber_window_layout.addWidget(self.set_start_delay_button, 2, 1, 1, 1)
        self.screen_grabber_window_layout.addWidget(self.set_timeout_button, 2, 2, 1, 1)
        self.screen_grabber_window_layout.addWidget(self.set_update_frequency_button, 3, 1, 1, 1)
        self.screen_grabber_window_layout.addWidget(self.set_image_similarity_button, 3, 2, 1, 1)
        self.screen_grabber_window_layout.addWidget(self.screen_grab_button, 5, 1, 1, 2)
        self.screen_grabber_window_layout.addWidget(self.exit_button, 7, 1, 1, 2)
        self.screen_grabber_window_layout.setRowStretch(0, 1)
        self.screen_grabber_window_layout.setRowStretch(4, 1)
        self.screen_grabber_window_layout.setRowStretch(6, 1)
        self.screen_grabber_window_layout.setRowStretch(8, 1)
        self.screen_grabber_window_layout.setColumnStretch(0, 1)
        self.screen_grabber_window_layout.setColumnStretch(3, 1)
        
        logger.debug("MainWindow::create_screen_grabber_visualiser )>")

    def create_status_bar(self):
        
        logger.debug("MainWindow::create_status_bar <(")
        
        # Instantiate a status bar        
        self.status_bar = QStatusBar()                
        # Define the status bar as part of the main window        
        self.setStatusBar(self.status_bar)        
        # Set text for the status bar        
        self.status_label = QLabel()        
        self.update_status_bar("")
        self.status_bar.addWidget(self.status_label)
        
        logger.debug("MainWindow::create_status_bar )>")

    def on_screen_grab_button_clicked(self):
        
        logger.debug("MainWindow::on_screen_grab_button_clicked <(")
        
        # Instatiate the alert message for the button
        alert = QMessageBox()
        alert.setText("Start process of finding hidden images?")

        # Set standard buttons for the alert window
        alert.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        alert.setDefaultButton(QMessageBox.Yes)
        
        # Handle alert window button press
        alert_value = alert.exec()
        if alert_value == QMessageBox.Yes:
            delayed_background_grab_process = Timer(
                    self.grab_screen_start_delay, 
                    lambda: self.background_grab_process()
            )
            delayed_background_grab_process.start()
            self.update_status_bar(f"Starting process in {self.grab_screen_start_delay} s. Hang on!")
            alert.close()
        
        logger.debug("MainWindow::on_screen_grab_button_clicked )>")

    def on_set_save_location_button_clicked(self):
        
        logger.debug("MainWindow::on_set_save_location_button_clicked <(")
        self.set_save_location()
        logger.debug("MainWindow::on_set_save_location_button_clicked )>")

    def on_set_start_delay_button_clicked(self):
        
        logger.debug("MainWindow::on_set_start_delay_button_clicked <(")
        
        options = ['0', '5', '10']
        value, is_inputted = QInputDialog.getItem(
                self,
                "Process start delay input",
                "Select your desired process start delay:",
                options,
        )
        if is_inputted:
            self.grab_screen_start_delay = float(value)
            logger.debug(f"MainWindow::on_set_start_delay_button_clicked - Updated screen start delay to: {self.grab_screen_start_delay}")
        
        logger.debug("MainWindow::on_set_start_delay_button_clicked )>")

    def on_set_timeout_button_clicked(self):
        
        logger.debug("MainWindow::on_set_timeout_button_clicked <(")
        
        options = ['5', '10', '15', '20']
        value, is_inputted = QInputDialog.getItem(
                self,
                "Process timeout input",
                "Select your desired process timeout:",
                options,
        )
        if is_inputted:
            self.grab_screen_timeout = float(value)
            logger.debug(f"MainWindow::on_set_timeout_button_clicked - Updated screen timeout to: {self.grab_screen_timeout}")
        
        logger.debug("MainWindow::on_set_timeout_button_clicked )>")

    def on_set_update_frequency_button_clicked(self):
        
        logger.debug("MainWindow::on_set_update_frequency_button_clicked <(")
        
        options = ['0.1', '0.25', '0.5', '1', '2']
        value, is_inputted = QInputDialog.getItem(
                self,
                "Process update frequency input",
                "Select your desired process update frequency:",
                options,
        )
        if is_inputted:
            self.grab_screen_frequency = float(value)
            logger.debug(f"MainWindow::on_set_update_frequency_button_clicked - Updated screen frequency to: {self.grab_screen_frequency}")
        
        logger.debug("MainWindow::on_set_update_frequency_button_clicked )>")

    def on_set_image_similarity_button_clicked(self):
        
        logger.debug("MainWindow::on_set_image_similarity_button_clicked <(")
        
        options = ['50', '75', '90', '95']
        value, is_inputted = QInputDialog.getItem(
                self,
                "Process image similarity input",
                "Select your desired process image similarity (%):",
                options,
        )
        if is_inputted:
            self.image_similarity_percentage = float(value)
            logger.debug(f"MainWindow::on_set_image_similarity_button_clicked - Updated image similarity to: {self.image_similarity_percentage}")
        
        logger.debug("MainWindow::on_set_image_similarity_button_clicked )>")

    def calculate_rmse_threshold(self):
        
        logger.debug("MainWindow::calculate_rmse_threshold <(")
        
        self.rmse_threshold = math.sqrt((100 - self.image_similarity_percentage)/100 * ((2**24) ** 2))  # 24-bit colour
        logger.debug(f"MainWindow::calculate_rmse_threshold - Updated RMSE threshold to: {self.rmse_threshold}")
        
        logger.debug("MainWindow::calculate_rmse_threshold )>")

    def background_grab_process(self):
        
        logger.debug("MainWindow::background_grab_process <(")
        
        # Reset timeout
        timeout = self.grab_screen_timeout
        # Reset image list
        self.image_list = []
        # Grab screenshots until timeout
        while timeout > 0:
            
            logger.debug(f"MainWindow::background_grab_process - Time left for screenshot grabbing: {timeout} s")

            # Inform user of the progress of the process
            self.update_status_bar(f"Grabbing screenshots for {self.round_up(timeout, 1)} s...")

            loop_start = time.time()

            self.grab_screen()
            time.sleep(self.grab_screen_frequency)
            self.grab_screen()

            loop_end = time.time()
            loop_elapsed_time = loop_end - loop_start
            logger.debug(f"MainWindow::background_grab_process - Time elapsed between 2 screenshots: {loop_elapsed_time} s")
            
            timeout -= loop_elapsed_time
        
        # Compare screenshots
        self.compare_screenshots()
        
        logger.debug("MainWindow::background_grab_process )>")

    def grab_screen(self):
        
        logger.debug("MainWindow::grab_screen <(")
        
        logger.info("MainWindow::grab_screen - Grabbing a screenshot")
        
        # Method 1 = QApplication self primary screen
        try:
            device_screen = QApplication.primaryScreen()
            logger.debug(f"MainWindow::grab_screen - Device 1 object confirmation: {device_screen}")
            screenshot_1 = device_screen.grabWindow(self.screen_grabber_window.winId())
            self.image_list.append(screenshot_1)
            logger.debug(f"MainWindow::grab_screen - Screenshot 1 object confirmation: {screenshot_1}")
            img_1 = screenshot_1.toImage()
            logger.debug(f"MainWindow::grab_screen - Screenshot 1 dimensions: {img_1.width()} x {img_1.height()}")
            img_1.save(os.path.join(self.img_saved_dir, 'img_1'), 'jpg') 
            logger.debug(f"MainWindow::grab_screen - Saved screenshot at: {os.path.join(self.img_saved_dir, 'img_1.jpg')}")
        except Exception as e:
            logger.warn(f"MainWindow::grab_screen - Exception 1 caught: {e}")

        # # Method 2 = device window from widget
        # try:
        #     device_window = self.windowHandle()
        #     logger.debug(f"MainWindow::grab_screen - Device 2 object confirmation: {device_window}")
        #     device_screen = device_window.screen()
        #     screenshot_2 = device_screen.grabWindow(0)
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 2 object confirmation: {screenshot_2}")
        #     img_2 = screenshot_2.toImage()
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 2 dimensions: {img_2.width()} x {img_2.height()}")
        #     img_2.save(os.path.join(self.img_saved_dir, 'img_2'), 'jpg')
        #     logger.debug(f"MainWindow::grab_screen - Saved screenshot at: {os.path.join(self.img_saved_dir, 'img_2.jpg')}")
        # except Exception as e:
        #     logger.warn(f"MainWindow::grab_screen - Exception 2 caught: {e}")
       
        # # Method 3 = QScreen
        # try:
        #     logger.debug(f"MainWindow::grab_screen - Device 3 object confirmation: None")
        #     screenshot_3 = QScreen.grabWindow(QApplication.primaryScreen(), QApplication.desktop().winId())
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 3 object confirmation: {screenshot_3}")
        #     img_3 = screenshot_3.toImage()
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 3 dimensions: {img_3.width()} x {img_3.height()}")
        #     img_3.save(os.path.join(self.img_saved_dir, 'img_3'), 'jpg') 
        # except Exception as e:
        #     logger.warn(f"MainWindow::grab_screen - Exception 3 caught: {e}")

        # # Method 4 = QApplication screen
        # try:
        #     device_screen = QApplication.primaryScreen()
        #     logger.debug(f"MainWindow::grab_screen - Device 4 object confirmation: {device_screen}")
        #     screenshot_4 = device_screen.grabWindow(self.screen_grabber_window.winId())
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 4 object confirmation: {screenshot_4}")
        #     img_4 = screenshot_4.toImage()
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 4 dimensions: {img_4.width()} x {img_4.height()}")
        #     img_4.save(os.path.join(self.img_saved_dir, 'img_4'), 'jpg') 
        # except Exception as e:
        #     logger.warn(f"MainWindow::grab_screen - Exception 4 caught: {e}")

        # # Method 5 = Screen off QWidget
        # try:
        #     qscreen_window = self.screen_grabber_window.windowHandle()
        #     logger.debug(f"MainWindow::grab_screen - Device 5 object confirmation: {qscreen_window}")
        #     device_screen = qscreen_window.screen()
        #     screenshot_5 = device_screen.grabWindow(0)
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 5 object confirmation: {screenshot_5}")
        #     img_5 = screenshot_5.toImage()
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 5 dimensions: {img_5.width()} x {img_5.height()}")
        #     img_5.save(os.path.join(self.img_saved_dir, 'img_5'), 'jpg')
        # except Exception as e:
        #     logger.warn(f"MainWindow::grab_screen - Exception 5 caught: {e}")

        # # Method 6 = QApplication screen
        # try:
        #     device_screen = QApplication.primaryScreen()
        #     logger.debug(f"MainWindow::grab_screen - Device 6 object confirmation: {device_screen}")
        #     screenshot_6 = device_screen.grabWindow(QApplication.desktop().winId())
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 6 object confirmation: {screenshot_6}")
        #     img_6 = screenshot_6.toImage()
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 6 dimensions: {img_6.width()} x {img_6.height()}")
        #     img_6.save(os.path.join(self.img_saved_dir, 'img_6'), 'jpg') 
        # except Exception as e:
        #     logger.warn(f"MainWindow::grab_screen - Exception 6 caught: {e}")

        # # Method 7 = QApplication primary
        # try:
        #     all_screens = QApplication.screens()
        #     logger.debug(f"MainWindow::grab_screen - Device 7 all screens: {all_screens}")
        #     all_windows = QApplication.allWindows()
        #     logger.debug(f"MainWindow::grab_screen - Device 7 all windows: {all_windows}")
        #     device_screen = QApplication.primaryScreen()
        #     logger.debug(f"MainWindow::grab_screen - Device 7 screen confirmation: {device_screen}")
        #     device_screen_size = device_screen.size()
        #     logger.debug(f"MainWindow::grab_screen - Device 7 screen size confirmation: {device_screen_size}")
        #     temp_img_a = 'img_7a'
        #     temp_img_b = 'img_7b'
        #     for win in range(len(all_windows)):
        #         logger.debug(f"MainWindow::grab_screen - Window {win} object: {all_windows[win]}")
        #         logger.debug(f"MainWindow::grab_screen - Window {win} dimensions: {all_windows[win].width()} x {all_windows[win].height()}")
        #         screenshot_7 = device_screen.grabWindow(win)
        #         logger.debug(f"MainWindow::grab_screen - Window {win} QPixmap confirmation: {screenshot_7}")
        #         logger.debug(f"MainWindow::grab_screen - Window {win} dimensions: {screenshot_7.size()}")
        #         screenshot_7.save(os.path.join(self.img_saved_dir, 'img_7a'), 'jpg') 
        #         temp_img_a += 'a'
        #         img_7 = screenshot_7.toImage()
        #         logger.debug(f"MainWindow::grab_screen - Image 7 dimensions: {img_7.width()} x {img_7.height()}")
        #         img_7.save(os.path.join(self.img_saved_dir, 'img_7b'), 'jpg') 
        #         temp_img_b += 'b'
        # except Exception as e:
        #     logger.warn(f"MainWindow::grab_screen - Exception 7 caught: {e}")

        # # Method 8 = QApplication screen
        # try:
        #     device_screen = QApplication.primaryScreen()
        #     logger.debug(f"MainWindow::grab_screen - Device 8 object confirmation: {device_screen}")
        #     screenshot_8 = device_screen.grabWindow(QApplication.desktop().winId(), 0, 0, 100, 100)
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 8 object confirmation: {screenshot_8}")
        #     img_8 = screenshot_8.toImage()
        #     logger.debug(f"MainWindow::grab_screen - Screenshot 8 dimensions: {img_8.width()} x {img_8.height()}")
        #     img_8.save(os.path.join(self.img_saved_dir, 'img_8'), 'jpg') 
        # except Exception as e:
        #     logger.warn(f"MainWindow::grab_screen - Exception 8 caught: {e}")

        logger.debug(f"MainWindow::grab_screen - Total screenshots taken: {len(self.image_list)}")

        logger.debug("MainWindow::grab_screen )>")

    def set_save_location(self):
        
        logger.debug("MainWindow::set_save_location <(")
       
        # Parametrise the File Dialog to select a directory to save content to
        file_dlg = QFileDialog()
        file_dlg.setAcceptMode(QFileDialog.AcceptOpen)
        file_dlg.setFileMode(QFileDialog.Directory)
        file_dlg.setOption(QFileDialog.DontUseNativeDialog)  # Custom dialog for more control on the options
        file_dlg.setViewMode(QFileDialog.List)
        
        # Define list of local writable locations
        std_path_list = [
                QStandardPaths.HomeLocation,
                QStandardPaths.DesktopLocation,
                QStandardPaths.PicturesLocation,
                QStandardPaths.MoviesLocation,
                QStandardPaths.DownloadLocation,
                QStandardPaths.AppDataLocation,
                QStandardPaths.AppLocalDataLocation,
        ]
        
        url_list = []

        for index, std_path in enumerate(std_path_list):
            if std_path:
                for path in QStandardPaths.standardLocations(std_path):
                    local_path = QUrl.fromLocalFile(path)
                    url_list.append(local_path)
                    logger.debug(f"MainWindow::set_save_location - Added path {local_path} to the list of urls")
            else:
                logger.debug(f"MainWindow::set_save_location - Std path index {index} is empty")

        file_dlg.setSidebarUrls(url_list)
        logger.debug(f"MainWindow::set_save_location - Sidebar contains the following urls: {file_dlg.sidebarUrls()}")
        
        # React to dialog execution
        if file_dlg.exec_():

            self.img_saved_dir = file_dlg.selectedFiles()[0]
            logger.debug(f"MainWindow::set_save_location - Selected directory: {self.img_saved_dir}")
        
            # Check write permissions for folder otherwise change to current folder
            if not os.access(self.img_saved_dir, os.W_OK):
                self.img_saved_dir = os.getcwd()
                logger.debug(f"MainWindow::set_save_location - No write permission on selected directory, changing to: {self.img_saved_dir}")
            
            logger.debug(f"MainWindow::set_save_location - Updated save location to: {self.img_saved_dir}")
        
        logger.debug("MainWindow::set_save_location )>")

    def compare_screenshots(self):
        
        logger.debug("MainWindow::compare_screenshots <(")
        
        # Inform user of the progress of the process
        self.update_status_bar("Comparing screenshots...")
        
        # Ensure image list contains enough images
        logger.debug(f"MainWindow::compare_screenshots - Total of images to compare: {len(self.image_list)}-1={len(self.image_list)-1} (since coupled)")
        if len(self.image_list) > 1 and len(self.image_list)%2 == 0:
            
            logger.info("MainWindow::compare_screenshots - Comparing stored screenshots")
            
            # Update rmse threshold
            self.calculate_rmse_threshold()

            for counter in range(len(self.image_list)-1):
                
                self.update_status_bar(f"Comparing screenshots {counter+1}/{len(self.image_list)-1}...")
                logger.debug(f"MainWindow::compare_screenshots - Progress: {counter+1}/{len(self.image_list)-1}")

                # Convert QPixmap to QImage
                image_1 = self.image_list[counter].toImage()
                image_2 = self.image_list[counter + 1].toImage()
                
                # Calculate the 'Root Mean Squared Error' between the two images is the
                # sum of the squared difference between the two images;
                # NOTE: the two images must have the same dimension
                w = image_1.width()
                h = image_1.height()
                
                logger.debug(f"MainWindow::compare_screenshots - Image dimensions in pixels: w={w} | h={h}")
                
                squared_err = 0
                logger.debug(f"MainWindow::compare_screenshots - Image 1 initial pixel: {image_1.pixel(0, 0)}")
                logger.debug(f"MainWindow::compare_screenshots - Image 2 initial pixel: {image_2.pixel(0, 0)}")
                for x in range(w):
                    for y in range(h):
                        squared_err += (image_1.pixel(x, y) - image_2.pixel(x, y)) ** 2
                # Ensure that there is no division by zero
                if w == 0 or h == 0:
                    w = 1
                    h = 1
                mse = squared_err/float(w * h)  # Divide by the number of pixels
                rmse = math.sqrt(mse)  # Take the square root of the MSE
                logger.debug(f"MainWindow::compare_screenshots - RMSE calculated = {rmse}")

                # return the RMSE, the lower the error, the more "similar" "the two images are
                # NOTE: With the similarity indicator, if it is negative, then the images are similar
                similarity_calc = rmse - self.rmse_threshold
                logger.debug(f"MainWindow::compare_screenshots - Similarity calculated = {similarity_calc}")
                similarity_indicator = True if similarity_calc < 0 else False
                logger.debug(f"MainWindow::compare_screenshots - Are images similar? {similarity_indicator}")

                # Save the 2 different images
                if not similarity_indicator:
                    logger.debug(f"MainWindow::compare_screenshots - Images differ, therefore saving them in {self.img_saved_dir}")
                    image_1.save(os.path.join(self.img_saved_dir, self.image_saved_name), 'jpg')
                    self.image_saved_name += '1'
                    image_2.save(os.path.join(self.img_saved_dir, self.image_saved_name), 'jpg')
                    self.image_saved_name += '1'
                
        else:
            logger.warn("MainWindow::compare_screenshots - Cannot perform screenshot comparison")
            pass

        # Inform user of the completion of the process
        logger.info("MainWindow::compare_screenshots - Finished comparing screenshots")
        self.update_status_bar("Done.")
        
        logger.debug("MainWindow::compare_screenshots )>")

    def update_status_bar(self, txt):

        logger.debug("MainWindow::update_status_bar <(")
        self.status_label.setText(txt)
        logger.debug("MainWindow::update_status_bar )>")

    def round_up(self, nb_to_round, decimals = 0): 
        
        logger.debug("MainWindow::round_up <(")
        multiplier = 10 ** decimals
        rounded_up_nb = math.ceil(nb_to_round * multiplier) / multiplier
        logger.debug("MainWindow::round_up )>")
        
        return rounded_up_nb

def main():
    
    logger.info("========================\n")
    logger.info("========================")
    logger.debug("main <(")
    logger.debug("main - Logger instantiated")
    logger.debug("main - Log output file can be found at: " + str(logger_output_file_path))

    # Define the app object/instance
    app = QApplication(sys.argv)
    
    # Create a Qt widget, which will be our window.
    main_window = MainWindow()
    
    # Start the event loop and handle the exit code
    logger.info("main - App started")
    sys.exit(app.exec())
    logger.info("main - App terminated")
    
    logger.debug("main )>")

if __name__ == "__main__":        
    main()
