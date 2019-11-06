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
import wrapt

from elkoa.utils import misc

# let numpy raise proper errors instead of just printing text to terminal
np.seterr(all="raise")

# calculate other response functions via universal response relations according
# to Starke & Schober (please use most recent versions on arXiv):
# "Functional Approach to Electrodynamics of Media"
# DOI: arXiv:1401.6800
# "Ab initio materials physics and microscopic electrodynamics of media"
# DOI: arXiv:1606.00445
# "Microscopic Theory of the Refractive Index"
# DOI: arXiv:1510.03404

# -----------------------------------------------------------------------------
#                    decorators used for class converters
# -----------------------------------------------------------------------------


def requires(lst):
    @wrapt.decorator
    def wrapper(converter, instance, args, kwargs):
        # convention: args[0] --> field
        field = args[0]
        if "nzq" in lst and (instance._q_frac == [0, 0, 0]).all():
            raise ValueError(
                "q-vector may not be (0,0,0) for this conversion!"
            )
        if "freqs" and instance._freqs is None:
            raise AttributeError(
                "required frequencies not set in converter class!"
            )
        if "nonan" in lst and np.isnan(field).any():
            raise ValueError(
                "not all tensor elements available or some contain NaN!"
            )
        if "basis" and instance._B is None:
            raise AttributeError(
                "transformation matrix B must be passed to converter first!"
            )
        return converter(field)

    return wrapper


# -----------------------------------------------------------------------------
#                              converter class
# -----------------------------------------------------------------------------


