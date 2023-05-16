from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import *
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5 import QtCore
from PyQt5.uic import loadUiType
import sys

from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from  datetime import date
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
import os

from datetime import datetime, timedelta
#import datetime
import mysql.connector

MainUI,_ = loadUiType('market.ui')
class Main(QMainWindow, MainUI):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        # self.timeEdit_6 = QtCore.QTimer(self)
        # self.timeEdit_6.timeout.connect(self.second)
        # self.timeEdit_6.start(1000)
        # self.c = canvas.Canvas(my_path,pagesize=letter)
        self.dateEdit.setDate(QDate.currentDate())  
        self.dateEdit_2.setDate(QDate.currentDate())
        self.dateEdit_3.setDate(QDate.currentDate())
        self.dateEdit_4.setDate(QDate.currentDate()) 
        self.dateEdit_5.setDate(QDate.currentDate())
        self.dateEdit_6.setDate(QDate.currentDate())
        self.dateEdit_7.setDate(QDate.currentDate())
        self.dateEdit_8.setDate(QDate.currentDate())
        self.dateEdit_9.setDate(QDate.currentDate())
        self.dateEdit_10.setDate(QDate.currentDate())
        self.dateEdit_11.setDate(QDate.currentDate())
        self.dateEdit_12.setDate(QDate.currentDate())
        self.dateEdit_13.setDate(QDate.currentDate())
        self.dateEdit_14.setDate(QDate.currentDate())        
        self.dateEdit_15.setDate(QDate.currentDate())
        self.dateEdit_16.setDate(QDate.currentDate())

        self.timeEdit.setTime(QTime.currentTime())        
        self.timeEdit_2.setTime(QTime.currentTime())        
        self.timeEdit_3.setTime(QTime.currentTime())        
        self.timeEdit_4.setTime(QTime.currentTime())       
        self.timeEdit_5.setTime(QTime.currentTime())
        self.timeEdit_6.setTime(QTime.currentTime())        
        self.timeEdit_7.setTime(QTime.currentTime())
        self.timeEdit_8.setTime(QTime.currentTime())
        self.timeEdit_9.setTime(QTime.currentTime())
        self.timeEdit_10.setTime(QTime.currentTime())
        self.timeEdit_11.setTime(QTime.currentTime())

        self.groupBox_14.hide()
        #self.tab_13.setEnabled(False)


        self.checkBox.stateChanged.connect(self.user_enabled)        
        self.comboBox_9.currentTextChanged.connect(self.imp_info)
        self.comboBox_15.activated.connect(self.shift_change)
        self.lineEdit_3.textEdited.connect(self.user_save_enabled)
        self.lineEdit_10.textEdited.connect(self.customer_save_enabled)
        self.lineEdit_25.textEdited.connect(self.item_save_enabled)    
        self.lineEdit_36.textEdited.connect(self.grp_save_enabled)
        self.lineEdit_38.textEdited.connect(self.company_save_enabled)
        self.lineEdit_42.textEdited.connect(self.place_save_enabled)
        self.lineEdit_69.textChanged.connect(self.total_buy_unit) 
        self.lineEdit_70.textChanged.connect(self.total_buy_unit) 
        self.lineEdit_66.textChanged.connect(self.buy_item_price) 
        self.lineEdit_65.textChanged.connect(self.total_sale_price) 
        self.lineEdit_55.textChanged.connect(self.total_earn) 
        self.lineEdit_65.textEdited.connect(self.item_pill_save_but)
        self.lineEdit_75.textEdited.connect(self.rebuypill_save_but)
        self.lineEdit_80.textEdited.connect(self.rebuypill_save_but)
        self.lineEdit_64.textChanged.connect(self.cash_rset)
        self.lineEdit_64.returnPressed.connect(self.salebill_save)        
        self.lineEdit_86.returnPressed.connect(self.get_sale_item_info)
        self.lineEdit_87.textChanged.connect(self.visa)
        # self.lineEdit_84.textChanged.connect(self.sale_item_add)        
        #dself.tableWidget_11.selectionModel().selectionChanged.connect(self.buybill_details_table_select)
        self.tableWidget.itemClicked.connect(self.user_table_select)
        self.tableWidget_2.itemClicked.connect(self.customer_table_select)
        self.tableWidget_3.itemClicked.connect(self.importer_table_select)
        self.tableWidget_4.itemClicked.connect(self.item_table_select)
        self.tableWidget_5.itemClicked.connect(self.grp_table_select)
        self.tableWidget_6.itemClicked.connect(self.company_table_select)
        self.tableWidget_7.itemClicked.connect(self.place_table_select)
        self.tableWidget_10.itemClicked.connect(self.buypill_table_select)
        self.tableWidget_11.itemClicked.connect(self.buybill_details_table_select)
        self.tableWidget_12.itemClicked.connect(self.rebuy_item_select)
        self.tableWidget_13.itemClicked.connect(self.sale_item_select)

        validator = QRegExpValidator(QRegExp(r'[0-9]+')) 
        
        self.lineEdit_73.setValidator(QIntValidator())
        self.lineEdit_73.setMaxLength(7)
        self.lineEdit_69.setValidator(QDoubleValidator())
        self.lineEdit_69.setMaxLength(7)
        self.lineEdit_70.setValidator(QDoubleValidator(0.00,999.99,2))
        self.lineEdit_70.setMaxLength(7)
        self.lineEdit_70.setValidator(validator)        
        self.pushButton_31.setEnabled(False)
        self.pushButton_35.setEnabled(False)
        self.pushButton_40.setEnabled(False)
        self.pushButton_43.setEnabled(False)
        

        self.db_connect()
        self.handel_buttons()
        self.user_table_fill()
        self.customer_table_fill()
        self.importer_table_fill()
        self.item_table_fill()
        self.grp_table_fill()
        self.company_table_fill()
        self.place_table_fill()
        self.grp_combo_fill()
        self.company_combo_fill()
        self.place_combo_fill()
        self.Hodor_table_fill()
        self.user_combo_fill()
        self.importer_combo_fill()
        self.item_combo_fill()
        

    def db_connect(self):
        self.db = mysql.connector.connect(user='root', password=str(1234),
                    host='localhost', db='market')
        self.cur = self.db.cursor(buffered=True)

    def handel_buttons(self):
        
        self.pushButton.clicked.connect(self.user_add_new)
        self.pushButton_2.clicked.connect(self.user_save)
        self.pushButton_3.clicked.connect(self.user_update)
        self.pushButton_4.clicked.connect(self.user_delete)
        self.pushButton_5.clicked.connect(self.user_search)

        self.pushButton_6.clicked.connect(self.customer_add_new)
        self.pushButton_7.clicked.connect(self.customer_save)
        self.pushButton_8.clicked.connect(self.customer_update)
        self.pushButton_9.clicked.connect(self.customer_delete)
        self.pushButton_10.clicked.connect(self.customer_search)

        self.pushButton_11.clicked.connect(self.importer_search)
        self.pushButton_12.clicked.connect(self.importer_add_new)
        self.pushButton_13.clicked.connect(self.importer_save)
        self.pushButton_14.clicked.connect(self.importer_update)
        self.pushButton_15.clicked.connect(self.importer_delete)        

        self.pushButton_16.clicked.connect(self.item_add_new)
        self.pushButton_17.clicked.connect(self.item_save)
        self.pushButton_18.clicked.connect(self.item_update)
        self.pushButton_19.clicked.connect(self.item_delete)
        self.pushButton_20.clicked.connect(self.item_search)

        self.pushButton_21.clicked.connect(self.grp_save)
        self.pushButton_22.clicked.connect(self.grp_delete)
        self.pushButton_23.clicked.connect(self.company_save)
        self.pushButton_24.clicked.connect(self.company_delete)
        self.pushButton_25.clicked.connect(self.place_save)

        self.pushButton_26.clicked.connect(self.place_delete)
        self.pushButton_27.clicked.connect(self.hodor_save)
        self.pushButton_28.clicked.connect(self.hodor_delete)
        self.pushButton_29.clicked.connect(self.hodor_update)
        self.pushButton_30.clicked.connect(self.hodor_report)

        self.pushButton_31.clicked.connect(self.buy_bill_save)
        self.pushButton_32.clicked.connect(self.buy_bill_add_new)
        self.pushButton_33.clicked.connect(self.buy_bill_add_new)
        self.pushButton_34.clicked.connect(self.buy_bill_save_item)
        self.pushButton_35.clicked.connect(self.buy_bill_update)

        self.pushButton_36.clicked.connect(self.buy_bill_item_search)
        self.pushButton_37.clicked.connect(self.buy_bill_item_update)
        self.pushButton_38.clicked.connect(self.buy_bill_search)
        self.pushButton_39.clicked.connect(self.buy_bill_item_delete)
        self.pushButton_40.clicked.connect(self.buy_bill_delete)

        self.pushButton_41.clicked.connect(self.buy_bill_return_to)
        self.pushButton_42.clicked.connect(self.row_go)
        self.pushButton_43.clicked.connect(self.buy_bill_return)
        self.pushButton_44.clicked.connect(self.rebuy_bill_add)
        self.pushButton_45.clicked.connect(self.rebuy_bill_save)

        self.pushButton_46.clicked.connect(self.rebuy_bill_search)
        self.pushButton_47.clicked.connect(self.rebuypill_update)
        self.pushButton_48.clicked.connect(self.rebuy_delete)
        self.pushButton_49.clicked.connect(self.sale_item_update)        
        self.pushButton_50.clicked.connect(self.sale_item_delete)

        self.pushButton_51.clicked.connect(self.grp_add_new)
        self.pushButton_52.clicked.connect(self.salebill_add_new)
        self.pushButton_53.clicked.connect(self.clear_fields)
        self.pushButton_54.clicked.connect(self.grp_update)
        self.pushButton_55.clicked.connect(self.company_add_new)
        
        self.pushButton_56.clicked.connect(self.company_update)
        self.pushButton_57.clicked.connect(self.place_update)
        self.pushButton_58.clicked.connect(self.place_add_new)
        self.pushButton_59.clicked.connect(self.cashier_daily_tally)
        self.pushButton_60.clicked.connect(self.most_selling_item)
        
        self.pushButton_61.clicked.connect(self.daily_sales)
        self.pushButton_62.clicked.connect(self.sales_range_report)
        self.pushButton_63.clicked.connect(self.buy_range_report)
        self.pushButton_64.clicked.connect(self.Items_inventory)
        self.pushButton_65.clicked.connect(self.salebill_print)

