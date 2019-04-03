# coding: utf-8
# vim: set ai ts=4 sw=4 sts=0 noet pi ci

# Copyright © 2018-2019 René Wirnata.
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

from PyQt5 import QtCore, QtGui, QtWidgets
import elkoa.gui.resources_rc  # noqa


class Ui_ElkOpticsAnalyzerMainWindow(object):
    def setupUi(self, ElkOpticsAnalyzerMainWindow):
        ElkOpticsAnalyzerMainWindow.setObjectName(
            "ElkOpticsAnalyzerMainWindow"
        )
        ElkOpticsAnalyzerMainWindow.resize(924, 724)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            ElkOpticsAnalyzerMainWindow.sizePolicy().hasHeightForWidth()
        )
        ElkOpticsAnalyzerMainWindow.setSizePolicy(sizePolicy)
        ElkOpticsAnalyzerMainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(ElkOpticsAnalyzerMainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.tabWidget.sizePolicy().hasHeightForWidth()
        )
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.start_text = QtWidgets.QLabel(self.tab)
        self.start_text.setGeometry(QtCore.QRect(70, 190, 521, 331))
        self.start_text.setWordWrap(False)
        self.start_text.setObjectName("start_text")
        self.logo_ITP = QtWidgets.QLabel(self.tab)
        self.logo_ITP.setGeometry(QtCore.QRect(600, 100, 250, 164))
        self.logo_ITP.setText("")
        self.logo_ITP.setPixmap(QtGui.QPixmap(":/logos/logos/logo_ITP.png"))
        self.logo_ITP.setScaledContents(True)
        self.logo_ITP.setObjectName("logo_ITP")
        self.logo_PS = QtWidgets.QLabel(self.tab)
        self.logo_PS.setGeometry(QtCore.QRect(50, 60, 554, 80))
        self.logo_PS.setText("")
        self.logo_PS.setPixmap(QtGui.QPixmap(":/logos/logos/logo_PS.png"))
        self.logo_PS.setScaledContents(True)
        self.logo_PS.setObjectName("logo_PS")
        self.logo_TUBAF = QtWidgets.QLabel(self.tab)
        self.logo_TUBAF.setGeometry(QtCore.QRect(620, 330, 200, 200))
        self.logo_TUBAF.setText("")
        self.logo_TUBAF.setPixmap(QtGui.QPixmap(":/logos/logos/logo_QFTM.png"))
        self.logo_TUBAF.setScaledContents(True)
        self.logo_TUBAF.setObjectName("logo_TUBAF")
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnRealPart = QtWidgets.QRadioButton(self.centralwidget)
        self.btnRealPart.setChecked(True)
        self.btnRealPart.setObjectName("btnRealPart")
        self.horizontalLayout_2.addWidget(self.btnRealPart)
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Maximum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnImaginaryPart = QtWidgets.QRadioButton(self.centralwidget)
        self.btnImaginaryPart.setObjectName("btnImaginaryPart")
        self.horizontalLayout_2.addWidget(self.btnImaginaryPart)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Maximum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btnSplitView = QtWidgets.QRadioButton(self.centralwidget)
        self.btnSplitView.setObjectName("btnSplitView")
        self.horizontalLayout_2.addWidget(self.btnSplitView)
        spacerItem2 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Maximum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btnTogether = QtWidgets.QRadioButton(self.centralwidget)
        self.btnTogether.setObjectName("btnTogether")
        self.horizontalLayout_2.addWidget(self.btnTogether)
        spacerItem3 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_2.addItem(spacerItem3)
        self.checkBoxfullRange = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxfullRange.setObjectName("checkBoxfullRange")
        self.horizontalLayout_2.addWidget(self.checkBoxfullRange)
        spacerItem4 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Maximum,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_2.addItem(spacerItem4)
        self.taskChooser = QtWidgets.QComboBox(self.centralwidget)
        self.taskChooser.setObjectName("taskChooser")
        self.taskChooser.addItem("")
        self.taskChooser.addItem("")
        self.taskChooser.addItem("")
        self.taskChooser.addItem("")
        self.taskChooser.addItem("")
        self.taskChooser.addItem("")
        self.taskChooser.addItem("")
        self.taskChooser.addItem("")
        self.horizontalLayout_2.addWidget(self.taskChooser)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        ElkOpticsAnalyzerMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ElkOpticsAnalyzerMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 924, 25))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuAdditionalData = QtWidgets.QMenu(self.menuView)
        self.menuAdditionalData.setObjectName("menuAdditionalData")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        ElkOpticsAnalyzerMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ElkOpticsAnalyzerMainWindow)
        self.statusbar.setObjectName("statusbar")
        ElkOpticsAnalyzerMainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(ElkOpticsAnalyzerMainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionVerticalSplit = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionVerticalSplit.setCheckable(False)
        self.actionVerticalSplit.setObjectName("actionVerticalSplit")
        self.actionHorizontalSplit = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionHorizontalSplit.setCheckable(False)
        self.actionHorizontalSplit.setObjectName("actionHorizontalSplit")
        self.actionSetWorkingDir = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionSetWorkingDir.setObjectName("actionSetWorkingDir")
        self.actionAbout = QtWidgets.QAction(ElkOpticsAnalyzerMainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionTensorElements = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionTensorElements.setObjectName("actionTensorElements")
        self.actionGlobalTensorSettings = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionGlobalTensorSettings.setCheckable(True)
        self.actionGlobalTensorSettings.setObjectName(
            "actionGlobalTensorSettings"
        )
        self.actionReadAdditionalData = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionReadAdditionalData.setObjectName("actionReadAdditionalData")
        self.actionRemoveAllAdditionalData = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionRemoveAllAdditionalData.setObjectName(
            "actionRemoveAllAdditionalData"
        )
        self.actionReload = QtWidgets.QAction(ElkOpticsAnalyzerMainWindow)
        self.actionReload.setObjectName("actionReload")
        self.actionBatchLoad = QtWidgets.QAction(ElkOpticsAnalyzerMainWindow)
        self.actionBatchLoad.setObjectName("actionBatchLoad")
        self.menuMenu.addAction(self.actionSetWorkingDir)
        self.menuMenu.addAction(self.actionReload)
        self.menuMenu.addAction(self.actionBatchLoad)
        self.menuMenu.addAction(self.actionQuit)
        self.menuAdditionalData.addAction(self.actionReadAdditionalData)
        self.menuAdditionalData.addAction(self.actionRemoveAllAdditionalData)
        self.menuView.addAction(self.actionVerticalSplit)
        self.menuView.addAction(self.actionHorizontalSplit)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionTensorElements)
        self.menuView.addAction(self.actionGlobalTensorSettings)
        self.menuView.addSeparator()
        self.menuView.addAction(self.menuAdditionalData.menuAction())
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(ElkOpticsAnalyzerMainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.taskChooser.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ElkOpticsAnalyzerMainWindow)

    def retranslateUi(self, ElkOpticsAnalyzerMainWindow):
        _translate = QtCore.QCoreApplication.translate
        ElkOpticsAnalyzerMainWindow.setWindowTitle(
            _translate(
                "ElkOpticsAnalyzerMainWindow", "Elk Optics Analyzer (ElkOA)"
            )
        )
        self.start_text.setText(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                '<html><head/><body><p>Hi there!<br/><br/>This is Elk Optics Analyzer (ElkOA) by R. Wirnata.</p><p>ElkOA is free software and licensed under GPLv3+. It has been <br/>written by a PhD student at the Institute for Theoretical Physics <br/>at TU Freiberg as a finger exercise during a bad cold to help <br/>analyzing Elk optics output data in a more convenient way.<br/><br/>Updates and new features can be found at:<br/><a href="https://github.com/PandaScience/ElkOA"><span style=" text-decoration: underline; color:#0000ff;">https://github.com/PandaScience/ElkOA</span></a></p><p>To start plotting your calculated data, please choose an <br/>Elk task from the bottom right menu..<br/><br/>Happy analyzing...</p></body></html>',
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab),
            _translate("ElkOpticsAnalyzerMainWindow", "Start Page"),
        )
        self.btnRealPart.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow", "Display only real parts..."
            )
        )
        self.btnRealPart.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "real part")
        )
        self.btnImaginaryPart.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Display only imaginary parts...",
            )
        )
        self.btnImaginaryPart.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "imaginar&y part")
        )
        self.btnSplitView.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Display 2 subplots according to split type (see View)...",
            )
        )
        self.btnSplitView.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "split view")
        )
        self.btnTogether.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Display real and imaginary parts in one figure...",
            )
        )
        self.btnTogether.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "to&gether")
        )
        self.checkBoxfullRange.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Display all available data instead of restricting to frequencies in [0, max]...",
            )
        )
        self.checkBoxfullRange.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "full range")
        )
        self.taskChooser.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Lists all currently available data with corresponding Elk task numbers...",
            )
        )
        self.taskChooser.setCurrentText(
            _translate(
                "ElkOpticsAnalyzerMainWindow", "Please choose an Elk task..."
            )
        )
        self.taskChooser.setItemText(
            0,
            _translate(
                "ElkOpticsAnalyzerMainWindow", "Please choose an Elk task..."
            ),
        )
        self.taskChooser.setItemText(
            1,
            _translate(
                "ElkOpticsAnalyzerMainWindow", "121 - RPA Dielectric Tensor"
            ),
        )
        self.taskChooser.setItemText(
            2,
            _translate(
                "ElkOpticsAnalyzerMainWindow", "187 - BSE Dielectric Function"
            ),
        )
        self.taskChooser.setItemText(
            3,
            _translate(
                "ElkOpticsAnalyzerMainWindow", "320 - TDDFT Dielectric Tensor"
            ),
        )
        self.taskChooser.setItemText(
            4,
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "330 - Density Response Function",
            ),
        )
        self.taskChooser.setItemText(
            5,
            _translate(
                "ElkOpticsAnalyzerMainWindow", "630 - Current Response Tensor"
            ),
        )
        self.taskChooser.setItemText(
            6,
            _translate(
                "ElkOpticsAnalyzerMainWindow", "631 - Density Response #2"
            ),
        )
        self.taskChooser.setItemText(
            7,
            _translate(
                "ElkOpticsAnalyzerMainWindow", "650 - Response Relations"
            ),
        )
        self.menuMenu.setTitle(
            _translate("ElkOpticsAnalyzerMainWindow", "&Menu")
        )
        self.menuView.setTitle(
            _translate("ElkOpticsAnalyzerMainWindow", "&View")
        )
        self.menuAdditionalData.setTitle(
            _translate("ElkOpticsAnalyzerMainWindow", "&Additional Data")
        )
        self.menuHelp.setTitle(
            _translate("ElkOpticsAnalyzerMainWindow", "&Help")
        )
        self.actionQuit.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Quit")
        )
        self.actionQuit.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Quit this great and very helpful application...",
            )
        )
        self.actionQuit.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+Q")
        )
        self.actionVerticalSplit.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Vertical Split")
        )
        self.actionVerticalSplit.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                'Switch split mode to "real -> left" - "imag -> right"...',
            )
        )
        self.actionVerticalSplit.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+V")
        )
        self.actionHorizontalSplit.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Horizontal Split")
        )
        self.actionHorizontalSplit.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                'Switch split mode to "real -> top" - "imag -> bottom"...',
            )
        )
        self.actionHorizontalSplit.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+H")
        )
        self.actionSetWorkingDir.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Set Working Directory")
        )
        self.actionSetWorkingDir.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Change current working directory...",
            )
        )
        self.actionAbout.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&About")
        )
        self.actionAbout.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Ok, this one is easy...no need to explain that, right?",
            )
        )
        self.actionTensorElements.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Tensor Elements")
        )
        self.actionTensorElements.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Open dialog to choose which tensor elements to display...",
            )
        )
        self.actionTensorElements.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+T")
        )
        self.actionGlobalTensorSettings.setText(
            _translate(
                "ElkOpticsAnalyzerMainWindow", "&Global Tensor Settings"
            )
        )
        self.actionGlobalTensorSettings.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Choose if tensor element settings should be applied also to all upcoming plots...",
            )
        )
        self.actionGlobalTensorSettings.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+G")
        )
        self.actionReadAdditionalData.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Choose Files...")
        )
        self.actionReadAdditionalData.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Open file dialog for loading e.g. experimental data...",
            )
        )
        self.actionReadAdditionalData.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+O")
        )
        self.actionRemoveAllAdditionalData.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Remove All")
        )
        self.actionRemoveAllAdditionalData.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Remove all manually added data plots from all figures...",
            )
        )
        self.actionReload.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Reload")
        )
        self.actionReload.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Reload all data from current working directory...",
            )
        )
        self.actionReload.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+R")
        )
        self.actionBatchLoad.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Batch load...")
        )
        self.actionBatchLoad.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Open dialog for choosing file, folders and parameter settings for batch loading...",
            )
        )
        self.actionBatchLoad.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+B")
        )


