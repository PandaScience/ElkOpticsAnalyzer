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

import elkoa.gui.UiDesigner as UiDesigner
import elkoa.gui.FrameLayout as FrameLayout
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


class BatchLoadDialog(QtWidgets.QDialog, UiDesigner.Ui_BatchLoadDialog):
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
        """Checks if user choices are valid and returns to main window."""
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
        if error is None:
            self.elkInput = elk.ElkInput(path=self.folders[0])
            for f in self.folders:
                if not os.path.isfile(os.path.join(f, "elk.in")):
                    error = (
                        "File(s) elk.in and/or INFO.OUT could not be found in "
                        "of the selected Folders."
                    )
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


class ConvertDialog(QtWidgets.QDialog, UiDesigner.Ui_ConvertDialog):
    """GUI interface to elkoa.utils.convert module.

    Attributes:
        inputDict: Shortcut reference to dict from dicts.py
        q: wave vector in fractional coordinates.
        opticalLimit: Bool indicating if formula simplifications from optical
            limit should be applied.
        regularization: Version of regularization to use:
            standard regularization w -> w+i*eta or the improved version
            w -> (w**2 + 2*i*w*eta)**1/2.
        outputFunction: User choice which conversion should be performed.
    """

    def __init__(self):
        super(ConvertDialog, self).__init__()
        self.setupUi(self)
        # create collapsible reference label and spacer
        self.frameLayout = FrameLayout.FrameLayout(title="References")
        # add frame to grid at correct position
        self.gridLayout.addWidget(self.frameLayout, 4, 0, Qt.AlignLeft)
        # move reference label from grid to frame layout
        self.gridLayout.removeWidget(self.labelReferences)
        self.frameLayout.addWidget(self.labelReferences)
        # connect resize to click signal
        self.frameLayout.collapseFinished.connect(self.onRefClick)
        # resize properly
        self.onRefClick()

        # attributes holding user input
        self.inputDict = None
        self.q = None
        self.opticalLimit = False
        self.regularization = None
        self.outputFunction = None
        # TODO
        # spoiler = Spoiler()
        # self.ConvertDialog.addWidget(spoiler)
        # connect signals and slots
        self.comboBox.currentTextChanged.connect(self.handleImprovedButton)
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.accepted.connect(self.accepted)

    def exec(self):
        """Extends QDialog's exec()."""
        # set correct input field text
        inputFieldName = self.inputDict["name"]
        self.textInputField.setText(inputFieldName)
        # refill output function combo box for currently visible tab
        for i in range(self.comboBox.count()):
            self.comboBox.removeItem(0)
        for name in self.inputDict["converters"]:
            self.comboBox.addItem(name)
        outputFieldName = self.comboBox.currentText()
        self.handleImprovedButton(outputFieldName, force=True)
        return super(ConvertDialog, self).exec()

    def onRefClick(self):
        """Takes care of resizing the dialog window properly."""
        if self.frameLayout.isCollapsed:
            self.resize(self.minimumSize())
        else:
            self.resize(self.maximumSize())

    def handleImprovedButton(self, outputField, force=False):
        """Disables improved regularization option according to dict."""
        # test only if dialog is visible, not while deleting entries
        if self.isVisible() or force:
            enabled = self.inputDict["converters"][outputField]["improved"]
            self.btnImproved.setEnabled(enabled)
            self.btnConventional.setChecked(not enabled)

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
        if self.btnImproved.isChecked():
            self.regularization = "imp"
        else:
            self.regularization = "conv"
        self.outputFunction = self.comboBox.currentText()
        # construct converter instance from user input
        _handleErrorsAndReturn(self, error)

    def rejected(self):
        """Writes some info to terminal and hide dialog."""
        print("\n--- cancelled by user ---")
        self.reject()