# =========== Usuers ===========
    def user_save_enabled(self):
        self.pushButton_2.setEnabled(True)

    def user_table_select(self):
        row = self.tableWidget.currentItem().row()
        id = self.tableWidget.item(row, 0).text()
        sql = f"SELECT * FROM users WHERE id={id}"
        self.cur.execute(sql) #, [(id)])
        data = self.cur.fetchone()
        self.lineEdit_2.setText(str(data[0]))
        self.lineEdit_4.setText(str(data[2]))
        self.lineEdit_3.setText(str(data[1]))
        self.comboBox.setCurrentText(data[3])
        self.lineEdit_5.setText(str(data[4]))
        self.lineEdit_6.setText(str(data[6]))
        self.comboBox_2.setCurrentText(data[5])
        self.lineEdit_7.setText(str(data[7]))
        self.lineEdit_8.setText(str(data[8]))
        self.dateEdit.setDate(data[9])
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)


    def user_enabled(self):
        if self.checkBox.isChecked() == True:
            self.groupBox_3.setEnabled(True)
        else:
            self.checkBox.setChecked(False)

    def user_table_fill(self):        
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        self.cur.execute('''SELECT * FROM users ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_pos)

    def user_add_new(self):
        self.cur.execute(''' SELECT id FROM users ORDER BY id ''')
        row = self.cur.fetchall()
        self.lineEdit_2.setText(str(row[-1][0] + 1))
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')      
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.groupBox_3.setEnabled(False)
        self.checkBox.setChecked(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)

    def user_save(self):        
        user_full_name = self.lineEdit_3.text()
        user_nid = self.lineEdit_4.text()
        user_gender = self.comboBox.currentText()
        user_phone = self.lineEdit_5.text()
        user_address = self.lineEdit_6.text()
        user_job = self.comboBox_2.currentText()
        user_date = self.dateEdit.date()
        user_date = user_date.toString(QtCore.Qt.ISODate)
        user_name = self.lineEdit_7.text()
        user_password = self.lineEdit_8.text()
        if user_full_name == '' or user_nid == '' or user_phone == '' :
            QMessageBox.warning(self, 'رسالة تحذير', 'من فضلك ادخل جميع البيانات المطلوبة', QMessageBox.Ok)
            return
        if self.checkBox.isChecked() == True:
            is_user = True
        else:
            is_user = False
            user_name = ''
            user_password = ''

        self.cur.execute('''
            INSERT INTO users(user_fullname, un_id, user_gender, user_phone, user_address, user_job, user_date, user_name, user_password, is_user)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ''',(user_full_name, user_nid, user_gender, user_phone, user_address, user_job, user_date, user_name, user_password, is_user))

        self.db.commit()        
        self.user_table_fill()
        self.groupBox_3.setEnabled(False)
        self.checkBox.setChecked(False)
        self.pushButton_2.setEnabled(False)

    def user_search(self):
        name = self.lineEdit.text()
        if name == '' :
            QMessageBox.warning(self, 'رسالة تنبيه', 'من فضلك ادخل الاسم المراد البحث عنه', QMessageBox.Ok)
            return
        sql = f''' SELECT * FROM users WHERE user_fullname LIKE '%{name}%' '''
        # sql = f"SELECT *, ROW_NUMBER()\
        #     OVER (ORDER BY id) FROM users WHERE user_fullname LIKE\
        #     '%{name}%' "        
        self.cur.execute(sql)
        data = self.cur.fetchall()        
        if data == []:
            QMessageBox.warning(self, 'لا توجد بيانات',  'لا توجد بيانات تخص المعلومات التي أدخلتها', QMessageBox.Ok)
            return
        self.lineEdit_2.setText(str(data[0][0]))
        self.lineEdit_4.setText(str(data[0][2]))
        self.lineEdit_3.setText(str(data[0][1]))
        self.comboBox.setCurrentText(data[0][3])
        self.lineEdit_5.setText(str(data[0][4]))
        self.lineEdit_6.setText(str(data[0][6]))
        self.comboBox_2.setCurrentText(data[0][5])
        self.lineEdit_7.setText(str(data[0][7]))
        self.lineEdit_8.setText(str(data[0][8]))
        self.dateEdit.setDate(data[0][9])
        self.lineEdit.setText('')
        matching_item = self.tableWidget.findItems(self.lineEdit_3.text(), Qt.MatchContains)        
        self.tableWidget.setCurrentItem(matching_item[0])
        
    def user_update(self):
        u_id = self.lineEdit_2.text()
        user_full_name = self.lineEdit_3.text()
        user_nid = self.lineEdit_4.text()
        user_gender = self.comboBox.currentText()
        user_phone = self.lineEdit_5.text()
        user_address = self.lineEdit_6.text()
        user_job = self.comboBox_2.currentText()
        user_date = self.dateEdit.date()
        user_date = user_date.toString(QtCore.Qt.ISODate)
        user_name = self.lineEdit_7.text()
        user_password = self.lineEdit_8.text()
        if self.checkBox.isChecked() == True:
            is_user = True
        else:
            is_user = False
            user_name = ''
            user_password = ''

        self.cur.execute('''
        UPDATE users SET un_id=%s, user_fullname=%s, user_gender=%s, user_phone=%s, user_address=%s, user_job=%s, user_name=%s, user_password=%s, user_date=%s, is_user=%s
        WHERE id=%s''', (user_nid, user_full_name, user_gender, user_phone, user_address, user_job, user_name, user_password, user_date, is_user, u_id))

        self.db.commit()       
        self.user_table_fill()
        self.groupBox_3.setEnabled(False)
        self.checkBox.setChecked(False)

    def user_delete(self):
        
        u_id = self.lineEdit_2.text()
        sql = ('''DELETE FROM users WHERE id = %s ''')
        self.cur.execute(sql, [(u_id)])

        self.db.commit()       
        self.user_table_fill()

# =========== Customers ===========
    
    def customer_save_enabled(self):
        self.pushButton_7.setEnabled(True)

    def customer_table_select(self):
        row = self.tableWidget_2.currentItem().row()
        id = self.tableWidget_2.item(row, 0).text()
        sql = f"SELECT * FROM customers WHERE id={id}"
        self.cur.execute(sql) #, [(id)])
        data = self.cur.fetchone()
        h, m, s = map(int, (str(data[8]).split(":")))
        x = QTime(h, m)
        self.lineEdit_9.setText(str(data[0]))
        self.lineEdit_10.setText(str(data[1]))
        self.lineEdit_11.setText(str(data[5]))
        self.comboBox_3.setCurrentText(data[2])
        self.lineEdit_12.setText(str(data[3]))
        self.lineEdit_13.setText(str(data[4]))       
        self.dateEdit_2.setDate(data[7])
        self.timeEdit.setTime(x)
        self.pushButton_8.setEnabled(True)
        self.pushButton_9.setEnabled(True)


    def customer_clear(self):
        self.lineEdit_9.setText('')
        self.lineEdit_10.setText('')
        self.lineEdit_11.setText('')
        self.lineEdit_12.setText('')      
        self.lineEdit_13.setText('')
        self.lineEdit_14.setText('')   
    
    def customer_table_fill(self):        
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        self.cur.execute('''
        SELECT id, customer_name, customer_type, customer_gender, customer_phone, customer_address, customer_balance, customer_date FROM customers
        ''')
        data = self.cur.fetchall()

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_pos)

    def customer_add_new(self):
        self.cur.execute('''
        SELECT id FROM customers
        ''')
        row = self.cur.fetchall()
        self.lineEdit_9.setText(str(row[-1][0] + 1))
        self.lineEdit_10.setText('')
        self.lineEdit_11.setText('')
        self.lineEdit_12.setText('')
        self.lineEdit_13.setText('')      
        self.lineEdit_14.setText('')
        self.pushButton_7.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_9.setEnabled(False)

    def customer_save(self):        
        customer_name = self.lineEdit_10.text()
        customer_type = self.lineEdit_11.text()
        customer_gender = self.comboBox_3.currentText()
        customer_phone = self.lineEdit_12.text()
        customer_address = self.lineEdit_13.text()
        customer_balance = self.lineEdit_14.text()
        customer_date = self.dateEdit_2.date()
        customer_date = customer_date.toString(QtCore.Qt.ISODate)
        customer_time = self.timeEdit.time()
        customer_time = customer_time.toString(QtCore.Qt.ISODate)
        if customer_name == '' or customer_phone == '' or customer_balance == '' :
            QMessageBox.warning(self, 'رسالة تحذير', 'من فضلك ادخل جميع البيانات المطلوبة', QMessageBox.Ok)
            return
        self.cur.execute('''
            INSERT INTO customers(customer_name, customer_type, customer_gender, customer_phone, customer_address, customer_balance, customer_date, customer_time)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
              ''',(customer_name, customer_type,customer_gender, customer_phone, customer_address, customer_balance, customer_date, customer_time))

        self.db.commit()        
        self.customer_table_fill()
        self.pushButton_7.setEnabled(False)

    def customer_search(self):
        name = self.lineEdit_15.text()
        if name == '' :
            QMessageBox.warning(self, 'رسالة تنبيه', 'من فضلك ادخل الاسم المراد البحث عنه', QMessageBox.Ok)
            return        
        sql = f''' SELECT * FROM customers WHERE customer_name LIKE '%{name}%' '''                    
        self.cur.execute(sql)
        data = self.cur.fetchall()        
        if data == []:
            QMessageBox.warning(self, 'لا توجد بيانات',  'لا توجد بيانات تخص المعلومات التي أدخلتها', QMessageBox.Ok)
            return        
        h, m, s = map(int, (str(data[0][8])).split(":"))        
        x = QTime(h, m)        
        self.lineEdit_9.setText(str(data[0][0]))
        self.lineEdit_10.setText(str(data[0][1]))
        self.lineEdit_11.setText(str(data[0][5]))
        self.comboBox_3.setCurrentText(data[0][2])
        self.lineEdit_12.setText(str(data[0][3]))
        self.lineEdit_13.setText(str(data[0][4]))
        self.lineEdit_14.setText(str(data[0][6]))
        self.dateEdit_2.setDate(data[0][7])        
        self.timeEdit.setTime(x) 
        self.lineEdit_15.setText('')
        item = self.tableWidget_2.findItems(self.lineEdit_10.text(), Qt.MatchContains)        
        self.tableWidget_2.setCurrentItem(item[0])

    def customer_update(self):
        id = self.lineEdit_9.text()
        customer_name = self.lineEdit_10.text()
        customer_gender = self.comboBox_3.currentText()
        customer_phone = self.lineEdit_12.text()
        customer_address = self.lineEdit_13.text()
        customer_type = self.lineEdit_11.text()
        customer_balance = self.lineEdit_14.text()
        customer_date = self.dateEdit_2.date()
        customer_date = customer_date.toString(QtCore.Qt.ISODate)
        customer_time = self.timeEdit.time()
        customer_time = customer_time.toString(QtCore.Qt.ISODate)
        
        self.cur.execute('''
        UPDATE customers SET customer_name=%s, customer_gender=%s, customer_phone=%s, customer_address=%s, customer_type=%s, customer_balance=%s, customer_date=%s, customer_time=%s
        WHERE id=%s''', (customer_name, customer_gender, customer_phone, customer_address, customer_type, customer_balance, customer_date, customer_time, id))

        self.db.commit()       
        self.customer_table_fill()

    def customer_delete(self):        
        id = self.lineEdit_9.text()
        sql = ('''DELETE FROM customers WHERE id = %s ''')
        self.cur.execute(sql, [(id)])

        self.db.commit()       
        self.customer_table_fill()
        self.customer_clear()

# =========== Importers ===========
    def importer_table_select(self):
        row = self.tableWidget_3.currentItem().row()
        id = self.tableWidget_3.item(row, 0).text()
        sql = f"SELECT * FROM importers WHERE id = {id}"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        h, m, s = map(int, (str(data[7])).split(":"))
        x = QTime(h, m)
        self.lineEdit_17.setText(str(data[0]))
        self.lineEdit_18.setText(str(data[1]))
        self.lineEdit_19.setText(str(data[4]))
        self.lineEdit_20.setText(str(data[2]))
        self.lineEdit_21.setText(str(data[3]))
        self.lineEdit_22.setText(str(data[5]))
        self.dateEdit_3.setDate(data[6])        
        self.timeEdit_2.setTime(x)
        self.pushButton_14.setEnabled(True)
        self.pushButton_15.setEnabled(True)

    def importer_clear(self):
        self.lineEdit_17.setText('')
        self.lineEdit_18.setText('')
        self.lineEdit_19.setText('')
        self.lineEdit_20.setText('')      
        self.lineEdit_21.setText('')
        self.lineEdit_22.setText('')

    def importer_table_fill(self):        
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)
        self.cur.execute('''
        SELECT id, importer_name, importer_type, importer_phone, importer_address, importer_balance, importer_date, importer_time FROM importers
        ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_pos)

    def importer_add_new(self):
        self.cur.execute('''
        SELECT id FROM importers
        ''')
        row = self.cur.fetchall()
        self.lineEdit_17.setText(str(row[-1][0] + 1))
        self.lineEdit_18.setText('')
        self.lineEdit_19.setText('')
        self.lineEdit_20.setText('')
        self.lineEdit_21.setText('')      
        self.lineEdit_22.setText('')
        self.pushButton_13.setEnabled(False)
        self.pushButton_14.setEnabled(False)
        self.pushButton_15.setEnabled(False)
        

    def importer_save(self):        
        importer_name = self.lineEdit_18.text()
        importer_type = self.lineEdit_19.text()       
        importer_phone = self.lineEdit_20.text()
        importer_address = self.lineEdit_21.text()
        importer_balance = self.lineEdit_22.text()
        importer_date = self.dateEdit_3.date()
        importer_date = importer_date.toString(QtCore.Qt.ISODate)
        importer_time = self.timeEdit_2.time()
        importer_time = importer_time.toString(QtCore.Qt.ISODate)
        self.cur.execute('''
            INSERT INTO importers(importer_name, importer_type, importer_phone, importer_address, importer_balance, importer_date, importer_time)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
              ''',(importer_name, importer_type, importer_phone, importer_address, importer_balance, importer_date, importer_time))

        self.db.commit()        
        self.importer_table_fill()

    def importer_search(self):
        name = self.lineEdit_16.text()
        if name == '' :
            QMessageBox.warning(self, 'رسالة تنبيه', 'من فضلك ادخل الاسم المراد البحث عنه', QMessageBox.Ok)
            return        
        sql = f''' SELECT * FROM importers WHERE importer_name LIKE '%{name}%' '''            
        self.cur.execute(sql)
        data = self.cur.fetchall()
        if data == []:
            QMessageBox.warning(self, 'لا توجد بيانات',  'لا توجد بيانات تخص المعلومات التي أدخلتها', QMessageBox.Ok)
            return
        h, m, s = map(int, (str(data[0][7]).split(":")))
        x = QTime(h, m)
        self.lineEdit_17.setText(str(data[0][0]))
        self.lineEdit_18.setText(str(data[0][1]))
        self.lineEdit_19.setText(str(data[0][4]))
        self.lineEdit_20.setText(str(data[0][2]))
        self.lineEdit_21.setText(str(data[0][3]))
        self.lineEdit_22.setText(str(data[0][5]))
        self.timeEdit_2.setTime(x)
        self.dateEdit_3.setDate(data[0][6])
        self.lineEdit_16.setText('')
        item = self.tableWidget_3.findItems(self.lineEdit_18.text(), Qt.MatchContains)        
        self.tableWidget_3.setCurrentItem(item[0])


    def importer_update(self):
        id = self.lineEdit_17.text()
        importer_name = self.lineEdit_18.text()        
        importer_type = self.lineEdit_19.text()
        importer_phone = self.lineEdit_20.text()
        importer_address = self.lineEdit_21.text()
        importer_balance = self.lineEdit_22.text()
        importer_date = self.dateEdit_3.date()
        importer_date = importer_date.toString(QtCore.Qt.ISODate)
        importer_time = self.timeEdit_2.time()
        importer_time = importer_time.toString(QtCore.Qt.ISODate)
        
        self.cur.execute('''
        UPDATE importers SET importer_name=%s, importer_phone=%s, importer_address=%s, importer_type=%s, importer_balance=%s, importer_date=%s, importer_time=%s
        WHERE id=%s''', (importer_name, importer_phone, importer_address, importer_type, importer_balance, importer_date, importer_time, id))
        self.db.commit()       
        self.importer_table_fill()

    def importer_delete(self):        
        id = self.lineEdit_17.text()
        sql = ('''DELETE FROM importers WHERE id = %s ''')
        self.cur.execute(sql, [(id)])

        self.db.commit()       
        self.importer_table_fill()
        self.importer_clear()

