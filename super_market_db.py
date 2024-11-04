from peewee import *

db = MySQLDatabase('market', user='root', password=str(""),
                   host='localhost', port=3306)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_fullname = CharField(unique=True)
    un_id = BigIntegerField(null=False)    
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
    customer_date = DateField()
    

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
    company_grp = ForeignKeyField(Grp, backref='companies', on_delete='CASCADE', on_update='CASCADE')

class Buybill(BaseModel):
    buy_date = DateField()
    buy_time = TimeField() 
    buy_item = CharField(unique=True, null=False) # اسم المنتج
    buy_item_qty = DecimalField(max_digits=10, decimal_places=2, null=False)
    buy_importer = ForeignKeyField(Importer, backref='buybills', null=False) # اسم المورد    
    buy_user = ForeignKeyField(User, null=False)
    buy_total_price = DecimalField(max_digits=10, decimal_places=2, null=False)
    buy_discount = DecimalField(max_digits=10, decimal_places=2, null=False)
    buy_item_count = IntegerField()  # عدد الفطع للفاتورة الواحدة

class Item(BaseModel):
    item_buybill_id = ForeignKeyField(Buybill) # رقم فاتورة المورد
    item_barcode = BigIntegerField(null=False)
    item_name = CharField(max_length= 100, null=False)
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
    

class Salebill(BaseModel):    
    date = DateField(null=False)
    time = TimeField(null=False)
    customer = ForeignKeyField(Customer, backref='salebills')
    bill_total = DecimalField(max_digits=10, decimal_places=2)
    discount = DecimalField(max_digits=10, decimal_places=2)  
    wanted = DecimalField(max_digits=10, decimal_places=2)
    cash = DecimalField(max_digits=10, decimal_places=2, null=False)
    cash_return = DecimalField(max_digits=10, decimal_places=2, null=False)
    visa = DecimalField(max_digits=10, decimal_places=2)    
    user = ForeignKeyField(User, backref='salebills')

class Salebill_details(BaseModel):
    bill_id = ForeignKeyField(Salebill, on_delete='CASCADE', on_update='CASCADE')
    item_barcode = BigIntegerField(null=False)
    item_name = CharField(max_length= 100, null=False)
    item_price = DecimalField(max_digits=10, decimal_places=2)
    item_qty = DecimalField(max_digits=6, decimal_places=2)
    item_discount = DecimalField(max_digits=4, decimal_places=2)
    total_price = DecimalField(max_digits=10, decimal_places=2)

 
class Rebuybill(BaseModel):    
    rebuy_date = DateField()
    rebuy_time = TimeField()    
    buybill_id = ForeignKeyField(Buybill, backref='rebuybills', on_update='CASCADE', on_delete='CASCADE')    
    rebuy_total_price = DecimalField(max_digits=10, decimal_places=2)
    importer = ForeignKeyField(Importer, backref='rebuybills')
    rebuy_user= ForeignKeyField(User, backref='rebuybills')

class Rebuybill_details(BaseModel):
    bill_id = ForeignKeyField(Rebuybill)
    rebuy_item_id = ForeignKeyField(Item, backref='rebuybills')
    rebuy_item_name = CharField(max_length=100)
    rebuy_item_qty = DecimalField(max_digits=6, decimal_places=2)
    unit_price = DecimalField(max_digits=10, decimal_places=2)

class Resalebill(BaseModel):
    resale_date = DateField()
    resale_time = TimeField()    
    salebill_id = ForeignKeyField(Salebill, backref='resalebills', on_update='CASCADE', on_delete='CASCADE')
    resale_total_price = DecimalField(max_digits=10, decimal_places=2)    
    resale_user= ForeignKeyField(User, backref='resalebills')

class Resalebill_details(BaseModel):
    resalebill_id = ForeignKeyField(Resalebill)
    resale_item_id = ForeignKeyField(Item, backref='resalebills')
    resale_item_name = CharField(max_length=100)
    resale_item_qty = DecimalField(max_digits=6, decimal_places=2)
    unit_price = DecimalField(max_digits=10, decimal_places=2)

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
db.create_tables([User, Customer, Importer, Grp, Company, Buybill, \
    Item, Buybill_details,Salebill, Salebill_details,Rebuybill, \
    Rebuybill_details, Resalebill, Resalebill_details, Hodoor_Ensraf])

