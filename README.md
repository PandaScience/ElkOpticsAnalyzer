## Elk Optics Analyzer
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License: GPL v3+](https://img.shields.io/badge/license-GPL%20v3%2B-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

### Description
This tool helps to analyze optics output data from 
[The Elk Code](http://elk.sourceforge.net).

Features:

* Visualize real and imaginary parts of Elk optics output data in various ways
* Select each tensor element to plot individually
* Import additional data files, e.g. experimental measurements
* Supports Elk tasks 121, 187, 320 and 330 

Soon to come:

* Batch opening and comparing parameter studies
* Advanced analysis of dieletric tensors
* Conversion of wavevector independent response functions into wavevector
  depentent ones
* Conversion of dielectric tensors in ordinary and extra-ordinary refractive
  indices
* Plotting of index ellipsoids

### Requirements
* [Python 3.x](https://www.python.org)
* [numpy](https://www.numpy.org/)
* [matplotlib](https://matplotlib.org)
* [PyQt5 (GPL version)](http://pyqt.sourceforge.net/Docs/PyQt5/installation.html)
* LaTeX suppoty for matplotlib, e.g. on Debian using texlive:
	* texlive
	* texlive-latex-extra
	* dvipng

### Usage Example
![](screenshots/basic.gif)
