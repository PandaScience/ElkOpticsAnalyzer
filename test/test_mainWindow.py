import os
import pytest
from PyQt5.QtCore import Qt

import elkoa.gui.UiMainWindow as UiMainWindow

# elkoa cd's into the data wd, so save the initial wd to go back after each
# test such that the baseline foldder is created in the correct path
iwd = os.getcwd()


@pytest.fixture
def ui(request, qtbot):
    """Creates a main window connected to a test data set for each test."""
    try:
        path = request.param
    except AttributeError:
        path = "./testdata/Si-full"
    ui = UiMainWindow.MainWindow(path)
    qtbot.addWidget(ui)
    ui.show()
    return ui


def finalizeMpl(ui):
    """Prepares test file creation in proper path."""
    os.chdir(iwd)
    tabIdx = ui.tabWidget.currentIndex()
    return ui.figures[tabIdx]


@pytest.mark.mpl_image_compare(savefig_kwargs={"dpi": 300}, tolerance=2)
class TestSimpleViews:
    @pytest.mark.parametrize("tab", [0, 1])
    def test_task_121(self, qtbot, ui, tab):
        """Tests choosing tasks via combo box."""
        with qtbot.waitSignal(ui.windowUpated, timeout=5000):
            idx = ui.taskChooser.findText("121", Qt.MatchContains)
            ui.taskChooser.setCurrentIndex(idx)
            ui.tabWidget.setCurrentIndex(tab)
        return finalizeMpl(ui)

    @pytest.mark.parametrize("tab", [0])
    def test_task_187(self, qtbot, ui, tab):
        """Tests choosing tasks via combo box."""
        with qtbot.waitSignal(ui.windowUpated, timeout=5000):
            idx = ui.taskChooser.findText("187", Qt.MatchContains)
            ui.taskChooser.setCurrentIndex(idx)
            ui.tabWidget.setCurrentIndex(tab)
        return finalizeMpl(ui)

    @pytest.mark.parametrize("tab", [0, 1])
    def test_task_320v5(self, qtbot, ui, tab):
        """Tests choosing tasks via combo box."""
        with qtbot.waitSignal(ui.windowUpated, timeout=5000):
            idx = ui.taskChooser.findText("320/v5", Qt.MatchContains)
            ui.taskChooser.setCurrentIndex(idx)
            ui.tabWidget.setCurrentIndex(tab)
        return finalizeMpl(ui)

    @pytest.mark.parametrize("tab", range(6))
    def test_task_330(self, qtbot, ui, tab):
        """Tests choosing tasks via combo box."""
        with qtbot.waitSignal(ui.windowUpated, timeout=5000):
            idx = ui.taskChooser.findText("330", Qt.MatchContains)
            ui.taskChooser.setCurrentIndex(idx)
            ui.tabWidget.setCurrentIndex(tab)
        return finalizeMpl(ui)

    @pytest.mark.parametrize(
        "button",
        [
            "btnRealPart",
            "btnImaginaryPart",
            "btnSplitView",
            "btnTogether",
            "checkBoxfullRange",
        ],
    )
    def test_buttons(self, qtbot, ui, button):
        """Tests views generated by different views via radio buttons."""
        ui.taskChooser.setCurrentIndex(1)
        with qtbot.waitSignal(ui.windowUpated, timeout=5000):
            qtbot.mouseClick(getattr(ui, button), Qt.LeftButton)
        # qtbot.wait(1000)
        return finalizeMpl(ui)


@pytest.mark.incremental
@pytest.mark.mpl_image_compare(savefig_kwargs={"dpi": 300}, tolerance=2)
class TestTensorElementSettings:
    def test_simple(self, qtbot, ui):
        """Tests diagonal elements via dialog functions."""
        ui.taskChooser.setCurrentIndex(1)
        ui.tenElementsDialog.initializeBoxStates()
        ui.tenElementsDialog.diagonalOnly()
        ui.tenElementsDialog.accepted()
        with qtbot.waitSignal(ui.windowUpated, timeout=5000):
            ui.updateWindow()
        return finalizeMpl(ui)

    @pytest.mark.parametrize("step", range(1, 8))
    def test_globalStates(self, qtbot, ui, step):
        """Tests correct views when global settings are activated."""
        ui.taskChooser.setCurrentIndex(1)
        ui.tenElementsDialog.diagonalOnly()
        ui.tenElementsDialog.accepted()
        with qtbot.waitSignal(ui.windowUpated, timeout=5000):
            ui.updateWindow()
        if step >= 1:
            with qtbot.waitSignal(ui.windowUpated, timeout=5000):
                qtbot.keyClick(ui, Qt.Key_G, modifier=Qt.ControlModifier)
        if step >= 2:
            ui.tabWidget.setCurrentIndex(1)
        if step >= 3:
            with qtbot.waitSignal(ui.windowUpated, timeout=5000):
                ui.taskChooser.setCurrentIndex(3)
        if step >= 4:
            ui.tabWidget.setCurrentIndex(1)
        if step >= 5:
            with qtbot.waitSignal(ui.windowUpated, timeout=5000):
                qtbot.mouseClick(ui.btnImaginaryPart, Qt.LeftButton)
        if step >= 6:
            with qtbot.waitSignal(ui.windowUpated, timeout=5000):
                qtbot.keyClick(ui, Qt.Key_G, modifier=Qt.ControlModifier)
        if step >= 7:
            with qtbot.waitSignal(ui.windowUpated, timeout=5000):
                ui.taskChooser.setCurrentIndex(1)
        return finalizeMpl(ui)


@pytest.mark.debug
@pytest.mark.parametrize(
    "ui", ["./testdata/batch/test-1"], indirect=True, ids=["eps11"]
)
@pytest.mark.mpl_image_compare(savefig_kwargs={"dpi": 300}, tolerance=2)
def test_batch(qtbot, ui):
    """Tests choosing tasks via combo box."""
    ui._pytest = True
    ui.batchLoadDialog.parameter = "scissor"
    ui.batchLoadDialog.file = "EPSILON_11.OUT"
    ui.batchLoadDialog.folders = []
    for i in range(1, 7):
        path = "../test-{}".format(i)
        ui.batchLoadDialog.folders.append(path)
    # use elkInput from default load path and save a 2nd load
    ui.batchLoadDialog.elkInput = ui.elkInput
    with qtbot.waitSignal(ui.windowUpated, timeout=5000):
        ui.batchLoad()
    return finalizeMpl(ui)


# EOF - test_mainWindow.py
