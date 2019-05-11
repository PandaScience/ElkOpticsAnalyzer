# This file was adapted from https://github.com/By0ute/pyqt-collapsible-widget
# by Caroline Beyne, licensed under MIT License.
__author__ = "Caroline Beyne, René Wirnata"

from PyQt5 import QtCore, QtWidgets


class FrameLayout(QtWidgets.QWidget):
    collapseFinished = QtCore.pyqtSignal()

    def __init__(self, parent=None, title=None):
        QtWidgets.QFrame.__init__(self, parent=parent)

        self.isCollapsed = True

        self.titleFrame = self.TitleFrame(title, self.isCollapsed)
        self.titleFrame.clicked.connect(self.toggleCollapsed)

        self.contentLayout = QtWidgets.QVBoxLayout()
        self.content = QtWidgets.QWidget()
        self.content.setLayout(self.contentLayout)
        self.content.setVisible(False)

        self.mainVLayout = QtWidgets.QVBoxLayout(self)
        self.mainVLayout.addWidget(self.titleFrame)
        self.mainVLayout.addWidget(self.content)

    def addWidget(self, widget):
        self.contentLayout.addWidget(widget)

    def toggleCollapsed(self):
        self.content.setVisible(self.isCollapsed)
        self.isCollapsed = not self.isCollapsed
        self.titleFrame.setArrow(self.isCollapsed)
        self.collapseFinished.emit()

    class TitleFrame(QtWidgets.QFrame):
        clicked = QtCore.pyqtSignal()

        def __init__(self, title="", collapsed=False):
            QtWidgets.QFrame.__init__(self)

            self.setMinimumHeight(24)
            self.move(QtCore.QPoint(24, 0))

            self.arrow = QtWidgets.QLabel("⯈")
            self.title = QtWidgets.QLabel(" " + title)
            self.title.setMinimumHeight(24)
            self.title.move(QtCore.QPoint(24, 0))

            self.verticalSpacer = QtWidgets.QSpacerItem(
                20,
                40,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Minimum,
            )

            self.hLayout = QtWidgets.QHBoxLayout(self)
            self.hLayout.setContentsMargins(0, 0, 0, 0)
            self.hLayout.setSpacing(0)
            self.hLayout.addWidget(self.arrow)
            self.hLayout.addWidget(self.title)
            self.hLayout.addItem(self.verticalSpacer)

        def setArrow(self, collapsed):
            if collapsed:
                self.arrow.setText("⯈")
            else:
                self.arrow.setText("⯆")

        def mousePressEvent(self, event):
            self.clicked.emit()
            return super(FrameLayout.TitleFrame, self).mousePressEvent(event)


# EOF - FrameLayout.py
