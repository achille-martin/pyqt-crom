#!/usr/bin/env python3

# ---- INTRODUCTION ----
# Pdy file parser based on the xml parser Element Tree library:
# https://docs.python.org/3/library/xml.etree.elementtree.html

import xml.etree.ElementTree as ET
import os.path
import sys

class PdyParser():
    def __init__(self, input_xml_path):
        self.root = ET.parse(input_xml_path).getroot()
    
    def __del__(self):
        pass

    def get_app_name(self):
        try:
            application_tag = self.root.find('Application')
            app_name = application_tag.attrib['name']
            return app_name
        except Exception as e:
            print("[ERROR] Cannot find application name")
            print("Error message:\n" + str(e))
            sys.exit(1)
    
    def get_app_entrypoint_script_name(self):
        try:
            application_tag = self.root.find('Application')
            entrypoint_full = application_tag.attrib['entrypoint']
            # Remove folder structure preceeding the script name
            entrypoint_end_part = entrypoint_full.split(".")[-1]
            # Remove callable
            entrypoint_script_ref = entrypoint_end_part.split(":")[0]
            # Add extension
            entrypoint_script_name = entrypoint_script_ref + ".py"
            return entrypoint_script_name
        except Exception as e:
            print("[ERROR] Cannot find application entrypoint script name")
            print("Error message:\n" + str(e))
            sys.exit(1)

    def get_app_package_path(self):
        try:
            application_tag = self.root.find('Application')
            package_tag =  application_tag.find('Package')
            package_path = package_tag.attrib['name']
            return package_path
        except Exception as e:
            print("[ERROR] Cannot find application package path")
            print("Error message:\n" + str(e))
            sys.exit(1)

# Example code
# script_folder = os.path.dirname(os.path.realpath(__file__)) 
# my_parser = PdyParser(os.path.join(script_folder, os.path.pardir, 'config_app.pdy'))
# app_name = my_parser.get_app_name()
# print("App name: " + str(app_name))
# app_entrypoint_script_name = my_parser.get_app_entrypoint_script_name()
# print("App entrypoint script name: " + str(app_entrypoint_script_name))
# app_package_path = my_parser.get_app_package_path()
# print("App package path: " + str(app_package_path))

