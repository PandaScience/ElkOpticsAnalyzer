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
        ElkOpticsAnalyzerMainWindow.resize(920, 700)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            ElkOpticsAnalyzerMainWindow.sizePolicy().hasHeightForWidth()
        )
        ElkOpticsAnalyzerMainWindow.setSizePolicy(sizePolicy)
        ElkOpticsAnalyzerMainWindow.setMinimumSize(QtCore.QSize(920, 700))
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
        self.logo_ITP.setGeometry(QtCore.QRect(600, 80, 250, 164))
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
        self.logo_TUBAF.setGeometry(QtCore.QRect(620, 310, 200, 200))
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
        self.horizontalLayout_2.addWidget(self.taskChooser)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        ElkOpticsAnalyzerMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ElkOpticsAnalyzerMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 920, 25))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuAdditionalData = QtWidgets.QMenu(self.menuMenu)
        self.menuAdditionalData.setObjectName("menuAdditionalData")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuLegendPlacement = QtWidgets.QMenu(self.menuView)
        self.menuLegendPlacement.setObjectName("menuLegendPlacement")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuConvert = QtWidgets.QMenu(self.menubar)
        self.menuConvert.setObjectName("menuConvert")
        ElkOpticsAnalyzerMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ElkOpticsAnalyzerMainWindow)
        self.statusbar.setObjectName("statusbar")
        ElkOpticsAnalyzerMainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(ElkOpticsAnalyzerMainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionVerticalSplit = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionVerticalSplit.setCheckable(True)
        self.actionVerticalSplit.setChecked(True)
        self.actionVerticalSplit.setObjectName("actionVerticalSplit")
        self.actionHorizontalSplit = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionHorizontalSplit.setCheckable(True)
        self.actionHorizontalSplit.setChecked(False)
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
        self.actionReload = QtWidgets.QAction(ElkOpticsAnalyzerMainWindow)
        self.actionReload.setObjectName("actionReload")
        self.actionBatchLoad = QtWidgets.QAction(ElkOpticsAnalyzerMainWindow)
        self.actionBatchLoad.setObjectName("actionBatchLoad")
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
        self.actionResponseRelations = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionResponseRelations.setObjectName("actionResponseRelations")
        self.actionRefractiveIndex = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionRefractiveIndex.setObjectName("actionRefractiveIndex")
        self.actionIndexEllipsoid = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionIndexEllipsoid.setObjectName("actionIndexEllipsoid")
        self.actionSaveTabAs = QtWidgets.QAction(ElkOpticsAnalyzerMainWindow)
        self.actionSaveTabAs.setObjectName("actionSaveTabAs")
        self.actionLegendBest = QtWidgets.QAction(ElkOpticsAnalyzerMainWindow)
        self.actionLegendBest.setCheckable(True)
        self.actionLegendBest.setChecked(True)
        self.actionLegendBest.setObjectName("actionLegendBest")
        self.actionLegendUpperRight = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionLegendUpperRight.setCheckable(True)
        self.actionLegendUpperRight.setObjectName("actionLegendUpperRight")
        self.actionLegendUpperLeft = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionLegendUpperLeft.setCheckable(True)
        self.actionLegendUpperLeft.setObjectName("actionLegendUpperLeft")
        self.actionLegendLowerLeft = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionLegendLowerLeft.setCheckable(True)
        self.actionLegendLowerLeft.setObjectName("actionLegendLowerLeft")
        self.actionLegendLowerRight = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionLegendLowerRight.setCheckable(True)
        self.actionLegendLowerRight.setObjectName("actionLegendLowerRight")
        self.actionLegendRight = QtWidgets.QAction(ElkOpticsAnalyzerMainWindow)
        self.actionLegendRight.setCheckable(True)
        self.actionLegendRight.setObjectName("actionLegendRight")
        self.actionLegendCenterLeft = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionLegendCenterLeft.setCheckable(True)
        self.actionLegendCenterLeft.setObjectName("actionLegendCenterLeft")
        self.actionLegendCenterRight = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionLegendCenterRight.setCheckable(True)
        self.actionLegendCenterRight.setObjectName("actionLegendCenterRight")
        self.actionLegendLowerCenter = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionLegendLowerCenter.setCheckable(True)
        self.actionLegendLowerCenter.setObjectName("actionLegendLowerCenter")
        self.actionLegendUpperCenter = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionLegendUpperCenter.setCheckable(True)
        self.actionLegendUpperCenter.setObjectName("actionLegendUpperCenter")
        self.actionLegendCenter = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionLegendCenter.setCheckable(True)
        self.actionLegendCenter.setObjectName("actionLegendCenter")
        self.actionRemoveADFromTab = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionRemoveADFromTab.setObjectName("actionRemoveADFromTab")
        self.actionRemoveADFromTask = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionRemoveADFromTask.setObjectName("actionRemoveADFromTask")
        self.actionShowAdditionalData = QtWidgets.QAction(
            ElkOpticsAnalyzerMainWindow
        )
        self.actionShowAdditionalData.setCheckable(True)
        self.actionShowAdditionalData.setChecked(True)
        self.actionShowAdditionalData.setObjectName("actionShowAdditionalData")
        self.menuAdditionalData.addAction(self.actionReadAdditionalData)
        self.menuAdditionalData.addAction(self.actionRemoveADFromTab)
        self.menuAdditionalData.addAction(self.actionRemoveADFromTask)
        self.menuAdditionalData.addAction(self.actionRemoveAllAdditionalData)
        self.menuMenu.addAction(self.actionSetWorkingDir)
        self.menuMenu.addAction(self.actionReload)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.menuAdditionalData.menuAction())
        self.menuMenu.addAction(self.actionBatchLoad)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionSaveTabAs)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionQuit)
        self.menuLegendPlacement.addAction(self.actionLegendBest)
        self.menuLegendPlacement.addAction(self.actionLegendUpperRight)
        self.menuLegendPlacement.addAction(self.actionLegendUpperLeft)
        self.menuLegendPlacement.addAction(self.actionLegendLowerLeft)
        self.menuLegendPlacement.addAction(self.actionLegendLowerRight)
        self.menuLegendPlacement.addAction(self.actionLegendRight)
        self.menuLegendPlacement.addAction(self.actionLegendCenterLeft)
        self.menuLegendPlacement.addAction(self.actionLegendCenterRight)
        self.menuLegendPlacement.addAction(self.actionLegendLowerCenter)
        self.menuLegendPlacement.addAction(self.actionLegendUpperCenter)
        self.menuLegendPlacement.addAction(self.actionLegendCenter)
        self.menuView.addAction(self.actionVerticalSplit)
        self.menuView.addAction(self.actionHorizontalSplit)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionTensorElements)
        self.menuView.addAction(self.actionGlobalTensorSettings)
        self.menuView.addSeparator()
        self.menuView.addAction(self.menuLegendPlacement.menuAction())
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionShowAdditionalData)
        self.menuHelp.addAction(self.actionAbout)
        self.menuConvert.addAction(self.actionResponseRelations)
        self.menuConvert.addAction(self.actionRefractiveIndex)
        self.menuConvert.addAction(self.actionIndexEllipsoid)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuConvert.menuAction())
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
                '<html><head/><body><p>Hi there!<br/><br/>This is Elk Optics Analyzer (ElkOA) by R. Wirnata.</p><p>ElkOA is free software and licensed under GPLv3+. It has been <br/>started by a PhD student at the Institute for Theoretical Physics <br/>at TU Freiberg as a finger exercise during a bad cold to help <br/>analyzing Elk optics output data in a more convenient way.<br/><br/>Updates and new features can be found at:<br/><a href="https://github.com/PandaScience/ElkOA"><span style=" text-decoration: underline; color:#0000ff;">https://github.com/PandaScience/ElkOA</span></a></p><p>To start plotting your calculated data, please choose an <br/>Elk task from the bottom right menu..<br/><br/>Happy analyzing...</p></body></html>',
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
                "ElkOpticsAnalyzerMainWindow", "121 - RPA Dielectric Tensor  "
            ),
        )
        self.taskChooser.setItemText(
            2,
            _translate(
                "ElkOpticsAnalyzerMainWindow", "187 - BSE Dielectric Tensor  "
            ),
        )
        self.taskChooser.setItemText(
            3,
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "320/v4 - TDDFT Dielectric Function  ",
            ),
        )
        self.taskChooser.setItemText(
            4,
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "320/v5 - TDDFT Dielectric Tensor  ",
            ),
        )
        self.taskChooser.setItemText(
            5,
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "330 - Density Response Function  ",
            ),
        )
        self.menuMenu.setTitle(
            _translate("ElkOpticsAnalyzerMainWindow", "&File")
        )
        self.menuAdditionalData.setTitle(
            _translate("ElkOpticsAnalyzerMainWindow", "&Plot On Top")
        )
        self.menuView.setTitle(
            _translate("ElkOpticsAnalyzerMainWindow", "&View")
        )
        self.menuLegendPlacement.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Set where legends should be drawn in plots...",
            )
        )
        self.menuLegendPlacement.setTitle(
            _translate("ElkOpticsAnalyzerMainWindow", "Legend Placement")
        )
        self.menuHelp.setTitle(
            _translate("ElkOpticsAnalyzerMainWindow", "&Help")
        )
        self.menuConvert.setTitle(
            _translate("ElkOpticsAnalyzerMainWindow", "&Convert")
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
            _translate(
                "ElkOpticsAnalyzerMainWindow", "&Change Working Directory"
            )
        )
        self.actionSetWorkingDir.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Change current working directory...",
            )
        )
        self.actionSetWorkingDir.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+D")
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
            _translate("ElkOpticsAnalyzerMainWindow", "&Batch Load...")
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
        self.actionReadAdditionalData.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Choose Files...")
        )
        self.actionReadAdditionalData.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Open dialog to load e.g. experimental data...",
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
                "Remove all additional data plots from all figures...",
            )
        )
        self.actionResponseRelations.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "&Response Relations...")
        )
        self.actionResponseRelations.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+C")
        )
        self.actionRefractiveIndex.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "Refractive &Index...")
        )
        self.actionRefractiveIndex.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+I")
        )
        self.actionIndexEllipsoid.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "Index &Ellipsoid")
        )
        self.actionIndexEllipsoid.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+E")
        )
        self.actionSaveTabAs.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "Save Tab As...")
        )
        self.actionSaveTabAs.setStatusTip(
            _translate(
                "ElkOpticsAnalyzerMainWindow",
                "Save currently visible data to file...",
            )
        )
        self.actionSaveTabAs.setShortcut(
            _translate("ElkOpticsAnalyzerMainWindow", "Ctrl+S")
        )
        self.actionLegendBest.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "best")
        )
        self.actionLegendUpperRight.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "upper right")
        )
        self.actionLegendUpperLeft.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "upper left")
        )
        self.actionLegendLowerLeft.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "lower left")
        )
        self.actionLegendLowerRight.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "lower right")
        )
        self.actionLegendRight.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "right")
        )
        self.actionLegendCenterLeft.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "center left")
        )
        self.actionLegendCenterRight.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "center right")
        )
        self.actionLegendLowerCenter.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "lower center")
        )
        self.actionLegendUpperCenter.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "upper center")
        )
        self.actionLegendCenter.setText(
            _translate("ElkOpticsAnalyzerMainWindow", "center")
        )
        self.actionRemoveADFromTab.setText(
            _translate(
                "ElkOpticsAnalyzerMainWindow", "Remove From Current Tab"
            )
        )
        self.actionRemoveADFromTask.setText(
            _translate(
                "ElkOpticsAnalyzerMainWindow", "Remove From Current Task"
            )
        )
        self.actionShowAdditionalData.setText(
            _translate("ElkOpticsAnalyzerMainWindow", 'Display "on-top data"')
        )


