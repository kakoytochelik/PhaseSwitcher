import sys
import shutil
from pathlib import Path
import json
import os
import pyperclip
import appdirs
import uuid
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore

class MainWindow(QTabWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initializeAttributes("Core")
        self.setupUI()

    def initializeAttributes(self, region):
        self.marks = []
        self.disabled = []
        self.enabled = []
        self.error = []
        self.skipped = []
        self.loadConfig()
        self.loadPaths()
        self.myFont = QFont()
        self.myFont.setItalic(True)
        self.getPaths(region)

    def setupUI(self):
        self.setWindowIcon(QIcon(resource_path('res/icon.ico')))
        self.setWindowTitle('Phase Switcher 6')
        self.setGeometry(500, 200, 400, 350)

        self.createLayout()
        self.setupWidgets()
        self.setupConnections()
        self.setupLayout()
        self.checkOnStart()

    def createLayout(self):
        self.tableLayout = QVBoxLayout()
        self.headerLayout = QHBoxLayout()
        self.guidLayout = QHBoxLayout()
        self.runLayout = QHBoxLayout()
        self.tabs = QTabWidget()

    def setupLayout(self):
        self.tableLayout.addLayout(self.headerLayout)
        self.headerLayout.addWidget(self.settingsButton)
        self.headerLayout.addWidget(self.regionComboBox)
        self.headerLayout.addWidget(self.refreshButton)
        self.headerLayout.addWidget(self.setDefaultButton)
        self.headerLayout.addWidget(self.markAllCheckBox)
        self.tableLayout.addWidget(self.tabs)

        self.tableLayout.addLayout(self.guidLayout)
        self.guidLayout.addWidget(self.guidField)
        self.guidLayout.addWidget(self.guidGenerateButton)
        self.guidLayout.addWidget(self.guidCopyButton)

        self.tableLayout.addLayout(self.runLayout)
        self.runLayout.addWidget(self.runButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.tableLayout)

    def setupWidgets(self):
        self.guidField = QLineEdit(self)
        self.guidField.setReadOnly(True)
        self.guidField.setPlaceholderText("GUID")

        self.guidGenerateButton = QPushButton(QIcon(resource_path('res/refresh.png')), '')
        self.guidCopyButton = QPushButton(QIcon(resource_path('res/copy.png')), '')
        self.markAllCheckBox = QCheckBox('Select all', self)
        self.setDefaultButton = QPushButton(QIcon(resource_path('res/defaults.png')), "Default values")
        self.regionComboBox = QComboBox()
        self.settingsButton = QPushButton(QIcon(resource_path('res/configuration.png')), "")
        self.refreshButton = QPushButton(QIcon(resource_path('res/refresh.png')), "Refresh")
        self.runButton = QPushButton(QIcon(resource_path('res/continue.png')), "Run")

        self.loadRegions()
        self.createTabs()
        self.marks_temp = self.marks.copy()

    def setupConnections(self):
        self.guidGenerateButton.clicked.connect(self.generateGUID)
        self.guidCopyButton.clicked.connect(self.copyGUID)
        self.markAllCheckBox.clicked.connect(lambda: self.markUnmarkAll(self.markAllCheckBox))
        self.setDefaultButton.clicked.connect(self.defaultCheckboxes)
        self.regionComboBox.currentIndexChanged.connect(self.changeRegion)
        self.refreshButton.clicked.connect(self.changeRegion)
        self.runButton.clicked.connect(self.doTheThings)
        self.runButton.clicked.connect(self.showDialog)
        self.settingsButton.clicked.connect(self.openPathsWindow)

    def loadConfig(self):
        app_data_dir = appdirs.user_data_dir('PhaseSwitcher6', 'AlexEremeev')
        self.config_path = os.path.join(app_data_dir, 'config.json')
        if not os.path.exists(app_data_dir):
            os.makedirs(app_data_dir)
        if not os.path.exists(self.config_path):
            default_config_path = resource_path('conf/config.json')
            shutil.copy(default_config_path, self.config_path)

        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        self.default_values = {}

    def loadPaths(self):
        app_data_dir = appdirs.user_data_dir('PhaseSwitcher6', 'AlexEremeev')
        self.paths_path = os.path.join(app_data_dir, 'projects.json')
        if not os.path.exists(app_data_dir):
            os.makedirs(app_data_dir)
        if not os.path.exists(self.paths_path):
            default_paths_path = resource_path('conf/projects.json')
            shutil.copy(default_paths_path, self.paths_path)

        with open(self.paths_path, 'r') as f:
            self.paths = json.load(f)

    def loadRegions(self):
        self.regionComboBox.clear()
        regions = list(self.paths.keys())
        self.regionComboBox.addItems(regions)

    def createTabs(self):
        self.tabs.clear()
        self.marks.clear()
        for idx, tab_info in enumerate(self.config['tabs'], start=1):
            tab_name = tab_info["name"]
            tab_items = tab_info["items"]
            tab_widget = QWidget()
            setattr(self, f"tab{idx}", tab_widget)
            self.tabs.addTab(tab_widget, tab_name)
            self.create_checkboxes(tab_widget, tab_items)

    def create_checkboxes(self, tab_widget, items):
        layout = QVBoxLayout(tab_widget)
        for item in items:
            if 'test' in item:
                checkbox = QCheckBox(item['test'], tab_widget)
                self.marks.append(checkbox)
                self.default_values[item['test']] = item.get('default', False)
                checkbox.clicked.connect(lambda state, regionComboBox=checkbox: self.uncheck(regionComboBox))
                layout.addWidget(checkbox)
            elif 'label' in item:
                label = QLabel(item['label'])
                if 'note' in item and item['note']:
                    layout.addStretch(1)
                    label.setFont(self.myFont)
                layout.addWidget(label)
        layout.addStretch()
        tab_widget.setLayout(layout)

    def markUnmarkAll(self, btn):
        if btn.isChecked() == False:
            for i in self.marks_temp:
                i.setChecked(False)
        if btn.isChecked() == True:
            for i in self.marks_temp:
                i.setChecked(True)

    def defaultCheckboxes(self):
        for checkbox in self.marks:
            if checkbox.isEnabled():
                checkbox.setChecked(self.default_values.get(checkbox.text(), True))

    def uncheck(self, btn):
        if btn.isChecked() == False:
            self.markAllCheckBox.setChecked(0)

    def doTheThings(self):
        for i in self.marks:
            catalog = None
            for tab in self.config['tabs']:
                for item in tab['items']:
                    if 'test' in item and item['test'] == i.text():
                        catalog = item['path']
                        break

            if catalog is None:
                print(f"Warning: No catalog found for {i.text()}")
                continue

            path_on = self.tests_dir_on + catalog + "test/"
            path_off = self.tests_dir_off + catalog + "test/"

            if i.isEnabled():
                if not i.isChecked():
                    if Path(str(path_on)).exists():
                        shutil.move(path_on, path_off)
                        if Path(str(path_off)).exists():
                            self.disabled.append(i.text())
                            print("\n", i.text(), "disabled! \n")
                        else:
                            self.error.append(i.text())
                            print("\n", i.text(), "wasn't disabled, something went wrong!")
                    elif Path(str(path_off)).exists():
                        self.skipped.append(i.text())
                        print("\n", i.text(), "already disabled, skipping!\n")
                else:
                    if Path(str(path_off)).exists():
                        shutil.move(path_off, path_on)
                        if Path(str(path_on)).exists():
                            self.enabled.append(i.text())
                            print("\n", i.text(), "enabled! \n")
                        else:
                            self.error.append(i.text())
                            print("\n", i.text(), "wasn't enabled, something went wrong!")
                    elif Path(str(path_on)).exists():
                        self.skipped.append(i.text())
                        print("\n", i.text(), "already enabled, skipping!\n")

    def showDialog(self):
        enabled = "Tests enabled: " + str(len(self.enabled))
        disabled = 'Tests disabled: ' + str(len(self.disabled))
        error = 'Errors: ' + str(len(self.error))
        skipped = 'No changes: ' + str(len(self.skipped))

        QMessageBox.about(self, "Done", enabled + '\n' + disabled + '\n' + skipped + '\n' + error)

        self.enabled.clear()
        self.disabled.clear()
        self.error.clear()
        self.skipped.clear()

    def openPathsWindow(self):
        self.pathsWindow = PathsWindow(self.paths, self.paths_path, self.config_path)
        self.pathsWindow.closed.connect(self.onPathsWindowClosed)
        self.pathsWindow.pathsUpdated.connect(self.loadRegions)
        self.pathsWindow.configUpdated.connect(self.reloadConfig)
        self.pathsWindow.show()

    def checkOnStart(self):
        count = 0
        print("I'M IN")
        print(self.marks_temp)
        for i in range(len(self.marks)):
            catalog = None
            for tab in self.config['tabs']:
                for item in tab['items']:
                    if 'test' in item and item['test'] == self.marks[i].text():
                        catalog = item['path']
                        break

            if catalog is None:
                print(f"Warning: No catalog found for {self.marks[i].text()}")
                self.marks[i].setDisabled(True)
                if i < len(self.marks_temp):
                    self.marks_temp[i] = 'Remove'
                else:
                    self.marks_temp.append('Remove')
                count += 1
                continue

            if Path(self.tests_dir_on + catalog + "test/").exists():
                print(self.marks[i].text())
                self.marks[i].setDisabled(False)
                self.marks[i].setChecked(True)
                count += 1
            elif Path(self.tests_dir_off + catalog + "test/").exists():
                self.marks[i].setDisabled(False)
                self.marks[i].setChecked(False)
            else:
                self.marks[i].setDisabled(True)
                if i < len(self.marks_temp):
                    self.marks_temp[i] = 'Remove'
                else:
                    self.marks_temp.append('Remove')
                count += 1

        if count == len(self.marks):
            self.markAllCheckBox.setChecked(True)
        else:
            self.markAllCheckBox.setChecked(False)

        while 'Remove' in self.marks_temp:
            self.marks_temp.remove('Remove')

        print(len(self.marks))
        print(len(self.marks_temp))
        print(self.tests_dir_on)
        print(self.tests_dir_off)

    def changeRegion(self):
        for i in self.marks:
            self.tableLayout.removeWidget(i)
            i.deleteLater()

        self.marks.clear()
        self.marks_temp.clear()

        while self.tabs.count() > 0:
            self.tabs.removeTab(0)

        self.initializeAttributes(str(self.regionComboBox.currentText()))
        self.createTabs()
        self.marks_temp = self.marks.copy()
        self.checkOnStart()
        self.tabs.update()

    def getPaths(self, line):
        directory_path = self.paths.get(line, '')
        print("LOAD JSON: ", directory_path)

        self.tests_dir_on = directory_path + "/tests/RegressionTests/Yaml/Drive/"
        self.tests_dir_off = directory_path + "/RegressionTests_Disabled/Yaml/Drive/"
        print(self.tests_dir_on)
        print(self.tests_dir_off)

    def generateGUID(self):
        self.guid = str(uuid.uuid4())
        self.guidField.setText(self.guid)
        pyperclip.copy(self.guid)

    def copyGUID(self):
        self.guid = self.guidField.text()
        pyperclip.copy(self.guid)

    def onPathsWindowClosed(self):
        self.changeRegion()

    def reloadConfig(self):
        self.loadConfig()
        self.createTabs()
        self.checkOnStart()

class PathsWindow(QWidget):

    closed = QtCore.pyqtSignal()
    pathsUpdated = QtCore.pyqtSignal()
    configUpdated = QtCore.pyqtSignal()

    def __init__(self, paths, paths_path, config_path):
        super().__init__()
        self.paths = paths
        self.paths_path = paths_path
        self.config_path = config_path
        self.labels = []
        self.fields = []
        self.paths_dict = {}
        self.layouts = []
        self.buttons = []
        self.setupUI()
        self.loadPathsFromFile()

    def setupUI(self):
        self.setWindowIcon(QIcon(resource_path('res/icon.ico')))
        self.setWindowTitle('Settings')
        self.setGeometry(200, 200, 370, 300)
        
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.createButtonsLayout()
        self.mainLayout.addLayout(self.buttonsLayout)

        self.scrollArea = QScrollArea()
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setWidgetResizable(True)
        self.pathsLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.mainLayout.addWidget(self.scrollArea)

    def createButtonsLayout(self):
        self.buttonsLayout = QHBoxLayout()
        self.loadPathsButton = QPushButton("Load Projects File")
        self.loadPathsButton.clicked.connect(self.loadPathsFile)
        self.loadConfigButton = QPushButton("Load Config File")
        self.loadConfigButton.clicked.connect(self.loadConfigFile)
        self.buttonsLayout.addWidget(self.loadPathsButton)
        self.buttonsLayout.addWidget(self.loadConfigButton)

    def setupLayout(self):
        self.clearLayout(self.pathsLayout)

        for layout, label, button in zip(self.layouts, self.labels, self.buttons):
            layout.addWidget(label)
            layout.addWidget(self.paths_dict[label.text()[:-1]])
            layout.addWidget(button)
            self.pathsLayout.addLayout(layout)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                if child.layout() is not None:
                    self.clearLayout(child.layout())

    def createLabels(self):
        self.labels = []
        self.fields = []
        self.paths_dict = {}
        self.layouts = []
        self.buttons = []

        for label_text in self.paths.keys():
            label = QLabel(label_text + ':')
            label.setFixedWidth(100)
            field = QLineEdit()
            self.labels.append(label)
            self.fields.append(field)
            self.paths_dict[label_text] = field

            layout = QHBoxLayout()
            button = QPushButton(QIcon(resource_path('res/folder.png')), '')
            button.setFixedWidth(30)
            button.clicked.connect(self.browsePath)
            self.buttons.append(button)
            self.layouts.append(layout)
            layout.addWidget(label)
            layout.addWidget(self.paths_dict[label.text()[:-1]])
            layout.addWidget(button)
            self.pathsLayout.addLayout(layout)

    def browsePath(self):
        button = self.sender()
        index = self.buttons.index(button)
        directory = self.fields[index].text()
        print(directory)
        selected_directory = QFileDialog.getExistingDirectory(self, "Select Project Directory", directory)
        if selected_directory:
            label = self.labels[index]
            self.paths_dict[label.text()[:-1]].setText(selected_directory)
            self.paths[label.text()[:-1]] = selected_directory
            self.savePathsToFile()

    def loadPathsFromFile(self):
        try:
            with open(self.paths_path, 'r') as file:
                paths_data = json.load(file)
                self.paths = paths_data
                self.updatePathsFields()
                self.savePathsToFile()
                self.pathsUpdated.emit()
        except FileNotFoundError:
            print("Paths file not found")

    def savePathsToFile(self):
        with open(self.paths_path, 'w') as file:
            json.dump(self.paths, file, indent=4)

    def closeEvent(self, event):
        for label_text, field in self.paths_dict.items():
            self.paths[label_text] = field.text()
        self.savePathsToFile()
        self.closed.emit()
        self.pathsUpdated.emit()
        event.accept()

    def loadPathsFile(self):
        paths_file, _ = QFileDialog.getOpenFileName(self, "Load Projects File", "", "JSON Files (*.json)")
        if paths_file:
            with open(paths_file, 'r') as file:
                self.paths = json.load(file)
                self.updatePathsFields()
                self.savePathsToFile()
                self.pathsUpdated.emit()

    def loadConfigFile(self):
        config_file, _ = QFileDialog.getOpenFileName(self, "Load Config File", "", "JSON Files (*.json)")
        if config_file:
            shutil.copy(config_file, self.config_path)
            print(f"Config file {config_file} loaded and copied to {self.config_path}")
            self.configUpdated.emit()

    def updatePathsFields(self):
        self.clearLayout(self.pathsLayout)
        self.createLabels()
        self.fillPathFields()

    def fillPathFields(self):
        for label_text, field in self.paths_dict.items():
            field.setText(self.paths.get(label_text, ""))



def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    main()
