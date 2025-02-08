import sys
import shutil
from pathlib import Path
import json
import os
import re
import pyperclip
import appdirs
import uuid
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore
# import qdarktheme

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
        self.setWindowTitle('Phase Switcher 6.9')
        self.setGeometry(500, 200, 430, 512)
        self.setMaximumWidth(550)
        self.setMaximumHeight(640)

        self.createLayout()
        self.setupWidgets()
        self.setupConnections()
        self.setupLayout()
        self.checkOnStart()

    def createLayout(self):
        self.tableLayout = QVBoxLayout()
        self.headerLayout = QHBoxLayout()
        self.guidLayout = QHBoxLayout()
        self.searchLayout = QHBoxLayout()
        self.runLayout = QHBoxLayout()
        self.tabs = QTabWidget()

    def setupLayout(self):
        self.tableLayout.addLayout(self.headerLayout)
        self.headerLayout.addWidget(self.settingsButton)
        self.headerLayout.addWidget(self.regionComboBox)
        self.headerLayout.addWidget(self.refreshButton)
        self.headerLayout.addWidget(self.markAllCheckBox)
        self.tableLayout.addWidget(self.tabs)

        self.tableLayout.addLayout(self.guidLayout)
        self.guidLayout.addWidget(self.guidField)
        self.guidLayout.addWidget(self.guidGenerateButton)
        self.guidLayout.addWidget(self.guidCopyButton)

        self.tableLayout.addLayout(self.searchLayout)
        self.searchLayout.addWidget(self.lastScenarioField)
        self.searchLayout.addWidget(self.lastScenarioButton)

        self.tableLayout.addLayout(self.runLayout)
        self.runLayout.addWidget(self.newScenarioButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.runLayout.addWidget(self.setDefaultButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.runLayout.addWidget(self.runButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.tableLayout)

    def setupWidgets(self):
        self.guidField = QLineEdit(self)
        self.guidField.setReadOnly(True)
        self.guidField.setPlaceholderText("UID")

        self.lastScenarioField = QLineEdit(self)
        self.lastScenarioField.setPlaceholderText("Find the last test number. Enter your prefix (eg. 12)")
        self.lastScenarioButton = QPushButton(QIcon(resource_path('res/search.svg')), '')

        self.lastScenarioButton.setFixedWidth(66)

        self.guidGenerateButton = QPushButton(QIcon(resource_path('res/refresh.svg')), '')
        self.guidGenerateButton.setFixedWidth(30)
        self.guidCopyButton = QPushButton(QIcon(resource_path('res/copy.svg')), '')
        self.guidCopyButton.setFixedWidth(30)
        self.markAllCheckBox = QCheckBox('Select all', self)
        self.setDefaultButton = QPushButton(QIcon(resource_path('res/defaults.svg')), "Default values")
        self.regionComboBox = QComboBox()
        self.regionComboBox.setFixedWidth(100)
        self.settingsButton = QPushButton(QIcon(resource_path('res/configuration.svg')), "Settings")
        self.settingsButton.setFixedWidth(100)
        self.refreshButton = QPushButton(QIcon(resource_path('res/refresh.svg')), "Refresh")
        self.refreshButton.setFixedWidth(100)
        self.runButton = QPushButton(QIcon(resource_path('res/apply.svg')), "Apply changes")
        self.newScenarioButton = QPushButton(QIcon(resource_path('res/add.svg')), "Create scenario")

        self.loadRegions()
        self.createTabs()
        self.marks_temp = self.marks.copy()

    def setupConnections(self):
        self.guidGenerateButton.clicked.connect(lambda: generateGUID(self, self.guidField))
        self.guidCopyButton.clicked.connect(self.copyGUID)
        self.markAllCheckBox.clicked.connect(lambda: self.markUnmarkAll(self.markAllCheckBox))
        self.setDefaultButton.clicked.connect(self.defaultCheckboxes)
        self.regionComboBox.currentIndexChanged.connect(self.changeRegion)
        self.refreshButton.clicked.connect(self.changeRegion)
        self.runButton.clicked.connect(self.doTheThings)
        self.runButton.clicked.connect(self.showDialog)
        self.settingsButton.clicked.connect(self.openPathsWindow)
        self.newScenarioButton.clicked.connect(self.openNewScenarioWindow)
        self.lastScenarioButton.clicked.connect(self.updateLastScenario)

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

    def openNewScenarioWindow(self):
        default_folder = self.tests_dir_on + "Parent scenarios/"
        self.NewScenWindow = NewMainScenarioWindow(default_folder)
        self.NewScenWindow.show()


    def updateLastScenario(self):
        prefix = self.lastScenarioField.text().strip()
        if not prefix.isdigit() or len(prefix) != 2:
            self.lastScenarioField.setStyleSheet("color: red;")
            return
        self.lastScenarioField.setStyleSheet("")

        scenarios_path = self.tests_dir_on
        last_scenario_number = self.searchScenariosByPrefix(scenarios_path, prefix)
        self.lastScenarioField.setText(last_scenario_number if last_scenario_number else "Not found")

    def searchScenariosByPrefix(self, path, prefix):
        if not os.path.exists(path):
            return None

        scenario_numbers = {}
        for root, dirs, _ in os.walk(path):
            for folder in dirs:
                match = re.match(r'(0*' + prefix + r'\d+)', folder) 
                if match:
                    original_name = match.group(1)
                    numeric_value = int(original_name)
                    scenario_numbers[numeric_value] = original_name

        if scenario_numbers:
            return scenario_numbers[max(scenario_numbers)]
        return None
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
        self.setMaximumWidth(370)
        self.setMinimumWidth(370)
        self.setMinimumHeight(300)

        
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

        # self.themeLayout = QHBoxLayout()
        # self.themeCheckBox = QCheckBox('Dark theme', self)
        # self.themeLayout.addWidget(self.themeCheckBox)
        # self.mainLayout.addLayout(self.themeLayout)
        # self.themeCheckBox.clicked.connect(lambda: self.toggleTheme(self.themeCheckBox))


    def toggleTheme(self, isDark):
        if isDark.isChecked() == True:
            qdarktheme.setup_theme("dark")
            self.setStyleSheet("""
                QPushButton {
                    color: white;
                }
            """)
        if isDark.isChecked() == False:
            qdarktheme.setup_theme("light")
            self.setStyleSheet("""
                QPushButton {
                    color: black;
                }
            """)

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
            button = QPushButton(QIcon(resource_path('res/folder.svg')), '')
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


class NewMainScenarioWindow(QWidget):

    def __init__(self, default_folder):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path('res/icon.ico')))
        self.setWindowTitle("New Scenario")
        self.setGeometry(450, 350, 480, 220)
        self.setFixedSize(480, 220)

        self.isMain = False

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        # Scrollable Area
        self.scrollArea = QScrollArea()
        self.scrollAreaWidgetContents = QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setWidgetResizable(True)
        self.formLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        
        # Is Main Checkbox
        isMainLayout = QHBoxLayout()
        self.isMainCheckBox = QCheckBox('Main scenario', self)
        self.isMainCheckBox.setChecked(False)
        isMainLayout.addWidget(self.isMainCheckBox)
        self.formLayout.addLayout(isMainLayout)

        # Name Field
        nameLayout = QHBoxLayout()
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Name")
        # nameLayout.addWidget(self.name_label)
        nameLayout.addWidget(self.name_field)
        self.formLayout.addLayout(nameLayout)

        # Code Field
        # codeLayout = QHBoxLayout()
        self.code_field = QLineEdit()
        self.code_field.setPlaceholderText("Code")
        # codeLayout.addWidget(self.code_label)
        # codeLayout.addWidget(self.code_field)
        nameLayout.addWidget(self.code_field)
        self.code_field.setFixedWidth(90)
        # self.formLayout.addLayout(codeLayout)
        self.code_field.setDisabled(False)

        # UID Field (Read-only, Auto-generated)
        uidLayout = QHBoxLayout()
        self.uid_label = QLabel("UID:")
        self.uid_label.setFixedWidth(35)
        self.uid_field = QLineEdit()
        self.uid_field.setReadOnly(True)
        self.uid_field.setText(str(uuid.uuid4()))
        uidLayout.addWidget(self.uid_label)
        uidLayout.addWidget(self.uid_field)
        self.guidGenerateButton = QPushButton(QIcon(resource_path('res/refresh.svg')), '')
        self.guidGenerateButton.setFixedWidth(30)
        self.guidGenerateButton.clicked.connect(lambda: generateGUID(self, self.uid_field))
        uidLayout.addWidget(self.guidGenerateButton)


        self.formLayout.addLayout(uidLayout)

        # Folder Field
        folderLayout = QHBoxLayout()
        self.folder_label = QLabel("Folder:")
        self.folder_label.setFixedWidth(35)
        self.folder_field = QLineEdit()
        self.folder_field.setText(default_folder)
        self.folder_button = QPushButton(QIcon(resource_path('res/folder.svg')), '')
        self.folder_button.setFixedWidth(30)
        self.folder_button.clicked.connect(self.browse_folder)
        folderLayout.addWidget(self.folder_label)
        folderLayout.addWidget(self.folder_field)
        folderLayout.addWidget(self.folder_button)
        self.formLayout.addLayout(folderLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.mainLayout.addWidget(self.scrollArea)

        # Create Button
        self.submit_button = QPushButton("Create")
        self.mainLayout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.create_scenario)

        self.isMainCheckBox.clicked.connect(lambda: self.isMainScenario(self.isMainCheckBox))


    def isMainScenario(self, isMain):
        if isMain.isChecked() == False:
            self.code_field.setDisabled(False)
            self.isMain = False


        if isMain.isChecked() == True:
            self.code_field.setDisabled(True)
            self.isMain = True


    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", self.folder_field.text())
        if folder:
            self.folder_field.setText(folder)


    def create_scenario(self):
        name = self.name_field.text().strip()
        code = self.code_field.text().strip()
        uid = self.uid_field.text()
        folder = self.folder_field.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Error", "Name field cannot be empty!")
            return

        elif not code and self.isMain == False:
            QMessageBox.warning(self, "Error", "Code field cannot be empty!")
            return
        

        if self.isMain == True:
            scen_template = resource_path('res/main.yaml')
            test_template = resource_path('res/test.yaml')
            scenario_path = os.path.join(folder, name)
            os.makedirs(os.path.join(scenario_path, "test"), exist_ok=True)

            with open(test_template, 'r', encoding='utf-8') as f:
                test_content = f.read().replace("Name_Placeholder", name).replace("UID_Placeholder", uid).replace("Random_UID", str(uuid.uuid4()))
            
            with open(os.path.join(scenario_path, "test", f"{name}.yaml"), 'w', encoding='utf-8') as f:
                f.write(test_content)

            with open(scen_template, 'r', encoding='utf-8') as f:
                scen_content = f.read().replace("Name_Placeholder", name).replace("Code_Placeholder", name).replace("UID_Placeholder", uid)


        if self.isMain == False:
            scen_template = resource_path('res/scen.yaml')
            scenario_path = os.path.join(folder, code)
            os.makedirs(os.path.join(scenario_path), exist_ok=True)
            with open(scen_template, 'r', encoding='utf-8') as f:
                scen_content = f.read().replace("Name_Placeholder", name).replace("Code_Placeholder", code).replace("UID_Placeholder", uid)

        with open(os.path.join(scenario_path, "scen.yaml"), 'w', encoding='utf-8') as f:
            f.write(scen_content)
        
        
        QMessageBox.information(self, "Success", f"Scenario \"{name}\" has been created in: \n\n{scenario_path}\n\nIf it's a main scenario, don't forget to include it in the config (See readme)")
        self.close()

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()

    # qdarktheme.setup_theme(theme="light", custom_colors={"foreground>disabled": "#D0BCFF"})

    ex.show()
    sys.exit(app.exec())


def generateGUID(self, guidField):
    self.guid = str(uuid.uuid4())
    guidField.setText(self.guid)
    pyperclip.copy(self.guid)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    main()