class Ui_TensorElementsDialog(object):
    def setupUi(self, TensorElementsDialog):
        TensorElementsDialog.setObjectName("TensorElementsDialog")
        TensorElementsDialog.resize(218, 215)
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
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_23 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_23.setObjectName("checkBox_23")
        self.gridLayout.addWidget(self.checkBox_23, 1, 2, 1, 1)
        self.checkBox_11 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_11.setObjectName("checkBox_11")
        self.gridLayout.addWidget(self.checkBox_11, 0, 0, 1, 1)
        self.checkBox_22 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_22.setObjectName("checkBox_22")
        self.gridLayout.addWidget(self.checkBox_22, 1, 1, 1, 1)
        self.checkBox_12 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_12.setObjectName("checkBox_12")
        self.gridLayout.addWidget(self.checkBox_12, 0, 1, 1, 1)
        self.checkBox_33 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_33.setObjectName("checkBox_33")
        self.gridLayout.addWidget(self.checkBox_33, 2, 2, 1, 1)
        self.checkBox_21 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_21.setObjectName("checkBox_21")
        self.gridLayout.addWidget(self.checkBox_21, 1, 0, 1, 1)
        self.checkBox_32 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_32.setObjectName("checkBox_32")
        self.gridLayout.addWidget(self.checkBox_32, 2, 1, 1, 1)
        self.checkBox_31 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_31.setObjectName("checkBox_31")
        self.gridLayout.addWidget(self.checkBox_31, 2, 0, 1, 1)
        self.checkBox_13 = QtWidgets.QCheckBox(TensorElementsDialog)
        self.checkBox_13.setObjectName("checkBox_13")
        self.gridLayout.addWidget(self.checkBox_13, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnNone = QtWidgets.QToolButton(TensorElementsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnNone.sizePolicy().hasHeightForWidth()
        )
        self.btnNone.setSizePolicy(sizePolicy)
        self.btnNone.setObjectName("btnNone")
        self.horizontalLayout_2.addWidget(self.btnNone)
        self.btnDiagonalOnly = QtWidgets.QPushButton(TensorElementsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnDiagonalOnly.sizePolicy().hasHeightForWidth()
        )
        self.btnDiagonalOnly.setSizePolicy(sizePolicy)
        self.btnDiagonalOnly.setObjectName("btnDiagonalOnly")
        self.horizontalLayout_2.addWidget(self.btnDiagonalOnly)
        self.btnAll = QtWidgets.QToolButton(TensorElementsDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnAll.sizePolicy().hasHeightForWidth()
        )
        self.btnAll.setSizePolicy(sizePolicy)
        self.btnAll.setObjectName("btnAll")
        self.horizontalLayout_2.addWidget(self.btnAll)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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
            _translate("TensorElementsDialog", "Choose Tensor Elements")
        )
        self.label.setText(
            _translate(
                "TensorElementsDialog",
                '<html><head/><body><p><span style=" font-size:10pt; font-weight:600;">Note: </span><span style=" font-size:10pt;">For vectors ∈ R</span><span style=" font-size:10pt; font-weight:600; vertical-align:super;">3 </span><span style=" font-size:10pt;">use<br/>1 → 11, 2 → 22, 3 → 33</span></p></body></html>',
            )
        )
        self.checkBox_23.setText(_translate("TensorElementsDialog", "23"))
        self.checkBox_11.setText(_translate("TensorElementsDialog", "11"))
        self.checkBox_22.setText(_translate("TensorElementsDialog", "22"))
        self.checkBox_12.setText(_translate("TensorElementsDialog", "12"))
        self.checkBox_33.setText(_translate("TensorElementsDialog", "33"))
        self.checkBox_21.setText(_translate("TensorElementsDialog", "21"))
        self.checkBox_32.setText(_translate("TensorElementsDialog", "32"))
        self.checkBox_31.setText(_translate("TensorElementsDialog", "31"))
        self.checkBox_13.setText(_translate("TensorElementsDialog", "13"))
        self.btnNone.setText(_translate("TensorElementsDialog", "none"))
        self.btnDiagonalOnly.setText(
            _translate("TensorElementsDialog", "diagonal")
        )
        self.btnAll.setText(_translate("TensorElementsDialog", "all"))


