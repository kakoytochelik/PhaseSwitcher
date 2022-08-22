import sys
import shutil
from pathlib import Path
import json

from PyQt6.QtWidgets import (
    QWidget, 
    QCheckBox, 
    QApplication,  
    QVBoxLayout, 
    QLabel, 
    QTabWidget, 
    QPushButton,
    QMessageBox,
    )


class tab(QTabWidget):
    def __init__(self, parent = None):
        super(tab, self).__init__(parent)
        
        self.marks = []
        self.disabled = []
        self.enabled = []
        self.error = []
        self.skipped = []

        data = open("paths.txt").read().splitlines()
        self.tests_dir_on  = data[0]
        self.tests_dir_off = data[1]

        with open('data.json', 'r') as f:
            self.paths = json.loads(str(f.read()))

        layout = QVBoxLayout()
        tabs = QTabWidget()
        self.markall = QCheckBox('Check all', self)
        self.markall.clicked.connect(lambda: self.MarkUnmarkAll(self.markall))

        run = QPushButton("Run")
        self.label = QLabel('')

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



        tabs.addTab(self.tab1,"Phase_5")
        tabs.addTab(self.tab2,"Phase_5.3")
        tabs.addTab(self.tab3,"Phase_5.3_2")
        tabs.addTab(self.tab4,"Phase_5.3_3")
        tabs.addTab(self.tab5,"Phase_5.4")
        tabs.addTab(self.tab6,"Phase_5.4_2")
        tabs.addTab(self.tab7,"Phase_5.4_3")
        tabs.addTab(self.tab8,"Phase_5.4_4")
        tabs.addTab(self.tab9,"Phase_5.4_5")
        tabs.addTab(self.tab10,"Phase_6")
        tabs.addTab(self.tab11,"Phase_7")



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


        self.marks_temp = self.marks.copy()


        self.setWindowTitle('Phase Switcher')
        self.setGeometry(60, 60, 350, 200)
        self.lblText = ''
        
        self.CheckOnStart()
        self.setLayout(layout)

        layout.addWidget(self.markall)
        layout.addWidget(tabs)
        layout.addWidget(self.label)
        layout.addWidget(run)
        run.clicked.connect(lambda: self.DoTheThings())
        run.clicked.connect(lambda: self.showdialog())
    


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

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_5.4_Sales_test_2'))

        layout.addWidget(self.t002pt)
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

        self.fl = QCheckBox('I_start_my_first_launch', self)
        self.marks.append(self.fl)
        self.fl.clicked.connect(lambda: self.Uncheck(self.fl))

        self.t0084 = QCheckBox('0084_Monkey_tests', self)
        self.marks.append(self.t0084)
        self.t0084.clicked.connect(lambda: self.Uncheck(self.t0084))

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_6_Smoke_tests '))

        layout.addWidget(self.fl)
        layout.addWidget(self.t0084)
        layout.addStretch()
        self.tab10.setLayout(layout)



    def tab11UI(self):

        self.flt = QCheckBox('I_start_my_first_launch_templates', self)
        self.marks.append(self.flt)
        self.flt.clicked.connect(lambda: self.Uncheck(self.flt))

        self.t420 = QCheckBox('420_Templates', self)
        self.marks.append(self.t420)
        self.t420.clicked.connect(lambda: self.Uncheck(self.t420))


        layout = QVBoxLayout()
        layout.addWidget(QLabel('Phase_7_Templates '))

        layout.addWidget(self.flt)
        layout.addWidget(self.t420)
        layout.addStretch()
        layout.addWidget(QLabel('(!) Turn off tests in this phase before push'))

        self.tab11.setLayout(layout)




    def MarkUnmarkAll(self, btn):
        if btn.isChecked() == False:
            for i in self.marks_temp:
                i.setChecked(0)
        if btn.isChecked() == True:
            for i in self.marks_temp:
                i.setChecked(1)



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

    def showdialog(self):
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

        while 'Remove' in self.marks_temp:
            self.marks_temp.remove('Remove')

        print(len(self.marks))
        print(len(self.marks_temp))

def main():
    app = QApplication(sys.argv)
    ex = tab()
    ex.show()
    sys.exit(app.exec())
	
if __name__ == '__main__':
   main()