class TensorElementsDialog(
    QtWidgets.QDialog, UiDesigner.Ui_TensorElementsDialog
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


class SaveTabDialog(QtWidgets.QDialog, UiDesigner.Ui_SaveTabDialog):
    """Dialog class for saving currently displayed tabdata to file.

    This class works as the GUI interface to the io.writeScalar and
    io.writeTensor functions.

    Attributes:
        tenElementsDialog: Dialog to choose tensor elements to be written.
        states: Output reference to chosen tensor elements.
        filename: Output reference to chosen filename.
        hartree: Output reference indicating if data should be in Hartree
            units (True) or in eV (False).
        threeColumn: Output reference indicating if data should be written in
            3-column style (True) or Elk's 2-column style (False).
        precision: Output reference to precision that should be used while
            writing data to file.
    """

    def __init__(self):
        super(SaveTabDialog, self).__init__()
        self.setupUi(self)
        self.tenElementsDialog = TensorElementsDialog()
        # output references
        self.states = None
        self.filename = None
        self.hartree = None
        self.threeColumn = None
        self.precision = None
        # connect signals and slots
        self.btnFilename.clicked.connect(self.selectFilename)
        self.btnTenElements.clicked.connect(self.tenElementsDialog.exec)
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.accepted.connect(self.accepted)

    def exec(self, states, vector):
        """Extends QDialog's exec()."""
        # disable tensor elements button for non-tensorial fields
        if states is None:
            self.btnTenElements.setEnabled(False)
            self.checkBoxVector.setEnabled(False)
        elif vector:
            # prevent user from saving vector as tensor
            self.checkBoxVector.setChecked(True)
            self.checkBoxVector.setEnabled(False)
            # disable off-diagonal elements
            for i in [1, 2, 3, 5, 6, 7]:
                states[i] = Qt.PartiallyChecked
        # link tensor states from current view to dialog's states
        self.tenElementsDialog.states = states
        return super(SaveTabDialog, self).exec()

    def selectFilename(self):
        """Opens dialog where user can select an existing filename."""
        cwd = os.getcwd()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select a filename",
            cwd,
            "All files (*.*)",
            options=QtWidgets.QFileDialog.DontUseNativeDialog,
        )
        if filename != "":
            self.lineEdit.setText(filename)

    def rejected(self):
        """Writes some info to terminal and hides dialog."""
        print("\n--- cancelled by user ---")
        self.reject()

    def accepted(self):
        """Checks if user choices are valid and returns to main window."""
        # check for valid selections and fill output references for caller
        error = None
        self.filename = self.lineEdit.text()
        if self.filename == "":
            error = "You must choose a filename."
        self.hartree = self.btnHartree.isChecked()
        self.threeColumn = self.btn3column.isChecked()
        self.precision = self.spinBox.value()
        self.states = self.tenElementsDialog.states
        vector = self.checkBoxVector
        if self.states is not None:
            if Qt.Checked not in self.states:
                error = "You must select at least one tensor/vector element."
            elif vector and "_i" not in self.filename:
                error = (
                    'Filename for vectors should contain "i" as in '
                    '"test_i_out.dat".'
                )
            elif not vector and "_ij" not in self.filename:
                error = (
                    'Filename for tensors should contain "ij" as in '
                    '"test_ij_out.dat".'
                )
        # return or notify user which selection is not valid
        _handleErrorsAndReturn(self, error)


class UnitDialog(QtWidgets.QDialog, UiDesigner.Ui_UnitDialog):
    def __init__(self):
        super(UnitDialog, self).__init__()
        self.setupUi(self)
        # output references
        self.hartree = None
        # connect signals and slots
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.accepted.connect(self.accepted)

    def rejected(self):
        """Writes some info to terminal and hides dialog."""
        print("\n--- cancelled by user ---")
        self.reject()

    def accepted(self):
        """Checks if user choices are valid and returns to main window."""
        self.hartree = self.btnHartree.isChecked()
        self.accept()


# EOF - UiDialogs.py