class Ui_BatchLoadDialog(object):
    def setupUi(self, BatchLoadDialog):
        BatchLoadDialog.setObjectName("BatchLoadDialog")
        BatchLoadDialog.resize(466, 338)
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
        self.label = QtWidgets.QLabel(BatchLoadDialog)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
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
        self.label.setText(
            _translate(
                "BatchLoadDialog",
                '<html><head/><body><p><span style=" font-size:8pt; font-weight:600;">NOTE:</span><span style=" font-size:8pt;"> All selected calculations must have at least the same number of frequencies in elk.in → wplot → nwplot!</span></p></body></html>',
            )
        )


class Ui_ConvertDialog(object):
    def setupUi(self, ConvertDialog):
        ConvertDialog.setObjectName("ConvertDialog")
        ConvertDialog.resize(475, 470)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            ConvertDialog.sizePolicy().hasHeightForWidth()
        )
        ConvertDialog.setSizePolicy(sizePolicy)
        ConvertDialog.setMinimumSize(QtCore.QSize(475, 285))
        ConvertDialog.setMaximumSize(QtCore.QSize(475, 470))
        self.gridLayout = QtWidgets.QGridLayout(ConvertDialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelInputField = QtWidgets.QLabel(ConvertDialog)
        self.labelInputField.setObjectName("labelInputField")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.labelInputField
        )
        self.textInputField = QtWidgets.QLabel(ConvertDialog)
        self.textInputField.setObjectName("textInputField")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.textInputField
        )
        self.labelOutputField = QtWidgets.QLabel(ConvertDialog)
        self.labelOutputField.setObjectName("labelOutputField")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.labelOutputField
        )
        self.comboBox = QtWidgets.QComboBox(ConvertDialog)
        self.comboBox.setObjectName("comboBox")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.comboBox
        )
        self.labelOpticalLimit_2 = QtWidgets.QLabel(ConvertDialog)
        self.labelOpticalLimit_2.setObjectName("labelOpticalLimit_2")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.labelOpticalLimit_2
        )
        self.labelRegularization = QtWidgets.QLabel(ConvertDialog)
        self.labelRegularization.setObjectName("labelRegularization")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.labelRegularization
        )
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnConventional = QtWidgets.QRadioButton(ConvertDialog)
        self.btnConventional.setText("")
        self.btnConventional.setChecked(True)
        self.btnConventional.setObjectName("btnConventional")
        self.horizontalLayout_4.addWidget(self.btnConventional)
        self.labelConventional = QtWidgets.QLabel(ConvertDialog)
        self.labelConventional.setObjectName("labelConventional")
        self.horizontalLayout_4.addWidget(self.labelConventional)
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_4.addItem(spacerItem1)
        self.formLayout.setLayout(
            3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4
        )
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnImproved = QtWidgets.QRadioButton(ConvertDialog)
        self.btnImproved.setText("")
        self.btnImproved.setObjectName("btnImproved")
        self.horizontalLayout.addWidget(self.btnImproved)
        self.labelImproved = QtWidgets.QLabel(ConvertDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.labelImproved.sizePolicy().hasHeightForWidth()
        )
        self.labelImproved.setSizePolicy(sizePolicy)
        self.labelImproved.setTextFormat(QtCore.Qt.RichText)
        self.labelImproved.setObjectName("labelImproved")
        self.horizontalLayout.addWidget(self.labelImproved)
        spacerItem2 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem2)
        self.labelRefImproved = QtWidgets.QLabel(ConvertDialog)
        self.labelRefImproved.setObjectName("labelRefImproved")
        self.horizontalLayout.addWidget(self.labelRefImproved)
        self.formLayout.setLayout(
            4, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout
        )
        self.labelQVector = QtWidgets.QLabel(ConvertDialog)
        self.labelQVector.setObjectName("labelQVector")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.LabelRole, self.labelQVector
        )
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEditQ1 = QtWidgets.QLineEdit(ConvertDialog)
        self.lineEditQ1.setObjectName("lineEditQ1")
        self.horizontalLayout_2.addWidget(self.lineEditQ1)
        self.labelB1 = QtWidgets.QLabel(ConvertDialog)
        self.labelB1.setObjectName("labelB1")
        self.horizontalLayout_2.addWidget(self.labelB1)
        self.lineEditQ2 = QtWidgets.QLineEdit(ConvertDialog)
        self.lineEditQ2.setObjectName("lineEditQ2")
        self.horizontalLayout_2.addWidget(self.lineEditQ2)
        self.labelB2 = QtWidgets.QLabel(ConvertDialog)
        self.labelB2.setObjectName("labelB2")
        self.horizontalLayout_2.addWidget(self.labelB2)
        self.lineEditQ3 = QtWidgets.QLineEdit(ConvertDialog)
        self.lineEditQ3.setObjectName("lineEditQ3")
        self.horizontalLayout_2.addWidget(self.lineEditQ3)
        self.labelB3 = QtWidgets.QLabel(ConvertDialog)
        self.labelB3.setObjectName("labelB3")
        self.horizontalLayout_2.addWidget(self.labelB3)
        self.formLayout.setLayout(
            5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2
        )
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBoxOL = QtWidgets.QCheckBox(ConvertDialog)
        self.checkBoxOL.setText("")
        self.checkBoxOL.setObjectName("checkBoxOL")
        self.horizontalLayout_3.addWidget(self.checkBoxOL)
        self.labelOpticalLimit = QtWidgets.QLabel(ConvertDialog)
        self.labelOpticalLimit.setObjectName("labelOpticalLimit")
        self.horizontalLayout_3.addWidget(self.labelOpticalLimit)
        spacerItem3 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_3.addItem(spacerItem3)
        self.labelRef_2 = QtWidgets.QLabel(ConvertDialog)
        self.labelRef_2.setObjectName("labelRef_2")
        self.horizontalLayout_3.addWidget(self.labelRef_2)
        self.formLayout.setLayout(
            2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3
        )
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConvertDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.buttonBox.sizePolicy().hasHeightForWidth()
        )
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 1)
        self.labelReferences = QtWidgets.QLabel(ConvertDialog)
        self.labelReferences.setTextFormat(QtCore.Qt.RichText)
        self.labelReferences.setObjectName("labelReferences")
        self.gridLayout.addWidget(self.labelReferences, 4, 0, 1, 1)

        self.retranslateUi(ConvertDialog)
        QtCore.QMetaObject.connectSlotsByName(ConvertDialog)

    def retranslateUi(self, ConvertDialog):
        _translate = QtCore.QCoreApplication.translate
        ConvertDialog.setWindowTitle(_translate("ConvertDialog", "Convert"))
        self.labelInputField.setText(
            _translate("ConvertDialog", "input field")
        )
        self.textInputField.setText(_translate("ConvertDialog", "dummy"))
        self.labelOutputField.setText(
            _translate(
                "ConvertDialog",
                '<html><head/><body><p>output field <span style=" font-size:9pt;">[1]</span></p></body></html>',
            )
        )
        self.labelOpticalLimit_2.setText(
            _translate("ConvertDialog", "optical limit")
        )
        self.labelRegularization.setText(
            _translate("ConvertDialog", "regularization")
        )
        self.labelConventional.setText(
            _translate("ConvertDialog", "ω → ω + iη")
        )
        self.labelImproved.setText(
            _translate(
                "ConvertDialog",
                '<html><head/><body><p>ω → (ω<span style=" vertical-align:super;">2</span>+2iωη)<span style=" vertical-align:super;">1/2</span></p></body></html>',
            )
        )
        self.labelRefImproved.setText(
            _translate(
                "ConvertDialog",
                '<html><head/><body><p><span style=" font-size:9pt;">[3]</span></p></body></html>',
            )
        )
        self.labelQVector.setText(_translate("ConvertDialog", "q-vector"))
        self.lineEditQ1.setText(_translate("ConvertDialog", "0.00"))
        self.labelB1.setText(
            _translate(
                "ConvertDialog",
                '<html><head/><body><p><span style=" font-weight:600;">b</span><span style=" font-weight:600; vertical-align:sub;">1 </span>+</p></body></html>',
            )
        )
        self.lineEditQ2.setText(_translate("ConvertDialog", "0.00"))
        self.labelB2.setText(
            _translate(
                "ConvertDialog",
                '<html><head/><body><p><span style=" font-weight:600;">b</span><span style=" font-weight:600; vertical-align:sub;">2 </span>+</p></body></html>',
            )
        )
        self.lineEditQ3.setText(_translate("ConvertDialog", "0.00"))
        self.labelB3.setText(
            _translate(
                "ConvertDialog",
                '<html><head/><body><p><span style=" font-weight:600;">b</span><span style=" font-weight:600; vertical-align:sub;">3</span></p></body></html>',
            )
        )
        self.labelOpticalLimit.setText(
            _translate(
                "ConvertDialog",
                '<html><head/><body><p>(assume <span style=" font-weight:600;">q</span> → <span style=" font-weight:600;">0</span> for σ)</p></body></html>',
            )
        )
        self.labelRef_2.setText(
            _translate(
                "ConvertDialog",
                '<html><head/><body><p><span style=" font-size:9pt;">[2]</span></p></body></html>',
            )
        )
        self.labelReferences.setText(
            _translate(
                "ConvertDialog",
                '<html><head/><body><p><span style=" font-size:9pt;">[1] Universal Response Relations according to<br/>Starke/Schober: </span><a href="https://doi.org/10.1016/j.photonics.2015.02.001"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;">J.Photonics </span></a><a href="https://doi.org/10.1016/j.photonics.2015.02.001"><span style=" font-size:9pt; font-weight:600; text-decoration: underline; color:#0000ff;">14</span></a><a href="https://doi.org/10.1016/j.photonics.2015.02.001"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;"> (2015)</span></a><span style=" font-size:9pt;">, § 2,4,7 <br/>Starke/Schober: </span><a href="https://doi.org/10.1016/j.ijleo.2017.03.088"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;">Optik </span></a><a href="https://doi.org/10.1016/j.ijleo.2017.03.088"><span style=" font-size:9pt; font-weight:600; text-decoration: underline; color:#0000ff;">140</span></a><a href="https://doi.org/10.1016/j.ijleo.2017.03.088"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;">, (2017)</span></a><span style=" font-size:9pt;">, § 2, 3</span><a href="https://doi.org/10.1016/j.ijleo.2017.03.088"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;"><br/></span></a><span style=" font-size:9pt;">Starke/Schober: </span><a href="https://arxiv.org/abs/1606.00012"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;">arXiv:1606.00012</span></a><span style=" font-size:9pt;">, App. C<br/><br/>[2] For detailed implications, see<br/>Starke et al.: </span><a href="https://arxiv.org/abs/1708.06330"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;">arXiv:1708.06330</span></a><span style=" font-size:9pt;"><br/><br/>[3] Improved version with no smearing at ω = 0 according to<br/>Sangalli et al.: </span><a href="https://doi.org/10.1103/PhysRevB.95.155203"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;">PRB </span></a><a href="https://doi.org/10.1103/PhysRevB.95.155203"><span style=" font-size:9pt; font-weight:600; text-decoration: underline; color:#0000ff;">95</span></a><a href="https://doi.org/10.1103/PhysRevB.95.155203"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;">, 155203 (2017)</span></a><span style=" font-size:9pt;">, § III.B <br/>(originally by Cazzaniga et al.: </span><a href="https://doi.org/10.1103/PhysRevB.82.035104"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;">PRB </span></a><a href="https://doi.org/10.1103/PhysRevB.82.035104"><span style=" font-size:9pt; font-weight:600; text-decoration: underline; color:#0000ff;">82</span></a><a href="https://doi.org/10.1103/PhysRevB.82.035104"><span style=" font-size:9pt; text-decoration: underline; color:#0000ff;">, 035104 (2010)</span></a><span style=" font-size:9pt;">)</span></p></body></html>',
            )
        )


