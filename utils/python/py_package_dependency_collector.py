#!/usr/bin/env python3

# MIT License

# Copyright (c) 2024 Achille MARTIN

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

# ---- INTRODUCTION ----
# Python package dependency collector
# based on module imports

# Note: this script assumes that pip package names
# that are searched have been installed on the machine

# Example:
# pip install pyyaml
# python3 py_package_dependency_collector -n pyyaml

import argparse
import sys
from os import walk
from os.path import (
    realpath, 
    join,
    isdir,
    isfile,
)
import subprocess
from importlib_metadata import packages_distributions
import list_imports
from inspect import cleandoc as cl


class PyDepCollector():
    def __init__(self):

        # Ensure minimum python version
        major, minor, micro = sys.version_info[:3]
        self.py_version = f"{major}.{minor}"
        assert sys.version_info >= (3, 10), \
            f"Python 3.10 or higher is required \n\
            Your Python version is: {self.py_version}"
        
        # Initialise attributes
        self.deps_collected_list = []
        
        print(
            cl(
                f"""
                [DEBUG] Initialised PyDepCollector object
                ----------
                """
            )
        )

    def collect_deps_from_pkg_name(self, py_pkg_name): 
        assert isinstance(py_pkg_name, str), \
            f"Python package name must be a string\
            This is your input: {py_pkg_name}"

        print(
            cl(
                f"""
                [DEBUG] Received request
                to collect deps
                from pkg name:
                {py_pkg_name}
                ----------
                """
            )
        )
     
        # Initialise pkg installation path list
        # associated to py pkg name
        pkg_installation_path_list = []

        try:
            # Retrieve PyPI package name from pip package name
            # using `pip show <py_pkg_name>`
            pip_show_res_b = subprocess.check_output(
                ["pip", "show", py_pkg_name]
            )
            pip_show_res_b_list = pip_show_res_b.split(b"\n")
            pip_show_res_list = [
                elem.decode('utf-8') 
                for elem 
                in pip_show_res_b_list
            ]
            pip_show_res_dict = {
                elem.split(":")[0]: elem.split(":")[1].lstrip() 
                for elem 
                in pip_show_res_list
                if ":" in elem
            }
            pypi_pkg_name = pip_show_res_dict["Name"]
            print(
                cl(
                    f"""
                    [DEBUG] pkg name {py_pkg_name}
                    is equivalent to pypi package name:
                    {pypi_pkg_name}
                    ----------
                    """
                )
            )
            
            # Retrieve site-packages names from PyPI package name
            # using `importlib.metadata`
            pkg_distr_dict = packages_distributions()
            site_pkg_name_list = [
                key
                for key, value in pkg_distr_dict.items()
                if value[0] == pypi_pkg_name
            ]
            print(
                cl(
                    f"""
                    [DEBUG] pypi package name {pypi_pkg_name}
                    is associated to site package names:
                    {site_pkg_name_list}
                    ----------
                    """
                )
            )
            
            # Identify installation path of site-packages names
            pkg_installation_path_list = [
                join(pip_show_res_dict["Location"], name)
                for name
                in site_pkg_name_list
            ]
            print(
                cl(
                    f"""
                    [DEBUG] site package names can be found
                    at locations:
                    {pkg_installation_path_list}
                    ----------
                    """
                )
            )
        except Exception as e:
            print(
                cl(
                    f"""
                    [WARN] Cannot collect deps from pkg name {py_pkg_name}
                    Exception caught: {e}
                    ----------
                    """
                )
            )

        # Search through the python package
        # at the specific path
        for path in pkg_installation_path_list:
            self.collect_deps_from_pkg_path(path)
    
    def collect_deps_from_pkg_path(self, py_pkg_path):
        assert isinstance(py_pkg_path, str), \
            f"Python package path must be a string\
            This is your input: {py_pkg_path}"
         
        print(
            cl(
                f"""
                [DEBUG] Received request
                to collect deps
                from pkg path:
                {py_pkg_path}
                ----------
                """
            )
        )

        try:

            # Determine if path exists
            py_pkg_path = realpath(py_pkg_path)
            print(
                cl(
                    f"""
                    [DEBUG] The pkg path exists
                    and is equivalent to:
                    {py_pkg_path}
                    ----------
                    """
                )
            )
            
            # Initialise list of python files in path
            py_file_list = []
            
            # Determine whether path is a directory
            if isdir(py_pkg_path):
                for dir_path, dir_names, file_names in walk(py_pkg_path):
                    for file_name in file_names:
                        file_path = join(dir_path, file_name)
                        if file_path.endswith('.py'):
                            py_file_list.append(file_path)
            
            # Determine whether path is a file
            if isfile(py_pkg_path):
                py_file_list.append(py_pkg_path)

            # Collect imports from each py file
            for file_path in py_file_list:
                py_file_imports = []
                try:
                    py_file_imports = list_imports.get(file_path)
                except Exception as e:
                    print(
                        cl(
                            f"""
                            [WARN] Cannot collect deps for py file {file_path}
                            Exception caught: {e}
                            ----------
                            """
                        )
                    )
                self.deps_collected_list.extend(py_file_imports)

        except Exception as e:
            print(
                cl(
                    f"""
                    [WARN] Cannot collect deps from pkg path {py_pkg_path}
                    Exception caught: {e}
                    ----------
                    """
                )
            )
        
        # Make deps collected list unique for clarity
        self.deps_collected_list = list(
            set(
                self.deps_collected_list
            )
        )

        # Sort deps collected list for clarity
        self.deps_collected_list.sort()

    def get_deps_list(self):
        print(
            cl(
                f"""
                [DEBUG] Received request
                to share deps list
                ----------
                """
            )
        )
        return self.deps_collected_list
    
    # Method returning the top-level imports (before the `.`)
    # and sorting the imports by module origin if `pdt_format`
    # is set to `True`
    def get_top_level_deps_list(self, pdt_format=False):
        print(
            cl(
                f"""
                [DEBUG] Received request
                to share top-level deps list
                with pdt format option {pdt_format}
                ----------
                """
            )
        )
        top_level_deps_collected_list = []
        return top_level_deps_collected_list

    def reset_deps_list(self):
        self.deps_collected_list = []


