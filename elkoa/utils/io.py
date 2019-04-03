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

from .misc import Hartree2eV


def readTensor(froot, numfreqs, threeColumn=False, hartree=True):
    """Reads complex tensor data from Elk output files.

    Tries to open all 9 files TEN_XY.OUT for a given tensor with basename
    TEN, where X and Y each run from 1 to 3, and stores the data into a
    multi-dimensional numpy array. If a file is not present, the field for
    this specific element is filled with NaN because of shape reasons. The
    number of frequencies in each file is compared to the setting in elk.in
    and if necessary adapted. In case not a single file for a specific
    tensor is available, the array is discarded and None is returned. If at
    least one file has been read successfully, real and imaginary parts are
    saved together as complex numbers and will be returned.

    Args:
        froot: File basename without _XY of Elk tensor output files.
        numfreqs: Number of frequencies according to elk.in.
        threeColumn: Indicates if file has frequencies, real and imaginary
            parts in 3 columns or stacked in 2 columns (Elk default).
        hartree: Indicates if frequencies from ile need to be converted
            from hartree to electron volts.

    Returns:
        Either Tuple[None, None] if tensor is not present in current path,
        or Tuple[freqs, tensor] if there was at least one data file.
        Frequencies are returned in units of eV, tensor data is a complex
        numpy array of shape (3, 3, num_freqs).
    """
    # tensor to read and store data in
    _ten = []
    # initialize to sth. invalid to use as check variable later
    numfreqsFile = None
    for i in [11, 12, 13, 21, 22, 23, 31, 32, 33]:
        fname = froot + "_" + str(i) + ".OUT"
        try:
            load = np.loadtxt(fname)
            _ten.append(load)
        except (FileNotFoundError, OSError):
            # append list of NaN instead of returning an error in case only
            # certain tensor elements have been calculated like 11, 22, 33
            # -> necessary for later reshaping!
            if threeColumn:
                _ten.append(np.full((numfreqs, 2), np.nan))
            else:
                _ten.append(np.full((2 * numfreqs, 2), np.nan))
        else:
            # take number of freqs from the first correctly read file
            if numfreqsFile is None:
                if threeColumn:
                    numfreqsFile = len(load[:, 0])
                else:
                    numfreqsFile = len(load[:, 0]) // 2
                # for safety, check against numfreqs from elk.in b/c Elk v5
                # task 320 deletes w=0 data point in each
                # EPSILON_TDDFT_XX.OUT file regardeless of 'kernel' in use
                # (previously happened only when using bootstrap kernel)
                if numfreqsFile != numfreqs:
                    print(
                        "[WARNING] number of frequencies from elk.in "
                        "(nwplot) differ \n"
                        "\t  from actual number of data points in {},\n"
                        "\t  changing from {} to {}.".format(
                            froot, numfreqs, numfreqsFile
                        )
                    )
                    numfreqs = numfreqsFile

    # indicate completely missing tensor with None
    if numfreqsFile is None:
        return None, None

    # when 11 element is n.a. and TDDFT data has one frequency less, there
    # are two dummy NaN too much in some missing elements - fix this.
    if not threeColumn:
        for idx, field in enumerate(_ten):
            if len(field) > 2 * numfreqs and np.isnan(field).all():
                _ten[idx] = field[:-2]

    # convert to 3x3 tensor field and separate real and imaginary parts
    freqs = load[0:numfreqs, 0]
    if threeColumn:
        ten = np.asarray(_ten).reshape(3, 3, numfreqs, 3)
        real = ten[:, :, :, 1]
        imag = ten[:, :, :, 2]
    else:
        ten = np.asarray(_ten).reshape(3, 3, 2 * numfreqs, 2)
        real = ten[:, :, :numfreqs, 1]
        imag = ten[:, :, numfreqs:, 1]

    # rebuild tensor structure using complex floats
    ten = np.zeros(real.shape, dtype=np.complex_)
    for iw in range(numfreqs):
        ten[:, :, iw] = real[:, :, iw] + imag[:, :, iw] * 1j

    if hartree:
        freqs *= Hartree2eV

    return freqs, ten


def readScalar(filename, numfreqs=None, threeColumn=False, hartree=True):
    """Reads complex data points of scalar fields from file.

    Loads data from 2 or 3 column files and stores complex values in a
    multi-dimensional numpy array.

    Args:
        filename: Filename or full path of file to load.
        numfreqs: Number of frequencies according to elk.in. Required only
            when loading from Elk output files.
        threeColumn: Indicates if file has frequencies, real and imaginary
            parts in 3 columns or stacked in 2 columns (Elk default).
        hartree: Indicates if frequencies from ile need to be converted
            from hartree to electron volts.

    Returns:
        Either Tuple[None, None] if file is not present in current path,
        or Tuple[freqs, tensor] otherwise. Frequencies are returned in
        units of eV, field data is a complex numpy array.
    """
    basename = os.path.basename(filename)
    try:
        load = np.loadtxt(filename, comments="#")
    except (FileNotFoundError, OSError):
        return None, None
    except ValueError:
        print(
            "[ERROR] Please check content of file {}. Non-data lines \n"
            "        comments must start with a '#'.".format(basename)
        )
        print(
            "        A proper data file looks like:\n"
            "        # This is a comment, e.g. a literature reference.\n"
            "        # frequency [eV]   real part      imaginary part \n"
            "        freq_1             real_1         imag_1    \n"
            "        freq_2             real_2         imag_2    \n"
            "        ...                ...            ...       \n"
            "        freq_N             real_N         imag_N    \n"
            "        --> Using 2nd column as real part \n"
        )
        return None, None

    if threeColumn:
        freqs = load[:, 0]
        real = load[:, 1]
        imag = load[:, 2]
    else:
        try:
            freqs = load[0:numfreqs, 0]
            real = load[:numfreqs, 1]
            imag = load[numfreqs:, 1]
        except IndexError:
            print(
                "[ERROR] When loading from Elk files, you must pass the "
                "number of frequencies as 'numfreqs'..."
            )

    field = real + imag * 1j

    if hartree:
        freqs *= Hartree2eV

    return freqs, field


def readTenElk(froot, numfreqs):
    """Wrapper function used to read tensor output files of Elk form."""
    return readTensor(froot, numfreqs)


def readTen635(froot, numfreqs):
    """Wrapper function used to read 3-column Elk tensor output files."""
    return readTensor(froot, numfreqs, threeColumn=True, hartree=True)


def readScalarElk(filename, numfreqs):
    """Wrapper function used to read scalar fields from Elk output."""
    return readScalar(filename, numfreqs)


def readScalar635(filename, numfreqs):
    """Wrapper function used to read files from Elk task 635 files."""
    return readScalar(filename, threeColumn=True)


def readAdditionalData(filename):
    """Wrapper function used to read e.g. experimental optics data."""
    return readScalar(filename, threeColumn=True, hartree=False)

# EOF - io.py
