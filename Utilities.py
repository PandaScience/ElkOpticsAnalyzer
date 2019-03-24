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
# along with Foobar. If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as plt
import os

# global numpy pretty printing options
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

# Hartree to electron Volt according to CODATA 2014, doi:10.5281/zenodo.22826
Hartree2eV = 27.21138602


class Plot:
    """Plotter class taking care of plotting of scalar and tensor fields.

    Attributes:
        every: Number of skipped data points in plots passed to
            matplotlib.pyplot.plot as 'markevery'.
        loc: Legend location passed to matplotlib.pyplot.legend.
        minw: Minimum frequency in eV to display in figures.
        maxw: Maximum frequency in eV to display in figures.
    """

    def __init__(self, minw, maxw):
        self.every = 5
        self.loc = "upper right"
        self.minw = minw
        self.maxw = maxw

    def plotTen(self, fig, freqs, ten, states, ylabel, style):
        """Plots real and imaginary parts of tensor fields.

        Creates two subplots and fills them with data from a tensorial field
        A(w). Subplots are used according to the plot style, where the first
        one contains the real parts and the other one the imaginary parts of
        each tensor element. Not all elements are plotted according to
        'states'. Also adds a legend and axes labels to the plots.

        Args:
            fig: Matplotlib figure where the (sub)plots should be added.
            freqs: 1D array containing the freqencies for x-Axis.
            ten: 3x3 Tensor field containing optical data.
            states: 9-element list indicating if a specific tensor element
                should be plotted or not.
            ylabel: Label with physical name for the current tensor field.
            style: Character specifying horizontal split mode vs verical.

        Returns:
            A tuple of two subplots containing the real and imaginary parts of
            the tensor field. One of the subplots may be None depending on the
            current plot style.
        """
        # initialize subplots for real and imaginary parts
        ax1, ax2 = self.createSubPlots(fig, style)

        # restrict data according to plot range (for auto scaling to work)
        mask = (freqs >= self.minw) & (freqs <= self.maxw)

        # use different line styles and markers in case curves are overlapping
        styles = ["-", "-.", "-.", "-", ":", "-", ":", "-", "--"]
        markers = [" ", " ", " ", ",", "2", " ", " ", " ", " "]
        colors = ["r", "g", "b", "y", "c", "m", "sienna", "crimson", "k"]

        numfreqs = len(freqs)
        tenList = ten.reshape(9, numfreqs)

        for idxAx, ax in enumerate([ax1, ax2]):
            if ax is not None:
                matElements = [11, 12, 13, 21, 22, 23, 31, 32, 33]
                for idx, elem in enumerate(matElements):
                    # Qt.Checked == 2, Qt.Unchecked == 0
                    if states[idx] != 2:
                        continue
                    if idxAx == 0:
                        funValues = tenList[idx, :].real
                    else:
                        funValues = tenList[idx, :].imag
                    ax.plot(
                        freqs[mask],
                        funValues[mask],
                        label=elem,
                        markevery=self.every,
                        color=colors[idx],
                        ls=styles[idx],
                        marker=markers[idx],
                    )
                ax.set_ylabel(ylabel)
                ax.set_xlabel(r"$\omega$ [eV]")
                ax.legend(loc=self.loc)
                ax.axvline(x=0.0, lw=1, color="b", ls="--")
                ax.axhline(y=0.0, lw=1, color="b", ls="--")
                ax.set_xlim([self.minw, self.maxw])

        return ax1, ax2

    def plotScal(self, fig, freqs, fun, ylabel, style):
        """Plots real and imaginary parts of scalar fields.

        Creates two subplots and fills them with data from a scalar field f(w).
        Subplots are used according to the plot style, where the first one
        contains the real part and the other one the imaginary part. Also adds
        a legend and axes labels to the plots.

        Args:
            fig: Matplotlib figure where the (sub)plots should be added.
            freqs: 1D array containing the freqencies for x-Axis.
            fun: Scalar field containing optical data.
            ylabel: Label with physical name for the current tensor field.
            style: Character specifying horizontal split mode vs verical.

        Returns:
            A tuple of two subplots containing the real and imaginary parts of
            the scalar field. One of the subplots may be None depending on the
            current plot style.
        """
        # initialize subplots for real and imaginary parts
        ax1, ax2 = self.createSubPlots(fig, style)

        # restrict data according to plot range (for auto scaling to work)
        mask = (freqs >= self.minw) & (freqs <= self.maxw)

        # simplification for next for-loop: real -> axIdx 0, imag -> axIdx 1
        funValues = [fun.real[mask], fun.imag[mask]]

        # set labels, legend, additional lines etc.
        for idx, ax in enumerate([ax1, ax2]):
            if ax is not None:
                ax.plot(freqs[mask], funValues[idx], "rg"[idx])
                ax.set_ylabel(ylabel)
                ax.set_xlabel(r"$\omega$ [eV]")
                ax.legend(loc=self.loc)
                ax.axvline(x=0.0, lw=1, color="b", ls="--")
                ax.axhline(y=0.0, lw=1, color="b", ls="--")
                # restrict plot range
                ax.set_xlim([self.minw, self.maxw])

        return ax1, ax2

    def plotBatch(self, fig, data, style):
        """Plots the same field from different folders using colormaps."""
        # initialize subplots for real and imaginary parts
        ax1, ax2 = self.createSubPlots(fig, style)
        # some shortcuts
        ylabel = data[0].label
        parameter = data[0].task
        # use dummy plot for label heading
        plt.plot([], [], " ", label=parameter)
        # create colors from scheme
        num = len(data)
        cmap = plt.cm.YlGn(np.linspace(0.7, 0.3, num))
        for idx, ax in enumerate([ax1, ax2]):
            if ax is not None and idx == 0:
                for colId, d in enumerate(data):
                    ax.plot(
                        d.freqs,
                        d.field.real,
                        color=cmap[colId],
                        label=d.tabname,
                    )
            elif ax is not None and idx == 1:
                for colId, d in enumerate(data):
                    ax.plot(
                        d.freqs,
                        d.field.imag,
                        color=cmap[colId],
                        label=d.tabname,
                    )
            else:
                continue
            # stuff that need to be done only once for each axis
            ax.set_ylabel(ylabel)
            ax.set_xlabel(r"$\omega$ [eV]")
            ax.legend(loc=self.loc)
            ax.axvline(x=0.0, lw=1, color="b", ls="--")
            ax.axhline(y=0.0, lw=1, color="b", ls="--")
            ax.set_xlim([self.minw, self.maxw])
        return ax1, ax2

    def createSubPlots(self, fig, style):
        """Creates two subplots for a given figure.

        Adds two horizontal or vertical subplots to figure according to the
        passed plot style. Possible values are:
        'h' -> horizontal split view,
        'v' -> vertical split view,
        't' -> together, i.e. ax1 = ax2,
        'r' -> real part only, i.e. ax2 = None,
        'i' -> imaginary part only, i.e. ax1 = None.

        Args:
            fig: The figure where the two subplots should be added.
            style: Plot style indicating how the subplots should be arranged.

        Returns:
            The two created subplots.
        """
        # decide wether subplots should be split horizontal or vertical
        if style == "h":
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)
            # ax2 = fig.add_subplot( 212, sharex = ax1 )
        elif style == "v":
            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)
            # ax2 = fig.add_subplot( 122, sharey = ax1 )
        elif style == "t":
            ax1 = fig.add_subplot(111)
            ax2 = ax1
        elif style == "r":
            ax1 = fig.add_subplot(111)
            ax2 = None
        elif style == "i":
            ax2 = fig.add_subplot(111)
            ax1 = None
        else:
            print("[ERROR] cannot create subplots, unknown split type")
        return ax1, ax2


