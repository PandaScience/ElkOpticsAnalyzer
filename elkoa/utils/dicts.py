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

FILE_NAME_DICT = {
    "121": ["EPSILON_ij.OUT", "SIGMA_ij.OUT"],
    "187": ["EPSILON_BSE_ij.OUT"],
    "320/v4": ["EPSILON_TDDFT.OUT", "EELS_TDDFT.OUT"],
    "320/v5": ["EPSILON_TDDFT_ij.OUT", "EPSINV_TDDFT_ij.OUT"],
    # 330 is 4x4 CHI/CHI0 matrix but currently not supported; we restrict to
    # density response (CHI_00.OUT) and magnetization response (CHI_ij.OUT)
    "330": [
        "CHI0_00.OUT",
        "CHI_00.OUT",
        "CHI0_T.OUT",
        "CHI_T.OUT",
        "CHI0_ij.OUT",
        "CHI_ij.OUT",
    ],
}

ADDITIONAL_DATA = {  # type: ignore
    "121": [[], []],
    "187": [[]],
    "320/v4": [[], []],
    "320/v5": [[], []],
    "330": [[], [], [], [], [], []],
}

READER_DICT = {
    "121": [io.readTensor] * 2,
    "187": [io.readTensor],
    "320/v4": [io.readScalar] * 2,
    "320/v5": [io.readTensor] * 2,
    "330": [io.readScalar] * 4 + [io.readTensor] * 2,
}

TAB_NAME_DICT = {
    "121": ["epsTen", "sigTen"],
    "187": ["epsTen"],
    "320/v4": ["epsL", "EELS"],
    "320/v5": ["epsTen", "epsInvTen"],
    "330": ["ϱ-chi0", "ϱ-chi", "m-chi0T", "m-chiT", "m-chi0", "m-chi"],
}

LABEL_DICT = {
    "sigTen": r"$\sigma_{ij}(\omega)$ [a.u.]",
    "epsTen": r"$\varepsilon_{ij}(\omega)$ [a.u.]",
    "epsInvTen": r"$\varepsilon^{-1}_{ij}(\omega)$ [a.u.]",
    "sigL": r"$\sigma_\mathrm{L}(\omega)$ [a.u.]",
    "epsL": r"$\varepsilon_\mathrm{L}(\omega)$ [a.u.]",
    "EELS": r"EELS$(\omega)$ [a.u.]",
    "ϱ-chi0": r"$\chi_\rho^0(\omega)$ [a.u.]",
    "ϱ-chi": r"$\chi_\rho(\omega)$ [a.u.]",
    "m-chi0T": r"$\chi_\mathrm{L}^0(\omega)$ [a.u.]",
    "m-chiT": r"$\chi_\mathrm{L}(\omega)$ [a.u.]",
    "m-chi0": r"$\chi_m^0(\omega)$ [a.u.]",
    "m-chi": r"$\chi_m(\omega)$ [a.u.]",
    "refInd": r"$n_{1/2}(\omega)$ [a.u.]",
    "epsMicro": r"$\varepsilon_{ij}(\omega)$ [a.u.]",
}

PARAMETER_LIST = [
    "--- Optics ---",
    "scissor",
    "swidth",
    "nwplot",
    "--- XC Functionals --",
    "xctype",
    "fxctype",
    "fxclrc",
    "--- Grids ---",
    "scale",
    "ngridk",
    "vecql",
    "vkloff",
]

# NOTE: these opts apply only to GUI, for CLI see decorators in convert.py
# options:
#   creg   - only conventional regularization w -> w+in possible
#   noreg  - disables regularization bullets completely
#   noq    - disables lineEdits for q-vector
#   nzq    - q-vector may not be (0, 0, 0)
#   vector - returns vector instead of tensor
CONVERSION_DICT = {
    "epsTen": {
        "name": "dielectric tensor",
        "converters": {
            "conductivity tensor": {
                "tabName": "sigTen",
                "functionName": "eps_to_sig",
                "opts": ["noq"],
            },
            "microscopic dielectric tensor": {
                "tabName": "epsMicro",
                "functionName": "eps_to_epsMicro",
                "opts": [],
            },
            "refractive indices": {
                "tabName": "refInd",
                "functionName": "eps_to_refInd",
                "opts": ["noreg", "nzq", "vector"],
            },
        },
    },
    "sigTen": {
        "name": "conductivity tensor",
        "converters": {
            "dielectric tensor": {
                "tabName": "epsTen",
                "functionName": "sig_to_eps",
                "opts": ["creg", "noq"],
            }
        },
    },
}

# add some generic converters valid for entire types of fields (e.g. tensors)
for field in CONVERSION_DICT.keys():
    if "Ten" in field:
        basename = field.split("Ten")[0]
        convDict = CONVERSION_DICT[field]["converters"]
        convDict.update(
            {
                "longitudinal part": {
                    "tabName": basename + "L",
                    "functionName": "long",
                    "opts": ["noreg", "nzq"],
                },
                "cartesian to fractional basis": {
                    "tabName": basename + "Ten",
                    "functionName": "cartToFrac",
                    "opts": ["noreg", "noq"],
                },
                "fractional to cartesian basis": {
                    "tabName": basename + "Ten",
                    "functionName": "fracToCart",
                    "opts": ["noreg", "noq"],
                },
            }
        )

# only for testing purpose
#                 "fractional to cartesian basis (alt)": {
#                     "tabName": basename + "Ten",
#                     "functionName": "fracToCartAlt",
#                     "opts": ["noreg", "noq"],
#                 },

# EOF - dicts.py