def parse_args():
    # Instantiate argument parser
    parser = argparse.ArgumentParser()
    
    # Add arguments
    parser.add_argument(
        "-n",
        "--pkg-name",
        dest="pkg_name",
        type=str,
        action="store",
        help="Search through an installed pip python package for its dependencies",
    )
    parser.add_argument(
        "-p",
        "--pkg-path", 
        dest="pkg_path",
        type=str,
        action="store",
        help="Search through a python package for its dependencies from its root path",
    )
    
    # Collect arguments
    args = parser.parse_args()
    
    # Ensure one argument only is used  
    if not args.pkg_name and not args.pkg_path:
        parser.error("Please specify at least one argument")
    elif args.pkg_name and args.pkg_path:
        parser.error("Please only specify one argument")
    else:
        pass
    
    return args

def main():
    # Parse arguments
    inputs=parse_args()
    
    # Instantiate python dependency collector
    py_dep_collector = PyDepCollector()

    # Start dependency collection
    if inputs.pkg_name:
        py_dep_collector.collect_deps_from_pkg_name(inputs.pkg_name)
    elif inputs.pkg_path:
        py_dep_collector.collect_deps_from_pkg_path(inputs.pkg_path)
    else:
        pass

    # Get dependency list
    deps_list = py_dep_collector.get_deps_list()
    # deps_list = py_dep_collector.get_top_level_deps_list()
    print(
        cl(
            f"""
            [INFO] Dependencies obtained:
            {deps_list}
            ----------
            """
        )
    )

if __name__ == "__main__":
    main()
