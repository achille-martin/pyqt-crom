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
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QMessageBox, QStatusBar, QLabel, QFileDialog

class MainWindow(QMainWindow):
    
    def __init__(self):
        
        super().__init__()
        
        # Set main window title
        self.setWindowTitle("Basic geometry shape visualiser")
        
        # Create components of the main window
        self.create_screen_grabber_visualiser()
        self.create_status_bar()

        # Configure settings for the app
        self.grab_screen_timeout = 5  # s
        self.grab_screen_frequency = 0.25  # s
        self.image_saved_name = "screenshot_saved_1"
        self.image_similarity_percentage = 80  # % - How similar are the images
        
        # Create useful variables
        self.image_list = []
        self.img_saved_dir = None
        self.rmse_threshold = math.sqrt((100 - self.image_similarity_percentage)/100 * ((2**24) ** 2))  # 24-bit colour
        print(f"RMSE threshold = {self.rmse_threshold}")

        # Display the main window
        self.showMaximized()

    def create_screen_grabber_visualiser(self):
            
        # Define a central widget with a specific layout
        # Tip: QLayout cannot be set on the MainWindow directly
        self.screen_grabber_window = QWidget()
        self.setCentralWidget(self.screen_grabber_window)
        self.screen_grabber_window_layout = QGridLayout()
        self.screen_grabber_window.setLayout(self.screen_grabber_window_layout)
        
        # Define control buttons
        self.screen_grab_button = QPushButton("Grab screenshots")
        self.screen_grab_button.clicked.connect(self.on_screen_grab_button_clicked)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)

        # Update the widgets in the selected layout
        self.screen_grabber_window_layout.addWidget(self.screen_grab_button, 1, 1, 1, 1)
        self.screen_grabber_window_layout.addWidget(self.exit_button, 3, 1, 1, 1)
        self.screen_grabber_window_layout.setRowStretch(0, 1)
        self.screen_grabber_window_layout.setRowStretch(2, 1)
        self.screen_grabber_window_layout.setRowStretch(4, 1)
        self.screen_grabber_window_layout.setColumnStretch(0, 1)
        self.screen_grabber_window_layout.setColumnStretch(2, 1)

    def create_status_bar(self):
        # Instantiate a status bar        
        self.status_bar = QStatusBar()                
        # Define the status bar as part of the main window        
        self.setStatusBar(self.status_bar)        
        # Set text for the status bar        
        self.status_label = QLabel()        
        self.update_status_bar("")
        self.status_bar.addWidget(self.status_label)

    def on_screen_grab_button_clicked(self):
        
        # Instatiate the alert message for the button
        alert = QMessageBox()
        alert.setText("Set save location\nand start grabbing screenshots?")

        # Set standard buttons for the alert window
        alert.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        alert.setDefaultButton(QMessageBox.Yes)
        
        # Handle alert window button press
        alert_value = alert.exec()
        if alert_value == QMessageBox.Yes:
            # Specify saving location
            self.get_save_location()
            delayed_background_grab_process = Timer(0, lambda: self.background_grab_process())
            delayed_background_grab_process.start()
            alert.close()

    def background_grab_process(self):
        # Reset timeout
        timeout = self.grab_screen_timeout
        # Reset image list
        self.image_list = []
        # Grab screenshots until timeout
        while timeout > 0:
            # Inform user of the progress of the process
            self.update_status_bar(f"Grabbing screenshots for {round(timeout, 1)} s...")
            loop_start = time.time()
            self.grab_screen()
            time.sleep(self.grab_screen_frequency)
            self.grab_screen()
            loop_end = time.time()
            loop_elapsed_time = loop_end - loop_start
            print(loop_elapsed_time)
            timeout -= loop_elapsed_time
        # Compare screenshots
        self.compare_screenshots()

    def grab_screen(self):
        print("Grabbing Screenshot")
        device_screen = QApplication.primaryScreen()
        screenshot = device_screen.grabWindow(self.screen_grabber_window.winId())
        self.image_list.append(screenshot)

    def get_save_location(self):
        self.img_saved_dir = QFileDialog.getExistingDirectory(self, "Select a Directory")
        print(f"Selected directory: {self.img_saved_dir}")
        # Check write permissions for folder otherwise change to current folder
        if not os.access(self.img_saved_dir, os.W_OK):
            self.img_saved_dir = os.getcwd()
            print(f"No write permission on selected directory, changing to: {self.img_saved_dir}")

    def compare_screenshots(self):
        # Inform user of the progress of the process
        self.update_status_bar("Comparing screenshots...")
        # Ensure image list contains enough images
        if len(self.image_list) > 1 and len(self.image_list)%2 == 0:
            print("Comparing screenshots")
            
            for counter in range(len(self.image_list)-1):

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
                print(f"RMSE = {rmse}")

                # return the RMSE, the lower the error, the more "similar" "the two images are
                # NOTE: With the similarity indicator, if it is negative, then the images are similar
                similarity_calc = rmse - self.rmse_threshold
                print(f"Similarity calculation = {similarity_calc}")
                similarity_indicator = True if similarity_calc < 0 else False
                print(f"Images are similar? {similarity_indicator}")

                # Save the 2 different images
                if not similarity_indicator:
                    print(f"Save images in: {self.img_saved_dir}")
                    image_1.save(os.path.join(self.img_saved_dir, self.image_saved_name), 'jpg')
                    self.image_saved_name += '1'
                    image_2.save(os.path.join(self.img_saved_dir, self.image_saved_name), 'jpg')
                    self.image_saved_name += '1'
                
        else:
            print("Cannot perform screenshot comparison")

        # Inform user of the completion of the process
        print("Compared screenshots")
        self.update_status_bar("Done.")

    def update_status_bar(self, txt):
        self.status_label.setText(txt)


if __name__ == '__main__':

    # Define the app object/instance
    app = QApplication(sys.argv)
    
    # Create a Qt widget, which will be our window.
    main_window = MainWindow()
    
    # Start the event loop and handle the exit code
    sys.exit(app.exec())