class Converter:
    """Converter class implementing response relations and more.

    Attributes:
        q: List or array holding a q-vector from 1st Brillouin zone in
            fractional (=lattice) coordinates as set by vecql in elk.in
        q_frac: alias to q
        q_cart: q-vector in cartesian coordinates
        B: Column-wise matrix of reciprocal lattice vectors in terms of
            cartesian standard basis (compare with e.g. LATTICE.OUT)
        qabs: Absolute value of q-vector
        qabs2: Squared absolute value of q-vector
        pL: Longitudinal projection operator
        pT: Transverse projection operator
        freqs: Frequencies in eV as returned by io.read functions
        rfreqs: Regularized frequencies in eV
        numfreqs: Number of frequencies in freqs
        eta: Regularization factor for frequencies w --> w + i*eta as used in
            elk.in, i.e. Hartree units
        reg: Indicates if "conv" = conventional or "imp" improved version of
            regularization should be used or "none". In latter case, freqs will
            be equal to rfreqs.
    """

    def __init__(self, q=[0, 0, 0], B=None, freqs=None, eta=0, reg="conv"):
        # keep this to prevent AttributeError cycle
        self._q_frac = np.array([0, 0, 0])
        self._freqs = None
        self._eta = 0
        self._reg = "conv"
        # keep this order of initializations --> will trigger update 3-4 times
        self._B = B  # don't let B.setter call q stuff again
        self.q = q
        self.eta = eta
        self.reg = reg
        self.freqs = freqs

    def _buildProjectionOperators(self):
        """Constructs transverse and longitudinal projectors.

        Projectors are defined (for arbitrary bases) by:
            P_L = q * q^T / |q|^2
            P_T = 1 - P_L
        For q == (0, 0, 0), these matrices are undefined.

        Returns:
            (P_L, P_T) in cartesian basis as 3x3 numpy arrays

        Raises:
            ZeroDivisionError or FloatingPointError for q = [0, 0, 0]
        """
        try:
            pL = np.dot(self._q_cart, self._q_cart.T) / self._qabs2
            pT = np.identity(3) - pL
            return pL, pT
        except (ZeroDivisionError, FloatingPointError) as e:
            raise ZeroDivisionError(
                "[ERROR] no projection operators defined for |q| = 0 !\n"
            ) from e

    def _buildEsg(self):
        """Constructs ESG and its inverse in cartesian basis for all freqs.

        The electric solution generator is defined by:
            E(q,w)      = P_L + pre   * P_T  ,  pre = w^2 / (w^2 - c^2 * q^2)
            E^{-1}(q,w) = P_L + 1/pre * P_T

        For pre -> 0, E is not invertible and we set E = P_L and E^{-1} = P_T.
        Zero limit cut-off is set to |pre| < 1e-10.

        In the optical limit q = [0, 0, 0], E becomes identity.

        Returns:
            (E, E^{-1}) in cartesian basis as 3x3 numpy arrays or
            (None, None) if frequencies are not available yet
        """
        # must use _freqs here b/c _rfreqs might not be defined yet
        if self._freqs is not None:
            esg = np.empty((3, 3, self._numfreqs), dtype=np.complex_)
            esgInv = np.empty((3, 3, self._numfreqs), dtype=np.complex_)
            # optical limit ESG --> 1
            if (self._q_frac == [0, 0, 0]).all():
                for idx in range(self._numfreqs):
                    esg[:, :, idx] = esgInv[:, :, idx] = np.identity(3)
            elif self._pL is not None:
                w2 = self._rfreqs ** 2
                c2 = misc.sol_au ** 2
                q2 = self.qabs2
                pre = w2 / (w2 - c2 * q2)
                for idx, p in enumerate(pre):
                    if abs(p) < 1e-10:
                        print(
                            "[INFO] for very small w at idx {} we set ESG "
                            "--> pL, ESGinv -> pT".format(idx)
                        )
                        esg[:, :, idx] = self._pL
                        esgInv[:, :, idx] = self._pT
                    else:
                        esg[:, :, idx] = self._pL + p * self._pT
                        esgInv[:, :, idx] = self._pL + 1 / p * self._pT
        else:
            esg = esgInv = None
        return esg, esgInv

    # -------------------------------------------------------------------------
    #                               attributes
    # -------------------------------------------------------------------------

    @property
    def q(self):
        return self._q_frac.flatten()

    @q.setter
    def q(self, q):
        # convert list or 1D array to (3x1) matrix --> column vector
        if type(q) == list or q.shape != (3, 1):
            q = np.atleast_2d(q).reshape((3, 1))
        self._q_frac = np.atleast_2d(q).reshape((3, 1))
        if (np.array(q) == [0, 0, 0]).all():
            self._q_cart = np.array([0, 0, 0])
            self._qabs = self._qabs2 = 0
            self._pL = self._pT = None
        elif q is not None:
            try:
                self._q_cart = np.dot(self._B, self._q_frac)
            except AttributeError as e:
                raise AttributeError(
                    "[ERROR] you must set matrix B for non-zero q!"
                ) from e
            self._qabs = np.linalg.norm(self._q_cart)
            self._qabs2 = self._qabs ** 2
            self._pL, self._pT = self._buildProjectionOperators()
        else:
            self._q_cart = None
            self._qabs = self._qabs2 = self._pL = self._pT = None
        self._esg, self._esgInv = self._buildEsg()

    @q.deleter
    def q(self):
        del self._q_frac
        del self._q_cart
        del self._qabs
        del self._qabs2
        del self._pL
        del self._pT
        del self._esg
        del self._esgInv

    @property
    def q_frac(self):
        return self.q

    @property
    def q_cart(self):
        return self._q_cart.flatten()

    @property
    def B(self):
        return self._B

    @B.setter
    def B(self, B):
        self._B = B
        # trigger construction of all q-vector associated attributes
        self.q = self.q

    @B.deleter
    def B(self):
        del self._B

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
    def freqs(self):
        if self._freqs is not None:
            return self._freqs * misc.hartreeInEv
        else:
            return None

    @freqs.setter
    def freqs(self, freqs):
        if freqs is not None:
            self._freqs = freqs / misc.hartreeInEv
            self._numfreqs = len(self._freqs)
            if self._reg == "conv":
                # conventional regularization
                self._rfreqs = self._freqs + self._eta * 1j
            elif self._reg == "imp":
                # improved regularization: Sangalli et al. PRB 95 155203 (2017)
                self._rfreqs = np.sqrt(
                    self._freqs ** 2 + 2 * self._eta * self._freqs * 1j
                )
            elif self._reg == "none":
                # do not regularize frequencies
                self._rfreqs = self._freqs
            self._esg, self._esgInv = self._buildEsg()
        else:
            self._freqs = self._rfreqs = self._numfreqs = None
            # keep manual for esg at w=0 not to warn multiple times
            self._esg = self._esgInv = None

    @freqs.deleter
    def freqs(self):
        del self._freqs
        del self._rfreqs
        del self._numfreqs
        del self._esg
        del self._esgInv

    @property
    def rfreqs(self):
        return self._rfreqs * misc.hartreeInEv

    @property
    def numfreqs(self):
        return self._numfreqs

    @property
    def eta(self):
        return self._eta

    @eta.setter
    def eta(self, eta):
        self._eta = eta
        # trigger construction of all frequency associated attributes, because
        # of unit conversion reasons, DO NOT use self._freqs here!
        self.freqs = self.freqs

    @property
    def reg(self):
        return self._reg

    @reg.setter
    def reg(self, reg):
        if reg == "imp" or reg == "conv":
            self._reg = reg
            # trigger construction of all frequency associated attributes
            self.freqs = self.freqs
        else:
            raise ValueError("Regularization must be 'conv' or 'imp'.")

    # -------------------------------------------------------------------------
    #                   utility functions and converters
    # -------------------------------------------------------------------------

    def getConverter(self, name):
        """Translates string to converter function and returns fun. pointer."""
        return getattr(self, name)

    @requires(["basis"])
    def cartToFrac(self, ten):
        tenFrac = np.empty_like(ten)
        B, Binv = self._B, np.linalg.inv(self._B)
        for idx in range(self._numfreqs):
            tenFrac[:, :, idx] = np.dot(Binv, np.dot(ten[:, :, idx], B))
        return tenFrac

    @requires(["basis"])
    def fracToCart(self, ten):
        tenCart = np.empty_like(ten)
        B, Binv = self._B, np.linalg.inv(self._B)
        for idx in range(self._numfreqs):
            tenCart[:, :, idx] = np.dot(B, np.dot(ten[:, :, idx], Binv))
        return tenCart

    @requires(["basis"])
    def fracToCartAlt(self, ten):
        # create metric tensor g_ij = b_i * b_j
        g = np.empty((3, 3))
        for i in range(3):
            for j in range(3):
                bi = np.atleast_2d(self._B[:, i]).T
                bj = np.atleast_2d(self._B[:, j]).T
                g[i, j] = np.dot(bi.T, bj)

        # e = B e' (g')^-1 B.T g; here: g = 1, g' = metric from above
        tenCart = np.zeros_like(ten)
        tmp = np.linalg.inv(g).dot(self._B.T)
        for idx in range(self._numfreqs):
            tenCart[:, :, idx] = self._B.dot(ten[:, :, idx].dot(tmp))
        return tenCart

    @requires(["nonan", "nzq"])
    def long(self, ten):
        """Extracts longitudinal part of response tensors. """
        long = np.empty(self._numfreqs, dtype=np.complex_)
        for idx in range(self._numfreqs):
            tmp = np.dot(ten[:, :, idx], self._q_cart)
            long[idx] = np.dot(self._q_cart.T, tmp) / self._qabs2
        return long

    @requires(["nonan", "freqs"])
    def eps_to_sig(self, eps):
        """Converts from (effective) epsilon to (proper) sigma."""
        sig = np.empty_like(eps)
        for idx, w in enumerate(self._rfreqs):
            pre = 1j * w / (4 * np.pi)
            sig[:, :, idx] = pre * (np.identity(3) - eps[:, :, idx])
        return sig

    @requires(["nonan", "freqs"])
    def eps_to_epsMicro(self, eps):
        """Converts effective dielectric tensor to microscopic one."""
        epsM = np.empty_like(eps)
        for idx, w in enumerate(self._rfreqs):
            epsM[:, :, idx] = np.identity(3) - self._esg[:, :, idx]
            epsM[:, :, idx] += np.dot(self._esg[:, :, idx], eps[:, :, idx])
        return epsM

    @requires(["nonan", "nzq"])
    def eps_to_refInd(self, eps):
        """Converts any dielectric tensor to (extra-)ordinary refr. indices.

        Detailed information about algorithm and difference between
        epsilon(q,w) vs. epsilon_eff(q,w) can be found in arXiv:1708.06330 .
        """
        from numpy.linalg import eig, norm, inv
        from numpy import sqrt

        # create random vector
        ov1 = np.random.randn(3)
        # make it orthogonal by subtracting longitudinal part
        ov1 -= np.dot(self.pL, ov1)
        # find second orthogonal vector
        ov2 = np.cross(self.q, ov1)
        # normalize both
        ov1 /= norm(ov1)
        ov2 /= norm(ov2)
        # find refractive indices
        n1 = np.zeros(self._numfreqs, dtype=np.complex_)
        n2 = np.zeros(self._numfreqs, dtype=np.complex_)
        for iw in range(self._numfreqs):
            # extract data for specific frequency
            E = eps[:, :, iw]  # noqa
            # invert tensor
            E = inv(E)  # noqa
            # prepare and build matrix in transverse subspace
            L = np.zeros((2, 2), dtype=np.complex_)  # noqa
            for idv1, v1 in enumerate([ov1, ov2]):
                for idv2, v2 in enumerate([ov1, ov2]):
                    L[idv1, idv2] = np.dot(v1.T, E.dot(v2))
            # find eigenvalues (n^2)_1/2 and corresponding eigenvectors
            # eXr = Re(n_1/2), eXi = Im(n_1/2), eXn = |n_1/2|
            ew, ev = eig(inv(L))
            e1r = ew[0].real
            e1n = norm(ew[0])
            e2r = ew[1].real
            e2n = norm(ew[1])
            # convert n^2 (= eigenvalues) to refractive indices n1 and n2
            n1[iw] = sqrt(0.5 * (e1n + e1r)) + sqrt(0.5 * (e1n - e1r)) * 1j
            n2[iw] = sqrt(0.5 * (e2n + e2r)) + sqrt(0.5 * (e2n - e2r)) * 1j
        # make sure that order of n1/n2 is identical for each run
        if n1[0] < n2[0]:
            tmp1, tmp2 = np.copy(n1), np.copy(n2)
            n1, n2 = tmp2, tmp1
        # combine to proper tensor data object and disable remaining
        # "tensor elements" for GUI
        refInd = np.empty_like(eps)
        for idx in [11, 12, 13, 21, 22, 23, 31, 32, 33]:
            i, j = [(int(n) - 1) for n in str(idx)]
            if idx == 11:
                refInd[i, j, :] = n1
            elif idx == 22:
                refInd[i, j, :] = n2
            else:
                refInd[i, j, :] = np.nan
        return refInd

    @requires(["nonan", "freqs"])
    def sig_to_eps(self, sigma):
        """Converts from (proper) sigma to (effective) epsilon tensor."""
        eps = np.empty_like(sigma)
        for idx, w in enumerate(self._rfreqs):
            pre = 4 * np.pi / (1j * w)
            eps[:, :, idx] = np.identity(3) - pre * sigma[:, :, idx]
        return eps


# EOF - convert.py
