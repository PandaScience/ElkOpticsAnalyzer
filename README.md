## Elk Optics Analyzer (ElkOA)
[![Python version](https://img.shields.io/pypi/pyversions/elkoa.svg)]()
[![PyPi version](https://img.shields.io/pypi/v/elkoa.svg)](pypi.org/project/elkoa/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![License: GPL v3+](https://img.shields.io/github/license/PandaScience/ElkOpticsAnalyzer.svg)](http://www.gnu.org/licenses/gpl-3.0)

### Description
Elk Optics Analyzer (ElkOA) helps to analyze optics output data from 
[The Elk Code](http://elk.sourceforge.net).

### Features

Elk Optics Analyzer...

* Comes with a GUI as well as a python CLI
* Supports Elk tasks 121, 187, 320 and 330 
* Recognizes available tasks / (tensor) fields automatically
* Is easily extendable

Users can...

* Visualize real and imaginary parts of Elk optics output data in various ways
* Import additional data files, e.g. experimental measurements
  <kbd>Ctrl+O</kbd>
* Convert response functions via 
  [Universal Response Relations](https://arxiv.org/abs/1401.6800), e.g. ε ➙ σ
  <kbd>Ctrl+C</kbd>
* Convert dielectric tensors into (extra-)ordinary refractive
  indices for arbitrary wavevectors <kbd>Ctrl+C</kbd>
* Select tensor elements to plot individually via dialog <kbd>Ctrl+T</kbd>
* Use global tensor elements settings for all plots <kbd>Ctrl+G</kdb>
* Batch-load parameter studies to visually analyze the impact of different
  parameter settings <kbd>Ctrl+B</kbd>
* Write out displayed data in different formats <kbd>Ctrl+W</kbd>

Soon to come:

* 3D-plotting of index ellipsoids
* Batch-convert for a set of different q-points
* Sample/geometry-dependent (i.e. thin films) conversions of response functions

### Requirements
* [Python 3.x](https://www.python.org)
* [numpy](https://www.numpy.org/)
* [matplotlib](https://matplotlib.org)
* [PyQt5](http://pyqt.sourceforge.net/Docs/PyQt5/installation.html)
* [pbr](https://docs.openstack.org/pbr/latest/)

You should use the packages provided by your linux distribution. On recent 
Debian systems for example, you can get all requirements by running
```bash
apt install python3-numpy python3-matplotlib python3-pyqt5 python3-pbr
```

Alternatively, you can get the latest PyPI versions of each package
automatically by installing via pip (see below).

For testing purposes, you additionally need the following packages:
* pytest
* pytest-qt
* pytest-mpl
* nose

### Installation

The easiest way to install ElkOA is via pip, either from PyPI directly
```bash
pip install elkoa
```
or, if you want the latest git version, 
```bash
git clone https://github.com/PandaScience/ElkOpticsAnalyzer.git
cd ElkOpticsAnalyzer
pip install .
```
This will also install all required but absent python packages automatically
from PyPI.

If you like to install ElkOA only for the current user, add the flag `--user`.
If you want to take care of the required python packages yourself (i.e. by
using the ones provided by your Linux distribution), add `--no-deps`.  If you
like to run a developer installation (no copying of files, instead use git repo
files directly), add `-e`.

In any case, after installation you can run the ElkOA GUI from everywhere in a
terminal using either `elkoa` or `ElkOpticsAnalyzer`.

Another way to install is by cloning the repo as above and instead of
installing via pip, put something like
```bash
export PATH=$PATH:/path/to/ElkOpticsAnalyzer/elkoa/gui
export PYTHONPATH=$PYTHONPATH:/path/to/ElkOpticsAnalyzer/
```
to your `.bashrc` or `.bash_profile`. Then you can start the ElkOA GUI with
`ElkOpticsAnalyzer.py`.


### Tests

Testing is done using the `pytest` library. Make sure you installed all
additional requirements beforehand.

1. Download and extract the sample data
	- TODO
2. Run (--mpl flag is mandatory!)
```python
	pytest test_figures.py --mpl
```


### Python CLI

In an Elk output directory containing e.g. the files
```bash
elk.in INFO.OUT EPSILON_11.OUT EPSILON_12.OUT EPSILON_13.OUT EPSILON_21.OUT
EPSILON_22.OUT EPSILON_23.OUT EPSILON_31.OUT EPSILON_32.OUT EPSILON_33.OUT
```
you can run in a python3 interpreter:
```python
from elkoa.utils import elk, io, convert
# parse Elk input file
elk_input = elk.ElkInput()
# read specific input parameter
eta = elk.readElkInputParameter("swidth")
# read tensorial Elk optics output (ij = dummy for 11, 12, etc.)
freqs, epsilon = io.readTenElk("EPSILON_TDDFT_ij.OUT")
# create converter instance
q = [0, 0, 0]
converter = convert.Converter(q, freqs, eta, opticalLimit=True)
# convert dielectric tensor to optical conductivity
sigma = converter.epsilonToSigma(epsilon)
# write out converted tensor
io.writeTensor("sigma_ij_test.dat", freqs, sigma, threeColumn=True)
# write out 11-element of converted tensor
io.writeScalar("sigma_11-scalar.dat", freqs, sigma[0, 0, :], threeColumn=True)
```


### Misc

* Auto-converting filenames to tex-labels
  * For this feature to work, filenames must follow the pattern
    `root`+`_sub`+`.ext`, which will show up as root<sub>sub</sub>.
  *  In case `root` contains a case-insensitive substring like eps,
    EPSILON, Sig, SIGma etc., corresponding greek letters will be used,
    i.e. eps_ex.dat ➙ ε<sub>ex</sub>.
* Additional data plots
    * Number is restricted to 6, but in return we use consistent coloring after
      consecutively adding more plots.


### Usage Examples GUI
![see https://github.com/PandaScience/ElkOpticsAnalyzer/](screenshots/basic.gif)
![and https://github.com/PandaScience/ElkOpticsAnalyzer/](screenshots/batchload.gif)