class Ui_TensorElementsDialog(object):
    def setupUi(self, TensorElementsDialog):
        TensorElementsDialog.setObjectName("TensorElementsDialog")
        TensorElementsDialog.resize(239, 217)
        self.horizontalLayout = QtWidgets.QHBoxLayout(TensorElementsDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(TensorElementsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth()
        )
        self.label.setSizePolicy(sizePolicy)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_33 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_33.setObjectName("checkBox_33")
        self.gridLayout.addWidget(self.checkBox_33, 2, 2, 1, 1)
        self.checkBox_32 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_32.setObjectName("checkBox_32")
        self.gridLayout.addWidget(self.checkBox_32, 2, 1, 1, 1)
        self.checkBox_22 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_22.setObjectName("checkBox_22")
        self.gridLayout.addWidget(self.checkBox_22, 1, 1, 1, 1)
        self.checkBox_31 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_31.setObjectName("checkBox_31")
        self.gridLayout.addWidget(self.checkBox_31, 2, 0, 1, 1)
        self.checkBox_23 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_23.setObjectName("checkBox_23")
        self.gridLayout.addWidget(self.checkBox_23, 1, 2, 1, 1)
        self.checkBox_13 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_13.setObjectName("checkBox_13")
        self.gridLayout.addWidget(self.checkBox_13, 0, 2, 1, 1)
        self.checkBox_21 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_21.setObjectName("checkBox_21")
        self.gridLayout.addWidget(self.checkBox_21, 1, 0, 1, 1)
        self.checkBox_11 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_11.setObjectName("checkBox_11")
        self.gridLayout.addWidget(self.checkBox_11, 0, 0, 1, 1)
        self.checkBox_12 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_12.setObjectName("checkBox_12")
        self.gridLayout.addWidget(self.checkBox_12, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.btnDiagonalOnly = QtWidgets.QPushButton(TensorElementsDialog)
        self.btnDiagonalOnly.setObjectName("btnDiagonalOnly")
        self.verticalLayout.addWidget(self.btnDiagonalOnly)
        self.buttonBox = QtWidgets.QDialogButtonBox(TensorElementsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.buttonBox.sizePolicy().hasHeightForWidth()
        )
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(TensorElementsDialog)
        QtCore.QMetaObject.connectSlotsByName(TensorElementsDialog)

    def retranslateUi(self, TensorElementsDialog):
        _translate = QtCore.QCoreApplication.translate
        TensorElementsDialog.setWindowTitle(
            _translate("TensorElementsDialog", "Tensor Elements")
        )
        self.label.setText(
            _translate(
                "TensorElementsDialog",
                "<html><head/><body><p>Choose all tensor elements<br/>"
                "to draw in plots:</p></body></html>",
            )
        )
        self.checkBox_33.setText(_translate("TensorElementsDialog", "33"))
        self.checkBox_32.setText(_translate("TensorElementsDialog", "32"))
        self.checkBox_22.setText(_translate("TensorElementsDialog", "22"))
        self.checkBox_31.setText(_translate("TensorElementsDialog", "31"))
        self.checkBox_23.setText(_translate("TensorElementsDialog", "23"))
        self.checkBox_13.setText(_translate("TensorElementsDialog", "13"))
        self.checkBox_21.setText(_translate("TensorElementsDialog", "21"))
        self.checkBox_11.setText(_translate("TensorElementsDialog", "11"))
        self.checkBox_12.setText(_translate("TensorElementsDialog", "12"))
        self.btnDiagonalOnly.setText(
            _translate("TensorElementsDialog", "check only diagonal")
        )


class Ui_BatchLoadDialog(object):
    def setupUi(self, BatchLoadDialog):
        BatchLoadDialog.setObjectName("BatchLoadDialog")
        BatchLoadDialog.resize(466, 235)
        self.horizontalLayout = QtWidgets.QHBoxLayout(BatchLoadDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelHeader = QtWidgets.QLabel(BatchLoadDialog)
        self.labelHeader.setObjectName("labelHeader")
        self.verticalLayout.addWidget(self.labelHeader)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(BatchLoadDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.listWidget = QtWidgets.QListWidget(BatchLoadDialog)
        self.listWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 2, 1, 1, 1)
        self.labelFolders = QtWidgets.QLabel(BatchLoadDialog)
        self.labelFolders.setObjectName("labelFolders")
        self.gridLayout.addWidget(self.labelFolders, 2, 0, 1, 1)
        self.labelFile = QtWidgets.QLabel(BatchLoadDialog)
        self.labelFile.setObjectName("labelFile")
        self.gridLayout.addWidget(self.labelFile, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(BatchLoadDialog)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 3, 1, 1, 1)
        self.btnFolderOpen = QtWidgets.QToolButton(BatchLoadDialog)
        self.btnFolderOpen.setObjectName("btnFolderOpen")
        self.gridLayout.addWidget(self.btnFolderOpen, 2, 2, 1, 1)
        self.labelParameter = QtWidgets.QLabel(BatchLoadDialog)
        self.labelParameter.setObjectName("labelParameter")
        self.gridLayout.addWidget(self.labelParameter, 3, 0, 1, 1)
        self.btnFileOpen = QtWidgets.QToolButton(BatchLoadDialog)
        self.btnFileOpen.setObjectName("btnFileOpen")
        self.gridLayout.addWidget(self.btnFileOpen, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(BatchLoadDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.buttonBox.sizePolicy().hasHeightForWidth()
        )
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(BatchLoadDialog)
        QtCore.QMetaObject.connectSlotsByName(BatchLoadDialog)

    def retranslateUi(self, BatchLoadDialog):
        _translate = QtCore.QCoreApplication.translate
        BatchLoadDialog.setWindowTitle(
            _translate("BatchLoadDialog", "Batch Load")
        )
        self.labelHeader.setText(
            _translate("BatchLoadDialog", "Please choose...")
        )
        self.labelFolders.setText(_translate("BatchLoadDialog", "Folders"))
        self.labelFile.setText(_translate("BatchLoadDialog", "File"))
        self.btnFolderOpen.setText(_translate("BatchLoadDialog", "..."))
        self.labelParameter.setText(_translate("BatchLoadDialog", "Parameter"))
        self.btnFileOpen.setText(_translate("BatchLoadDialog", "..."))
