from setuptools import setup

setup(
    name='externalpy',
    version='0.1',
    description='Demo package for inclusion of non-standard (external) python packages into PyQt5 apps',
    url='',
    author='Achille MARTIN',
    author_email='',
    license='MIT',
    packages=[
        'externalpy',
        'externalpy.resources',
    ],
    install_requires=[
        'PyQt5>=5.15.10',   
        'PyYAML>=6.0.1',
    ],
    package_data={
        'externalpy.resources': ["*.yaml"]
    },
    entry_points={
        'console_scripts': [
            'externalpycmd=externalpy.pyqt5_app_with_yaml:main',                 
        ],
    },
)
