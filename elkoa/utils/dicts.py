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
    "320": ["epsL", "EELS"],
    "320/v5": ["epsTen", "epsInvTen"],
    "330": ["rchi"],
    "330/v5": ["rchi"],
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
    "121": ["EPSILON_XX.OUT", "SIGMA_XX.OUT"],
    "187": ["EPSILON_BSE.OUT"],
    "320": ["EPSILON_TDDFT.OUT", "EELS_TDDFT.OUT"],
    "320/v5": ["EPSILON_TDDFT_XX.OUT", "EPSINV_TDDFT_XX.OUT"],
    "330": ["CHI0_00.OUT"],
    "330/v5": ["CHI0_XX.OUT"],
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
    "EELS": r"EELS$(\omega)$ [a.u.]",
}

READER_DICT = {
    "121": [io.readTensor] * 2,
    "187": [io.readTensor] * 2,
    "320": [io.readScalar] * 2,
    "320/v5": [io.readTensor] * 2,
    "330": [io.readScalar],
    "330/v5": [io.readTensor],
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

# CONVERTER_DICT is class attribute of Converter class in file convert.py

# EOF - dicts.py
