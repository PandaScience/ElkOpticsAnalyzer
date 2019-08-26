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

import copy
import numpy as np
from numpy import linalg
import os

from elkoa.utils import dicts, misc


def readElkInputParameter(parameter, path=None):
    """Reads a specific input parameter from path/elk.in."""
    inputFile = "elk.in"
    if path is not None:
        inputFile = os.path.join(path, inputFile)
    with open(inputFile, "r") as f:
        p = None
        for line in f:
            if line.startswith(parameter):
                p = next(f).split()
    # catch non-existing p as NameError here b/c enumerate will throw TypeError
    if p is None:
        raise NameError(
            '[ERROR] No value for "{p}" found in {f}'.format(
                p=parameter, f=misc.shortenPath(inputFile)
            )
        )
    # do some rudimentary auto-conversion for the most obvious cases
    for idx, item in enumerate(p):
        if item == ".true.":
            p[idx] = True
        elif item == ".false.":
            p[idx] = False
        elif "." in item:
            p[idx] = float(item)
        elif item.isdecimal():
            p[idx] = int(item)
    # return item instead of list when list contains only one entry
    if len(p) == 1:
        return p[0]
    else:
        return p


def parseElkInput(path=None):
    """Reads absolutely required parameters from path/elk.in file."""
    # make sure to load correct file
    filename = "elk.in"
    if path is not None:
        filename = os.path.join(path, filename)
    # use this as template and remove all "--- Optics ---" and the like keys
    par = copy.deepcopy(dicts.PARAMETER_DICT)
    for k in list(par.keys()):
        if k.startswith("---"):
            par.pop(k)
    # replace default values with settings from elk.in
    with open(filename, "r") as f:
        for line in f:
            # number of frequencies and min/max from section wplot
            if line.startswith("wplot"):
                par["nwplot"] = int(next(f).split()[0])
                par["wplot"] = [float(i) for i in next(f).split()[0:2]]
            # q-vector in fractional coordinates
            elif line.startswith("vecql"):
                par["vecql"] = np.asarray([float(n) for n in next(f).split()])
            # scaling for all three crystal axes
            elif line.startswith("scale"):
                par["scale"] = float(next(f).split()[0])
            # smearing width for Dirac delta
            elif line.startswith("swidth"):
                par["swidth"] = float(next(f).split()[0])
            # real-space crystal axes
            elif line.startswith("avec"):
                par["a1"] = np.asarray([float(n) for n in next(f).split()])
                par["a2"] = np.asarray([float(n) for n in next(f).split()])
                par["a3"] = np.asarray([float(n) for n in next(f).split()])
            # Born-von Karman vectors (Brillouin zone sampling)
            elif line.startswith("ngridk"):
                par["ngridk"] = np.asarray([int(n) for n in next(f).split()])
    return par


class ElkInput:
    """Read-only storage class giving access to Elk input parameters.

    Attributes:
        path: location of elk.in where data is taken from
        nwplot: number of frequencies
        numfreqs: alias to nwplot
        wplot: (minw, maxw) in Hartree
        minw: minimum frequency in eV
        maxw: maximum frequency in eV
        scale: scaling factor for real-space unit cell
        swidth: smearing factor for Dirac delta
        avec: row-wise real space lattice vectors a1, a2 and a3 in Bohr
        bvec: row-wise dual space lattice vectors b1, b2 and b3 in 1/Bohr
        A: similar to avec but column-wise
        B: similar to bvec but column-wise
        vol_real: volume of real space unit cell
        vol_reci: volume of dual space = 1st Brillouin zone
        vecql: q-vector in fractional coordinates
        q_frac: alias to vecql
        q_cart: q-vector in cartesian coordinates
        qnorm: euclidean norm of q-vector
        qnorm2: squared euclidean norm of q-vector
        ngridk: k-point grid = sampling of 1st Brillouin zone
    """

    def __init__(self, path=None, verbose=False):
        # set path where input files are located
        self.path = path if path is not None else os.getcwd()
        # parse elk.in and convert returned dict into class attributes
        self.__dict__.update(parseElkInput(path=path))
        # lattice vectors as column-wise (!) matrices A and B
        self.avec = np.array([self.a1, self.a2, self.a3])
        self.A = self.avec.T * self.scale
        self.B = 2 * np.pi * linalg.inv(self.A.T)  # A.T*B = 2pi*1
        self.bvec = self.B.T
        # unit cell volume in real and reciprocal space
        self.vol_real = linalg.det(self.A)
        self.vol_reci = linalg.det(self.B)
        # q-vector in cartesian coordinates and magnitude in 1/[Bohr]
        self.q_frac = self.vecql
        self.q_cart = np.dot(self.B, self.q_frac)
        self.qabs = linalg.norm(self.q_cart)
        self.qabs2 = self.qabs ** 2
        # convert frequencies to eV, alias nwplot
        self.minw = self.wplot[0] * misc.hartreeInEv
        self.maxw = self.wplot[1] * misc.hartreeInEv
        self.numfreqs = self.nwplot

        if verbose:
            with np.printoptions(precision=4, suppress=True):
                self.printUserInformation()

    def printUserInformation(self):
        """Prints all important parameters from elk.in or default values."""
        print("\n--- parsed data from elk.in ---\n")
        print("number of frequencies: ", self.numfreqs)
        print("smearing width: ", self.swidth)
        print("q-vector in fract. coord.:   ", self.q_frac)
        print("q-vector in cartesian coord.:", self.q_cart)
        print("norm of q-vector [1/Bohr]: %.4f" % self.qabs)
        print("squared norm of q-vector: %.4f" % self.qabs2)
        print("")

        print("k-grid: ", self.ngridk, "-->", self.ngridk.prod(), "total")
        print("unit cell volume direct space [Bohr^3]: %.4f" % self.vol_real)
        print("unit cell volume reciprocal space: %.4f" % self.vol_reci)
        print("scaling factor taken into account: %.4f" % self.scale)
        print("")

        print("real space lattice vectors (column-wise cartesian): ")
        print(self.A)
        print("")

        print("dual space lattice vectors (column-wise cartesian): ")
        print(self.B)


# EOF - elk.py
