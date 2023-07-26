#!/usr/bin/env python3

# ---- INTRODUCTION ----
# Pdy file parser based on the xml parser Element Tree library:
# https://docs.python.org/3/library/xml.etree.elementtree.html

import xml.etree.ElementTree as ET

class PdyParser():
    def __init__(self, input_xml_path):
        self.root = ET.parse(input_xml_path).getroot()
    
    def __del__(self):
        pass

    def get_app_name(self):
        application_tag = self.root.find('Application')
        return application_tag.attrib['name']

# Example code
# my_parser = PdyParser('./config-app.pdy')
# app_name = my_parser.get_app_name()
# print(app_name)

