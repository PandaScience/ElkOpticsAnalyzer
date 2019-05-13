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

import copy
import functools
import os
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

import elkoa
import elkoa.gui.UiDesigner as UiDesigner
import elkoa.gui.UiDialogs as UiDialogs
from elkoa.utils import convert, elk, dicts, misc, io, plot

import matplotlib as mpl
import numpy as np

# make sure we use QT5; needs to come before any other mpl imports
mpl.use("Qt5Agg")  # noqa

import matplotlib.pyplot as plt
from matplotlib.backends import backend_qt5agg


def rejectOnStartScreen(f):
    """Decorator preventing users to activate features on start screen."""

    @functools.wraps(f)
    def wrapper(self, checked=None, *args, **kwargs):
        # checked is return value from QAction::triggered(bool checked = False)
        # we need to masked to prevent error:
        # f() takes 1 positional argument but 2 were given
        if self.taskChooser.currentIndex() < 1:
            QtWidgets.QMessageBox.warning(
                self, "No task chosen!", "Please choose a task..."
            )
            return
        else:
            return f(self, *args, **kwargs)

    return wrapper


class TooManyOnTopPlotsError(Exception):
    """Raised when user adds more than 6 on-top plots."""

    pass


class TabData:
    """Stores content of Elk optical output files

    Attributes:
        freqs: Frequencies in eV.
        field: Tensor or scalar field with real and imaginary parts as ndarray.
        label: Labeltext for plot from labelDict.
        filename: Name of file where data has been loaded from.
        notes: Space for additional data, e.g. batch load label.
        enabled: Bool indicating if tab should be "filled" at all.
        isTensor: Indicates if field should be handled as tensor or scalar
            field.
        isVector: Indicates if tensor field is actually a vector field and only
            elements 11, 22 and 33 should be used. This needs to be set
            manually, misc.isTensor() cannot decide vector vs. tensor with only
            diagonal elements available.
        states: Array holding the currently enabled/disabled/n.a. elements.
    """

    def __init__(
        self, freqs=None, field=None, label=None, filename=None, notes=None
    ):
        self.freqs = freqs
        self.field = field
        self.label = label
        self.filename = filename
        self.notes = notes
        self.enabled = None
        self.isTensor = None
        self.isVector = False
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
        # mark scalar functions as such
        else:
            self.enabled = True
            self.isTensor = False
            print("[INFO] Successfully read data for scalar", self.filename)


