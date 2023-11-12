#!/usr/bin/env python3

# Aim: Beat the pause game by capturing the quickly switched image in a video automatically

# Refresher: the pause game consists in hiding a picture in one frame of a video and
# let the user try to see it by pausing the video
# Note that the pause takes a few seconds to actually trigger
# making the game pretty hard sometimes

# Concept:
# 1) Record screenshots in the background while playing the video
# 2) Identify image / frame changes and save at each sharp change
# 3) Reveal the images hidden to the user (hopefully including the hidden one)

import sys
from threading import Timer
import math
import time
import os
import logging as log_tool # The logging library for debugging
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QMessageBox, QStatusBar, QLabel, QFileDialog, QInputDialog

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
        
        device_screen = QApplication.primaryScreen()
        screenshot = device_screen.grabWindow(self.screen_grabber_window.winId())
        self.image_list.append(screenshot)
        
        logger.debug(f"MainWindow::grab_screen - Total screenshots taken: {len(self.image_list)}")

        logger.debug("MainWindow::grab_screen )>")

    def set_save_location(self):
        
        logger.debug("MainWindow::set_save_location <(")
        
        self.img_saved_dir = QFileDialog.getExistingDirectory(self, "Select a Directory")
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
        logger.debug(f"MainWindow::compare_screenshots - Total of images to compare: {len(self.image_list)}-1 (since coupled)")
        if len(self.image_list) > 1 and len(self.image_list)%2 == 0:
            
            logger.info("MainWindow::compare_screenshots - Comparing stored screenshots")
            
            # Update rmse threshold
            self.calculate_rmse_threshold()

            for counter in range(len(self.image_list)-1):
                
                logger.debug(f"MainWindow::compare_screenshots - Progress: {counter+1}/{len(self.image_list)-1}")

                # Convert QPixmap to QImage
                image_1 = self.image_list[counter].toImage()
                image_2 = self.image_list[counter + 1].toImage()
                
                # Calculate the 'Root Mean Squared Error' between the two images is the
                # sum of the squared difference between the two images;
                # NOTE: the two images must have the same dimension
                w = image_1.width()
                h = image_1.height()
                squared_err = 0
                for x in range(w):
                    for y in range(h):
                        squared_err += (image_1.pixel(x, y) - image_2.pixel(x, y)) ** 2
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
