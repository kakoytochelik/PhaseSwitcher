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
        self.getPaths(region)
        self.myFont=QFont()
        self.myFont.setItalic(True)



    def setupUI(self):
        self.setWindowIcon(QIcon(resource_path('res/icon.ico')))
        self.setWindowTitle('Phase Switcher 5.1')
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
        self.headerLayout.addWidget(self.pathsButton)
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
        self.pathsButton = QPushButton(QIcon(resource_path('res/folder.png')), "")
        self.regionComboBox.addItems(["Core", "Turkey", "Colombia", "Germany", "Poland", "Mexico"])
        self.refreshButton = QPushButton(QIcon(resource_path('res/refresh.png')), "Refresh")
        self.runButton = QPushButton(QIcon(resource_path('res/continue.png')), "Run")

        self.createTabs()
        self.marks_temp = self.marks.copy()



    def setupConnections(self):
        self.guidGenerateButton.clicked.connect(self.generateGUID)
        self.guidCopyButton.clicked.connect(self.copyGUID)
        self.markAllCheckBox.clicked.connect(self.markUnmarkAll)
        self.setDefaultButton.clicked.connect(self.defaultCheckboxes)
        self.regionComboBox.currentIndexChanged.connect(self.changeRegion)
        self.refreshButton.clicked.connect(self.changeRegion)
        self.runButton.clicked.connect(self.doTheThings)
        self.runButton.clicked.connect(self.showDialog)  
        self.pathsButton.clicked.connect(self.openPathsWindow)  

    
    def createTabs(self):

        tab_info = [
            ("FirstTest", self.tab1UI),
            ("Purchases subsystem 1", self.tab2UI),
            ("Purchases subsystem 2", self.tab3UI),
            ("Purchases subsystem 3", self.tab4UI),
            ("Sales tests 1", self.tab5UI),
            ("Sales tests 2", self.tab6UI),
            ("Sales tests 3", self.tab7UI),
            ("Sales tests 4", self.tab8UI),
            ("Sales tests 5", self.tab9UI),
            ("Smoke tests", self.tab10UI),
            ("Templates", self.tab11UI),
            ("Regions", self.tab12UI)
        ]

        for idx, (tab_name, tab_ui_method) in enumerate(tab_info, start=1):
            tab_widget = QWidget()
            setattr(self, f"tab{idx}", tab_widget)
            self.tabs.addTab(tab_widget, tab_name)
            tab_ui_method(tab_widget)



    def create_checkboxes(self, tab_widget, items):
        layout = QVBoxLayout(tab_widget)
        for item in items:
            if 'label' in item:
                checkbox = QCheckBox(item['label'], tab_widget)
                self.marks.append(checkbox)
                checkbox.clicked.connect(lambda state, regionComboBox=checkbox: self.uncheck(regionComboBox))
                layout.addWidget(checkbox)
            elif 'text' in item:
                label = QLabel(item['text'])
                if 'bold' in item and item['bold']:
                    layout.addStretch(1)
                    label.setFont(self.myFont)
                layout.addWidget(label)
        layout.addStretch()
        tab_widget.setLayout(layout)



    def tab1UI(self, tab_widget):
        items = [
            {'text':  'Phase5_Vanessa_First_Test'},
            {'label': '001_Company_tests'}
        ]
        self.create_checkboxes(tab_widget, items)



    def tab2UI(self, tab_widget):
        items = [
            {'text':  'Phase_5.3_Purchases_subsystem_tests'},
            {'label': '003_I_test_purchases'},
            {'label': '006_Debit_note'},
            {'label': '0081_Goods_issue_after_sales_invoice'},
            {'label': '0085_Monkey_tests'}
        ]
        self.create_checkboxes(tab_widget, items)



    def tab3UI(self, tab_widget):
        items = [
            {'text':  'Phase_5.3_Purchases_subsystem_tests_2'},
            {'label': '0031_Purchases_reverse_charge'},
            {'label': '0032_Purchases_ZERO_VAT'},
            {'label': '0034_Stocktaking_documents'},
            {'label': '0035_Goods_receipt'}
        ]
        self.create_checkboxes(tab_widget, items)



    def tab4UI(self, tab_widget):
        items = [
            {'text':  'Phase_5.3_Purchases_subsystem_tests_3'},
            {'label': '0036_Supplier_invoice_Continental'},
            {'label': '0037_Subcontractor_order_Continental'},
            {'label': '0038_Subcontractor_order_anglo-saxon'},
            {'label': '0039_Assembly_Disassembly'}
        ]
        self.create_checkboxes(tab_widget, items)



    def tab5UI(self, tab_widget):
        items = [
            {'text':  'Phase_5.4_Sales_test'},
            {'label': '0083_Work_orders'},
            {'label': '008_FIFO'}
        ]
        self.create_checkboxes(tab_widget, items)



    def tab6UI(self, tab_widget):
        items = [
            {'text':  'Phase_5.4_Sales_test_2'},
            {'label': '002_Payments_terms_Advance_payments'},
            {'label': '002_Production'}
        ]
        self.create_checkboxes(tab_widget, items)



    def tab7UI(self, tab_widget):
        items = [
            {'text':  'Phase_5.4_Sales_test_3'},
            {'label': '0051_Credit_note_plus_GoodsReturn'},
            {'label': '0052_Credit_note_do_not_use_GR_and_TI'},
            {'label': '0053_Credit_note_withoutVat'},
            {'label': '0086_Monkey_tests'}
        ]
        self.create_checkboxes(tab_widget, items)



    def tab8UI(self, tab_widget):
        items = [
            {'text':  'Phase_5.4_Sales_test_4'},
            {'label': '0082_Retail_tests_sales_without_VAT'},
            {'label': '0081_Retail_tests_operations_with_VAT'},
            {'label': '0041_Loans_tests'},
            {'label': '0042_Loans_tests'},
            {'label': '0043_Loans_tests'},
            {'label': '0044_Loans_tests'},
            {'label': '0045_Foreign_currency_exchanges'},
            {'label': '0046_AR_AP_adjustment'}
        ]
        self.create_checkboxes(tab_widget, items)



    def tab9UI(self, tab_widget):
        items = [
            {'text':  'Phase_5.4_Sales_test_5'},
            {'label': '002_Subcontracting'},
            {'label': '0021_Direct_debit'},
            {'label': '007_I_test_users_creation'},
            {'label': '009_CRM'}
        ]
        self.create_checkboxes(tab_widget, items)



    def tab10UI(self, tab_widget):
        items = [
            {'text':  'Phase_10_Check_Update_Base_With_Templates'},
            {'label': 'I_start_my_first_launch_templates'},
            {'text':  ' '},
            {'text':  'Phase_6_Smoke_tests'},
            {'label': 'I_start_my_first_launch'},
            {'label': '0084_Monkey_tests'},
            {'text':  'Reset tests on this tab before push! (Default values -> Run)', 'bold': True},
        ]
        self.create_checkboxes(tab_widget, items)



    def tab11UI(self, tab_widget):
        items = [
            {'text':  'Phase_7_Templates'},
            {'label': '0098_Accounting_templates'},
            {'text':  ' '},
            {'text':  'Phase_7_Templates_2'},
            {'label': '0100_Templates_in_invoices'},
            {'text':  ' '},
            {'text':  'Phase_7_Templates_3'},
            {'label': '0101_Templates_in_documents_and_reports'},
            {'text':  ' '},
            {'text':  'Phase_7_Templates_4'},
            {'label': '0102_Accounting_entries_data_register'},
            {'text':  ' '},
            {'text':  'Phase_7_Templates_5'},
            {'label': '0103_Transferred_accounting_templates'},
            {'text':  ' '},
            {'text':  '420_Templates (legacy/for regions)'},
            {'label': '420_Templates'},
            {'text':  ' '},
            {'text':  'Reset tests on this tab before push! (Default values -> Run)', 'bold': True},
        ]
        self.create_checkboxes(tab_widget, items)



    def tab12UI(self, tab_widget):
        items = [
            {'text':  'Turkey:'},
            {'label': '0089_Turkey_tests'},
            {'text':  ' '},
            {'text':  'Colombia:'},
            {'label': '0089_Colombian_tests'},
            {'text':  ' '},
            {'text':  'Germany:'},
            {'label': '0088_Germany_tests'},
            {'text':  ' '},
            {'text':  'Poland:'},
            {'label': '0087_Poland_tests'},
            {'text':  ' '},
            {'text':  'Mexico:'},
            {'label': '0089_Mexico_tests'}
        ]
        self.create_checkboxes(tab_widget, items)



    def markUnmarkAll(self, btn):
        if btn.isChecked() == False:
            for i in self.marks_temp:
                i.setChecked(False)
        if btn.isChecked() == True:
            for i in self.marks_temp:
                i.setChecked(True)



    def defaultCheckboxes(self):
        for i in self.marks_temp:
            i.setChecked(1)
            if i.text() == "I_start_my_first_launch":
              i.setChecked(0)
            if i.text() == "I_start_my_first_launch_templates":
              i.setChecked(0)
            if i.text() == "0098_Accounting_templates":
              i.setChecked(0)
            if i.text() == "0100_Templates_in_invoices":
              i.setChecked(0)
            if i.text() == "0101_Templates_in_documents_and_reports":
              i.setChecked(0)  
            if i.text() == "0102_Accounting_entries_data_register":
              i.setChecked(0)
            if i.text() == "0103_Transferred_accounting_templates":
              i.setChecked(0)
            if i.text() == "420_Templates":
              i.setChecked(0)  



    def uncheck(self, btn):
        if btn.isChecked() == False:
            self.markAllCheckBox.setChecked(0)
        


    def doTheThings(self):
        for i in self.marks:
            path_on = self.tests_dir_on + self.paths.get(i.text()) + "test/"
            path_off = self.tests_dir_off + self.paths.get(i.text()) + "test/"

            if i.isEnabled():

                if i.isChecked() == False:
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

                if i.isChecked() == True:
                    if Path(str(path_off)).exists():
                        shutil.move(path_off, path_on)
                        if Path(str(path_on)).exists():
                            self.enabled.append(i.text())
                            print("\n", i.text(), "enabled! \n")
                        else:
                            self.error.append(i.text())
                            print("\n", i.text(), "wasn't disabled, something went wrong!")
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
        self.pathsWindow = PathsWindow()
        self.pathsWindow.closed.connect(self.onPathsWindowClosed)
        self.pathsWindow.show()


    def checkOnStart(self):
        count = 0
        print("I'M IN")
        print(self.marks_temp)
        for i in range(len(self.marks)):        
            catalog = self.paths.get(self.marks[i].text())
            if Path(self.tests_dir_on + catalog + "test/").exists() :
                print(self.marks[i].text())
                self.marks[i].setDisabled(0)
                self.marks[i].setChecked(1)
                count = count + 1
            elif Path(self.tests_dir_off + catalog + "test/").exists() :
                self.marks[i].setDisabled(0)
                self.marks[i].setChecked(0)
            else:
                self.marks[i].setDisabled(1)
                self.marks_temp[i] = 'Remove'
                count = count + 1

        if count == len(self.marks):
            self.markAllCheckBox.setChecked(1)
        if count != len(self.marks):
            self.markAllCheckBox.setChecked(0)

        while 'Remove' in self.marks_temp:
            self.marks_temp.remove('Remove')

        print(len(self.marks))
        print(len(self.marks_temp))
        print(self.tests_dir_on)
        print(self.tests_dir_off)



    def changeRegion(self):
        for i in self.marks:
            self.tableLayout.removeWidget(i)
            print(i)
            i.deleteLater()

        for i in range(1, 13):
            tab = getattr(self, f"tab{i}")
            self.tableLayout.removeWidget(tab)
            tab = None

        self.initializeAttributes(str(self.regionComboBox.currentText()))
 
        self.createTabs()
        self.marks_temp = self.marks.copy()
        self.checkOnStart()
        self.tabs.update()



    def getPaths(self, line):
        app_data_dir = appdirs.user_data_dir('PhaseSwitcher', 'AlexEremeev')
        os.makedirs(app_data_dir, exist_ok=True)
        path_source = resource_path('conf/paths.json')
        path_target = os.path.join(app_data_dir, 'paths.json')

        if not os.path.exists(path_target):
            shutil.copy(path_source, path_target)

        with open(path_target, 'r') as f:
            data = json.loads(str(f.read()))
            directory_path = data.get(line, '')
            print("LOAD JSON: ", directory_path)

        self.tests_dir_on  = directory_path + "/tests/RegressionTests/Yaml/Drive/"
        self.tests_dir_off = directory_path + "/RegressionTests_Disabled/Yaml/Drive/"
        print(self.tests_dir_on)
        print(self.tests_dir_off)

        with open(resource_path('conf/data.json'), 'r') as f:
            self.paths = json.loads(str(f.read()))



    def generateGUID(self):
        self.guid = str(uuid.uuid4())
        self.guidField.setText(self.guid)
        pyperclip.copy(self.guid)



    def copyGUID(self):
        self.guid = self.guidField.text()
        pyperclip.copy(self.guid)
    
    def onPathsWindowClosed(self):
        self.changeRegion()




