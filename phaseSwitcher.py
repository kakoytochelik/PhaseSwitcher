import sys
import shutil
from pathlib import Path
import json
import os
import pyperclip
import uuid

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore



class tab(QTabWidget):
    def __init__(self):
        super(tab, self).__init__()
        
        self.marks = []
        self.disabled = []
        self.enabled = []
        self.error = []
        self.skipped = []

        self.GetPaths(1)

        self.setWindowTitle('Phase Switcher 4.0')
        self.setGeometry(500, 200, 400, 350)

        self.tableLayout = QVBoxLayout()
        self.headerLayout = QHBoxLayout()
        self.guidLayout = QHBoxLayout()
        self.runLayout = QHBoxLayout()
        self.tabs = QTabWidget()

        self.guidField = QLineEdit(self)
        self.guidField.setReadOnly(True)
        self.guidField.setPlaceholderText("GUID")

        self.guidGenerateButton = QPushButton()
        self.guidGenerateButton.setIcon(QIcon(resource_path('Refresh.png')))
        self.guidGenerateButton.clicked.connect(lambda:self.GenerateGUID())

        self.guidCopyButton = QPushButton()
        self.guidCopyButton.setIcon(QIcon(resource_path('copy.png')))
        self.guidCopyButton.clicked.connect(lambda:self.CopyGUID())

        self.markall = QCheckBox('Select all', self)
        self.markall.clicked.connect(lambda: self.MarkUnmarkAll(self.markall))

        self.setDefault = QPushButton("Default values")
        self.setDefault.clicked.connect(lambda: self.DefaultCheckboxes(self.setDefault))
        self.setDefault.setIcon(QIcon(resource_path('defaults.png')))

        self.cb = QComboBox()
        self.cb.addItems(["Core Drive", "Turkey", "Colombia", "Germany", "Poland", "Mexico"])
        self.cb.currentIndexChanged.connect(lambda: self.ChangeRegion())

        self.refresh = QPushButton("Refresh")
        self.refresh.clicked.connect(lambda: self.ChangeRegion())
        self.refresh.setIcon(QIcon(resource_path('Refresh.png')))

        self.run = QPushButton("Run")
        self.run.clicked.connect(lambda: self.DoTheThings())
        self.run.clicked.connect(lambda: self.ShowDialog())
        self.run.setIcon(QIcon(resource_path('continue.png')))



        self.CreateTabs()
        self.marks_temp = self.marks.copy()
        self.CheckOnStart()

        self.setLayout(self.tableLayout)


        self.tableLayout.addLayout(self.headerLayout)
        self.headerLayout.addWidget(self.cb)
        self.headerLayout.addWidget(self.refresh)
        self.headerLayout.addWidget(self.setDefault)
        self.headerLayout.addWidget(self.markall)
        self.tableLayout.addWidget(self.tabs)
        
        self.tableLayout.addLayout(self.guidLayout)
        self.guidLayout.addWidget(self.guidField)
        self.guidLayout.addWidget(self.guidGenerateButton)
        self.guidLayout.addWidget(self.guidCopyButton)

        self.tableLayout.addLayout(self.runLayout)
        self.runLayout.addWidget(self.run, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
    
    def CreateTabs(self):
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        self.tab8 = QWidget()
        self.tab9 = QWidget()
        self.tab10 = QWidget()
        self.tab11 = QWidget()
        self.tab12 = QWidget()

        self.tabs.addTab(self.tab1,"FirstTest")
        self.tabs.addTab(self.tab2,"Purchases subsystem 1")
        self.tabs.addTab(self.tab3,"Purchases subsystem 2")
        self.tabs.addTab(self.tab4,"Purchases subsystem 3")
        self.tabs.addTab(self.tab5,"Sales tests 1")
        self.tabs.addTab(self.tab6,"Sales tests 2")
        self.tabs.addTab(self.tab7,"Sales tests 3")
        self.tabs.addTab(self.tab8,"Sales tests 4")
        self.tabs.addTab(self.tab9,"Sales tests 5")
        self.tabs.addTab(self.tab10,"Smoke tests")
        self.tabs.addTab(self.tab11,"Templates")
        self.tabs.addTab(self.tab12,"Regions")

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.tab5UI()
        self.tab6UI()
        self.tab7UI()
        self.tab8UI()
        self.tab9UI()
        self.tab10UI()
        self.tab11UI()
        self.tab12UI()

    def tab1UI(self):
        self.t001 = QCheckBox('001_Company_tests', self)
        self.marks.append(self.t001)
        self.t001.clicked.connect(lambda: self.Uncheck(self.t001))

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase5_Vanessa_First_Test'))
        layout.addWidget(self.t001)
        layout.addStretch()
        self.tab1.setLayout(layout)

    def tab2UI(self):
        self.t003 = QCheckBox('003_I_test_purchases', self)
        self.marks.append(self.t003)
        self.t003.clicked.connect(lambda: self.Uncheck(self.t003))

        self.t006 = QCheckBox('006_Debit_note', self)
        self.marks.append(self.t006)
        self.t006.clicked.connect(lambda: self.Uncheck(self.t006))

        self.t0081 = QCheckBox('0081_Goods_issue_after_sales_invoice', self)
        self.marks.append(self.t0081)
        self.t0081.clicked.connect(lambda: self.Uncheck(self.t0081))

        self.t0085 = QCheckBox('0085_Monkey_tests', self)
        self.marks.append(self.t0085)
        self.t0085.clicked.connect(lambda: self.Uncheck(self.t0085))

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_5.3_Purchases_subsystem_tests'))
        layout.addWidget(self.t003)
        layout.addWidget(self.t006)
        layout.addWidget(self.t0081)
        layout.addWidget(self.t0085)
        layout.addStretch()
        self.tab2.setLayout(layout)

    def tab3UI(self):

        self.t0031 = QCheckBox('0031_Purchases_reverse_charge', self)
        self.marks.append(self.t0031)
        self.t0031.clicked.connect(lambda: self.Uncheck(self.t0031))

        self.t0032 = QCheckBox('0032_Purchases_ZERO_VAT', self)
        self.marks.append(self.t0032)
        self.t0032.clicked.connect(lambda: self.Uncheck(self.t0032))

        self.t0034 = QCheckBox('0034_Stocktaking_documents', self)
        self.marks.append(self.t0034)
        self.t0034.clicked.connect(lambda: self.Uncheck(self.t0034))

        self.t0035 = QCheckBox('0035_Goods_receipt', self)
        self.marks.append(self.t0035)
        self.t0035.clicked.connect(lambda: self.Uncheck(self.t0035))

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_5.3_Purchases_subsystem_tests_2'))

        layout.addWidget(self.t0031)
        layout.addWidget(self.t0032)
        layout.addWidget(self.t0034)
        layout.addWidget(self.t0035)
        layout.addStretch()
        self.tab3.setLayout(layout)

    def tab4UI(self):

        self.t0036 = QCheckBox('0036_Supplier_invoice_Continental', self)
        self.marks.append(self.t0036)
        self.t0036.clicked.connect(lambda: self.Uncheck(self.t0036))

        self.t0037 = QCheckBox('0037_Subcontractor_order_Continental', self)
        self.marks.append(self.t0037)
        self.t0037.clicked.connect(lambda: self.Uncheck(self.t0037))

        self.t0038 = QCheckBox('0038_Subcontractor_order_anglo-saxon', self)
        self.marks.append(self.t0038)
        self.t0038.clicked.connect(lambda: self.Uncheck(self.t0038))

        self.t0039 = QCheckBox('0039_Assembly_Disassembly', self)
        self.marks.append(self.t0039)
        self.t0039.clicked.connect(lambda: self.Uncheck(self.t0039))

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_5.3_Purchases_subsystem_tests_3'))

        layout.addWidget(self.t0036)
        layout.addWidget(self.t0037)
        layout.addWidget(self.t0038)
        layout.addWidget(self.t0039)
        layout.addStretch()
        self.tab4.setLayout(layout)

    def tab5UI(self):

        self.t0083 = QCheckBox('0083_Work_orders', self)
        self.marks.append(self.t0083)
        self.t0083.clicked.connect(lambda: self.Uncheck(self.t0083))

        self.t008 = QCheckBox('008_FIFO', self)
        self.marks.append(self.t008)
        self.t008.clicked.connect(lambda: self.Uncheck(self.t008))

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_5.4_Sales_test'))

        layout.addWidget(self.t0083)
        layout.addWidget(self.t008)
        layout.addStretch()
        self.tab5.setLayout(layout)

    def tab6UI(self):

        self.t002pt = QCheckBox('002_Payments_terms_Advance_payments', self)
        self.marks.append(self.t002pt)
        self.t002pt.clicked.connect(lambda: self.Uncheck(self.t002pt))

        self.t0020pt = QCheckBox('002_Production', self)
        self.marks.append(self.t0020pt)
        self.t0020pt.clicked.connect(lambda: self.Uncheck(self.t0020pt))

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_5.4_Sales_test_2'))

        layout.addWidget(self.t002pt)
        layout.addWidget(self.t0020pt)
        layout.addStretch()
        self.tab6.setLayout(layout)

    def tab7UI(self):

        self.t0051 = QCheckBox('0051_Credit_note_plus_GoodsReturn', self)
        self.marks.append(self.t0051)
        self.t0051.clicked.connect(lambda: self.Uncheck(self.t0051))

        self.t0052 = QCheckBox('0052_Credit_note_do_not_use_GR_and_TI', self)
        self.marks.append(self.t0052)
        self.t0052.clicked.connect(lambda: self.Uncheck(self.t0052))

        self.t0053 = QCheckBox('0053_Credit_note_withoutVat', self)
        self.marks.append(self.t0053)
        self.t0053.clicked.connect(lambda: self.Uncheck(self.t0053))

        self.t0086 = QCheckBox('0086_Monkey_tests', self)
        self.marks.append(self.t0086)
        self.t0086.clicked.connect(lambda: self.Uncheck(self.t0086))

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_5.4_Sales_test_3'))

        layout.addWidget(self.t0051)
        layout.addWidget(self.t0052)
        layout.addWidget(self.t0053)
        layout.addWidget(self.t0086)
        layout.addStretch()
        self.tab7.setLayout(layout)

    def tab8UI(self):

        self.t0082 = QCheckBox('0082_Retail_tests_sales_without_VAT', self)
        self.marks.append(self.t0082)
        self.t0082.clicked.connect(lambda: self.Uncheck(self.t0082))

        self.t0081 = QCheckBox('0081_Retail_tests_operations_with_VAT', self)
        self.marks.append(self.t0081)
        self.t0081.clicked.connect(lambda: self.Uncheck(self.t0081))

        self.t0041 = QCheckBox('0041_Loans_tests', self)
        self.marks.append(self.t0041)
        self.t0041.clicked.connect(lambda: self.Uncheck(self.t0041))

        self.t0042 = QCheckBox('0042_Loans_tests', self)
        self.marks.append(self.t0042)
        self.t0042.clicked.connect(lambda: self.Uncheck(self.t0042))

        self.t0043 = QCheckBox('0043_Loans_tests', self)
        self.marks.append(self.t0043)
        self.t0043.clicked.connect(lambda: self.Uncheck(self.t0043))

        self.t0044 = QCheckBox('0044_Loans_tests', self)
        self.marks.append(self.t0044)
        self.t0044.clicked.connect(lambda: self.Uncheck(self.t0044))

        self.t0045 = QCheckBox('0045_Foreign_currency_exchanges', self)
        self.marks.append(self.t0045)
        self.t0045.clicked.connect(lambda: self.Uncheck(self.t0045))

        self.t0046 = QCheckBox('0046_AR_AP_adjustment', self)
        self.marks.append(self.t0046)
        self.t0046.clicked.connect(lambda: self.Uncheck(self.t0046))

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_5.4_Sales_test_4'))

        layout.addWidget(self.t0082)
        layout.addWidget(self.t0081)
        layout.addWidget(self.t0041)
        layout.addWidget(self.t0042)
        layout.addWidget(self.t0043)
        layout.addWidget(self.t0044)
        layout.addWidget(self.t0045)
        layout.addWidget(self.t0046)

        layout.addStretch()
        self.tab8.setLayout(layout)

    def tab9UI(self):

        self.t002s = QCheckBox('002_Subcontracting', self)
        self.marks.append(self.t002s)
        self.t002s.clicked.connect(lambda: self.Uncheck(self.t002s))

        self.t0021 = QCheckBox('0021_Direct_debit', self)
        self.marks.append(self.t0021)
        self.t0021.clicked.connect(lambda: self.Uncheck(self.t0021))

        self.t007 = QCheckBox('007_I_test_users_creation', self)
        self.marks.append(self.t007)
        self.t007.clicked.connect(lambda: self.Uncheck(self.t007))

        self.t009 = QCheckBox('009_CRM', self)
        self.marks.append(self.t009)
        self.t009.clicked.connect(lambda: self.Uncheck(self.t009))

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_5.4_Sales_test_5'))

        layout.addWidget(self.t002s)
        layout.addWidget(self.t0021)
        layout.addWidget(self.t007)
        layout.addWidget(self.t009)
        layout.addStretch()
        self.tab9.setLayout(layout)

    def tab10UI(self):

        self.flt = QCheckBox('I_start_my_first_launch_templates', self)
        self.marks.append(self.flt)
        self.flt.clicked.connect(lambda: self.Uncheck(self.flt))

        self.fl = QCheckBox('I_start_my_first_launch', self)
        self.marks.append(self.fl)
        self.fl.clicked.connect(lambda: self.Uncheck(self.fl))

        self.t0084 = QCheckBox('0084_Monkey_tests', self)
        self.marks.append(self.t0084)
        self.t0084.clicked.connect(lambda: self.Uncheck(self.t0084))

        layout = QVBoxLayout()

        layout.addWidget(QLabel('Phase_6_Smoke_tests'))
        layout.addWidget(self.fl)
        layout.addWidget(self.t0084)

        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('Phase_10_Check_Update_Base_With_Templates'))
        layout.addWidget(self.flt)

        layout.addStretch()
        self.tab10.setLayout(layout)

    def tab11UI(self):

        self.t098 = QCheckBox('0098_Accounting_templates', self)
        self.marks.append(self.t098)
        self.t098.clicked.connect(lambda: self.Uncheck(self.t098))

        self.t099 = QCheckBox('0099_Manual_entries_and_subconto', self)
        self.marks.append(self.t099)
        self.t099.clicked.connect(lambda: self.Uncheck(self.t099))

        self.t100 = QCheckBox('0100_Templates_in_invoices', self)
        self.marks.append(self.t100)
        self.t100.clicked.connect(lambda: self.Uncheck(self.t100))

        self.t101 = QCheckBox('0101_Templates_in_documents_and_reports', self)
        self.marks.append(self.t101)
        self.t101.clicked.connect(lambda: self.Uncheck(self.t101))

        self.t102 = QCheckBox('0102_Accounting_entries_data_register', self)
        self.marks.append(self.t102)
        self.t102.clicked.connect(lambda: self.Uncheck(self.t102))

        self.t420 = QCheckBox('420_Templates')
        self.marks.append(self.t420)
        self.t420.clicked.connect(lambda: self.Uncheck(self.t420))  

        layout = QVBoxLayout()

        layout.addWidget(QLabel('Phase_7_Templates'))
        layout.addWidget(self.t098)
        layout.addWidget(self.t099)

        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('Phase_7_Templates_2'))
        layout.addWidget(self.t100)

        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('Phase_7_Templates_3'))
        layout.addWidget(self.t101)

        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('Phase_7_Templates_4'))
        layout.addWidget(self.t102)

        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('420_Templates (legacy/for regions):'))
        layout.addWidget(self.t420)

        layout.addStretch()
        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('Turn off tests on this tab before push! (Default values -> Run)'))
        
        self.tab11.setLayout(layout)
    
    def tab12UI(self):
        
        self.TE = QCheckBox('0089_Turkey_tests')
        self.marks.append(self.TE)
        self.TE.clicked.connect(lambda: self.Uncheck(self.TE))

        self.CE = QCheckBox('0089_Colombian_tests')
        self.marks.append(self.CE)
        self.CE.clicked.connect(lambda: self.Uncheck(self.CE))       

        self.GE = QCheckBox('0088_Germany_tests')
        self.marks.append(self.GE)
        self.GE.clicked.connect(lambda: self.Uncheck(self.GE))  

        self.PE = QCheckBox('0087_Poland_tests')
        self.marks.append(self.PE)
        self.PE.clicked.connect(lambda: self.Uncheck(self.PE))

        self.ME = QCheckBox('0089_Mexico_tests')
        # self.marks.append(self.ME)
        # self.ME.clicked.connect(lambda: self.Uncheck(self.ME))

        # Temp
        self.ME.setDisabled(1)
        self.ME.setChecked(0)
        # Temp



        layout = QVBoxLayout()

        layout.addWidget(QLabel('Turkey:'))
        layout.addWidget(self.TE)

        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('Colombia:'))
        layout.addWidget(self.CE)

        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('Germany:'))
        layout.addWidget(self.GE)

        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('Poland:'))
        layout.addWidget(self.PE)

        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('Mexico:'))
        layout.addWidget(self.ME)



        layout.addStretch()
        self.tab12.setLayout(layout)

    def MarkUnmarkAll(self, btn):
        if btn.isChecked() == False:
            for i in self.marks_temp:
                i.setChecked(0)
        if btn.isChecked() == True:
            for i in self.marks_temp:
                i.setChecked(1)

    def DefaultCheckboxes(self, btn):
        for i in self.marks_temp:
            i.setChecked(1)
            if i.text() == "0098_Accounting_templates":
              i.setChecked(0)
            if i.text() == "0099_Manual_entries_and_subconto":
              i.setChecked(0)
            if i.text() == "0100_Templates_in_invoices":
              i.setChecked(0)
            if i.text() == "0101_Templates_in_documents_and_reports":
              i.setChecked(0)  
            if i.text() == "0102_Accounting_entries_data_register":
              i.setChecked(0)
            if i.text() == "420_Templates":
              i.setChecked(0)  

    def Uncheck(self, btn):
        if btn.isChecked() == False:
            self.markall.setChecked(0)
        
    def DoTheThings(self):

        for i in self.marks:
            path_on = self.tests_dir_on + self.paths.get(i.text()) + "test/"
            path_off = self.tests_dir_off + self.paths.get(i.text()) + "test/"

            if i.isEnabled():

                if i.isChecked() == False:
                    if Path(str(path_on)).exists():
                        # disable folders here
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
                        # enable folders here
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

    def ShowDialog(self):
        enabled = "Tests enabled: " + str(len(self.enabled))
        disabled = 'Tests disabled: ' + str(len(self.disabled))
        error = 'Errors: ' + str(len(self.error))
        skipped = 'No changes: ' + str(len(self.skipped))

        QMessageBox.about(self, "Done", enabled + '\n' + disabled + '\n' + skipped + '\n' + error)

        
        self.enabled.clear()
        self.disabled.clear()
        self.error.clear()
        self.skipped.clear()

    def CheckOnStart(self):
        count = 0
        print("I'M IN")
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
            self.markall.setChecked(1)
        if count != len(self.marks):
            self.markall.setChecked(0)

        while 'Remove' in self.marks_temp:
            self.marks_temp.remove('Remove')

        print(len(self.marks))
        print(len(self.marks_temp))
        print(self.tests_dir_on)
        print(self.tests_dir_off)

    def ChangeRegion(self):
        for i in self.marks:
            self.tableLayout.removeWidget(i)
            print(i)
            i = None
        self.tableLayout.removeWidget(self.tab1)
        self.tab1 = None
        self.tableLayout.removeWidget(self.tab2)
        self.tab2 = None
        self.tableLayout.removeWidget(self.tab3)
        self.tab3 = None
        self.tableLayout.removeWidget(self.tab4)
        self.tab4 = None
        self.tableLayout.removeWidget(self.tab5)
        self.tab5 = None
        self.tableLayout.removeWidget(self.tab6)
        self.tab6 = None
        self.tableLayout.removeWidget(self.tab7)
        self.tab7 = None
        self.tableLayout.removeWidget(self.tab8)
        self.tab8 = None
        self.tableLayout.removeWidget(self.tab9)
        self.tab9 = None
        self.tableLayout.removeWidget(self.tab10)
        self.tab10 = None
        self.tableLayout.removeWidget(self.tab11)
        self.tab11 = None
        self.tableLayout.removeWidget(self.tab12)
        self.tab12 = None

        self.marks = []
        self.disabled = []
        self.enabled = []
        self.error = []
        self.skipped = []
        if str(self.cb.currentText()) == "Core Drive" :
            self.GetPaths(1)
        if str(self.cb.currentText()) == "Turkey" :
            self.GetPaths(4)
        if str(self.cb.currentText()) == "Colombia" :
            self.GetPaths(7)
        if str(self.cb.currentText()) == "Germany" :
            self.GetPaths(10)
        if str(self.cb.currentText()) == "Poland" :
            self.GetPaths(13)
        if str(self.cb.currentText()) == "Mexico" :
            self.GetPaths(16)
                   
        self.CreateTabs()
        self.marks_temp = self.marks.copy()
        self.CheckOnStart()
        self.tabs.update()

    def GetPaths(self, line):
        data = open("paths.txt").read().splitlines()
        print("\nCURRENT LINE:")
        print(data[line])
        self.tests_dir_on  = data[line] + "tests/RegressionTests/Yaml/Drive/"
        self.tests_dir_off = data[line] + "RegressionTests_Disabled/Yaml/Drive/"
        print(self.tests_dir_on)
        print(self.tests_dir_off)
        with open(resource_path('data.json'), 'r') as f:
            self.paths = json.loads(str(f.read()))

    def GenerateGUID(self):
        self.guid = str(uuid.uuid4())
        self.guidField.setText(self.guid)
        pyperclip.copy(self.guid)

    def CopyGUID(self):
        self.guid = self.guidField.text()
        pyperclip.copy(self.guid)

def main():
    app = QApplication(sys.argv)
    ex = tab()
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