# =========== Items ===========
    def item_save_enabled(self):
        self.pushButton_17.setEnabled(True)


    def item_clear(self):
        self.lineEdit_24.setText('')
        self.lineEdit_25.setText('')
        self.lineEdit_26.setText('')
        self.lineEdit_27.setText('')      
        self.lineEdit_28.setText('')
        self.lineEdit_29.setText('')
        self.lineEdit_30.setText('')
        self.lineEdit_31.setText('')

    def item_table_fill(self):        
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)
        self.cur.execute('''
        SELECT * FROM items
        ''')
        data = self.cur.fetchall()

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_pos)

    def item_table_select(self):
        row = self.tableWidget_4.currentItem().row()
        id = self.tableWidget_4.item(row, 0).text()
        sql = f"SELECT * FROM items WHERE id = {id}"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        self.lineEdit_24.setText(str(data[0]))
        self.lineEdit_25.setText(str(data[1]))
        self.lineEdit_26.setText(str(data[2]))
        self.comboBox_4.setCurrentText(str(data[3]))
        self.comboBox_5.setCurrentText(str(data[4]))
        self.comboBox_6.setCurrentText(str(data[5]))
        self.lineEdit_27.setText(str(data[6]))        
        self.lineEdit_28.setText(str(data[7]))
        self.lineEdit_29.setText(str(data[9]))
        self.lineEdit_30.setText(str(data[8]))
        self.lineEdit_31.setText(str(data[10]))
        self.dateEdit_4.setDate(data[11])

        self.pushButton_18.setEnabled(True)
        self.pushButton_19.setEnabled(True)



    def item_add_new(self):
        self.cur.execute('''
        SELECT id FROM items ORDER BY id ''')
        row = self.cur.fetchall()
        self.lineEdit_23.setText('')
        self.lineEdit_24.setText(str(row[-1][0] + 1))        
        self.lineEdit_25.setText('')
        self.lineEdit_26.setText('')
        self.lineEdit_27.setText('')
        self.lineEdit_28.setText('')      
        self.lineEdit_29.setText('')
        self.lineEdit_30.setText('')
        self.lineEdit_31.setText('')        
        self.pushButton_18.setEnabled(False)
        self.pushButton_19.setEnabled(False)

    def item_save(self):        
        item_barcode = self.lineEdit_25.text()
        item_name = str(self.lineEdit_26.text())       
        item_price = self.lineEdit_27.text()
        item_qty = self.lineEdit_28.text()
        item_limit = self.lineEdit_29.text()
        item_discount = self.lineEdit_30.text()
        item_unit = self.lineEdit_31.text()
        item_group = self.comboBox_4.currentText()
        item_company = self.comboBox_5.currentText()
        item_place = self.comboBox_6.currentText()
        item_date = self.dateEdit_4.date()
        item_date = item_date.toString(QtCore.Qt.ISODate)
        if item_name == '' or item_price == '' or item_qty == '' :
            QMessageBox.warning(self, 'بيانات ناقصة', 'من فضلك أدخل البيانات الناقصة', QMessageBox.Ok)
            return
        self.cur.execute('''
            INSERT INTO items(item_barcode, item_name, item_group, item_company, item_place, item_price, item_qty, item_limit, item_discount, item_unit, item_date)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ''',(item_barcode, item_name, item_group, item_company, item_place, item_price, item_qty, item_limit, item_discount, item_unit, item_date))

        self.db.commit()        
        self.item_table_fill()
        self.item_combo_fill()
        self.item_clear()
        self.pushButton_17.setEnabled(False)

    def item_search(self):
        name = self.lineEdit_23.text()
        if name == '' :
            QMessageBox.warning(self, 'بيانات ناقصة', 'من فضلك أدخل البيانات المطلوب البحث عنها', QMessageBox.Ok)
            return        
        sql = f''' SELECT * FROM items WHERE item_name LIKE '%{name}%' '''            
        self.cur.execute(sql)
        data = self.cur.fetchone()        

        self.lineEdit_24.setText(str(data[0]))
        self.lineEdit_25.setText(str(data[1]))
        self.lineEdit_26.setText(str(data[2]))
        self.comboBox_4.setCurrentText(data[3])
        self.comboBox_5.setCurrentText(data[4])
        self.comboBox_6.setCurrentText(data[5])
        self.lineEdit_27.setText(str(data[6]))
        self.lineEdit_28.setText(str(data[7]))
        self.lineEdit_29.setText(str(data[8]))
        self.lineEdit_30.setText(str(data[9]))
        self.lineEdit_31.setText(str(data[10]))
        self.dateEdit_2.setDate(data[11])
        item = self.tableWidget_4.findItems(name, Qt.MatchContains)        
        self.tableWidget_4.setCurrentItem(item[0])
        

    def item_update(self):
        id = self.lineEdit_24.text()
        item_barcode = self.lineEdit_25.text()
        item_name = self.lineEdit_26.text()        
        item_price = self.lineEdit_27.text()
        item_qty = self.lineEdit_28.text()
        item_limit = self.lineEdit_29.text()
        item_discount = self.lineEdit_30.text()
        item_unit = self.lineEdit_31.text()
        item_group = self.comboBox_4.currentText()
        item_company = self.comboBox_5.currentText()
        item_place = self.comboBox_6.currentText()
        item_date = self.dateEdit_4.date()
        item_date = item_date.toString(QtCore.Qt.ISODate)        
        self.cur.execute('''
        UPDATE items SET item_barcode=%s, item_name=%s, item_group=%s, item_company=%s, item_place=%s, item_price=%s, item_qty=%s, item_discount=%s, item_limit=%s, item_unit=%s, item_date=%s
        WHERE id=%s''', (item_barcode, item_name, item_group, item_company, item_place, item_price, item_qty, item_limit, item_discount, item_unit, item_date, id))        
        self.db.commit()
        self.item_table_fill()
        

    def item_delete(self):        
        id = self.lineEdit_24.text()
        sql = ('''DELETE FROM items WHERE id = %s ''')
        self.cur.execute(sql, [(id)])

        self.db.commit()       
        self.item_table_fill()
        self.item_clear()
        self.pushButton_16.setEnabled(True)        
        self.pushButton_18.setEnabled(False)
        self.pushButton_19.setEnabled(False)

# =========== Groups ===========

    def grp_add_new(self):
        self.cur.execute('''SELECT id FROM grps ORDER BY id ''')
        row = self.cur.fetchall()        
        self.lineEdit_35.setText(str(row[-1][0] + 1))        
        self.lineEdit_36.setText('')
        self.pushButton_22.setEnabled(False)
        self.pushButton_54.setEnabled(False)

    def grp_save(self):        
        grp_name = self.lineEdit_36.text()
        grp_date = self.dateEdit_5.date()
        grp_date = grp_date.toString(QtCore.Qt.ISODate)
        grp_time = self.timeEdit_3.time()
        grp_time = grp_time.toString(QtCore.Qt.ISODate)
        grp_user = self.comboBox_17.currentText()

        self.cur.execute('''
            INSERT INTO grps(grp_name, grp_date, grp_time, grp_user)
            VALUES(%s, %s, %s, %s)
              ''',(grp_name, grp_date, grp_time, grp_user))

        self.db.commit()        
        self.grp_table_fill()
        self.pushButton_21.setEnabled(False)

    def grp_update(self):
        id = self.lineEdit_35.text()
        grp_name = self.lineEdit_36.text()        
        grp_date = self.dateEdit_5.date()
        grp_date = grp_date.toString(QtCore.Qt.ISODate)
        grp_time = self.timeEdit_3.time()
        grp_time = grp_time.toString(QtCore.Qt.ISODate)
        grp_user = self.comboBox_17.currentText()        
        self.cur.execute('''
        UPDATE grps SET grp_name=%s, grp_date=%s, grp_time=%s, grp_user=%s
        WHERE id=%s''', (grp_name, grp_date, grp_time, grp_user, id))
        self.db.commit()       
        self.grp_table_fill()

    def grp_delete(self):
        id = self.lineEdit_35.text()
        sql = ('''DELETE FROM grps WHERE id = %s ''')
        self.cur.execute(sql, [(id)])

        self.db.commit()       
        self.grp_table_fill()
        self.grp_combo_fill()

    def grp_combo_fill(self):
        self.comboBox_4.clear()
        self.cur.execute('''SELECT grp_name FROM grps ORDER BY id ''')
        grops = self.cur.fetchall()
        for grop in grops:
            self.comboBox_4.addItem(grop[0])

    def grp_save_enabled(self):
        self.pushButton_21.setEnabled(True)

    def grp_table_fill(self):        
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        self.cur.execute(''' SELECT * FROM grps ''')
        data = self.cur.fetchall()

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_pos)


    def grp_table_select(self):
        row = self.tableWidget_5.currentItem().row()
        id = self.tableWidget_5.item(row, 0).text()
        sql = f"SELECT * FROM grps WHERE id={id}"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        self.lineEdit_35.setText(str(data[0]))
        self.lineEdit_36.setText(str(data[1]))
        self.comboBox_17.setCurrentText(str(data[4]))                     
        self.dateEdit_2.setDate(data[2])
        #self.timeEdit_3.setTime(data[3])        
        self.pushButton_21.setEnabled(False)
        self.pushButton_22.setEnabled(True)
        self.pushButton_54.setEnabled(True)

#=========== Companies ===========

    def company_add_new(self):
        self.cur.execute('''SELECT id FROM companies ORDER BY id ''')
        row = self.cur.fetchall()        
        self.lineEdit_37.setText(str(row[-1][0] + 1))        
        self.lineEdit_38.setText('')
        self.pushButton_24.setEnabled(False)
        self.pushButton_56.setEnabled(False)

    def company_save(self):        
        company_name = self.lineEdit_38.text()
        company_date = self.dateEdit_6.date()
        company_date = company_date.toString(QtCore.Qt.ISODate)
        company_time = self.timeEdit_4.time()
        company_time = company_time.toString(QtCore.Qt.ISODate)
        company_user = self.comboBox_18.currentText()

        self.cur.execute('''
            INSERT INTO companies(company_name, company_date, company_time, company_user)
            VALUES(%s, %s, %s, %s)
              ''',(company_name, company_date, company_time, company_user))

        self.db.commit()        
        self.company_table_fill()
        self.pushButton_23.setEnabled(False)

    def company_update(self):
        id = self.lineEdit_37.text()
        company_name = self.lineEdit_38.text()        
        company_date = self.dateEdit_6.date()
        company_date = company_date.toString(QtCore.Qt.ISODate)
        company_time = self.timeEdit_4.time()
        company_time = company_time.toString(QtCore.Qt.ISODate)
        company_user = self.comboBox_18.currentText()        
        self.cur.execute('''
        UPDATE companies SET company_name=%s, company_date=%s, company_time=%s, company_user=%s
        WHERE id=%s''', (company_name, company_date, company_time, company_user, id))
        self.db.commit()       
        self.company_table_fill()

    def company_delete(self):
        id = self.lineEdit_37.text()
        sql = ('''DELETE FROM companies WHERE id = %s ''')
        self.cur.execute(sql, [(id)])

        self.db.commit()       
        self.company_table_fill()
        self.company_combo_fill()

    def company_combo_fill(self):
        self.comboBox_5.clear()
        self.cur.execute('''SELECT company_name FROM companies ORDER BY id ''')
        companies = self.cur.fetchall()
        for company in companies:
            self.comboBox_5.addItem(company[0])

    def company_save_enabled(self):
        self.pushButton_23.setEnabled(True)

    def company_table_fill(self):        
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)
        self.cur.execute('''
        SELECT * FROM companies
        ''')
        data = self.cur.fetchall()

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_6.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_pos)

    def company_table_select(self):
        row = self.tableWidget_6.currentItem().row()
        id = self.tableWidget_6.item(row, 0).text()
        sql = f"SELECT * FROM companies WHERE id={id}"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        self.lineEdit_37.setText(str(data[0]))
        self.lineEdit_38.setText(str(data[1]))
        self.comboBox_18.setCurrentText(str(data[4]))                     
        self.dateEdit_6.setDate(data[2])
        #self.timeEdit_4.setTime(data[3])        
        self.pushButton_23.setEnabled(False)
        self.pushButton_24.setEnabled(True)
        self.pushButton_56.setEnabled(True)

