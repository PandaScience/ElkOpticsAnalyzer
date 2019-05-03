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

import os
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

import elkoa
import elkoa.gui.UiInterface as UiInterface
import elkoa.gui.UiDialogs as UiDialogs
from elkoa.utils import convert, elk, dicts, misc, io, plot

import matplotlib as mpl
import numpy as np

# make sure we use QT5; needs to come before any other mpl imports
mpl.use("Qt5Agg")  # noqa

import matplotlib.pyplot as plt
from matplotlib.backends import backend_qt5agg


class TabData:
    """Stores content of Elk optical output files

    Attributes:
        freqs: Frequencies in eV.
        field: Tensor or scalar field with real and imaginary parts as ndarray.
        label: Labeltext for plot from labelDict.
        tabname: Name from tabNameDict.
        filename: Name of file where data has been loaded from.
        task: Elk task [str] where data belongs to.
        enabled: Bool indicating if tab should be "filled" at all.
        states: Array holding the currently enabled/disabled/n.a. elements.
    """

    def __init__(
        self,
        freqs=None,
        field=None,
        label=None,
        filename=None,
        tabname=None,
        task=None,
    ):
        self.freqs = freqs
        self.field = field
        self.label = label
        self.tabname = tabname
        self.filename = filename
        self.task = task
        self.enabled = None
        self.isTensor = None
        self.states = None
        self.updateAttributes()

    def updateAttributes(self):
        """Analyzes stored field data and sets some attributes accordingly"""
        # disable tab if field data is not present
        if self.field is None:
            self.enabled = False
            return
        # update tensor element states for tensor fields
        if misc.isTensor(self.field):
            self.enabled = True
            self.isTensor = True
            self.states = misc.checkStates(self.field)
            print("[INFO] Successfully read data for tensor", self.filename)
        else:
            self.enabled = True
            self.isTensor = False
            print("[INFO] Successfully read data for scalar", self.filename)


