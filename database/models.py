from tortoise import Model, fields

class Medicines(Model):
    id = fields.IntField(pk=True)
    trade_name = fields.CharField(max_length=255)
    mnn = fields.CharField(max_length=255)
    manufacturer = fields.CharField(max_length=255)
    form = fields.CharField(max_length=750)
    registration_number = fields.CharField(max_length=255)  
    state = fields.CharField(max_length=255)
    dispensing_mode = fields.TextField()
    farm_group = fields.CharField(max_length=255)
    code_atx = fields.CharField(max_length=255)
    