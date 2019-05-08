# coding: utf-8
# vim: set ai ts=4 sw=4 sts=0 noet pi ci

# Copyright © 2019 René Wirnata.
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
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

import elkoa.gui.UiInterface as UiInterface
from elkoa.utils import dicts, elk


def _handleErrorsAndReturn(widget, error):
    # return or notify user which selection is not valid
    if error is None:
        widget.accept()
    else:
        from PyQt5.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            widget,
            "Warning!",
            "{err} Go on or cancel?".format(err=error),
            QMessageBox.Retry | QMessageBox.Close,
            QMessageBox.Retry,
        )
        if reply == QMessageBox.Close:
            # click <cancel> button on behalf of user
            print("\n--- cancelled by user ---")
            widget.reject()


class BatchLoadDialog(QtWidgets.QDialog, UiInterface.Ui_BatchLoadDialog):
    """Dialog class for choosing file, folders and parameter to batch-plot.

    Attributes:
        file: Elk optics output file, e.g. "SIGMA_11.OUT".
        folders: Elk calculation folders, each containing <file> and <elk.in>.
        parameter: Valid elk input parameter that can be read from elk.in in
            each <folder>.
        cwd: Path where ElkOA was started from or which user has selected as
            current working path.
    """

    def __init__(self):
        super(BatchLoadDialog, self).__init__()
        self.setupUi(self)
        # initialize class members
        self._folderDir = None
        self.file = None
        self.folders = None
        self.parameter = None
        self.elkInput = None
        self.cwd = os.getcwd()
        # enable <DEL> key on folder list via shortcut
        self.deleteShortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence(Qt.Key_Delete), self.listWidget
        )
        # populate parameter combo box
        self.fillParamerBox()
        # connect signals and slots
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.accepted.connect(self.accepted)
        self.btnFileOpen.clicked.connect(self.selectFile)
        self.btnFolderOpen.clicked.connect(self.selectFolders)
        self.deleteShortcut.activated.connect(self.removeFolders)

        # since by default, QT5 doesn't support multiple folders, we have to
        # build our own dialog, see e.g. https://stackoverflow.com/a/38255958
        self.fdialog = QtWidgets.QFileDialog()
        # only show directories, not files
        self.fdialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        # as above, use QT dialog instead of the OS one
        self.fdialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        # enable multi-folder selection for list and tree view
        listView = self.fdialog.findChild(QtWidgets.QListView, "listView")
        if listView:
            listView.setSelectionMode(
                QtWidgets.QAbstractItemView.ExtendedSelection
            )
        treeView = self.fdialog.findChild(QtWidgets.QTreeView)
        if treeView:
            treeView.setSelectionMode(
                QtWidgets.QAbstractItemView.ExtendedSelection
            )

    def exec(self):
        """Extends QDialog's exec()."""
        # update cwd in case user changed working dir
        self.cwd = os.getcwd()
        # call original method from base class QDialog
        return super(BatchLoadDialog, self).exec()

    def rejected(self):
        """Writes some info to terminal and hides dialog."""
        print("\n--- cancelled by user ---")
        self.reject()

    def accepted(self):
        """Check if user choices are valid and returns to main window."""
        # update class members to currently visible selections
        self.file = self.lineEdit.text()
        self.folders = []
        for index in range(self.listWidget.count()):
            self.folders.append(self.listWidget.item(index).text())
        self.parameter = self.comboBox.currentText()
        # check for valid selections
        error = None
        if self.file == "":
            error = "No file selected."
        elif len(self.folders) == 0:
            error = "Empty folder list."
        elif self.parameter.startswith("-"):
            error = "Invalid input parameter."
        elif self.parameter.startswith("Please choose"):
            error = "You have to choose a parameter."
        # parse elk.in which should be equal up to a parameter for all
        # selected folders of parameter study
        try:
            self.elkInput = elk.ElkInput(path=self.folders[0], verbose=True)
            for f in self.folders:
                if not os.path.isfile(os.path.join(f, "elk.in")):
                    raise FileNotFoundError
        except FileNotFoundError:
            error = (
                "File(s) elk.in and/or INFO.OUT could not be found in one "
                "of the selected Folders."
            )
        except IndexError:
            # TODO what was going on here again??
            print("\n\n[WARNING] IndexError in batchLoadDialog\n\n")
        # return or notify user which selection is not valid
        _handleErrorsAndReturn(self, error)

    def fillParamerBox(self):
        """Populates comboBox with possible parameters from utilities dict."""
        self.comboBox.addItem("Please choose a parameter...")
        self.comboBox.setItemData(0, QtGui.QBrush(Qt.gray), Qt.TextColorRole)
        self.comboBox.addItems(dicts.PARAMETER_LIST)
        for idx in range(self.comboBox.count()):
            if self.comboBox.itemText(idx).startswith("---"):
                self.comboBox.setItemData(
                    idx, QtGui.QBrush(Qt.gray), Qt.TextColorRole
                )

    def selectFile(self):
        """Opens dialog where user can select one Elk output file."""
        self.file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select the filename that you want to batch-open",
            self.cwd,
            "Elk output files (*.out);;All files (*.*)",
            options=QtWidgets.QFileDialog.DontUseNativeDialog,
        )
        # split basename and path for later reuse
        self._folderDir = os.path.dirname(os.path.dirname(self.file))
        self.file = os.path.basename(self.file)
        # put into line edit next to button
        self.lineEdit.setText(self.file)

    def selectFolders(self):
        """Opens dialog where user can select mutliple folders to study."""
        # use path of selected file if available, cd one level back otherwise
        if self._folderDir:
            self.fdialog.setDirectory(self._folderDir)
        else:
            self.fdialog.setDirectory(os.path.split(self.cwd)[0])
        if self.fdialog.exec():
            # let user choose folders
            self.folders = self.fdialog.selectedFiles()
            # update list view next to button
            self.listWidget.addItems(self.folders)

    def removeFolders(self):
        """Removes active item on <DEL> key press when listWidget has focus."""
        folders = self.listWidget.selectedItems()
        if folders is not None:
            for item in folders:
                row = self.listWidget.row(item)
                self.listWidget.takeItem(row)