class MainWindow(
    QtWidgets.QMainWindow, UiInterface.Ui_ElkOpticsAnalyzerMainWindow
):
    """Main window class where the plots are located.

    The user can choose to display data from available tasks and how to plot
    them, i.e. real/imag part together, only one or in vertical/horizontal
    split screen. Combobox tasks with unavailable files in current working
    directory will be disabled.

    Attributes:
        Shortcuts for convenience:
            tabNameDict, fileNameDict, labelDict, readerDict
        splitMode: Character indicating horizontal or vertical split mode.
        dpi: Pixel density to use in figures.
        use_global_states: Bool, true if tensor element dialog should apply to
            all plots, false when apply only to current figure.
        additionalPlots: 'triggered' -> true after user loaded additional data
            manually, 'tabID' -> in which tab new plots should be added.
        additionalData: List with data from manually loaded files.
        data: Holds all optical data from Elk output files read during startup.
        figures: Holds all figure objects from all available tabs.
        tenElementsDialog: Dialog to choose tensor elements to plot.
        batchLoadDialog: Dialog to choose file, folder and parameter for
            batch-plotting parameter studies.
        globalStates: States to use when global states option is enabled.
        currentTask: String identifyer of currently selected task used for e.g.
            label dictionaries.
        elkInput: Class that holds all parameters read from elk.in and
            INFO.OUT in current working directory.
        plotter: Class instance taking care of global plot settings .
        ElkDict: Class of many dictionaries used to find the correct reader,
            plotter and axes labels for each Elk task.
    """

    # shortcuts
    tabNameDict = dicts.TAB_NAME_DICT
    fileNameDict = dicts.FILE_NAME_DICT
    readerDict = dicts.READER_DICT
    labelDict = dicts.LABEL_DICT

    # new signals
    windowUpated = QtCore.pyqtSignal()

    def __init__(self, cwd=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # attributes with default values
        self.splitMode = "v"
        self.dpi = 100
        # NOTE: keep in sync with MainWindow.ui
        self.use_global_states = False
        self.additionalPlots = {"triggered": False, "tabID": [0]}
        self.tenElementsDialog = UiDialogs.TensorElementsDialog()
        self.batchLoadDialog = UiDialogs.BatchLoadDialog()
        self.convertDialog = UiDialogs.ConvertDialog()
        self.globalStates = None
        self.currentTask = None

        # apply signal/slot settings
        self.connectSignals()
        # add version number permanently to far right end of status bar
        versionLabel = QtWidgets.QLabel("v{}".format(elkoa.__version__), self)
        self.statusbar.addPermanentWidget(versionLabel)
        self.setStyleSheet("QStatusBar::item {border: 2px;}")
        # print license information in terminal
        self.printAbout()
        # set global plot options
        self.setMplOptions()
        # read Elk input file and INFO.OUT
        self.changeWorkingDirectory(cwd)
        while self.elkInput is None:
            self.changeWorkingDirectory()

    def connectSignals(self):
        """Connects GUI buttons and menu options to functions of this class."""
        # combo box for tasks
        self.taskChooser.currentIndexChanged[str].connect(
            lambda: self.updateWindow(newtask=True)
        )
        # menu "Menu"
        self.actionSetWorkingDir.triggered.connect(
            lambda: self.changeWorkingDirectory(path=None)
        )
        self.actionReload.triggered.connect(self.reloadData)
        self.actionReadAdditionalData.triggered.connect(
            self.readAdditionalData
        )
        self.actionRemoveAllAdditionalData.triggered.connect(
            self.removeAllAdditionalData
        )
        self.actionBatchLoad.triggered.connect(self.batchLoad)
        self.actionQuit.triggered.connect(self.quitGui)
        # menu "Convert"
        self.actionResponseRelations.triggered.connect(self.convert)
        self.actionRefractiveIndex.triggered.connect(self.dummy)
        self.actionIndexEllipsoid.triggered.connect(self.dummy)
        # menu "View"
        self.actionVerticalSplit.triggered.connect(
            lambda: self.changeSplitMode("v")
        )
        self.actionHorizontalSplit.triggered.connect(
            lambda: self.changeSplitMode("h")
        )
        self.actionTensorElements.triggered.connect(
            self.tenElementsDialogWrapper
        )
        self.actionGlobalTensorSettings.triggered.connect(
            self.updateGlobalTensorSettings
        )
        # menu "Help"
        self.actionAbout.triggered.connect(self.showAbout)
        # bottom menu
        self.btnRealPart.clicked.connect(self.updateWindow)
        self.btnImaginaryPart.clicked.connect(self.updateWindow)
        self.btnSplitView.clicked.connect(self.updateWindow)
        self.btnTogether.clicked.connect(self.updateWindow)
        self.checkBoxfullRange.clicked.connect(self.setPlotRange)
        # other user interaction
        self.tabWidget.currentChanged.connect(self.onTabChanged)

    def readAllData(self):
        """Reads data from Elk input files and Elk optical output."""
        self.elkInput = self.parseElkFiles()
        if self.elkInput is None:
            raise FileNotFoundError("[ERROR] No Elk input files found in cwd!")
        print("\n--- reading optics data ---\n")
        for task in self.fileNameDict:
            # prepare array holding new TabData instances for each tab of task
            self.data[task] = []
            for tabIdx, tab in enumerate(self.tabNameDict[task]):
                reader = self.readerDict[task][tabIdx]
                filename = self.fileNameDict[task][tabIdx]
                tabname = self.tabNameDict[task][tabIdx]
                label = self.labelDict[tabname]
                freqs, field = reader(filename, self.elkInput.numfreqs)
                self.data[task].append(
                    TabData(freqs, field, label, filename, tabname, task)
                )
            # disable/mark combo box entry if no task data is present at all
            tabStates = [tab.enabled for tab in self.data[task]]
            if not any(tabStates):
                # find index of comboBox item that contains `task` as substring
                idx = self.taskChooser.findText(task, Qt.MatchContains)
                # remove unavailable tasks
                self.taskChooser.removeItem(idx)

    def reloadData(self):
        """Forces to read all Elk output data again from current path."""
        # if existing remove all batch items from comboBox / task list
        while True:
            idx = self.taskChooser.findText("batch", Qt.MatchContains)
            if idx == -1:
                break
            else:
                self.taskChooser.removeItem(idx)
        # clear old data
        # TODO test garbage collection and reference cycles
        self.additionalData = []
        self.data = {}
        self.figures = []
        # read in new data
        try:
            self.readAllData()
        except FileNotFoundError:
            return
        # setup plotters for different Elk output files / tasks
        self.plotter = plot.Plot(self.elkInput.minw, self.elkInput.maxw)
        # inform user
        self.statusbar.showMessage("Data loaded, ready to plot...", 0)
        print("\n/-------------------------------------------\\")
        print("|               start plotting              |")
        print("\\-------------------------------------------/\n")
        # only update window if this is not an initial load
        if self.currentTask is not None:
            self.updateWindow()

    def updateWindow(self, newtask=False):
        """Redraws figure for currently chosen Elk task."""
        currentText = self.taskChooser.currentText()
        # extract task number (integer) from combobox entry
        self.currentTask = currentText.split()[0]
        # make batch entries unique by using entire string
        if self.currentTask == "batch":
            self.currentTask = currentText
        # force user to choose valid task
        # TODO: replace with isEnabled == False check
        if currentText in ("", None, "Please choose an Elk task..."):
            QtWidgets.QMessageBox.warning(
                self, "No task chosen!", "Please choose a task..."
            )
            # TODO find cleaner solution
            self.additionalPlots["triggered"] = False
            return
        # save current tab ID for later
        oldTabIdx = self.getCurrent("tabIdx")
        # TODO need to remove child widgets manually??
        self.figures = []
        plt.close("all")
        self.tabWidget.clear()
        self.createTabs()
        # go back to same tab as before the update if still viewing same task
        if not newtask:
            self.tabWidget.setCurrentIndex(oldTabIdx)
        # inform internal structure about tab change
        # --> does not work automatically for newly created tabs
        self.onTabChanged()
        self.windowUpated.emit()

    def createTabs(self):
        """Creates and enables/disables new QT tab widgets for current task."""
        # check if only real/imag part or both should be displayed
        style = self.getPlotStyle()
        task = self.currentTask
        for tabIdx, tabData in enumerate(self.data[task]):
            # create new tab in tab widget
            tab = QtWidgets.QWidget()
            self.tabWidget.addTab(tab, tabData.tabname)
            # create new figure or disable tab if no data is available
            if not tabData.enabled:
                self.tabWidget.setTabEnabled(tabIdx, False)
            else:
                fig = self.createFigure(tab, style, tabIdx)
                self.figures.append(fig)

    def createFigure(self, tab, style, tabIdx):
        """Creates subplots for figure in current tab.

        Args:
            tab: Reference to tab widget that is to be filled.
            style: Plot style passed to subplot creater.
            tabIdx: Index of this tab w.r.t. tab bar parent widget.
        """
        # create matplotlib interface
        fig = plt.figure(dpi=self.dpi)
        canvas = backend_qt5agg.FigureCanvasQTAgg(fig)
        canvas.mpl_connect("resize_event", self.tightLayout)
        toolbar = backend_qt5agg.NavigationToolbar2QT(canvas, self)
        grid = QtWidgets.QGridLayout()
        tab.setLayout(grid)
        grid.addWidget(toolbar, 0, 0)
        grid.addWidget(canvas, 1, 0)
        # resolve tab titles etc. from dictionaries
        # NOTE: cannot use getCurrent here!
        task = self.currentTask
        data = self.data[task][tabIdx]
        if self.use_global_states:
            states = self.globalStates
        else:
            states = data.states
        # create plots
        if task.startswith("batch"):
            # instead of using only first TabData instance, use all for batch
            data = self.data[task]
            ax1, ax2 = self.plotter.plotBatch(fig, data, style)
        elif data.isTensor:
            ax1, ax2 = self.plotter.plotTen(
                fig, data.freqs, data.field, states, data.label, style
            )
        else:
            ax1, ax2 = self.plotter.plotScal(
                fig, data.freqs, data.field, data.label, style
            )
        # additional plots, e.g. experimental data
        if (
            self.additionalPlots["triggered"]
            and tabIdx in self.additionalPlots["tabID"]
        ):
            # colors
            # num = len(self.additionalData)
            # use hard-coded max. of 10 for consistent coloring
            num = 6
            cmap = plt.cm.cool(np.linspace(0, 1, num))
            alpha = 0.6
            lw = 4
            # real parts
            if ax1 is not None:
                for idx, ad in enumerate(self.additionalData):
                    ax1.plot(
                        ad.freqs,
                        ad.field.real,
                        label=ad.label,
                        color=cmap[idx],
                        alpha=alpha,
                        lw=lw,
                    )
                ax1.legend()
            # imaginary parts
            if ax2 is not None:
                for idx, ad in enumerate(self.additionalData):
                    # prevent doublings when plotting "together"
                    label = None if (style == "t") else ad.label
                    ax2.plot(
                        ad.freqs,
                        ad.field.imag,
                        label=label,
                        color=cmap[idx],
                        alpha=alpha,
                        lw=lw,
                    )
                ax2.legend()
        # make sure all figures/tabs are tight initially, not only last one
        plt.tight_layout()
        # draw all plots to canvas
        canvas.draw()
        return fig

    def onTabChanged(self):
        """Wrapper for functions to be called after a tab has changed."""
        self.linkTensorStatesToDialog()

    def linkTensorStatesToDialog(self):
        """Informs tensor elements dialog which dataset's states to set."""
        if not self.use_global_states:
            data = self.getCurrent("tabData")
            # valid array reference if tensor, None if scalar field
            self.tenElementsDialog.states = data.states
        else:
            self.tenElementsDialog.states = self.globalStates

    def readAdditionalData(self):
        """Reads non-Elk data from file(s) and triggers window update."""
        cwd = os.getcwd()
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Select one or more files to add to the current plot",
            cwd,
            "Data files (*.dat *.out *.mat);;All files (*.*)",
            options=QtWidgets.QFileDialog.DontUseNativeDialog,
        )
        for fname in files:
            freqs, field = io.readScalar(fname, hartree=False)
            if field is None:
                return
            # extract filename from path
            fname = os.path.basename(fname)
            # remove extension --> (base, ext)
            label = os.path.splitext(fname)[0]
            # make label latex friendly by escaping underscores
            label = misc.convertFileNameToLatex(label, unit=False)
            self.additionalData.append(TabData(freqs, field, label, fname))
        self.additionalPlots["triggered"] = True
        self.updateWindow()

    def removeAllAdditionalData(self):
        """Redraws window with all non-Elk data removed."""
        self.additionalData = []
        self.additionalPlots["triggered"] = False
        self.updateWindow()

    def batchLoad(self):
        """Loads data from user-selected folders for parameter studies."""
        print("\n/-------------------------------------------\\")
        print("|               batch-loading               |")
        print("\\-------------------------------------------/")
        # run dialog and check return state --> did user confirm or reject?
        if self.batchLoadDialog.exec() == QtWidgets.QDialog.Rejected:
            return

        # in case user confirmed valid choices, inform via terminal
        filename = self.batchLoadDialog.file
        folders = self.batchLoadDialog.folders
        parameter = self.batchLoadDialog.parameter
        numfreqs = self.batchLoadDialog.elkInput.numfreqs
        print("parameter:\n    {}".format(parameter))
        print("filename: \n    {}".format(filename))
        print("folders: ")
        for f in folders:
            print("    {}".format(f))
        print()

        # load individual output files into new list
        batchData = []
        for folder in folders:
            fname = os.path.join(folder, filename)
            reader = io.readScalar
            freqs, field = reader(fname, numfreqs)
            ylabel = misc.convertFileNameToLatex(filename)
            pvalue = elk.readElkInputParameter(parameter, path=folder)
            if pvalue is None:
                plabel = "not found"
                print(
                    "[WARNING] No value for {p} found in {f}\n".format(
                        p=parameter, f=fname
                    )
                )
                return
            elif isinstance(pvalue, list):
                pvalue = [str(item) for item in pvalue]
                plabel = " - ".join(pvalue)
            else:
                plabel = str(pvalue)
            # abuse task + tabname slot for parameter + value
            batchData.append(
                TabData(freqs, field, ylabel, fname, plabel, parameter)
            )
        # we need some unique string w/o whitespaces for each item
        taskText = "batch - {par}".format(par=parameter)
        # link batch data to corresponding batch "task" in data list
        self.data[taskText] = batchData
        # take care of Elk dicts
        self.tabNameDict[taskText] = [filename]
        # update combobox entry
        self.taskChooser.addItem(taskText)
        idx = self.taskChooser.findText(taskText)
        # update task and trigger window update per currentIndexChanged
        self.statusbar.showMessage("Batch loading files...", 2000)
        self.taskChooser.setCurrentIndex(idx)

    def convert(self):
        """Converts and displays currently visible field acc. to user input."""
        if self.currentTask is None:
            QtWidgets.QMessageBox.warning(
                self, "No task chosen!", "Please choose a task..."
            )
            return
        print("\n/-------------------------------------------\\")
        print("|                 converting                |")
        print("\\-------------------------------------------/")
        # shortcuts
        convDialog = self.convertDialog
        task, tabIdx, tabName, data = self.getCurrent("all")
        # create converter instance with dummy q-vector
        dummyQ = [1, 0, 0]
        eta = self.elkInput.swidth
        converter = convert.Converter(dummyQ, data.freqs, eta)
        # set input function text
        dictEntry = converter._CONVERTER_DICT[tabName]
        inputFunction = dictEntry[0]
        convDialog.textInputFunction.setText(inputFunction)
        # refill output function combo box for currently visible tab
        for i in range(convDialog.comboBox.count()):
            convDialog.comboBox.removeItem(0)
        # leave out first item in entry (= input function name)
        for item in dictEntry[1:]:
            convDialog.comboBox.addItem(item[0])
        # run dialog and check return state --> did user confirm or reject?
        if convDialog.exec() == QtWidgets.QDialog.Rejected:
            return
        # if accepted, update converter settings accordingly
        if convDialog.improvedRegularization:
            regularization = "improved"
        else:
            regularization = "standard"
        converter.q = convDialog.q
        converter.opticalLimit = convDialog.opticalLimit
        # TODO add regularization
        # converter.regularization = ?
        print("[INFO] Starting conversion with following settings:")
        print("-------------------------------------------")
        print(inputFunction, "-->", convDialog.outputFunction)
        print("-------------------------------------------")
        print("q-vector        =", convDialog.q)
        print("optical limit   =", convDialog.opticalLimit)
        print("regularization. =", regularization)
        print("-------------------------------------------\n")
        # add +1 b/c first item (dictEntry[0] = input name) is not in combobox
        idx = convDialog.outputFunctionIdx + 1
        convertFunction = dictEntry[idx][2]
        output = convertFunction(data.field)
        # create new TabData instance for new field and append to plot data
        tabNameConv = dictEntry[idx][1]
        label = self.labelDict[tabNameConv]
        tabNameConv += "[c]"
        td = TabData(data.freqs, output, label, "[convert]", tabNameConv, task)
        self.data[task].append(td)
        self.updateWindow()

    def dummy(self):
        QtWidgets.QMessageBox.about(
            self,
            "Not yet available",
            "Coming soon...please have a look at our github page for updates."
        )

    def getCurrent(self, attr):
        """Finds and returns current task and/or tab name, ID and data."""
        task = self.currentTask
        tabIdx = self.tabWidget.currentIndex()
        try:
            # use strings from dictionary for pre-defined tabs
            tabName = self.tabNameDict[task][tabIdx]
        except IndexError:
            # derive name from string saved in tabData instance for e.g.
            # converted data
            tabName = self.data[task][tabIdx].tabname
            if "[" in tabName:
                tabName = tabName.split("[")[0]
        tabData = self.data[task][tabIdx]
        # return only what caller asked for
        if attr == "all":
            return task, tabIdx, tabName, tabData
        elif type(attr) in [list, tuple]:
            local = locals()
            return [local[a] for a in attr]
        elif isinstance(attr, str):
            return locals()[attr]
        else:
            raise TypeError("[ERROR] must be str or list[str] / tuple[str]")

    def parseElkFiles(self):
        """Wrapper that handles reading of Elk input files."""
        try:
            elkInput = elk.ElkInput(verbose=True)
        except FileNotFoundError:
            QtWidgets.QMessageBox.about(
                self,
                "[ERROR] File not found!",
                "File(s) elk.in and/or INFO.OUT could not be found in current "
                "working directory. \n\nPlease choose an Elk output folder...",
            )
            return None
        return elkInput

    def changeWorkingDirectory(self, path=None):
        """Updates current working dir to user choice and reads Elk input."""
        from PyQt5.QtWidgets import QFileDialog
        if path is None:
            path = QFileDialog.getExistingDirectory(
                self,
                "Choose Directory",
                os.getcwd(),
                QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog,
            )
        try:
            os.chdir(path)
        except FileNotFoundError:
            print("\n[ERROR] Invalid path! Please start again...")
            sys.exit()
        self.statusbar.showMessage("Change working dir to " + str(path), 2000)
        self.reloadData()

    def tenElementsDialogWrapper(self):
        """Wrapper that handles opening of tensor element dialog."""
        try:
            # check if user changed any settings or cancelled the dialog
            if self.tenElementsDialog.exec() == QtWidgets.QDialog.Accepted:
                self.updateWindow()
                self.statusbar.showMessage("Plot updated...", 2000)
        except TypeError:
            QtWidgets.QMessageBox.about(
                self, "[ERROR] No task!", "Please choose a task first..."
            )

    def updateGlobalTensorSettings(self):
        """Updates global tensor states and settings."""
        if self.actionGlobalTensorSettings.isChecked():
            self.use_global_states = True
            data = self.getCurrent("tabData")
            # copy over (not reference!) states of current view as global ones
            try:
                self.globalStates = list(data.states)
            except KeyError:
                QtWidgets.QMessageBox.about(
                    self, "[ERROR] No task!", "Please choose a task first..."
                )
            # inform tensor elements dialog to use global states now
            self.linkTensorStatesToDialog()
        else:
            self.use_global_states = False
            self.globalStates = None
        self.updateWindow()

    def setPlotRange(self, full):
        """Sets the visible frequency range either to minimum or to zero."""
        if full:
            self.plotter.minw = self.elkInput.minw
            self.statusbar.showMessage(
                "Setting minimum frequency to {} eV...".format(
                    self.elkInput.minw
                ),
                2000,
            )
        else:
            self.plotter.minw = 0
            self.statusbar.showMessage(
                "Setting minimum frequency to 0 eV", 2000
            )
        self.updateWindow()

    def changeSplitMode(self, action):
        """Updates window with new split mode when split is enabled.

        Args:
            mode: Split style can be 'v' for vertical or 'h' for horizontal.
        """
        oldSplitMode = self.splitMode
        if action == "h":
            self.splitMode = "h"
            self.actionHorizontalSplit.setChecked(True)
            self.actionVerticalSplit.setChecked(False)
        elif action == "v":
            self.splitMode = "v"
            self.actionHorizontalSplit.setChecked(False)
            self.actionVerticalSplit.setChecked(True)
        modeChanged = (oldSplitMode != self.splitMode)
        if self.btnSplitView.isChecked() and modeChanged:
            self.updateWindow()

    def getPlotStyle(self):
        """Reads plot style from current GUI configuration."""
        if self.btnRealPart.isChecked():
            return "r"
        elif self.btnImaginaryPart.isChecked():
            return "i"
        elif self.btnSplitView.isChecked():
            return self.splitMode
        elif self.btnTogether.isChecked():
            return "t"
        else:
            assert False

    def tightLayout(self, event):
        """Wrapper to catch strange error from mpl's resize function."""
        try:
            for fig in self.figures:
                fig.tight_layout()
        except ValueError:
            print("[ERROR] strange error from plt.tight_layout()")

    def setMplOptions(self):
        """Makes default plot lines, markers and fonts more visible."""
        # font configuration for axes, legend, etc.
        font = {"family": "serif", "size": 18}
        plt.rc("font", **font)
        plt.rc("legend", fontsize=16)
        # use mpl's own tex-engine and set consistent font to stix
        mpl.rcParams["mathtext.fontset"] = "stix"
        mpl.rcParams['font.family'] = 'STIXGeneral'
        # global line and marker options
        mpl.rcParams["lines.linewidth"] = 2
        mpl.rcParams["lines.markeredgewidth"] = 2
        mpl.rcParams["lines.markersize"] = 10
        mpl.rcParams["markers.fillstyle"] = "none"

    def showAbout(self):
        """Opens GUI window with copyright and license information."""
        about = QtWidgets.QMessageBox(self)
        about.setWindowTitle("About...")
        # make links work
        about.setTextFormat(Qt.RichText)
        about.setText(
            "<div align='center'>"
            "Elk Optics Analyzer (ElkOA) v{} <br>".format(elkoa.__version__)
            + "- Easily plot and analyze Elk optics output data -</div>"
            "<p>Copyright © 2017-2019 René Wirnata</p>"
            "<p>This program is free software: you can redistribute it and/or "
            "modify it under the terms of the GNU General Public License as "
            "published by the Free Software Foundation, either version 3 of "
            "the License, or (at your option) any later version. </p>"
            "<p>This program is distributed in the hope that it will be "
            "useful, but WITHOUT ANY WARRANTY; without even the implied "
            "warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. "
            "See the GNU General Public License for more details. </p>"
            "<p>You should have received a copy of the GNU General Public "
            "License along with this program. If not, see "
            "<a href='https://www.gnu.org/licenses/'>"
            "https://www.gnu.org/licenses/</a>.</p>"
            "<p style='line-height:1.4'>See also:<br>"
            "<a href='http://elk.sourceforge.net'> The Elk Code</a><br>"
            "<a href='https://qftmaterials.wordpress.com'> Quantum Field "
            "Theory of Material Properties</a><br>"
            "<a href='https://tu-freiberg.de/fakultaet2/thph'> Institute for "
            "Theoretical Physics @ TU BA Freiberg</a>"
        )
        about.exec()

    def printAbout(self):
        """Prints copyright and license information to terminal."""
        txt = (
            "\n============================================================\n"
            ">>>             Elk Optics Analyzer (ElkOA)              <<<\n"
            ">>>         Copyright (C) 2017-2019 René Wirnata         <<<\n"
            "============================================================\n\n"
            "This program is free software and comes with ABSOLUTELY NO \n"
            "WARRANTY. You are welcome to redistribute it under certain \n"
            "conditions. See Help->About in GUI for details.\n\n"
            "Running version {} \n".format(elkoa.__version__)
        )
        print(txt)

    def quitGui(self):
        """Quits QT application."""
        print("\n/-------------------------------------------\\")
        print("|            quitting application           |")
        print("\\-------------------------------------------/")
        self.close()


# EOF - UiMainWindow.py
