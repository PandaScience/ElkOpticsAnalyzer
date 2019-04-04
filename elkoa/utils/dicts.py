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

from elkoa.utils import io

TAB_NAME_DICT = {
    "121": ["epsTen", "sigTen"],
    "187": ["epsTen"],
    "320": ["epsTen", "epsInvTen"],
    "330": ["rchi"],
    "630": ["jchiTen"],
    "631": ["rchi"],
    "650": [
        "jchiTen",
        "sigTen",
        "epsTen",
        "jchiL",
        "sigL",
        "epsL",
        "rchi",
    ],
}

FILE_NAME_DICT = {
    "121": ["EPSILON", "SIGMA"],
    "187": ["EPSILON_BSE"],
    "320": ["EPSILON_TDDFT", "EPSINV_TDDFT"],
    "330": ["CHI0_00"],
    "630": ["JCHI0"],
    "631": ["RCHI0"],
    "650": [
        "JCHI0",
        "SIG",
        "EPS",
        "JCHI0_LONG",
        "SIG_LONG",
        "EPS_LONG",
        "RCHI0_LONG",
    ],
}

LABEL_DICT = {
    "jchiTen": r"$\chi_{ij}(\omega)$ [a.u.]",
    "sigTen": r"$\sigma_{ij}(\omega)$ [a.u.]",
    "epsTen": r"$\varepsilon_{ij}(\omega)$ [a.u.]",
    "epsInvTen": r"$\varepsilon^{-1}_{ij}(\omega)$ [a.u.]",
    "jchiL": r"$\chi_\mathrm{L}(\omega)$ [a.u.]",
    "sigL": r"$\sigma_\mathrm{L}(\omega)$ [a.u.]",
    "epsL": r"$\varepsilon_\mathrm{L}(\omega)$ [a.u.]",
    "rchi": r"$\chi_0(\omega)$ [a.u.]",
}

READER_DICT = {
    "121": [io.readTenElk] * 2,
    "187": [io.readTenElk] * 2,
    "320": [io.readTenElk] * 2,
    "330": [io.readScalarElk],
    "630": [io.readTen635],
    "631": [io.readScalarElk],
    "650": [io.readTen635] * 3 + [io.readScalar635] * 4,  # type: ignore
}

PARAMETER_LIST = [
    "--- Optics ---",
    "scissor",
    "swidth",
    "--- XC Functionals --",
    "xctype",
    "fxctype",
    "fxclrc",
    "--- Grids ---",
    "ngridk",
    "vecql",
    "vkloff",
]