class ConvertDialog(QtWidgets.QDialog, UiInterface.Ui_ConvertDialog):
    """GUI interface to elkoa.utils.convert module.

    Attributes:
        q: wave vector in fractional coordinates.
        opticalLimit: Bool indicating if formula simplifications from optical
            limit should be applied.
        improvedRegularization: Bool indicating if converter should use the
            standard regularization w -> w+i*eta or the improved version
            w -> (w**2 + 2*i*w*eta)**1/2.
        outputFunction: User choice which conversion should be performed.
    """

    def __init__(self):
        super(ConvertDialog, self).__init__()
        self.setupUi(self)
        # attributes holding user input
        self.q = None
        self.opticalLimit = False
        self.improvedRegularization = None
        self.outputFunction = None
        # TODO
        # spoiler = Spoiler()
        # self.ConvertDialog.addWidget(spoiler)
        # connect signals and slots
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.accepted.connect(self.accepted)

    def accepted(self):
        """Processes and check user input and returns accepted values."""
        error = None
        try:
            q1 = float(self.lineEditQ1.text())
            q2 = float(self.lineEditQ2.text())
            q3 = float(self.lineEditQ3.text())
            self.q = [q1, q2, q3]
        except ValueError:
            error = "Invalid values for q-vector. Must be float."
        self.opticalLimit = bool(self.checkBoxOL.checkState())
        self.improvedRegularization = self.radioButtonImproved.isChecked()
        self.outputFunction = self.comboBox.currentText()
        self.outputFunctionIdx = self.comboBox.currentIndex()
        # construct converter instance from user input
        _handleErrorsAndReturn(self, error)

    def rejected(self):
        """Writes some info to terminal and hide dialog."""
        print("\n--- cancelled by user ---")
        self.reject()


class TensorElementsDialog(
    QtWidgets.QDialog, UiInterface.Ui_TensorElementsDialog
):
    """Dialog class for choosing tensor elements to plot.

    The user can decide which of the currently available elements should be
    plotted by clicking checkboxes. In case files for certain elements are
    missing, the associated box will be disabled.

    Attributes:
        states: Array holding the currently enabled/disabled/n.a. elements.
        boxes: Array holding all checkBox objects for convenient looping.
    """

    def __init__(self):
        super(TensorElementsDialog, self).__init__()
        # generate dialog box
        self.setupUi(self)
        # initialize class variables
        self.states = None
        self.boxes = [
            self.checkBox_11,
            self.checkBox_12,
            self.checkBox_13,
            self.checkBox_21,
            self.checkBox_22,
            self.checkBox_23,
            self.checkBox_31,
            self.checkBox_32,
            self.checkBox_33,
        ]
        # connect signals and slots
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accepted)
        self.btnDiagonalOnly.clicked.connect(self.diagonalOnly)
        self.btnAll.clicked.connect(self.all)
        self.btnNone.clicked.connect(self.none)

    def exec(self):
        """Extends QDialog's exec() with checkbox initialization."""
        self.initializeBoxStates()
        # call original method from base class QDialog
        return super(TensorElementsDialog, self).exec()

    def initializeBoxStates(self):
        """Sets checkbox check-states according to current configuration."""
        for boxID, box in enumerate(self.boxes):
            state = self.states[boxID]
            box.setCheckState(state)
            # disable box when corresponding file not in path
            if state == Qt.PartiallyChecked:
                box.setEnabled(False)
            else:
                box.setEnabled(True)

    def diagonalOnly(self):
        """Checks all diagonal elements if available, unchecks rest."""
        for boxID, box in enumerate(self.boxes):
            # leave unavailable data files as is
            if box.checkState() == Qt.PartiallyChecked:
                continue
            elif boxID in [0, 4, 8]:
                box.setCheckState(Qt.Checked)
            else:
                box.setCheckState(Qt.Unchecked)

    def all(self):
        """Checks all elements if available."""
        for boxID, box in enumerate(self.boxes):
            if box.checkState() == Qt.PartiallyChecked:
                continue
            else:
                box.setCheckState(Qt.Checked)

    def none(self):
        """Unchecks all elements if available."""
        for boxID, box in enumerate(self.boxes):
            if box.checkState() == Qt.PartiallyChecked:
                continue
            else:
                box.setCheckState(Qt.Unchecked)

    def accepted(self):
        """Updates tensor states and signals main window to update."""
        # read current states from GUI and update array of states
        for boxID, box in enumerate(self.boxes):
            self.states[boxID] = box.checkState()
        # instead of destroying the widget, hide and re-use it later via show
        self.accept()


# EOF - UiDialogs.py