class MainWindow(
    QtWidgets.QMainWindow, UiDesigner.Ui_ElkOpticsAnalyzerMainWindow
):
    """Main window class where the plots are located.

    The user can choose to display data from available tasks and how to plot
    them, i.e. real/imag part together, only one or in vertical/horizontal
    split screen. Combobox tasks with unavailable files in current working
    directory will be disabled.

    Attributes:
        Shortcuts for convenience:
            tabNameDict, fileNameDict, labelDict, readerDict, additionalData
        splitMode: Character indicating horizontal or vertical split mode.
        dpi: Pixel density to use in figures.
        use_global_states: Bool, true if tensor element dialog should apply to
            all plots, false when apply only to current figure.
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
    """

    # new signals - must be class members
    windowUpated = QtCore.pyqtSignal()

    def __init__(self, cwd=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.modifyUi()

        # shortcuts or deepcopies for dicts being modified later
        self.tabNameDict = copy.deepcopy(dicts.TAB_NAME_DICT)
        self.fileNameDict = dicts.FILE_NAME_DICT
        self.readerDict = dicts.READER_DICT
        self.labelDict = dicts.LABEL_DICT
        self.conversionDict = dicts.CONVERSION_DICT
        self.additionalData = copy.deepcopy(dicts.ADDITIONAL_DATA)

        # construct dialog
        self.tenElementsDialog = UiDialogs.TensorElementsDialog()
        self.batchLoadDialog = UiDialogs.BatchLoadDialog()
        self.convertDialog = UiDialogs.ConvertDialog()
        self.saveTabDialog = UiDialogs.SaveTabDialog()
        self.unitDialog = UiDialogs.UnitDialog()

        # attributes with default values
        self.splitMode = "v"
        self.dpi = 100
        # NOTE: keep in sync with MainWindow.ui
        self.use_global_states = False
        self.additionalPlots = {"triggered": False, "tabID": [0]}
        self.globalStates = None
        self.currentTask = None
        self._pytest = False

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
        self.changeWorkingDirectory(path=cwd, update=True)
        # set min/max frequency on x-axis, default: minw=0
        self.plotter = plot.Plot(maxw=self.elkInput.maxw)

    def modifyUi(self):
        """Contains further modifications the designer can't do by default."""
        # view --> legend location
        self.legendGroup = QtWidgets.QActionGroup(self)
        actions = [
            self.actionLegendBest,
            self.actionLegendUpperRight,
            self.actionLegendUpperLeft,
            self.actionLegendLowerLeft,
            self.actionLegendLowerRight,
            self.actionLegendRight,
            self.actionLegendCenterLeft,
            self.actionLegendCenterRight,
            self.actionLegendLowerCenter,
            self.actionLegendUpperCenter,
            self.actionLegendCenter,
        ]
        for action in actions:
            self.legendGroup.addAction(action)
        # view --> split view
        self.splitGroup = QtWidgets.QActionGroup(self)
        self.splitGroup.addAction(self.actionVerticalSplit)
        self.splitGroup.addAction(self.actionHorizontalSplit)

    def connectSignals(self):
        """Connects GUI buttons and menu options to functions of this class."""
        # combo box for tasks
        self.taskChooser.currentIndexChanged[str].connect(
            lambda: self.updateWindow(newtask=True)
        )
        # menu "File"
        self.actionSetWorkingDir.triggered.connect(
            lambda: self.changeWorkingDirectory(path=None, update=True)
        )
        self.actionReload.triggered.connect(self.reloadData)
        self.actionReadAdditionalData.triggered.connect(
            self.readAdditionalData
        )
        self.actionRemoveADFromTab.triggered.connect(
            lambda: self.removeAdditionalData("tab")
        )
        self.actionRemoveADFromTask.triggered.connect(
            lambda: self.removeAdditionalData("task")
        )
        self.actionRemoveAllAdditionalData.triggered.connect(
            lambda: self.removeAdditionalData("all")
        )
        self.actionBatchLoad.triggered.connect(self.batchLoad)
        self.actionSaveTabAs.triggered.connect(self.saveTab)
        self.actionQuit.triggered.connect(self.quitGui)
        # menu "Convert"
        self.actionResponseRelations.triggered.connect(self.convert)
        self.actionRefractiveIndex.triggered.connect(self.dummy)
        self.actionIndexEllipsoid.triggered.connect(self.dummy)
        # menu "View"
        self.splitGroup.triggered.connect(self.changeSplitMode)
        self.actionTensorElements.triggered.connect(
            self.tenElementsDialogWrapper
        )
        self.actionGlobalTensorSettings.triggered.connect(
            self.updateGlobalTensorSettings
        )
        self.legendGroup.triggered.connect(self.setLegendPlacing)
        self.actionShowAdditionalData.triggered.connect(self.updateWindow)
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
        self.additionalData = copy.deepcopy(dicts.ADDITIONAL_DATA)
        self.tabNameDict = copy.deepcopy(dicts.TAB_NAME_DICT)
        self.data = {}
        self.figures = []
        self.readAllData()
        # inform user
        self.statusbar.showMessage("Data loaded, ready to plot...", 0)
        print("\n/-------------------------------------------\\")
        print("|               start plotting              |")
        print("\\-------------------------------------------/\n")
        # only update window if this is not an initial load
        if self.currentTask is not None:
            # go to 1st tab and prevent opening tab which doesn't exist anymore
            self.updateWindow(newtask=True)

    def readAllData(self):
        """Reads data from Elk input files and Elk optical output."""
        self.elkInput = None
        while self.elkInput is None:
            try:
                self.elkInput = self.parseElkFiles()
            except FileNotFoundError:
                self.changeWorkingDirectory()
        # set min/max frequency on x-axis using elk.in data (default: minw=0)
        # NOTE: must stay here for initial load AND reload to work!
        self.plotter = plot.Plot(maxw=self.elkInput.maxw)
        print("\n--- reading optics data ---\n")
        for task in self.fileNameDict:
            # prepare array holding new TabData instances for each tab of task
            self.data[task] = []
            for tabIdx, tab in enumerate(self.tabNameDict[task]):
                reader = self.readerDict[task][tabIdx]
                filename = self.fileNameDict[task][tabIdx]
                tabName = self.tabNameDict[task][tabIdx]
                label = self.labelDict[tabName]
                freqs, field = reader(filename, self.elkInput.numfreqs)
                self.data[task].append(TabData(freqs, field, label, filename))
            # disable/mark combo box entry if no task data is present at all
            tabStates = [tab.enabled for tab in self.data[task]]
            if not any(tabStates):
                # find index of comboBox item that contains `task` as substring
                idx = self.taskChooser.findText(task, Qt.MatchContains)
                # remove unavailable tasks
                self.taskChooser.removeItem(idx)

    @rejectOnStartScreen
    def updateWindow(self, newtask=False):
        """Redraws figure for currently chosen Elk task."""
        currentText = self.taskChooser.currentText()
        # extract task number (integer) from combobox entry
        self.currentTask = currentText.split("-")[0].strip()
        if not newtask:
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
        task = self.currentTask
        # use tabNameDict here to make sure to find all batch tasks, since new
        # batch data is appended in a special way
        for tabIdx, tabData in enumerate(self.data[task]):
            # make sure to stop after first tab for batch data
            if task.startswith("batch") and tabIdx >= 1:
                break
            # create new tab in tab widget
            tab = QtWidgets.QWidget()
            # use dict instead b/c td.tabname will not work for batch tabs
            tabName = self.tabNameDict[task][tabIdx]
            self.tabWidget.addTab(tab, tabName)
            # create new figure or disable tab if no data is available
            if tabData.enabled is False:
                self.tabWidget.setTabEnabled(tabIdx, False)
            else:
                fig = self.createFigure(tab, tabIdx)
                self.figures.append(fig)

    def createFigure(self, tab, tabIdx):
        """Creates subplots for figure in current tab.

        Args:
            tab: Reference to tab widget that is to be filled.
            tabIdx: Index of this tab w.r.t. tab bar parent widget.
        """
        # create matplotlib interface
        fig, canvas = self.createMplInterface(tab)
        # resolve tab titles etc. from dictionaries
        # NOTE: cannot use getCurrent() here!
        task = self.currentTask
        data = self.data[task][tabIdx]
        # apply correct tensor elements states acc. to user setting
        if self.use_global_states:
            states = self.globalStates
        else:
            states = data.states
        # create plots
        style = self.getPlotStyle()
        if task.startswith("batch"):
            # instead of using only first TabData instance, use all for batch
            batchData = self.data[task]
            ax1, ax2 = self.plotter.plotBatch(fig, batchData, style)
        elif data.isVector:
            ax1, ax2 = self.plotter.plotVector(
                fig, data.freqs, data.field, states, data.label, style
            )
        elif data.isTensor:
            ax1, ax2 = self.plotter.plotTensor(
                fig, data.freqs, data.field, states, data.label, style
            )
        else:
            ax1, ax2 = self.plotter.plotScalar(
                fig, data.freqs, data.field, data.label, style
            )
        # draw additional plots on top
        if self.actionShowAdditionalData.isChecked():
            try:
                ad = self.additionalData[task][tabIdx]
                if len(ad) == 0:
                    raise ValueError
                self.createAdditionalPlots(ax1, ax2, ad)
            except (IndexError, KeyError, ValueError):
                # happens for new tabs/tasks when no add.data loaded yet
                pass
            except TooManyOnTopPlotsError:
                QtWidgets.QMessageBox.warning(
                    self, "[ERROR]", "Can't add more than 6 on-top plots."
                )
                return
        # make sure all figures/tabs are tight initially, not only last one
        plt.tight_layout()
        # draw all plots to canvas
        canvas.draw()
        return fig

    def createAdditionalPlots(self, ax1, ax2, addData):
        """Adds additional plots to existing figure and updates legend."""
        # use hard-coded max. for consistent coloring
        num = 6
        cmap = plt.cm.cool(np.linspace(0, 1, num))
        alpha = 0.6
        lw = 4
        if len(addData) > 6:
            raise TooManyOnTopPlotsError
        # real parts
        if ax1 is not None:
            for idx, ad in enumerate(addData):
                ax1.plot(
                    ad.freqs,
                    ad.field.real,
                    label=ad.label,
                    color=cmap[idx],
                    alpha=alpha,
                    lw=lw,
                )
            # update legend
            ax1.legend()
        # imaginary parts
        if ax2 is not None:
            for idx, ad in enumerate(addData):
                # prevent doublings when plotting "together"
                label = None if (self.getPlotStyle == "t") else ad.label
                ax2.plot(
                    ad.freqs,
                    ad.field.imag,
                    label=label,
                    color=cmap[idx],
                    alpha=alpha,
                    lw=lw,
                )
            ax2.legend()

    def createMplInterface(self, tab):
        """Create mpl interface as grid of figure and navigation toolbar."""
        fig = plt.figure(dpi=self.dpi)
        canvas = backend_qt5agg.FigureCanvasQTAgg(fig)
        canvas.mpl_connect("resize_event", self.tightLayout)
        toolbar = backend_qt5agg.NavigationToolbar2QT(canvas, self)
        grid = QtWidgets.QGridLayout()
        tab.setLayout(grid)
        grid.addWidget(toolbar, 0, 0)
        grid.addWidget(canvas, 1, 0)
        return fig, canvas

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

    @rejectOnStartScreen
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
        if len(files) == 0:
            print("\n--- cancelled by user ---")
            return
        # ask for format settings
        if self.unitDialog.exec() == QtWidgets.QDialog.Rejected:
            return
        hartree = self.unitDialog.hartree
        # check if dict-array is already present and add new [] as required
        task, tabIdx = self.getCurrent(["task", "tabIdx"])
        while True:
            try:
                num = len(self.additionalData[task][tabIdx])
            except KeyError:
                # happens when user added new batch data
                self.additionalData[task] = []
                continue
            except IndexError:
                # happens when user created new tabs, e.g. via convert
                self.additionalData[task].append([])
                continue
            # go on if all conditions are met
            break
        if len(files) + num > 6:
            QtWidgets.QMessageBox.warning(
                self, "[ERROR]", "Can't add more than 6 on-top plots."
            )
            return
        for fname in files:
            freqs, field = io.readScalar(fname, hartree=hartree)
            # extract filename from path
            fname = os.path.basename(fname)
            # check if loading was successful
            if field is None:
                print("[WARNING] Could not load {}, skipping...".format(fname))
                continue
            # remove extension --> (base, ext)
            label = os.path.splitext(fname)[0]
            # make label latex friendly by escaping underscores
            label = misc.convertFileNameToLatex(label, unit=False)
            td = TabData(freqs, field, label, fname)
            self.additionalData[task][tabIdx].append(td)
        self.updateWindow()

    def removeAdditionalData(self, mode):
        """Removes all on-top plots from task/tab/everywhere."""
        task, tabIdx = self.getCurrent(["task", "tabIdx"])
        if mode == "tab":
            self.additionalData[task][tabIdx] = []
        elif mode == "task":
            self.additionalData[task] = [[]]
        elif mode == "all":
            self.additionalData = copy.deepcopy(dicts.ADDITIONAL_DATA)
        self.updateWindow()

    def batchLoad(self):
        """Loads data from user-selected folders for parameter studies."""
        print("\n/-------------------------------------------\\")
        print("|               batch-loading               |")
        print("\\-------------------------------------------/")
        # don't open dialog when auto-testing
        if self._pytest is False:
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
            fullPath = os.path.join(folder, filename)
            shortPath = misc.shortenPath(fullPath, 3)
            freqs, field = io.readScalar(fullPath, numfreqs)
            ylabel = misc.convertFileNameToLatex(filename)
            if field is None:
                print("[ERROR] File {} not found".format(shortPath))
                return
            try:
                # convert e.g. [A, 0.5, 200] --> "A, 0.5, 200"
                pvalue = elk.readElkInputParameter(parameter, path=folder)
                plist = [str(item) for item in pvalue]
                plabel = ", ".join(plist)
            except TypeError:
                # in case no list, only single value
                plabel = str(pvalue)
            except NameError as e:
                # in case parameter not found
                print(e)
                return
            # abuse task + tabname slot for parameter + value
            batchData.append(
                TabData(freqs, field, ylabel, shortPath, [parameter, plabel])
            )
        # we need some unique string for each item --> |batch #N - parameter|
        task = "batch #1"
        while self.taskChooser.findText(task, Qt.MatchContains) != -1:
            task = "batch #" + str(int(task.split("#")[1]) + 1)
        taskText = task + " - {}".format(parameter)
        # link batch data to corresponding batch "task" in data list
        self.data[task] = batchData
        # use batch-filename as tabname -> generates only 1 tab per batch later
        self.tabNameDict[task] = [filename]
        # update combobox entry
        self.taskChooser.addItem(taskText)
        idx = self.taskChooser.findText(taskText)
        # update task and trigger window update per currentIndexChanged
        self.statusbar.showMessage("Batch loading files...", 2000)
        self.taskChooser.setCurrentIndex(idx)

    @rejectOnStartScreen
    def saveTab(self):
        """Saves data from current tab view without on-top add. data."""
        print("\n/-------------------------------------------\\")
        print("|               save tab data               |")
        print("\\-------------------------------------------/")
        dialog = self.saveTabDialog
        data = self.getCurrent("tabData")
        # if tensor: states = ndarray, if scalar: states = None
        states = copy.deepcopy(data.states)
        if dialog.exec(states, data.isVector) == QtWidgets.QDialog.Rejected:
            return
        # get user selections
        filename = dialog.filename
        hartree = dialog.hartree
        threeColumn = dialog.threeColumn
        prec = dialog.precision
        states = dialog.states
        if data.isVector:
            elements = [
                (i + 1) for i in range(3) if states[i * 4] == Qt.Checked
            ]
            io.writeVector(
                filename,
                data.freqs,
                data.field,
                elements=elements,
                threeColumn=threeColumn,
                hartree=hartree,
                prec=prec,
            )
            for e in elements:
                fname = filename.replace("_i", "_" + str(e))
                print("[INFO] Tabdata saved as {}".format(fname))
        elif data.isTensor:
            # choose indices/elements to write to file from user selection
            default = [11, 12, 13, 21, 22, 23, 31, 32, 33]
            elements = [
                e for idx, e in enumerate(default) if states[idx] == Qt.Checked
            ]
            # save chosen data to files
            io.writeTensor(
                filename,
                data.freqs,
                data.field,
                elements=elements,
                threeColumn=threeColumn,
                hartree=hartree,
                prec=prec,
            )
            for e in elements:
                fname = filename.replace("_ij", "_" + str(e))
                print("[INFO] Tabdata saved as {}".format(fname))
        else:
            io.writeScalar(
                filename,
                data.freqs,
                data.field,
                threeColumn=threeColumn,
                hartree=hartree,
                prec=prec,
            )
            print("[INFO] Tabdata saved as {}".format(filename))

    @rejectOnStartScreen
    def convert(self):
        """Converts and displays currently visible field acc. to user input."""
        task, tabIdx, tabName, data = self.getCurrent("all")
        # remove ext. from converted data to find correct converter entry
        if "[c]" in tabName:
            tabName = tabName.split("[")[0]
        # check if any converter is available
        try:
            inputDict = self.conversionDict[tabName]
        except KeyError:
            print("[WARNING] No conversion available for {}.".format(tabName))
            QtWidgets.QMessageBox.warning(
                self, "[WARNING]", "No conversion available for this field."
            )
            return
        # check if all tensor elements are available
        if data.isTensor and Qt.PartiallyChecked in data.states:
            QtWidgets.QMessageBox.warning(
                self, "[ERROR]", "Not all tensor elements available..."
            )
            return

        print("\n/-------------------------------------------\\")
        print("|                 converting                |")
        print("\\-------------------------------------------/")
        # set input function text
        convDialog = self.convertDialog
        convDialog.inputDict = inputDict
        # run dialog and check return state --> did user confirm or reject?
        if convDialog.exec() == QtWidgets.QDialog.Rejected:
            return
        # create converter instance with dummy q-vector
        eta = self.elkInput.swidth
        converter = convert.Converter(convDialog.q, data.freqs, eta)
        converter.opticalLimit = convDialog.opticalLimit
        converter.regularization = convDialog.regularization

        # print user-friendly info strings
        inputFieldName = inputDict["name"]
        outputFieldName = convDialog.outputFunction
        regularization = converter.regularization.replace("imp", "improved")
        regularization = regularization.replace("conv", "conventional")
        print("[INFO] Starting conversion with following settings:")
        print("-------------------------------------------")
        print(inputFieldName, "-->", outputFieldName)
        print("-------------------------------------------")
        print("q-vector       =", converter.q)
        print("optical limit  =", converter.opticalLimit)
        print("regularization =", regularization)
        print("-------------------------------------------\n")
        # find correct converter
        converterDict = inputDict["converters"][outputFieldName]
        convertFunction = converter.getConverter(converterDict["functionName"])
        try:
            output = convertFunction(data.field)
        except ValueError as e:
            msg = str(e).split("[ERROR]")[1].strip()
            QtWidgets.QMessageBox.warning(self, "[ERROR]", msg)
            print(str(e))
            return
        # create new TabData instance for new field and append to plot data
        tabName = converterDict["tabName"]
        label = self.labelDict[tabName]
        tabNameConv = tabName + "[c]"
        td = TabData(data.freqs, output, label, "[convert]", task)
        if converterDict["returnsVector"]:
            td.isVector = True
        self.data[task].append(td)
        # append corresponding dictionary entries
        self.tabNameDict[task].append(tabNameConv)
        self.additionalData[task].append([])
        # draw new data to screen
        self.updateWindow()
        tabIdx = len(self.tabNameDict[task]) - 1
        self.tabWidget.setCurrentIndex(tabIdx)

    def dummy(self):
        QtWidgets.QMessageBox.about(
            self,
            "Not yet available",
            "Coming soon...please have a look at our github page for updates.",
        )

    def getCurrent(self, attr):
        """Finds and returns current task and/or tab name, ID and data."""
        task = self.currentTask
        tabIdx = self.tabWidget.currentIndex()
        # use strings from dictionaries
        tabName = self.tabNameDict[task][tabIdx]
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
            raise FileNotFoundError
        return elkInput

    def changeWorkingDirectory(self, path=None, update=False):
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
            # stops event loop (when called in while-loop, will hang there...)
            self.quitGui()
            # terminates program directly (to break while-loop)
            sys.exit()
        self.statusbar.showMessage("Change working dir to " + str(path), 2000)
        if update:
            self.reloadData()

    @rejectOnStartScreen
    def tenElementsDialogWrapper(self):
        """Wrapper that handles opening of tensor element dialog."""
        if self.tenElementsDialog.exec() == QtWidgets.QDialog.Accepted:
            self.updateWindow()
            self.statusbar.showMessage("Plot updated...", 2000)

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

    def setPlotRange(self, checked):
        """Sets the visible frequency range either to minimum or to zero."""
        if checked:
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
        """Updates window with new split mode when split is enabled."""
        oldSplitMode = self.splitMode
        if action == self.actionHorizontalSplit:
            self.splitMode = "h"
        else:
            self.splitMode = "v"
        modeChanged = oldSplitMode != self.splitMode
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
            raise ValueError("[ERROR] Can't find style...")

    def tightLayout(self, event):
        """Wrapper to catch strange error from mpl's resize function."""
        try:
            for fig in self.figures:
                fig.tight_layout()
        except ValueError:
            print("[ERROR] strange error from plt.tight_layout()")

    def setLegendPlacing(self, action):
        """Sets legend loc. in plotter instance to what is checked in GUI."""
        oldLocation = self.plotter.loc
        self.plotter.loc = action.text()
        if oldLocation != self.plotter.loc:
            self.updateWindow()

    def setMplOptions(self):
        """Makes default plot lines, markers and fonts more visible."""
        # font configuration for axes, legend, etc.
        font = {"family": "serif", "size": 18}
        plt.rc("font", **font)
        plt.rc("legend", fontsize=16)
        # use mpl's own tex-engine and set consistent font to stix
        mpl.rcParams["mathtext.fontset"] = "stix"
        mpl.rcParams["font.family"] = "STIXGeneral"
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
