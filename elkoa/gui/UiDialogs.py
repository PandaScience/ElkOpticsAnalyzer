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
import wrapt

import elkoa.gui.UiDesigner as UiDesigner
import elkoa.gui.FrameLayout as FrameLayout
from elkoa.utils import dicts, elk


@wrapt.decorator
def handleDialogErrors(wrapped, instance, args, kwargs):
    error = wrapped(*args, **kwargs)
    # return or notify user which selection is not valid
    if error is None:
        instance.accept()
    else:
        from PyQt5.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            instance,
            "Warning!",
            "<p>{err}</p> <p>Go on or cancel?</p>".format(err=error),
            QMessageBox.Retry | QMessageBox.Close,
            QMessageBox.Retry,
        )
        if reply == QMessageBox.Close:
            # click <cancel> button on behalf of user
            print("\n--- cancelled by user ---")
            instance.reject()


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

    @handleDialogErrors
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
        return error

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
        # NOTE: for preventing "hopping" references button, adjust minimum and
        # maximum height in qt-designer. currently: delta = 185px

        # attributes holding user input
        self.inputDict = None
        self.q = None
        self.regularization = None
        self.outputFunction = None
        # connect signals and slots
        self.comboBox.currentTextChanged.connect(self.deactivateFields)
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
        # round q-vector to better fit in lineEdit later
        self.q = self.q.round(6)
        # enables or disables certain fields when reasonable
        self.deactivateFields(outputFieldName, force=True)
        return super(ConvertDialog, self).exec()

    def onRefClick(self):
        """Takes care of resizing the dialog window properly."""
        if self.frameLayout.isCollapsed:
            self.resize(self.minimumSize())
        else:
            self.resize(self.maximumSize())

    def deactivateFields(self, outputField, force=False):
        """En-/Disables certain buttons and fields if reasonable (see dict)."""
        # test only if dialog is visible, not while deleting entries, b/c this
        # function is used as slot for signal 'currentTextChanged'
        if self.isVisible() or force:
            opts = self.inputDict["converters"][outputField]["opts"]
            # disable different regularization options when e.g. dividing by w
            if "noreg" in opts:
                self.btnNone.setChecked(True)
                self.btnNone.setEnabled(False)
                self.btnConventional.setEnabled(False)
                self.btnImproved.setEnabled(False)
            elif "creg" in opts:
                self.btnNone.setEnabled(False)
                self.btnImproved.setEnabled(False)
                self.btnConventional.setEnabled(True)
                self.btnConventional.setChecked(True)
            else:
                self.btnNone.setEnabled(True)
                self.btnImproved.setEnabled(True)
                self.btnConventional.setEnabled(True)
                self.btnConventional.setChecked(True)
            # disable q-vector fields if converter does not require any q
            enabled = "noq" not in opts
            self.lineEditQ1.setEnabled(enabled)
            self.lineEditQ2.setEnabled(enabled)
            self.lineEditQ3.setEnabled(enabled)
            self.btnCartesian.setEnabled(enabled)
            self.btnFractional.setEnabled(enabled)
            if enabled:
                # fill fractional coordinates of q-vector
                self.btnFractional.setChecked(True)
                self.lineEditQ1.setText(str(self.q[0]))
                self.lineEditQ2.setText(str(self.q[1]))
                self.lineEditQ3.setText(str(self.q[2]))
                # let user see beginning of longer numbers instead of end
                self.lineEditQ1.setCursorPosition(0)
                self.lineEditQ2.setCursorPosition(0)
                self.lineEditQ3.setCursorPosition(0)
            else:
                self.lineEditQ1.setText("n.a.")
                self.lineEditQ2.setText("n.a.")
                self.lineEditQ3.setText("n.a.")

    @handleDialogErrors
    def accepted(self):
        """Processes and check user input and returns accepted values."""
        self.outputFunction = self.comboBox.currentText()
        error = None
        # check only if q-vector field can be filled by user
        if self.lineEditQ1.isEnabled():
            # check for valid floats
            try:
                q1 = float(self.lineEditQ1.text())
                q2 = float(self.lineEditQ2.text())
                q3 = float(self.lineEditQ3.text())
                self.q = [q1, q2, q3]
            except ValueError:
                error = "Invalid values for q-vector. Must be float."
            # check for non-zero q if required
            opts = self.inputDict["converters"][self.outputFunction]["opts"]
            if "nzq" in opts and self.q == [0, 0, 0]:
                error = "q-vector may not be zero for this conversion!"
        # make sure to always set q=0 when edits are disabled b/c q could still
        # be set from previous conversion
        else:
            self.q = [0, 0, 0]
        # check even if radio buttons are disabled to prevent NameError for
        # regularization when main window prints converter settings
        if self.btnConventional.isChecked():
            self.regularization = "imp"
        elif self.btnImproved.isChecked():
            self.regularization = "conv"
        elif self.btnNone.isChecked():
            self.regularization = "none"
        else:
            # this should actually never happen...
            error = "Please choose a regularization!"
        return error

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
        self.states_init = None
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
        self.checkBoxVector.clicked.connect(self.onVectorToggled)

    def exec(self, states, vector):
        """Extends QDialog's exec()."""
        # keep reference to current view's states
        self.states_init = states
        # link tensor states from current view to tensor dialog's states
        self.tenElementsDialog.states = states.copy()
        # disable tensor elements button for scalar fields
        if states is None:
            self.btnTenElements.setEnabled(False)
            self.checkBoxVector.setEnabled(False)
        elif vector:
            # prevent user from saving vector as tensor
            self.checkBoxVector.setChecked(True)
            self.checkBoxVector.setEnabled(False)
        # tensor box could still be checked from last call, so query manually
        self.onVectorToggled()
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

    def onVectorToggled(self):
        """Disables off-diagonal elements when vector box is checked."""
        if self.checkBoxVector.isChecked():
            # disable off-diagonal elements
            for i in [1, 2, 3, 5, 6, 7]:
                self.tenElementsDialog.states[i] = Qt.PartiallyChecked
        else:
            # re-enable off-diagonal elements and set back to inital state
            for i in [1, 2, 3, 5, 6, 7]:
                self.tenElementsDialog.states = self.states_init.copy()

    def rejected(self):
        """Writes some info to terminal and hides dialog."""
        print("\n--- cancelled by user ---")
        self.reject()

    @handleDialogErrors
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
        vector = self.checkBoxVector.isChecked()
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
        return error


