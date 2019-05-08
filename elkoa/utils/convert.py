# coding: utf-8
# vim: set ai ts=4 sw=4 sts=0 noet pi ci

# Copyright © 2016-2019 René Wirnata.
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
from elkoa.utils import decorators, misc

# calculate other response functions via universal response relations according
# to Starke & Schober:
# "Functional Approach to Electrodynamics of Media"
# DOI: 10.1016/j.photonics.2015.02.001
# "Ab initio materials physics and microscopic electrodynamics of media"
# DOI: arXiv:1606.00445
# "Microscopic Theory of the Refractive Index"
# DOI: arXiv:1510.03404


def buildProjectionOperators(q, print=False):
    """Constructs transverse and longitudinal projectors.

    Projectors are built w.r.t. the q-vector set in elk.in:
        P_L = q * q^T / |q|^2
        P_T = 1 - P_L
    Obviously, if q == (0, 0, 0), these matrices are undefined.

    Returns:
        Either (None, None) if q=(0, 0, 0), (P_L, P_T) as 3x3 numpy arrays
        otherwise.
    """

    qabs2 = np.linalg.norm(q) ** 2
    if qabs2 < 1e-10:
        print("[INFO] q-vector is zero, no projection operators defined...\n")
        return None, None
    else:
        pL = np.dot(q, q.T) / qabs2
        pT = np.identity(3) - pL
        if print:
            print("Longitudinal and transverse projection operators: \n")
            print("PL = ")
            misc.matrixPrint(pL)
            print("PT = ")
            misc.matrixPrint(pT)
            print("\n")
        return pL, pT


class Converter:
    """Converter class implementing response relations and more.

    Attributes:
        q: List or array holding a vector q from 1st Brillouin zone in units of
            the reciprocal lattice vectors
        qabs: Absolute value of q-vector
        qabs2: Squared absolute value of q-vector
        pL: Longitudinal projection operator
        pT: Transverse projection operator
        freqs: Frequencies in eV as returned by io.read functions
        numfreqs: Number of frequencies
        eta: Regularization factor for frequencies w --> w + i*eta
        opticalLimit: Indicating if simpliciations in optical limes should be
            used instead of the full response relations using the ESG
    """

    def __init__(self, q, freqs, eta, opticalLimit=False):
        self._q = np.atleast_2d(q).T
        # store in Hartree units for convenient usage in conversion formulae
        self._freqs = freqs / misc.hartree2ev
        self._numfreqs = len(freqs)
        self._eta = eta
        self._opticalLimit = opticalLimit
        self._buildMembers()

    def _buildMembers(self):
        self._qabs2 = np.linalg.norm(self.q) ** 2
        self._qabs = np.sqrt(self._qabs2)
        # use improved regularization replacement according to
        # Sangalli et al., PRB 95 155203 (2017)
        # self._rfreqs = np.sqrt(self._freqs**2 + 2*self.eta*self._freqs*1j)
        self._rfreqs = self._freqs + self._eta * 1j
        self._esg = np.empty((3, 3, self._numfreqs), dtype=np.complex_)
        self._esgInv = np.empty((3, 3, self._numfreqs), dtype=np.complex_)

        if self.qabs2 < 1e-10:
            print(
                "[WARNING] q-vector is zero, no projection operators defined;"
                "\n          some conversions not available!"
            )
            self._pL = None
            self._pT = None
            for idx in range(self._numfreqs):
                self._esg[:, :, idx] = np.identity(3)
                self._esgInv[:, :, idx] = np.identity(3)
        elif self._opticalLimit:
            print(
                "[INFO] Optical limit assumed for current response tensor;\n"
                "       Electric Solution Generator set to identity."
            )
            self._pL, self._pT = buildProjectionOperators(self._q)
            for idx in range(self._numfreqs):
                self._esg[:, :, idx] = np.identity(3)
                self._esgInv[:, :, idx] = np.identity(3)
        else:
            # fmt:off
            self._pL, self._pT = buildProjectionOperators(self._q)
            fac = misc.sol_au**2 * self.qabs2 / self._rfreqs**2
            pre = 1 / (1 - fac)
            for idx, p in enumerate(pre):
                self._esg[:, :, idx] = self._pL + p * self.pT
                self._esgInv[:, :, idx] = self._pL + 1/p * self.pT
            # fmt:on

    @property
    def freqs(self):
        return self._freqs

    @freqs.setter
    def freqs(self, freqs):
        self._freqs = freqs / misc.hartree2ev
        self._buildMembers()

    @freqs.deleter
    def freqs(self):
        del self._freqs

    @property
    def numfreqs(self):
        return self._numfreqs

    @property
    def q(self):
        return self._q.flatten()

    @q.setter
    def q(self, q):
        self._q = np.atleast_2d(q).T
        self._buildMembers()

    @q.deleter
    def q(self):
        del self._q

    @property
    def qabs2(self):
        return self._qabs2

    @property
    def qabs(self):
        return self._qabs

    @property
    def pL(self):
        return self._pL

    @property
    def pT(self):
        return self._pT

    @property
    def eta(self):
        return self._eta

    @eta.setter
    def eta(self, eta):
        self._eta = eta
        self._buildMembers()

    @property
    def opticalLimit(self):
        return self._opticalLimit

    @opticalLimit.setter
    def opticalLimit(self, b):
        if type(b) == bool:
            self._opticalLimit = b
        else:
            raise TypeError("opticalLimit must be set to a boolean value!")

    def getConverter(self, name):
        """Translates string to converter function and returns fun. pointer."""
        return getattr(self, name)

    def longitudinalPart(self, ten):
        """Extracts longitudinal part of response tensors. """
        if self._pL is None:
            print("[ERROR] Converter not available b/c q-vector is zero.")
            return None
        return np.dot(self._pL, ten)

    def sigmaToEpsilon(self, sigma):
        eps = np.empty_like(sigma)
        for idx, w in enumerate(self._rfreqs):
            # fmt:off
            eps[:, :, idx] = np.identity(3) - 4 * np.pi / (1j*w) * \
                np.dot(self._esg[:, :, idx], sigma[:, :, idx])
            # fmt:on
        return eps

    @decorators.checkForNan
    def epsilonToSigma(self, eps):
        sig = np.empty_like(eps)
        for idx, w in enumerate(self._rfreqs):
            pre = 1j * w / (4 * np.pi)
            tmp = pre * (np.identity(3) - eps[:, :, idx])
            sig[:, :, idx] = np.dot(self._esgInv[:, :, idx], tmp)
        return sig


# EOF - convert.py
