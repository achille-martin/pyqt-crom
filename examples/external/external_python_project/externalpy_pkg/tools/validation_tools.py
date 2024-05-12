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

from os.path import join
import importlib.util

def validate_pkg_format(dotted_pkg_name, logger=None):
    """
    Get the python package name
    following the package naming convention
    that is most relevant
    for the application in use
  
    Parameters
    ----------
    dotted_pkg_name: str
        The package name to validate
        for subpackages, separate with dots
        example: 'pkg_1.subpkg_1'
  
    Returns
    -------
    str
        Same package name
        but with the relevant
        package naming convention
    """
    
    logger.debug(
        f"""
        validation_tools::validate_pkg_format -
        Received request to validate: {dotted_pkg_name}
        """
    ) if logger else None

    # Initialise pkg name to return
    supported_pkg_name = ''
    
    # Split the dotted pkg name at the dots
    split_pkg_name_list = dotted_pkg_name.split('.')
 
    # Create a joined pkg name readable by the OS
    joined_pkg_name = join(*split_pkg_name_list)
    
    logger.debug(
        f"""
        validation_tools::validate_pkg_format -
        Generated joined package name: {joined_pkg_name}
        """
    ) if logger else None
   
    # Evaluate which pkg name is suited for the application
    if importlib.util.find_spec(joined_pkg_name) is not None:
        supported_pkg_name = joined_pkg_name
        logger.debug(
            f"""
            validation_tools::validate_pkg_format -
            Found joined package name
            """
        ) if logger else None
    elif importlib.util.find_spec(dotted_pkg_name) is not None:
        supported_pkg_name = dotted_pkg_name
        logger.debug(
            f"""
            validation_tools::validate_pkg_format -
            Found dotted package name
            """
        ) if logger else None
    else:
        logger.warn(
            f"""
            validation_tools::validate_pkg_format -
            Cannot find package name
            """
        ) if logger else None
        pass
    
    logger.debug(
        f"""
        validation_tools::validate_pkg_format -
        Returning package name: {supported_pkg_name}
        """
    ) if logger else None
    
    return supported_pkg_name