#=========== Places ===========

    def place_add_new(self):
        self.cur.execute('''SELECT id FROM places ORDER BY id ''')
        row = self.cur.fetchall()        
        self.lineEdit_41.setText(str(row[-1][0] + 1))        
        self.lineEdit_42.setText('')
        self.pushButton_26.setEnabled(False)
        self.pushButton_57.setEnabled(False)

    def place_save(self):        
        place_name = self.lineEdit_42.text()
        place_date = self.dateEdit_7.date()
        place_date = place_date.toString(QtCore.Qt.ISODate)
        place_time = self.timeEdit_5.time()
        place_time = place_time.toString(QtCore.Qt.ISODate)
        place_user = self.comboBox_19.currentText()

        self.cur.execute('''
            INSERT INTO places(place_name, place_date, place_time, place_user)
            VALUES(%s, %s, %s, %s)
              ''',(place_name, place_date, place_time, place_user))

        self.db.commit()        
        self.place_table_fill()
        self.pushButton_25.setEnabled(False)

    def place_update(self):
        id = self.lineEdit_41.text()
        place_name = self.lineEdit_42.text()        
        place_date = self.dateEdit_7.date()
        place_date = place_date.toString(QtCore.Qt.ISODate)
        place_time = self.timeEdit_5.time()
        place_time = place_time.toString(QtCore.Qt.ISODate)
        place_user = self.comboBox_19.currentText()        
        self.cur.execute('''
        UPDATE places SET place_name=%s, place_date=%s, place_time=%s, place_user=%s
        WHERE id=%s''', (place_name, place_date, place_time, place_user, id))
        self.db.commit()       
        self.place_table_fill()

    def place_delete(self):
        id = self.lineEdit_41.text()
        sql = ('''DELETE FROM places WHERE id = %s ''')
        self.cur.execute(sql, [(id)])

        self.db.commit()       
        self.place_table_fill()
        self.place_combo_fill()

    def place_combo_fill(self):
        self.comboBox_6.clear()
        self.cur.execute('''SELECT place_name FROM places ORDER BY id ''')
        places = self.cur.fetchall()
        for place in places:
            self.comboBox_6.addItem(place[0])

    def place_save_enabled(self):
        self.pushButton_25.setEnabled(True)

    def place_table_fill(self):        
        self.tableWidget_7.setRowCount(0)
        self.tableWidget_7.insertRow(0)
        self.cur.execute(''' SELECT * FROM places ''')
        data = self.cur.fetchall()

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_7.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_7.rowCount()
            self.tableWidget_7.insertRow(row_pos)

    def place_table_select(self):
        row = self.tableWidget_7.currentItem().row()
        id = self.tableWidget_7.item(row, 0).text()
        sql = f"SELECT * FROM places WHERE id={id}"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        self.lineEdit_41.setText(str(data[0]))
        self.lineEdit_42.setText(str(data[1]))
        self.comboBox_19.setCurrentText(str(data[4]))                     
        self.dateEdit_7.setDate(data[2])
        #self.timeEdit_5.setTime(data[3])        
        self.pushButton_25.setEnabled(False)
        self.pushButton_26.setEnabled(True)
        self.pushButton_57.setEnabled(True)

