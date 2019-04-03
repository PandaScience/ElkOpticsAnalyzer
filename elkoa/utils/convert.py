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
from elkoa.utils import misc


def buildProjectionOperators(vecq, print=True):
    """Constructs transverse and longitudinal projectors.

    Projectors are built w.r.t. the q-vector set in elk.in:
        P_L = q * q^T / |q|^2
        P_T = 1 - P_L
    Obviously, if q == (0, 0, 0), these matrices are undefined.

    Returns:
        Either (None, None) if q=(0, 0, 0), (P_L, P_T) as 3x3 numpy arrays
        otherwise.
    """
    print("\n--- building projection operators  ---\n")

    vecql2 = np.linalg.norm(vecq) ** 2
    if vecql2 < 1e-10:
        print(
            "[INFO] q-vector is zero, no projection operators defined...\n"
        )
        return None, None
    else:
        projLong = np.dot(vecq, vecq.T) / vecql2
        projTrans = np.identity(3) - projLong
        if print:
            print("Longitudinal and transverse projection operators: \n")
            print("PL = ")
            misc.matrixPrint(projLong)
            print("PT = ")
            misc.matrixPrint(projTrans)
            print("\n")
        return projLong, projTrans

# EOF - convert.py
