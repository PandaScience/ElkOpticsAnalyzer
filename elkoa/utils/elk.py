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
import os

from elkoa.utils.misc import Hartree2eV


def readElkInputParameter(path, parameter):
    """Reads a specific input parameter from folder/elk.in."""
    inputFile = os.path.join(path, "elk.in")
    with open(inputFile, "r") as f:
        p = None
        for line in f:
            if line.startswith(parameter):
                p = next(f).split()
    return p


def parseElkInput(path=None, verbose=False):
    """Reads some relevant parameter settings from elk.in file."""
    # make sure to load correct file
    filename = "elk.in"
    if path is not None:
        filename = os.path.join(path, filename)
    # set default scale in case this option is not set in elk.in
    scale = 1.0
    with open(filename, "r") as f:
        for line in f:
            # get number of frequencies and min/max from section wplot
            if line == "wplot\n":
                numfreqs = int(next(f).split()[0])
                minw, maxw = [float(i) for i in next(f).split()[0:2]]
                # convert to eV
                minw, maxw = minw * Hartree2eV, maxw * Hartree2eV
            # get q-vector in fractional coordinates
            elif line == "vecql\n":
                vecqFrac = np.asarray([float(n) for n in next(f).split()])
                vecqlFrac = np.linalg.norm(vecqFrac)
            elif line == "scale\n":
                scale = float(next(f).split()[0])
    # convert fract. coord. to cartesian coords. for FCC (!) crystal,
    # where |b1|=|b2|=|b3| and |b|=sqrt(12)*pi/|a|=sqrt(3)*pi/scale
    qscale = np.pi / scale
    if "vecqFrac" in locals():
        vecq = vecqFrac * qscale
        # enable correct matrix dot product for q-vector
        vecq = np.atleast_2d(vecq).T
        vecql = np.linalg.norm(vecq)
        # result of matrix product is still a matrix, so take the only
        # element of this 1x1 2D matrix
        vecql2 = np.dot(vecq.T, vecq)[0, 0]
    else:
        vecq = None
        vecql2 = None
    # inform user
    if verbose:
        print("\n--- parsed data from elk.in ---\n")
        print("number of frequencies: {0}".format(numfreqs))
        print("q-vector in fract. coord.: ", vecqFrac)
        print("length of q-vector in frac. coord.: %.4f" % vecqlFrac)

        print("scaling factor for fcc-cell: %.4f" % scale)
        print("(should be equal to a/2 [bohr])")

        print("scaling factor for recip.-fcc-cell: %.4f" % qscale)
        print("(should be equal to 2pi/a [bohr])")

        print("norm of q-vector in cartesian coord. [1/Bohr]: %.4f" % vecql)
        print("squared norm of q-vector: %.4f" % vecql2)

    return numfreqs, minw, maxw, vecq, vecql2


def parseElkInfoOut(path=None, verbose=False):
    """Reads some relevant parameters which are only listed in INFO.OUT."""
    # make sure to load correct file
    filename = "INFO.OUT"
    if path is not None:
        filename = os.path.join(path, filename)
    # parse file
    with open(filename, "r") as f:
        for line in f:
            # get volume of unit cell in real space in Bohr^3
            if line.startswith("Unit cell volume"):
                cellVol = float(line.strip().split(":")[1])
            elif line.startswith("Brillouin zone volume"):
                cellVol = float(line.strip().split(":")[1])
            # get k-point grid and calculate number of k-points
            # (without symmetry reduction)
            elif line.startswith("k-point grid"):
                split = line.split()
                kgrid = np.array([split[3], split[4], split[5]], dtype=int)
                numkpts = np.prod(kgrid)
            elif line.startswith("Total electronic charge"):
                cellCharge = -1 * float(line.strip().split(":")[1])
    # inform user
    if verbose:
        print("\n--- parsed data from INFO.OUT ---\n")
        print("unit cell volume: {0} [Bohr^3]".format(cellVol))
        print("Brillouin zone volume: {0} [1/Bohr^3]".format(cellVol))
        print("k-grid: ", kgrid)
        print("total number of k-points: ", numkpts)
        print("total electronic charge per cell: ", cellCharge)

    return cellVol, cellCharge, numkpts


class ElkInput:
    """Gives access to Elk input parameters."""

    def __init__(self, path=None, verbose=False):
        # set path where files are located
        self.path = path
        # read all Elk input parameters
        self.numfreqs, self.minw, self.maxw, self.vecq, self.vecql2 = (
            parseElkInput(path=path, verbose=verbose)
        )
        self.cellVol, self.cellCharge, self.numkpts = (
            parseElkInfoOut(path=path, verbose=verbose)
        )

# EOF - elk.py