class UnitDialog(QtWidgets.QDialog, UiDesigner.Ui_UnitDialog):
    """Dialog class for choosing units when loading on-top data."""

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


class ManipulateFieldDialog(
    QtWidgets.QDialog, UiDesigner.Ui_ManipulateFieldDialog
):
    """Dialog class for modifying field data, e.g. shifting, scaling, etc.

    Attributes:
        x-shift: Value by which the originally loaded field data should be
            shifted to the right, or equivalently by which the frequencies
            should be shifted to the left.
        yexpr: numepr compatible expression the modified field values should be
            assigned to. Can take only a subset of all possible numexpr
            operators and functions because not all can be applied to complex
            valued multi-dimensional numpy arrays.
    """

    def __init__(self):
        super(ManipulateFieldDialog, self).__init__()
        self.setupUi(self)
        # output values
        self.xshift = None
        self.yexpr = None
        # connect signals and slots
        self.buttonBox.rejected.connect(self.rejected)
        self.buttonBox.accepted.connect(self.accepted)

    def exec(self, xshift):
        """Initializes x-shift value on each call to correct tabdata value."""
        self.lineEditXShift.setText(str(xshift))
        # call original method from base class QDialog
        return super(ManipulateFieldDialog, self).exec()

    def rejected(self):
        """Writes some info to terminal and hides dialog."""
        print("\n--- cancelled by user ---")
        self.reject()

    @handleDialogErrors
    def accepted(self):
        """Checks for invalid input in lineEdits."""
        error = None
        # if empty, use default values
        yexpr = self.lineEditYExpr.text()
        xshift = self.lineEditXShift.text()
        if yexpr == "":
            yexpr = "y"
        if xshift == "":
            xshift = 0
        try:
            self.xshift = float(xshift)
        except ValueError:
            error = "Invalid x-shift. Must be int or float."
        try:
            import numexpr as ne
            import numpy as np

            # use 2D array of complex floats to raise all NotImplementedErrors
            testArray = np.array([1.1, 2.2, 3.3] * 3).reshape(3, 3) + 0.5j
            ne.evaluate(yexpr, local_dict={"y": testArray, "x": testArray})
            # if no errors until now, assume valid input
            self.yexpr = yexpr
        except KeyError:
            error = (
                "In the formula field, you may only use "
                "<ul style='margin-left: -20px;'>"
                "<li> &nbsp; the symbol 'y' (for field values in a.u.)</li>"
                "<li> &nbsp; the symbol 'x' (for corresponding frequencies "
                "in eV)</li>"
                "<li> &nbsp; operators and functions supported by the numexpr "
                "<br> &nbsp; module and compatible with complex ndarrrays."
                "</li></ul>"
            )
        except TypeError:
            error = "Seems like you misspelled one of your math functions."
        except SyntaxError:
            error = (
                "There are syntax errors in your expression for y. You need "
                "to explicitly use * between factors and may not use "
                "invalid operators like =."
            )
        except NotImplementedError:
            error = (
                "<p>Sorry, seems like an operator you used in your expression "
                "is not implemented (with good reason) in numexpr.<p/>"
                "<p>Remember that you act operators on (in general) complex "
                "multi-dimensional arrays of floats. Typically, this error "
                "is raised when you try to use"
                "<ul style='margin-left: -20px;'>"
                "<li> &nbsp;logical operators &amp;, |, ~ </li>"
                "<li> &nbsp;comparison operators &lt;, &lt;=, &gt;=, &gt;</li>"
                "<li> &nbsp;a bitshift operator &lt;&lt; or &gt;&gt;</li>"
                "<li> &nbsp;the modulo operator %</li>"
                "</ul> on such a field - which does not really make sense.</p>"
            )
        return error


# EOF - UiDialogs.py
