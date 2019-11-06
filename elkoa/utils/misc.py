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
from numpy import linalg

# TODO maybe put in its own module 'units'?
# Hartree to electron Volt according to CODATA 2014, doi:10.5281/zenodo.22826
hartreeInEv = 27.21138602
# fine-structure constant according to CODATA 2014, doi:10.5281/zenodo.2282
alpha = 7.2973525664e-3
# speed of light in atomic units = 1/alpha
sol_au = 1 / alpha
# reduced Planck's constant in units of eV*s
hbar = 6.582119e-16
# Bohr to nano meter
bohrInNm = 0.0529177210563841


def hartree2ev(e):
    """Convert Energy in Hartree to electron Volts."""
    return e * hartreeInEv


def hartree2nm(e):
    """Convert Hartree to nanometers acc. to w=ck --> lambda = 2pi*c/w."""
    return 2 * np.pi * sol_au / e * bohrInNm


def qabs2nm(q):
    """Convert length in reciprocal space to wave length via lambda = 2pi/k."""
    return 2 * np.pi / q * bohrInNm


def nm2hartree(l):
    """Convert wave length [nm] to energy [Hartree] via lambda = 2pi*c/w."""
    return 2 * np.pi * sol_au / (l / bohrInNm)


def nm2qabs(l):
    """Convert length in reciprocal space to wave length via k = 2pi/lambda."""
    return 2 * np.pi / (l / bohrInNm)


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


def joinPath(path, filename):
    """Wrapper for os.join.path that can handle path=None."""
    if path is not None:
        return os.path.join(path, filename)
    else:
        return filename


def shortenPath(path, n=3, dots=True):
    """Truncates long paths/filenames and returns only last n segments."""
    path, short = os.path.split(path)
    # if file is in workdir, no need to shorten
    if path == "":
        return short
    # iterate only as long as necessary or (n-1) times
    count = 1
    while "/" in path and count < n - 1:
        path, tail = os.path.split(path)
        short = tail + "/" + short
        count += 1
    if dots:
        short = ".../" + short
    return short


def matrixPrint(mat, decimals=4):
    """Prints a 2-dimensional rounded array in matrix form to screen."""
    for idx, row in enumerate(mat):
        body = "  ".join("{: 8.{d}f}".format(cell, d=decimals) for cell in row)
        if idx == 0:
            print("⎡" + body + " ⎤")
        elif idx == len(mat[0]) - 1:
            print("⎣" + body + " ⎦")
        else:
            print("⎢" + body + " ⎥")


def compare(ten1, ten2):
    """Computes the max distance of two tensors using Frobenius and 2-norm."""
    assert ten1.shape == ten2.shape, "both tensors must have same dimensions"
    try:
        numfreqs = ten1.shape[2]
    except IndexError:
        raise TypeError("[ERROR] You must pass ndarrays with shape 3x3xN")
    # version 1: use Frobenius norm for each 3x3 matrix at frequency w, then
    # find the maximum w.r.t w
    frob = np.zeros(numfreqs)
    for idx in range(numfreqs):
        diff = ten1[:, :, idx] - ten2[:, :, idx]
        frob[idx] = linalg.norm(diff)
    print("Frobenius: ", max(frob))
    # version 2: use the 2-norm on every tensor element as a function of w and
    # find the max under these 9
    norm = []
    for i in range(3):
        for j in range(3):
            diff = ten1[i, j, :] - ten2[i, j, :]
            norm.append(linalg.norm(diff))
    print("2-norm:    ", max(norm))


# EOF - misc.py