class CollapsibleDialog(QtWidgets.QDialog):
    """A dialog to which collapsible sections can be added;
       subclass and reimplement define_sections() to define sections and
       add them as (title, widget) tuples to self.sections
    """

    def __init__(self):
        super().__init__()
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderHidden(True)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)
        self.tree.setIndentation(0)

        self.sections = []
        self.define_sections()
        self.add_sections()

    def add_sections(self):
        """adds a collapsible sections for every
        (title, widget) tuple in self.sections
        """
        for (title, widget) in self.sections:
            button1 = self.add_button(title)
            section1 = self.add_widget(button1, widget)
            button1.addChild(section1)

    def define_sections(self):
        """reimplement this to define all your sections
        and add them as (title, widget) tuples to self.sections
        """
        widget = QtWidgets.QFrame(self.tree)
        layout = QtWidgets.QHBoxLayout(widget)
        layout.addWidget(QtWidgets.QLabel("Bla"))
        layout.addWidget(QtWidgets.QLabel("Blubb"))
        title = "Section 1"
        self.sections.append((title, widget))

    def add_button(self, title):
        """creates a QTreeWidgetItem containing a button
        to expand or collapse its section
        """
        item = QtWidgets.QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(
            item, 0, QtWidgets.SectionExpandButton(item, text=title)
        )
        return item

    def add_widget(self, button, widget):
        """creates a QWidgetItem containing the widget,
        as child of the button-QWidgetItem
        """
        section = QtWidgets.QTreeWidgetItem(button)
        section.setDisabled(True)
        self.tree.setItemWidget(section, 0, widget)
        return section


