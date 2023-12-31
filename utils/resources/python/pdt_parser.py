#!/usr/bin/env python3

# ---- INTRODUCTION ----
# Pdt file parser based on python file parsing utilities

import os.path
import sys

class PdtParser():
    def __init__(self, input_pdt_path):
        self.pdt_path = input_pdt_path
        with open(self.pdt_path) as pdt_object:
            pdt_data = pdt_object.readlines()
        self.pdt_data = pdt_data
    
    def __del__(self):
        pass

    def get_sysroot_path(self):
        try:
            sysroot_entries = [line for line in self.pdt_data if line.startswith('sysroot ')]
            # TODO: add sysroots_dir potential entry
            sysroot_entry_split = sysroot_entries[0].split("\"")
            sysroot_entry_relative_path = sysroot_entry_split[1]
            if sysroot_entry_relative_path == '':
                raise Exception("Sysroot path not specified in pdt")
            sysroot_path = os.path.join(os.path.dirname(os.path.abspath(self.pdt_path)), sysroot_entry_relative_path)
            return sysroot_path
        except Exception as e:
            print("[ERROR] Cannot find sysroot path")
            print("Error message:\n" + str(e))
            sys.exit(1)

    def get_app_name(self):
        try:
            application_entry = [line for line in self.pdt_data if line.startswith('[Application]')]
            application_entry_index = self.pdt_data.index(application_entry[0])
            application_name_entry_split = self.pdt_data[application_entry_index + 4].split("\"")
            application_name_entry = application_name_entry_split[1]
            if application_name_entry == '':
                raise Exception("Application name not specified in pdt")
            app_name = application_name_entry
            return app_name
        except Exception as e:
            print("[ERROR] Cannot find application name")
            print("Error message:\n" + str(e))
            sys.exit(1)
    
    def get_app_entry_point_script_name(self):
        try:
            entry_point_entries = [line for line in self.pdt_data if line.startswith('entry_point ')]
            entry_point_entry_split = entry_point_entries[0].split("\"")
            entry_point_entry = entry_point_entry_split[1]
            if entry_point_entry == '':
                raise Exception("Entry point not specified in pdt")
            # Remove folder structure preceeding the script name
            entrypoint_end_part = entry_point_entry.split(".")[-1]
            # Remove callable
            entrypoint_script_ref = entrypoint_end_part.split(":")[0]
            app_entrypoint_script_name = entrypoint_script_ref
            return app_entrypoint_script_name
        except Exception as e:
            print("[ERROR] Cannot find application entrypoint script name")
            print("Error message:\n" + str(e))
            sys.exit(1)

    def get_app_package_path(self):
        try:
            application_package_entry = [line for line in self.pdt_data if line.startswith('[Application.Package]')]
            application_package_entry_index = self.pdt_data.index(application_package_entry[0])
            application_package_name_entry_split = self.pdt_data[application_package_entry_index + 1].split("\"")
            application_package_name_entry = application_package_name_entry_split[1]
            if application_package_name_entry == '':
                raise Exception("Package path not specified in pdt")
            app_package_relative_path = application_package_name_entry
            app_package_path = os.path.join(os.path.dirname(os.path.abspath(self.pdt_path)), app_package_relative_path)
            return app_package_path
        except Exception as e:
            print("[ERROR] Cannot find application package path")
            print("Error message:\n" + str(e))
            sys.exit(1)

# Example code
script_folder = os.path.dirname(os.path.realpath(__file__))
print(f"Current script folder location: {script_folder}")
pdt_path = os.path.abspath(os.path.join(script_folder, os.path.pardir, os.path.pardir, 'pyqt-demo.pdt'))
print(f"Pdt path: {pdt_path}")
my_parser = PdtParser(pdt_path)
pdt_data = my_parser.pdt_data
print(f"Pdt data: {pdt_data}")
sysroot_path = my_parser.get_sysroot_path()
print(f"Sysroot path: {sysroot_path}")
app_name = my_parser.get_app_name()
print(f"Application name: {app_name}")
app_entry_point_script_name = my_parser.get_app_entry_point_script_name()
print(f"Application entry point script name: {app_entry_point_script_name}")
app_package_path = my_parser.get_app_package_path()
print(f"Application package path: {app_package_path}")

