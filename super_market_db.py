from peewee import *

db = MySQLDatabase('market', user='root', password=str(""),
                   host='localhost', port=3306)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
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

class Customer(BaseModel):    
    customer_name = CharField()    
    customer_phone = CharField()
    customer_address = CharField()
    

class Importer(BaseModel):
    importer_name = CharField()  
    importer_phone = CharField()
    importer_address = CharField()
    importer_type = CharField()
    importer_balance = DecimalField(max_digits=10, decimal_places=2)
    importer_date = DateField()
    importer_time = TimeField()    

class Grp(BaseModel):   
    grp_name = CharField(unique=True, null=False)
    grp_date = DateField(null=False)
    grp_time = TimeField(null=False)
    grp_user = ForeignKeyField(User, backref='grps', null=False)

class Company(BaseModel):   
    company_name = CharField(unique=True, null=False)
    company_date = DateField(null=False)
    company_time = TimeField(null=False)
    company_user = ForeignKeyField(User, backref='companies', null=False)
    company_grp = ForeignKeyField(Grp, backref='companies', Update='CASCADE', Delete='CASCADE')

class Buybill(BaseModel):
    buy_date = DateField()
    buy_time = TimeField() 
    buy_item = CharField(unique=True, null=False) # اسم المنتج
    buy_item_qty = DecimalField(max_digits=10, decimal_places=2, null=False)
    buy_importer = ForeignKeyField(Importer, backref='buybills', null=False) # اسم المورد    
    buy_user = ForeignKeyField(User, null=False)
    buy_total_price = DecimalField(max_digits=10, decimal_places=2, null=False)
    buy_discount = DecimalField(max_digits=10, decimal_places=2, null=False)

class Item(BaseModel):
    item_buybill_id = ForeignKeyField(Buybill) # رقم فاتورة المورد
    item_barcode = BigIntegerField(null=False)
    item_name = CharField(null=False)
    item_group = ForeignKeyField(Grp, backref='items', on_update='CASCADE', on_delete='CASCADE')
    item_company = ForeignKeyField(Company, backref='items', on_update='CASCADE', on_delete='CASCADE')    
    item_price = DecimalField(max_digits=10, decimal_places=2) # سعر شراء المنتج
    item_public_price = DecimalField(max_digits=10, decimal_places=2) # سعر البيع للجمهور
    item_discount = DecimalField(max_digits=6, decimal_places=2)
    item_qty = IntegerField()
    item_unit = CharField(max_length = 50)

class Buybill_details(BaseModel):
    date = DateField()
    time = TimeField()
    customer = ForeignKeyField(Customer, backref='buybills')    
    item_id = ForeignKeyField(Item)
    item_price = DecimalField(max_digits=10, decimal_places=2)
    item_qty = DecimalField(max_digits=6, decimal_places=2)
    item_discount = DecimalField(max_digits=4, decimal_places=2)
    item_count = IntegerField()

class Sellbill(BaseModel):    
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
    user = CharField(User, backref='sellbills')


class Rebuybill(BaseModel):    
    rebuy_date = DateField()
    rebuy_time = TimeField()
    buybill_id = IntegerField()
    detail_bill_id = IntegerField()
    import_bill_id = IntegerField()
    rebuy_item_name = CharField()
    rebuy_item_count = IntegerField()
    unit_price = DecimalField(max_digits=10, decimal_places=2)
    rebuy_totalG = DecimalField(max_digits=10, decimal_places=2)
    importer = CharField()
    rebuy_user_id = IntegerField()

class Resellbill(BaseModel):
    resell_date = DateField()
    resell_time = TimeField()
    resell_user = CharField()
    resell_totalG = DecimalField(max_digits=10, decimal_places=2)
    resell_item_count = IntegerField()

class Hodoor_Ensraf(BaseModel):    
    he_date = DateField()
    he_time = TimeField()
    he_employee = IntegerField()
    he_come = TimeField(null=True)
    he_go = TimeField(null=True)
    he_difference = TimeField(null=True)
    he_note = CharField(null=True)
    he_user = CharField(null=True)

db.connect()
db.create_tables([User, Customer, Importer, \
     Item, Company, Grp, Buybill, Sellbill, Rebuybill, \
     Resellbill, Hodoor_Ensraf])

