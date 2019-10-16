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

import numpy as np
from numpy import linalg
import os

from elkoa.utils import misc


def readElkInputParameter(parameter, path=None):
    """Reads a specific input parameter from path/elk.in."""
    inputFile = misc.joinPath(path, "elk.in")
    with open(inputFile, "r") as f:
        p = None
        for line in f:
            if line.startswith(parameter):
                p = []
                while True:
                    split = next(f).split()
                    # stop when parameter block ends
                    if split == []:
                        break
                    # remove comments from lines
                    elif ":" in split:
                        idx = split.index(":")
                        split = split[:idx]
                    p.extend(split)
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


def readElkLattice(path=None):
    """Reads real lattice vectors from path/LATTICE.OUT."""
    fname = misc.joinPath(path, "LATTICE.OUT")
    with open(fname, "r") as f:
        for line in f:
            if line.startswith("vector a1 :"):
                a1 = line.split()[3:]
            elif line.startswith("vector a2 :"):
                a2 = line.split()[3:]
            elif line.startswith("vector a3 :"):
                a3 = line.split()[3:]
    return np.array([a1, a2, a3]).astype(float)


class ElkInput:
    """Read-only storage class giving access to Elk input parameters.

    Attributes:
        path: location of elk.in where data is taken from
        nwplot: number of frequencies
        numfreqs: alias to nwplot
        wplot: (minw, maxw) in Hartree
        minw: minimum frequency in eV
        maxw: maximum frequency in eV
        swidth: smearing factor for Dirac delta
        avec: row-wise real space lattice vectors a1, a2 and a3 in Bohr
        bvec: row-wise dual space lattice vectors b1, b2 and b3 in 1/Bohr
        A: similar to avec but column-wise
        B: similar to bvec but column-wise
        avol: volume of real space unit cell
        bvol: volume of dual space = 1st Brillouin zone
        vecql: q-vector in fractional coordinates
        q_frac: alias to vecql
        q_cart: q-vector in cartesian coordinates
        qnorm: euclidean norm of q-vector
        qnorm2: squared euclidean norm of q-vector
    """

    def __init__(self, path=None, verbose=False):
        # set path where input files are located
        self.path = path if path is not None else os.getcwd()
        # parse elk.in and convert returned dict into class attributes
        self.__dict__.update(self.getRequiredParameters(verbose=verbose))
        # lattice vectors as column-wise (!) matrices A and B
        self.A = self.avec.T
        self.B = 2 * np.pi * linalg.inv(self.A.T)  # A.T*B = 2pi*1
        self.bvec = self.B.T
        # unit cell volume in real and reciprocal space
        self.avol = linalg.det(self.A)
        self.bvol = linalg.det(self.B)
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

    def getRequiredParameters(self, verbose=False):
        # we only need few parameters absolutely;
        # default values taken from ELK v6.3.2 readinput.f90
        p = {
            "swidth": 0.001,
            "wplot": [-0.5, 0.5],
            "nwplot": 500,
            "vecql": [0.0, 0.0, 0.0],
        }
        # update default values with settings from elk.in
        for key in ["swidth", "wplot", "vecql"]:
            try:
                if key == "wplot":
                    value = readElkInputParameter(key)
                    try:
                        p["nwplot"] = value[0]
                        p["ngrkf"] = value[1]
                        p["nswplot"] = value[2]
                        # NOTE: slicing out of bounds does not raise an error!
                        p["wplot"] = value[4]
                        p["wplot"] = value[3:5]
                    except IndexError as e:
                        raise IndexError(
                            "[ERROR] You must specify the entire wplot block "
                            "in your elk.in"
                        ) from e
                else:
                    p[key] = readElkInputParameter(key)
            except NameError:
                if verbose:
                    print("[INFO] Using default value for {}".format(key))
                continue
        # read avec from LATTICE.OUT instead of elk.in since it can be altered
        # during initialization by e.g. scale(1|2|3) or rotavec/axang
        p["avec"] = readElkLattice(self.path)
        # convert all lists to numpy arrays
        for key, value in p.items():
            if type(value) is list:
                p[key] = np.asarray(value)
        return p

    def printUserInformation(self):
        """Prints all important parameters to terminal."""
        print("\n--- PLEASE CHECK parsed input parameters ---\n")
        print("number of frequencies: ", self.numfreqs)
        print("frequency range [Hartree]: ", self.wplot)
        print("frequency range [eV]: ", self.wplot * misc.hartreeInEv)
        print("smearing width: ", self.swidth)
        print("q-vector in fract. coord.:   ", self.q_frac)
        print("q-vector in cartesian coord.:", self.q_cart)
        print("norm of q-vector [1/Bohr]: %.4f" % self.qabs)
        print("squared norm of q-vector: %.4f" % self.qabs2)
        print("")

        print("unit cell volume real space [Bohr^3]: %.4f" % self.avol)
        print("unit cell volume reciprocal space: %.4f" % self.bvol)
        print("")

        print("real space lattice vectors (column-wise): ")
        print(self.A)
        print("")

        print("reciprocal space lattice vectors (column-wise): ")
        print(self.B)


# EOF - elk.py