class Ui_SaveTabDialog(object):
    def setupUi(self, SaveTabDialog):
        SaveTabDialog.setObjectName("SaveTabDialog")
        SaveTabDialog.resize(359, 327)
        self.gridLayout = QtWidgets.QGridLayout(SaveTabDialog)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 1)
        self.labelNote = QtWidgets.QLabel(SaveTabDialog)
        self.labelNote.setWordWrap(True)
        self.labelNote.setObjectName("labelNote")
        self.gridLayout.addWidget(self.labelNote, 8, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(SaveTabDialog)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 1)
        self.gridLayoutFilename = QtWidgets.QGridLayout()
        self.gridLayoutFilename.setObjectName("gridLayoutFilename")
        self.lineEdit = QtWidgets.QLineEdit(SaveTabDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayoutFilename.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelFilename = QtWidgets.QLabel(SaveTabDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.labelFilename.sizePolicy().hasHeightForWidth()
        )
        self.labelFilename.setSizePolicy(sizePolicy)
        self.labelFilename.setObjectName("labelFilename")
        self.horizontalLayout_4.addWidget(self.labelFilename)
        self.btnFilename = QtWidgets.QToolButton(SaveTabDialog)
        self.btnFilename.setObjectName("btnFilename")
        self.horizontalLayout_4.addWidget(self.btnFilename)
        spacerItem2 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontalLayout_4.addItem(spacerItem2)
        self.checkBoxVector = QtWidgets.QCheckBox(SaveTabDialog)
        self.checkBoxVector.setObjectName("checkBoxVector")
        self.horizontalLayout_4.addWidget(self.checkBoxVector)
        self.gridLayoutFilename.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.btnTenElements = QtWidgets.QToolButton(SaveTabDialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnTenElements.sizePolicy().hasHeightForWidth()
        )
        self.btnTenElements.setSizePolicy(sizePolicy)
        self.btnTenElements.setObjectName("btnTenElements")
        self.gridLayoutFilename.addWidget(self.btnTenElements, 0, 1, 2, 1)
        self.gridLayout.addLayout(self.gridLayoutFilename, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.gridLayout.addItem(spacerItem3, 9, 0, 1, 1)
        self.gridLayoutSettings = QtWidgets.QGridLayout()
        self.gridLayoutSettings.setObjectName("gridLayoutSettings")
        spacerItem4 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.gridLayoutSettings.addItem(spacerItem4, 2, 1, 1, 1)
        self.labelUnit = QtWidgets.QLabel(SaveTabDialog)
        self.labelUnit.setObjectName("labelUnit")
        self.gridLayoutSettings.addWidget(self.labelUnit, 1, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(SaveTabDialog)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(15)
        self.spinBox.setProperty("value", 8)
        self.spinBox.setObjectName("spinBox")
        self.gridLayoutSettings.addWidget(self.spinBox, 2, 4, 1, 1)
        self.labelPrecision = QtWidgets.QLabel(SaveTabDialog)
        self.labelPrecision.setObjectName("labelPrecision")
        self.gridLayoutSettings.addWidget(self.labelPrecision, 1, 4, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.gridLayoutSettings.addItem(spacerItem5, 2, 3, 1, 1)
        self.btnHartree = QtWidgets.QRadioButton(SaveTabDialog)
        self.btnHartree.setChecked(False)
        self.btnHartree.setObjectName("btnHartree")
        self.btnGroupUnit = QtWidgets.QButtonGroup(SaveTabDialog)
        self.btnGroupUnit.setObjectName("btnGroupUnit")
        self.btnGroupUnit.addButton(self.btnHartree)
        self.gridLayoutSettings.addWidget(self.btnHartree, 3, 0, 1, 1)
        self.btnEV = QtWidgets.QRadioButton(SaveTabDialog)
        self.btnEV.setChecked(True)
        self.btnEV.setObjectName("btnEV")
        self.btnGroupUnit.addButton(self.btnEV)
        self.gridLayoutSettings.addWidget(self.btnEV, 2, 0, 1, 1)
        self.btn3column = QtWidgets.QRadioButton(SaveTabDialog)
        self.btn3column.setChecked(True)
        self.btn3column.setObjectName("btn3column")
        self.btnGroupFormat = QtWidgets.QButtonGroup(SaveTabDialog)
        self.btnGroupFormat.setObjectName("btnGroupFormat")
        self.btnGroupFormat.addButton(self.btn3column)
        self.gridLayoutSettings.addWidget(self.btn3column, 3, 2, 1, 1)
        self.btn2column = QtWidgets.QRadioButton(SaveTabDialog)
        self.btn2column.setObjectName("btn2column")
        self.btnGroupFormat.addButton(self.btn2column)
        self.gridLayoutSettings.addWidget(self.btn2column, 2, 2, 1, 1)
        self.labelFormat = QtWidgets.QLabel(SaveTabDialog)
        self.labelFormat.setObjectName("labelFormat")
        self.gridLayoutSettings.addWidget(self.labelFormat, 1, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayoutSettings, 4, 0, 1, 1)

        self.retranslateUi(SaveTabDialog)
        QtCore.QMetaObject.connectSlotsByName(SaveTabDialog)

    def retranslateUi(self, SaveTabDialog):
        _translate = QtCore.QCoreApplication.translate
        SaveTabDialog.setWindowTitle(
            _translate("SaveTabDialog", "Save tab as...")
        )
        self.labelNote.setText(
            _translate(
                "SaveTabDialog",
                '<html><head/><body><p><span style=" font-size:8pt; font-weight:600;">NOTE:</span><span style=" font-size:8pt;"> For tensors use dummy names like epsilon_ij.dat, then ij → 11, 12, ... for all selected elements. When checking &quot;[x] Vector&quot;, only diagonal elements are used and filenames like data_i.dat will be replaced as i → 1, 2, 3.</span></p></body></html>',
            )
        )
        self.labelFilename.setText(_translate("SaveTabDialog", "Filename"))
        self.btnFilename.setText(_translate("SaveTabDialog", "..."))
        self.checkBoxVector.setText(_translate("SaveTabDialog", "Vector"))
        self.btnTenElements.setText(
            _translate("SaveTabDialog", "Tensor\n" " Elements")
        )
        self.btnTenElements.setShortcut(_translate("SaveTabDialog", "Ctrl+T"))
        self.labelUnit.setText(_translate("SaveTabDialog", "Unit"))
        self.labelPrecision.setText(_translate("SaveTabDialog", "Precision"))
        self.btnHartree.setText(_translate("SaveTabDialog", "Hartree"))
        self.btnEV.setText(_translate("SaveTabDialog", "eV"))
        self.btn3column.setText(_translate("SaveTabDialog", "3-column"))
        self.btn2column.setText(_translate("SaveTabDialog", "2-column"))
        self.labelFormat.setText(_translate("SaveTabDialog", "Format"))


class Ui_UnitDialog(object):
    def setupUi(self, UnitDialog):
        UnitDialog.setObjectName("UnitDialog")
        UnitDialog.resize(209, 127)
        self.gridLayout = QtWidgets.QGridLayout(UnitDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.btnHartree = QtWidgets.QRadioButton(UnitDialog)
        self.btnHartree.setChecked(False)
        self.btnHartree.setObjectName("btnHartree")
        self.gridLayout.addWidget(self.btnHartree, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(UnitDialog)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.btnEV = QtWidgets.QRadioButton(UnitDialog)
        self.btnEV.setChecked(True)
        self.btnEV.setObjectName("btnEV")
        self.gridLayout.addWidget(self.btnEV, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)

        self.retranslateUi(UnitDialog)
        QtCore.QMetaObject.connectSlotsByName(UnitDialog)

    def retranslateUi(self, UnitDialog):
        _translate = QtCore.QCoreApplication.translate
        UnitDialog.setWindowTitle(_translate("UnitDialog", "Unit"))
        self.btnHartree.setText(_translate("UnitDialog", "Hartree"))
        self.btnEV.setText(_translate("UnitDialog", "eV"))