#=========== حضور وانصراف ===========
    
    def Hodor_table_fill(self):        
        self.tableWidget_8.setRowCount(0)
        self.tableWidget_8.insertRow(0)
        self.cur.execute(''' SELECT * FROM hodoor_ensraf ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):            
            for col , item in enumerate(form):                
                if col == 3:                    
                    sql = '''SELECT user_fullname FROM users WHERE id=%s'''
                    self.cur.execute(sql, [((item))])
                    emp_name = self.cur.fetchone()                   
                    if emp_name != None:                        
                        employee_name = emp_name[0]
                        self.tableWidget_8.setItem(row, col, QTableWidgetItem((employee_name)))
                else:                    
                    self.tableWidget_8.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_8.rowCount()
            self.tableWidget_8.insertRow(row_pos)

    def hodor_save(self):

        self.timeEdit_7.setTime(QTime.currentTime())
        emp_name = self.comboBox_7.currentText()
        he_date = self.dateEdit_8.date()
        he_date = he_date.toString(QtCore.Qt.ISODate)        
        sql = ('''SELECT id FROM users WHERE user_fullname = %s ''')
        self.cur.execute(sql, [(emp_name)])
        data = self.cur.fetchone()
        he_name_id = data[0]

        sql = ('''SELECT he_come FROM hodoor_ensraf WHERE he_date = %s AND he_employee_id = %s''')
        self.cur.execute(sql, [(he_date), (he_name_id)])
        data = self.cur.fetchone()
        if data != '00:00:00' :            
            msgbox = QMessageBox(QMessageBox.Warning, "تنويه", "لقد تم تسجيل حضور الموظف : %s بالفعل هذا اليوم" % emp_name, QMessageBox.Ok)
            msgbox.exec_()
            return
        he_time = self.timeEdit_6.time()
        he_time = he_time.toString(QtCore.Qt.ISODate)        
        he_come = self.timeEdit_7.time()
        he_come = he_come.toString(QtCore.Qt.ISODate)        
        he_go = '' # he_go.toString(QtCore.Qt.ISODate)
        he_diff = 0 # self.lineEdit_44.text()
        he_note = '' # self.lineEdit_45.text()
        he_user = '' # self.lineEdit_46.text()
        self.cur.execute('''
            INSERT INTO hodoor_ensraf(he_date, he_time, he_employee_id, he_come, he_go, he_difference, he_note, he_user)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
              ''',(he_date, he_time, he_name_id, he_come, he_go, he_diff, he_note, he_user))                     
        
        msgbox = QMessageBox(QMessageBox.Information, "تنويه", "تم تسجيل حضور الموظف :  %s" % emp_name, QMessageBox.Ok)
        msgbox.exec_()    
        self.db.commit()        
        self.Hodor_table_fill()

    def hodor_delete(self):
        emp_name = self.comboBox_7.currentText()
        sql = ('''SELECT id FROM users WHERE user_fullname = %s ''')
        self.cur.execute(sql, [(emp_name)])
        data = self.cur.fetchone()
        sql = ('''DELETE FROM hodoor_ensraf WHERE he_employee_id = %s ''')
        self.cur.execute(sql, [(data[0])])

        self.db.commit()       
        self.Hodor_table_fill()

    def hodor_update(self):
        self.timeEdit_8.setTime(QTime.currentTime())
        he_date = self.dateEdit_8.date()
        he_date = he_date.toString(QtCore.Qt.ISODate)       
        he_time = self.timeEdit_6.time()
        he_time = he_time.toString(QtCore.Qt.ISODate) 
        emp_name = self.comboBox_7.currentText()
        sql = ('''SELECT id FROM users WHERE user_fullname = %s ''')
        self.cur.execute(sql, [(emp_name)])
        data = self.cur.fetchone()
        sql = ('''SELECT he_come, he_go FROM hodoor_ensraf WHERE he_employee_id=%s AND he_date = %s ''')
        self.cur.execute(sql, [(data[0]), (he_date)])
        dat = self.cur.fetchone()
        he_come = str(dat[0])
        he_go = str(dat[1])
        if he_come == '00:00:00' :            
            QMessageBox.warning(self, 'تنويه', 'من فضلك يجب تسجيل الحضور أولا', QMessageBox.Ok)
            return
        if he_go != '0:00:00' :
            msgbox = QMessageBox(QMessageBox.Warning, "تنويه", "لقد تم تسجيل انصراف الموظف : %s بالفعل هذا اليوم" % emp_name, QMessageBox.Ok)
            msgbox.exec_()   
            return
        h, m, s = map(int, (he_come).split(":"))
        self.timeEdit_7.setTime(QTime(h, m))
        he_come = datetime.strptime(he_come,"%H:%M:%S")
        he_go =  self.timeEdit_8.time()
        he_go = he_go.toString(QtCore.Qt.ISODate)
        he_go = datetime.strptime(he_go, '%H:%M:%S')        
        he_diff = timedelta(hours=(he_go.hour - he_come.hour), \
                      minutes=(he_go.minute - he_come.minute), \
                      seconds=(he_go.second - he_come.second))
        
        self.lineEdit_44.setText(str(he_diff))
        self.cur.execute('''
        UPDATE hodoor_ensraf SET he_go=%s, he_difference=%s WHERE he_employee_id=%s AND he_date = %s''', (he_go, he_diff, data[0], he_date))

        self.db.commit()          
        self.Hodor_table_fill()

        msgbox = QMessageBox(QMessageBox.Information, "تنويه", "تم تسجيل انصراف الموظف :  %s" % emp_name, QMessageBox.Ok)
        msgbox.exec_()

#=========== تقارير الحضور والانصراف ===========
    def hodor_report(self):

        total_time = 0
        date_1 = self.dateEdit_9.date()        
        date_1 = date_1.toString(QtCore.Qt.ISODate)       
        #date_1 = datetime.datetime.strptime(date_1, '%Y-%m-%d').date()
        date_2 = self.dateEdit_10.date()
        date_2 = date_2.toString(QtCore.Qt.ISODate)        
        #date_2 = datetime.datetime.strptime(date_2, '%Y-%m-%d').date()
        emp_name = self.comboBox_8.currentText()
        sql = ('''SELECT id FROM users WHERE user_fullname = %s ''')
        self.cur.execute(sql, [(emp_name)])
        data = self.cur.fetchone()

        self.tableWidget_9.setRowCount(0)
        self.tableWidget_9.insertRow(0)

        sql = '''SELECT he_employee_id, he_date, \
            he_come, he_go, he_difference, \
            he_note, he_user FROM hodoor_ensraf \
            WHERE (he_employee_id=%s \
            AND  he_date BETWEEN %s AND %s)'''
        
        self.cur.execute(sql, [data[0], date_1, date_2])
        data = self.cur.fetchall()
        if data == [] :
            QMessageBox.warning(self, 'بيانات غير موجودة', 'لاتوجد معلومات تطابق البيانات التي أدخلتها', QMessageBox.Ok)
            return 
        
        for row, form in enumerate(data):            
            for col , item in enumerate(form):                
                if col == 0:                    
                    sql = '''SELECT user_fullname FROM users WHERE id=%s'''
                    self.cur.execute(sql, [((item))])                                      
                    emp_name = self.cur.fetchone()                    
                    if emp_name != None:
                        employee_name = emp_name[0]                        
                        self.tableWidget_9.setItem(row, col, QTableWidgetItem(employee_name))
                elif col == 4:                    
                    item = str(item)                    
                    h, m, s = map(int, item.split(":"))                    
                    total_time += 3600*h + 60*m + s                    
                    self.tableWidget_9.setItem(row, col, QTableWidgetItem(str(item)))
                else:                    
                    self.tableWidget_9.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_9.rowCount()
            self.tableWidget_9.insertRow(row_pos)            
        total_time = ("%02d:%02d:%02d" % (total_time//3600, total_time//60%60, total_time%60))    
        self.lineEdit_47.setText(str(row_pos))
        self.lineEdit_48.setText(str(total_time))

#=========== فاتورة الشراء ===========
    def importer_combo_fill(self):
        self.comboBox_9.clear()
        self.comboBox_10.clear()
        self.cur.execute('''SELECT importer_name, importer_phone, importer_balance FROM importers ORDER BY id ''')
        importers = self.cur.fetchall()
        # self.lineEdit_49.setText(str(importers[0][1]))
        # self.lineEdit_50.setText(str(importers[0][2]))
        for importer in importers:
            self.comboBox_9.addItem(importer[0])
            self.comboBox_10.addItem(importer[0])

    def user_combo_fill(self):
        self.comboBox_7.clear()
        self.comboBox_8.clear()        
        self.comboBox_11.clear()
        self.comboBox_14.clear()
        self.comboBox_15.clear()
        self.comboBox_20.clear()
        self.comboBox_17.clear()
        self.comboBox_18.clear()
        self.comboBox_19.clear()
        self.cur.execute('''SELECT user_fullname, user_job FROM users ORDER BY id ''')
        users = self.cur.fetchall()        
        for user in users:            
            self.comboBox_7.addItem(user[0])
            self.comboBox_8.addItem(user[0])            
            self.comboBox_11.addItem(user[0])    
            self.comboBox_14.addItem(user[0])
            if user[1] == 'كاشير' :
                self.comboBox_15.addItem(user[0])
                self.comboBox_20.addItem(user[0])
            self.comboBox_17.addItem(user[0])
            self.comboBox_18.addItem(user[0])
            self.comboBox_19.addItem(user[0])
            

    def item_combo_fill(self):        
        self.comboBox_12.clear()
        self.comboBox_13.clear()
        self.comboBox_16.clear()
        self.cur.execute('''SELECT item_name FROM items ORDER BY id ''')
        items = self.cur.fetchall()
        for item in items:            
            self.comboBox_12.addItem(item[0])
            self.comboBox_13.addItem(item[0])
            self.comboBox_16.addItem(item[0])
    
    def imp_info(self):
        imp_name = self.comboBox_9.currentText()
        sql = '''SELECT importer_phone, importer_balance FROM importers WHERE importer_name=%s'''
        self.cur.execute(sql, [(imp_name)])
        data = self.cur.fetchone()
        self.lineEdit_49.setText(str(data[0]))
        self.lineEdit_50.setText(str(data[1]))

    def buy_bill_add_new(self):
        self.lineEdit_68.setText('')
        self.lineEdit_71.setText('')
        self.lineEdit_67.setText('0')
        self.lineEdit_69.setText('1')
        self.lineEdit_70.setText('0')
        self.lineEdit_66.setText('1')
        self.lineEdit_65.setText('0')
        self.lineEdit_55.setText('0')
        self.lineEdit_74.setText('0')
        self.lineEdit_54.setText('0')
        self.lineEdit_53.setText('0')
        self.pushButton_37.setEnabled(False)
        self.pushButton_39.setEnabled(False)
        self.pushButton_33.setEnabled(True)
        self.pushButton_41.setEnabled(True)        
        
    def buy_bill_save_item(self):
        minus = float(self.lineEdit_58.text())
        totalB = float(self.lineEdit_56.text())        
        totalG = float(self.lineEdit_57.text())
        buypill_id = self.lineEdit_73.text()
        invoice_no = self.lineEdit_72.text()
        item_name = self.comboBox_12.currentText()
        buy_unit = self.lineEdit_68.text()
        buy_unit_count = self.lineEdit_69.text()
        unit_price = self.lineEdit_70.text()
        sale_unit = self.lineEdit_71.text()        
        total_buy = self.lineEdit_67.text()
        item_count_peruint = self.lineEdit_66.text()
        item_buy_price = self.lineEdit_74.text()
        buy_item_sale = self.lineEdit_65.text()
        total_sale = self.lineEdit_54.text() 
        buy_minus = self.lineEdit_55.text()      
        minus += float(self.lineEdit_55.text())        
        buy_earn = self.lineEdit_53.text()
        totalB += float(self.lineEdit_67.text())        
        self.lineEdit_56.setText(str(totalB))
        totalG += float(self.lineEdit_54.text())
        self.lineEdit_57.setText(str(totalG))
        self.lineEdit_58.setText(str(minus)) 

        self.cur.execute('''
            INSERT INTO buypill_details( buypill_id, item_name, buy_invoice_no, buy_unit, buy_unit_count, unit_price, sale_unit, item_count_in_buyunit, item_buy_price, buy_item_sale, total_buy, total_sale, buy_minus, buy_earn)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ''',(buypill_id, item_name, invoice_no, buy_unit, buy_unit_count, unit_price, sale_unit, item_count_peruint, item_buy_price, buy_item_sale, total_buy, total_sale, buy_minus, buy_earn))

        self.cur.execute(''' SELECT item_qty FROM items WHERE item_name=%s ''', [(item_name)])
        data = self.cur.fetchone()        
        
        item_qty = int(buy_unit_count) + data[0]

        self.cur.execute(''' UPDATE items SET item_qty=%s, item_price=%s WHERE item_name=%s'''
        , (item_qty, buy_item_sale, item_name))        

        self.db.commit()
        self.pushButton_31.setEnabled(True)
        self.pushButton_34.setEnabled(False)
        self.pushButton_32.setEnabled(False)
        self.pushButton_38.setEnabled(False)
        self.buy_item_table_fill()
        self.buy_bill_add_new()
        QMessageBox.warning(self, 'رسالة تأكيد', 'تم حفظ البيانات بنجاج', QMessageBox.Ok)

    def buy_item_table_fill(self):        
        total_buy = 0
        total_sale = 0
        buy_minus = 0        
        pill_id = self.lineEdit_52.text()
        self.tableWidget_11.setRowCount(0)
        self.tableWidget_11.insertRow(0)
        sql = "SELECT * FROM buypill_details WHERE buypill_id = %s"
        self.cur.execute(sql, [(pill_id)] )
        data = self.cur.fetchall()        
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_11.setItem(row, col, QTableWidgetItem(str(item)))
                if col == 11:                    
                    total_buy += float(item)
                elif col == 12:
                    total_sale += float(item)
                elif col == 13:
                    buy_minus += float(item)

                col += 1
            row_pos = self.tableWidget_11.rowCount()
            self.tableWidget_11.insertRow(row_pos)        
        if total_buy == 0 :
            sql = f"DELETE FROM buypill WHERE id={pill_id} "
            self.cur.execute(sql)

            sql = f"DELETE FROM operations WHERE buy_id={pill_id}"
            self.cur.execute(sql)

            self.db.commit()

        sql = f"UPDATE buypill SET buy_totalG={total_sale}, buy_totalB={total_buy}, buy_minus={buy_minus} WHERE id={pill_id} "
        self.cur.execute(sql)

        sql = f"UPDATE operations SET buy_totalB={total_buy}, buy_extra_exp={buy_minus} WHERE buy_id={pill_id} "
        self.cur.execute(sql)
        self.db.commit()
        self.pushButton_34.setEnabled(False)

    def buy_bill_add_new(self):
        if self.lineEdit_51.text() == '':
            QMessageBox.warning(self, 'بيانات ناقصة', 'من فضلك أدخل رقم فاتورة المورد', QMessageBox.Ok)
            return        
        #self.cur.execute("SELECT * FROM buypill WHERE id=(SELECT max(id) FROM buypill)")
        self.cur.execute("SELECT MAX( id ) FROM buypill")
        id = self.cur.fetchone()        
        # هذه الخطوة للتغلب فيما إذا تم حذف السجل الأخير من قاعدة البيانات
        self.cur.execute(f"ALTER TABLE buypill AUTO_INCREMENT = {id[0]}")
        self.cur.execute("SELECT MAX( id ) FROM buypill")
        id = self.cur.fetchone()        
        # self.cur.execute("SELECT id FROM buypill ORDER BY id")
        # data = self.cur.fetchall()
        #print(data[-1][0])
        #id = self.cur.lastrowid        
        self.lineEdit_52.setText(str(id[0]+1))
        self.lineEdit_73.setText(str(id[0]+1))
        self.lineEdit_72.setText(self.lineEdit_51.text())        
        self.pushButton_34.setEnabled(False)
        self.pushButton_36.setEnabled(False)
        self.pushButton_37.setEnabled(False)
        self.pushButton_39.setEnabled(False)
        self.pushButton_43.setEnabled(False)        
        self.tabWidget_4.setCurrentIndex(1)
    
    def buy_bill_return_to(self):
        self.pushButton_33.setEnabled(True)
        self.pushButton_34.setEnabled(False)
        self.pushButton_36.setEnabled(True)
        self.pushButton_37.setEnabled(False)
        self.pushButton_39.setEnabled(False)
        self.pushButton_41.setEnabled(False)
        self.tableWidget_11.setRowCount(0)
        self.tableWidget_11.insertRow(0)        
        self.lineEdit_54.setText('0')
        self.lineEdit_55.setText('0')
        self.lineEdit_65.setText('0')
        self.lineEdit_66.setText('1')
        self.lineEdit_67.setText('0')
        self.lineEdit_68.setText('')
        self.lineEdit_69.setText('1')
        self.lineEdit_70.setText('0')
        self.lineEdit_71.setText('')
        self.lineEdit_72.setText('')
        self.lineEdit_73.setText('')
        self.lineEdit_74.setText('0')
        self.lineEdit_53.setText('0')
        self.pushButton_33.setEnabled(False)
        self.tabWidget_4.setCurrentIndex(0)

    def buy_bill_save(self):
        buy_pill_date = self.dateEdit_11.date()
        buy_pill_date = buy_pill_date.toString(QtCore.Qt.ISODate)
        buy_pill__time = self.timeEdit_9.time()
        buy_pill__time = buy_pill__time.toString(QtCore.Qt.ISODate) 
        invoice_no = self.lineEdit_51.text()
        buy_id = self.lineEdit_52.text()
        importer = self.comboBox_9.currentText()
        user = self.comboBox_11.currentText()
        cash = self.checkBox_2.isChecked()
        credit = self.checkBox_3.isChecked()        
        totalG = self.lineEdit_57.text()
        totalB = self.lineEdit_56.text()
        buy_minus = self.lineEdit_58.text()

        sql = '''SELECT id FROM importers WHERE importer_name = %s'''
        self.cur.execute(sql, [(importer)])
        data = self.cur.fetchone()
        importer_id = data[0]
        sql = '''SELECT id FROM users WHERE user_fullname = %s''' 
        self.cur.execute(sql, [(user)])
        data = self.cur.fetchone()
        user_id = data[0]

        self.cur.execute('''
            INSERT INTO buypill(buy_date, buy_time, buy_invoice_no, buy_importer_id, buy_cash, buy_postpone, buy_user_id, buy_totalG, buy_totalB, buy_minus)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ''',(buy_pill_date, buy_pill__time, invoice_no, importer_id, cash, credit, user_id, totalG, totalB, buy_minus))

        self.cur.execute("INSERT INTO operations\
            (buy_id, buy_totalB, buy_extra_exp, \
            oper_date, oper_time, oper_user) \
            VALUES(%s, %s, %s, %s, %s, %s)", \
            (buy_id, totalB, buy_minus, \
            buy_pill_date, buy_pill__time, user))

        self.db.commit()
        self.buy_item_table_fill()
        self.buy_bill_table_fill()
        self.lineEdit_51.setText('')
        self.lineEdit_52.setText('')
        self.lineEdit_72.setText('')
        self.lineEdit_73.setText('')
        self.pushButton_31.setEnabled(False)
        self.pushButton_32.setEnabled(True)
        self.pushButton_34.setEnabled(False)
        self.pushButton_36.setEnabled(True)
        self.pushButton_38.setEnabled(True)
        self.pushButton_43.setEnabled(True)       
    
    def buy_bill_table_fill(self):
        pill_id = self.lineEdit_52.text()
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.insertRow(0)
        sql = "SELECT * FROM buypill WHERE id = %s "
        self.cur.execute(sql, [(pill_id)] )
        data = self.cur.fetchall()        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 4:                    
                    sql = '''SELECT importer_name FROM importers WHERE id=%s'''
                    self.cur.execute(sql, [((item))])                    
                    imp_name = self.cur.fetchone()                    
                    if imp_name != None:
                        importer_name = imp_name[0]                        
                        self.tableWidget_10.setItem(row, col, QTableWidgetItem(importer_name))
                elif col == 7:                    
                    sql = '''SELECT user_fullname FROM users WHERE id=%s'''
                    self.cur.execute(sql, [((item))])                    
                    emp_name = self.cur.fetchone()                    
                    if emp_name != None:
                        employee_name = emp_name[0]                        
                        self.tableWidget_10.setItem(row, col, QTableWidgetItem(employee_name))
                else:
                    self.tableWidget_10.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_10.rowCount()
            self.tableWidget_10.insertRow(row_pos)
    
    def total_buy_unit(self):
        buy_unit_count = self.lineEdit_69.text()
        unit_price = self.lineEdit_70.text()
        sale_unit = self.lineEdit_71.text()
        x = int(buy_unit_count) * float(unit_price)
        total_buy = self.lineEdit_67.setText(str(x))
        total_buy = self.lineEdit_67.text()        
        self.buy_item_price

    def buy_item_price(self):        
        buy_unit_count = self.lineEdit_69.text()
        item_count_peruint = self.lineEdit_66.text()
        x = int(buy_unit_count) * int(item_count_peruint)
        total_buy = self.lineEdit_67.text()        
        y = float(total_buy) / x
        y = float("{:.2f}".format(y))
        item_buy_price = self.lineEdit_74.setText(str(y))
        item_buy_price = self.lineEdit_74.text()
        self.total_sale_price

    def total_sale_price(self):
        buy_unit_count = self.lineEdit_69.text()
        item_count_peruint = self.lineEdit_66.text()
        total_buy = self.lineEdit_67.text()
        x = float(total_buy)
        buy_item_sale = self.lineEdit_65.text()
        y = int(buy_unit_count) * int(item_count_peruint) * float(buy_item_sale)
        total_sale = self.lineEdit_54.setText(str(y))
        total_sale = self.lineEdit_54.text()
        #self.lineEdit_57.setText(self.lineEdit_54.text())
        buy_minus = self.lineEdit_55.text()
        z = x + float(buy_minus)
        buy_earn = self.lineEdit_53.setText(str(y-z))
        buy_earn = self.lineEdit_53.text()

    def total_earn(self):
        x = self.lineEdit_67.text()
        y = self.lineEdit_54.text()
        z = self.lineEdit_55.text()
        i = float(y) - float(x) - float(z)
        buy_earn = self.lineEdit_53.setText(str(i))
        buy_earn = self.lineEdit_53.text()
    
    def item_pill_save_but(self):
        if self.pushButton_37.isEnabled():
            self.pushButton_34.setEnabled(False)
        else:
            self.pushButton_34.setEnabled(True)

    def buy_bill_update(self):
        id = self.lineEdit_52.text()
        buy_pill_date = self.dateEdit_11.date()
        buy_pill_date = buy_pill_date.toString(QtCore.Qt.ISODate)
        buy_pill__time = self.timeEdit_9.time()
        buy_pill__time = buy_pill__time.toString(QtCore.Qt.ISODate) 
        invoice_no = self.lineEdit_51.text()        
        importer = self.comboBox_9.currentText()
        user = self.comboBox_11.currentText()
        cash = self.checkBox_2.isChecked()
        credit = self.checkBox_3.isChecked()
        totalG = self.lineEdit_57.text()
        totalB = self.lineEdit_56.text()
        buy_minus = self.lineEdit_58.text()   

        sql = '''SELECT id FROM importers WHERE importer_name = %s'''
        self.cur.execute(sql, [(importer)])
        data = self.cur.fetchone()
        importer_id = data[0]
        sql = '''SELECT id FROM users WHERE user_fullname = %s''' 
        self.cur.execute(sql, [(user)])
        data = self.cur.fetchone()
        user_id = data[0]

        self.cur.execute('''
            UPDATE buypill SET buy_date=%s, buy_time=%s, buy_invoice_no=%s, buy_importer_id=%s, buy_cash=%s, buy_postpone=%s, buy_user_id=%s, buy_totalG=%s, buy_totalB=%s, buy_minus=%s WHERE id=%s
              ''',(buy_pill_date, buy_pill__time, invoice_no, importer_id, cash, credit, user_id, totalG, totalB, buy_minus, id))

        self.cur.execute("UPDATE operations SET buy_totalB=%s, buy_extra_exp=%s WHERE buy_id=%s", (totalB, buy_minus, id))
        self.db.commit()
        self.buy_bill_table_fill()        
        QMessageBox.warning(self, 'تأكيد بيانات', 'لقد تم تعديل البيانات بنجاح', QMessageBox.Ok )
        self.buy_bill_return()
        self.lineEdit_56.setText('0')
        self.lineEdit_57.setText('0')
        self.lineEdit_58.setText('0')

    def buy_bill_search(self):
        self.groupBox_14.show()
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.insertRow(0)        
        sql = "SELECT * FROM buypill"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_10.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_10.rowCount()
            self.tableWidget_10.insertRow(row_pos)
        self.pushButton_32.setEnabled(False)
        self.pushButton_43.setEnabled(True)
        self.pushButton_38.setEnabled(False)        

    def row_go(self):        
        rows=[]
        if self.lineEdit_33.text() == '' and self.lineEdit_32.text() == '':
            QMessageBox.warning(self, 'بيانات مفقودة', 'من فضلك أدخل البيانات المطلوبة', QMessageBox.Ok)
            return
        if self.lineEdit_33.text() == '':
            row = self.lineEdit_32.text()            
        else:
            invoice_no = self.lineEdit_33.text()            
            self.cur.execute(f"SELECT id FROM buypill WHERE buy_invoice_no={invoice_no}")
            row = self.cur.fetchone() 
                   
            if row == None:
                QMessageBox.warning(self, 'بيانات مفقودة', 'البيانات التي ادخلتها غير موجودة في قاعدة البيانات', QMessageBox.Ok)
                return
            else:
                row = row[0]
        self.cur.execute("SELECT id FROM buypill ORDER BY id")
        id_s = self.cur.fetchall()        
        for i in range(len(id_s)):
            rows.append(id_s[i][0])            
        if int(row) in rows:
            row_no = rows.index(int(row)) + 1        
            self.tableWidget_10.setCurrentCell(int(row_no)-1, 1)
        else:
            QMessageBox.warning(self, 'بيانات مفقودة', 'البيانات التي ادخلتها غير موجودة في قاعدة البيانات', QMessageBox.Ok)
            return
        # elif invoice_no != '':
        #     self.tableWidget_10.setCurrentCell(int(invoice_no)-1, 4)
        self.lineEdit_32.setText('')
        self.lineEdit_33.setText('')
        self.pushButton_43.setEnabled(True)        
        self.groupBox_14.hide()
    
    def buy_bill_delete(self):
        del_item = QMessageBox.warning(self, 'مسح بيانات' , 'هل انت متأكد من حذف هذه البيانات', QMessageBox.Yes | QMessageBox.No)
        if del_item == QMessageBox.No :
            return

        id = int(self.lineEdit_52.text())
        self.cur.execute(f"DELETE FROM buypill WHERE id={id}")
        self.cur.execute(f"DELETE FROM buypill_details WHERE buypill_id={id}")
        self.db.commit()
        self.buy_bill_table_fill()
        self.lineEdit_32.setText('')
        self.lineEdit_33.setText('')
        self.lineEdit_51.setText('')
        self.lineEdit_52.setText('')
        self.lineEdit_56.setText('0')
        self.lineEdit_57.setText('0')
        self.lineEdit_58.setText('0')
        self.pushButton_35.setEnabled(False)
        self.pushButton_40.setEnabled(False)
        self.pushButton_43.setEnabled(True)
        self.timeEdit_9.setTime(QTime.currentTime())
        self.dateEdit_11.setDate(QDate.currentDate())
        QMessageBox.warning(self, 'حذف بيانات', 'تم حذف البيانات بنجاح', QMessageBox.Ok)
        self.buy_bill_return()

    def buypill_table_select(self):
        row = self.tableWidget_10.currentItem().row()
        id = self.tableWidget_10.item(row, 0).text()              
        sql = f"SELECT * FROM buypill WHERE id={id}"
        self.cur.execute(sql) #, [(id)])
        data = self.cur.fetchone()
        h, m, s = map(int, (str(data[2])).split(":"))
        x = QTime(h, m)
        self.lineEdit_52.setText(str(data[0]))
        self.lineEdit_51.setText(str(data[3]))
        self.dateEdit_11.setDate(data[1])
        self.timeEdit_9.setTime(x)
        self.lineEdit_57.setText(str(data[8]))
        self.lineEdit_56.setText(str(data[9]))
        self.lineEdit_58.setText(str(data[10]))        
        self.checkBox_2.setChecked(data[5])
        self.checkBox_3.setChecked(data[6])

        self.cur.execute(f"SELECT user_fullname FROM users WHERE id={data[7]}")
        user = self.cur.fetchone()
        self.comboBox_11.setCurrentText(user[0])

        self.cur.execute(f"SELECT importer_name, importer_phone, importer_balance FROM importers WHERE id={data[4]}")
        imp = self.cur.fetchone()        
        self.comboBox_9.setCurrentText(imp[0])
        self.lineEdit_49.setText(imp[1])
        self.lineEdit_50.setText(str(imp[2]))
        self.pushButton_32.setEnabled(False)
        self.pushButton_35.setEnabled(True)
        self.pushButton_40.setEnabled(True)
    
    def buy_bill_return(self):
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.insertRow(0)
        self.lineEdit_51.setText('')
        self.lineEdit_52.setText('')
        self.lineEdit_56.setText('0')
        self.lineEdit_57.setText('0')
        self.lineEdit_58.setText('0')
        self.pushButton_32.setEnabled(True)
        self.pushButton_35.setEnabled(False)
        self.pushButton_40.setEnabled(False)
        self.pushButton_43.setEnabled(False)
        self.pushButton_38.setEnabled(True)
        self.timeEdit_9.setTime(QTime.currentTime())
        self.dateEdit_11.setDate(QDate.currentDate())
        self.groupBox_14.hide()

    def buy_bill_item_search(self):
        if self.lineEdit_73.text() == '':
            QMessageBox.warning(self, 'بيانات ناقصة', 'من فضلك أدخل الرقم المرجعي للفاتورة', QMessageBox.Ok)
            return

        self.tableWidget_11.setRowCount(0)
        self.tableWidget_11.insertRow(0)
        bp_id = self.lineEdit_73.text()
        sql = "SELECT * FROM buypill_details WHERE buypill_id = %s"
        self.cur.execute(sql, [((bp_id))])
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_11.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_11.rowCount()
            self.tableWidget_11.insertRow(row_pos)

        self.pushButton_33.setEnabled(False)
        self.pushButton_34.setEnabled(False)
        self.pushButton_36.setEnabled(False)
        self.pushButton_37.setEnabled(True)
        self.pushButton_39.setEnabled(True)
        self.pushButton_41.setEnabled(True)

    def buybill_details_table_select(self, selected):
        
        row = self.tableWidget_11.currentItem().row()
        cell = self.tableWidget_11.item(row, 0).text()        
        # for i in selected.indexes():
        #     print(f'Selected cell location Row: {i.row()} , Column: {i.column()}')
                
        bp_id = self.lineEdit_73.text()        
        sql = "SELECT * FROM buypill_details WHERE id=%s AND buypill_id=%s"
        self.cur.execute(sql, [(cell), (bp_id)])
        data = self.cur.fetchone() 

        self.comboBox_12.setCurrentText(data[2])
        self.lineEdit_72.setText(str(data[3]))
        self.lineEdit_68.setText(data[4])
        self.lineEdit_69.setText(str(data[5]))
        self.lineEdit_70.setText(str(data[6]))
        self.lineEdit_71.setText(str(data[7]))
        self.lineEdit_66.setText(str(data[8]))
        self.lineEdit_65.setText(str(data[10]))
        self.lineEdit_67.setText(str(data[11]))        
        self.lineEdit_55.setText(str(data[13]))
        self.lineEdit_53.setText(str(data[14]))   
        self.pushButton_34.setEnabled(False)
        self.pushButton_37.setEnabled(True)
        self.pushButton_39.setEnabled(True)

    def buy_bill_item_update(self):
        
        row = self.tableWidget_11.currentItem().row()
        id = self.tableWidget_11.item(row, 0).text()        
        buypill_id = self.lineEdit_73.text()
        item_name = self.comboBox_12.currentText()
        invoice_no = self.lineEdit_72.text()
        buy_unit = self.lineEdit_68.text()
        buy_unit_count = self.lineEdit_69.text()
        unit_price = self.lineEdit_70.text()
        sale_unit = self.lineEdit_71.text()        
        item_count_peruint = self.lineEdit_66.text()
        item_buy_price = self.lineEdit_74.text()
        buy_item_sale = self.lineEdit_65.text()
        total_buy = self.lineEdit_67.text()
        total_sale = self.lineEdit_54.text() 
        buy_minus = self.lineEdit_55.text()
        buy_earn = self.lineEdit_53.text()        
        
        self.cur.execute(''' UPDATE buypill_details SET item_name=%s, buy_invoice_no=%s, \
            buy_unit=%s, buy_unit_count=%s, unit_price=%s, \
            sale_unit=%s, item_count_in_buyunit=%s, \
            item_buy_price=%s, buy_item_sale=%s, \
            total_buy=%s, total_sale=%s, buy_minus=%s, buy_earn=%s \
            WHERE id=%s AND buypill_id=%s

        ''', (item_name, invoice_no, buy_unit, buy_unit_count, \
           unit_price, sale_unit, item_count_peruint, \
            item_buy_price, buy_item_sale, total_buy, \
            total_sale, buy_minus, buy_earn, id, buypill_id ))

        #self.execute("UPDATE buypill SET buy_totalB=%s, buy_totalG=%s, buy_minus=%s WHERE id=%s",(total_buy, total_sale, buy_minus, buypill_id))
        self.db.commit() 
        self.buy_item_table_fill()
            
        

        
        self.pushButton_37.setEnabled(False)
        self.pushButton_39.setEnabled(False)

    def buy_bill_item_delete(self):

        row = self.tableWidget_11.currentItem().row()
        id = self.tableWidget_11.item(row, 0).text()
        puypill_id = self.lineEdit_73.text()
        item_name = self.comboBox_12.currentText()
        buy_unit_count = self.lineEdit_69.text()

        del_item = QMessageBox.warning(self, 'مسح بيانات' , 'هل انت متأكد من حذف هذه البيانات', QMessageBox.Yes | QMessageBox.No)
        if del_item == QMessageBox.No :
            return
        else:
            sql = f" DELETE FROM buypill_details WHERE buypill_id={puypill_id} AND id={id} "
            self.cur.execute(sql)
            self.cur.execute(''' SELECT item_qty FROM items WHERE item_name=%s ''', [(item_name)])
            data = self.cur.fetchone()            
            item_qty = data[0] - int(buy_unit_count)

            self.cur.execute(''' UPDATE items SET item_qty=%s WHERE item_name=%s'''
            , (item_qty, item_name))

            self.db.commit()
            self.buy_item_table_fill()

    #  -------------------- فواتير المرتجعات -------------
    
    def rebuy_bill_add(self):
        self.cur.execute("SELECT MAX( id ) FROM rebuypill")
        id = self.cur.fetchone()
        self.lineEdit_75.setText('1')
        self.lineEdit_76.setText(str(id[0]+1))
        self.lineEdit_77.setText('')
        self.lineEdit_78.setText('')
        self.lineEdit_79.setText('')
        self.lineEdit_80.setText('0')
        self.lineEdit_81.setText('0')
        self.pushButton_45.setEnabled(False)
        self.pushButton_47.setEnabled(False)
        self.pushButton_48.setEnabled(False)
        

    def rebuy_bill_save(self):
        rebuy_date = self.dateEdit_12.date()
        rebuy_date = rebuy_date.toString(QtCore.Qt.ISODate)
        rebuy_time = self.timeEdit_10.time()
        rebuy_time = rebuy_time.toString(QtCore.Qt.ISODate)
        buypill_id = self.lineEdit_77.text()
        detailpill_id = self.lineEdit_78.text()
        import_pill_id = self.lineEdit_79.text()
        rebuy_item_name = self.comboBox_13.currentText()
        rebuy_item_count = self.lineEdit_75.text()
        unit_price = self.lineEdit_80.text()
        rebuy_totalG = self.lineEdit_81.text()
        importer = self.comboBox_10.currentText()
        rebuy_user = self.comboBox_14.currentText()        
        
        sql = '''SELECT id FROM users WHERE user_fullname = %s''' 
        self.cur.execute(sql, [(rebuy_user)])
        data = self.cur.fetchone()
        user_id = data[0]

        self.cur.execute('''
            INSERT INTO rebuypill(rebuy_date, rebuy_time, buypill_id, detail_pill_id, import_pill_id, rebuy_item_name, rebuy_item_count, unit_price, rebuy_totalG, importer, rebuy_user_id)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ''',(rebuy_date, rebuy_time, buypill_id, detailpill_id, import_pill_id, rebuy_item_name, rebuy_item_count, unit_price, rebuy_totalG, importer, user_id))
        self.db.commit()

        sql = '''SELECT item_qty FROM items WHERE item_name = %s'''
        self.cur.execute(sql, [(rebuy_item_name)])
        data = self.cur.fetchone()
        item_qty = data[0]        
        item_qty -= int(rebuy_item_count)
        self.cur.execute("UPDATE items SET item_qty=%s WHERE item_name = %s", (item_qty, rebuy_item_name))
        self.db.commit()

        self.lineEdit_75.setText('1')
        self.lineEdit_77.setText('')
        self.lineEdit_78.setText('')
        self.lineEdit_79.setText('')
        self.lineEdit_80.setText('0')
        self.lineEdit_81.setText('0')
        self.pushButton_45.setEnabled(False)
        QMessageBox.warning(self, 'إفــادة', 'تم حفظ البيانات بنجاح', QMessageBox.Ok)
        return

        
    def rebuy_bill_search(self):
        self.tableWidget_12.setRowCount(0)
        self.tableWidget_12.insertRow(0)
        sql = "SELECT * FROM rebuypill"
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_12.setItem(row, col, QTableWidgetItem(str(item)))
                if col == 11:                    
                    sql = '''SELECT user_fullname FROM users WHERE id=%s'''
                    self.cur.execute(sql, [(item)])
                    emp_name = self.cur.fetchone()                    
                    if emp_name != None:                        
                        employee_name = emp_name[0]
                        self.tableWidget_12.setItem(row, col, QTableWidgetItem((employee_name)))

                col += 1
            row_pos = self.tableWidget_12.rowCount()
            self.tableWidget_12.insertRow(row_pos)
            self.pushButton_47.setEnabled(True)
            self.pushButton_48.setEnabled(True)

    def rebuy_item_select(self):
        row = self.tableWidget_12.currentItem().row()
        cell = self.tableWidget_12.item(row, 0).text()
        
        sql = f"SELECT * FROM rebuypill WHERE id = {cell} "
        self.cur.execute(sql)
        data = self.cur.fetchone()
        h, m, s = map(int, (str(data[2])).split(":"))
        x = QTime(h, m)
        self.lineEdit_76.setText(str(data[0]))
        self.dateEdit_12.setDate(data[1])
        self.timeEdit_10.setTime(x)
        self.lineEdit_77.setText(str(data[3]))
        self.lineEdit_78.setText(str(data[4]))
        self.lineEdit_79.setText(str(data[5]))
        self.comboBox_13.setCurrentText(str(data[6]))
        self.lineEdit_75.setText(str(data[7]))
        self.lineEdit_80.setText(str(data[8]))
        self.lineEdit_81.setText(str(data[9]))
        self.comboBox_10.setCurrentText(str(data[10]))
        self.comboBox_14.setCurrentText(str(data[11]))

    def rebuypill_update(self):

        id = self.lineEdit_76.text()
        sql = "SELECT rebuy_item_count FROM rebuypill WHERE id=%s"        
        self.cur.execute(sql, [(id)])
        data = self.cur.fetchone()
        item_count = data[0]        
        rebuy_date = self.dateEdit_12.date()
        rebuy_date = rebuy_date.toString(QtCore.Qt.ISODate)
        rebuy_time = self.timeEdit_10.time()
        rebuy_time = rebuy_time.toString(QtCore.Qt.ISODate)
        rebuy_item_name = self.comboBox_13.currentText()
        buypill_id = self.lineEdit_77.text()
        detailpill_id = self.lineEdit_78.text()
        import_pill_id = self.lineEdit_79.text()        
        rebuy_item_cnt = int(self.lineEdit_75.text())
        item_count -= rebuy_item_cnt        
        unit_price = self.lineEdit_80.text()
        rebuy_totalG = self.lineEdit_81.text()
        importer = self.comboBox_10.currentText()
        rebuy_user = self.comboBox_14.currentText()

        sql = "SELECT item_qty FROM items WHERE item_name=%s"
        self.cur.execute(sql, [(rebuy_item_name)])
        data = self.cur.fetchone()
        qty = data[0]
        item_qty = qty + item_count
        self.cur.execute("UPDATE items SET item_qty=%s WHERE item_name=%s",(item_qty, rebuy_item_name))
        sql = '''SELECT id FROM users WHERE user_fullname = %s''' 
        self.cur.execute(sql, [(rebuy_user)])
        data = self.cur.fetchone()
        user_id = data[0]

        self.cur.execute(''' UPDATE rebuypill SET \
         rebuy_date=%s, rebuy_time=%s, \
         buypill_id=%s, detail_pill_id=%s, \
         import_pill_id=%s, rebuy_item_name=%s,\
         rebuy_item_count=%s, unit_price=%s, \
         rebuy_totalG=%s, importer=%s, \
         rebuy_user_id=%s WHERE id=%s ''', (
         rebuy_date, rebuy_time, buypill_id, \
         detailpill_id, import_pill_id, rebuy_item_name,\
         rebuy_item_cnt, unit_price,\
         rebuy_totalG, importer, user_id, id))

        self.db.commit()

    def rebuy_delete(self):
        
        del_item = QMessageBox.warning(self, 'مسح بيانات' , 'هل انت متأكد من حذف هذه البيانات', QMessageBox.Yes | QMessageBox.No)
        if del_item == QMessageBox.No :
            return
        id = self.lineEdit_76.text()
        item_name = self.comboBox_13.currentText()
        sql = "SELECT rebuy_item_count FROM rebuypill WHERE id = %s"
        self.cur.execute(sql, [(id)])
        data = self.cur.fetchone()
        rebuy_item_qty = data[0]

        sql = "SELECT item_qty FROM items WHERE item_name = %s"
        self.cur.execute(sql, [(item_name)])
        data = self.cur.fetchone()
        item_qty = data[0]
        item_qty += rebuy_item_qty
        
        self.cur.execute("UPDATE items SET item_qty=%s WHERE item_name=%s ", (item_qty, item_name))

        sql = ('''DELETE FROM rebuypill WHERE id = %s ''')
        self.cur.execute(sql, [(id)])

        self.db.commit()
        self.rebuy_bill_search()

    def rebuypill_save_but(self):

        x = float(self.lineEdit_75.text())
        y = float(self.lineEdit_80.text())
        z = x * y
        z = float("{:.2f}".format(z))
        self.lineEdit_81.setText(str(z))
        
        if self.pushButton_47.isEnabled():            
            self.pushButton_45.setEnabled(False)
        else:
            self.pushButton_45.setEnabled(True)

# =============== Sales ===============
    def shift_change(self):
        shift_time = self.timeEdit_11.time()
        shift_time = shift_time.toString(QtCore.Qt.ISODate)
        today_date = self.dateEdit_13.date()
        today_date = today_date.toString(QtCore.Qt.ISODate)
        shift_no = int(self.lineEdit_90.text())
        shift_no += 1
        if shift_no == 4:
            shift_no = 1
        self.lineEdit_90.setText(str(shift_no))
        casher_name = self.comboBox_15.currentText()
        sql = ("SELECT id FROM users WHERE user_fullname=%s")
        self.cur.execute(sql, [(casher_name)])
        data = self.cur.fetchone()
        id = data[0]

        query = '''SELECT employee_id, shift_no FROM operations WHERE oper_date=%s'''
        self.cur.execute(query, [(today_date)])
        data = self.cur.fetchone()        
        #if data[0] != id and data[1] != shift_no:
        if data == None:
        
            sale_cash = 0
            sale_visa = 0        
            self.cur.execute("INSERT INTO operations\
                (employee_id, shift_no, casher_name, sale_cash, sale_visa,\
                oper_date, oper_time) VALUES(%s, %s, %s,\
                %s, %s, %s, %s)", (id, shift_no, casher_name, \
                sale_cash, sale_visa, today_date, shift_time))
            self.db.commit()

    
    def visa(self):
        self.lineEdit_82.setText('0')
        x = float(self.lineEdit_62.text())
        y = float(self.lineEdit_64.text())
        z = float(self.lineEdit_87.text())
        m = x - (y+z)
        self.lineEdit_60.setText(str(m))

            
    def cash_rset(self):
        self.lineEdit_82.setText((str(float(self.lineEdit_64.text())-(float(self.lineEdit_62.text())))))
        #self.salebill_save()
        x = float(self.lineEdit_82.text())
        #self.lineEdit_60.setText(str(-1*x))

    def item_qty_x_sale_price(self):
        item_price = self.lineEdit_85.text()
        item_qty = self.lineEdit_83.text()
        x = float(item_qty) * float(item_price)
        self.lineEdit_84.setText(str(x))
        self.sale_item_add()

    def get_sale_item_info(self):
        bar_code = self.lineEdit_86.text()
        sql = f"SELECT item_name, item_price, item_unit FROM items WHERE item_barcode={bar_code}"
        self.cur.execute(sql)
        data = self.cur.fetchone()        
        self.comboBox_16.setCurrentText(data[0])
        self.lineEdit_85.setText(str(data[1]))
        self.lineEdit_88.setText(data[2])
        self.item_qty_x_sale_price()

    def sale_item_select(self):
        invo_no = int(self.lineEdit_59.text())
        row = self.tableWidget_13.currentItem().row()
        it_code = self.tableWidget_13.item(row, 0).text()              
        sql = f"SELECT * FROM salepill_details WHERE item_code={it_code} AND salepill_id={invo_no}"
        self.cur.execute(sql)
        data = self.cur.fetchone()        
        
        self.lineEdit_86.setText(str(data[2]))
        self.comboBox_16.setCurrentText(data[3])
        self.lineEdit_85.setText(str(data[5]))
        self.lineEdit_88.setText(data[4])
        self.lineEdit_83.setText(str(data[6]))
        self.lineEdit_84.setText(str(data[7]))
        self.pushButton_49.setEnabled(True)
        self.pushButton_50.setEnabled(True)


    def sale_item_delete(self):
        invo_no = int(self.lineEdit_59.text())
        it_code = int(self.lineEdit_86.text())        
        sql = ('''DELETE FROM salepill_details WHERE item_code=%s AND salepill_id=%s''')
        self.cur.execute(sql, [(it_code), (invo_no)])
        self.db.commit()        
        self.pushButton_49.setEnabled(False)
        self.pushButton_50.setEnabled(False)
        self.lineEdit_83.setText('1')
        self.lineEdit_84.setText('')
        self.lineEdit_85.setText('1')
        self.lineEdit_86.setText('')        
        self.lineEdit_88.setText('')
        self.salebill_details_table_fill()

    def sale_item_add(self):
        it_code = int(self.lineEdit_86.text())
        if self.lineEdit_59.text() == '' :
            QMessageBox.warning(self,'تنبيه', 'من فضلك اضغط على فاتورة جديدة', QMessageBox.Ok)
            return
        id = int(self.lineEdit_59.text())        
        code = self.lineEdit_86.text()
        name = self.comboBox_16.currentText()
        price = self.lineEdit_85.text()
        count = float(self.lineEdit_83.text())
        item_total_price = self.lineEdit_84.text()
        unit = self.lineEdit_88.text()
        x = float(item_total_price)
        y = x + float(self.lineEdit_61.text())
        self.lineEdit_61.setText(str(y))
        self.lineEdit_62.setText(str(float(self.lineEdit_61.text())-(float(self.lineEdit_63.text()))))
        self.cur.execute("INSERT INTO salepill_details \
            (salepill_id, item_code, item_name,\
            item_price, item_total_price, item_count, item_unit) \
            VALUES(%s, %s, %s, %s, %s, %s, %s)",\
            (id, code, name, price, item_total_price,\
            count, unit))
        
        self.cur.execute(f"UPDATE items SET item_qty=item_qty-{count} WHERE item_barcode={it_code}")
        self.db.commit()
        self.salebill_details_table_fill()

    def salebill_add_new(self):
        self.cur.execute("SELECT MAX( id ) FROM salepill")
        id = self.cur.fetchone()
        id = list(id)        
        if id[0] == None:
            id[0] = 0
        # هذه الخطوة للتغلب فيما إذا تم حذف السجل الأخير من قاعدة البيانات
        self.cur.execute(f"ALTER TABLE salepill AUTO_INCREMENT = {id[0]}")
        self.cur.execute("SELECT MAX( id ) FROM salepill")
        id = self.cur.fetchone()
        id = list(id)        
        if id[0] == None:
            id[0] = 0
        
        self.timeEdit_11.setTime(QTime.currentTime())
        self.lineEdit_59.setText(str(id[0]+1))        
        self.lineEdit_60.setText('0')
        self.lineEdit_61.setText('0')
        self.lineEdit_62.setText('0')
        self.lineEdit_63.setText('0')        
        self.lineEdit_64.setText('0')
        self.lineEdit_82.setText('0')
        self.lineEdit_83.setText('1')
        self.lineEdit_84.setText('')
        self.lineEdit_85.setText('1')
        self.lineEdit_86.setText('')
        self.lineEdit_87.setText('0')
        self.lineEdit_88.setText('')
        self.pushButton_53.setEnabled(True)
        self.lineEdit_86.setFocus(QtCore.Qt.MouseFocusReason)        
        self.lineEdit_86.setCursorPosition(0)
        
        self.tableWidget_13.setRowCount(0)
        self.tableWidget_13.insertRow(0)

        self.pushButton_52.setEnabled(False)

    def clear_fields(self):
        self.lineEdit_86.setText('')
        self.lineEdit_85.setText('1')
        self.lineEdit_88.setText('')
        self.lineEdit_83.setText('1')
        self.lineEdit_84.setText('')


    def salebill_save(self):
        if self.lineEdit_59.text() == '' :
            QMessageBox.warning(self, 'بيانات ناقصة', 'من فضلك اضغط فاتورة جديدة', QMessageBox.Ok)
            return
        shift_no = self.lineEdit_90.text()
        sale_time = self.timeEdit_11.time()
        sale_time = sale_time.toString(QtCore.Qt.ISODate)
        sale_date = self.dateEdit_13.date()
        sale_date = sale_date.toString(QtCore.Qt.ISODate)        
        customer = self.lineEdit_89.text()
        invo_total = self.lineEdit_61.text()
        dis = self.lineEdit_63.text()
        wanted = self.lineEdit_62.text()
        cash = self.lineEdit_64.text()
        cash_rtn = self.lineEdit_82.text()
        net_cash = float(cash) - float(cash_rtn)        
        visa = self.lineEdit_87.text()
        rest_cash = self.lineEdit_60.text()
        user = self.comboBox_15.currentText()
        self.cur.execute("INSERT INTO salepill(date,\
            time, customer, invoice_total,\
            discount, wanted, cash, cash_return,\
            visa, rest_cash, user) VALUES(%s, %s,\
            %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
            (sale_date, sale_time, customer, invo_total,\
             dis, wanted, cash, cash_rtn, visa,\
             rest_cash, user))
        
        self.cur.execute('''UPDATE operations
         SET sale_cash=sale_cash+%s, 
         sale_visa=sale_visa+%s WHERE 
         shift_no=%s AND oper_date=%s 
         AND casher_name=%s''', 
         (net_cash, visa, shift_no, sale_date, user))        
        self.db.commit()
        self.pushButton_52.setEnabled(True)


    def sale_item_update(self):
        invo_no = int(self.lineEdit_59.text())
        row = self.tableWidget_13.currentItem().row()
        it_code = self.tableWidget_13.item(row, 0).text()              
        sql = f"SELECT * FROM salepill_details WHERE item_code={it_code} AND salepill_id={invo_no}"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        old_qty = float(data[6])
        new_qty = float(self.lineEdit_83.text())
        dif_qty = old_qty - new_qty
        sql = f"UPDATE salepill_details SET item_count={new_qty}, item_total_price=item_price*{new_qty} WHERE salepill_id={invo_no} AND item_code={it_code}"
        self.cur.execute(sql)

        sql = f"UPDATE items SET item_qty=item_qty+{dif_qty} WHERE item_barcode={it_code}"
        self.cur.execute(sql)
        self.db.commit()
        self.salebill_details_table_fill()
        self.pushButton_49.setEnabled(False)
        self.pushButton_50.setEnabled(False)

    def salebill_details_table_fill(self):        
        x = 0
        y = 0
        s_bill_id = int(self.lineEdit_59.text())
        self.tableWidget_13.setRowCount(0)
        self.tableWidget_13.insertRow(0)
        self.cur.execute(f"SELECT item_code, item_name, item_unit, item_price, item_count, item_total_price FROM salepill_details WHERE salepill_id={s_bill_id}")
        data = self.cur.fetchall()
        if data == []:
            self.lineEdit_61.setText('0')
            self.lineEdit_62.setText('0')
            QMessageBox.warning(self,'تنبيه', 'انتبه تم حذف جميع أصناف الفاتورة', QMessageBox.Ok)            
            return
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_13.setItem(row, col, QTableWidgetItem(str(item)))
                if col == 4 :
                    y += float(item)
                elif col == 5 :
                    x += float(item)
                col += 1
            row_pos = self.tableWidget_13.rowCount()            
            self.tableWidget_13.insertRow(row_pos)
        self.tableWidget_13.setItem(row_pos, 4, QTableWidgetItem(str(y)))
        self.tableWidget_13.setItem(row_pos, 5, QTableWidgetItem(str(x)))
        self.lineEdit_61.setText(str(x))
        self.lineEdit_62.setText(str(x))

# =============== تقارير ===============
    def cashier_daily_tally(self):

        casher = self.comboBox_20.currentText()
        date = self.dateEdit_14.date()
        date = date.toString(QtCore.Qt.ISODate)
        
        sql = ''' SELECT o.casher_name,
                        o.shift_no,
                        o.sale_cash,
                        o.sale_visa,
                        o.oper_date,
                        h.he_come,
                        h.he_go,
                        h.he_difference
                        FROM operations o
                        JOIN hodoor_ensraf h
                        ON o.employee_id = h.he_employee_id
                        AND o.oper_date=%s AND h.he_date=%s
                        '''
        self.cur.execute(sql, [(date), (date)])
        data = self.cur.fetchall()
        
        self.tableWidget_14.setRowCount(0)
        self.tableWidget_14.insertRow(0)
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_14.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_14.rowCount()
            self.tableWidget_14.insertRow(row_pos)
        

    def most_selling_item(self):

        query = ''' SELECT s.item_name,s.item_code, SUM(s.item_total_price) as total_sales
                FROM salepill_details s
                JOIN items i ON s.item_code = i.item_barcode
                GROUP BY s.item_code
                ORDER BY total_sales DESC '''
        self.cur.execute(query)
        data = self.cur.fetchall()
        self.tableWidget_15.setRowCount(0)
        self.tableWidget_15.insertRow(0)
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_15.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_15.rowCount()
            self.tableWidget_15.insertRow(row_pos)

    def daily_sales(self):
        date = self.dateEdit_15.date()
        date = date.toString(QtCore.Qt.ISODate)
        query = ''' SELECT SUM(sale_cash), SUM(sale_visa) FROM operations WHERE oper_date=%s '''
        self.cur.execute(query, [(date)])
        data = self.cur.fetchone()        
        self.lineEdit_91.setText(str(data[0]))
        self.lineEdit_92.setText(str(data[1]))

    def sales_range_report(self):

        date1 = self.dateEdit_15.date()
        date1 = date1.toString(QtCore.Qt.ISODate)
        date2 = self.dateEdit_16.date()
        date2 = date2.toString(QtCore.Qt.ISODate)
        query = ''' SELECT SUM(sale_cash), SUM(sale_visa) FROM operations WHERE oper_date BETWEEN %s AND %s '''
        self.cur.execute(query, [(date1), (date2)])
        data = self.cur.fetchone()        
        self.lineEdit_93.setText(str(data[0]))
        self.lineEdit_94.setText(str(data[1]))
    
    def buy_range_report(self):
        date1 = self.dateEdit_15.date()
        date1 = date1.toString(QtCore.Qt.ISODate)
        date2 = self.dateEdit_16.date()
        date2 = date2.toString(QtCore.Qt.ISODate)
        query = ''' SELECT SUM(buy_totalB), SUM(buy_extra_exp) FROM operations WHERE oper_date BETWEEN %s AND %s '''
        self.cur.execute(query, [(date1), (date2)])
        data = self.cur.fetchone()        
        self.lineEdit_95.setText(str(data[0]))
        self.lineEdit_96.setText(str(data[1]))
    
    def Items_inventory(self):
        query = '''SELECT item_barcode,
         item_name, item_qty, item_unit, 
         item_price, item_price * item_qty 
         FROM items ORDER BY 
         item_barcode'''
        self.cur.execute(query)
        data = self.cur.fetchall()
        self.tableWidget_16.setRowCount(0)
        self.tableWidget_16.insertRow(0)
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_16.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_16.rowCount()
            self.tableWidget_16.insertRow(row_pos)

    def salebill_print(self):

        pdfmetrics.registerFont(TTFont('ae_AlMateen_1', 'ae_AlMateen_1.ttf'))
        page = canvas.Canvas("my_pdf.pdf", pagesize=A4)
        page.setFont('ae_AlMateen_1', 14)
        text_1 = arabic_reshaper.reshape('رقم الفاتورة')
        text_1 = get_display(text_1)
        text_2 = arabic_reshaper.reshape('اسم الصنف')
        text_2 = get_display(text_2)
        text_3 = arabic_reshaper.reshape('الكمية')
        text_3 = get_display(text_3)
        text_4 = arabic_reshaper.reshape('السعر')
        text_4 = get_display(text_4)
        text_5 = arabic_reshaper.reshape('إجمالي الصنف')
        text_5 = get_display(text_5)
        text_6 = arabic_reshaper.reshape('إجمالي الفاتورة')
        text_6 = get_display(text_6)
        page.drawRightString(195*mm, 280*mm, text_1)
        dt = date.today().strftime('%d-%m-%Y')
        page.drawRightString(195*mm, 270*mm, dt) 
        page.setStrokeColorRGB(0.1,0.8,0.1) # up Line colour 
        page.line(20*mm,265*mm,270*mm,265*mm)
        page.setStrokeColorRGB(0,0,0)
        page.drawRightString(175*mm, 255*mm, text_2)
        page.drawRightString(110*mm, 255*mm, text_3)
        page.drawRightString(80*mm, 255*mm, text_4)
        page.drawRightString(50*mm, 255*mm, text_5)
        page.drawRightString(175*mm, 70*mm, text_6)
        page.line(60*mm,250*mm,60*mm,80*mm)# first vertical line
        page.line(90*mm,250*mm,90*mm,80*mm)# second vertical line
        page.line(120*mm,250*mm,120*mm,80*mm)# third vertical line
        page.line(20*mm,80*mm,270*mm,80*mm)# horizontal line total

        salepill_id = self.lineEdit_59.text()
        query = '''SELECT item_name, 
           item_count, item_price, 
           item_total_price 
           FROM salepill_details 
           WHERE salepill_id = %s'''
        self.cur.execute(query, [(salepill_id)])
        data = self.cur.fetchall()
        total = 0
        y_gap = 10
        y = 240
        
        for row, form in enumerate(data):
            x = 190
            for col, item in enumerate(form):
                x_gap = 80
                if col > 0:
                    x_gap = 30
                if col == 3:
                    total += item
                text_7 = arabic_reshaper.reshape(str(item))
                text_7 = get_display(text_7)
                page.drawRightString(x*mm, y*mm, text_7)
                x -= x_gap
            y -= y_gap
        tot = arabic_reshaper.reshape(str(total))
        tot = get_display(tot)
        page.drawRightString(50*mm, 70*mm, tot)

        page.showPage()
        page.save()
        os.startfile("my_pdf.pdf")


def main():
    #app = QApplication(sys.argv)  
    app = QtWidgets.QApplication([])
    Window = QtWidgets.QWidget()  
    Window = Main()
    Window.show()
    app.exec_()
if __name__ == '__main__':
    main()
