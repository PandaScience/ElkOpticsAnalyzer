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
import matplotlib.pyplot as plt


class Plot:
    """Plotter class taking care of plotting different types of fields.

    Attributes:
        every: Number of skipped data points in plots passed to
            matplotlib.pyplot.plot as 'markevery'.
        loc: Legend location passed to matplotlib.pyplot.legend.
        minw: Minimum frequency in eV to display in figures.
        maxw: Maximum frequency in eV to display in figures.
    """

    def __init__(self, minw=0, maxw=10):
        self.every = 5
        self._loc = "best"
        self.minw = minw
        self.maxw = maxw

    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, location):
        locs = [
            "best",
            "upper right",
            "upper left",
            "lower left",
            "lower right",
            "right",
            "center left",
            "center right",
            "lower center",
            "upper center",
            "center",
        ]
        if location not in locs:
            raise ValueError("[ERROR] Invalid legend location")
        else:
            self._loc = location

    def plotTensor(self, fig, freqs, ten, states, ylabel, style, vector=False):
        """Plots real and imaginary parts of tensor fields.

        Creates two subplots and fills them with data from a tensorial field
        A(w). Subplots are used according to the plot style, where the first
        one contains the real parts and the other one the imaginary parts of
        each tensor element. Not all elements are plotted according to
        'states'. Also adds a legend and axes labels to the plots.

        Args:
            fig: Matplotlib figure where the (sub)plots should be added.
            freqs: 1D array containing the freqencies for x-Axis.
            ten: 3x3 tensor field containing optical data.
            states: 9-element list indicating if a specific tensor element
                should be plotted or not.
            ylabel: Label with physical name for the tensor field.
            style: Character specifying horizontal split mode vs vertical.
            vector: Indicates if tensor field has only diagonal elements and
                should be regarded as a vector field.

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
        if vector:
            styles = ["-", "-.", "-."]
            markers = [" ", " ", " "]
            colors = ["r", "g", "b"]
            elements = [11, 22, 33]
            tenList = np.array([ten[0, 0, :], ten[1, 1, :], ten[2, 2, :]])
            states = [states[0], states[4], states[8]]
        else:
            styles = ["-", "-.", "-.", "-", ":", "-", ":", "-", "--"]
            markers = [" ", " ", " ", ",", "2", " ", " ", " ", " "]
            colors = ["r", "g", "b", "y", "c", "m", "sienna", "crimson", "k"]
            elements = [11, 12, 13, 21, 22, 23, 31, 32, 33]
            numfreqs = len(freqs)
            tenList = ten.reshape(9, numfreqs)

        for idxAx, ax in enumerate([ax1, ax2]):
            if ax is not None:
                for idx, elem in enumerate(elements):
                    # Qt.Checked == 2, Qt.Unchecked == 0; skip if unchecked
                    if states[idx] != 2:
                        continue
                    # find correct value parts for current axis
                    if idxAx == 0:
                        funValues = tenList[idx, :].real
                    else:
                        funValues = tenList[idx, :].imag
                    # prevent doublings when plotting "together"
                    if idxAx == 1 and style == "t":
                        label = None
                    else:
                        label = elem // 10 if vector else elem
                    # create the plot
                    ax.plot(
                        freqs[mask],
                        funValues[mask],
                        label=label,
                        markevery=self.every,
                        color=colors[idx],
                        ls=styles[idx],
                        marker=markers[idx],
                    )
                ax.set_ylabel(ylabel)
                ax.set_xlabel(r"$\omega$ [eV]")
                ax.legend(loc=self._loc)
                ax.axvline(x=0.0, lw=1, color="b", ls="--")
                ax.axhline(y=0.0, lw=1, color="b", ls="--")
                ax.set_xlim([self.minw, self.maxw])

        return ax1, ax2

    def plotVector(self, fig, freqs, ten, states, ylabel, style):
        """Shortcut for plotTensor(*args, vector=True)."""
        return self.plotTensor(
            fig, freqs, ten, states, ylabel, style, vector=True
        )

    def plotScalar(self, fig, freqs, fun, ylabel, style):
        """Plots real and imaginary parts of scalar fields.

        Creates two subplots and fills them with data from a scalar field f(w).
        Subplots are used according to the plot style, where the first one
        contains the real part and the other one the imaginary part. Also adds
        axes labels to the plots.

        Args:
            fig: Matplotlib figure where the (sub)plots should be added.
            freqs: 1D array containing the freqencies for x-Axis.
            fun: Scalar field containing optical data.
            ylabel: Label with physical name for the scalar field.
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
        parameter = data[0].notes[0]
        ylabel = data[0].label
        # create colors from scheme
        num = len(data)
        cmap = plt.cm.YlGn(np.linspace(0.7, 0.3, num))
        # real part
        if ax1 is not None:
            # use dummy plot for label heading
            ax1.plot([], [], " ", label=parameter)
            for colId, d in enumerate(data):
                label = d.notes[1]
                ax1.plot(d.freqs, d.field.real, c=cmap[colId], label=label)
        # imaginary part
        if ax2 is not None:
            if style != "t":
                ax2.plot([], [], " ", label=parameter)
            for colId, d in enumerate(data):
                # prevent doublings when plotting "together"
                label = None if (style == "t") else d.notes[1]
                ax2.plot(d.freqs, d.field.imag, c=cmap[colId], label=label)
        # stuff that need to be done only once for each axis
        for ax in [ax1, ax2]:
            if ax is not None:
                ax.set_ylabel(ylabel)
                ax.set_xlabel(r"$\omega$ [eV]")
                ax.legend(loc=self._loc)
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
