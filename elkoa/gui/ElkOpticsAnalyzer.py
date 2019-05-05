#!/usr/bin/env python3
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
import signal

import elkoa.gui.UiMainWindow as UiMainWindow
from PyQt5 import QtWidgets


def main():
    # handle Ctrl+C in terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # create main window and process cmd line arguments
    app = QtWidgets.QApplication(sys.argv)
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.getcwd()
    ui = UiMainWindow.MainWindow(path)
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

# EOF - ElkOpticsAnalyzer.py
