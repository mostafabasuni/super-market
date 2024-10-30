from peewee import *

db = MySQLDatabase('market', user='root', password=str(""),
                   host='localhost', port=3306)

class Users(Model):
    un_id = BigIntegerField(null=False)
    user_fullname = CharField(unique=True)
    user_gender = CharField()
    user_phone = CharField()
    user_address = CharField()
    user_job = CharField()
    user_name = CharField(null=True)
    user_password = CharField(null=True)
    user_date = DateField()
    is_user = BooleanField()

    class Meta:
        database = db

class Customers(Model):    
    customer_name = CharField()
    customer_gender = CharField()
    customer_phone = CharField()
    customer_address = CharField()
    customer_type = CharField()
    customer_balance = DecimalField(max_digits=10, decimal_places=2)
    customer_date = DateField()
    customer_time = TimeField()

    class Meta:
        database = db

class Importers(Model):
    importer_name = CharField()  
    importer_phone = CharField()
    importer_address = CharField()
    importer_type = CharField()
    importer_balance = DecimalField(max_digits=10, decimal_places=2)
    importer_date = DateField()
    importer_time = TimeField()    

    class Meta:
        database = db

class Companies(Model):   
    company_name = CharField(unique=True, null=False)
    company_date = DateField(null=False)
    company_time = TimeField(null=False)
    company_user = CharField(null=False)

    class Meta:
        database = db

class Places(Model):
    place_name = CharField(unique=True, null=False)
    place_date = DateField(null=False)
    place_time = TimeField(null=False)
    place_user = CharField(null=False)

    class Meta:
        database = db


class Grps(Model):   
    grp_name = CharField(unique=True, null=False)
    grp_date = DateField(null=False)
    grp_time = TimeField(null=False)
    grp_user = CharField(null=False)

    class Meta:
        database = db

class Items(Model):
    item_barcode = CharField(null=False)
    item_name = CharField(null=False)
    item_group = CharField(max_length = 45)
    item_company = CharField(max_length = 100)
    item_place = CharField(max_length = 45)
    item_price = DecimalField(max_digits=10, decimal_places=2)
    item_qty = IntegerField()
    item_unit = CharField(max_length = 100)
    item_date = DateField()

    class Meta:
        database = db

class Buypill(Model):
    buy_date = DateField()
    buy_time = TimeField()
    buy_invoice_no = IntegerField()    
    buy_importer_id = IntegerField(null=False)
    buy_cash = BooleanField()
    buy_postpone = BooleanField()
    buy_user_id = IntegerField(null=False)
    buy_totalG = DecimalField(max_digits=10, decimal_places=2, null=False)
    buy_totalB = DecimalField(max_digits=10, decimal_places=2, null=False)
    buy_minus = DecimalField(max_digits=10, decimal_places=2, null=False)
    class Meta:
        database = db

class Salepill(Model):    
    date = DateField(null=False)
    time = TimeField(null=False)
    customer = CharField()
    invoice_total = CharField()     
    discount = DecimalField(max_digits=10, decimal_places=2)  
    wanted = DecimalField(max_digits=10, decimal_places=2)
    cash = DecimalField(max_digits=10, decimal_places=2, null=False)
    cash_return = DecimalField(max_digits=10, decimal_places=2, null=False)
    visa = DecimalField(max_digits=10, decimal_places=2)
    rest_cash = DecimalField(max_digits=10, decimal_places=2, null=False)
    user = CharField()
    class Meta:
        database = db


class Rebuypill(Model):    
    rebuy_date = DateField()
    rebuy_time = TimeField()
    buypill_id = IntegerField()
    detail_pill_id = IntegerField()
    import_pill_id = IntegerField()
    rebuy_item_name = CharField()
    rebuy_item_count = IntegerField()
    unit_price = DecimalField(max_digits=10, decimal_places=2)
    rebuy_totalG = DecimalField(max_digits=10, decimal_places=2)
    importer = CharField()
    rebuy_user_id = IntegerField()
    class Meta:
        database = db

class Resalepill(Model):
    resale_date = DateField()
    resale_time = TimeField()
    resale_user = CharField()
    resale_totalG = DecimalField(max_digits=10, decimal_places=2)
    resale_item_count = IntegerField()
    class Meta:
        database = db

class Operations(Model):
    buy_id = IntegerField(null=True)
    sale_id = IntegerField(null=True)
    rebuy_id = IntegerField(null=True)
    employee_id = IntegerField(null=True)
    oper_item = CharField()
    oper_item_exp = DateField(null=True)    
    buy_qty = IntegerField(null=True)
    buy_extra_exp = DecimalField(max_digits=10, decimal_places=2)    
    buy_discount = DecimalField(null=True, max_digits=10, decimal_places=2)    
    buy_unit_price = DecimalField(null=True, max_digits=10, decimal_places=2)
    sale_qty = IntegerField(null=True)
    sale_cash = DecimalField()    
    sale_discount = DecimalField(null=True, max_digits=10, decimal_places=2)    
    sale_unit_price = DecimalField(null=True, max_digits=10, decimal_places=2)
    sale_qty = IntegerField()
    sale_visa = DecimalField(max_digits=10, decimal_places=2)
    sale_notes = CharField()
    rebuy_qty = IntegerField(null=True)
    rebuy_totalG = DecimalField(null=True, max_digits=10, decimal_places=2)
    rebuy_notes = CharField(null=True)
    shift_no = IntegerField()    
    resale_totalG = DecimalField(null=True, max_digits=10, decimal_places=2)
    casher_name = CharField()
    resale_notes = CharField(null=True)
    oper_date = DateField()
    oper_time = TimeField()
    oper_user = CharField(null=True)
    class Meta:
        database = db


class Hodoor_Ensraf(Model):    
    he_date = DateField()
    he_time = TimeField()
    he_employee = IntegerField()
    he_come = TimeField(null=True)
    he_go = TimeField(null=True)
    he_difference = TimeField(null=True)
    he_note = CharField(null=True)
    he_user = CharField(null=True)

    class Meta:
        database = db

db.connect()
db.create_tables([Users, Customers, \
    Importers, Items, Companies, \
    Places, Grps, Buypill, \
    Salepill, Rebuypill, Resalepill, \
    Operations, Hodoor_Ensraf])

