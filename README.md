## Elk Optics Analyzer (ElkOA)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License: GPL v3+](https://img.shields.io/badge/license-GPL%20v3%2B-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

### Description
This tool helps to analyze optics output data from 
[The Elk Code](http://elk.sourceforge.net).

### Features

Elk Optics Analyzer...

* Supports Elk tasks 121, 187, 320 and 330 
* Recognizes available tasks / (tensor) fields automatically
* Is easily extendable

Users can...

* Visualize real and imaginary parts of Elk optics output data in various ways
* Import additional data files, e.g. experimental measurements `(CTRL+O)`
* Select tensor elements to plot individually via dialog `(CTRL+T)`
* Use global tensor elements settings for all plots `(CTRL+G)`
* Batch-load parameter studies to visually analyze the impact of different
  parameter settings `(CTRL+B)`

Soon to come:

* Conversion of wavevector independent response functions into wavevector
  dependent ones via [Universal Response Relations](https://arxiv.org/abs/1401.6800)
* Conversion of dielectric tensors in ordinary and extra-ordinary refractive
  indices for arbitrary k-vectors
* Plotting of index ellipsoids

### Requirements
* [Python 3.x](https://www.python.org)
* [numpy](https://www.numpy.org/)
* [matplotlib](https://matplotlib.org)
* [PyQt5 (GPL version)](http://pyqt.sourceforge.net/Docs/PyQt5/installation.html)
* LaTeX support for matplotlib

On Debian systems, you can get all required packages by running
```bash
apt install python3-numpy python3-matplotlib
apt install texlive texlive-latex-extra dvipng
```

### Usage Example
![](screenshots/basic.gif)
