from PyQt5 import QtWidgets, uic
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
from datetime import date
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
import os
from datetime import datetime, timedelta
import datetime
from decimal import Decimal
import mysql.connector
'''
MainUI,_ = loadUiType('market.ui')
class Main(QMainWindow, MainUI):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)        
'''
class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('market.ui', self)  # تحميل ملف التصميم

        # إعداد مؤقت لتحديث الوقت بشكل دوري
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.timeout.connect(self.update_date)
        self.timer.timeout.connect(self.update_title)        
        self.timer.start(1000)  # تحديث كل ثانية (1000 ميلي ثانية)
        self.update_title()
        # self.c = canvas.Canvas(my_path,pagesize=letter)
        self.timeEdit_2.setTime(QTime.currentTime())
        self.dateEdit_4.setDate(QDate.currentDate())
        self.dateEdit_14.setDate(QDate.currentDate())
        self.dateEdit_15.setDate(QDate.currentDate())
        self.dateEdit_16.setDate(QDate.currentDate())
        

        self.groupBox_14.hide()
        #self.tab_13.setEnabled(False)
        self.checkBox.stateChanged.connect(self.user_enabled)        
        self.comboBox_9.currentTextChanged.connect(self.importer_info)
        self.comboBox_24.currentTextChanged.connect(self.customer_info)
        self.comboBox_15.activated.connect(self.shift_change)
        self.lineEdit_3.textEdited.connect(self.user_save_enabled)
        self.lineEdit_10.textEdited.connect(self.customer_save_enabled)
        self.lineEdit_18.textEdited.connect(self.importer_save_enabled)
        self.lineEdit_25.textEdited.connect(self.item_save_enabled)    
        self.lineEdit_36.textEdited.connect(self.grp_save_enabled)
        self.lineEdit_38.textEdited.connect(self.company_save_enabled)
        self.lineEdit_64.textChanged.connect(self.cash_rset)
        self.lineEdit_64.returnPressed.connect(self.cash)
        self.lineEdit_69.textChanged.connect(self.buy_unit_total)
        self.lineEdit_71.textChanged.connect(self.buy_unit_total)
        self.lineEdit_70.textChanged.connect(self.total_discount)        
        self.lineEdit_73.returnPressed.connect(self.enabled_buy_item_but)
        self.lineEdit_77.returnPressed.connect(self.rebuy_item_info)
        self.lineEdit_81.textChanged.connect(self.rebuybill_save_but)
        
        self.lineEdit_86.returnPressed.connect(self.get_sale_item_info)       
        self.lineEdit_87.returnPressed.connect(self.visa)
        # self.lineEdit_84.textChanged.connect(self.sale_item_add)        
        # self.tableWidget_11.selectionModel().selectionChanged.connect(self.buy_item_table_select)
        self.tableWidget.itemClicked.connect(self.user_table_select)
        self.tableWidget_2.itemClicked.connect(self.customer_table_select)
        self.tableWidget_3.itemClicked.connect(self.importer_table_select)
        self.tableWidget_4.itemClicked.connect(self.item_table_select)
        self.tableWidget_5.itemClicked.connect(self.grp_table_select)
        self.tableWidget_6.itemClicked.connect(self.company_table_select)        
        self.tableWidget_10.itemClicked.connect(self.buybill_table_select)
        self.tableWidget_11.itemClicked.connect(self.buy_item_table_select)
        self.tableWidget_12.itemClicked.connect(self.rebuy_item_select)
        self.tableWidget_13.itemClicked.connect(self.sale_item_select)
        self.tableWidget_17.itemClicked.connect(self.resalebill_table_select)

        validator = QRegExpValidator(QRegExp(r'[0-9]+')) 
        self.lineEdit_64.setValidator(QDoubleValidator())
        self.lineEdit_87.setValidator(QDoubleValidator())
        self.lineEdit_73.setValidator(QDoubleValidator())
        self.lineEdit_73.setMaxLength(13)
        self.lineEdit_69.setValidator(QDoubleValidator())
        self.lineEdit_69.setMaxLength(7)
        self.lineEdit_70.setValidator(QDoubleValidator(0.00,999.99,2))
        self.lineEdit_70.setMaxLength(7)
        self.lineEdit_70.setValidator(validator)        
        self.pushButton_31.setEnabled(False)
        self.pushButton_35.setEnabled(False)
        self.pushButton_40.setEnabled(False)
        self.pushButton_43.setEnabled(False)
        
        #self.lineEdit_64 = self.findChild(QtWidgets.QLineEdit, 'lineEdit_64')
        #self.lineEdit_64.installEventFilter(self)       

        self.db_connect()
        self.handel_buttons()
        self.user_table_fill()
        self.customer_table_fill()
        self.importer_table_fill()
        self.item_table_fill()
        self.grp_table_fill()
        self.company_table_fill()        
        self.grp_combo_fill()
        self.company_combo_fill()        
        self.Hodor_table_fill()
        self.user_combo_fill()
        self.importer_combo_fill()
        self.item_combo_fill()
        self.customer_combo_fill()
        self.resalebill_table_fill()
    '''
    def eventFilter(self, source, event):        
        if source == self.lineEdit_64 and event.type() == event.FocusIn:  # عند التركيز                                    
            #self.lineEdit_64.setText('0')
            self.lineEdit_64.selectAll()  # تحديد النص بالكامل
            print('Mostafa')
            
        return super(Main, self).eventFilter(source, event)    
    '''
    def update_time(self):
        # الحصول على الوقت الحالي
        current_time = QTime.currentTime()
        # تحديث عنصر timeEdit
        self.timeEdit.setTime(current_time) 
        self.timeEdit_2.setTime(current_time)
        self.timeEdit_4.setTime(current_time)
        self.timeEdit_5.setTime(current_time)
        self.timeEdit_8.setTime(current_time)
        self.timeEdit_9.setTime(current_time)
        self.timeEdit_11.setTime(current_time)
        self.timeEdit_14.setTime(current_time)

    def update_date(self):
        # الحصول على التاريخ الحالي
        current_date = QDate.currentDate()
        # تحديث عنصر dateEdit
        self.dateEdit.setDate(current_date)         
        self.dateEdit_2.setDate(current_date)
        self.dateEdit_3.setDate(current_date)         
        self.dateEdit_5.setDate(current_date)
        self.dateEdit_6.setDate(current_date)
        self.dateEdit_7.setDate(current_date)
        self.dateEdit_8.setDate(current_date)
        self.dateEdit_9.setDate(current_date)
        self.dateEdit_10.setDate(current_date)
        self.dateEdit_11.setDate(current_date)
        self.dateEdit_12.setDate(current_date)
        self.dateEdit_13.setDate(current_date)
        #self.dateEdit_14.setDate(current_date)        
        #self.dateEdit_15.setDate(current_date)
        #self.dateEdit_16.setDate(current_date)
        self.dateEdit_19.setDate(current_date)

    def update_title(self):
        # الحصول على الوقت والتاريخ الحاليين
        current_time = datetime.datetime.now().strftime('%d/%m/%Y    %I:%M:%S %p')
        self.setWindowTitle(current_time)  # تحديث عنوان النافذة

    def db_connect(self):
        self.db = mysql.connector.connect(user='root', password=str(""),
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
        
        self.pushButton_27.clicked.connect(self.hodor_save)
        self.pushButton_28.clicked.connect(self.hodor_delete)
        self.pushButton_29.clicked.connect(self.hodor_update)
        self.pushButton_30.clicked.connect(self.hodor_report)

        self.pushButton_31.clicked.connect(self.buybill_save)
        self.pushButton_32.clicked.connect(self.buybill_add_new)
        self.pushButton_33.clicked.connect(self.buy_item_add_new)
        self.pushButton_34.clicked.connect(self.buy_item_clear)        
        self.pushButton_35.clicked.connect(self.buybill_update)

        self.pushButton_36.clicked.connect(self.buy_item_search)
        self.pushButton_37.clicked.connect(self.buy_item_update)
        self.pushButton_38.clicked.connect(self.buybill_search)
        self.pushButton_39.clicked.connect(self.buy_item_delete)
        self.pushButton_40.clicked.connect(self.buybill_delete)

        self.pushButton_41.clicked.connect(self.buybill_return_to)
        self.pushButton_42.clicked.connect(self.row_go)
        self.pushButton_43.clicked.connect(self.buybill_return)
        self.pushButton_44.clicked.connect(self.rebuybill_add_new)
        self.pushButton_45.clicked.connect(self.rebuybill_save)

        self.pushButton_46.clicked.connect(self.rebuybill_search)
        self.pushButton_47.clicked.connect(self.rebuybill_update)
        self.pushButton_48.clicked.connect(self.rebuy_delete)
        self.pushButton_49.clicked.connect(self.sale_item_update)        
        self.pushButton_50.clicked.connect(self.sale_item_delete)

        self.pushButton_51.clicked.connect(self.grp_add_new)
        self.pushButton_52.clicked.connect(self.salebill_add_new)
        self.pushButton_53.clicked.connect(self.clear_fields)
        self.pushButton_54.clicked.connect(self.grp_update)
        self.pushButton_55.clicked.connect(self.company_add_new)
        
        self.pushButton_56.clicked.connect(self.company_update)        
        self.pushButton_59.clicked.connect(self.cashier_daily_tally)
        self.pushButton_60.clicked.connect(self.most_selling_item)
        
        self.pushButton_61.clicked.connect(self.daily_sales)
        self.pushButton_62.clicked.connect(self.sales_range_report)
        self.pushButton_63.clicked.connect(self.buy_range_report)
        self.pushButton_64.clicked.connect(self.Items_inventory)
        self.pushButton_65.clicked.connect(self.salebill_print)

        self.pushButton_66.clicked.connect(self.toggle_keypad)
        self.pushButton_67.clicked.connect(self.resalebill_add_new)
        self.pushButton_68.clicked.connect(self.resalebill_save)
        self.pushButton_69.clicked.connect(self.item_clear)
        self.pushButton_70.clicked.connect(self.resalebill_update)

        self.pushButton_71.clicked.connect(self.resalebill_delete)
        self.pushButton_72.clicked.connect(self.item_table_fill)
    # ===================== keybad =======================
        self.keypad = QFrame(self)
        self.keypad.setGeometry(132, 142, 180, 230)
        self.keypad.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        self.keypad.setVisible(False)  # مخفية في البداية

        # تصميم الأزرار داخل اللوحة
        layout = QGridLayout(self.keypad)
        self.keypad_buttons = []
        for i in range(10):
            btn = QPushButton(str(i), self.keypad)
            btn.setFixedSize(40, 40)
            btn.clicked.connect(lambda checked, num=i: self.on_number_clicked(num))
            row = (i - 1) // 3 + 1 if i != 0 else 4  # الأرقام 1-9 في الشبكة            
            col = (i - 1) % 3 if i != 0 else 1      # زر 0 في المنتصف
            layout.addWidget(btn, row, col)
            self.keypad_buttons.append(btn)
        
        # زر "حذف"
        del_btn = QPushButton("Del", self.keypad)
        del_btn.setFixedSize(40, 40)
        del_btn.clicked.connect(self.delete_last_character)
        layout.addWidget(del_btn, 4, 0)
        
        # زر "إغلاق اللوحة"
        close_btn = QPushButton("Close", self.keypad)
        close_btn.setFixedSize(40, 40)
        close_btn.clicked.connect(self.hide_keypad)
        layout.addWidget(close_btn, 4, 2)
          
    def toggle_keypad(self):
        # إظهار أو إخفاء لوحة الأرقام
        self.keypad.setVisible(not self.keypad.isVisible())
        if self.lineEdit_83.text() == '1':
            self.lineEdit_83.setText('')
        else:
            self.lineEdit_83.setText('1')
        

    def hide_keypad(self):
        # إخفاء اللوحة فقط
        self.keypad.setVisible(False)
    
    def on_number_clicked(self, num):
        # إضافة الرقم إلى مربع الإدخال
        current_text = self.lineEdit_83.text()
        self.lineEdit_83.setText(current_text + str(num))
        self.lineEdit_86.setFocus(QtCore.Qt.MouseFocusReason)        
        self.lineEdit_86.setCursorPosition(0)
        
    
    def delete_last_character(self):
        # حذف آخر حرف في مربع الإدخال
        current_text = self.lineEdit_83.text()
        self.lineEdit_83.setText(current_text[:-1])
        
# =========== Usuers ===========
    def user_save_enabled(self):
        if self.lineEdit_2.text() != '':
            self.pushButton_2.setEnabled(True)

    def user_table_select(self):

        self.groupBox_3.setEnabled(True)
        self.checkBox.setChecked(True)
        row = self.tableWidget.currentItem().row()
        id = self.tableWidget.item(row, 0).text()
        sql = f"SELECT * FROM user WHERE id={id}"
        self.cur.execute(sql) #, [(id)])
        data = self.cur.fetchone()
        self.lineEdit_2.setText(str(data[0]))
        self.lineEdit_4.setText(str(data[2]))
        self.lineEdit_3.setText(str(data[1]))
        self.comboBox.setCurrentText(data[3])
        self.lineEdit_5.setText(str(data[4]))
        self.lineEdit_6.setText(str(data[5]))
        self.comboBox_2.setCurrentText(data[6])
        self.lineEdit_7.setText(str(data[7]))
        self.lineEdit_8.setText(str(data[8]))
        self.dateEdit.setDate(data[9])
        self.pushButton.setEnabled(True)
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
        self.cur.execute('''SELECT * FROM user ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_pos)

    def user_add_new(self):
        self.cur.execute(''' SELECT id FROM user ORDER BY id ''')
        row = self.cur.fetchall()
        if row == [] :
            self.lineEdit_2.setText('1')
        else:            
            self.lineEdit_2.setText(str(row[-1][0] + 1))
            id = int(self.lineEdit_2.text())
            alter_query = f"ALTER TABLE user AUTO_INCREMENT = {id}"
            self.cur.execute(alter_query)
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')      
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.groupBox_3.setEnabled(True)
        self.checkBox.setChecked(True)
        self.pushButton.setEnabled(False)
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
        user_date = self.dateEdit.date().toString(QtCore.Qt.ISODate)        
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
        INSERT INTO user(user_fullname, un_id, user_gender, user_phone, user_address, user_job, user_date, user_name, user_password, is_user)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''',(user_full_name, user_nid, user_gender, user_phone, user_address, user_job, user_date, user_name, user_password, is_user))

        self.db.commit()        
        self.user_table_fill()
        self.user_combo_fill()
        self.user_field_clear()   

    def user_search(self):
        name = self.lineEdit.text()
        if name == '' :
            QMessageBox.warning(self, 'رسالة تنبيه', 'من فضلك ادخل الاسم المراد البحث عنه', QMessageBox.Ok)
            return
        sql = f''' SELECT * FROM user WHERE user_fullname LIKE '%{name}%' '''
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
        self.lineEdit_6.setText(str(data[0][5]))
        self.comboBox_2.setCurrentText(data[0][6])
        self.lineEdit_7.setText(str(data[0][7]))
        self.lineEdit_8.setText(str(data[0][8]))
        self.dateEdit.setDate(data[0][9])
        self.lineEdit.setText('')
        matching_item = self.tableWidget.findItems(self.lineEdit_3.text(), Qt.MatchContains)        
        self.tableWidget.setCurrentItem(matching_item[0])
        self.pushButton.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_4.setEnabled(True)
        
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
        UPDATE user SET un_id=%s, user_fullname=%s, user_gender=%s, user_phone=%s, user_address=%s, user_job=%s, user_name=%s, user_password=%s, user_date=%s, is_user=%s
        WHERE id=%s''', (user_nid, user_full_name, user_gender, user_phone, user_address, user_job, user_name, user_password, user_date, is_user, u_id))

        self.db.commit()       
        self.user_table_fill()
        self.user_field_clear()

    def user_delete(self):
                
        u_id = int(self.lineEdit_2.text())
        try:        
            sql = ('''DELETE FROM user WHERE id = %s ''')
            self.cur.execute(sql, [(u_id)])
            self.db.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            self.db.rollback()
            # print(f"Error: {e}")  # Optionally log or show the error to the user 
            QMessageBox.warning(self, 'رسالة تحذير', 'لايمكن حذف هذا السجل نظرا للاعتماد عليه في بعض سجلات قاعدة البيانات', QMessageBox.Ok)
            return
        self.user_table_fill()
        self.user_field_clear()

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
        self.comboBox_26.clear()
        self.cur.execute('''SELECT user_fullname, user_job FROM user ORDER BY id ''')
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
            self.comboBox_26.addItem(user[0])

    def user_field_clear(self):

        self.groupBox_3.setEnabled(False)
        self.checkBox.setChecked(False)
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')

# =========== Customers ===========
    
    def customer_save_enabled(self):
        if self.lineEdit_9.text() != '':
            self.pushButton_7.setEnabled(True)        

    def customer_table_select(self):
        row = self.tableWidget_2.currentItem().row()
        id = self.tableWidget_2.item(row, 0).text()
        sql = f"SELECT * FROM customer WHERE id={id}"
        self.cur.execute(sql) #, [(id)])
        data = self.cur.fetchone()
        #h, m, s = map(int, (str(data[5]).split(":")))
        #x = QTime(h, m)
        self.lineEdit_9.setText(str(data[0]))
        self.lineEdit_10.setText(str(data[1]))
        #self.lineEdit_11.setText(str(data[5]))
        #self.comboBox_3.setCurrentText(data[2])
        self.lineEdit_12.setText(str(data[2]))
        self.lineEdit_13.setText(str(data[3]))       
        self.dateEdit_2.setDate(data[4])
        #self.timeEdit.setTime(x)
        self.pushButton_6.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.pushButton_9.setEnabled(True)


    def customer_field_clear(self):
        self.pushButton_6.setEnabled(True)
        self.pushButton_7.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_9.setEnabled(False)
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
        SELECT id, customer_name, customer_phone, customer_address, customer_date FROM customer
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
        SELECT id FROM customer  ORDER BY id ''')
        row = self.cur.fetchall()
        if row == [] :
            self.lineEdit_9.setText('1')
        else:
            self.lineEdit_9.setText(str(row[-1][0] + 1))
            id = int(self.lineEdit_9.text())
            alter_query = f"ALTER TABLE customer AUTO_INCREMENT = {id}"
            self.cur.execute(alter_query)
        self.lineEdit_10.setText('')
        self.lineEdit_11.setText('')
        self.lineEdit_12.setText('')
        self.lineEdit_13.setText('')      
        self.lineEdit_14.setText('')
        self.pushButton_6.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_9.setEnabled(False)

    def customer_save(self):        
        customer_name = self.lineEdit_10.text()
        #customer_type = self.lineEdit_11.text()
        #customer_gender = self.comboBox_3.currentText()
        customer_phone = self.lineEdit_12.text()
        customer_address = self.lineEdit_13.text()
        #customer_balance = self.lineEdit_14.text()
        customer_date = self.dateEdit_2.date()
        customer_date = customer_date.toString(QtCore.Qt.ISODate)
        customer_time = self.timeEdit.time()
        customer_time = customer_time.toString(QtCore.Qt.ISODate)
        if customer_name == '' or customer_phone == '' or customer_address == '' :
            QMessageBox.warning(self, 'رسالة تحذير', 'من فضلك ادخل جميع البيانات المطلوبة', QMessageBox.Ok)
            return
        self.cur.execute('''
            INSERT INTO customer(customer_name, customer_phone, customer_address, customer_date)
            VALUES(%s, %s, %s, %s)
              ''',(customer_name, customer_phone, customer_address, customer_date))

        self.db.commit()        
        self.customer_table_fill()
        self.customer_combo_fill()
        self.customer_field_clear() 

    def customer_search(self):
        name = self.lineEdit_15.text()
        if name == '' :
            QMessageBox.warning(self, 'رسالة تنبيه', 'من فضلك ادخل الاسم المراد البحث عنه', QMessageBox.Ok)
            return        
        sql = f''' SELECT * FROM customer WHERE customer_name LIKE '%{name}%' '''                    
        self.cur.execute(sql)
        data = self.cur.fetchall()      
        if data == []:
            QMessageBox.warning(self, 'لا توجد بيانات',  'لا توجد بيانات تخص المعلومات التي أدخلتها', QMessageBox.Ok)
            return        
        #h, m, s = map(int, (str(data[0][8])).split(":"))        
        #x = QTime(h, m)        
        self.lineEdit_9.setText(str(data[0][0]))
        self.lineEdit_10.setText(str(data[0][1]))
        #self.lineEdit_11.setText(str(data[0][5]))
        #self.comboBox_3.setCurrentText(data[0][2])
        self.lineEdit_12.setText(str(data[0][2]))
        self.lineEdit_13.setText(str(data[0][3]))
        #self.lineEdit_14.setText(str(data[0][6]))
        self.dateEdit_2.setDate(data[0][4])        
        #self.timeEdit.setTime(x) 
        self.lineEdit_15.setText('')
        item = self.tableWidget_2.findItems(self.lineEdit_10.text(), Qt.MatchContains)        
        self.tableWidget_2.setCurrentItem(item[0])
        self.pushButton_6.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.pushButton_9.setEnabled(True)

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
        UPDATE customer SET customer_name=%s, customer_phone=%s, customer_address=%s, customer_date=%s
        WHERE id=%s''', (customer_name, customer_phone, customer_address, customer_date, id))

        self.db.commit()       
        self.customer_table_fill()        
        self.customer_field_clear()

    def customer_delete(self):        
        id = self.lineEdit_9.text()

        try:        
            sql = ('''DELETE FROM customer WHERE id = %s ''')
            self.cur.execute(sql, [(id)])
            self.db.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            self.db.rollback()
            # print(f"Error: {e}")  # Optionally log or show the error to the user 
            QMessageBox.warning(self, 'رسالة تحذير', 'لايمكن حذف هذا السجل نظرا للاعتماد عليه في بعض سجلات قاعدة البيانات', QMessageBox.Ok)
            return              
        self.customer_table_fill()
        self.customer_field_clear()

    def customer_combo_fill(self):
        self.comboBox_24.clear()
        self.cur.execute('''SELECT customer_name FROM customer ORDER BY id ''')
        customers = self.cur.fetchall()        
        for customer in customers:
            self.comboBox_24.addItem(customer[0])

    def customer_info(self):
        cus_name = self.comboBox_24.currentText()
        self.cur.execute("SELECT * FROM customer WHERE customer_name=%s", ([cus_name]) )
        data = self.cur.fetchone()
        if data != None:
            self.lineEdit_97.setText(data[2])
            self.lineEdit_98.setText(data[3])               
        
# =========== Importers ===========

    def importer_save_enabled(self):
        if self.lineEdit_17.text() != '':
            self.pushButton_13.setEnabled(True)       

    def importer_table_select(self):
        row = self.tableWidget_3.currentItem().row()
        id = self.tableWidget_3.item(row, 0).text()
        grp_id = self.tableWidget_3.item(row, 4).text()
        company_id = self.tableWidget_3.item(row, 5).text()
        sql = f'''SELECT i.*, g.grp_name, c.company_name
                FROM importer i
                LEFT JOIN grp g ON g.id = {grp_id}
                LEFT JOIN company c ON c.id = {company_id}
                WHERE i.id = {id}'''
        self.cur.execute(sql)
        data = self.cur.fetchone()        
        h, m, s = map(int, (str(data[8])).split(":"))
        x = QTime(h, m)
        self.lineEdit_17.setText(str(data[0]))
        self.lineEdit_18.setText(str(data[1]))        
        self.lineEdit_20.setText(str(data[2]))
        self.lineEdit_21.setText(str(data[3]))
        self.lineEdit_22.setText(str(data[6]))
        self.comboBox_22.setCurrentText(data[9])
        self.comboBox_23.setCurrentText(data[10])
        self.dateEdit_3.setDate(data[7])        
        self.timeEdit_2.setTime(x)
        self.pushButton_12.setEnabled(True)
        self.pushButton_14.setEnabled(True)
        self.pushButton_15.setEnabled(True)

    def importer_field_clear(self):
        self.pushButton_12.setEnabled(True)
        self.pushButton_13.setEnabled(False)
        self.pushButton_14.setEnabled(False)
        self.pushButton_15.setEnabled(False)
        self.lineEdit_17.setText('')
        self.lineEdit_18.setText('')
        self.lineEdit_19.setText('')
        self.lineEdit_20.setText('')      
        self.lineEdit_21.setText('')
        self.lineEdit_22.setText('')

    def importer_table_fill(self):        
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)
        self.cur.execute("SELECT * FROM importer")
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_pos)

    def importer_add_new(self):
        self.cur.execute('''
        SELECT id FROM importer  ORDER BY id ''')
        row = self.cur.fetchall()
        if row == [] :
            self.lineEdit_17.setText('1')
        else:
            self.lineEdit_17.setText(str(row[-1][0] + 1))
            id = int(self.lineEdit_17.text())
            alter_query = f"ALTER TABLE importer AUTO_INCREMENT = {id}"
            self.cur.execute(alter_query)
                   
        self.lineEdit_18.setText('')
        self.lineEdit_19.setText('')
        self.lineEdit_20.setText('')
        self.lineEdit_21.setText('')      
        self.lineEdit_22.setText('')
        self.pushButton_12.setEnabled(False)
        self.pushButton_13.setEnabled(False)
        self.pushButton_14.setEnabled(False)
        self.pushButton_15.setEnabled(False)
        

    def importer_save(self):
        importer_name = self.lineEdit_18.text()        
        importer_phone = self.lineEdit_20.text()
        importer_address = self.lineEdit_21.text()
        importer_balance = self.lineEdit_22.text()
        importer_grp = self.comboBox_22.currentText()
        importer_company = self.comboBox_23.currentText()
        importer_date = self.dateEdit_3.date().toString(QtCore.Qt.ISODate)
        importer_time = self.timeEdit_2.time().toString(QtCore.Qt.ISODate)

        insert_sql = '''
            INSERT INTO importer(importer_name, importer_phone, importer_address, importer_balance, importer_date, importer_time, importer_grp_id, importer_company_id)
            SELECT %s, %s, %s, %s, %s, %s,
                         (SELECT id FROM grp WHERE grp_name = %s),
                         (SELECT id FROM company WHERE company_name = %s)
              '''
        self.cur.execute(insert_sql,(importer_name, importer_phone, importer_address, importer_balance, importer_date, importer_time, importer_grp, importer_company))
        self.db.commit()        
        self.importer_table_fill()
        self.importer_combo_fill()
        self.importer_field_clear()

    def importer_search(self):
        name = self.lineEdit_16.text()
        if name == '' :
            QMessageBox.warning(self, 'رسالة تنبيه', 'من فضلك ادخل الاسم المراد البحث عنه', QMessageBox.Ok)
            return        
        sql = f''' SELECT * FROM importer WHERE importer_name LIKE '%{name}%' '''            
        self.cur.execute(sql)
        data = self.cur.fetchall()        
        if data == []:
            QMessageBox.warning(self, 'لا توجد بيانات',  'لا توجد بيانات تخص المعلومات التي أدخلتها', QMessageBox.Ok)
            return
        h, m, s = map(int, (str(data[0][8]).split(":")))
        x = QTime(h, m)
        self.lineEdit_17.setText(str(data[0][0]))
        self.lineEdit_18.setText(str(data[0][1]))
        self.lineEdit_19.setText(str(data[0][4]))
        self.lineEdit_20.setText(str(data[0][2]))
        self.lineEdit_21.setText(str(data[0][3]))
        self.lineEdit_22.setText(str(data[0][5]))
        self.timeEdit_2.setTime(x)
        self.dateEdit_3.setDate(data[0][7])
        self.lineEdit_16.setText('')
        item = self.tableWidget_3.findItems(self.lineEdit_18.text(), Qt.MatchContains)        
        self.tableWidget_3.setCurrentItem(item[0])
        self.pushButton_12.setEnabled(True)
        self.pushButton_14.setEnabled(True)
        self.pushButton_15.setEnabled(True)


    def importer_update(self):
        id = self.lineEdit_17.text()
        importer_name = self.lineEdit_18.text()        
        importer_type = self.lineEdit_19.text()
        importer_phone = self.lineEdit_20.text()
        importer_address = self.lineEdit_21.text()
        importer_balance = self.lineEdit_22.text()
        grp_name = self.comboBox_22.currentText()
        company_name = self.comboBox_23.currentText()
        importer_date = self.dateEdit_3.date().toString(QtCore.Qt.ISODate)        
        importer_time = self.timeEdit_2.time().toString(QtCore.Qt.ISODate)        
        
        self.cur.execute('''
        UPDATE importer SET importer_name=%s, importer_phone=%s, 
        importer_address=%s, importer_grp_id=(SELECT id FROM grp WHERE grp_name=%s), 
        importer_company_id=(SELECT id FROM company WHERE company_name=%s),
        importer_balance=%s, importer_date=%s, importer_time=%s
        WHERE id=%s''', (importer_name, importer_phone, importer_address, grp_name, company_name, importer_balance, importer_date, importer_time, id))
        self.db.commit()       
        self.importer_table_fill()
        self.importer_field_clear()

    def importer_delete(self):        
        id = self.lineEdit_17.text()
        try:        
            sql = ('''DELETE FROM importer WHERE id = %s ''')
            self.cur.execute(sql, [(id)])
            self.db.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            self.db.rollback()
            # print(f"Error: {e}")  # Optionally log or show the error to the user 
            QMessageBox.warning(self, 'رسالة تحذير', 'لايمكن حذف هذا السجل نظرا للاعتماد عليه في بعض سجلات قاعدة البيانات', QMessageBox.Ok)
            return
        self.db.commit()       
        self.importer_table_fill()
        self.importer_field_clear()

    def importer_info(self):
        
        imp_name = self.comboBox_9.currentText()
        if imp_name != '':
            sql = '''SELECT i.importer_phone, i.importer_balance, g.grp_name, c.company_name 
            FROM importer i
            JOIN grp g ON g.id = i.importer_grp_id
            JOIN company c ON c.id = i.importer_company_id
            WHERE importer_name=%s'''
            self.cur.execute(sql, [(imp_name)])
            data = self.cur.fetchone()               
            self.lineEdit_49.setText(str(data[0]))
            self.lineEdit_51.setText(str(data[1]))
            self.lineEdit_53.setText(str(data[2]))
            self.lineEdit_54.setText(str(data[3]))

    def importer_combo_fill(self):
        self.comboBox_6.clear()
        self.comboBox_9.clear()        
        self.comboBox_10.clear()
        self.cur.execute('''SELECT importer_name FROM importer ORDER BY id ''')
        importers = self.cur.fetchall()
        for importer in importers:
            self.comboBox_6.addItem(importer[0])
            self.comboBox_9.addItem(importer[0])           
            self.comboBox_10.addItem(importer[0])   
    
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
        self.pushButton_16.setEnabled(True)

    def item_table_fill(self):        
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)
        
        self.cur.execute("SELECT item_name, item_barcode,item_unit, item_buybill_id, \
            item_price, item_qty, item_discount, item_public_price FROM item")
        data = self.cur.fetchall()
        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_4.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_pos)

    def item_table_select(self):
        row = self.tableWidget_4.currentItem().row()
        barcode = self.tableWidget_4.item(row, 1).text()              

        sql = f''' SELECT i.* , g.grp_name, c.company_name, im.importer_name, b.buy_date
            FROM item i
            LEFT JOIN buybill b ON b.id = i.item_buybill_id AND b.buy_importer_id = i.item_importer_id
            LEFT JOIN importer im ON im.id = i.item_importer_id
            LEFT JOIN grp g ON g.id = im.importer_grp_id
            LEFT JOIN company c ON c.id = im.importer_company_id
            WHERE i.item_barcode = {barcode} ''' 

        self.cur.execute(sql)
        data = self.cur.fetchone()       
       
        self.lineEdit_24.setText(str(data[0]))
        self.lineEdit_25.setText(str(data[2]))
        self.lineEdit_26.setText(str(data[1]))
        self.comboBox_4.setCurrentText(str(data[10]))
        self.comboBox_5.setCurrentText(str(data[11]))
        self.comboBox_6.setCurrentText(str(data[12]))
        self.lineEdit_27.setText(str(data[8]))        
        self.lineEdit_28.setText(str(data[6]))
        self.lineEdit_29.setText(str(data[5]))
        self.lineEdit_30.setText(str(data[7]))
        self.lineEdit_31.setText(str(data[3]))
        self.dateEdit_4.setDate(data[13])

        self.pushButton_18.setEnabled(True)
        self.pushButton_19.setEnabled(True)



    def item_add_new(self):
        self.cur.execute('''
        SELECT id FROM item ORDER BY id ''')
        row = self.cur.fetchall()
        # when using database first time
        if row == []:
            self.lineEdit_24.setText('1')
        else:
            self.lineEdit_24.setText(str(row[-1][0] + 1))
        self.lineEdit_23.setText('')                
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
        item_discount = self.lineEdit_30.text()
        item_unit = self.lineEdit_31.text()
        item_group = self.comboBox_4.currentText()
        item_company = self.comboBox_5.currentText()        
        if item_name == '' or item_price == '' or item_qty == '' :
            QMessageBox.warning(self, 'بيانات ناقصة', 'من فضلك أدخل البيانات الناقصة', QMessageBox.Ok)
            return
        self.cur.execute('''
            INSERT INTO item(item_buybill_id, item_barcode, item_name, item_group_id, item_company_id, item_price, item_public_price, item_discount, item_qty, item_unit)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ''',(item_barcode, item_name, item_group, item_company, item_price, item_qty, item_discount, item_unit))

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
        sql = f''' SELECT i.* , b.buy_date, g.grp_name, c.company_name, im.importer_name
        FROM item i
        LEFT JOIN buybill b ON b.id = i.item_buybill_id AND b.buy_importer_id = i.item_importer_id
        LEFT JOIN importer im ON im.id = i.item_importer_id
        LEFT JOIN grp g ON g.id = im.importer_grp_id
        LEFT JOIN company c ON c.id = im.importer_company_id
        WHERE i.item_name LIKE '%{name}%' '''            
        self.cur.execute(sql)
        data = self.cur.fetchone()
        if data == None:
            QMessageBox.warning(self, ' إفادة', 'الصنف الذي تبحث عنه غير موجود', QMessageBox.Ok)
            return

        self.lineEdit_24.setText(str(data[0]))
        self.lineEdit_25.setText(str(data[2]))
        self.lineEdit_26.setText(str(data[1]))
        self.comboBox_4.setCurrentText(data[11])
        self.comboBox_5.setCurrentText(data[12])
        self.comboBox_6.setCurrentText(data[13])
        self.lineEdit_27.setText(str(data[8]))
        self.lineEdit_28.setText(str(data[6]))
        self.lineEdit_29.setText(str(data[5]))
        self.lineEdit_30.setText(str(data[7]))
        self.lineEdit_31.setText(str(data[3]))
        self.dateEdit_4.setDate(data[10])
        item = self.tableWidget_4.findItems(name, Qt.MatchContains)        
        self.tableWidget_4.setCurrentItem(item[0])
        

    def item_update(self):
        id = self.lineEdit_24.text()
        barcode = self.lineEdit_25.text()
        name = self.lineEdit_26.text()        
        pub_price = self.lineEdit_27.text()
        qty = self.lineEdit_28.text()
        buy_price = self.lineEdit_29.text()
        discount = self.lineEdit_30.text()
        unit = self.lineEdit_31.text()
        group = self.comboBox_4.currentText()
        company = self.comboBox_5.currentText()
        importer = self.comboBox_6.currentText()
        date = self.dateEdit_4.date().toString(QtCore.Qt.ISODate)
            
        self.cur.execute('''
        UPDATE item SET item_name=%s, item_unit=%s, 
        item_price=%s, item_qty=%s, item_discount=%s, item_public_price=%s        
        WHERE item_barcode=%s''', (name, unit, buy_price, qty, discount, 
        pub_price, barcode))
        self.db.commit()
        self.item_table_fill()
        

    def item_delete(self):        
        barcode = self.lineEdit_25.text()
        sql = ('''DELETE FROM item WHERE item_barcode = %s ''')
        self.cur.execute(sql, [(barcode)])

        self.db.commit()       
        self.item_table_fill()
        self.item_clear()
        self.pushButton_16.setEnabled(True)        
        self.pushButton_18.setEnabled(False)
        self.pushButton_19.setEnabled(False)

    def item_combo_fill(self):        
        self.comboBox_13.clear()
        self.comboBox_16.clear()
        self.comboBox_25.clear()
        self.cur.execute('''SELECT item_name FROM item ORDER BY id ''')
        items = self.cur.fetchall()
        for item in items:            
            self.comboBox_13.addItem(item[0])
            self.comboBox_16.addItem(item[0])
            self.comboBox_25.addItem(item[0])


    def item_bill_save_but(self):
        if self.pushButton_37.isEnabled():
            self.pushButton_34.setEnabled(False)
        else:
            self.pushButton_34.setEnabled(True)
    
# =========== Groups ===========

    def grp_add_new(self):

        self.cur.execute('''
        SELECT id FROM grp  ORDER BY id ''')
        row = self.cur.fetchall()
        if row == [] :
            self.lineEdit_35.setText('1')
        else:
            self.lineEdit_35.setText(str(row[-1][0] + 1))
            id = int(self.lineEdit_35.text())
            alter_query = f"ALTER TABLE grp AUTO_INCREMENT = {id}"
            self.cur.execute(alter_query)                
        self.lineEdit_36.setText('')
        self.pushButton_21.setEnabled(False)
        self.pushButton_22.setEnabled(False)
        self.pushButton_51.setEnabled(False)
        self.pushButton_54.setEnabled(False)

    def grp_save(self):
        # Get values from the UI
        grp_name = self.lineEdit_36.text()
        grp_date = self.dateEdit_5.date().toString(Qt.ISODate)
        grp_time = self.timeEdit_3.time().toString(Qt.ISODate)
        grp_user = self.comboBox_17.currentText()

        # Insert directly using a subquery to get the user_id
        insert_sql = '''
            INSERT INTO grp (grp_name, grp_date, grp_time, grp_user_id)
            SELECT %s, %s, %s, id
            FROM user
            WHERE user_fullname = %s
        '''

        # Execute the SQL with the appropriate parameters
        try:
            self.cur.execute(insert_sql, (grp_name, grp_date, grp_time, grp_user))
            
            # Commit the transaction
            self.db.commit()

        except Exception as e:
            # Rollback the transaction in case of an error
            self.db.rollback()
            print(f"Error: {e}")  # Optionally log or show the error to the user        
        self.grp_table_fill()
        self.grp_combo_fill()        
        self.grp_field_clear()

    def grp_update(self):
        grp_id = self.lineEdit_35.text()
        grp_name = self.lineEdit_36.text()        
        grp_date = self.dateEdit_5.date().toString(QtCore.Qt.ISODate)        
        grp_time = self.timeEdit_3.time().toString(QtCore.Qt.ISODate)        
        grp_user = self.comboBox_17.currentText()

        # Single query using a subquery to get user_id
        sql = '''
        UPDATE grp 
        SET grp_name=%s, grp_date=%s, grp_time=%s, grp_user_id=(
            SELECT id FROM user WHERE user_fullname=%s
        )
        WHERE id=%s
        '''
        self.cur.execute(sql, (grp_name, grp_date, grp_time, grp_user, grp_id))
        self.db.commit()
        self.grp_table_fill()
        self.grp_field_clear()

    def grp_delete(self):
        id = self.lineEdit_35.text()
        try:        
            sql = ('''DELETE FROM grp WHERE id = %s ''')
            self.cur.execute(sql, [(id)])
            self.db.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            self.db.rollback()
            # print(f"Error: {e}")  # Optionally log or show the error to the user 
            QMessageBox.warning(self, 'رسالة تحذير', 'لايمكن حذف هذا السجل نظرا للاعتماد عليه في بعض سجلات قاعدة البيانات', QMessageBox.Ok)
            return
        self.db.commit()
        self.lineEdit_35.setText('')
        self.lineEdit_36.setText('')
        self.grp_table_fill()
        self.grp_combo_fill()
        self.grp_field_clear()
        self.company_combo_fill
        self.company_table_fill
        

    def grp_combo_fill(self):
        self.comboBox_4.clear()
        self.comboBox_21.clear()
        self.comboBox_22.clear()
        self.cur.execute('''SELECT grp_name FROM grp ORDER BY id ''')
        grops = self.cur.fetchall()
        for grop in grops:
            self.comboBox_4.addItem(grop[0])
            self.comboBox_21.addItem(grop[0])
            self.comboBox_22.addItem(grop[0])
            

    def grp_save_enabled(self):
        self.pushButton_21.setEnabled(True)

    def grp_table_fill(self):        
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        self.cur.execute(''' SELECT * FROM grp ''')
        data = self.cur.fetchall()

        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_5.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_pos)


    def grp_table_select(self):
        row = self.tableWidget_5.currentItem().row()
        grp_id = self.tableWidget_5.item(row, 0).text()
        user_id = self.tableWidget_5.item(row, 4).text()
        # Combined SQL query with JOINs to get user_fullname and grp_name in one query
        sql = f"""
        SELECT grp.*, user.user_fullname
        FROM grp
        LEFT JOIN user ON user.id = {user_id}       
        WHERE grp.id = {grp_id}
        """
        self.cur.execute(sql)
        data = self.cur.fetchone()        
        self.lineEdit_35.setText(str(data[0]))
        self.lineEdit_36.setText(str(data[1]))
        self.dateEdit_5.setDate(data[2])       
        # Convert timedelta to hours, minutes, and seconds
        hours, remainder = divmod(data[3].total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        # Set the time in QTimeEdit
        self.timeEdit_3.setTime(QTime(int(hours), int(minutes), int(seconds)))        
        user_name = data[5]
        self.comboBox_17.setCurrentText(user_name)               
        self.pushButton_21.setEnabled(False)
        self.pushButton_51.setEnabled(True)
        self.pushButton_22.setEnabled(True)
        self.pushButton_54.setEnabled(True)

    def grp_field_clear(self):

        self.pushButton_51.setEnabled(True)
        self.pushButton_21.setEnabled(False)
        self.pushButton_22.setEnabled(False)
        self.pushButton_54.setEnabled(False)
        self.lineEdit_35.setText('')
        self.lineEdit_36.setText('')
        
#=========== Companies ===========

    def company_add_new(self):

        self.cur.execute('''
        SELECT id FROM company  ORDER BY id ''')
        row = self.cur.fetchall()
        if row == [] :
            self.lineEdit_37.setText('1')
        else:
            self.lineEdit_37.setText(str(row[-1][0] + 1))
            id = int(self.lineEdit_37.text())
            alter_query = f"ALTER TABLE company AUTO_INCREMENT = {id}"
            self.cur.execute(alter_query)       
        self.lineEdit_38.setText('')
        self.pushButton_23.setEnabled(False)
        self.pushButton_24.setEnabled(False)
        self.pushButton_55.setEnabled(False)
        self.pushButton_56.setEnabled(False)

    def company_save(self):        
        company_name = self.lineEdit_38.text()
        company_date = self.dateEdit_6.date().toString(Qt.ISODate)        
        company_time = self.timeEdit_4.time().toString(Qt.ISODate)        
        company_user = self.comboBox_18.currentText()
        company_grp = self.comboBox_21.currentText()

        # Combine the SELECT queries into the INSERT statement
        insert_sql = '''
            INSERT INTO company (company_name, company_date, company_time, company_user_id, company_grp_id)
            SELECT %s, %s, %s,
                (SELECT id FROM user WHERE user_fullname = %s),
                (SELECT id FROM grp WHERE grp_name = %s)
        '''
        
        # Execute the combined query
        try:
            self.cur.execute(insert_sql, (company_name, company_date, company_time, company_user, company_grp))
            
            # Commit the transaction
            self.db.commit()

        except Exception as e:
            # Rollback the transaction if an error occurs
            self.db.rollback()
            print(f"Error: {e}")
            # Optionally, you could show an error message to the user
        self.company_table_fill()
        self.company_combo_fill()
        self.company_field_clear()

    def company_update(self):
        id = self.lineEdit_37.text()
        company_name = self.lineEdit_38.text()        
        company_date = self.dateEdit_6.date().toString(QtCore.Qt.ISODate)        
        company_time = self.timeEdit_4.time().toString(QtCore.Qt.ISODate)        
        company_user = self.comboBox_18.currentText()
        company_grp = self.comboBox_21.currentText()
        self.cur.execute('''
        UPDATE company SET company_name=%s, company_date=%s, company_time=%s, 
        company_user_id=(SELECT id FROM user WHERE user_fullname=%s),
        company_grp_id=(SELECT id FROM grp WHERE grp_name=%s)
        WHERE id=%s''', (company_name, company_date, company_time, company_user, company_grp, id))
        self.db.commit()       
        self.company_table_fill()
        self.company_field_clear()

    def company_delete(self):
        id = self.lineEdit_37.text()
        try:        
            sql = ('''DELETE FROM company WHERE id = %s ''')
            self.cur.execute(sql, [(id)])
            self.db.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            self.db.rollback()
            # print(f"Error: {e}")  # Optionally log or show the error to the user 
            QMessageBox.warning(self, 'رسالة تحذير', 'لايمكن حذف هذا السجل نظرا للاعتماد عليه في بعض سجلات قاعدة البيانات', QMessageBox.Ok)
            return
        self.db.commit() 
     
        self.company_table_fill()
        self.company_combo_fill()
        self.company_field_clear()       

    def company_combo_fill(self):
        self.comboBox_5.clear()
        self.comboBox_23.clear()
        self.cur.execute('''SELECT company_name FROM company ORDER BY id ''')
        companies = self.cur.fetchall()
        for company in companies:
            self.comboBox_5.addItem(company[0])
            self.comboBox_23.addItem(company[0])

    def company_save_enabled(self):
        self.pushButton_23.setEnabled(True)

    def company_table_fill(self):        
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)
        self.cur.execute('''
        SELECT * FROM company
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
        company_id = self.tableWidget_6.item(row, 0).text()
        user_id = self.tableWidget_6.item(row, 4).text()
        grp_id = self.tableWidget_6.item(row, 5).text()
        
        
        # Combined SQL query with JOINs to get user_fullname and grp_name in one query
        sql = f"""
        SELECT company.*, user.user_fullname, grp.grp_name 
        FROM company
        LEFT JOIN user ON user.id = {user_id}
        LEFT JOIN grp ON grp.id = {grp_id}
        WHERE company.id = {company_id}
        """        
        self.cur.execute(sql)
        data = self.cur.fetchone()

        # Assuming data is in this order: company.*, user_fullname, grp_name
        self.lineEdit_37.setText(str(data[0]))
        self.lineEdit_38.setText(str(data[1]))                            
        self.dateEdit_6.setDate(data[2])

        # Convert timedelta to hours, minutes, and seconds
        hours, remainder = divmod(data[3].total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Set the time in QTimeEdit
        self.timeEdit_4.setTime(QTime(int(hours), int(minutes), int(seconds)))

        # user_fullname and grp_name are at the end of the fetched row
        user_name = data[-2]
        grp_name = data[-1]
        
        # Set user_fullname and grp_name in combo boxes
        self.comboBox_18.setCurrentText(user_name)
        self.comboBox_21.setCurrentText(grp_name)

        # Enable/Disable buttons
        self.pushButton_23.setEnabled(False)
        self.pushButton_24.setEnabled(True)
        self.pushButton_55.setEnabled(True)
        self.pushButton_56.setEnabled(True)

    def company_field_clear(self):

        self.pushButton_55.setEnabled(True)
        self.pushButton_23.setEnabled(False)
        self.pushButton_56.setEnabled(False)
        self.pushButton_24.setEnabled(False)
        self.lineEdit_37.setText('')
        self.lineEdit_38.setText('')

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

        self.timeEdit_6.setTime(QTime.currentTime())
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
        if data == None:
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
        else:                       
            msgbox = QMessageBox(QMessageBox.Warning, "تنويه", "لقد تم تسجيل حضور الموظف : %s   هذا اليوم بالفعل" % emp_name, QMessageBox.Ok)
            msgbox.exec_()            

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
        self.timeEdit_6.setTime(QTime.currentTime())
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

    def enabled_buy_item_but(self):
        self.pushButton_33.setEnabled(True)

    def buy_item_add_new(self):
        code = self.lineEdit_73.text()
        name = self.lineEdit_68.text()
        qty = self.lineEdit_69.text()
        unit = self.lineEdit_66.text()
        discount = self.lineEdit_70.text()
        tot_discount = self.lineEdit_100.text()
        bill_id = int(self.lineEdit_72.text())        
        price = self.lineEdit_71.text()
        total = self.lineEdit_67.text()
        public = self.lineEdit_65.text()
        importer = self.comboBox_9.currentText()
        query = "INSERT INTO item (item_name, item_barcode, item_unit, \
        item_buybill_id, item_price, item_qty, item_discount, item_public_price, \
        item_importer_id) SELECT %s, %s, %s, %s, %s, %s, %s, %s, \
        (SELECT id FROM importer WHERE importer_name=%s)"
        self.cur.execute(query, (name, code, unit, bill_id, price, qty, discount, public, importer) )
        self.db.commit()
        query = "INSERT INTO buybill_details (buybill_id, item_price, item_qty, item_discount, item_total, item_id) SELECT %s,%s,%s,%s,%s, (SELECT id FROM item WHERE item_barcode=%s) "
        self.cur.execute(query, (bill_id, price, qty, tot_discount,total, code))
        self.db.commit()
        query = '''
            UPDATE buybill b
            SET 
                b.buy_total_price = (
                    SELECT SUM(bd.item_total) 
                    FROM buybill_details bd 
                    WHERE bd.buybill_id = b.id
                ),
                b.buy_discount = (
                    SELECT SUM(bd.item_discount) 
                    FROM buybill_details bd 
                    WHERE bd.buybill_id = b.id
                ),
                b.buy_item_count = (
                    SELECT COUNT(*) 
                    FROM buybill_details bd 
                    WHERE bd.buybill_id = b.id
                )
            WHERE 
                b.id = %s
            '''
        params = (bill_id,)
        self.cur.execute(query, params)
        self.db.commit()

        sql = f"SELECT SUM(item_total), SUM(item_discount), COUNT(id) FROM buybill_details WHERE buybill_id = {bill_id}"
        self.cur.execute(sql)
        data = self.cur.fetchone()        
        self.lineEdit_57.setText(str(data[0]))
        self.lineEdit_56.setText(str(data[1]))
        self.lineEdit_58.setText(str(data[2]))

        self.lineEdit_73.setText('')
        self.lineEdit_68.setText('')
        self.lineEdit_69.setText('0')
        self.lineEdit_66.setText('')
        self.lineEdit_70.setText('0')
        self.lineEdit_71.setText('0')
        self.lineEdit_65.setText('0')
        self.pushButton_31.setEnabled(True)
        self.pushButton_33.setEnabled(False)
        self.buy_item_table_fill()

    def buy_item_search(self):

        self.lineEdit_72.setEnabled(True)
        bb_id = self.lineEdit_72.text()
        code = self.lineEdit_73.text()
        if self.lineEdit_72.text() == '' or self.lineEdit_73.text()=='':
            QMessageBox.warning(self, 'بيانات ناقصة', 'من فضلك أدخل رقم الفاتورة والباركود', QMessageBox.Ok)
            return

        query = '''SELECT b.*,item_name, i.item_unit, i.item_public_price
            FROM buybill_details b
            LEFT JOIN item i 
            ON i.item_barcode = %s
            WHERE b.buybill_id = %s AND b.item_id=i.id
            '''
        self.cur.execute(query, (code, int(bb_id)))        
        data = self.cur.fetchone()

        if data == None:
            QMessageBox.warning(self, 'بيانات خاطئة', 'هذا المنتج لايوجد في هذه الفاتورة', QMessageBox.Ok)
            return
        
        self.lineEdit_68.setText(data[7])
        self.lineEdit_69.setText(str(data[4]))
        self.lineEdit_70.setText(str(data[5]))
        self.lineEdit_71.setText(str(data[3]))
        self.lineEdit_67.setText(str(data[6]))
        self.lineEdit_65.setText(str(data[9]))          
        self.lineEdit_66.setText(str(data[8]))
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

    def buy_item_update(self):

        code = self.lineEdit_73.text()
        bb_id = self.lineEdit_72.text()
        name = self.lineEdit_68.text()        
        unit = self.lineEdit_66.text()
        qty = Decimal(self.lineEdit_69.text())
        price = Decimal(self.lineEdit_71.text())
        public_price = Decimal(self.lineEdit_65.text())
        total = Decimal(self.lineEdit_67.text())
        discount = Decimal(self.lineEdit_70.text())
        

        sql = '''
            UPDATE buybill_details b
            JOIN item i ON i.item_barcode = %s
            JOIN buybill bb ON bb.id = %s
            SET 
                b.item_price = %s, 
                b.item_qty = %s, 
                b.item_discount = %s, 
                b.item_total = %s, 
                i.item_name = %s, 
                i.item_unit = %s, 
                i.item_price = %s, 
                i.item_qty = %s, 
                i.item_discount = %s, 
                i.item_public_price = %s                 
            WHERE 
                b.buybill_id = %s 
                AND b.item_id = i.id;
            '''
        params = (code, bb_id, price, qty, discount, total, name, unit, price, qty, discount, public_price, bb_id)

            # تنفيذ الاستعلام
        self.cur.execute(sql, params)

        query = '''
            UPDATE buybill b
            SET 
                b.buy_total_price = (
                    SELECT SUM(bd.item_total) 
                    FROM buybill_details bd 
                    WHERE bd.buybill_id = b.id
                ),
                b.buy_discount = (
                    SELECT SUM(bd.item_discount) 
                    FROM buybill_details bd 
                    WHERE bd.buybill_id = b.id
                ),
                b.buy_item_count = (
                    SELECT COUNT(*) 
                    FROM buybill_details bd 
                    WHERE bd.buybill_id = b.id
                )
            WHERE 
                b.id = %s
            '''
        params = (bb_id,)
        self.cur.execute(query, params)
        self.db.commit()        
        self.buy_item_table_fill()        
        self.pushButton_37.setEnabled(False)
        self.pushButton_39.setEnabled(False)

    def buy_item_table_select(self, selected):
        bb_id = int(self.lineEdit_72.text())
        row = self.tableWidget_11.currentItem().row()
        band_id = self.tableWidget_11.item(row, 0).text()
        item_name = self.tableWidget_11.item(row, 1).text()
        item_code = self.tableWidget_11.item(row, 2).text()       

        query = '''SELECT b.*, i.item_unit,
            i.item_public_price, i.item_discount
            FROM buybill_details b
            LEFT JOIN item i 
            ON i.item_barcode = %s
            WHERE b.buybill_id = %s AND b.id = %s
            '''
        self.cur.execute(query, (item_code, bb_id, band_id))
        data = self.cur.fetchone()
        
        self.lineEdit_68.setText(item_name)
        self.lineEdit_69.setText(str(data[4]))
        self.lineEdit_70.setText(str(data[5]))
        self.lineEdit_71.setText(str(data[3]))
        self.lineEdit_67.setText(str(data[6]))
        self.lineEdit_65.setText(str(data[8]))
        self.lineEdit_70.setText(str(data[9]))          
        self.lineEdit_66.setText(str(data[7]))  
        self.lineEdit_73.setText(item_code)
        self.pushButton_34.setEnabled(True)
        self.pushButton_37.setEnabled(True)
        self.pushButton_39.setEnabled(True)

    def buybill_add_new(self):
        self.lineEdit_68.setText('')
        self.lineEdit_71.setText('')
        self.lineEdit_67.setText('0')
        self.lineEdit_69.setText('1')
        self.lineEdit_70.setText('0')
        self.lineEdit_66.setText('1')        
        self.lineEdit_55.setText('0')
        self.lineEdit_74.setText('0')
        self.lineEdit_54.setText('0')
        self.lineEdit_53.setText('0')
        self.pushButton_37.setEnabled(False)
        self.pushButton_39.setEnabled(False)
        self.pushButton_33.setEnabled(True)
        self.pushButton_41.setEnabled(True)        
        
    def buy_item_table_fill(self):

        bill_id = self.lineEdit_72.text()        
        self.tableWidget_11.setRowCount(0)
        self.tableWidget_11.insertRow(0)
        sql = f''' SELECT b.id, i.item_name, i.item_barcode, i.item_unit,
        i.item_public_price, b.item_discount, b.item_price, b.item_qty, b.item_total
        FROM buybill_details b 
        LEFT JOIN item i ON b.item_id = i.id
        WHERE b.buybill_id = {bill_id}
        '''
        self.cur.execute(sql)
        data = self.cur.fetchall()       
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_11.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_11.rowCount()
            self.tableWidget_11.insertRow(row_pos)

    def buy_item_delete(self):

        row = self.tableWidget_11.currentItem().row()
        id = self.tableWidget_11.item(row, 0).text()
        buybill_id = int(self.lineEdit_72.text())
        item_name = self.lineEdit_68.text()
        buy_unit_qty = self.lineEdit_69.text()

        del_item = QMessageBox.warning(self, 'مسح بيانات' , 'هل انت متأكد من حذف هذه البيانات', QMessageBox.Yes | QMessageBox.No)
        if del_item == QMessageBox.No :
            return
        else:
            sql = f" DELETE FROM buybill_details WHERE buybill_id={buybill_id} AND id={id} "
            self.cur.execute(sql)
            self.cur.execute(''' SELECT item_qty FROM item WHERE item_name=%s ''', [(item_name)])
            data = self.cur.fetchone()            
            item_qty = data[0] - Decimal(buy_unit_qty)

            self.cur.execute(''' UPDATE item SET item_qty=%s WHERE item_name=%s'''
            , (item_qty, item_name))

            self.db.commit()
            self.buy_item_table_fill()
    
    def buy_item_price(self):
        ''' 
        qty = self.lineEdit_69.text()
        item_count_peruint = self.lineEdit_66.text()
        x = int(qty) * int(item_count_peruint)
        total_buy = self.lineEdit_67.text()        
        y = float(total_buy) / x
        y = float("{:.2f}".format(y))
        item_buy_price = self.lineEdit_74.setText(str(y))
        item_buy_price = self.lineEdit_74.text()
        self.total_sale_price
        '''

    def buy_item_clear(self):
        self.lineEdit_73.setText('')
        self.lineEdit_68.setText('')
        self.lineEdit_69.setText('0')
        self.lineEdit_66.setText('')
        self.lineEdit_70.setText('0')
        self.lineEdit_71.setText('0')
        self.lineEdit_65.setText('0')
        self.pushButton_31.setEnabled(True)
        self.pushButton_33.setEnabled(False)
        self.pushButton_34.setEnabled(False)
        self.pushButton_37.setEnabled(False)
        self.pushButton_39.setEnabled(False)
        self.pushButton_41.setEnabled(False)


    def buybill_add_new(self):
        importer_name = self.comboBox_9.currentText()
        user_name = self.comboBox_11.currentText()
        buy_date = self.dateEdit_11.date().toString(Qt.ISODate)        
        buy_time = self.timeEdit_9.time().toString(Qt.ISODate)
        imp_bil_no = self.lineEdit_50.text()

        if self.lineEdit_50.text() == '':
            QMessageBox.warning(self, 'بيانات ناقصة', 'من فضلك أدخل رقم فاتورة المورد ', QMessageBox.Ok)
            return        
        self.cur.execute("SELECT id, buy_total_price FROM buybill WHERE id=(SELECT max(id) FROM buybill)")        
        data = self.cur.fetchone()        
        if data and data[1] == 0:
            id = data[0]
        else:
            if not data:
                id = 1
            else:
                if data[1] != 0:
                    id = data[0] + 1
            # Combine the SELECT queries into the INSERT statement
            insert_sql = '''
                INSERT INTO buybill (id, buy_date, buy_time, importer_bill_no, buy_importer_id, buy_user_id)
                SELECT %s,%s,%s,%s, 
                    (SELECT id FROM importer WHERE importer_name = %s),
                    (SELECT id FROM user WHERE user_fullname = %s)                
            '''        
            # Execute the combined query
            try:
                self.cur.execute(insert_sql, (id, buy_date, buy_time, imp_bil_no, importer_name, user_name))
                
                # Commit the transaction
                self.db.commit()

            except Exception as e:
                # Rollback the transaction if an error occurs
                self.db.rollback()
                print(f"Error: {e}")        

        self.lineEdit_73.setText('')
        self.lineEdit_68.setText('')
        self.lineEdit_69.setText('1')
        self.lineEdit_66.setText('')
        self.lineEdit_70.setText('0')
        self.lineEdit_71.setText('0')
        self.lineEdit_65.setText('0')    
        self.lineEdit_52.setText(str(id))        
        self.lineEdit_72.setText(self.lineEdit_52.text())
        self.pushButton_33.setEnabled(False)
        self.pushButton_34.setEnabled(True)
        self.pushButton_36.setEnabled(True)
        self.pushButton_37.setEnabled(False)
        self.pushButton_39.setEnabled(False)
        self.pushButton_43.setEnabled(False)        
        self.tabWidget_4.setCurrentIndex(1)
    
    def buybill_table_fill(self):
        bill_id = self.lineEdit_52.text()
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.insertRow(0)
        sql = f''' SELECT b.id, b.buy_date, b.buy_time, i.id,
        b.importer_bill_no, u.id, b.buy_total_price,
        b.buy_discount, b.buy_item_count
        FROM buybill b 
        LEFT JOIN importer i ON i.id = b.buy_importer_id
        LEFT JOIN user u ON u.id = b.buy_user_id
        WHERE b.id = {bill_id}
        '''        
        self.cur.execute(sql)
        data = self.cur.fetchall()        
       
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_10.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_10.rowCount()
            self.tableWidget_10.insertRow(row_pos)

    def buybill_return_to(self):
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

    def buybill_save(self):
        buybill_date = self.dateEdit_11.date().toString(QtCore.Qt.ISODate)        
        buybill__time = self.timeEdit_9.time().toString(QtCore.Qt.ISODate)        
        buybill_id = self.lineEdit_52.text()
        importer = self.comboBox_9.currentText()
        user = self.comboBox_11.currentText()
        total = Decimal(self.lineEdit_57.text())
        diccount = Decimal(self.lineEdit_56.text())
        count = Decimal(self.lineEdit_58.text())
    
        self.cur.execute('''
            UPDATE buybill SET buy_total_price=%s, buy_discount=%s, buy_item_count=%s
            WHERE id=%s ''',(total, diccount, count, buybill_id))
                
        self.db.commit()
        self.buybill_table_fill()

        self.lineEdit_52.setText('')
        #self.lineEdit_72.setText('')
        self.lineEdit_73.setText('')
        self.pushButton_31.setEnabled(False)
        self.pushButton_32.setEnabled(True)
        self.pushButton_34.setEnabled(False)
        self.pushButton_36.setEnabled(True)
        self.pushButton_38.setEnabled(True)
        self.pushButton_43.setEnabled(True)       

    def buybill_table_select(self):
        row = self.tableWidget_10.currentItem().row()
        buybill_id = self.tableWidget_10.item(row, 0).text()
        self.lineEdit_72.setText(buybill_id)
        importer_id = int(self.tableWidget_10.item(row, 3).text())        
        user_id = int(self.tableWidget_10.item(row, 5).text())        
        
        # Combined SQL query with JOINs to get user_fullname and grp_name in one query
        sql = f'''
        SELECT b.*, i.importer_name, i.importer_phone, u.user_fullname
        FROM buybill b
        LEFT JOIN importer i ON i.id = '{importer_id}'
        LEFT JOIN user u ON u.id = '{user_id}'
        WHERE b.id = {buybill_id}
        '''        
        self.cur.execute(sql)
        data = self.cur.fetchone()        
        h, m, s = map(int, (str(data[2])).split(":"))
        x = QTime(h, m)
        self.lineEdit_52.setText(str(data[0]))
        self.dateEdit_11.setDate(data[1])
        self.timeEdit_9.setTime(x)        
        self.lineEdit_50.setText(str(data[4]))
        self.lineEdit_57.setText(str(data[6]))
        self.lineEdit_56.setText(str(data[7]))
        self.lineEdit_58.setText(str(data[8]))
        self.comboBox_9.setCurrentText(data[9])
        self.lineEdit_49.setText(str(data[10]))
        self.comboBox_11.setCurrentText(data[11])
        self.pushButton_32.setEnabled(False)
        self.pushButton_35.setEnabled(True)
        self.pushButton_40.setEnabled(True)
        self.buy_item_table_fill()    

 
    def buybill_update(self):
        bb_id = self.lineEdit_52.text()
        date = self.dateEdit_11.date().toString(QtCore.Qt.ISODate)        
        time = self.timeEdit_9.time().toString(QtCore.Qt.ISODate)        
        importer = self.comboBox_9.currentText()
        user = self.comboBox_11.currentText()        

        self.cur.execute('''
            UPDATE buybill SET buy_date=%s, buy_time=%s, 
            buy_importer_id=(SELECT id FROM importer WHERE importer_name=%s), 
            buy_user_id=(SELECT id FROM user WHERE user_fullname=%s)  WHERE id=%s
              ''',(date, time, importer, user, bb_id))
        
        self.db.commit()
        self.buybill_table_fill()        
        QMessageBox.warning(self, 'تعديل بيانات', 'لقد تم تعديل البيانات بنجاح', QMessageBox.Ok )
        self.buybill_return()
        self.lineEdit_56.setText('0')
        self.lineEdit_57.setText('0')
        self.lineEdit_58.setText('0')

    def buybill_search(self):
        self.groupBox_14.show()
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.insertRow(0)        
        sql = "SELECT * FROM buybill"
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

    
    
    def buybill_delete(self):
        del_item = QMessageBox.warning(self, 'حذف بيانات' , 'هل انت متأكد من حذف هذه البيانات', QMessageBox.Yes | QMessageBox.No)
        if del_item == QMessageBox.No :
            return

        id = int(self.lineEdit_52.text())
        self.cur.execute(f"DELETE FROM buybill WHERE id={id}")
        self.db.commit()
        self.buybill_table_fill()
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
        self.buybill_return()

    def buybill_return(self):
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.insertRow(0)        
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

    def buy_unit_total(self):
        qty = Decimal(self.lineEdit_69.text())
        unit_price = Decimal(self.lineEdit_71.text())        
        x = qty * unit_price
        self.lineEdit_67.setText(str(x))
    
    def total_discount(self):
        qty = Decimal(self.lineEdit_69.text())
        unit_dis = Decimal(self.lineEdit_70.text())
        dis = round(qty * unit_dis, 2)
        self.lineEdit_100.setText(str(dis))

    def row_go(self):        
        rows=[]
        '''
        if self.lineEdit_33.text() == '' and self.lineEdit_32.text() == '':
            QMessageBox.warning(self, 'بيانات مفقودة', 'من فضلك أدخل البيانات المطلوبة', QMessageBox.Ok)
            return
        if self.lineEdit_33.text() == '':
            row = self.lineEdit_32.text()            
        else:
            invoice_no = self.lineEdit_33.text()            
            self.cur.execute(f"SELECT id FROM buybill WHERE buy_invoice_no={invoice_no}")
            row = self.cur.fetchone() 
                   
            if row == None:
                QMessageBox.warning(self, 'بيانات مفقودة', 'البيانات التي ادخلتها غير موجودة في قاعدة البيانات', QMessageBox.Ok)
                return
            else:
                row = row[0]
        '''
        if self.lineEdit_32.text() == '':
            QMessageBox.warning(self, 'بيانات مفقودة', 'من فضلك أدخل البيانات المطلوبة', QMessageBox.Ok)
            return
        row = int(self.lineEdit_32.text())
        self.cur.execute("SELECT id FROM buybill ORDER BY id")
        id_s = self.cur.fetchall()        
        for i in range(len(id_s)):
            rows.append(id_s[i][0])            
        if row in rows:
            row_no = rows.index(row) + 1        
            self.tableWidget_10.setCurrentCell(int(row_no)-1, 1)
        else:
            QMessageBox.warning(self, 'بيانات مفقودة', 'البيانات التي ادخلتها غير موجودة في قاعدة البيانات', QMessageBox.Ok)
            return
        # elif invoice_no != '':
        #     self.tableWidget_10.setCurrentCell(int(invoice_no)-1, 4)
        self.lineEdit_32.setText('')        
        self.pushButton_43.setEnabled(True)        
        self.groupBox_14.hide()

    def total_earn(self):
        x = self.lineEdit_67.text()
        y = self.lineEdit_54.text()
        z = self.lineEdit_55.text()
        i = float(y) - float(x) - float(z)
        buy_earn = self.lineEdit_53.setText(str(i))
        buy_earn = self.lineEdit_53.text()


    def total_sale_price(self):
        buy_unit_count = self.lineEdit_69.text()
        item_count_peruint = self.lineEdit_66.text()
        total_buy = self.lineEdit_67.text()
        x = float(total_buy)        
        y = int(buy_unit_count) * int(item_count_peruint) * float(total_buy)
        total_sale = self.lineEdit_54.setText(str(y))
        total_sale = self.lineEdit_54.text()
        #self.lineEdit_57.setText(self.lineEdit_54.text())
        buy_minus = self.lineEdit_55.text()
        z = x + float(buy_minus)
        buy_earn = self.lineEdit_53.setText(str(y-z))
        buy_earn = self.lineEdit_53.text()

    #  -------------------- فواتير المرتجعات -------------
    
    def rebuybill_add_new(self):

        self.cur.execute('''
        SELECT id FROM rebuybill  ORDER BY id ''')
        row = self.cur.fetchall()
        if row == [] :
            self.lineEdit_76.setText('1')
        else:
            self.lineEdit_76.setText(str(row[-1][0] + 1))
            id = int(self.lineEdit_76.text())
            alter_query = f"ALTER TABLE rebuybill AUTO_INCREMENT = {id}"
            self.cur.execute(alter_query)
        self.lineEdit_75.setText('1')        
        self.lineEdit_77.setText('')        
        self.lineEdit_79.setText('')
        self.lineEdit_80.setText('0')
        self.lineEdit_81.setText('0')
        self.pushButton_45.setEnabled(False)
        self.pushButton_47.setEnabled(False)
        self.pushButton_48.setEnabled(False)        

    def rebuybill_save(self):
        rebuybill_id = int(self.lineEdit_76.text()) # رقم طلب مرتجع الشراء      
        buybill_no = int(self.lineEdit_79.text())
        date = self.dateEdit_12.date().toString(QtCore.Qt.ISODate)        
        time = self.timeEdit_10.time().toString(QtCore.Qt.ISODate)        
        user = self.comboBox_14.currentText()
        importer = self.comboBox_10.currentText()       
               
        # Combine the SELECT queries into the INSERT statement
        insert_sql = '''
            INSERT INTO rebuybill (id, rebuy_date, rebuy_time, 
            buybill_id, importer_id, rebuy_user_id)
            SELECT %s, %s, %s,
                (SELECT id FROM buybill WHERE importer_bill_no = %s),                              
                (SELECT id FROM importer WHERE importer_name = %s),
                (SELECT id FROM user WHERE user_fullname = %s)               
        '''        
        # Execute the combined query
        try:
            self.cur.execute(insert_sql, (rebuybill_id, date, time, buybill_no, importer, user))
            # Commit the transaction
            self.db.commit()
            self.rebuy_clear()
            QMessageBox.warning(self, 'إفــادة', 'تم حفظ البيانات بنجاح', QMessageBox.Ok)
            return
        except Exception as e:
            # Rollback the transaction if an error occurs
            self.db.rollback()            
            print(f"Error: {e}")       
        
    def rebuybill_search(self):
        self.tableWidget_12.setRowCount(0)
        self.tableWidget_12.insertRow(0)
        sql = "SELECT * FROM rebuybill"
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
        
        sql = f"SELECT * FROM rebuybill WHERE id = {cell} "
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

    def rebuybill_update(self):

        id = self.lineEdit_76.text()
        sql = "SELECT rebuy_item_count FROM rebuybill WHERE id=%s"        
        self.cur.execute(sql, [(id)])
        data = self.cur.fetchone()
        item_count = data[0]        
        rebuy_date = self.dateEdit_12.date()
        rebuy_date = rebuy_date.toString(QtCore.Qt.ISODate)
        rebuy_time = self.timeEdit_10.time()
        rebuy_time = rebuy_time.toString(QtCore.Qt.ISODate)
        rebuy_item_name = self.comboBox_13.currentText()
        buybill_id = self.lineEdit_77.text()
        detailbill_id = self.lineEdit_78.text()
        import_bill_id = self.lineEdit_79.text()        
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

        self.cur.execute(''' UPDATE rebuybill SET \
         rebuy_date=%s, rebuy_time=%s, \
         buybill_id=%s, detail_bill_id=%s, \
         import_bill_id=%s, rebuy_item_name=%s,\
         rebuy_item_count=%s, unit_price=%s, \
         rebuy_totalG=%s, importer=%s, \
         rebuy_user_id=%s WHERE id=%s ''', (
         rebuy_date, rebuy_time, buybill_id, \
         detailbill_id, import_bill_id, rebuy_item_name,\
         rebuy_item_cnt, unit_price,\
         rebuy_totalG, importer, user_id, id))

        self.db.commit()

    def rebuy_delete(self):
        
        del_item = QMessageBox.warning(self, 'مسح بيانات' , 'هل انت متأكد من حذف هذه البيانات', QMessageBox.Yes | QMessageBox.No)
        if del_item == QMessageBox.No :
            return
        id = self.lineEdit_76.text()
        item_name = self.comboBox_13.currentText()
        sql = "SELECT rebuy_item_count FROM rebuybill WHERE id = %s"
        self.cur.execute(sql, [(id)])
        data = self.cur.fetchone()
        rebuy_item_qty = data[0]

        sql = "SELECT item_qty FROM items WHERE item_name = %s"
        self.cur.execute(sql, [(item_name)])
        data = self.cur.fetchone()
        item_qty = data[0]
        item_qty += rebuy_item_qty
        
        self.cur.execute("UPDATE items SET item_qty=%s WHERE item_name=%s ", (item_qty, item_name))

        sql = ('''DELETE FROM rebuybill WHERE id = %s ''')
        self.cur.execute(sql, [(id)])

        self.db.commit()
        self.rebuybill_search()

    def rebuy_item_info(self):
        resale_no = int(self.lineEdit_78.text()) # رقم طلب مرتجع العميل
        barcode = int(self.lineEdit_77.text())
        item_info = ''' SELECT  sd.resale_item_name,
        sd.unit_price, sd.resale_item_qty, sd.resale_reason,
        i.item_importer_id, i.item_buybill_id, im.importer_name, 
        im.importer_grp_id, im.importer_company_id, b.buy_date,
        b.importer_bill_no, g.grp_name, c.company_name
        FROM resalebill_details sd        
        LEFT JOIN item i ON i.item_barcode = %s
        LEFT JOIN importer im ON im.id = i.item_importer_id
        LEFT JOIN grp g ON g.id = im.importer_grp_id
        LEFT JOIN buybill b ON b.id = i.item_buybill_id AND b.buy_importer_id = i.item_importer_id
        LEFT JOIN company c ON c.id = im.importer_company_id
        WHERE sd.resalebill_id = %s AND sd.resale_item_id = i.id
        '''
        self.cur.execute(item_info, (barcode, resale_no))
        data = self.cur.fetchone()
        
        total = round(data[1] * data[2], 2)
        self.lineEdit_79.setText(str(data[10]))
        self.lineEdit_89.setText(str(data[11]))
        self.lineEdit_90.setText(str(data[12]))
        self.comboBox_10.setCurrentText(str(data[6]))
        self.dateEdit_17.setDate(data[9])
        self.comboBox_13.setCurrentText(str(data[0]))
        self.lineEdit_75.setText(str(data[2]))
        self.lineEdit_80.setText(str(data[1]))
        self.lineEdit_108.setText(data[3])
        self.lineEdit_81.setText(str(total))
        

    def rebuybill_save_but(self):
        
        self.pushButton_45.setEnabled(True)

    def rebuy_clear(self):
        self.lineEdit_75.setText('1')
        self.lineEdit_76.setText('')
        self.lineEdit_77.setText('')
        self.lineEdit_78.setText('')
        self.lineEdit_79.setText('')
        self.lineEdit_80.setText('0')
        self.lineEdit_81.setText('0')
        self.lineEdit_89.setText('')
        self.lineEdit_90.setText('')
        self.lineEdit_108.setText('')
        self.pushButton_44.setEnabled(True)
        self.pushButton_45.setEnabled(False)
        self.pushButton_46.setEnabled(True)
        self.pushButton_47.setEnabled(False)
        self.pushButton_48.setEnabled(False)

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
        self.salebill_save()
        self.salebill_add_new()

            
    def cash_rset(self):
        self.lineEdit_82.setText((str(Decimal(self.lineEdit_64.text())-(Decimal(self.lineEdit_62.text())))))        
        x = Decimal(self.lineEdit_82.text())
        

    def cash(self):
        self.salebill_save()
        self.salebill_add_new()

    def item_qty_x_sale_price(self):
        item_price = Decimal(self.lineEdit_85.text())        
        item_qty = Decimal(self.lineEdit_83.text())
        x = item_qty * item_price
        self.lineEdit_84.setText(str(x))        
        self.sale_item_add()

    def get_sale_item_info(self):
        bar_code = self.lineEdit_86.text()
        sql = f"SELECT item_name, item_public_price, item_unit, item_discount FROM item WHERE item_barcode={bar_code}"
        self.cur.execute(sql)
        data = self.cur.fetchone()        
        if data == None :
            QMessageBox.warning(self, 'بيانات خاطئة', 'هذا الصنف غير موجود', QMessageBox.Ok)
            self.lineEdit_86.setText('')
            return

        qty = Decimal(self.lineEdit_83.text())
        discount = data[3] * qty
        discount = f"{discount:.2f}"
        self.comboBox_16.setCurrentText(data[0])
        self.lineEdit_85.setText(str(data[1]))
        self.lineEdit_88.setText(data[2])
        self.lineEdit_99.setText(str(discount))
        unit = self.lineEdit_88.text()
        wight_chk = bar_code[:2]        
        if unit == 'كيلو جرام' and wight_chk == '20':
            wight = int(bar_code[5:8])            
            wight = Decimal(wight/1000)
            wight = f"{wight:.3f}"            
            self.lineEdit_83.setText(str(wight))

        self.item_qty_x_sale_price()

    def sale_item_select(self):
        invo_no = int(self.lineEdit_59.text())
        row = self.tableWidget_13.currentItem().row()
        it_code = self.tableWidget_13.item(row, 1).text()              
        sql = f"SELECT s.*, i.item_unit \
            FROM salebill_details s \
            JOIN item i ON i.item_barcode = {it_code} \
            WHERE s.item_barcode={it_code} AND s.bill_id={invo_no}"
        self.cur.execute(sql)
        data = self.cur.fetchone()        
        self.lineEdit_86.setText(str(data[2]))
        self.comboBox_16.setCurrentText(data[3])
        self.lineEdit_85.setText(str(data[4]))
        self.lineEdit_99.setText(str(data[7]))
        self.lineEdit_83.setText(str(data[5]))
        self.lineEdit_84.setText(str(data[8]))
        self.lineEdit_88.setText(data[9])
        self.pushButton_49.setEnabled(True)
        self.pushButton_50.setEnabled(True)


    def sale_item_delete(self):
        invo_no = int(self.lineEdit_59.text())
        it_code = int(self.lineEdit_86.text())
        discount = Decimal(self.lineEdit_99.text())
        qty = Decimal(self.lineEdit_83.text())
        total = Decimal(self.lineEdit_84.text())
        sale_update = ''' UPDATE salebill s
            JOIN salebill_details sd ON sd.item_barcode=%s AND bill_id=%s
            JOIN item i ON i.item_barcode=%s
            SET
            s.bill_total=s.bill_total - sd.item_price, 
            s.discount=s.discount - sd.item_discount, 
            s.wanted=s.wanted - sd.total_price,
            s.item_count=s.item_count - sd.item_count,
            i.item_qty=i.item_qty + %s
             '''
        params = (it_code, invo_no, it_code, qty)
        self.cur.execute(sale_update, params)

        sql = ('''DELETE FROM salebill_details WHERE item_barcode=%s AND bill_id=%s''')
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
        qty = Decimal(self.lineEdit_83.text())
        total = Decimal(self.lineEdit_84.text())
        discount = Decimal(self.lineEdit_99.text())
        unit = self.lineEdit_88.text()
        if unit == 'كيلو جرام':
            count = 1
        else: 
            count = qty
        sql = "SELECT item_barcode FROM salebill_details WHERE bill_id=%s AND item_barcode=%s"
        self.cur.execute(sql, (id, it_code))
        data = self.cur.fetchone()
        
        if not data or unit=='كيلو جرام':            
            self.lineEdit_62.setText(str(Decimal(self.lineEdit_61.text())-(Decimal(self.lineEdit_63.text()))))
            self.cur.execute("INSERT INTO salebill_details \
                (bill_id, item_barcode, item_name, item_price,\
                item_qty, item_count, item_discount, total_price) \
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",\
                (id, code, name, price, qty, count, discount, total))
        else:            
            self.cur.execute(f"UPDATE salebill_details SET item_count=item_count+{count}, \
                item_qty=item_count, total_price=item_price * item_qty \
                WHERE item_barcode={it_code}")
        
        self.cur.execute(f"UPDATE item SET item_qty=item_qty-{qty} \
            WHERE item_barcode={it_code}")
        self.db.commit()
        self.hide_keypad()
        self.lineEdit_83.setText('1')
        self.salebill_details_table_fill()
        self.salebill_save()
        self.clear_fields()
        

    def salebill_add_new(self):
        date = self.dateEdit_13.date().toString(Qt.ISODate)
        time = self.timeEdit_11.time().toString(Qt.ISODate)
        cus_name = self.comboBox_24.currentText()
        user_name = self.comboBox_15.currentText()
        count = 0    
        
        self.cur.execute("SELECT id, cash, visa FROM salebill WHERE id=(SELECT max(id) FROM salebill)")
        data = self.cur.fetchone()        
        if data and data[1] == 0 and data[2] == 0:
            id = data[0]
        else:
            if not data:
                id = 1
            else:
                if data[1] != 0 or data[2] !=0 :
                    id = data[0] + 1
        
            insert_sql = ''' INSERT INTO salebill (id, date, time, item_count, customer_id, user_id)
                SELECT %s, %s, %s, %s,
                (SELECT id FROM customer WHERE customer_name=%s),
                (SELECT id FROM user WHERE user_fullname=%s) '''
            self.cur.execute(insert_sql, (id, date, time, count, cus_name, user_name))
            self.db.commit()
        
        #self.timeEdit_11.setTime(QTime.currentTime())
        self.lineEdit_59.setText(str(id))        
        self.lineEdit_61.setText('0')
        self.lineEdit_62.setText('0')
        self.lineEdit_63.setText('0')        
        self.lineEdit_64.setText('0')
        self.lineEdit_74.setText('0')
        self.lineEdit_82.setText('0')
        self.lineEdit_83.setText('1')
        self.lineEdit_84.setText('')
        self.lineEdit_85.setText('1')
        self.lineEdit_86.setText('')
        self.lineEdit_87.setText('0')
        self.lineEdit_88.setText('')
        self.lineEdit_99.setText('0')
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
        self.lineEdit_86.setFocus(QtCore.Qt.MouseFocusReason)        
        self.lineEdit_86.setCursorPosition(0)

    def salebill_save(self):
        if self.lineEdit_59.text() == '' :
            QMessageBox.warning(self, 'بيانات ناقصة', 'من فضلك اضغط فاتورة جديدة', QMessageBox.Ok)
            return
        
        sale_time = self.timeEdit_11.time().toString(QtCore.Qt.ISODate)        
        sale_date = self.dateEdit_13.date().toString(QtCore.Qt.ISODate)
        user = self.comboBox_15.currentText()              
        customer = self.comboBox_24.currentText()
        id = int(self.lineEdit_59.text())
        total = self.lineEdit_61.text()
        dis = self.lineEdit_63.text()
        wanted = self.lineEdit_62.text()
        cash = self.lineEdit_64.text()
        cash_rtn = self.lineEdit_82.text()
        net_cash = Decimal(cash) - Decimal(cash_rtn)        
        visa = self.lineEdit_87.text()        
        count = int(self.lineEdit_74.text())
        
        self.cur.execute('''
        UPDATE salebill SET date=%s, time=%s, bill_total=%s, discount=%s, wanted=%s,
        cash=%s, cash_return=%s, visa=%s, item_count=%s,
        user_id=(SELECT id FROM user WHERE user_fullname=%s),
        customer_id=(SELECT id FROM customer WHERE customer_name=%s)
        WHERE id=%s''', (sale_date, sale_time, total, dis, wanted, cash, cash_rtn, visa, count, user, customer, id))
        
        
        self.db.commit()
        self.pushButton_52.setEnabled(True)
        


    def sale_item_update(self):
        invo_no = int(self.lineEdit_59.text())
        row = self.tableWidget_13.currentItem().row()
        it_code = self.tableWidget_13.item(row, 0).text()              
        sql = f"SELECT * FROM salebill_details WHERE item_code={it_code} AND salebill_id={invo_no}"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        old_qty = float(data[6])
        new_qty = float(self.lineEdit_83.text())
        dif_qty = old_qty - new_qty
        sql = f"UPDATE salebill_details SET item_count={new_qty}, item_total_price=item_price*{new_qty} WHERE salebill_id={invo_no} AND item_code={it_code}"
        self.cur.execute(sql)

        sql = f"UPDATE items SET item_qty=item_qty+{dif_qty} WHERE item_barcode={it_code}"
        self.cur.execute(sql)
        self.db.commit()
        self.salebill_details_table_fill()
        self.pushButton_49.setEnabled(False)
        self.pushButton_50.setEnabled(False)

    def salebill_details_table_fill(self):        
        
        sb_id = int(self.lineEdit_59.text())
        self.tableWidget_13.setRowCount(0)
        self.tableWidget_13.insertRow(0)
        
        sql = f''' SELECT s.item_name, s.item_barcode, i.item_unit,
        s.item_price, s.item_qty, s.item_discount, s.total_price
        FROM salebill_details s 
        LEFT JOIN item i ON s.item_barcode = i.item_barcode
        WHERE s.bill_id = {sb_id}        '''
        self.cur.execute(sql)
        data = self.cur.fetchall()        
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_13.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_13.rowCount()
            self.tableWidget_13.insertRow(row_pos)
        
        sql = f''' SELECT SUM(item_price), SUM(item_qty), SUM(item_count),
        SUM(item_discount), SUM(total_price) FROM salebill_details 
        WHERE bill_id = {sb_id}
        '''
        self.cur.execute(sql)
        data = self.cur.fetchone()        
        self.lineEdit_61.setText(str(data[4]))
        self.lineEdit_63.setText(str(data[3]))
        wanted = Decimal(self.lineEdit_61.text()) - Decimal(self.lineEdit_63.text())
        self.lineEdit_62.setText(str(wanted))
        self.lineEdit_74.setText(str(data[2]))

    def resalebill_add_new(self):
        self.cur.execute('''
        SELECT id FROM resalebill  ORDER BY id ''')
        row = self.cur.fetchall()
        if row == [] :
            self.lineEdit_107.setText('1')
        else:
            self.lineEdit_107.setText(str(row[-1][0] + 1))
            id = int(self.lineEdit_107.text())
            alter_query = f"ALTER TABLE resalebill AUTO_INCREMENT = {id}"
            self.cur.execute(alter_query)
        
        self.resalebill_clear()

    def resalebill_save(self):        
        resalebill_id = self.lineEdit_107.text()
        salebill_id = self.lineEdit_102.text()
        resalebill_date = self.dateEdit_19.date().toString(Qt.ISODate)        
        resalebill_time = self.timeEdit_14.time().toString(Qt.ISODate)        
        resalebill_user = self.comboBox_26.currentText()
        # Combine the SELECT queries into the INSERT statement
        insert_sql = '''
            INSERT INTO resalebill (id, resale_date, resale_time, salebill_id, resale_user_id)
            SELECT %s, %s, %s, %s,
                (SELECT id FROM user WHERE user_fullname = %s)                
        '''        
        # Execute the combined query
        try:
            self.cur.execute(insert_sql, (resalebill_id, resalebill_date, resalebill_time, salebill_id, resalebill_user))            
            # Commit the transaction
            self.db.commit()
        except Exception as e:
            # Rollback the transaction if an error occurs
            self.db.rollback()
            print(f"Error: {e}")
            # Optionally, you could show an error message to the user
                
        #self.resalebill_field_clear()
        self.resalebill_details_save()

    def resalebill_details_save(self):
        item_barcode = self.lineEdit_101.text()
        salebill_id = int(self.lineEdit_102.text())
        resalebill_id = int(self.lineEdit_107.text())
        qty = Decimal(self.lineEdit_103.text())
        reason = self.lineEdit_106.text()
        item_info = '''SELECT sd.item_name, 
        (sd.item_price - sd.item_discount) AS price,
        s.date, s.time
        FROM salebill_details sd 
        LEFT JOIN salebill s ON s.id=%s
        WHERE sd.bill_id=%s AND sd.item_barcode=%s'''

        self.cur.execute(item_info, (salebill_id, salebill_id, item_barcode))
        it_info = self.cur.fetchone()
        if it_info == None :
            QMessageBox.warning(self, 'بيانات خاطئة', 'هناك خطأ إما الباركود أو رقم فاتورة البيع', QMessageBox.Ok)
            return
        self.comboBox_25.setCurrentText(it_info[0])
        self.lineEdit_104.setText(str(it_info[1]))
        total = qty * it_info[1]
        self.lineEdit_105.setText(str(total))
        self.dateEdit_18.setDate(it_info[2])
        # Convert timedelta to hours, minutes, and seconds
        hours, remainder = divmod(it_info[3].total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        # Set the time in QTimeEdit
        self.timeEdit_13.setTime(QTime(int(hours), int(minutes), int(seconds))) 

        sql = '''UPDATE resalebill SET resale_total_price=%s 
        WHERE id=%s AND salebill_id =%s'''
        self.cur.execute(sql, (total,resalebill_id, salebill_id))

        sql='''INSERT INTO resalebill_details (resalebill_id, 
        resale_item_name, resale_item_qty,
        unit_price, resale_reason, resale_item_id) 
        SELECT %s, %s, %s, %s, %s, 
        (SELECT id FROM item WHERE item_barcode = %s)
        '''
        self.cur.execute(sql,(resalebill_id, it_info[0], qty, total, reason, item_barcode))
        self.db.commit()
        self.resalebill_table_fill()
        self.resalebill_clear()

    def resalebill_table_fill(self):        
        sql = '''SELECT resalebill_id, resale_item_id,
        resale_item_name, unit_price, resale_item_qty, 
        ROUND(unit_price * resale_item_qty, 2) AS total,
        resale_reason
        FROM resalebill_details '''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        self.tableWidget_17.setRowCount(0)
        self.tableWidget_17.insertRow(0)
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_17.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_pos = self.tableWidget_17.rowCount()
            self.tableWidget_17.insertRow(row_pos)

    def resalebill_clear(self):
        #self.lineEdit_107.setText('')
        self.lineEdit_101.setText('')
        self.lineEdit_102.setText('')
        self.lineEdit_104.setText('')
        self.lineEdit_105.setText('')
        self.lineEdit_106.setText('')
        self.pushButton_67.setEnabled(True)
        self.pushButton_68.setEnabled(False)
        self.pushButton_69.setEnabled(False)
        self.pushButton_70.setEnabled(False)
        self.pushButton_71.setEnabled(False)
    
    def resalebill_table_select(self):        
        row = self.tableWidget_17.currentItem().row()
        rs_id = self.tableWidget_17.item(row, 0).text()
        item_id = self.tableWidget_17.item(row, 1).text()
        query = '''SELECT rd.*, i.item_barcode, 
            ROUND(rd.unit_price * rd.resale_item_qty, 2) AS total,
            r.resale_date, r.resale_time, r.id
            FROM resalebill_details rd
            LEFT JOIN item i ON i.id = %s
            LEFT JOIN resalebill r ON r.id = %s
            WHERE rd.resalebill_id = %s AND rd.resale_item_id = %s
            '''
        self.cur.execute(query, (item_id, rs_id, rs_id, item_id))
        data = self.cur.fetchone()        
        self.lineEdit_101.setText(str(data[7]))
        self.lineEdit_102.setText(str(data[1]))
        self.lineEdit_103.setText(str(data[4]))
        self.lineEdit_104.setText(str(data[5]))
        self.lineEdit_105.setText(str(data[8]))          
        self.lineEdit_106.setText(str(data[6]))
        self.lineEdit_107.setText(str(data[11]))
        self.comboBox_25.setCurrentText(data[3])
        self.dateEdit_18.setDate(data[9])
        hours, remainder = divmod(data[10].total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        # Set the time in QTimeEdit
        self.timeEdit_13.setTime(QTime(int(hours), int(minutes), int(seconds)))         
        self.pushButton_67.setEnabled(True)
        self.pushButton_68.setEnabled(False)        
        self.pushButton_70.setEnabled(True)
        self.pushButton_71.setEnabled(True)

    def resalebill_update(self):
        barcode = int(self.lineEdit_101.text())       
        salebill_id = int(self.lineEdit_102.text())
        order_no = int(self.lineEdit_107.text())
        qty = Decimal(self.lineEdit_103.text())
        it_name = self.comboBox_25.currentText()
        price = Decimal(self.lineEdit_104.text())
        reason = self.lineEdit_106.text()
        user = self.comboBox_26.currentText()
        resale_query = '''UPDATE resalebill_details rd
        JOIN resalebill r ON r.id = %s
        SET rd.resale_item_id = (SELECT i.id FROM item i WHERE i.item_barcode = %s),
            rd.resale_item_name = %s,
            rd.resale_item_qty = %s,
            rd.unit_price = %s,
            rd.resale_reason = %s,
            r.resale_total_price = %s,
            r.resale_user_id = (SELECT u.id FROM user u WHERE u.user_fullname = %s)
        WHERE rd.resalebill_id = %s AND rd.resale_item_name = %s
        '''
        params = (order_no, barcode, it_name, qty, price, reason, price, user, order_no, it_name)
        try:        
            
            self.cur.execute(resale_query, params)
            self.db.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            self.db.rollback()
            # print(f"Error: {e}")  # Optionally log or show the error to the user 
            QMessageBox.warning(self, 'رسالة تحذير', 'لايمكن حذف هذا السجل نظرا للاعتماد عليه في بعض سجلات قاعدة البيانات', QMessageBox.Ok)
            return
        self.db.commit()        
        self.resalebill_table_fill()        

    def resalebill_delete(self):
        order_no = int(self.lineEdit_107.text())
        try:        
            sql = ('''DELETE FROM resalebill WHERE id = %s ''')
            self.cur.execute(sql, [(order_no)])
            self.db.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            self.db.rollback()
            # print(f"Error: {e}")  # Optionally log or show the error to the user 
            QMessageBox.warning(self, 'رسالة تحذير', 'لايمكن حذف هذا السجل نظرا للاعتماد عليه في بعض سجلات قاعدة البيانات', QMessageBox.Ok)
            return
        self.resalebill_table_fill()
        self.resalebill_clear()
# =============== تقارير ===============
    def cashier_daily_tally(self):

        casher = self.comboBox_20.currentText()
        date = self.dateEdit_14.date().toString(QtCore.Qt.ISODate)
        
        
        sql = ''' SELECT u.user_fullname, s.date, SUM(s.cash),
            SUM(s.visa) FROM salebill s
            JOIN user u ON u.user_fullname = %s
            WHERE s.date = %s AND s.user_id = u.id '''
        self.cur.execute(sql, [(casher), (date)])
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

        query = '''
        SELECT s.item_name,
            s.item_barcode,
            SUM(s.item_qty) AS qty,
            SUM(s.total_price) AS total,
            SUM(s.item_discount) AS discount,
            (SUM(s.total_price) - SUM(s.item_discount)) AS net,
            ROUND((SUM(s.item_qty) * i.item_price), 2) AS net_buy, 
            ((SUM(s.total_price) - SUM(s.item_discount))-ROUND((SUM(s.item_qty) * i.item_price), 2)) AS profits
        FROM salebill_details s
        JOIN item i ON s.item_barcode = i.item_barcode
        GROUP BY s.item_barcode
        ORDER BY qty DESC
        '''
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
        date = self.dateEdit_15.date().toString(QtCore.Qt.ISODate)        
        query = ''' SELECT SUM(cash), SUM(visa) FROM salebill WHERE date=%s '''
        self.cur.execute(query, [(date)])
        data = self.cur.fetchone()        
        self.lineEdit_91.setText(str(data[0]))
        self.lineEdit_92.setText(str(data[1]))

    def sales_range_report(self):

        date1 = self.dateEdit_15.date().toString(QtCore.Qt.ISODate)        
        date2 = self.dateEdit_16.date().toString(QtCore.Qt.ISODate)        
        query = ''' SELECT SUM(cash), SUM(visa) FROM salebill WHERE date BETWEEN %s AND %s '''
        self.cur.execute(query, [(date1), (date2)])
        data = self.cur.fetchone()        
        self.lineEdit_93.setText(str(data[0]))
        self.lineEdit_94.setText(str(data[1]))
    
    def buy_range_report(self):
        date1 = self.dateEdit_15.date().toString(QtCore.Qt.ISODate)        
        date2 = self.dateEdit_16.date().toString(QtCore.Qt.ISODate)       
        query = ''' SELECT SUM(buy_total_price), SUM(buy_discount) FROM buybill WHERE buy_date BETWEEN %s AND %s '''
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

        salebill_id = self.lineEdit_59.text()
        query = '''SELECT item_name, 
           item_qty, item_price, 
           total_price 
           FROM salebill_details 
           WHERE bill_id = %s'''
        self.cur.execute(query, [(salebill_id)])
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
    ##app = QApplication(sys.argv)  
    #app = QtWidgets.QApplication([])
    app = QtWidgets.QApplication(sys.argv)
    #Window = QtWidgets.QWidget()  
    Window = Main()
    Window.show()
    app.exec_()
if __name__ == '__main__':
    main()