class Read:
    """Container class taking care of reading Elk and other raw output data."""

    def getTenElk(froot, numfreqs):
        """Wrapper function used to read tensor output files of Elk form."""
        return Read.readTensor(froot, numfreqs)

    def getTen635(froot, numfreqs):
        """Wrapper function used to read 3-column Elk tensor output files."""
        return Read.readTensor(froot, numfreqs, threeColumn=True, hartree=True)

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
                    _ten.append(np.empty((numfreqs, 3)) * np.nan)
                else:
                    _ten.append(np.empty((2 * numfreqs, 2)) * np.nan)
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

    def getScalarElk(filename, numfreqs):
        """Wrapper function used to read scalar fields from Elk output."""
        return Read.readScalar(filename, numfreqs)

    def getScalar635(filename, numfreqs):
        """Wrapper function used to read files from Elk task 635 files."""
        return Read.readScalar(filename, threeColumn=True)

    def getAdditionalData(filename):
        """Wrapper function used to read e.g. experimental optics data."""
        return Read.readScalar(filename, threeColumn=True, hartree=False)

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


class ElkInput:
    """Gives access to Elk input parameters."""

    def __init__(self, path=None):
        # set path where files are located
        self.path = path
        # read all Elk input parameters
        self.numfreqs, self.minw, self.maxw, self.vecq, self.vecql2 = (
            self.parseElkInput()
        )
        self.cellVol, self.cellCharge, self.numkpts = self.parseElkInfoOut()
        # decide if projectors should be constructed
        if self.vecql2 is None:
            print(
                "no q-vector set in input file, so no projection operators "
                "will be build..."
            )
            self.projLong = None
            self.projTrans = None
        else:
            self.projLong, self.projTrans = self.buildProjectionOperators()

    def parseElkInput(self):
        """Reads some relevant parameter settings from elk.in file."""
        # make sure to load correct file
        filename = "elk.in"
        if self.path is not None:
            filename = os.path.join(self.path, filename)
        # set default scale in case this option is not set in elk.in
        scale = 1.0
        if self.path is not None:
            filename = os.path.join(self.path, filename)
        with open(filename, "r") as f:
            for line in f:
                # get number of frequencies and min/max from section wplot
                if line == "wplot\n":
                    numfreqs = int(next(f).split()[0])
                    minw, maxw = [float(i) for i in next(f).split()[0:2]]
                # get q-vector in fractional coordinates
                elif line == "vecql\n":
                    vecqFrac = np.asarray([float(n) for n in next(f).split()])
                    vecqlFrac = np.linalg.norm(vecqFrac)
                elif line == "scale\n":
                    scale = float(next(f).split()[0])
        # print some information for the user to check correct input
        print("--- parsed data from elk.in ---\n")
        print("number of frequencies: {0}".format(numfreqs))
        print("q-vector in fract. coord.: ", vecqFrac)
        print("length of q-vector in frac. coord.: %.4f" % vecqlFrac)
        # convert fract. coord. to cartesian coords. for FCC (!) crystal,
        # where |b1|=|b2|=|b3| and |b|=sqrt(12)*pi/|a|=sqrt(3)*pi/scale
        print("scaling factor for fcc-cell: %.4f" % scale)
        print("(should be equal to a/2 [bohr])")
        qscale = np.pi / scale
        print("scaling factor for recip.-fcc-cell: %.4f" % qscale)
        print("(should be equal to 2pi/a [bohr])")
        if "vecqFrac" in locals():
            vecq = vecqFrac * qscale
            # enable correct matrix dot product for q-vector
            vecq = np.atleast_2d(vecq).T
            vecql = np.linalg.norm(vecq)
            # result of matrix product is still a matrix, so take the only
            # element of this 1x1 2D matrix
            vecql2 = np.dot(vecq.T, vecq)[0, 0]
            print(
                "norm of q-vector in cartesian coord. [1/Bohr]: %.4f" % vecql
            )
            print("squared norm of q-vector: %.4f" % vecql2)
        else:
            vecq = None
            vecql2 = None
        return numfreqs, minw * Hartree2eV, maxw * Hartree2eV, vecq, vecql2

    def parseElkInfoOut(self):
        """Reads some relevant parameters which are only listed in INFO.OUT."""
        print("\n--- parsed data from INFO.OUT ---\n")
        # make sure to load correct file
        filename = "INFO.OUT"
        if self.path is not None:
            filename = os.path.join(self.path, filename)
        # parse file
        with open(filename, "r") as f:
            for line in f:
                # get volume of unit cell in real space in Bohr^3
                if line.startswith("Unit cell volume"):
                    cellVol = float(line.strip().split(":")[1])
                    print("unit cell volume: {0} [Bohr^3]".format(cellVol))
                elif line.startswith("Brillouin zone volume"):
                    cellVol = float(line.strip().split(":")[1])
                    print(
                        "Brillouin zone volume: "
                        + "{0} [1/Bohr^3]".format(cellVol)
                    )
                # get k-point grid and calculate number of k-points
                # (without symmetry reduction)
                elif line.startswith("k-point grid"):
                    split = line.split()
                    kgrid = np.array([split[3], split[4], split[5]], dtype=int)
                    numkpts = np.prod(kgrid)
                    print("k-grid: ", kgrid)
                    print("total number of k-points: ", numkpts)
                elif line.startswith("Total electronic charge"):
                    cellCharge = -1 * float(line.strip().split(":")[1])
                    print("total electronic charge per cell: ", cellCharge)
        return cellVol, cellCharge, numkpts

    def buildProjectionOperators(self):
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
        if self.vecql2 < 1e-10:
            print(
                "[INFO] q-vector is zero, no projection operators defined...\n"
            )
            return None, None
        else:
            projLong = np.dot(self.vecq, self.vecq.T) / self.vecql2
            projTrans = np.identity(3) - projLong
            print("Longitudinal and transverse projection operators: \n")
            print("PL = ")
            self.matrixPrint(projLong)
            print("PT = ")
            self.matrixPrint(projTrans)
            print("\n")
            return projLong, projTrans

    def matrixPrint(self, mat):
        """Prints a 2-dimensional array in matrix form to screen.

        Args:
            mat: Array with shape (m, n) that is to be printed.
        """
        print("\n".join("\t".join(str(cell) for cell in row) for row in mat))
        print("\n")


