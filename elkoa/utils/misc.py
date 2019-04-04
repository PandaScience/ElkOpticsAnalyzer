# coding: utf-8
# vim: set ai ts=4 sw=4 sts=0 noet pi ci

# Copyright © 2017-2019 René Wirnata.
# This file is part of Elk Optics Analyzer (ElkOA).
#
# Elk Optics Analyzer (ElkOA) is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Elk Optics Analyzer (ElkOA) is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Elk Optics Analyzer. If not, see <http://www.gnu.org/licenses/>.

import os
import numpy as np

"""Storage class containing some helpful dictionaries for Elk.

Attributes:
    TAB_NAME_DICT: Strings used for tabs in main windowi for each task.
    FILE_NAME_DICT: Basenames of Elk output files for each task.
    LABEL_DICT: Legend labels for each field.
    READER_DICT: Reader function for each type of Elk optics data file.
    PARAMETER_LIST: Some example Elk input parameters.
"""

# Hartree to electron Volt according to CODATA 2014, doi:10.5281/zenodo.22826
Hartree2eV = 27.21138602


def isTensor(field):
    """Checks if field is a tensor, i.e. shape = (3,3,N)."""
    if field.shape[:2] == (3, 3):
        return True
    else:
        return False


def checkStates(field):
    """Checks if certain tensor elements are completely NaN."""
    numfreqs = field.shape[2]
    nan = np.isnan(field).reshape(9, numfreqs)
    # Qt.PartiallyChecked == 1, Qt.Checked == 2
    states = [1 if nan[i].all() else 2 for i in range(9)]
    return states


def convertFileNameToLatex(s, unit=True):
    """Tries to convert Elk output filenames into latex code."""
    # remove extension, e.g. "SIGMA_33.OUT" --> ['SIGMA_33', '.OUT']
    s, ext = os.path.splitext(s)
    # if possible, extract tensor indices of FIELD_??_XX, X in (1,2,3),
    # e.g. "EPSILON_TDDFT_12".split("_") --> ['EPSILON', 'TDDFT', '12']
    sub = s.split("_")[-1]
    field = s.split("_")[0]
    if field.lower().startswith("eps"):
        # we need 3 {}: double {{}} for escaping, another {idx} for format
        latex = r"$\varepsilon_{{{sub}}}$".format(sub=sub)
    elif field == "SIGMA":
        latex = r"$\sigma_{{{sub}}}$".format(sub=sub)
    elif sub:
        latex = r"${{{name}}}_{{{sub}}}$".format(name=field, sub=sub)
    else:
        latex = s
    if unit:
        latex = latex + r"$(\omega)$ [a.u.]"
    return latex


def matrixPrint(mat):
    """Prints a 2-dimensional array in matrix form to screen.

    Args:
        mat: Array with shape (m, n) that is to be printed.
    """
    print("\n".join("\t".join(str(cell) for cell in row) for row in mat))
    print("\n")

# EOF - misc.py
