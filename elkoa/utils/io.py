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

import elkoa
from elkoa.utils.misc import hartree2ev


def checkTensorPresent(dummyName):
    """Tests if at least one tensor element present and reads numFreqs."""
    avail = False
    for i in [11, 12, 13, 21, 22, 23, 31, 32, 33]:
        fname = dummyName.replace("_ij.OUT", "_" + str(i) + ".OUT")
        avail = avail or os.path.isfile(fname)
        # in case we found a file, read-off numFreqs for later
        if avail:
            _tmp = np.loadtxt(fname)
            if _tmp.shape[1] == 3:
                threeColumn = True
                numFreqs = _tmp.shape[0]
            else:
                threeColumn = False
                numFreqs = _tmp.shape[0] // 2
            del _tmp
            break
    # indicate completely missing tensor with None
    if not avail:
        return None, None
    else:
        return numFreqs, threeColumn


def separateParts(array, num, threeColumn):
    """Converts array to 3x3 tensor separating real and imaginary parts."""
    if threeColumn:
        array = np.asarray(array).reshape(3, 3, num, 3)
        real = array[:, :, :, 1]
        imag = array[:, :, :, 2]
    else:
        array = np.asarray(array).reshape(3, 3, 2 * num, 2)
        real = array[:, :, :num, 1]
        imag = array[:, :, num:, 1]

    # rebuild tensor structure using complex floats
    ten = np.zeros(real.shape, dtype=np.complex_)
    for i in range(num):
        ten[:, :, i] = real[:, :, i] + imag[:, :, i] * 1j
    return ten


def readTensor(dummyName, numFreqsTest=None, hartree=True):
    """Reads complex tensor data from Elk output files.

    Tries to open all 9 files TEN_XY.OUT for a given tensor where X and Y each
    run from 1 to 3, and stores the data into a multi-dimensional numpy array.
    If a file is not present, the field for this specific element is filled
    with NaN because of shape reasons. The number of frequencies in each file
    is optionally compared to the setting in elk.in and if necessary adapted.
    In case not a single file for a specific tensor is available, the array is
    discarded and None is returned. If at least one file has been read
    successfully, real and imaginary parts are saved together as complex
    numbers and will be returned as tensor field.

    Args:
        dummyName: Filename with _ij.OUT ending as dummy for _11.OUT etc.
        numFreqs: Number of frequencies according to elk.in - only used for
            checking against, not strictly required for loading.
        hartree: Indicates if frequencies from file are given in Hartree units
            and need to be converted to electron volts.

    Returns:
        Either Tuple[None, None] if tensor is not present in current path,
        or Tuple[freqs, tensor] if there was at least one data file.
        Frequencies are returned in units of eV, tensor data is a complex
        numpy array of shape (3, 3, num_freqs).
    """
    numFreqs, threeColumn = checkTensorPresent(dummyName)
    if numFreqs is None:
        return None, None
    # if at least one element is present, read and store it, fill rest with NaN
    data = []
    for i in [11, 12, 13, 21, 22, 23, 31, 32, 33]:
        fname = dummyName.replace("_ij.OUT", "_" + str(i) + ".OUT")
        try:
            load = np.loadtxt(fname)
            data.append(load)
        except (FileNotFoundError, OSError):
            # append list of NaN instead of returning an error;
            # necessary for later reshaping!
            if threeColumn:
                data.append(np.full((numFreqs, 2), np.nan))
            else:
                data.append(np.full((2 * numFreqs, 2), np.nan))
        # process data if loading was successfull
        else:
            # for safety, check against numFreqs from elk.in b/c Elk v5
            # task 320 deletes w=0 data point in each
            # EPSILON_TDDFT_ij.OUT file regardeless of 'kernel' in use
            # (previously happened only when using bootstrap kernel)
            if numFreqsTest and numFreqs != numFreqsTest:
                print(
                    "[WARNING] number of frequencies from elk.in "
                    "(nwplot) differ \n"
                    "\t  from actual number of data points in {},\n"
                    "\t  changing from {} to {}.".format(
                        dummyName, numFreqsTest, numFreqs
                    )
                )
                # prevent spawning this error 9 times
                numFreqsTest = numFreqs
    ten = separateParts(data, numFreqs, threeColumn)
    if hartree:
        freqs = load[0:numFreqs, 0] * hartree2ev
    else:
        freqs = load[0:numFreqs, 0]
    return freqs, ten


