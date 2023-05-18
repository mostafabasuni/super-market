from peewee import *

db = MySQLDatabase('market', user='root', password=str(1234),
                   host='localhost', port=3306)

class Users(Model):
    un_id = BigIntegerField()
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
    customer_balance = DecimalField()
    customer_date = DateField()
    customer_time = TimeField()

    class Meta:
        database = db

class Importers(Model):
    importer_name = CharField()  
    importer_phone = CharField()
    importer_address = CharField()
    importer_type = CharField()
    importer_balance = DecimalField()
    importer_date = DateField()
    importer_time = TimeField()    

    class Meta:
        database = db

class Companies(Model):   
    company_name = CharField(unique=True)
    company_date = DateField()
    company_time = TimeField()
    company_user = CharField()

    class Meta:
        database = db

class Places(Model):
    place_name = CharField(unique=True)
    place_date = DateField()
    place_time = TimeField()
    place_user = CharField()

    class Meta:
        database = db


class Grps(Model):   
    grp_name = CharField(unique=True)
    grp_date = DateField()
    grp_time = TimeField()
    grp_user = CharField()

    class Meta:
        database = db

class Items(Model):
    item_barcode = CharField()
    item_name = CharField()
    item_group = ForeignKeyField(Grps, backref='item_group', null=True)    
    item_company = ForeignKeyField(Companies, backref='item_company', null=True)    
    item_place = ForeignKeyField(Places, backref='item_place', null=True)    
    item_price = DecimalField()
    item_qty = IntegerField()
    item_limit = CharField()    
    item_discount = DecimalField()
    item_earn = DecimalField()
    item_date = DateField()

    class Meta:
        database = db

class Buypill(Model):
    buy_date = DateField()
    buy_time = TimeField()
    buy_invoice_no = CharField()
    buy_unit = CharField(null=True)
    buy_importer = ForeignKeyField(Importers, backref='buy_importer')
    buy_cash = BooleanField()
    buy_postpone = BooleanField()
    buy_user = ForeignKeyField(Users, backref='buy_user')
    buy_totalG = DecimalField()
    buy_totalB = DecimalField()
    buy_item_count = IntegerField()
    buy_earn = DecimalField()
    buy_earn_percent = DecimalField()
    buy_add = DecimalField()
    buy_minus = DecimalField()
    item_id = IntegerField()

    class Meta:
        database = db

class Salepill(Model):    
    sale_date = DateField()
    sale_time = TimeField()
    sale_customer = CharField()
    sale_cash = BooleanField()
    sale_postpone = BooleanField()
    sale_visa = BooleanField()
    sale_delivery = BooleanField()
    sale_user = ForeignKeyField(Users, backref='sale_user')
    sale_totalG = DecimalField()
    sale_totalS = DecimalField()
    sale_item_count = IntegerField()
    sale_earn = DecimalField()
    sale_earn_percent =DecimalField()
    sale_add = DecimalField()
    sale_minus = DecimalField()    

    class Meta:
        database = db


class Rebuypill(Model):    
    rebuy_date = DateField()
    rebuy_time = TimeField()
    rebuy_user = ForeignKeyField(Users, backref='rebuy_user')
    rebuy_totalG = DecimalField()
    rebuy_item_count = IntegerField()

    class Meta:
        database = db

class Resalepill(Model):
    resale_date = DateField()
    resale_time = TimeField()
    resale_user = CharField()
    resale_totalG = DecimalField()
    resale_item_count = IntegerField()

    class Meta:
        database = db

class Operations(Model):
    buy_id = IntegerField(null=True)
    sale_id = IntegerField(null=True)
    rebuy_id = IntegerField(null=True)
    resale_id = IntegerField(null=True)
    oper_item = CharField()
    oper_item_exp = DateField(null=True)
    buy_qty = IntegerField(null=True)
    buy_totalG = DecimalField(null=True)
    buy_discount = DecimalField(null=True)
    buy_unit_price = DecimalField(null=True)
    buy_totalB = DecimalField(null=True)
    buy_earn = DecimalField(null=True)
    buy_notes = CharField(null=True)
    sale_qty = IntegerField(null=True)
    sale_totalG = DecimalField(null=True)
    sale_discount = DecimalField(null=True)
    sale_unit_price = DecimalField(null=True)
    sale_totalB = DecimalField(null=True)
    sale_notes = CharField(null=True)
    rebuy_qty = IntegerField(null=True)
    rebuy_totalG = DecimalField(null=True)
    rebuy_notes = CharField(null=True)
    resale_qty = IntegerField(null=True)
    resale_totalG = DecimalField(null=True)
    resale_notes = CharField(null=True)
    oper_date = DateField()
    oper_time = TimeField()
    oper_user = CharField(null=True)    

    class Meta:
        database = db


class Hodoor_Ensraf(Model):    
    he_date = DateField()
    he_time = TimeField()
    he_employee = ForeignKeyField(Users, backref='he_employee')
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

