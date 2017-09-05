from setuptools import setup, find_packages
import os

# ---------------------------------
# imports the version from the package
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'readme.rst')) as f:
    README = f.read()
exec(open(os.path.join(here, 'bootycontrol/version.py')).read())

# ---------------------------------
# project requirements
requirements = [
    'booty',
    'pyserial',
    'tk_tools >= 0.2.0'
]

# ---------------------------------
# project setup
setup(
    name='bootycontrol',
    version=__version__,
    description='GUI for booty',
    long_description=README,
    author='Jason R. Jones',
    author_email='slightlynybbled@gmail.com',
    url='https://github.com/slightlynybbled/bootycontrol',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={'console_scripts': ['bootycontrol = bootycontrol.__main__:main']},
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English'
    ],
    keywords='bootloader gui pic24 dspic'
)