def readScalar(filename, numFreqsTest=None, hartree=True):
    """Reads complex data points of scalar fields from file.

    Loads data from 2 or 3 column files and stores complex values in a
    multi-dimensional numpy array.

    Args:
        filename: Filename or full path of file to load.
        numFreqsTest: Number of frequencies according to elk.in. Used to check
            against when loading from Elk output files.
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

    try:
        # construct field depending on 2 or 3 column data file
        if load.shape[1] == 3:
            freqs = load[:, 0]
            real = load[:, 1]
            imag = load[:, 2]
        elif load.shape[1] == 2:
            numFreqs = load.shape[0] // 2
            # optionally check against passed entry from e.g. elk.in
            if numFreqsTest and numFreqs != numFreqsTest:
                print(
                    "[WARNING] number of frequencies from elk.in "
                    "(nwplot) differ \n"
                    "\t  from actual number of data points in {},\n"
                    "\t  changing from {} to {}.".format(
                        filename, numFreqsTest, numFreqs
                    )
                )
            freqs = load[0:numFreqs, 0]
            real = load[:numFreqs, 1]
            imag = load[numFreqs:, 1]
        else:
            print("[ERROR] invalid data file! - {}".format(filename))
            return None, None

        field = real + imag * 1j

        if hartree:
            freqs *= hartree2ev

        return freqs, field

    except (ValueError, IndexError):
        print(
            "[ERROR] Please check content of file {}. Non-data lines \n"
            "        comments must start with a '#'.".format(basename)
        )
        print(
            "        A proper data file has either Elk style or looks like:\n"
            "        # This is a comment, e.g. a literature reference.\n"
            "        # frequency [eV]   real part      imaginary part \n"
            "        freq_1             real_1         imag_1    \n"
            "        freq_2             real_2         imag_2    \n"
            "        ...                ...            ...       \n"
            "        freq_N             real_N         imag_N    \n"
            "        --> Using 2nd column as real part \n"
        )
        return None, None


def writeScalar(
    filename, freqs, field, threeColumn=False, hartree=True, prec=8
):
    """Generic write function for scalar fields.

    Args:
        filename: Filename of output file.
        freqs: Frequencies corresponding to field.
        field: Complex scalar field of the form ndarray(numfreqs).
        threeColumn: Indicates if output file should be in 3-column-style
            (frequencies, real part, imaginary part) or Elk style (real and
            imaginary part stacked in 2 columns).
        hartree: Indicates if frequencies should be converted from electron
            volts to hartree units.
        prec: Precision of output data.
    """
    version = elkoa.__version__
    header = "Generated using ElkOpticsAnalyzer v{}".format(version)
    dim = len(freqs)
    if threeColumn:
        fmt = "% 1.{p}E    % 1.{p}E    % 1.{p}E".format(p=prec)
        header += "\n{:{w1}}{:{w2}}{:{w2}}".format(
            "frequency",
            "real part",
            "imaginary part",
            w1=prec + 10,
            w2=prec + 11,
        )
        array = np.zeros((dim, 3))
        array[:, 0] = freqs * 1 / hartree2ev if hartree else freqs
        array[:, 1] = field.real
        array[:, 2] = field.imag
        np.savetxt(filename, array, header=header, fmt=fmt)
    else:
        fmt = "% 1.{p}E    % 1.{p}E".format(p=prec)
        header += "\n{:{w1}}{:{w2}}".format(
            "frequency", "field", w1=prec + 10, w2=prec + 11
        )
        array = np.zeros((dim, 2))
        array[:, 0] = freqs * 1 / hartree2ev if hartree else freqs
        fd = open(filename, "wb")
        # real part
        array[:, 1] = field.real
        np.savetxt(fd, array, header=header, fmt=fmt)
        # empty line in byte mode
        fd.write(b"\n")
        # imaginary part (stacked)
        array[:, 1] = field.imag
        np.savetxt(fd, array, fmt=fmt)
        fd.close()


def writeVector(
    dummyName,
    freqs,
    field,
    elements=[1, 2, 3],
    threeColumn=False,
    hartree=True,
    prec=8,
):
    """Generic write function for vector fields.

    Args:
        dummyName: Output filename, e.g. E-field_i.dat, where i is replaced by
            1, 2, 3.
        freqs: Frequencies corresponding to field.
        field: Complex vector field of the form ndarray(3,3,numfreqs) as used
            for tensor fields, but with only diagonal filled.
        elements: Array with indices of vector elements to be written to file.
            Numbers range from 1 to 3.
        threeColumn: Indicates if output file should be in 3-column-style
            (frequencies, real part, imaginary part) or Elk style (real and
            imaginary part stacked in 2 columns).
        hartree: Indicates if frequencies should be converted from electron
            volts to hartree units.
        prec: Precision of output data.
    """
    for i in elements:
        fname = dummyName.replace("_i", "_" + str(i))
        writeScalar(
            fname,
            freqs,
            field[i - 1, i - 1],
            threeColumn=threeColumn,
            hartree=hartree,
            prec=prec,
        )


def writeTensor(
    dummyName,
    freqs,
    field,
    elements=[11, 12, 13, 21, 22, 23, 31, 32, 33],
    threeColumn=False,
    hartree=True,
    prec=8,
):
    """Generic write function for tensor fields.

    Args:
        dummyName: Output filename, e.g. epsilon_ij_test.dat, where ij is
            replaced by 11, 12, etc.
        freqs: Frequencies corresponding to field.
        field: Complex tensor field of the form ndarray(3,3,numfreqs)
        elements: Array with indices of tensor elements to be written to file.
        threeColumn: Indicates if output file should be in 3-column-style
            (frequencies, real part, imaginary part) or Elk style (real and
            imaginary part stacked in 2 columns).
        hartree: Indicates if frequencies should be converted from electron
            volts to hartree units.
        prec: Precision of output data.
    """
    for idx in elements:
        i, j = [int(n) for n in str(idx)]
        fname = dummyName.replace("_ij", "_" + str(i) + str(j))
        writeScalar(
            fname,
            freqs,
            field[i - 1, j - 1],
            threeColumn=threeColumn,
            hartree=hartree,
            prec=prec,
        )


# EOF - io.py