class PathsWindow(QWidget):

    closed = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.loadPathsFromFile()
        


    def setupUI(self):
        self.setWindowIcon(QIcon(resource_path('res/icon.ico')))
        self.setWindowTitle('Specify paths to projects')
        self.setGeometry(200, 200, 370, 300)
        self.createLabels()
        self.createLayout()
        self.setupLayout()



    def createLabels(self):
        self.labels = []
        self.fields = []
        self.paths = {}
        for label_text in ['Core', 'Turkey', 'Colombia', 'Germany', 'Poland', 'Mexico']:
            label = QLabel(label_text + ':')
            label.setFixedWidth(60)
            field = QLineEdit()
            self.labels.append(label)
            self.fields.append(field)
            self.paths[label_text] = field



    def createLayout(self):
        self.pathsLayout = QVBoxLayout()
        self.layouts = []
        self.buttons = []

        for label in self.labels:
            layout = QHBoxLayout()
            button = QPushButton(QIcon(resource_path('res/dots.png')), '')
            button.clicked.connect(self.browsePath)

            self.buttons.append(button)
            self.layouts.append(layout)



    def setupLayout(self):
        for layout, label, button in zip(self.layouts, self.labels, self.buttons):
            layout.addWidget(label)
            layout.addWidget(self.paths[label.text()[:-1]])
            layout.addWidget(button)
            self.pathsLayout.addLayout(layout)

        self.setLayout(self.pathsLayout)



    def browsePath(self):
        button = self.sender()
        index = self.buttons.index(button)
        directory = self.fields[index].text()
        print(directory)
        selected_directory = QFileDialog.getExistingDirectory(self, "Select Directory", directory)
        if selected_directory:
            label = self.labels[index]
            self.paths[label.text()[:-1]].setText(selected_directory)
            self.savePathsToFile()



    def loadPathsFromFile(self):
        app_data_dir = appdirs.user_data_dir('PhaseSwitcher', 'AlexEremeev')
        self.path_target = os.path.join(app_data_dir, 'paths.json')

        try:
            with open(self.path_target, 'r') as file:
                paths_data = json.load(file)
                for label_text, field_text in paths_data.items():
                    if label_text in self.paths:
                        self.paths[label_text].setText(field_text)
        except FileNotFoundError:
            pass



    def savePathsToFile(self):
        with open(self.path_target, 'w') as file:
            paths_data = {label_text: field.text() for label_text, field in self.paths.items()}
            json.dump(paths_data, file, indent=4)


    def closeEvent(self, event):
        self.savePathsToFile()
        self.closed.emit()  # Emit the closed signal
        event.accept()



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