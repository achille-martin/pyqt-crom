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

# Assumption 1: this script assumes that pip package names
# that are searched have been installed on the machine
# Assumption 2: this script will not search
# for folders with unique leading underscore
# and will not search
# for files with unique leading underscore
# since they are all meant for internal use

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
    basename,
)
import subprocess
from importlib_metadata import packages_distributions
from stdlib_list import stdlib_list
import list_imports
from inspect import cleandoc as cl
import re


class PyDepCollector():
    def __init__(self):

        # Initialise attributes
        self.deps_collected_list = []
        self.pip_required_deps_list = []
        self.site_pkg_names_list = []
        
        print(
            cl(
                f"""
                [DEBUG] Initialised PyDepCollector object
                Dependencies collected list is:
                {self.deps_collected_list}
                ----------
                """
            )
        )

    def collect_deps_from_pkg_name(
            self, 
            py_pkg_name,
            dir_name_exclusion_list=[],
            file_name_exclusion_list=[]): 

        print(
            cl(
                f"""
                [DEBUG] Received request
                to collect deps
                from pkg name:
                {py_pkg_name}
                with directories to exclude:
                {dir_name_exclusion_list}
                and files to exclude:
                {file_name_exclusion_list}
                ----------
                """
            )
        )
     
        # Initialise pkg installation path list
        # associated to py pkg name
        pkg_installation_path_list = []

        try:
            # Ensure that py pkg name is a string
            if not isinstance(py_pkg_name, str):
                raise Exception(
                    f"""
                    Python package name must be a string
                    This is your input: {py_pkg_name}
                    ----------
                    """
                )
           
            # Reset pip required deps list
            self.reset_pip_required_deps_list()

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
            # Note that the names starting with a unique underscore
            # are dropped
            pkg_distr_dict = packages_distributions()
            site_pkg_names_list = [
                key
                for key, value in pkg_distr_dict.items()
                if (value[0] == pypi_pkg_name
                    and not re.search("^_[^_].*$", key))
            ]
            self.site_pkg_names_list.extend(site_pkg_names_list)
            print(
                cl(
                    f"""
                    [DEBUG] pypi package name {pypi_pkg_name}
                    is associated to site package names:
                    {self.site_pkg_names_list}
                    ----------
                    """
                )
            )
            
            # Identify installation path of site-packages names
            pkg_installation_path_list = [
                join(pip_show_res_dict["Location"], name)
                for name
                in self.site_pkg_names_list
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
            
            # Save pip required deps
            print(pip_show_res_dict["Requires"])
            self.pip_required_deps_list.extend(
                pip_show_res_dict["Requires"].split(",")
            )
            print(
                cl(
                    f"""
                    [DEBUG] Saved pip required deps:
                    {self.pip_required_deps_list}
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
            self.collect_deps_from_pkg_path(
                path,
                dir_name_exclusion_list,
                file_name_exclusion_list, 
            )
    
    def collect_deps_from_pkg_path(
            self, 
            py_pkg_path,
            dir_name_exclusion_list=[],
            file_name_exclusion_list=[]): 
         
        print(
            cl(
                f"""
                [DEBUG] Received request
                to collect deps
                from pkg path:
                {py_pkg_path}
                with directories to exclude:
                {dir_name_exclusion_list}
                and files to exclude:
                {file_name_exclusion_list}
                ----------
                """
            )
        )

        try:
            # Ensure that py pkg path is a string
            if not isinstance(py_pkg_path, str):
                raise Exception(
                    f"""
                    Python package name must be a string
                    This is your input: {py_pkg_path}
                    ----------
                    """
                )

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
                # Create a list of directories
                # and exclude directory names
                # starting with `_` (since they are for internal use)
                # as well as the dir names
                # specified in the dir_name_exclusion_list
                for dir_path, dir_names, file_names in walk(py_pkg_path, topdown=True):
                    # Modify directory names in place
                    # to make the exclusion effective
                    dir_names[:] = [
                        d 
                        for d in dir_names 
                        if (d not in set(dir_name_exclusion_list)
                            and not re.search("^_[^_].*$", d))
                    ]
                    for file_name in file_names:
                        file_path = join(dir_path, file_name)
                        # Confirm that file has python extension
                        # and does not start with a unique `_`
                        # since meant for internal use only
                        # Besides, exclude file names
                        # specified in the file_name_exclusion_list
                        if (not re.search("^_[^_].*$", file_path) 
                                and re.search("(\.py)$", file_path)
                                and file_name not in file_name_exclusion_list):
                            py_file_list.append(file_path)
            
            # Determine whether path is a file
            if (isfile(py_pkg_path) 
                    and basename(py_pkg_path) 
                    not in file_name_exclusion_list):
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
        
        # Make deps collected list unique and sorted for clarity
        self.deps_collected_list = list(
            set(
                self.deps_collected_list
            )
        )
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
        
        # Split deps collected 
        # and retrieve only top level module
        top_level_deps_collected_list = [
            dep_name.split(".")[0] 
            for dep_name 
            in self.deps_collected_list
        ]
 
        # Sort the imports by module origin
        # if pdt format is desired
        if pdt_format:
            # Identify python version
            # to list standard libraries
            # associated to the version
            major, minor, micro = sys.version_info[:3]
            py_version = f"{major}.{minor}"
            py_std_libs_list = stdlib_list(py_version) 
            
            top_level_deps_collected_list = [
                    "Python:" + lib 
                    if lib in py_std_libs_list
                    else lib
                    for lib
                    in top_level_deps_collected_list
            ]

        # Make the top level deps list unique and sorted
        top_level_deps_collected_list = list(
            set(
                top_level_deps_collected_list
            )
        )
        top_level_deps_collected_list.sort()

        return top_level_deps_collected_list

    def get_pip_required_deps_list(self):
        print(
            cl(
                f"""
                [DEBUG] Received request
                to share pip required deps list
                ----------
                """
            )
        )
        return self.pip_required_deps_list

    def get_site_pkg_names_list(self):
        print(
            cl(
                f"""
                [DEBUG] Received request
                to share site pkg names list
                ----------
                """
            )
        )
        return self.site_pkg_names_list

    def reset_deps_list(self):
        print(
            cl(
                f"""
                [DEBUG] Received request
                to reset deps list
                ----------
                """
            )
        )
        self.deps_collected_list = []

    def reset_pip_required_deps_list(self):
        print(
            cl(
                f"""
                [DEBUG] Received request
                to reset pip required deps list
                ----------
                """
            )
        )
        self.deps_collected_list = []

# Method defining custom argument type 
# for a list of strings
def list_of_strings(arg):
    return arg.split(',')

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
    parser.add_argument(
        "-d",
        "--exclude-dirs", 
        dest="exclude_dir_list",
        type=list_of_strings,
        action="store",
        help="List directory names (comma-separated) to exclude from the search",
    )
    parser.add_argument(
        "-f",
        "--exclude-files", 
        dest="exclude_file_list",
        type=list_of_strings,
        action="store",
        help="List file names (comma-separated) to exclude from the search",
    )
    
    # Collect arguments
    args = parser.parse_args()
    
    # Ensure one argument only is used  
    if not args.pkg_name and not args.pkg_path:
        parser.error("Please specify at least one argument between -n and -p")
    elif args.pkg_name and args.pkg_path:
        parser.error("Please only specify one argument -n or -p")
    else:
        pass
    
    return args

def main():
    # Parse arguments
    inputs=parse_args()
   
    # Convert None inputs where required
    if inputs.exclude_dir_list is None:
        inputs.exclude_dir_list = []
    if inputs.exclude_file_list is None:
        inputs.exclude_file_list = []

    # Instantiate python dependency collector
    py_dep_collector = PyDepCollector()

    # Start dependency collection
    if inputs.pkg_name:
        py_dep_collector.collect_deps_from_pkg_name(
            inputs.pkg_name,
            inputs.exclude_dir_list,
            inputs.exclude_file_list,
        )
    elif inputs.pkg_path:
        py_dep_collector.collect_deps_from_pkg_path(
            inputs.pkg_path,
            inputs.exclude_dir_list,
            inputs.exclude_file_list,
        )
    else:
        pass

    # Get dependency list
    # deps_list = py_dep_collector.get_deps_list()
    # deps_list = py_dep_collector.get_top_level_deps_list()
    deps_list = py_dep_collector.get_top_level_deps_list(pdt_format=True)
    
    # Get site packages name list
    site_pkg_names_list = py_dep_collector.get_site_pkg_names_list()
    
    # Get pip required dependency list
    pip_required_deps_list = py_dep_collector.get_pip_required_deps_list()
    
    # Print output in a clear way
    # for the user
    if inputs.pkg_name:
        print(
            cl(
                f"""
                ====================
                [INFO] Site packages names obtained:
                {site_pkg_names_list}
                ----------
                """
            )
        )

        print(
            cl(
                f"""
                [INFO] Pip required dependencies obtained:
                {pip_required_deps_list}
                ----------
                """
            )
        )
    else:
        print(cl(f"===================="))
    
    print(
        cl(
            f"""
            [INFO] Dependencies obtained:
            {deps_list}
            ====================
            """
        )
    )


if __name__ == "__main__":
    main()