class ElkDict:
    """Storage class containing some helpful dictionaries for Elk.

    Attributes:
        TAB_NAME_DICT: Strings used for tabs in main windowi for each task.
        FILE_NAME_DICT: Basenames of Elk output files for each task.
        LABEL_DICT: Legend labels for each field.
        READER_DICT: Reader function for each type of Elk optics data file.
        PARAMETER_LIST: Some example Elk input parameters.
    """

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
        "jchiTen": r"${}^j\chi^0(\omega)$",
        "sigTen": r"$\sigma(\omega)$",
        "epsTen": r"$\varepsilon(\omega)$",
        "epsInvTen": r"$\varepsilon^{-1}(\omega)$",
        "jchiL": r"${}^j\chi_{\mathrm{L}}(\omega)$",
        "sigL": r"$\sigma_{\mathrm{L}}(\omega)$",
        "epsL": r"$\varepsilon_{\mathrm{L}}(\omega)$",
        "rchi": r"${}^\rho\chi(\omega)$",
    }

    READER_DICT = {
        "121": [Read.getTenElk] * 2,
        "187": [Read.getTenElk] * 2,
        "320": [Read.getTenElk] * 2,
        "330": [Read.getScalarElk],
        "630": [Read.getTen635],
        "631": [Read.getScalarElk],
        "650": [Read.getTen635] * 3 + [Read.getScalar635] * 4,  # type: ignore
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


class misc:
    """Some helper functions"""

    def isTensor(field):
        """Checks if field is a tensor, i.e. shape = (3,3,N)."""
        if field.shape[:2] == (3, 3):
            return True
        else:
            return False

    def getStates(field):
        """Checks if certain tensor elements are completely NaN."""
        numfreqs = field.shape[2]
        nan = np.isnan(field).reshape(9, numfreqs)
        # Qt.PartiallyChecked == 1, Qt.Checked == 2
        states = [1 if nan[i].all() else 2 for i in range(9)]
        return states

    def readElkInputParameter(folder, parameter):
        """Reads a specific input parameter from folder/elk.in."""
        inputFile = os.path.join(folder, "elk.in")
        with open(inputFile, "r") as f:
            p = None
            for line in f:
                if line.startswith(parameter):
                    p = next(f).split()
        return p

    def convertFileNameToLatex(s):
        """Tries to convert Elk output filenames into latex code."""
        # remove extension, e.g. "SIGMA_33.OUT" --> ['SIGMA_33', '.OUT']
        s, ext = os.path.splitext(s)
        # if possible, extract tensor indices of FIELD_??_XX, X in (1,2,3),
        # e.g. "EPSILON_TDDFT_12".split("_") --> ['EPSILON', 'TDDFT', '12']
        idx = s.split("_")[-1]
        field = s.split("_")[0]
        if field == "EPSILON":
            # we need 3 {}: double {{}} for escaping, another {idx} for format
            latex = r"$\varepsilon_{{{idx}}}(\omega)$".format(idx=idx)
        elif field == "SIGMA":
            latex = r"$\sigma_{{{idx}}}(\omega)$".format(idx=idx)
        else:
            latex = s
        return latex


# EOF - Utilities.py
