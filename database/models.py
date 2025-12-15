from tortoise import Model, fields

class Medicines(Model):
    id = fields.IntField(pk=True)
    trade_name = fields.TextField()
    mnn = fields.TextField()
    manufacturer = fields.TextField()
    form = fields.TextField()
    registration_number = fields.CharField(max_length=255)  
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    dispensing_mode = fields.TextField()
        